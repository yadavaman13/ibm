"""
Market Intelligence API Endpoints

Provides endpoints for market price forecasting, comparison, and recommendations
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
import logging

from app.models.market_models import (
    ForecastRequest,
    ForecastResponse,
    MarketComparisonRequest,
    MarketComparisonResponse,
    RecommendationRequest,
    RecommendationResponse,
    CommoditiesResponse,
    InsightsResponse,
    MarketData
)
from app.models.common import ResponseModel
from app.services.market_intelligence_service import (
    MarketIntelligenceService,
    get_market_intelligence_service
)

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/commodities", response_model=ResponseModel)
async def get_available_commodities(
    service: MarketIntelligenceService = Depends(get_market_intelligence_service)
):
    """
    Get list of all available commodities with metadata
    
    Returns:
    - List of commodities with record count, date range, and category
    """
    try:
        commodities = service.get_available_commodities()
        
        return ResponseModel(
            success=True,
            message=f"Found {len(commodities)} commodities",
            data={
                'commodities': commodities,
                'total_count': len(commodities)
            }
        )
    
    except Exception as e:
        logger.error(f"Error fetching commodities: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/forecast", response_model=ResponseModel)
async def forecast_prices(
    request: ForecastRequest,
    service: MarketIntelligenceService = Depends(get_market_intelligence_service)
):
    """
    Forecast commodity prices for the next N days
    
    Parameters:
    - **commodity**: Commodity name (e.g., Cotton, Wheat, Potato)
    - **days**: Number of days to forecast (1-30, default: 7)
    - **district**: Optional district filter
    
    Returns:
    - Price forecasts with confidence intervals
    - Trend analysis (rising/falling/stable)
    - Moving averages
    """
    try:
        result = service.simple_forecast(
            commodity=request.commodity,
            days=request.days
        )
        
        if 'error' in result:
            raise HTTPException(status_code=404, detail=result['error'])
        
        return ResponseModel(
            success=True,
            message=f"Price forecast generated for {request.commodity}",
            data=result
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating forecast: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/compare", response_model=ResponseModel)
async def compare_markets(
    request: MarketComparisonRequest,
    service: MarketIntelligenceService = Depends(get_market_intelligence_service)
):
    """
    Compare prices across different markets for a commodity
    
    Parameters:
    - **commodity**: Commodity name
    - **date**: Optional date (YYYY-MM-DD format, defaults to latest)
    - **district**: Optional district filter
    - **variety**: Optional variety filter
    
    Returns:
    - List of markets with prices and arrival quantities
    - Sorted by modal price (highest first)
    """
    try:
        markets = service.get_market_comparison(
            commodity=request.commodity,
            date=request.date,
            district=request.district,
            variety=request.variety
        )
        
        if not markets:
            raise HTTPException(
                status_code=404, 
                detail=f"No market data found for {request.commodity}"
            )
        
        result = {
            'commodity': request.commodity,
            'date': request.date or 'latest',
            'markets': markets,
            'total_markets': len(markets)
        }
        
        return ResponseModel(
            success=True,
            message=f"Found {len(markets)} markets for {request.commodity}",
            data=result
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error comparing markets: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/recommend", response_model=ResponseModel)
async def get_market_recommendation(
    request: RecommendationRequest,
    service: MarketIntelligenceService = Depends(get_market_intelligence_service)
):
    """
    Get best market recommendations for selling
    
    Parameters:
    - **commodity**: Commodity name
    - **user_district**: Your current district (for distance calculation)
    - **quantity**: Quantity to sell in Metric Tonnes (for profit calculation)
    
    Returns:
    - Best market with scoring and reasoning
    - Top 3 alternative markets
    - Potential profit calculations
    - AI-powered insights
    """
    try:
        result = service.get_best_market_recommendation(
            commodity=request.commodity,
            user_district=request.user_district,
            quantity=request.quantity
        )
        
        if 'error' in result:
            raise HTTPException(status_code=404, detail=result['error'])
        
        return ResponseModel(
            success=True,
            message=f"Market recommendation generated for {request.commodity}",
            data=result
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating recommendation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/insights/{commodity}", response_model=ResponseModel)
async def get_commodity_insights(
    commodity: str,
    days: int = 30,
    service: MarketIntelligenceService = Depends(get_market_intelligence_service)
):
    """
    Get comprehensive insights for a commodity
    
    Parameters:
    - **commodity**: Commodity name
    - **days**: Number of recent days to analyze (default: 30)
    
    Returns:
    - Price statistics (min, max, avg, volatility)
    - Arrival statistics (supply trends)
    - Market coverage (districts, markets, varieties)
    - Price trend analysis
    - Top markets by price
    """
    try:
        result = service.get_commodity_insights(commodity, days)
        
        if not result:
            raise HTTPException(
                status_code=404, 
                detail=f"No data found for {commodity}"
            )
        
        return ResponseModel(
            success=True,
            message=f"Insights generated for {commodity}",
            data=result
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting insights: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health", response_model=ResponseModel)
async def health_check(
    service: MarketIntelligenceService = Depends(get_market_intelligence_service)
):
    """Health check for market intelligence service"""
    try:
        commodities = service.get_available_commodities()
        
        return ResponseModel(
            success=True,
            message="Market Intelligence service is healthy",
            data={
                'available_commodities': len(commodities),
                'status': 'operational'
            }
        )
    
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unavailable")
