"""
Market Intelligence Pydantic Models

Request and response models for market intelligence endpoints
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ForecastRequest(BaseModel):
    """Request model for price forecasting"""
    commodity: str = Field(..., description="Commodity name (e.g., Cotton, Wheat, Potato)")
    days: int = Field(default=7, ge=1, le=30, description="Number of days to forecast")
    district: Optional[str] = Field(None, description="Filter by specific district")


class PriceForecast(BaseModel):
    """Individual price forecast for a date"""
    date: str
    predicted_price: float
    lower_bound: float
    upper_bound: float


class TrendInfo(BaseModel):
    """Price trend information"""
    direction: str  # 'rising', 'falling', 'stable'
    slope: float
    ma_7: Optional[float] = None
    ma_14: Optional[float] = None
    change_percent: Optional[float] = None


class ForecastResponse(BaseModel):
    """Response model for price forecasting"""
    commodity: str
    current_price: float
    forecast: List[PriceForecast]
    trend: TrendInfo
    model: str
    last_updated: str


class MarketComparisonRequest(BaseModel):
    """Request model for market comparison"""
    commodity: str
    date: Optional[str] = Field(None, description="Date in YYYY-MM-DD format (defaults to latest)")
    district: Optional[str] = Field(None, description="Filter by district")
    variety: Optional[str] = Field(None, description="Filter by variety")


class MarketData(BaseModel):
    """Market price and arrival data"""
    district: str
    market: str
    variety: str
    modal_price: float
    min_price: float
    max_price: float
    arrival_quantity: float
    date: str
    price_unit: str
    score: Optional[float] = None
    reasoning: Optional[List[str]] = None


class MarketComparisonResponse(BaseModel):
    """Response model for market comparison"""
    commodity: str
    date: str
    markets: List[MarketData]
    total_markets: int


class RecommendationRequest(BaseModel):
    """Request model for market recommendations"""
    commodity: str
    user_district: Optional[str] = Field(None, description="User's current district for distance calculation")
    quantity: Optional[float] = Field(None, description="Quantity to sell in Metric Tonnes")


class RecommendationResponse(BaseModel):
    """Response model for market recommendations"""
    commodity: str
    best_market: MarketData
    alternatives: List[MarketData]
    market_average_price: float
    premium_percent: float
    potential_profit_per_quintal: float
    potential_total_profit: Optional[float] = None
    quantity_quintals: Optional[float] = None
    insights: List[str]


class CommodityInfo(BaseModel):
    """Commodity metadata"""
    name: str
    category: str
    record_count: int
    date_range: Optional[Dict[str, Any]] = None


class CommoditiesResponse(BaseModel):
    """Response model for available commodities"""
    commodities: List[CommodityInfo]
    total_count: int


class PriceStats(BaseModel):
    """Price statistics"""
    current_avg: float
    period_avg: float
    min: float
    max: float
    std: float


class ArrivalStats(BaseModel):
    """Arrival quantity statistics"""
    avg_daily: float
    total: float
    min: float
    max: float


class MarketInfo(BaseModel):
    """Market information"""
    total_districts: int
    total_markets: int
    varieties: List[str]


class TopMarket(BaseModel):
    """Top market by price"""
    market: str
    avg_price: float
    total_arrival: float


class InsightsResponse(BaseModel):
    """Response model for commodity insights"""
    commodity: str
    total_records: int
    recent_records: int
    date_range: Dict[str, str]
    price_stats: PriceStats
    arrival_stats: ArrivalStats
    markets: MarketInfo
    trend: Optional[TrendInfo] = None
    top_markets: List[TopMarket]
