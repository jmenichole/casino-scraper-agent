# Casino Intelligence Collector - Quick Start Guide

## Installation

```bash
# Clone the repository
git clone https://github.com/jmenichole/casino-scraper-agent.git
cd casino-scraper-agent

# Install dependencies
pip install -r requirements.txt

# Or install as a package
pip install -e .
```

## Quick Usage

### 1. Run the Demo
See the system in action with sample data:

```bash
python demo.py
```

This creates sample casino data and saves it to `demo_output/` directory.

### 2. Scrape a Single Casino

```bash
python -m casino_collector.cli --url https://example-casino.com
```

### 3. Scrape Multiple Casinos

Create a file `casinos.txt` with URLs (one per line):
```
https://casino1.com
https://casino2.com
https://casino3.com
```

Then run:
```bash
python -m casino_collector.cli --file casinos.txt
```

**NEW:** Files can now contain mixed content! The tool automatically extracts URLs from text:
```
My casino list:
https://casino1.com - Great bonuses
https://casino2.com
```

### 3b. Copy-Paste Casino Lists (NEW!)

No need to create a file! Paste your casino list directly:
```bash
python -m casino_collector.cli --list "https://casino1.com
https://casino2.com
https://casino3.com"
```

Works with mixed content too:
```bash
python -m casino_collector.cli --list "Check out:
https://casino1.com - best odds
https://casino2.com"
```

### 4. Use Configuration File

Copy and edit the example config:
```bash
cp config.example.json config.json
# Edit config.json with your settings
python -m casino_collector.cli --config config.json
```

### 5. Programmatic Usage

See `example.py` for how to use the collector in your own Python code:

```python
from casino_collector.scrapers import GenericCasinoScraper
from casino_collector.storage import DataStorage

scraper = GenericCasinoScraper()
storage = DataStorage()

# Scrape a casino
casino_data = scraper.scrape("https://example-casino.com")

# Save results
if casino_data:
    storage.save_json([casino_data])
    storage.save_csv([casino_data])
```

## Output Files

All outputs are saved to the `output/` directory (or custom directory specified with `-o`):

- **JSON**: Full structured data with all fields
- **CSV**: Flattened data for spreadsheet analysis
- **Summary**: Human-readable text report

## Data Collected

The system collects 7 categories of casino information:

1. **Licenses**: Licensing authorities, jurisdictions, verification
2. **RTP**: Return to Player percentages for games
3. **Fairness**: Independent testing and certifications
4. **Providers**: Game providers and their portfolios
5. **Security**: SSL, encryption, 2FA, responsible gambling tools
6. **Withdrawals**: Payment methods, limits, processing times
7. **Reviews**: Ratings and reviews from various sources

## Common Options

```bash
# Change output directory
python -m casino_collector.cli --url URL --output ./my_data

# Copy-paste a list of casinos
python -m casino_collector.cli --list "https://casino1.com
https://casino2.com"

# Adjust scraping delays (be more respectful)
python -m casino_collector.cli --file casinos.txt --delay-min 2 --delay-max 5

# Save only JSON
python -m casino_collector.cli --url URL --no-csv --no-summary

# Debug mode
python -m casino_collector.cli --url URL --log-level DEBUG

# Quiet mode (log to file only)
python -m casino_collector.cli --url URL --quiet
```

## Best Practices

1. **Respect robots.txt**: Always check before scraping
2. **Use appropriate delays**: Default is 1-3 seconds
3. **Monitor resources**: Watch memory when scraping many sites
4. **Validate data**: Review collected data for accuracy
5. **Legal compliance**: Ensure you have permission to scrape

## Troubleshooting

**No data collected?**
- Check if the URL is accessible
- Verify website structure hasn't changed
- Try increasing timeout with `--delay-max`

**Low completeness scores?**
- Some data may not be available on all sites
- Consider creating site-specific scrapers

**Request errors?**
- Website may be blocking automated requests
- Try increasing delays between requests
- Check your internet connection

## Need Help?

- See full documentation: `README.md`
- Check examples: `demo.py` and `example.py`
- Review config: `config.example.json`

## License & Disclaimer

This tool is for research and educational purposes only. Users are responsible for complying with target websites' terms of service and applicable laws.
