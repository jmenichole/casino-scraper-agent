#!/usr/bin/env python3
"""
Example demonstrating the copy-paste feature for casino lists.

This shows how you can paste casino URLs with mixed content
and the tool will automatically extract valid URLs.
"""
from casino_collector.utils import extract_urls

# Example 1: Clean list of URLs
print("=" * 80)
print("Example 1: Clean list of URLs")
print("=" * 80)

clean_list = """
https://www.example-casino1.com
https://www.example-casino2.com
https://www.example-casino3.com
"""

urls = extract_urls(clean_list)
print(f"Extracted {len(urls)} URLs:")
for url in urls:
    print(f"  - {url}")
print()

# Example 2: List with descriptions and comments
print("=" * 80)
print("Example 2: List with descriptions and mixed content")
print("=" * 80)

mixed_list = """
My favorite online casinos:

https://www.casino1.com - Great welcome bonus!
https://www.casino2.com/?ref=abc123 - Fast withdrawals
Some random text here
https://www.casino3.com - Best slots selection

Check out https://www.casino4.com for live dealer games
"""

urls = extract_urls(mixed_list)
print(f"Extracted {len(urls)} URLs:")
for url in urls:
    print(f"  - {url}")
print()

# Example 3: Affiliate links (like casinoslist.md)
print("=" * 80)
print("Example 3: Affiliate links with referral codes")
print("=" * 80)

affiliate_list = """
Affiliate links:
https://www.hellomillions.com/lp/raf?r=26d6760f%2F1236643867
https://www.spinblitz.com/lp/raf?r=606f64a3%2F1246446739
https://www.megabonanza.com/?r=72781897
"""

urls = extract_urls(affiliate_list)
print(f"Extracted {len(urls)} URLs:")
for url in urls:
    print(f"  - {url}")
print()

# Example 4: How to use with CLI
print("=" * 80)
print("How to use with the CLI:")
print("=" * 80)
print()
print("Method 1 - Direct paste:")
print('python -m casino_collector.cli --list "https://casino1.com')
print('https://casino2.com"')
print()
print("Method 2 - From a file with mixed content:")
print("python -m casino_collector.cli --file casinoslist.md")
print()
print("Method 3 - Traditional (still works):")
print("python -m casino_collector.cli --url https://casino.com")
print()
print("=" * 80)
