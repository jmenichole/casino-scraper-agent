# Casino Intelligence Collector

An end-to-end system for automatically gathering structured data about online casinos. This tool collects comprehensive information including licensing, RTP (Return to Player), fairness certifications, game providers, security measures, withdrawal methods, and reviews.

## Features

- **Comprehensive Data Collection**: Gathers 7+ categories of casino information
  - Licensing information (authority, jurisdiction, verification)
  - RTP (Return to Player) percentages
  - Fairness certifications (eCOGRA, iTech Labs, etc.)
  - Game providers (NetEnt, Microgaming, etc.)
  - Security measures (SSL, encryption, 2FA)
  - Withdrawal methods and policies
  - Reviews and ratings

- **Multiple Output Formats**:
  - JSON (detailed structured data)
  - CSV (flattened for analysis)
  - Text summary reports

- **Configurable & Extensible**:
  - JSON-based configuration
  - Environment variable support
  - Customizable scraping delays
  - Extensible scraper architecture

- **Respectful Scraping**:
  - Configurable delays between requests
  - User-agent rotation
  - Error handling and retry logic

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/jmenichole/casino-scraper-agent.git
cd casino-scraper-agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### Scrape a Single Casino

```bash
python -m casino_collector.cli --url https://example-casino.com
```

### Scrape Multiple Casinos from a File

1. Create a text file with casino URLs (one per line):
```text
https://casino1.com
https://casino2.com
https://casino3.com
```

2. Run the scraper:
```bash
python -m casino_collector.cli --file casinos.txt
```

### Use a Configuration File

1. Copy the example config:
```bash
cp config.example.json config.json
```

2. Edit `config.json` with your settings and target URLs

3. Run with the config:
```bash
python -m casino_collector.cli --config config.json
```

## Usage

### Command Line Options

```
usage: python -m casino_collector.cli [-h] (-u URL | -f FILE | --config CONFIG)
                                       [-o OUTPUT] [--no-json] [--no-csv]
                                       [--no-summary] [--delay-min DELAY_MIN]
                                       [--delay-max DELAY_MAX]
                                       [--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                                       [--log-file LOG_FILE] [--quiet] [--version]

Options:
  -h, --help            Show this help message and exit
  -u URL, --url URL     Single casino URL to scrape
  -f FILE, --file FILE  File containing list of casino URLs (one per line)
  --config CONFIG       Path to configuration file (JSON)
  -o OUTPUT, --output OUTPUT
                        Output directory for results (default: output)
  --no-json             Skip JSON output
  --no-csv              Skip CSV output
  --no-summary          Skip summary report generation
  --delay-min DELAY_MIN
                        Minimum delay between requests in seconds (default: 1.0)
  --delay-max DELAY_MAX
                        Maximum delay between requests in seconds (default: 3.0)
  --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Logging level (default: INFO)
  --log-file LOG_FILE   Path to log file
  --quiet               Suppress console output (only log to file)
  --version             Show version number
```

### Examples

**Scrape with custom output directory:**
```bash
python -m casino_collector.cli --url https://example-casino.com --output ./data
```

**Scrape with custom delays (be more respectful):**
```bash
python -m casino_collector.cli --file casinos.txt --delay-min 2 --delay-max 5
```

**Generate only JSON output:**
```bash
python -m casino_collector.cli --url https://example-casino.com --no-csv --no-summary
```

**Debug mode with detailed logging:**
```bash
python -m casino_collector.cli --url https://example-casino.com --log-level DEBUG
```

## Output Files

The collector generates three types of output files in the specified output directory:

### 1. JSON Output (`casino_data_YYYYMMDD_HHMMSS.json`)

Complete structured data in JSON format with all collected information:

```json
[
  {
    "name": "Example Casino",
    "url": "https://example-casino.com",
    "description": "Casino description...",
    "licenses": [
      {
        "authority": "Malta Gaming Authority",
        "license_number": "MGA/B2C/123/2020",
        "jurisdiction": "Malta",
        "verified": false
      }
    ],
    "rtp_info": [...],
    "fairness": [...],
    "providers": [...],
    "security": {...},
    "withdrawal_methods": [...],
    "reviews": [...],
    "collection_date": "2024-01-01T12:00:00",
    "data_completeness_score": 85.7
  }
]
```

### 2. CSV Output (`casino_data_YYYYMMDD_HHMMSS.csv`)

Flattened data suitable for spreadsheet analysis with key metrics and aggregated information.

### 3. Summary Report (`casino_summary_YYYYMMDD_HHMMSS.txt`)

Human-readable text report with:
- Overall statistics
- Data completeness metrics
- Individual casino summaries

## Data Model

### CasinoData

The main data structure containing:

- **name**: Casino name
- **url**: Casino website URL
- **description**: Brief description
- **licenses**: List of licensing information
  - authority: Licensing authority name
  - license_number: License number (if available)
  - jurisdiction: Country/region
  - verified: Verification status
- **rtp_info**: List of RTP percentages
  - game_name: Name of the game
  - rtp_percentage: RTP percentage (0-100)
  - game_category: Category (slots, table games, etc.)
  - provider: Game provider
- **fairness**: List of fairness certifications
  - testing_agency: Name of testing agency
  - certification: Certification details
  - certified: Certification status
- **providers**: List of game providers
  - name: Provider name
  - games_count: Number of games
  - popular_games: List of popular titles
- **security**: Security information
  - ssl_certificate: SSL status
  - encryption_type: Type of encryption
  - two_factor_auth: 2FA availability
  - responsible_gambling_tools: List of RG tools
  - data_protection_compliance: Compliance (GDPR, etc.)
- **withdrawal_methods**: List of withdrawal options
  - method: Payment method name
  - min_amount: Minimum withdrawal
  - max_amount: Maximum withdrawal
  - processing_time: Processing duration
  - fees: Fee information
- **reviews**: List of reviews
  - source: Review platform
  - rating: Rating (0-5)
  - review_count: Number of reviews
  - positive_aspects: List of pros
  - negative_aspects: List of cons
- **collection_date**: When data was collected
- **data_completeness_score**: Completeness percentage (0-100)

## Configuration

### Configuration File Format

Create a `config.json` file:

```json
{
  "scraper": {
    "delay_min": 1.0,
    "delay_max": 3.0,
    "timeout": 30,
    "max_retries": 3
  },
  "storage": {
    "output_dir": "output",
    "auto_save_json": true,
    "auto_save_csv": true,
    "generate_summary": true
  },
  "logging": {
    "level": "INFO",
    "log_file": "logs/casino_collector.log"
  },
  "target_urls": [
    "https://casino1.com",
    "https://casino2.com"
  ]
}
```

### Environment Variables

You can also configure via environment variables:

- `SCRAPER_DELAY_MIN`: Minimum delay between requests
- `SCRAPER_DELAY_MAX`: Maximum delay between requests
- `OUTPUT_DIR`: Output directory path
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

## Architecture

The system is organized into modular components:

```
casino_collector/
├── __init__.py           # Package initialization
├── __main__.py           # Module entry point
├── cli.py                # Command-line interface
├── config.py             # Configuration management
├── models/               # Data models
│   └── __init__.py       # Pydantic models for casino data
├── scrapers/             # Scraping modules
│   ├── __init__.py
│   ├── base.py           # Base scraper class
│   └── generic_scraper.py # Generic casino scraper
├── storage/              # Data storage and export
│   └── __init__.py       # Storage handlers
└── utils/                # Utility functions
    └── __init__.py       # Helper functions
```

## Extending the System

### Adding a Custom Scraper

Create a new scraper by extending the `BaseScraper` class:

```python
from casino_collector.scrapers.base import BaseScraper
from casino_collector.models import CasinoData

class CustomCasinoScraper(BaseScraper):
    def scrape(self, url: str, **kwargs) -> CasinoData:
        # Your custom scraping logic
        casino_data = CasinoData(name="Casino Name", url=url)
        # ... collect data ...
        return casino_data
```

### Adding New Data Categories

Extend the data models in `casino_collector/models/__init__.py`:

```python
class NewCategory(BaseModel):
    field1: str
    field2: int

class CasinoData(BaseModel):
    # ... existing fields ...
    new_category: Optional[NewCategory] = None
```

## Best Practices

1. **Respect Robots.txt**: Always check a website's robots.txt before scraping
2. **Use Appropriate Delays**: Default 1-3 seconds between requests; increase if needed
3. **Monitor Resources**: Watch memory usage when scraping many sites
4. **Validate Data**: Review collected data for accuracy
5. **Legal Compliance**: Ensure you have permission to scrape target websites
6. **Rate Limiting**: Don't overwhelm target servers with requests

## Limitations

- This is a generic scraper that works best with well-structured websites
- Some data may not be available on all casino websites
- Accuracy depends on the structure and availability of information on target sites
- Dynamic content (JavaScript-rendered) may not be captured by the basic scraper
- Some casinos may block automated scraping attempts

## Troubleshooting

### No data collected

- Check if the URL is accessible
- Verify the website structure hasn't changed
- Try increasing the timeout value
- Check logs for specific error messages

### Low completeness scores

- Some data categories may not be available on the website
- The scraper may need customization for specific sites
- Consider creating site-specific scrapers for better accuracy

### Request errors

- Website may be blocking automated requests
- Check your internet connection
- Verify the URL is correct and accessible
- Try increasing delays between requests

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is provided as-is for educational and research purposes.

## Disclaimer

This tool is for research and educational purposes only. Users are responsible for:
- Complying with target websites' terms of service
- Respecting robots.txt files
- Following applicable laws and regulations
- Obtaining necessary permissions before scraping

The authors are not responsible for misuse of this tool.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

## Changelog

### Version 1.0.0
- Initial release
- Generic casino scraper implementation
- JSON, CSV, and text report outputs
- Command-line interface
- Configuration file support
- Comprehensive data model with 7+ categories