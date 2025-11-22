"""
Configuration management for the Casino Intelligence Collector.
"""
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel, Field
import json
import os


class ScraperConfig(BaseModel):
    """Configuration for scrapers."""
    delay_min: float = Field(default=1.0, description="Minimum delay between requests (seconds)")
    delay_max: float = Field(default=3.0, description="Maximum delay between requests (seconds)")
    timeout: int = Field(default=30, description="Request timeout (seconds)")
    max_retries: int = Field(default=3, description="Maximum retry attempts")
    user_agent: Optional[str] = None


class StorageConfig(BaseModel):
    """Configuration for data storage."""
    output_dir: str = Field(default="output", description="Output directory for data")
    auto_save_json: bool = Field(default=True, description="Automatically save JSON after scraping")
    auto_save_csv: bool = Field(default=True, description="Automatically save CSV after scraping")
    generate_summary: bool = Field(default=True, description="Generate summary report")


class LoggingConfig(BaseModel):
    """Configuration for logging."""
    level: str = Field(default="INFO", description="Logging level")
    log_file: Optional[str] = Field(default="logs/casino_collector.log", description="Log file path")
    console_output: bool = Field(default=True, description="Output logs to console")


class Config(BaseModel):
    """Main configuration for Casino Intelligence Collector."""
    scraper: ScraperConfig = Field(default_factory=ScraperConfig)
    storage: StorageConfig = Field(default_factory=StorageConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    target_urls: List[str] = Field(default_factory=list, description="List of casino URLs to scrape")
    
    @classmethod
    def load_from_file(cls, config_path: str) -> 'Config':
        """
        Load configuration from JSON file.
        
        Args:
            config_path: Path to config file
            
        Returns:
            Config object
        """
        path = Path(config_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        with open(path, 'r') as f:
            config_data = json.load(f)
        
        return cls(**config_data)
    
    def save_to_file(self, config_path: str) -> None:
        """
        Save configuration to JSON file.
        
        Args:
            config_path: Path to save config file
        """
        path = Path(config_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w') as f:
            json.dump(self.model_dump(), f, indent=2)
    
    @classmethod
    def load_from_env(cls) -> 'Config':
        """
        Load configuration from environment variables.
        
        Returns:
            Config object
        """
        config = cls()
        
        # Load from environment variables if present
        if os.getenv('SCRAPER_DELAY_MIN'):
            config.scraper.delay_min = float(os.getenv('SCRAPER_DELAY_MIN'))
        
        if os.getenv('SCRAPER_DELAY_MAX'):
            config.scraper.delay_max = float(os.getenv('SCRAPER_DELAY_MAX'))
        
        if os.getenv('OUTPUT_DIR'):
            config.storage.output_dir = os.getenv('OUTPUT_DIR')
        
        if os.getenv('LOG_LEVEL'):
            config.logging.level = os.getenv('LOG_LEVEL')
        
        return config
