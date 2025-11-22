"""
Generic casino scraper using requests and BeautifulSoup.
"""
import requests
from bs4 import BeautifulSoup
from typing import Optional, List
from datetime import datetime, timezone
import logging

from casino_collector.models import (
    CasinoData, LicenseInfo, RTpInfo, FairnessInfo,
    ProviderInfo, SecurityInfo, WithdrawalInfo, ReviewInfo,
    utcnow
)
from casino_collector.scrapers.base import BaseScraper


class GenericCasinoScraper(BaseScraper):
    """Generic scraper for casino websites."""
    
    def __init__(self, delay_range: tuple = (1, 3)):
        super().__init__(delay_range)
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def scrape(self, url: str, casino_name: Optional[str] = None) -> Optional[CasinoData]:
        """
        Scrape casino data from a website.
        
        Args:
            url: Casino website URL
            casino_name: Optional casino name (will try to extract if not provided)
            
        Returns:
            CasinoData object or None if scraping fails
        """
        try:
            self.logger.info(f"Scraping casino data from: {url}")
            
            # Fetch the page
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract casino name if not provided
            if not casino_name:
                casino_name = self._extract_name(soup, url)
            
            # Create casino data object
            casino_data = CasinoData(
                name=casino_name,
                url=url,
                description=self._extract_description(soup)
            )
            
            # Scrape different data categories
            casino_data.licenses = self._extract_licenses(soup)
            casino_data.rtp_info = self._extract_rtp_info(soup)
            casino_data.fairness = self._extract_fairness(soup)
            casino_data.providers = self._extract_providers(soup)
            casino_data.security = self._extract_security(soup)
            casino_data.withdrawal_methods = self._extract_withdrawal_methods(soup)
            casino_data.reviews = self._extract_reviews(soup)
            
            # Calculate completeness score
            casino_data.data_completeness_score = self.calculate_completeness_score(casino_data)
            casino_data.last_updated = utcnow()
            
            self.logger.info(f"Successfully scraped {casino_name} (completeness: {casino_data.data_completeness_score:.1f}%)")
            
            return casino_data
            
        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch {url}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error scraping {url}: {e}")
            return None
    
    def _extract_name(self, soup: BeautifulSoup, url: str) -> str:
        """Extract casino name from page."""
        # Try common locations for casino name
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.get_text().strip().split('|')[0].strip()
        
        # Fallback to domain name
        from urllib.parse import urlparse
        domain = urlparse(url).netloc
        return domain.replace('www.', '').replace('.com', '').title()
    
    def _extract_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract casino description."""
        # Look for meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            return meta_desc['content'].strip()
        
        # Look for first paragraph in main content
        main_content = soup.find('main') or soup.find('div', class_='content')
        if main_content:
            first_p = main_content.find('p')
            if first_p:
                return first_p.get_text().strip()[:500]
        
        return None
    
    def _extract_licenses(self, soup: BeautifulSoup) -> List[LicenseInfo]:
        """Extract licensing information."""
        licenses = []
        
        # Look for common license-related keywords
        license_keywords = ['license', 'licensed', 'regulated', 'mga', 'ukgc', 'curacao']
        
        for keyword in license_keywords:
            elements = soup.find_all(text=lambda text: text and keyword.lower() in text.lower())
            
            for element in elements[:3]:  # Limit to first 3 matches
                text = element.strip()
                
                # Try to identify licensing authority
                if 'malta' in text.lower() or 'mga' in text.lower():
                    licenses.append(LicenseInfo(
                        authority="Malta Gaming Authority",
                        jurisdiction="Malta",
                        verified=False
                    ))
                elif 'uk' in text.lower() or 'ukgc' in text.lower():
                    licenses.append(LicenseInfo(
                        authority="UK Gambling Commission",
                        jurisdiction="United Kingdom",
                        verified=False
                    ))
                elif 'curacao' in text.lower():
                    licenses.append(LicenseInfo(
                        authority="Curacao eGaming",
                        jurisdiction="Curacao",
                        verified=False
                    ))
        
        # Remove duplicates
        unique_licenses = []
        seen_authorities = set()
        for license in licenses:
            if license.authority not in seen_authorities:
                unique_licenses.append(license)
                seen_authorities.add(license.authority)
        
        return unique_licenses
    
    def _extract_rtp_info(self, soup: BeautifulSoup) -> List[RTpInfo]:
        """Extract RTP information."""
        rtp_info = []
        
        # Look for RTP mentions
        rtp_elements = soup.find_all(text=lambda text: text and 'rtp' in text.lower())
        
        for element in rtp_elements[:5]:  # Limit results
            text = element.strip()
            
            # Try to extract percentage
            import re
            percentages = re.findall(r'(\d+\.?\d*)%', text)
            
            for pct in percentages:
                try:
                    pct_value = float(pct)
                    if 80 <= pct_value <= 100:  # Reasonable RTP range
                        rtp_info.append(RTpInfo(
                            rtp_percentage=pct_value,
                            game_category="General"
                        ))
                except ValueError:
                    continue
        
        return rtp_info
    
    def _extract_fairness(self, soup: BeautifulSoup) -> List[FairnessInfo]:
        """Extract fairness/testing information."""
        fairness = []
        
        testing_agencies = [
            'eCOGRA', 'iTech Labs', 'GLI', 'Gaming Laboratories',
            'BMM Testlabs', 'TST', 'Technical Systems Testing'
        ]
        
        for agency in testing_agencies:
            if soup.find(text=lambda text: text and agency.lower() in text.lower()):
                fairness.append(FairnessInfo(
                    testing_agency=agency,
                    certified=True
                ))
        
        return fairness
    
    def _extract_providers(self, soup: BeautifulSoup) -> List[ProviderInfo]:
        """Extract game provider information."""
        providers = []
        
        common_providers = [
            'NetEnt', 'Microgaming', 'Playtech', 'Evolution Gaming',
            'Pragmatic Play', 'Play\'n GO', 'Yggdrasil', 'Betsoft',
            'IGT', 'Novomatic', 'EGT', 'Quickspin', 'Red Tiger'
        ]
        
        for provider_name in common_providers:
            if soup.find(text=lambda text: text and provider_name.lower() in text.lower()):
                providers.append(ProviderInfo(name=provider_name))
        
        return providers
    
    def _extract_security(self, soup: BeautifulSoup) -> Optional[SecurityInfo]:
        """Extract security information."""
        security = SecurityInfo()
        
        # Check for SSL (this will always be true for HTTPS sites)
        security.ssl_certificate = True
        
        # Look for encryption mentions
        if soup.find(text=lambda text: text and 'ssl' in text.lower()):
            security.encryption_type = "SSL/TLS"
        
        if soup.find(text=lambda text: text and '128-bit' in text.lower()):
            security.encryption_type = "128-bit SSL"
        elif soup.find(text=lambda text: text and '256-bit' in text.lower()):
            security.encryption_type = "256-bit SSL"
        
        # Look for 2FA
        if soup.find(text=lambda text: text and ('two-factor' in text.lower() or '2fa' in text.lower())):
            security.two_factor_auth = True
        
        # Look for responsible gambling tools
        responsible_gambling_keywords = [
            'self-exclusion', 'deposit limit', 'time limit',
            'reality check', 'cool-off', 'self-assessment'
        ]
        
        for keyword in responsible_gambling_keywords:
            if soup.find(text=lambda text: text and keyword in text.lower()):
                security.responsible_gambling_tools.append(keyword.title())
        
        # Look for GDPR/data protection
        if soup.find(text=lambda text: text and 'gdpr' in text.lower()):
            security.data_protection_compliance.append("GDPR")
        
        return security if security.ssl_certificate else None
    
    def _extract_withdrawal_methods(self, soup: BeautifulSoup) -> List[WithdrawalInfo]:
        """Extract withdrawal method information."""
        methods = []
        
        common_methods = [
            'Visa', 'Mastercard', 'PayPal', 'Skrill', 'Neteller',
            'Bank Transfer', 'Bitcoin', 'Cryptocurrency', 'ecoPayz',
            'Paysafecard', 'Trustly', 'Zimpler'
        ]
        
        for method_name in common_methods:
            if soup.find(text=lambda text: text and method_name.lower() in text.lower()):
                methods.append(WithdrawalInfo(
                    method=method_name,
                    processing_time="Varies"
                ))
        
        return methods
    
    def _extract_reviews(self, soup: BeautifulSoup) -> List[ReviewInfo]:
        """Extract review information if available on the page."""
        reviews = []
        
        # Look for common review patterns
        import re
        
        # Check for star ratings
        rating_patterns = [
            r'(\d+\.?\d*)\s*(?:out of|/)\s*5',
            r'(\d+\.?\d*)\s*stars?',
        ]
        
        for pattern in rating_patterns:
            matches = re.findall(pattern, soup.get_text(), re.IGNORECASE)
            for match in matches[:3]:
                try:
                    rating = float(match)
                    if 0 <= rating <= 5:
                        reviews.append(ReviewInfo(
                            source="Website",
                            rating=rating,
                            review_date=utcnow()
                        ))
                except ValueError:
                    continue
        
        return reviews
