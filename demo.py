#!/usr/bin/env python3
"""
Demo script that creates sample casino data to show the system's capabilities.
"""
from datetime import datetime, timezone
from casino_collector.models import (
    CasinoData, LicenseInfo, RTpInfo, FairnessInfo,
    ProviderInfo, SecurityInfo, WithdrawalInfo, ReviewInfo,
    utcnow
)
from casino_collector.storage import DataStorage
from casino_collector.utils import setup_logging

def create_sample_data():
    """Create sample casino data for demonstration."""
    
    # Sample Casino 1
    casino1 = CasinoData(
        name="Royal Fortune Casino",
        url="https://www.royalfortune-casino.example.com",
        description="A premium online casino offering a wide selection of games with top-tier security and fast withdrawals.",
        licenses=[
            LicenseInfo(
                authority="Malta Gaming Authority",
                license_number="MGA/B2C/123/2020",
                jurisdiction="Malta",
                verified=True,
                verification_date=datetime(2024, 1, 15, tzinfo=timezone.utc)
            ),
            LicenseInfo(
                authority="UK Gambling Commission",
                license_number="UKGC-54321",
                jurisdiction="United Kingdom",
                verified=True,
                verification_date=datetime(2024, 1, 15, tzinfo=timezone.utc)
            )
        ],
        rtp_info=[
            RTpInfo(game_name="Starburst", rtp_percentage=96.1, game_category="Slots", provider="NetEnt"),
            RTpInfo(game_name="Book of Dead", rtp_percentage=96.21, game_category="Slots", provider="Play'n GO"),
            RTpInfo(game_name="European Roulette", rtp_percentage=97.3, game_category="Table Games", provider="Evolution Gaming"),
        ],
        fairness=[
            FairnessInfo(
                testing_agency="eCOGRA",
                certification="Safe and Fair",
                certified=True,
                last_audit_date=datetime(2024, 1, 1, tzinfo=timezone.utc)
            ),
            FairnessInfo(
                testing_agency="iTech Labs",
                certification="RNG Certified",
                certified=True,
                last_audit_date=datetime(2024, 2, 1, tzinfo=timezone.utc)
            )
        ],
        providers=[
            ProviderInfo(name="NetEnt", games_count=150, popular_games=["Starburst", "Gonzo's Quest"]),
            ProviderInfo(name="Microgaming", games_count=200, popular_games=["Mega Moolah", "Immortal Romance"]),
            ProviderInfo(name="Evolution Gaming", games_count=50, popular_games=["Lightning Roulette", "Dream Catcher"]),
            ProviderInfo(name="Play'n GO", games_count=100),
            ProviderInfo(name="Pragmatic Play", games_count=120),
        ],
        security=SecurityInfo(
            ssl_certificate=True,
            encryption_type="256-bit SSL",
            two_factor_auth=True,
            responsible_gambling_tools=["Self-Exclusion", "Deposit Limits", "Time Limits", "Reality Check"],
            data_protection_compliance=["GDPR", "PCI DSS"]
        ),
        withdrawal_methods=[
            WithdrawalInfo(method="Visa", min_amount=20.0, max_amount=5000.0, processing_time="1-3 days", fees="Free"),
            WithdrawalInfo(method="Mastercard", min_amount=20.0, max_amount=5000.0, processing_time="1-3 days", fees="Free"),
            WithdrawalInfo(method="PayPal", min_amount=10.0, max_amount=10000.0, processing_time="0-24 hours", fees="Free"),
            WithdrawalInfo(method="Skrill", min_amount=10.0, max_amount=10000.0, processing_time="0-24 hours", fees="Free"),
            WithdrawalInfo(method="Bank Transfer", min_amount=100.0, max_amount=50000.0, processing_time="3-5 days", fees="Free"),
        ],
        reviews=[
            ReviewInfo(
                source="TrustPilot",
                rating=4.5,
                review_count=1250,
                positive_aspects=["Fast withdrawals", "Great game selection", "Professional support"],
                negative_aspects=["Limited crypto options"],
                review_date=datetime(2024, 1, 20, tzinfo=timezone.utc)
            ),
            ReviewInfo(
                source="AskGamblers",
                rating=4.2,
                review_count=890,
                positive_aspects=["Licensed and regulated", "Good bonuses"],
                negative_aspects=["Wagering requirements"],
                review_date=datetime(2024, 1, 15, tzinfo=timezone.utc)
            )
        ],
        collection_date=utcnow(),
        data_completeness_score=100.0
    )
    
    # Sample Casino 2
    casino2 = CasinoData(
        name="Lucky Spin Casino",
        url="https://www.luckyspin-casino.example.com",
        description="An exciting casino platform with innovative games and rewarding promotions.",
        licenses=[
            LicenseInfo(
                authority="Curacao eGaming",
                license_number="CEG-8048/JAZ",
                jurisdiction="Curacao",
                verified=False
            )
        ],
        rtp_info=[
            RTpInfo(rtp_percentage=96.5, game_category="Slots"),
            RTpInfo(rtp_percentage=97.0, game_category="Table Games"),
        ],
        fairness=[
            FairnessInfo(
                testing_agency="Gaming Laboratories International",
                certified=True
            )
        ],
        providers=[
            ProviderInfo(name="Betsoft"),
            ProviderInfo(name="Pragmatic Play"),
            ProviderInfo(name="Yggdrasil"),
            ProviderInfo(name="Red Tiger"),
        ],
        security=SecurityInfo(
            ssl_certificate=True,
            encryption_type="128-bit SSL",
            two_factor_auth=False,
            responsible_gambling_tools=["Self-Exclusion", "Deposit Limits"],
            data_protection_compliance=["GDPR"]
        ),
        withdrawal_methods=[
            WithdrawalInfo(method="Bitcoin", processing_time="0-24 hours"),
            WithdrawalInfo(method="Ethereum", processing_time="0-24 hours"),
            WithdrawalInfo(method="Visa", processing_time="3-5 days"),
            WithdrawalInfo(method="Mastercard", processing_time="3-5 days"),
        ],
        reviews=[
            ReviewInfo(
                source="Casino.org",
                rating=3.8,
                review_count=450,
                positive_aspects=["Crypto-friendly", "Good mobile experience"],
                negative_aspects=["Slower support response"],
                review_date=datetime(2024, 1, 10, tzinfo=timezone.utc)
            )
        ],
        collection_date=utcnow(),
        data_completeness_score=85.7
    )
    
    # Sample Casino 3
    casino3 = CasinoData(
        name="Diamond Palace Casino",
        url="https://www.diamond-palace.example.com",
        description="Luxury casino experience with VIP programs and exclusive tournaments.",
        licenses=[
            LicenseInfo(
                authority="Malta Gaming Authority",
                license_number="MGA/B2C/456/2021",
                jurisdiction="Malta",
                verified=True
            )
        ],
        rtp_info=[
            RTpInfo(game_name="Mega Fortune", rtp_percentage=96.6, game_category="Progressive Slots", provider="NetEnt"),
        ],
        fairness=[
            FairnessInfo(testing_agency="eCOGRA", certified=True)
        ],
        providers=[
            ProviderInfo(name="NetEnt"),
            ProviderInfo(name="Playtech"),
            ProviderInfo(name="Evolution Gaming"),
        ],
        security=SecurityInfo(
            ssl_certificate=True,
            encryption_type="256-bit SSL",
            two_factor_auth=True,
            responsible_gambling_tools=["Self-Exclusion", "Deposit Limits", "Cool-off Period"],
            data_protection_compliance=["GDPR"]
        ),
        withdrawal_methods=[
            WithdrawalInfo(method="PayPal", min_amount=10.0, processing_time="0-24 hours"),
            WithdrawalInfo(method="Trustly", min_amount=20.0, processing_time="Instant"),
            WithdrawalInfo(method="Bank Transfer", processing_time="2-4 days"),
        ],
        reviews=[
            ReviewInfo(
                source="CasinoMeister",
                rating=4.7,
                review_count=680,
                positive_aspects=["Excellent VIP program", "Fast payouts", "Great live casino"],
                review_date=datetime(2024, 1, 25, tzinfo=timezone.utc)
            )
        ],
        collection_date=utcnow(),
        data_completeness_score=92.9
    )
    
    return [casino1, casino2, casino3]


def main():
    """Run the demo."""
    print("=" * 80)
    print("CASINO INTELLIGENCE COLLECTOR - DEMO")
    print("=" * 80)
    print()
    print("This demo creates sample casino data to showcase the system's capabilities.")
    print()
    
    # Setup logging
    setup_logging(level="INFO")
    
    # Create sample data
    print("Creating sample casino data...")
    casinos = create_sample_data()
    print(f"✓ Created {len(casinos)} sample casinos")
    print()
    
    # Display summary
    for casino in casinos:
        print(f"Casino: {casino.name}")
        print(f"  Completeness: {casino.data_completeness_score:.1f}%")
        print(f"  Licenses: {len(casino.licenses)}")
        print(f"  RTP Info: {len(casino.rtp_info)}")
        print(f"  Providers: {len(casino.providers)}")
        print(f"  Withdrawal Methods: {len(casino.withdrawal_methods)}")
        print(f"  Reviews: {len(casino.reviews)}")
        print()
    
    # Save to files
    storage = DataStorage(output_dir="demo_output")
    
    print("Saving data to files...")
    json_path = storage.save_json(casinos, filename="demo_casinos.json")
    print(f"✓ JSON: {json_path}")
    
    csv_path = storage.save_csv(casinos, filename="demo_casinos.csv")
    print(f"✓ CSV: {csv_path}")
    
    summary_path = storage.generate_summary_report(casinos, filename="demo_summary.txt")
    print(f"✓ Summary: {summary_path}")
    print()
    
    # Statistics
    avg_completeness = sum([c.data_completeness_score for c in casinos]) / len(casinos)
    total_licenses = sum([len(c.licenses) for c in casinos])
    total_providers = sum([len(c.providers) for c in casinos])
    avg_rating = sum([
        sum([r.rating for r in c.reviews]) / len(c.reviews) 
        for c in casinos if c.reviews
    ]) / len([c for c in casinos if c.reviews])
    
    print("=" * 80)
    print("STATISTICS")
    print("=" * 80)
    print(f"Casinos analyzed: {len(casinos)}")
    print(f"Average completeness: {avg_completeness:.1f}%")
    print(f"Total licenses: {total_licenses}")
    print(f"Total providers: {total_providers}")
    print(f"Average rating: {avg_rating:.2f}/5.0")
    print("=" * 80)
    print()
    print("Demo complete! Check the 'demo_output' directory for generated files.")


if __name__ == "__main__":
    main()
