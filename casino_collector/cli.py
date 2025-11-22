#!/usr/bin/env python3
"""
Casino Intelligence Collector - Command Line Interface

An end-to-end system for gathering structured data about online casinos.
"""
import argparse
import sys
from pathlib import Path
from typing import List
import time

from casino_collector.models import CasinoData
from casino_collector.scrapers import GenericCasinoScraper
from casino_collector.storage import DataStorage
from casino_collector.config import Config
from casino_collector.utils import setup_logging, validate_url, format_duration, extract_urls


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Casino Intelligence Collector - Gather structured data about online casinos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scrape a single casino
  python -m casino_collector.cli --url https://example-casino.com
  
  # Scrape multiple casinos from a file
  python -m casino_collector.cli --file casinos.txt
  
  # Paste a list of casino URLs directly
  python -m casino_collector.cli --list "https://casino1.com
  https://casino2.com
  https://casino3.com"
  
  # Use custom config
  python -m casino_collector.cli --config config.json --url https://example-casino.com
  
  # Set output directory
  python -m casino_collector.cli --url https://example-casino.com --output ./data
        """
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '-u', '--url',
        help='Single casino URL to scrape'
    )
    input_group.add_argument(
        '-f', '--file',
        help='File containing list of casino URLs (one per line, or mixed with text)'
    )
    input_group.add_argument(
        '-l', '--list',
        help='Multi-line list of casino URLs or text containing URLs (paste directly)'
    )
    input_group.add_argument(
        '--config',
        help='Path to configuration file (JSON)'
    )
    
    # Output options
    parser.add_argument(
        '-o', '--output',
        default='output',
        help='Output directory for results (default: output)'
    )
    parser.add_argument(
        '--no-json',
        action='store_true',
        help='Skip JSON output'
    )
    parser.add_argument(
        '--no-csv',
        action='store_true',
        help='Skip CSV output'
    )
    parser.add_argument(
        '--no-summary',
        action='store_true',
        help='Skip summary report generation'
    )
    
    # Scraper options
    parser.add_argument(
        '--delay-min',
        type=float,
        default=1.0,
        help='Minimum delay between requests in seconds (default: 1.0)'
    )
    parser.add_argument(
        '--delay-max',
        type=float,
        default=3.0,
        help='Maximum delay between requests in seconds (default: 3.0)'
    )
    
    # Logging options
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default='INFO',
        help='Logging level (default: INFO)'
    )
    parser.add_argument(
        '--log-file',
        help='Path to log file (default: logs/casino_collector.log)'
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress console output (only log to file)'
    )
    
    # Other options
    parser.add_argument(
        '--version',
        action='version',
        version='Casino Intelligence Collector 1.0.0'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    log_file = args.log_file or 'logs/casino_collector.log'
    if not args.quiet:
        setup_logging(level=args.log_level, log_file=log_file)
    else:
        setup_logging(level=args.log_level, log_file=log_file)
    
    # Load configuration
    config = None
    if args.config:
        try:
            config = Config.load_from_file(args.config)
            urls = config.target_urls
        except Exception as e:
            print(f"Error loading config file: {e}")
            sys.exit(1)
    else:
        # Build URL list from arguments
        urls = []
        if args.url:
            urls = [args.url]
        elif args.file:
            try:
                with open(args.file, 'r') as f:
                    file_content = f.read()
                # Extract URLs from file content (handles mixed text)
                urls = extract_urls(file_content)
                if not urls:
                    # Fallback to line-by-line reading for backward compatibility
                    urls = [line.strip() for line in file_content.split('\n') 
                           if line.strip() and not line.startswith('#')]
            except FileNotFoundError:
                print(f"Error: File not found: {args.file}")
                sys.exit(1)
        elif args.list:
            # Extract URLs from pasted list
            urls = extract_urls(args.list)
    
    # Validate URLs
    valid_urls = []
    for url in urls:
        if validate_url(url):
            valid_urls.append(url)
        else:
            print(f"Warning: Invalid URL skipped: {url}")
    
    if not valid_urls:
        print("Error: No valid URLs to scrape")
        sys.exit(1)
    
    print("=" * 80)
    print("CASINO INTELLIGENCE COLLECTOR")
    print("=" * 80)
    print(f"URLs to scrape: {len(valid_urls)}")
    print(f"Output directory: {args.output}")
    print(f"Delay range: {args.delay_min}s - {args.delay_max}s")
    print("=" * 80)
    print()
    
    # Initialize scraper and storage
    scraper = GenericCasinoScraper(delay_range=(args.delay_min, args.delay_max))
    storage = DataStorage(output_dir=args.output)
    
    # Scrape casinos
    collected_data: List[CasinoData] = []
    start_time = time.time()
    
    for i, url in enumerate(valid_urls, 1):
        print(f"[{i}/{len(valid_urls)}] Scraping: {url}")
        
        try:
            casino_data = scraper.scrape(url)
            
            if casino_data:
                collected_data.append(casino_data)
                print(f"  ✓ Success - {casino_data.name} (completeness: {casino_data.data_completeness_score:.1f}%)")
                print(f"    - Licenses: {len(casino_data.licenses)}")
                print(f"    - Providers: {len(casino_data.providers)}")
                print(f"    - Withdrawal methods: {len(casino_data.withdrawal_methods)}")
            else:
                print(f"  ✗ Failed to scrape {url}")
        
        except Exception as e:
            print(f"  ✗ Error scraping {url}: {e}")
        
        # Add delay between requests (except for last one)
        if i < len(valid_urls):
            scraper.random_delay()
        
        print()
    
    elapsed_time = time.time() - start_time
    
    # Save results
    print("=" * 80)
    print("SAVING RESULTS")
    print("=" * 80)
    
    if collected_data:
        if not args.no_json:
            json_path = storage.save_json(collected_data)
            print(f"✓ JSON saved to: {json_path}")
        
        if not args.no_csv:
            csv_path = storage.save_csv(collected_data)
            print(f"✓ CSV saved to: {csv_path}")
        
        if not args.no_summary:
            summary_path = storage.generate_summary_report(collected_data)
            print(f"✓ Summary report saved to: {summary_path}")
    else:
        print("No data collected to save")
    
    # Final summary
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total URLs processed: {len(valid_urls)}")
    print(f"Successfully scraped: {len(collected_data)}")
    print(f"Failed: {len(valid_urls) - len(collected_data)}")
    print(f"Total time: {format_duration(elapsed_time)}")
    
    if collected_data:
        avg_completeness = sum([c.data_completeness_score or 0 for c in collected_data]) / len(collected_data)
        print(f"Average data completeness: {avg_completeness:.1f}%")
    
    print("=" * 80)
    
    return 0 if collected_data else 1


if __name__ == '__main__':
    sys.exit(main())
