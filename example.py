#!/usr/bin/env python3
"""
Example script demonstrating how to use the Casino Intelligence Collector programmatically.
"""
from casino_collector.scrapers import GenericCasinoScraper
from casino_collector.storage import DataStorage
from casino_collector.utils import setup_logging

def main():
    # Setup logging
    setup_logging(level="INFO")
    
    # List of casino URLs to scrape
    casino_urls = [
        "https://www.example-casino1.com",
        "https://www.example-casino2.com",
    ]
    
    # Initialize scraper and storage
    scraper = GenericCasinoScraper(delay_range=(1, 2))
    storage = DataStorage(output_dir="example_output")
    
    # Collect data
    collected_data = []
    
    print("Starting casino data collection...")
    print("=" * 80)
    
    for url in casino_urls:
        print(f"\nScraping: {url}")
        
        try:
            casino_data = scraper.scrape(url)
            
            if casino_data:
                collected_data.append(casino_data)
                
                print(f"✓ Successfully scraped: {casino_data.name}")
                print(f"  Completeness: {casino_data.data_completeness_score:.1f}%")
                print(f"  Licenses: {len(casino_data.licenses)}")
                print(f"  Providers: {len(casino_data.providers)}")
                print(f"  Withdrawal methods: {len(casino_data.withdrawal_methods)}")
                
                # Access specific data
                if casino_data.licenses:
                    print(f"  Primary license: {casino_data.licenses[0].authority}")
                
                if casino_data.security:
                    print(f"  SSL: {casino_data.security.ssl_certificate}")
                    if casino_data.security.encryption_type:
                        print(f"  Encryption: {casino_data.security.encryption_type}")
            else:
                print(f"✗ Failed to scrape: {url}")
                
        except Exception as e:
            print(f"✗ Error: {e}")
        
        # Be respectful - add delay
        scraper.random_delay()
    
    print("\n" + "=" * 80)
    print(f"Collection complete! Scraped {len(collected_data)} casinos")
    
    # Save results
    if collected_data:
        print("\nSaving results...")
        
        json_path = storage.save_json(collected_data)
        print(f"✓ JSON saved to: {json_path}")
        
        csv_path = storage.save_csv(collected_data)
        print(f"✓ CSV saved to: {csv_path}")
        
        summary_path = storage.generate_summary_report(collected_data)
        print(f"✓ Summary saved to: {summary_path}")
        
        # Calculate statistics
        avg_completeness = sum([c.data_completeness_score or 0 for c in collected_data]) / len(collected_data)
        total_licenses = sum([len(c.licenses) for c in collected_data])
        total_providers = sum([len(c.providers) for c in collected_data])
        
        print("\nStatistics:")
        print(f"  Average completeness: {avg_completeness:.1f}%")
        print(f"  Total licenses found: {total_licenses}")
        print(f"  Total provider relationships: {total_providers}")
    else:
        print("\nNo data collected")
    
    print("=" * 80)

if __name__ == "__main__":
    main()
