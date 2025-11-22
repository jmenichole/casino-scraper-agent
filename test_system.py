#!/usr/bin/env python3
"""
Test script to validate the Casino Intelligence Collector components.
"""
import sys
from datetime import datetime, timezone

# Test imports
try:
    from casino_collector.models import (
        CasinoData, LicenseInfo, RTpInfo, FairnessInfo,
        ProviderInfo, SecurityInfo, WithdrawalInfo, ReviewInfo,
        utcnow
    )
    from casino_collector.scrapers import GenericCasinoScraper, BaseScraper
    from casino_collector.storage import DataStorage
    from casino_collector.config import Config
    from casino_collector.utils import (
        setup_logging, validate_url, sanitize_filename, format_duration
    )
    print("✓ All imports successful")
except ImportError as e:
    print(f"✗ Import failed: {e}")
    sys.exit(1)

# Test data model creation
try:
    casino = CasinoData(
        name="Test Casino",
        url="https://test.com"
    )
    assert casino.name == "Test Casino"
    assert str(casino.url) == "https://test.com/"
    assert len(casino.licenses) == 0
    print("✓ Data model creation works")
except Exception as e:
    print(f"✗ Data model creation failed: {e}")
    sys.exit(1)

# Test license creation
try:
    license = LicenseInfo(
        authority="Test Authority",
        jurisdiction="Test Country",
        verified=True
    )
    assert license.authority == "Test Authority"
    print("✓ License model creation works")
except Exception as e:
    print(f"✗ License model creation failed: {e}")
    sys.exit(1)

# Test RTP creation
try:
    rtp = RTpInfo(
        game_name="Test Game",
        rtp_percentage=96.5,
        game_category="Slots"
    )
    assert rtp.rtp_percentage == 96.5
    print("✓ RTP model creation works")
except Exception as e:
    print(f"✗ RTP model creation failed: {e}")
    sys.exit(1)

# Test scraper initialization
try:
    scraper = GenericCasinoScraper(delay_range=(0.1, 0.2))
    assert scraper.delay_range == (0.1, 0.2)
    print("✓ Scraper initialization works")
except Exception as e:
    print(f"✗ Scraper initialization failed: {e}")
    sys.exit(1)

# Test storage initialization
try:
    storage = DataStorage(output_dir="/tmp/test_output")
    assert str(storage.output_dir) == "/tmp/test_output"
    print("✓ Storage initialization works")
except Exception as e:
    print(f"✗ Storage initialization failed: {e}")
    sys.exit(1)

# Test config
try:
    config = Config()
    assert config.scraper.delay_min == 1.0
    assert config.storage.output_dir == "output"
    print("✓ Config creation works")
except Exception as e:
    print(f"✗ Config creation failed: {e}")
    sys.exit(1)

# Test URL validation
try:
    assert validate_url("https://example.com") == True
    assert validate_url("http://test.com") == True
    assert validate_url("not-a-url") == False
    assert validate_url("ftp://invalid.com") == False
    print("✓ URL validation works")
except Exception as e:
    print(f"✗ URL validation failed: {e}")
    sys.exit(1)

# Test filename sanitization
try:
    assert sanitize_filename("test file.txt") == "test_file.txt"
    assert sanitize_filename("bad/name\\here.txt") == "badnamehere.txt"
    print("✓ Filename sanitization works")
except Exception as e:
    print(f"✗ Filename sanitization failed: {e}")
    sys.exit(1)

# Test duration formatting
try:
    assert format_duration(30) == "30.0s"
    assert format_duration(90) == "1m 30s"
    assert format_duration(3660) == "1h 1m"
    print("✓ Duration formatting works")
except Exception as e:
    print(f"✗ Duration formatting failed: {e}")
    sys.exit(1)

# Test completeness score calculation
try:
    casino = CasinoData(name="Test", url="https://test.com")
    scraper = GenericCasinoScraper()
    score = scraper.calculate_completeness_score(casino)
    assert score == 0.0  # Empty data
    
    casino.licenses = [LicenseInfo(authority="Test", jurisdiction="Test")]
    casino.providers = [ProviderInfo(name="Test Provider")]
    score = scraper.calculate_completeness_score(casino)
    assert score > 0.0
    print("✓ Completeness score calculation works")
except Exception as e:
    print(f"✗ Completeness score calculation failed: {e}")
    sys.exit(1)

# Test JSON serialization
try:
    import json
    casino = CasinoData(
        name="Test Casino",
        url="https://test.com",
        licenses=[
            LicenseInfo(authority="Test", jurisdiction="Test")
        ]
    )
    data_dict = casino.model_dump(mode='json')
    json_str = json.dumps(data_dict, default=str)
    assert "Test Casino" in json_str
    print("✓ JSON serialization works")
except Exception as e:
    print(f"✗ JSON serialization failed: {e}")
    sys.exit(1)

# Test datetime handling
try:
    now = utcnow()
    assert now.tzinfo is not None  # Should be timezone-aware
    print("✓ Timezone-aware datetime works")
except Exception as e:
    print(f"✗ Datetime handling failed: {e}")
    sys.exit(1)

# Test data validation
try:
    # Valid data
    casino = CasinoData(
        name="Valid Casino",
        url="https://valid.com"
    )
    scraper = GenericCasinoScraper()
    assert scraper.validate_data(casino) == True
    
    # Invalid RTP (should fail)
    try:
        invalid_rtp = RTpInfo(rtp_percentage=150.0)  # > 100
        print("✗ RTP validation should have failed")
        sys.exit(1)
    except:
        pass  # Expected to fail
    
    print("✓ Data validation works")
except Exception as e:
    print(f"✗ Data validation failed: {e}")
    sys.exit(1)

# Test storage save/load
try:
    import tempfile
    import os
    
    # Create test data
    casinos = [
        CasinoData(name="Casino 1", url="https://casino1.com"),
        CasinoData(name="Casino 2", url="https://casino2.com")
    ]
    
    # Create temp directory
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = DataStorage(output_dir=tmpdir)
        
        # Save JSON
        json_path = storage.save_json(casinos, filename="test.json")
        assert os.path.exists(json_path)
        
        # Load JSON
        loaded = storage.load_json("test.json")
        assert len(loaded) == 2
        assert loaded[0].name == "Casino 1"
        
        # Save CSV
        csv_path = storage.save_csv(casinos, filename="test.csv")
        assert os.path.exists(csv_path)
        
        # Generate summary
        summary_path = storage.generate_summary_report(casinos, filename="test_summary.txt")
        assert os.path.exists(summary_path)
    
    print("✓ Storage save/load works")
except Exception as e:
    print(f"✗ Storage save/load failed: {e}")
    sys.exit(1)

# All tests passed
print("\n" + "=" * 60)
print("ALL TESTS PASSED ✓")
print("=" * 60)
print("\nThe Casino Intelligence Collector is working correctly!")
print("You can now use it to scrape real casino websites.")
print("\nTry the demo: python demo.py")
print("Or see examples: python example.py")
