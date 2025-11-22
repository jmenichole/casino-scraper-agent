"""
Base scraper class and utilities.
"""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
import logging
from datetime import datetime
import time
import random

from casino_collector.models import CasinoData


class BaseScraper(ABC):
    """Base class for all casino data scrapers."""
    
    def __init__(self, delay_range: tuple = (1, 3)):
        """
        Initialize the scraper.
        
        Args:
            delay_range: Tuple of (min, max) seconds to wait between requests
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.delay_range = delay_range
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    
    def random_delay(self):
        """Add random delay between requests to be respectful."""
        delay = random.uniform(*self.delay_range)
        self.logger.debug(f"Waiting {delay:.2f} seconds...")
        time.sleep(delay)
    
    @abstractmethod
    def scrape(self, url: str, **kwargs) -> Optional[CasinoData]:
        """
        Scrape casino data from the given URL.
        
        Args:
            url: The URL to scrape
            **kwargs: Additional scraper-specific parameters
            
        Returns:
            CasinoData object if successful, None otherwise
        """
        pass
    
    def validate_data(self, data: CasinoData) -> bool:
        """
        Validate scraped data.
        
        Args:
            data: CasinoData object to validate
            
        Returns:
            True if data is valid, False otherwise
        """
        try:
            # Pydantic will validate the data structure
            data.model_validate(data.model_dump())
            return True
        except Exception as e:
            self.logger.error(f"Data validation failed: {e}")
            return False
    
    def calculate_completeness_score(self, data: CasinoData) -> float:
        """
        Calculate how complete the collected data is.
        
        Args:
            data: CasinoData object
            
        Returns:
            Completeness score between 0 and 100
        """
        total_fields = 7  # Total number of main data categories
        filled_fields = 0
        
        if data.licenses:
            filled_fields += 1
        if data.rtp_info:
            filled_fields += 1
        if data.fairness:
            filled_fields += 1
        if data.providers:
            filled_fields += 1
        if data.security:
            filled_fields += 1
        if data.withdrawal_methods:
            filled_fields += 1
        if data.reviews:
            filled_fields += 1
        
        return (filled_fields / total_fields) * 100
