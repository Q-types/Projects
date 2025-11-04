#!/usr/bin/env python3
"""
Quick test script for AI Domain Finder
Tests with a small sample of words to verify functionality
"""

from ai_domain_finder import AIWordDomainFinder, SyllableCounter

def test_syllable_counting():
    """Test syllable counting functionality."""
    print("=" * 60)
    print("Testing Syllable Counter")
    print("=" * 60)
    
    counter = SyllableCounter()
    test_words = [
        ('art', 1),
        ('code', 1),
        ('bright', 1),
        ('cloud', 1),
        ('data', 2),
        ('vision', 2),
        ('logic', 2),
        ('computer', 3),
        ('algorithm', 4),
    ]
    
    print("\nWord → Expected Syllables → Counted Syllables")
    print("-" * 60)
    
    for word, expected in test_words:
        counted = counter.count_syllables(word)
        status = "✓" if counted == expected else "✗"
        print(f"{status} {word:12} → {expected:2} → {counted:2}")
    
    print()


def test_domain_finder_small():
    """Test domain finder with a small sample."""
    print("=" * 60)
    print("Testing Domain Finder (Small Sample)")
    print("=" * 60)
    print("\nThis will check 20 words as a quick test...\n")
    
    # Create finder with test settings
    finder = AIWordDomainFinder(
        max_syllables=2,
        max_price=100.0,
        max_workers=3  # Use fewer workers for testing
    )
    
    # Run with limit
    results = finder.find_domains(limit=20)
    
    # Display results
    if results:
        print(f"\nFound {len(results)} available domain pairs!")
        print("\nFirst 5 results:")
        for r in results[:5]:
            print(f"\n  {r['word']}:")
            print(f"    • {r['ai_domain']['domain']}: ${r['ai_domain']['price']:.2f}")
            print(f"    • {r['com_domain']['domain']}: ${r['com_domain']['price']:.2f}")
            print(f"    → Total: ${r['total_price']:.2f}")
    else:
        print("\nNo available domains found in this sample.")
        print("This is normal - try running with more words!")


def test_custom_words():
    """Test with a specific list of custom words."""
    print("\n" + "=" * 60)
    print("Testing Custom Word List")
    print("=" * 60)
    
    from ai_domain_finder import DomainChecker, SyllableCounter
    
    custom_words = [
        'spark', 'glow', 'rise', 'flow', 'edge',
        'swift', 'bright', 'quick', 'smart', 'pure'
    ]
    
    counter = SyllableCounter()
    checker = DomainChecker(max_price=100.0)
    
    print(f"\nChecking {len(custom_words)} custom words...\n")
    
    for word in custom_words:
        syllables = counter.count_syllables(word)
        if syllables <= 2:
            domain_ai = f"{word}ai.ai"
            domain_com = f"{word}ai.com"
            
            print(f"{word} ({syllables} syllable{'s' if syllables > 1 else ''}):")
            print(f"  → {domain_ai}")
            print(f"  → {domain_com}")
            print()


if __name__ == "__main__":
    print("\n🔍 AI Domain Finder - Test Suite\n")
    
    # Run tests
    test_syllable_counting()
    print("\n")
    
    test_custom_words()
    print("\n")
    
    # Ask before running full domain check
    response = input("Run domain availability test? (y/n): ")
    if response.lower() == 'y':
        test_domain_finder_small()
    else:
        print("\nSkipped domain check. To run manually:")
        print("  python ai_domain_finder.py --limit 20")
    
    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)
    print("\nTo run the full domain finder:")
    print("  python ai_domain_finder.py --limit 100")
    print("\nFor help:")
    print("  python ai_domain_finder.py --help")
    print()
