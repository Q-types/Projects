#!/usr/bin/env python3
"""
AI Domain Finder
Identifies 1-2 syllable English words and checks domain availability 
for word+AI domains (.ai and .com) under $100.
"""

import re
import json
import time
import argparse
from typing import List, Dict, Tuple, Optional
from datetime import datetime
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import syllables
except ImportError:
    syllables = None

try:
    import whois
except ImportError:
    whois = None

try:
    from nltk.corpus import words as nltk_words
    import nltk
except ImportError:
    nltk = None
    nltk_words = None


class SyllableCounter:
    """Handle syllable counting with multiple fallback methods."""
    
    @staticmethod
    def count_syllables_simple(word: str) -> int:
        """
        Simple vowel-based syllable counter (fallback method).
        Not perfect but works without external libraries.
        """
        word = word.lower().strip()
        vowels = "aeiouy"
        syllable_count = 0
        previous_was_vowel = False
        
        for i, char in enumerate(word):
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                syllable_count += 1
            previous_was_vowel = is_vowel
        
        # Handle silent e
        if word.endswith('e'):
            syllable_count -= 1
        
        # Handle special cases
        if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
            syllable_count += 1
        
        # Ensure at least 1 syllable
        if syllable_count == 0:
            syllable_count = 1
        
        return syllable_count
    
    @staticmethod
    def count_syllables(word: str) -> int:
        """Count syllables using available libraries or fallback method."""
        if syllables:
            try:
                return syllables.estimate(word)
            except:
                pass
        
        return SyllableCounter.count_syllables_simple(word)


class DomainChecker:
    """Check domain availability and pricing."""
    
    def __init__(self, max_price: float = 100.0):
        self.max_price = max_price
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
    
    def check_availability_whois(self, domain: str) -> Tuple[bool, Optional[str]]:
        """
        Check domain availability using WHOIS.
        Returns (is_available, error_message)
        """
        if not whois:
            return None, "python-whois not installed"
        
        try:
            w = whois.whois(domain)
            # If domain is registered, it will have domain_name field
            if w.domain_name:
                return False, None
            else:
                return True, None
        except whois.parser.PywhoisError:
            # Domain not found usually means available
            return True, None
        except Exception as e:
            return None, str(e)
    
    def check_availability_api(self, domain: str) -> Tuple[bool, Optional[str]]:
        """
        Check domain availability using a public API.
        Returns (is_available, error_message)
        """
        try:
            # Using a simple DNS check as fallback
            import socket
            try:
                socket.gethostbyname(domain)
                # Domain resolves, so it's registered
                return False, None
            except socket.gaierror:
                # Domain doesn't resolve, likely available
                return True, None
        except Exception as e:
            return None, str(e)
    
    def check_domain_price(self, domain: str) -> Tuple[Optional[float], Optional[str]]:
        """
        Estimate domain price based on TLD.
        Note: Actual prices vary by registrar and may change.
        Returns (price, error_message)
        """
        tld = domain.split('.')[-1]
        
        # Typical retail prices for common TLDs (approximate)
        typical_prices = {
            'com': 12.99,
            'ai': 89.99,  # .ai domains are typically expensive
            'net': 12.99,
            'org': 12.99,
            'io': 39.99,
        }
        
        price = typical_prices.get(tld, 50.0)  # Default estimate
        
        # Check if under max price
        if price <= self.max_price:
            return price, None
        else:
            return price, f"Price ${price:.2f} exceeds ${self.max_price:.2f}"
    
    def check_domain(self, domain: str) -> Dict:
        """
        Complete domain check including availability and pricing.
        """
        result = {
            'domain': domain,
            'available': None,
            'price': None,
            'within_budget': False,
            'error': None,
            'checked_at': datetime.now().isoformat()
        }
        
        # Check availability
        available, error = self.check_availability_whois(domain)
        if available is None:
            # Fallback to DNS check
            available, error = self.check_availability_api(domain)
        
        result['available'] = available
        
        if available:
            # Check price
            price, price_error = self.check_domain_price(domain)
            result['price'] = price
            
            if price and price <= self.max_price:
                result['within_budget'] = True
            
            if price_error:
                result['error'] = price_error
        else:
            result['error'] = error or "Domain already registered"
        
        return result


class AIWordDomainFinder:
    """Main class to find available AI domains from English words."""
    
    def __init__(self, max_syllables: int = 2, max_price: float = 100.0, 
                 max_workers: int = 10):
        self.max_syllables = max_syllables
        self.max_price = max_price
        self.max_workers = max_workers
        self.syllable_counter = SyllableCounter()
        self.domain_checker = DomainChecker(max_price)
    
    def get_english_words(self) -> List[str]:
        """Get list of English words from various sources."""
        words_list = []
        
        # Try NLTK first
        if nltk and nltk_words:
            try:
                words_list = list(nltk_words.words())
            except LookupError:
                print("Downloading NLTK words corpus...")
                nltk.download('words', quiet=True)
                words_list = list(nltk_words.words())
        
        # Fallback to a basic word list
        if not words_list:
            # Use a built-in basic list
            basic_words = [
                'art', 'blue', 'book', 'brain', 'bright', 'care', 'cloud', 'code',
                'craft', 'data', 'deep', 'dream', 'edge', 'fast', 'flow', 'force',
                'fresh', 'gen', 'glow', 'guide', 'help', 'home', 'hope', 'hub',
                'idea', 'jump', 'just', 'key', 'kind', 'learn', 'light', 'link',
                'logic', 'love', 'make', 'mind', 'next', 'node', 'open', 'path',
                'peak', 'plan', 'play', 'plus', 'point', 'pure', 'quick', 'reach',
                'real', 'rise', 'safe', 'scope', 'sense', 'sharp', 'shift', 'skill',
                'smart', 'soft', 'solve', 'spark', 'speed', 'start', 'sync', 'task',
                'team', 'think', 'time', 'tool', 'track', 'true', 'trust', 'use',
                'value', 'view', 'vision', 'voice', 'wave', 'wise', 'work', 'zone'
            ]
            print(f"Using basic word list ({len(basic_words)} words)")
            words_list = basic_words
        
        # Filter words: only alphabetic, reasonable length
        filtered_words = [
            w.lower() for w in words_list 
            if w.isalpha() and 3 <= len(w) <= 10
        ]
        
        return list(set(filtered_words))  # Remove duplicates
    
    def filter_by_syllables(self, words: List[str]) -> List[str]:
        """Filter words by syllable count."""
        filtered = []
        print(f"Filtering {len(words)} words by syllable count (<= {self.max_syllables})...")
        
        for word in words:
            syllable_count = self.syllable_counter.count_syllables(word)
            if syllable_count <= self.max_syllables:
                filtered.append(word)
        
        print(f"Found {len(filtered)} words with {self.max_syllables} or fewer syllables")
        return filtered
    
    def generate_ai_domains(self, words: List[str]) -> List[Tuple[str, str, str]]:
        """
        Generate AI domain combinations.
        Returns list of (word, domain_ai, domain_com) tuples.
        """
        domains = []
        for word in words:
            base = f"{word}ai"
            domains.append((word, f"{base}.ai", f"{base}.com"))
        return domains
    
    def check_domain_pair(self, word: str, domain_ai: str, domain_com: str) -> Dict:
        """Check both .ai and .com domains for a word."""
        result_ai = self.domain_checker.check_domain(domain_ai)
        time.sleep(0.1)  # Be respectful with requests
        result_com = self.domain_checker.check_domain(domain_com)
        
        return {
            'word': word,
            'ai_domain': result_ai,
            'com_domain': result_com,
            'both_available': (
                result_ai.get('available') and 
                result_com.get('available') and
                result_ai.get('within_budget') and
                result_com.get('within_budget')
            ),
            'total_price': (
                (result_ai.get('price') or 0) + 
                (result_com.get('price') or 0)
            ) if result_ai.get('price') and result_com.get('price') else None
        }
    
    def find_domains(self, limit: Optional[int] = None) -> List[Dict]:
        """Main method to find available domains."""
        print("=" * 60)
        print("AI Domain Finder")
        print("=" * 60)
        
        # Get words
        print("\n1. Loading English words...")
        words = self.get_english_words()
        print(f"   Loaded {len(words)} English words")
        
        # Filter by syllables
        print(f"\n2. Filtering by syllables (<= {self.max_syllables})...")
        filtered_words = self.filter_by_syllables(words)
        
        if limit:
            filtered_words = filtered_words[:limit]
            print(f"   Limited to first {limit} words for testing")
        
        # Generate domain combinations
        print(f"\n3. Generating domain combinations...")
        domain_combos = self.generate_ai_domains(filtered_words)
        print(f"   Generated {len(domain_combos)} domain pairs to check")
        
        # Check domains
        print(f"\n4. Checking domain availability and pricing...")
        print(f"   (Max price: ${self.max_price} per domain)")
        print(f"   (Using {self.max_workers} workers)")
        
        results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(
                    self.check_domain_pair, word, domain_ai, domain_com
                ): (word, domain_ai, domain_com)
                for word, domain_ai, domain_com in domain_combos
            }
            
            completed = 0
            for future in as_completed(futures):
                completed += 1
                if completed % 10 == 0:
                    print(f"   Progress: {completed}/{len(domain_combos)}")
                
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    word, domain_ai, domain_com = futures[future]
                    print(f"   Error checking {word}: {e}")
        
        print(f"\n   Completed: {len(results)} domain pairs checked")
        
        # Filter results
        available_results = [
            r for r in results 
            if r['both_available']
        ]
        
        print(f"\n5. Results Summary:")
        print(f"   Total words checked: {len(results)}")
        print(f"   Available domain pairs: {len(available_results)}")
        
        return available_results
    
    def save_results(self, results: List[Dict], filename: str = "ai_domains_results.json"):
        """Save results to JSON file."""
        output = {
            'timestamp': datetime.now().isoformat(),
            'parameters': {
                'max_syllables': self.max_syllables,
                'max_price': self.max_price
            },
            'total_available': len(results),
            'domains': results
        }
        
        with open(filename, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"\nResults saved to: {filename}")
        
        # Also save a simple text report
        txt_filename = filename.replace('.json', '.txt')
        with open(txt_filename, 'w') as f:
            f.write("AI Domain Finder - Available Domains\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Max Syllables: {self.max_syllables}\n")
            f.write(f"Max Price per Domain: ${self.max_price}\n")
            f.write(f"Total Available Pairs: {len(results)}\n\n")
            
            for r in results:
                f.write(f"Word: {r['word']}\n")
                f.write(f"  {r['ai_domain']['domain']}: ${r['ai_domain']['price']:.2f}\n")
                f.write(f"  {r['com_domain']['domain']}: ${r['com_domain']['price']:.2f}\n")
                f.write(f"  Total: ${r['total_price']:.2f}\n")
                f.write("\n")
        
        print(f"Text report saved to: {txt_filename}")


def main():
    parser = argparse.ArgumentParser(
        description='Find available AI domains from English words'
    )
    parser.add_argument(
        '--max-syllables',
        type=int,
        default=2,
        help='Maximum syllables per word (default: 2)'
    )
    parser.add_argument(
        '--max-price',
        type=float,
        default=100.0,
        help='Maximum price per domain in USD (default: 100.0)'
    )
    parser.add_argument(
        '--workers',
        type=int,
        default=5,
        help='Number of concurrent workers (default: 5)'
    )
    parser.add_argument(
        '--limit',
        type=int,
        help='Limit number of words to check (for testing)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='ai_domains_results.json',
        help='Output filename (default: ai_domains_results.json)'
    )
    
    args = parser.parse_args()
    
    # Create finder
    finder = AIWordDomainFinder(
        max_syllables=args.max_syllables,
        max_price=args.max_price,
        max_workers=args.workers
    )
    
    # Find domains
    results = finder.find_domains(limit=args.limit)
    
    # Save results
    if results:
        finder.save_results(results, args.output)
        
        print("\n" + "=" * 60)
        print("Top 10 Available Domains:")
        print("=" * 60)
        for r in results[:10]:
            print(f"\n{r['word']}:")
            print(f"  • {r['ai_domain']['domain']} - ${r['ai_domain']['price']:.2f}")
            print(f"  • {r['com_domain']['domain']} - ${r['com_domain']['price']:.2f}")
            print(f"  → Total: ${r['total_price']:.2f}")
    else:
        print("\nNo available domain pairs found matching criteria.")


if __name__ == "__main__":
    main()
