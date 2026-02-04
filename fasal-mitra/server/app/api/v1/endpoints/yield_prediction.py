"""
Yield Prediction API Endpoints
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
import logging

from app.models.yield_models import (
    YieldPredictionRequest,
    YieldPredictionResponse,
    YieldGapRequest,
    YieldGapResponse,
    BenchmarkRequest,
    BenchmarkResponse
)
from app.models.common import ResponseModel
from app.services.yield_service import YieldPredictionService, get_yield_service

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/predict", response_model=ResponseModel)
async def predict_yield(
    request: YieldPredictionRequest,
    service: YieldPredictionService = Depends(get_yield_service)
):
    """
    Predict crop yield based on input parameters
    
    - **crop**: Crop name (e.g., Rice, Wheat)
    - **state**: State name (e.g., Punjab, Maharashtra)
    - **season**: Season (Kharif, Rabi, Summer, etc.)
    - **area**: Cultivated area in hectares
    - **fertilizer**: Fertilizer amount in kg/ha
    - **pesticide**: Pesticide amount in kg/ha
    
    Returns predicted yield with confidence interval
    """
    try:
        result = await service.predict_yield(request)
        
        return ResponseModel(
            success=True,
            message="Yield predicted successfully",
            data=result
        )
    
    except Exception as e:
        logger.error(f"Error in yield prediction: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/gap-analysis", response_model=ResponseModel)
async def analyze_yield_gap(
    request: YieldGapRequest,
    service: YieldPredictionService = Depends(get_yield_service)
):
    """
    Analyze yield gap compared to benchmarks
    
    **Supports TWO scenarios:**
    
    **Scenario 1 - Post-Harvest Analysis (Actual Yield Known):**
    ```json
    {
      "crop": "Wheat",
      "state": "Punjab",
      "season": "Rabi",
      "actual_yield": 2.1
    }
    ```
    Use this after harvest to see how you performed vs others.
    
    **Scenario 2 - Pre-Harvest Planning (Predict First):**
    ```json
    {
      "crop": "Wheat",
      "state": "Punjab",
      "season": "Rabi",
      "area": 50,
      "fertilizer": 20000,
      "pesticide": 300
    }
    ```
    Use this before/during season to plan and optimize.
    
    Returns gap analysis with improvement recommendations.
    """
    try:
        # Determine which scenario: actual yield or prediction?
        if request.actual_yield is not None:
            # Scenario 1: Post-harvest analysis with known yield
            yield_to_analyze = request.actual_yield
            analysis_type = "post_harvest"
            logger.info(f"Post-harvest gap analysis: actual_yield={yield_to_analyze}")
        
        elif request.area is not None:
            # Scenario 2: Pre-harvest planning - predict first
            prediction_request = YieldPredictionRequest(
                crop=request.crop,
                state=request.state,
                season=request.season or "Kharif",
                area=request.area,
                fertilizer=request.fertilizer or 0,
                pesticide=request.pesticide or 0,
                avg_temp_c=request.avg_temp_c,
                total_rainfall_mm=request.total_rainfall_mm,
                avg_humidity_percent=request.avg_humidity_percent
            )
            prediction = await service.predict_yield(prediction_request)
            yield_to_analyze = prediction['predicted_yield']
            analysis_type = "pre_harvest"
            logger.info(f"Pre-harvest gap analysis: predicted_yield={yield_to_analyze}")
        
        else:
            raise HTTPException(
                status_code=400,
                detail="Must provide either 'actual_yield' (post-harvest) or farming inputs 'area, fertilizer, pesticide' (pre-harvest)"
            )
        
        # Get benchmarks for comparison
        benchmark_request = BenchmarkRequest(
            crop=request.crop,
            state=request.state,
            season=request.season
        )
        benchmarks = service.get_benchmarks(benchmark_request)
        
        # Calculate gaps
        avg_yield = benchmarks.get('average_yield', 0)
        top_10 = benchmarks.get('top_10_percent', 0)
        top_25 = benchmarks.get('top_25_percent', 0)
        max_yield = benchmarks.get('max_yield_achieved', 0)
        
        gap_vs_avg = ((yield_to_analyze - avg_yield) / avg_yield * 100) if avg_yield > 0 else 0
        gap_vs_top10 = ((top_10 - yield_to_analyze) / top_10 * 100) if top_10> 0 else 0
        gap_vs_top25 = ((top_25 - yield_to_analyze) / top_25 * 100) if top_25 > 0 else 0
        
        # Generate recommendations based on gap
        recommendations = []
        
        if gap_vs_top10 > 30:
            recommendations.append("⚠️ Significant yield gap detected (>30% below top performers)")
            recommendations.append("Consider adopting best practices from top-performing farms")
        elif gap_vs_top10 > 15:
            recommendations.append("Moderate yield gap detected (15-30% below top performers)")
            recommendations.append("Room for improvement through better resource management")
        elif gap_vs_avg > 0:
            if analysis_type == "post_harvest":
                recommendations.append("✅ Your yield is above regional average!")
            else:
                recommendations.append("✅ Your predicted yield is above regional average!")
            recommendations.append("Continue current practices and optimize further")
        else:
            if analysis_type == "post_harvest":
                recommendations.append("⚠️ Your yield is below regional average")
            else:
                recommendations.append("⚠️ Predicted yield is below regional average")
            recommendations.append("Review fertilizer and pesticide application rates")
        
        # Specific recommendations (only for pre-harvest)
        if analysis_type == "pre_harvest" and request.fertilizer is not None:
            if request.fertilizer < avg_yield * 300:
                recommendations.append("💡 Consider increasing fertilizer application gradually")
        
        if gap_vs_top10 > 20:
            recommendations.append("💡 Consult with agricultural extension officers for advanced techniques")
            recommendations.append("💡 Consider soil testing for precise nutrient management")
        
        result = {
            "analysis_type": analysis_type,
            "yield_analyzed": round(yield_to_analyze, 2),
            "current_yield": round(yield_to_analyze, 2),  # For compatibility
            "predicted_yield": round(yield_to_analyze, 2) if analysis_type == "pre_harvest" else None,
            "actual_yield": round(yield_to_analyze, 2) if analysis_type == "post_harvest" else None,
            "potential_yield": round(top_10, 2),
            "average_yield": round(avg_yield, 2),
            "gap_percentage": round(gap_vs_top10, 2),
            "gap_vs_average": round(gap_vs_avg, 2),
            "performance_level": "Excellent" if gap_vs_avg > 20 else "Good" if gap_vs_avg > 0 else "Below Average",
            "benchmarks": {
                "average": round(avg_yield, 2),
                "top_25_percent": round(top_25, 2),
                "top_10_percent": round(top_10, 2),
                "maximum": round(max_yield, 2)
            },
            "top_performers": {
                "yield": round(top_10, 2),
                "practices": [
                    "Optimal fertilizer timing and split application",
                    "Integrated pest management",
                    "Precision irrigation scheduling",
                    "High-quality seed varieties"
                ]
            },
            "improvement_steps": recommendations,
            "estimated_increase": round(max(0, top_10 - yield_to_analyze), 2),
            "yield_potential_percentage": round((yield_to_analyze / top_10 * 100), 1) if top_10 > 0 else 0
        }
        
        return ResponseModel(
            success=True,
            message="Yield gap analysis completed",
            data=result
        )
    
    except Exception as e:
        logger.error(f"Error in yield gap analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/benchmarks", response_model=ResponseModel)
async def get_yield_benchmarks(
    request: BenchmarkRequest,
    service: YieldPredictionService = Depends(get_yield_service)
):
    """
    Get yield benchmarks for a crop in a specific region
    
    Returns statistical benchmarks including:
    - Average, median, max yields
    - Top performer thresholds
    - Historical trends
    """
    try:
        result = service.get_benchmarks(request)
        
        return ResponseModel(
            success=True,
            message="Benchmarks retrieved successfully",
            data=result
        )
    
    except Exception as e:
        logger.error(f"Error retrieving benchmarks: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/crops", response_model=ResponseModel)
async def get_available_crops(service: YieldPredictionService = Depends(get_yield_service)):
    """Get list of available crops"""
    crops = service.get_available_crops()
    
    return ResponseModel(
        success=True,
        message=f"Found {len(crops)} crops",
        data={"crops": crops}
    )


@router.get("/states", response_model=ResponseModel)
async def get_available_states(service: YieldPredictionService = Depends(get_yield_service)):
    """Get list of available states"""
    states = service.get_available_states()
    
    return ResponseModel(
        success=True,
        message=f"Found {len(states)} states",
        data={"states": states}
    )


@router.get("/seasons", response_model=ResponseModel)
async def get_available_seasons(service: YieldPredictionService = Depends(get_yield_service)):
    """Get list of available seasons"""
    seasons = service.get_available_seasons()
    
    return ResponseModel(
        success=True,
        message=f"Found {len(seasons)} seasons",
        data={"seasons": seasons}
    )
