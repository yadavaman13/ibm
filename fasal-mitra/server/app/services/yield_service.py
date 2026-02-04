"""
Yield Prediction Service

Ports logic from src/features/yield_gap_analyzer.py and multi_scenario_predictor.py
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Optional, Dict, List
import uuid
import logging
from functools import lru_cache
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

from app.core.data_loader import DataLoader, get_data_loader
from app.models.yield_models import (
    YieldPredictionRequest,
    YieldGapRequest,
    BenchmarkRequest
)

logger = logging.getLogger(__name__)


class YieldPredictionService:
    """Yield prediction and gap analysis service"""
    
    def __init__(self, data_loader: DataLoader):
        self.data_loader = data_loader
        self.model: Optional[RandomForestRegressor] = None
        self.label_encoders = {}
        self.feature_columns = []
        self.is_trained = False
        
        # Load datasets if not loaded
        if data_loader.crop_data is None:
            data_loader.load_datasets()
        
        # Train model on initialization
        self._train_model()
    
    def _train_model(self):
        """Train the yield prediction model"""
        try:
            logger.info("Training yield prediction model...")
            
            # Merge datasets if needed
            if self.data_loader.merged_data is None:
                self.data_loader.merge_datasets()
            
            data = self.data_loader.merged_data.dropna()
            
            # Define features
            categorical_features = ['crop', 'state', 'season']
            numerical_features = ['area', 'fertilizer', 'pesticide', 'avg_temp_c', 
                                'total_rainfall_mm', 'avg_humidity_percent', 'N', 'P', 'K', 'pH']
            
            self.feature_columns = categorical_features + numerical_features
            
            # Prepare features
            X = data[self.feature_columns].copy()
            y = data['yield'].values
            
            # Encode categorical variables
            for col in categorical_features:
                le = LabelEncoder()
                X[col] = le.fit_transform(X[col].astype(str))
                self.label_encoders[col] = le
            
            # Train model
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=15,
                min_samples_split=5,
                random_state=42,
                n_jobs=-1
            )
            
            self.model.fit(X_train, y_train)
            
            # Evaluate
            train_score = self.model.score(X_train, y_train)
            test_score = self.model.score(X_test, y_test)
            
            logger.info(f"✅ Model trained - Train R²: {train_score:.3f}, Test R²: {test_score:.3f}")
            self.is_trained = True
        
        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
            self.is_trained = False
    
    async def predict_yield(self, request: YieldPredictionRequest) -> Dict:
        """Predict crop yield"""
        if not self.is_trained:
            raise ValueError("Model not trained")
        
        try:
            # Prepare input
            input_data = {
                'crop': request.crop,
                'state': request.state,
                'season': request.season,
                'area': request.area,
                'fertilizer': request.fertilizer,
                'pesticide': request.pesticide
            }
            
            # Get default weather values if not provided
            if request.avg_temp_c is None or request.total_rainfall_mm is None or request.avg_humidity_percent is None:
                defaults = self._get_weather_defaults(request.state)
                input_data.update({
                    'avg_temp_c': request.avg_temp_c or defaults['temp'],
                    'total_rainfall_mm': request.total_rainfall_mm or defaults['rainfall'],
                    'avg_humidity_percent': request.avg_humidity_percent or defaults['humidity']
                })
            else:
                input_data.update({
                    'avg_temp_c': request.avg_temp_c,
                    'total_rainfall_mm': request.total_rainfall_mm,
                    'avg_humidity_percent': request.avg_humidity_percent
                })
            
            # Get soil data
            soil_data = self.data_loader.get_soil_data_for_state(request.state)
            if soil_data:
                input_data.update({
                    'N': soil_data.get('N', 50),
                    'P': soil_data.get('P', 25),
                    'K': soil_data.get('K', 30),
                    'pH': soil_data.get('pH', 6.5)
                })
            else:
                input_data.update({'N': 50, 'P': 25, 'K': 30, 'pH': 6.5})
            
            # Encode and predict
            X = pd.DataFrame([input_data])
            for col in ['crop', 'state', 'season']:
                X[col] = self.label_encoders[col].transform(X[col].astype(str))
            
            X = X[self.feature_columns]
            prediction = self.model.predict(X)[0]
            
            # Calculate confidence interval (using model's tree predictions)
            tree_predictions = np.array([tree.predict(X)[0] for tree in self.model.estimators_])
            lower_bound = np.percentile(tree_predictions, 10)
            upper_bound = np.percentile(tree_predictions, 90)
            
            # Generate recommendations
            recommendations = self._generate_yield_recommendations(request, prediction)
            
            response = {
                "prediction_id": str(uuid.uuid4()),
                "timestamp": datetime.now(),
                "input_params": request.dict(),
                "predicted_yield": round(prediction, 2),
                "confidence_interval": {
                    "lower": round(lower_bound, 2),
                    "upper": round(upper_bound, 2)
                },
                "factors_affecting": self._get_important_factors(),
                "recommendations": recommendations,
                "model_confidence": 0.85
            }
            
            return response
        
        except Exception as e:
            logger.error(f"Error in yield prediction: {str(e)}")
            raise
    
    async def analyze_yield_gap(self, request: YieldGapRequest) -> Dict:
        """Analyze yield gap"""
        benchmarks = self.get_benchmarks(
            BenchmarkRequest(
                crop=request.crop,
                state=request.state,
                season=request.season
            )
        )
        
        if 'error' in benchmarks:
            return benchmarks
        
        # Calculate gaps
        gaps = {
            'vs_average': round(benchmarks['average_yield'] - request.current_yield, 2),
            'vs_top_25': round(benchmarks['top_25_percent'] - request.current_yield, 2),
            'vs_top_10': round(benchmarks['top_10_percent'] - request.current_yield, 2),
            'vs_maximum': round(benchmarks['max_yield_achieved'] - request.current_yield, 2)
        }
        
        # Calculate percentile rank
        data = self.data_loader.filter_data(crop=request.crop, state=request.state, season=request.season)
        if not data.empty:
            yields = data['yield'].values
            percentile_rank = round((yields < request.current_yield).sum() / len(yields) * 100, 1)
        else:
            percentile_rank = 50.0
        
        # Improvement potential
        improvement_potential = max(0, round((benchmarks['top_10_percent'] - request.current_yield) / request.current_yield * 100, 1))
        
        response = {
            "analysis_id": str(uuid.uuid4()),
            "timestamp": datetime.now(),
            "current_yield": request.current_yield,
            "benchmarks": benchmarks,
            "gaps": gaps,
            "percentile_rank": percentile_rank,
            "improvement_potential": improvement_potential,
            "recommendations": self._generate_gap_recommendations(gaps, percentile_rank),
            "top_performers_characteristics": self._get_top_performer_characteristics(request.crop, request.state, request.season)
        }
        
        return response
    
    def get_benchmarks(self, request: BenchmarkRequest) -> Dict:
        """Get yield benchmarks"""
        data = self.data_loader.filter_data(
            crop=request.crop,
            state=request.state,
            season=request.season
        )
        
        if data.empty:
            return {
                'error': f'No data available for {request.crop} in {request.state}' + (f' during {request.season}' if request.season else ''),
                'available_seasons': self.data_loader.filter_data(crop=request.crop, state=request.state)['season'].str.strip().unique().tolist()
            }
        
        yields = data['yield'].values
        
        benchmarks = {
            'crop': request.crop,
            'state': request.state,
            'season': request.season,
            'total_records': len(data),
            'years_covered': f"{data['year'].min()}-{data['year'].max()}",
            'average_yield': round(np.mean(yields), 2),
            'median_yield': round(np.median(yields), 2),
            'top_10_percent': round(np.percentile(yields, 90), 2),
            'top_25_percent': round(np.percentile(yields, 75), 2),
            'max_yield_achieved': round(np.max(yields), 2),
            'yield_std': round(np.std(yields), 2)
        }
        
        return benchmarks
    
    def _get_weather_defaults(self, state: str) -> Dict:
        """Get default weather values for a state"""
        if self.data_loader.weather_data is not None:
            state_weather = self.data_loader.weather_data[
                self.data_loader.weather_data['state'].str.lower() == state.lower()
            ]
            if not state_weather.empty:
                return {
                    'temp': state_weather['avg_temp_c'].mean(),
                    'rainfall': state_weather['total_rainfall_mm'].mean(),
                    'humidity': state_weather['avg_humidity_percent'].mean()
                }
        
        return {'temp': 25.0, 'rainfall': 1000.0, 'humidity': 70.0}
    
    def _generate_yield_recommendations(self, request: YieldPredictionRequest, predicted_yield: float) -> List[str]:
        """Generate recommendations based on prediction"""
        return [
            f"Expected yield: {predicted_yield:.2f} tons/hectare",
            f"Based on {request.area} hectares, total production: {(predicted_yield * request.area):.2f} tons",
            "Monitor soil moisture regularly",
            "Apply fertilizer in split doses for better efficiency"
        ]
    
    def _generate_gap_recommendations(self, gaps: Dict, percentile: float) -> List[str]:
        """Generate recommendations based on yield gap"""
        recommendations = []
        
        if percentile < 25:
            recommendations.append("⚠️ Your yield is in bottom 25% - significant improvement needed")
        elif percentile < 50:
            recommendations.append("Your yield is below average - moderate improvement possible")
        elif percentile < 75:
            recommendations.append("Your yield is above average - good performance")
        else:
            recommendations.append("✅ Excellent! You're in top 25% of performers")
        
        if gaps['vs_top_10'] > 0:
            recommendations.append(f"Potential to increase yield by {gaps['vs_top_10']:.2f} tons/hectare")
        
        return recommendations
    
    def _get_important_factors(self) -> List[Dict]:
        """Get important factors affecting yield"""
        if not self.is_trained or not hasattr(self.model, 'feature_importances_'):
            return []
        
        importances = self.model.feature_importances_
        factors = []
        for i, col in enumerate(self.feature_columns):
            factors.append({
                'factor': col,
                'importance': round(float(importances[i]), 3)
            })
        
        return sorted(factors, key=lambda x: x['importance'], reverse=True)[:5]
    
    def _get_top_performer_characteristics(self, crop: str, state: str, season: Optional[str]) -> Dict:
        """Get characteristics of top performers"""
        data = self.data_loader.filter_data(crop=crop, state=state, season=season)
        
        if data.empty:
            return {}
        
        threshold = np.percentile(data['yield'], 80)
        top_performers = data[data['yield'] >= threshold]
        
        return {
            'avg_fertilizer': round(top_performers['fertilizer'].mean(), 0) if 'fertilizer' in top_performers.columns else None,
            'avg_area': round(top_performers['area'].mean(), 2) if 'area' in top_performers.columns else None,
            'count': len(top_performers)
        }
    
    def get_available_crops(self) -> List[str]:
        """Get available crops"""
        return self.data_loader.get_available_crops()
    
    def get_available_states(self) -> List[str]:
        """Get available states"""
        return self.data_loader.get_available_states()
    
    def get_available_seasons(self) -> List[str]:
        """Get available seasons"""
        return self.data_loader.get_available_seasons()


@lru_cache()
def get_yield_service() -> YieldPredictionService:
    """Get singleton instance of yield prediction service"""
    data_loader = get_data_loader()
    return YieldPredictionService(data_loader)
