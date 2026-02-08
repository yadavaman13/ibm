"""
API v1 Router

Aggregates all endpoint routers
"""

from fastapi import APIRouter
from app.api.v1.endpoints import health, disease_detection, yield_prediction, weather, soil_analysis, chatbot, market_intelligence

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(disease_detection.router, prefix="/disease", tags=["Disease Detection"])
api_router.include_router(yield_prediction.router, prefix="/yield", tags=["Yield Prediction"])
api_router.include_router(weather.router, prefix="/weather", tags=["Weather"])
api_router.include_router(soil_analysis.router, prefix="/soil", tags=["Soil Analysis"])
api_router.include_router(chatbot.router, prefix="/chatbot", tags=["Chatbot"])
api_router.include_router(market_intelligence.router, prefix="/market", tags=["Market Intelligence"])
