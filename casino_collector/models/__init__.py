"""
Data models for casino information.
"""
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, HttpUrl


def utcnow():
    """Return current UTC time as timezone-aware datetime."""
    return datetime.now(timezone.utc)


class LicenseInfo(BaseModel):
    """Casino licensing information."""
    authority: str = Field(..., description="Licensing authority name")
    license_number: Optional[str] = Field(None, description="License number if available")
    jurisdiction: str = Field(..., description="Jurisdiction/country")
    verified: bool = Field(default=False, description="Whether license was verified")
    verification_date: Optional[datetime] = None


class RTpInfo(BaseModel):
    """Return to Player (RTP) information."""
    game_name: Optional[str] = None
    rtp_percentage: float = Field(..., ge=0, le=100, description="RTP percentage")
    game_category: Optional[str] = None
    provider: Optional[str] = None


class FairnessInfo(BaseModel):
    """Casino fairness and testing information."""
    testing_agency: str = Field(..., description="Independent testing agency")
    certification: Optional[str] = None
    last_audit_date: Optional[datetime] = None
    certified: bool = Field(default=False)


class ProviderInfo(BaseModel):
    """Game provider information."""
    name: str = Field(..., description="Provider name")
    games_count: Optional[int] = Field(None, ge=0)
    popular_games: List[str] = Field(default_factory=list)


class SecurityInfo(BaseModel):
    """Security measures and certifications."""
    ssl_certificate: bool = Field(default=False)
    encryption_type: Optional[str] = None
    two_factor_auth: bool = Field(default=False)
    responsible_gambling_tools: List[str] = Field(default_factory=list)
    data_protection_compliance: List[str] = Field(default_factory=list)


class WithdrawalInfo(BaseModel):
    """Withdrawal methods and policies."""
    method: str = Field(..., description="Withdrawal method name")
    min_amount: Optional[float] = Field(None, ge=0)
    max_amount: Optional[float] = Field(None, ge=0)
    processing_time: Optional[str] = None
    fees: Optional[str] = None


class ReviewInfo(BaseModel):
    """Casino review information."""
    source: str = Field(..., description="Review source/platform")
    rating: float = Field(..., ge=0, le=5, description="Rating out of 5")
    review_count: Optional[int] = Field(None, ge=0)
    positive_aspects: List[str] = Field(default_factory=list)
    negative_aspects: List[str] = Field(default_factory=list)
    review_date: Optional[datetime] = None


class CasinoData(BaseModel):
    """Complete casino information model."""
    name: str = Field(..., description="Casino name")
    url: Optional[HttpUrl] = None
    description: Optional[str] = None
    
    # Core data categories
    licenses: List[LicenseInfo] = Field(default_factory=list)
    rtp_info: List[RTpInfo] = Field(default_factory=list)
    fairness: List[FairnessInfo] = Field(default_factory=list)
    providers: List[ProviderInfo] = Field(default_factory=list)
    security: Optional[SecurityInfo] = None
    withdrawal_methods: List[WithdrawalInfo] = Field(default_factory=list)
    reviews: List[ReviewInfo] = Field(default_factory=list)
    
    # Metadata
    collection_date: datetime = Field(default_factory=utcnow)
    last_updated: Optional[datetime] = None
    data_completeness_score: Optional[float] = Field(None, ge=0, le=100)
    additional_info: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Example Casino",
                "url": "https://example-casino.com",
                "licenses": [
                    {
                        "authority": "Malta Gaming Authority",
                        "license_number": "MGA/B2C/123/2020",
                        "jurisdiction": "Malta",
                        "verified": True
                    }
                ],
                "rtp_info": [
                    {
                        "game_name": "Starburst",
                        "rtp_percentage": 96.1,
                        "game_category": "Slots",
                        "provider": "NetEnt"
                    }
                ]
            }
        }
