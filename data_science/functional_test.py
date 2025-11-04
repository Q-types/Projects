#!/usr/bin/env python3
"""
Functional Testing Suite for AI Domain Finder
Tests all core functionality with known test cases
"""

import sys
import time
from datetime import datetime
from ai_domain_finder import (
    SyllableCounter, 
    DomainChecker, 
    AIWordDomainFinder
)


class FunctionalTester:
    """Comprehensive functional testing."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        
    def assert_test(self, name, condition, actual=None, expected=None):
        """Assert a test condition."""
        if condition:
            print(f"  ✓ {name}")
            self.passed += 1
            return True
        else:
            print(f"  ✗ {name}")
            if actual is not None and expected is not None:
                print(f"    Expected: {expected}, Got: {actual}")
            self.failed += 1
            return False
    
    def warning(self, message):
        """Log a warning."""
        print(f"  ⚠ {message}")
        self.warnings += 1
    
    def print_section(self, title):
        """Print section header."""
        print(f"\n{'=' * 80}")
        print(f"{title}")
        print(f"{'=' * 80}\n")
    
    def test_syllable_counter(self):
        """Test syllable counting accuracy."""
        self.print_section("TEST 1: Syllable Counter")
        
        counter = SyllableCounter()
        
        test_cases = [
            # (word, expected_syllables)
            ('art', 1),
            ('blue', 1),
            ('bright', 1),
            ('cloud', 1),
            ('code', 1),
            ('edge', 1),
            ('fast', 1),
            ('glow', 1),
            ('help', 1),
            ('jump', 1),
            ('key', 1),
            ('light', 1),
            ('make', 1),
            ('next', 1),
            ('pure', 1),
            ('quick', 1),
            ('rise', 1),
            ('safe', 1),
            ('spark', 1),
            ('swift', 1),
            ('think', 1),
            ('use', 1),
            ('voice', 1),
            ('wave', 1),
            ('zone', 1),
            ('data', 2),
            ('logic', 2),
            ('vision', 2),
            ('focus', 2),
            ('simple', 2),
            ('magic', 2),
            ('neural', 2),
            ('pixel', 2),
            ('robot', 2),
            ('signal', 2),
            ('vector', 2),
        ]
        
        correct = 0
        total = len(test_cases)
        
        print("Testing syllable counts:\n")
        for word, expected in test_cases:
            actual = counter.count_syllables(word)
            if actual == expected:
                correct += 1
                status = "✓"
            else:
                status = "✗"
            print(f"{status} {word:12} -> Expected: {expected}, Got: {actual}")
        
        accuracy = (correct / total) * 100
        print(f"\nAccuracy: {correct}/{total} ({accuracy:.1f}%)")
        
        self.assert_test(
            "Syllable counter accuracy >= 80%",
            accuracy >= 80,
            f"{accuracy:.1f}%",
            ">= 80%"
        )
        
        if accuracy < 90:
            self.warning("Syllable accuracy below 90% - consider using 'syllables' library")
    
    def test_domain_checker_initialization(self):
        """Test DomainChecker initialization."""
        self.print_section("TEST 2: DomainChecker Initialization")
        
        try:
            checker = DomainChecker(max_price=100.0)
            self.assert_test("DomainChecker initialization", True)
            self.assert_test(
                "Max price set correctly",
                checker.max_price == 100.0,
                checker.max_price,
                100.0
            )
            self.assert_test(
                "Session initialized",
                hasattr(checker, 'session')
            )
        except Exception as e:
            self.assert_test(f"DomainChecker initialization - Error: {e}", False)
    
    def test_domain_price_estimates(self):
        """Test domain price estimation."""
        self.print_section("TEST 3: Domain Price Estimates")
        
        checker = DomainChecker(max_price=100.0)
        
        test_domains = [
            ('example.com', 12.99),
            ('example.ai', 89.99),
            ('example.net', 12.99),
            ('example.org', 12.99),
            ('example.io', 39.99),
        ]
        
        print("Testing price estimates:\n")
        for domain, expected_price in test_domains:
            price, error = checker.check_domain_price(domain)
            
            if price is not None:
                print(f"  {domain:20} -> ${price:.2f} (expected: ${expected_price:.2f})")
                self.assert_test(
                    f"{domain} price matches",
                    price == expected_price,
                    price,
                    expected_price
                )
            else:
                self.assert_test(f"{domain} price check - Error: {error}", False)
    
    def test_domain_availability_known_domains(self):
        """Test with domains known to be registered."""
        self.print_section("TEST 4: Domain Availability (Known Registered Domains)")
        
        checker = DomainChecker(max_price=100.0)
        
        # These are extremely well-known domains that should be registered
        known_registered = [
            'google.com',
            'facebook.com',
            'amazon.com',
            'microsoft.com',
        ]
        
        print("Testing known registered domains:\n")
        for domain in known_registered:
            print(f"  Checking {domain}...", end=" ")
            available, error = checker.check_availability_api(domain)
            
            if available is False:
                print("✓ Correctly identified as registered")
                self.passed += 1
            elif available is True:
                print("✗ Incorrectly identified as available")
                self.failed += 1
                self.warning(f"{domain} should be registered but was reported as available")
            else:
                print(f"⚠ Error: {error}")
                self.warning(f"Could not check {domain}: {error}")
            
            time.sleep(0.2)  # Be respectful
    
    def test_domain_checker_full_check(self):
        """Test full domain check including pricing."""
        self.print_section("TEST 5: Complete Domain Check")
        
        checker = DomainChecker(max_price=100.0)
        
        # Use a very unusual domain that's likely not registered
        test_domain = f"xyztest{int(time.time())}.com"
        
        print(f"Testing complete check for: {test_domain}\n")
        
        result = checker.check_domain(test_domain)
        
        self.assert_test("Result has 'domain' key", 'domain' in result)
        self.assert_test("Result has 'available' key", 'available' in result)
        self.assert_test("Result has 'price' key", 'price' in result)
        self.assert_test("Result has 'within_budget' key", 'within_budget' in result)
        self.assert_test("Result has 'checked_at' key", 'checked_at' in result)
        
        if result.get('available'):
            self.assert_test("Available domain has price", result.get('price') is not None)
            if result.get('price'):
                self.assert_test(
                    "Price is within budget",
                    result.get('price') <= 100.0
                )
    
    def test_ai_domain_finder_initialization(self):
        """Test AIWordDomainFinder initialization."""
        self.print_section("TEST 6: AIWordDomainFinder Initialization")
        
        try:
            finder = AIWordDomainFinder(
                max_syllables=2,
                max_price=100.0,
                max_workers=3
            )
            
            self.assert_test("AIWordDomainFinder initialization", True)
            self.assert_test("Max syllables set", finder.max_syllables == 2)
            self.assert_test("Max price set", finder.max_price == 100.0)
            self.assert_test("Max workers set", finder.max_workers == 3)
            self.assert_test("Syllable counter initialized", hasattr(finder, 'syllable_counter'))
            self.assert_test("Domain checker initialized", hasattr(finder, 'domain_checker'))
            
        except Exception as e:
            self.assert_test(f"AIWordDomainFinder initialization - Error: {e}", False)
    
    def test_word_loading(self):
        """Test English word loading."""
        self.print_section("TEST 7: English Word Loading")
        
        finder = AIWordDomainFinder(max_syllables=2, max_price=100.0)
        
        print("Loading English words...\n")
        words = finder.get_english_words()
        
        self.assert_test("Words loaded", len(words) > 0, len(words), "> 0")
        self.assert_test("Reasonable word count", len(words) >= 50)
        
        if len(words) < 1000:
            self.warning("Using small word list. Install NLTK for comprehensive results.")
        
        # Check word quality
        sample_words = words[:10]
        print(f"\nSample words: {', '.join(sample_words)}")
        
        all_alpha = all(w.isalpha() for w in sample_words)
        self.assert_test("All words are alphabetic", all_alpha)
        
        all_lowercase = all(w.islower() for w in sample_words)
        self.assert_test("All words are lowercase", all_lowercase)
    
    def test_syllable_filtering(self):
        """Test syllable-based word filtering."""
        self.print_section("TEST 8: Syllable Filtering")
        
        finder = AIWordDomainFinder(max_syllables=2, max_price=100.0)
        
        test_words = [
            'art', 'code', 'spark',  # 1 syllable
            'data', 'logic', 'vision',  # 2 syllables
            'computer', 'algorithm', 'analysis'  # 3+ syllables
        ]
        
        print("Testing syllable filtering:\n")
        filtered = finder.filter_by_syllables(test_words)
        
        print(f"\nFiltered words: {', '.join(filtered)}\n")
        
        # Should include 1-2 syllable words, exclude 3+
        expected_included = ['art', 'code', 'spark', 'data', 'logic', 'vision']
        expected_excluded = ['computer', 'algorithm', 'analysis']
        
        for word in expected_included:
            self.assert_test(
                f"'{word}' included (1-2 syllables)",
                word in filtered
            )
        
        for word in expected_excluded:
            self.assert_test(
                f"'{word}' excluded (3+ syllables)",
                word not in filtered
            )
    
    def test_domain_generation(self):
        """Test AI domain generation."""
        self.print_section("TEST 9: Domain Generation")
        
        finder = AIWordDomainFinder(max_syllables=2, max_price=100.0)
        
        test_words = ['spark', 'glow', 'data']
        
        print("Testing domain generation:\n")
        domains = finder.generate_ai_domains(test_words)
        
        self.assert_test("Generated correct number of domain pairs", len(domains) == 3)
        
        expected_results = [
            ('spark', 'sparkai.ai', 'sparkai.com'),
            ('glow', 'glowai.ai', 'glowai.com'),
            ('data', 'dataai.ai', 'dataai.com'),
        ]
        
        for i, (word, expected_ai, expected_com) in enumerate(expected_results):
            if i < len(domains):
                actual_word, actual_ai, actual_com = domains[i]
                print(f"  {word}: {actual_ai}, {actual_com}")
                self.assert_test(f"Word '{word}' correct", actual_word == word)
                self.assert_test(f".ai domain for '{word}' correct", actual_ai == expected_ai)
                self.assert_test(f".com domain for '{word}' correct", actual_com == expected_com)
    
    def test_live_domain_search(self):
        """Perform a small live domain search."""
        self.print_section("TEST 10: Live Domain Search (3 words)")
        
        finder = AIWordDomainFinder(max_syllables=1, max_price=100.0, max_workers=1)
        
        print("Performing live search with 3 words...\n")
        print("Note: This makes real network requests and may take time.\n")
        
        try:
            # Run with very small limit
            results = finder.find_domains(limit=3)
            
            self.assert_test("Search completed without error", True)
            self.assert_test("Results returned", results is not None)
            
            print(f"\nSearch returned {len(results) if results else 0} available domain pairs")
            
            if results and len(results) > 0:
                print("\nSample result:")
                sample = results[0]
                print(f"  Word: {sample['word']}")
                print(f"  {sample['ai_domain']['domain']}: ${sample['ai_domain']['price']:.2f}")
                print(f"  {sample['com_domain']['domain']}: ${sample['com_domain']['price']:.2f}")
                
        except Exception as e:
            self.assert_test(f"Live search - Error: {e}", False)
            self.warning("Network requests may be rate-limited or blocked")
    
    def print_summary(self):
        """Print test summary."""
        self.print_section("TEST SUMMARY")
        
        total_tests = self.passed + self.failed
        success_rate = (self.passed / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests:    {total_tests}")
        print(f"Passed:         {self.passed} ✓")
        print(f"Failed:         {self.failed} ✗")
        print(f"Warnings:       {self.warnings} ⚠")
        print(f"Success Rate:   {success_rate:.1f}%")
        print()
        
        if self.failed == 0:
            print("🎉 ALL TESTS PASSED!")
            print("\nThe AI Domain Finder tool is functioning correctly.")
        elif success_rate >= 80:
            print("⚠ MOSTLY PASSING - Some issues detected")
            print(f"\n{self.failed} test(s) failed. Review failures above.")
        else:
            print("❌ SIGNIFICANT ISSUES DETECTED")
            print(f"\n{self.failed} test(s) failed. Tool may need debugging.")
        
        if self.warnings > 0:
            print(f"\n⚠ {self.warnings} warning(s) - See details above")
        
        print()
        print("=" * 80)
        
        return self.failed == 0


def main():
    """Run all functional tests."""
    print("\n" + "=" * 80)
    print("AI DOMAIN FINDER - COMPREHENSIVE FUNCTIONAL TEST SUITE")
    print("=" * 80)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    tester = FunctionalTester()
    
    # Run all tests
    tester.test_syllable_counter()
    tester.test_domain_checker_initialization()
    tester.test_domain_price_estimates()
    tester.test_domain_availability_known_domains()
    tester.test_domain_checker_full_check()
    tester.test_ai_domain_finder_initialization()
    tester.test_word_loading()
    tester.test_syllable_filtering()
    tester.test_domain_generation()
    
    # Ask before live search
    print("\n" + "=" * 80)
    response = input("Run live domain search test (makes network requests)? (y/n): ")
    if response.lower() == 'y':
        tester.test_live_domain_search()
    else:
        print("\nSkipped live search test.")
    
    # Print summary
    all_passed = tester.print_summary()
    
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80 + "\n")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
