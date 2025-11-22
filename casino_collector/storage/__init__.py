"""
Data storage and export utilities.
"""
import json
import csv
from pathlib import Path
from typing import List, Optional
from datetime import datetime
import logging

from casino_collector.models import CasinoData


class DataStorage:
    """Handle storage and export of casino data."""
    
    def __init__(self, output_dir: str = "output"):
        """
        Initialize storage handler.
        
        Args:
            output_dir: Directory to store output files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def save_json(self, data: List[CasinoData], filename: Optional[str] = None) -> str:
        """
        Save casino data to JSON file.
        
        Args:
            data: List of CasinoData objects
            filename: Optional filename (will generate timestamped name if not provided)
            
        Returns:
            Path to saved file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"casino_data_{timestamp}.json"
        
        filepath = self.output_dir / filename
        
        # Convert to dict and handle datetime serialization
        data_dicts = [casino.model_dump(mode='json') for casino in data]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data_dicts, f, indent=2, ensure_ascii=False, default=str)
        
        self.logger.info(f"Saved {len(data)} casino records to {filepath}")
        return str(filepath)
    
    def save_csv(self, data: List[CasinoData], filename: Optional[str] = None) -> str:
        """
        Save casino data to CSV file (flattened structure).
        
        Args:
            data: List of CasinoData objects
            filename: Optional filename
            
        Returns:
            Path to saved file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"casino_data_{timestamp}.csv"
        
        filepath = self.output_dir / filename
        
        if not data:
            self.logger.warning("No data to save to CSV")
            return str(filepath)
        
        # Flatten data for CSV
        flattened_data = []
        for casino in data:
            row = {
                'name': casino.name,
                'url': str(casino.url) if casino.url else '',
                'description': casino.description or '',
                'collection_date': casino.collection_date.isoformat() if casino.collection_date else '',
                'data_completeness_score': casino.data_completeness_score or 0,
                'license_count': len(casino.licenses),
                'licenses': ', '.join([f"{lic.authority} ({lic.jurisdiction})" for lic in casino.licenses]),
                'rtp_count': len(casino.rtp_info),
                'avg_rtp': sum([rtp.rtp_percentage for rtp in casino.rtp_info]) / len(casino.rtp_info) if casino.rtp_info else 0,
                'fairness_certifications': ', '.join([f.testing_agency for f in casino.fairness]),
                'provider_count': len(casino.providers),
                'providers': ', '.join([p.name for p in casino.providers]),
                'has_ssl': casino.security.ssl_certificate if casino.security else False,
                'encryption': casino.security.encryption_type if casino.security else '',
                'two_factor_auth': casino.security.two_factor_auth if casino.security else False,
                'withdrawal_methods_count': len(casino.withdrawal_methods),
                'withdrawal_methods': ', '.join([w.method for w in casino.withdrawal_methods]),
                'review_count': len(casino.reviews),
                'avg_rating': sum([r.rating for r in casino.reviews]) / len(casino.reviews) if casino.reviews else 0,
            }
            flattened_data.append(row)
        
        # Write to CSV
        if flattened_data:
            fieldnames = flattened_data[0].keys()
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(flattened_data)
        
        self.logger.info(f"Saved {len(data)} casino records to {filepath}")
        return str(filepath)
    
    def load_json(self, filename: str) -> List[CasinoData]:
        """
        Load casino data from JSON file.
        
        Args:
            filename: Path to JSON file
            
        Returns:
            List of CasinoData objects
        """
        filepath = Path(filename)
        
        if not filepath.exists():
            # Try in output directory
            filepath = self.output_dir / filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filename}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data_dicts = json.load(f)
        
        casinos = [CasinoData(**casino_dict) for casino_dict in data_dicts]
        self.logger.info(f"Loaded {len(casinos)} casino records from {filepath}")
        
        return casinos
    
    def generate_summary_report(self, data: List[CasinoData], filename: Optional[str] = None) -> str:
        """
        Generate a summary report of collected data.
        
        Args:
            data: List of CasinoData objects
            filename: Optional filename
            
        Returns:
            Path to saved report
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"casino_summary_{timestamp}.txt"
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("CASINO INTELLIGENCE COLLECTOR - SUMMARY REPORT\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Casinos Analyzed: {len(data)}\n\n")
            
            # Overall statistics
            f.write("-" * 80 + "\n")
            f.write("OVERALL STATISTICS\n")
            f.write("-" * 80 + "\n")
            
            avg_completeness = sum([c.data_completeness_score or 0 for c in data]) / len(data) if data else 0
            f.write(f"Average Data Completeness: {avg_completeness:.1f}%\n")
            
            total_licenses = sum([len(c.licenses) for c in data])
            f.write(f"Total Licenses Found: {total_licenses}\n")
            
            total_providers = sum([len(c.providers) for c in data])
            f.write(f"Total Provider Relationships: {total_providers}\n")
            
            casinos_with_ssl = sum([1 for c in data if c.security and c.security.ssl_certificate])
            f.write(f"Casinos with SSL: {casinos_with_ssl}/{len(data)}\n")
            
            casinos_with_2fa = sum([1 for c in data if c.security and c.security.two_factor_auth])
            f.write(f"Casinos with 2FA: {casinos_with_2fa}/{len(data)}\n\n")
            
            # Individual casino details
            f.write("-" * 80 + "\n")
            f.write("INDIVIDUAL CASINO DETAILS\n")
            f.write("-" * 80 + "\n\n")
            
            for casino in data:
                f.write(f"Casino: {casino.name}\n")
                f.write(f"URL: {casino.url or 'N/A'}\n")
                f.write(f"Completeness: {casino.data_completeness_score or 0:.1f}%\n")
                f.write(f"Licenses: {len(casino.licenses)}\n")
                f.write(f"Providers: {len(casino.providers)}\n")
                f.write(f"Withdrawal Methods: {len(casino.withdrawal_methods)}\n")
                f.write(f"Reviews: {len(casino.reviews)}\n")
                f.write("\n")
        
        self.logger.info(f"Generated summary report: {filepath}")
        return str(filepath)
