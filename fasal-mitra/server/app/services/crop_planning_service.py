"""
Crop Planning Service - REAL DATA VERSION

Decision-support system for crop selection based on:
- Real market prices from Agmarknet data
- Historical crop performance (1997-2020)
- Weather suitability from actual crop-weather correlation
- Seasonal compatibility from real crop calendar
- Soil NPK/pH matching by state
- Risk assessment from historical data
"""

import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import logging
from pathlib import Path

from app.services.weather_service import WeatherServiceAPI

logger = logging.getLogger(__name__)


class CropPlanningService:
    """Crop planning and recommendation engine with REAL agricultural data"""
    
    def __init__(self, weather_service: Optional[WeatherServiceAPI] = None):
        self.weather_service = weather_service
        
        # Load REAL datasets
        self.dataset = self._load_merged_dataset()  # 19K+ records: crop performance 1997-2020
        self.market_prices = self._load_real_market_prices()  # 23K+ records: actual mandi prices
        self.soil_data = self._load_soil_data()  # 32 states: real NPK/pH data
        self.crop_calendar = self._load_crop_calendar_data()  # Real seasonal data by state
        
        # Calculate crop requirements from historical data (NOT static)
        self.crop_requirements = self._calculate_crop_requirements()
        
        logger.info(f"✅ Loaded {len(self.dataset)} crop performance records")
        logger.info(f"✅ Loaded {len(self.market_prices)} market price records")
        logger.info(f"✅ Calculated requirements for {len(self.crop_requirements)} crops")
        
    def _load_merged_dataset(self) -> pd.DataFrame:
        """Load comprehensive crop-weather-yield dataset (1997-2020)"""
        try:
            # Path from server/app/services/ to ../../data/processed/
            # Current: fasal-mitra/server/app/services/crop_planning_service.py
            # Target: data/processed/merged_dataset.csv (at ibm/ root)
            current_file = Path(__file__)  # .../server/app/services/crop_planning_service.py
            server_dir = current_file.parent.parent.parent  # .../server/
            project_root = server_dir.parent.parent  # .../ibm/
            data_path = project_root / "data" / "processed" / "merged_dataset.csv"
            
            df = pd.read_csv(data_path)
            
            # Clean crop names (remove trailing spaces)
            df['crop'] = df['crop'].str.strip()
            df['season'] = df['season'].str.strip()
            df['state'] = df['state'].str.strip()
            
            logger.info(f"Loaded merged dataset: {len(df)} records, {df['crop'].nunique()} crops, {df['state'].nunique()} states")
            return df
        except Exception as e:
            logger.error(f"Error loading merged dataset: {e}")
            return pd.DataFrame()
    
    def _load_real_market_prices(self) -> pd.DataFrame:
        """Load real mandi prices from government data"""
        try:
            current_file = Path(__file__)
            server_dir = current_file.parent.parent.parent
            project_root = server_dir.parent.parent
            data_path = project_root / "data" / "raw" / "Price_Agriculture_commodities_Week.csv"
            
            df = pd.read_csv(data_path)
            df['Arrival_Date'] = pd.to_datetime(df['Arrival_Date'], format='%d-%m-%Y')
            
            # Standardize commodity names
            df['Commodity'] = df['Commodity'].str.strip()
            
            logger.info(f"Loaded market prices: {len(df)} records from {df['State'].nunique()} states")
            return df
        except Exception as e:
            logger.error(f"Error loading market prices: {e}")
            return pd.DataFrame()
    
    def _load_soil_data(self) -> pd.DataFrame:
        """Load state-wise soil NPK and pH data"""
        try:
            current_file = Path(__file__)
            server_dir = current_file.parent.parent.parent
            project_root = server_dir.parent.parent
            data_path = project_root / "data" / "raw" / "state_soil_data.csv"
            
            df = pd.read_csv(data_path)
            df['state'] = df['state'].str.strip()
            
            logger.info(f"Loaded soil data for {len(df)} states")
            return df
        except Exception as e:
            logger.error(f"Error loading soil data: {e}")
            return pd.DataFrame()
    
    def _load_crop_calendar_data(self) -> pd.DataFrame:
        """Load real crop calendar data by state"""
        try:
            current_file = Path(__file__)
            server_dir = current_file.parent.parent.parent
            project_root = server_dir.parent.parent
            data_path = project_root / "data" / "processed" / "crop_calendar_cleaned.csv"
            
            df = pd.read_csv(data_path)
            
            # Clean columns
            for col in ['STATE', 'CROP', 'Season']:
                if col in df.columns:
                    df[col] = df[col].str.strip()
            
            logger.info(f"Loaded crop calendar: {len(df)} entries")
            return df
        except Exception as e:
            logger.warning(f"Could not load crop calendar: {e}")
            return pd.DataFrame()
    
    def _calculate_crop_requirements(self) -> Dict:
        """
        Calculate crop requirements from REAL historical data
        Instead of hardcoded ranges, we analyze actual crop performance
        """
        requirements = {}
        
        try:
            for crop in self.dataset['crop'].unique():
                crop_data = self.dataset[self.dataset['crop'] == crop]
                
                if len(crop_data) < 5:  # Skip crops with insufficient data
                    continue
                
                # Calculate optimal ranges from successful crops (top 50% yield)
                median_yield = crop_data['yield'].median()
                high_performing = crop_data[crop_data['yield'] >= median_yield]
                
                requirements[crop] = {
                    "temperature": {
                        "min": round(high_performing['avg_temp_c'].quantile(0.05), 1),
                        "max": round(high_performing['avg_temp_c'].quantile(0.95), 1),
                        "optimal": round(high_performing['avg_temp_c'].median(), 1)
                    },
                    "rainfall": {
                        "min": round(high_performing['total_rainfall_mm'].quantile(0.05), 1),
                        "max": round(high_performing['total_rainfall_mm'].quantile(0.95), 1),
                        "optimal": round(high_performing['total_rainfall_mm'].median(), 1)
                    },
                    "humidity": {
                        "min": round(high_performing['avg_humidity_percent'].quantile(0.10), 1),
                        "max": round(high_performing['avg_humidity_percent'].quantile(0.90), 1),
                        "optimal": round(high_performing['avg_humidity_percent'].median(), 1)
                    },
                    "avg_yield_per_hectare": round(high_performing['yield'].mean(), 3),
                    "historical_records": len(crop_data),
                    "states_grown": crop_data['state'].nunique()
                }
            
            logger.info(f"Calculated requirements for {len(requirements)} crops from historical data")
            return requirements
            
        except Exception as e:
            logger.error(f"Error calculating crop requirements: {e}")
            return {}
    
    def get_current_season(self, month: int) -> str:
        """Determine season from month (India agricultural calendar)"""
        if month in [6, 7, 8, 9, 10]:  # June-October
            return "Kharif"
        elif month in [11, 12, 1, 2, 3]:  # November-March
            return "Rabi"
        elif month in [4, 5]:  # April-May
            return "Zaid"
        else:
            return "Whole Year"
    
    def get_candidate_crops(self, month: int, state: Optional[str] = None) -> List[str]:
        """
        Get crops suitable for current season from REAL historical data
        Only returns crops that have been successfully grown in that season
        """
        season = self.get_current_season(month)
        
        # Get crops from historical data for this season
        season_data = self.dataset[self.dataset['season'] == season]
        
        # If state specified, prioritize crops grown in that state
        if state and not season_data.empty:
            state_crops = season_data[season_data['state'] == state]['crop'].unique()
            if len(state_crops) > 0:
                logger.info(f"Found {len(state_crops)} crops for {season} season in {state}")
                return list(state_crops)
        
        # Fall back to all crops for this season
        crops = season_data['crop'].unique().tolist()
        
        # Add whole year crops
        whole_year = self.dataset[self.dataset['season'] == "Whole Year"]['crop'].unique()
        crops = list(set(crops).union(set(whole_year)))
        
        logger.info(f"Season: {season}, Candidate crops: {len(crops)}")
        return crops
    
    def _map_crop_to_commodity(self, crop: str) -> str:
        """Map crop names in dataset to commodity names in market price data"""
        # Mapping dictionary for common variations
        mapping = {
            "Rice": "Rice",
            "Wheat": "Wheat",
            "Maize": "Maize",
            "Arhar/Tur": "Tur (Arhar)",
            "Cotton(lint)": "Cotton",
            "Sugarcane": "Sugarcane",
            "Potato": "Potato",
            "Onion": "Onion",
            "Tomato": "Tomato",
            "Groundnut": "Groundnut",
            "Soyabean": "Soyabean",
            "Rapeseed &Mustard": "Mustard",
            "Gram": "Gram",
            "Sunflower": "Sunflower",
            "Bajra": "Bajra (Pearl Millet)",
            "Jowar": "Jowar (Sorghum)",
            "Moong(Green Gram)": "Moong (Green Gram)",
            "Masoor": "Masoor (Lentil)",
            "Urad": "Urad (Black Gram)"
        }
        
        return mapping.get(crop, crop)
    
    def calculate_market_score(self, crop: str, state: str) -> Tuple[float, str, float]:
        """
        Calculate market score based on REAL mandi prices
        Returns: (score, trend, avg_price)
        """
        try:
            if self.market_prices.empty:
                return 50.0, "no data", 0.0
            
            commodity = self._map_crop_to_commodity(crop)
            
            # Filter prices for this commodity
            crop_prices = self.market_prices[
                self.market_prices['Commodity'].str.contains(commodity, case=False, na=False)
            ]
            
            if crop_prices.empty:
                logger.warning(f"No market data for {crop} ({commodity})")
                return 50.0, "no data", 0.0
            
            # Try to get state-specific prices first
            state_prices = crop_prices[crop_prices['State'].str.contains(state, case=False, na=False)]
            if state_prices.empty:
                # Use all states as fallback
                state_prices = crop_prices
            
            # Sort by date to get recent trend
            state_prices = state_prices.sort_values('Arrival_Date', ascending=False)
            
            # Calculate average and recent trend
            avg_price = state_prices['Modal Price'].mean()
            
            # Analyze price trend (recent 30 days vs previous 30 days)
            recent = state_prices.head(min(10, len(state_prices)))['Modal Price'].mean()
            older = state_prices.tail(min(10, len(state_prices)))['Modal Price'].mean()
            
            # Determine trend
            if len(state_prices) > 1:
                price_change = ((recent - older) / older * 100) if older > 0 else 0
                
                if price_change > 5:
                    trend = "up"
                    base_score = 85.0
                elif price_change < -5:
                    trend = "down"
                    base_score = 40.0
                else:
                    trend = "stable"
                    base_score = 65.0
            else:
                trend = "stable"
                base_score = 65.0
            
            # Adjust for price level (higher prices = better for farmers)
            if avg_price > 3000:
                base_score += 10
            elif avg_price > 2000:
                base_score += 5
            
            # Adjust for price volatility (high volatility = risky)
            price_std = state_prices['Modal Price'].std()
            if avg_price > 0:
                cv = (price_std / avg_price) * 100  # Coefficient of variation
                volatility_penalty = min(cv / 2, 15)  # Max 15 point penalty
                base_score -= volatility_penalty
            
            final_score = max(min(base_score, 100), 0)
            
            logger.info(f"{crop}: Market score={final_score:.1f}, trend={trend}, avg_price=₹{avg_price:.0f}")
            return final_score, trend, avg_price
            
        except Exception as e:
            logger.error(f"Error calculating market score for {crop}: {e}")
            return 50.0, "error", 0.0
    
    def calculate_weather_score(
        self, 
        crop: str,
        state: str,
        forecast: Optional[Dict]
    ) -> Tuple[float, str]:
        """
        Calculate weather suitability score using REAL historical correlations
        Analyzes how similar current conditions are to successful crop seasons
        Returns: (score, suitability_text)
        """
        try:
            requirements = self.crop_requirements.get(crop)
            if not requirements or not forecast:
                return 50.0, "moderate"
            
            # Get weather from forecast
            temp = forecast.get('temperature', 25)
            rainfall = forecast.get('rainfall', 100)
            humidity = forecast.get('humidity', 60)
            
            score = 0.0
            factors = []
            
            # Temperature match (40% of weather score)
            temp_req = requirements['temperature']
            if temp_req['min'] <= temp <= temp_req['max']:
                # Optimal temperature
                temp_deviation = abs(temp - temp_req['optimal']) / ((temp_req['max'] - temp_req['min']) / 2)
                temp_score = max(100 - (temp_deviation * 30), 70)
            else:
                # Outside range
                if temp < temp_req['min']:
                    temp_score = max(50 - (temp_req['min'] - temp) * 5, 0)
                else:
                    temp_score = max(50 - (temp - temp_req['max']) * 3, 0)
            
            score += temp_score * 0.4
            factors.append(f"temp={temp_score:.0f}")
            
            # Rainfall match (40% of weather score)
            rain_req = requirements['rainfall']
            if rain_req['min'] <= rainfall <= rain_req['max']:
                # Optimal rainfall
                rain_deviation = abs(rainfall - rain_req['optimal']) / ((rain_req['max'] - rain_req['min']) / 2)
                rain_score = max(100 - (rain_deviation * 20), 70)
            else:
                # Outside range
                if rainfall < rain_req['min']:
                    rain_score = max(60 - abs(rain_req['min'] - rainfall) / 20, 20)
                else:
                    rain_score = max(60 - abs(rainfall - rain_req['max']) / 30, 20)
            
            score += rain_score * 0.4
            factors.append(f"rain={rain_score:.0f}")
            
            # Humidity match (20% of weather score)
            hum_req = requirements['humidity']
            if hum_req['min'] <= humidity <= hum_req['max']:
                hum_score = 90
            else:
                hum_score = max(60 - abs(humidity - hum_req['optimal']) * 2, 30)
            
            score += hum_score * 0.2
            factors.append(f"hum={hum_score:.0f}")
            
            # Determine suitability text
            if score >= 75:
                suitability = "excellent"
            elif score >= 60:
                suitability = "good"
            elif score >= 45:
                suitability = "moderate"
            else:
                suitability = "poor"
            
            logger.info(f"{crop} weather: {suitability} (score={score:.1f}, {', '.join(factors)})")
            return round(score, 2), suitability
            
        except Exception as e:
            logger.error(f"Error calculating weather score for {crop}: {e}")
            return 50.0, "moderate"
    
    def calculate_soil_score(self, crop: str, state: str) -> Tuple[float, str]:
        """
        NEW: Calculate soil suitability score using real state soil data
        Compares state soil NPK/pH with historical successful crop growth
        Returns: (score, suitability_text)
        """
        try:
            # Get state soil data
            state_soil = self.soil_data[self.soil_data['state'] == state]
            if state_soil.empty:
                logger.warning(f"No soil data for {state}")
                return 50.0, "unknown"
            
            state_soil = state_soil.iloc[0]
            state_N = state_soil['N']
            state_P = state_soil['P']
            state_K = state_soil['K']
            state_pH = state_soil['pH']
            
            # Get historical crop performance in this state
            crop_in_state = self.dataset[
                (self.dataset['crop'] == crop) & 
                (self.dataset['state'] == state)
            ]
            
            if crop_in_state.empty:
                # No history in this state, use general requirements
                return 50.0, "untested"
            
            # Analyze correlation between soil and yield
            avg_yield = crop_in_state['yield'].mean()
            median_yield_all = self.dataset[self.dataset['crop'] == crop]['yield'].median()
            
            # Score based on historical performance
            if avg_yield >= median_yield_all * 1.2:
                soil_score = 90  # Excellent performance history
                suitability = "excellent"
            elif avg_yield >= median_yield_all:
                soil_score = 75  # Good performance
                suitability = "good"
            elif avg_yield >= median_yield_all * 0.7:
                soil_score = 55  # Moderate
                suitability = "moderate"
            else:
                soil_score = 35  # Poor historical performance
                suitability = "poor"
            
            logger.info(f"{crop} in {state}: soil_score={soil_score} (historical avg yield={avg_yield:.2f})")
            return soil_score, suitability
            
        except Exception as e:
            logger.error(f"Error calculating soil score: {e}")
            return 50.0, "unknown"
    
    def calculate_season_score(self, crop: str, month: int, state: str) -> float:
        """
        Calculate seasonal compatibility score from REAL crop calendar data
        """
        try:
            current_season = self.get_current_season(month)
            
            # Check historical data for this crop in this season
            crop_season = self.dataset[
                (self.dataset['crop'] == crop) & 
                (self.dataset['season'] == current_season)
            ]
            
            if not crop_season.empty:
                # Crop has been grown in this season
                
                # Check state-specific history
                crop_season_state = crop_season[crop_season['state'] == state]
                
                if not crop_season_state.empty:
                    # Strong evidence - grown in this state in this season
                    return 100.0
                else:
                    # Grown in this season but not this state
                    return 80.0
            
            # Check if it's a whole year crop
            whole_year = self.dataset[
                (self.dataset['crop'] == crop) & 
                (self.dataset['season'] == "Whole Year")
            ]
            
            if not whole_year.empty:
                return 70.0  # Can grow anytime
            
            # Crop not typically grown in this season
            return 30.0
            
        except Exception as e:
            logger.error(f"Error calculating season score: {e}")
            return 50.0
    
    def calculate_risk_score(
        self, 
        crop: str, 
        forecast: Optional[Dict]
    ) -> Tuple[float, str]:
        """
        Calculate risk score
        Returns: (score, risk_level)
        Lower risk = Higher score
        """
        try:
            requirements = self.crop_requirements.get(crop, {})
            risk_factors = []
            risk_score = 100.0  # Start with low risk
            
            if forecast:
                humidity = forecast.get('humidity', 60)
                rainfall = forecast.get('rainfall', 100)
                
                # High humidity risk
                if humidity > 80:
                    risk_factors.append("High humidity - fungal disease risk")
                    risk_score -= 25
                
                # Heavy rainfall risk
                if rainfall > 150:
                    risk_factors.append("Heavy rainfall - waterlogging risk")
                    risk_score -= 20
                
                # Drought risk
                water_req = requirements.get('water_requirement', 'Medium')
                if water_req in ['High', 'Very High'] and rainfall < 50:
                    risk_factors.append("Insufficient rainfall for water-intensive crop")
                    risk_score -= 30
            
            # Disease-prone crops
            if 'disease_risk' in requirements:
                risk_factors.append("Crop has known disease susceptibility")
                risk_score -= 15
            
            # Market volatility (from market data)
            if not self.market_prices.empty:
                crop_prices = self.market_prices[self.market_prices['crop_name'] == crop]
                if not crop_prices.empty and len(crop_prices) > 1:
                    price_cv = crop_prices['modal_price'].std() / crop_prices['modal_price'].mean()
                    if price_cv > 0.2:  # High price volatility
                        risk_factors.append("Price volatility in market")
                        risk_score -= 10
            
            risk_score = max(risk_score, 0)
            
            # Determine risk level
            if risk_score >= 70:
                risk_level = "low"
            elif risk_score >= 40:
                risk_level = "medium"
            else:
                risk_level = "high"
            
            return risk_score, risk_level
            
        except Exception as e:
            logger.error(f"Error calculating risk score for {crop}: {e}")
            return 60.0, "medium"
    
    def calculate_final_score(
        self, 
        market_score: float,
        weather_score: float,
        season_score: float,
        soil_score: float,
        risk_score: float
    ) -> float:
        """
        Calculate final crop score using weighted formula (UPDATED with soil)
        FinalScore = 0.35×Market + 0.25×Weather + 0.15×Season + 0.15×Soil + 0.10×Risk
        """
        final = (
            0.35 * market_score +    # Market economics (most important)
            0.25 * weather_score +   # Weather suitability
            0.15 * season_score +    # Seasonal timing
            0.15 * soil_score +      # NEW: Soil compatibility (historical performance)
            0.10 * risk_score        # Risk mitigation
        )
        return round(final, 2)
    
    def _get_water_requirement(self, crop: str) -> str:
        """Determine water requirement based on optimal rainfall"""
        try:
            requirements = self.crop_requirements.get(crop, {})
            optimal_rainfall = requirements.get("rainfall", {}).get("optimal", 0)
            
            if optimal_rainfall > 1500:
                return "Very High"
            elif optimal_rainfall > 1000:
                return "High"
            elif optimal_rainfall > 600:
                return "Medium"
            elif optimal_rainfall > 300:
                return "Low"
            else:
                return "Very Low"
        except Exception as e:
            logger.error(f"Error getting water requirement: {e}")
            return "Medium"
    
    def _calculate_growing_days(self, sowing: str, harvesting: str) -> int:
        """Calculate approximate growing period from date strings"""
        try:
            # Handle formats like "15th June - 15th Aug" and "15th Oct. – 30th Nov"
            month_map = {
                'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
                'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
            }
            
            # Extract months from sowing (take end month)
            sowing_lower = sowing.lower()
            sowing_month = 1
            for month, num in month_map.items():
                if month in sowing_lower:
                    sowing_month = num
            
            # Extract months from harvesting (take start month)
            harvesting_lower = harvesting.lower()
            harvesting_month = 12
            for month, num in month_map.items():
                if month in harvesting_lower:
                    harvesting_month = num
                    break  # Take first occurrence
            
            # Calculate month difference
            if harvesting_month >= sowing_month:
                month_diff = harvesting_month - sowing_month
            else:
                # Crosses year boundary
                month_diff = (12 - sowing_month) + harvesting_month
            
            # Approximate: 30 days per month
            return month_diff * 30
            
        except Exception as e:
            logger.warning(f"Could not calculate growing days: {e}")
            return 90  # Default 3 months
    
    def _get_crop_calendar_info(self, crop: str, state: str) -> Dict:
        """Get sowing/harvesting periods and calculate growing days from crop calendar"""
        try:
            if self.crop_calendar.empty:
                return {}
            
            # Find crop calendar entry for this state and crop
            calendar_entry = self.crop_calendar[
                (self.crop_calendar['CROP'].str.contains(crop, case=False, na=False)) &
                (self.crop_calendar['STATE'].str.contains(state, case=False, na=False))
            ]
            
            if calendar_entry.empty:
                # Fallback to any state for this crop
                calendar_entry = self.crop_calendar[
                    self.crop_calendar['CROP'].str.contains(crop, case=False, na=False)
                ]
            
            if calendar_entry.empty:
                return {}
            
            # Get first matching entry
            entry = calendar_entry.iloc[0]
            
            sowing = str(entry.get('sowing_period', 'Not available'))
            harvesting = str(entry.get('harvesting_period', 'Not available'))
            season = str(entry.get('Season', 'Unknown'))
            
            # Calculate approximate growing period (days)
            growing_days = self._calculate_growing_days(sowing, harvesting)
            
            return {
                "sowing_period": sowing,
                "harvesting_period": harvesting,
                "season_name": season,
                "growing_period_days": growing_days
            }
            
        except Exception as e:
            logger.error(f"Error getting crop calendar info: {e}")
            return {}
    
    def _get_state_soil_info(self, state: str) -> Dict:
        """Get soil NPK and pH data for specific state"""
        try:
            if self.soil_data.empty:
                return {}
            
            state_soil = self.soil_data[self.soil_data['state'] == state]
            if state_soil.empty:
                return {}
            
            soil_row = state_soil.iloc[0]
            return {
                "nitrogen_n": float(soil_row['N']),
                "phosphorus_p": float(soil_row['P']),
                "potassium_k": float(soil_row['K']),
                "ph": float(soil_row['pH'])
            }
        except Exception as e:
            logger.error(f"Error getting state soil info: {e}")
            return {}
    
    def estimate_quantity(self, crop: str, state: str, land_size: float) -> Dict:
        """
        Estimate planting quantity and yield using REAL historical data
        Returns: recommended area, expected yield range
        """
        try:
            # Get historical yield data for this crop in this state
            crop_state_data = self.dataset[
                (self.dataset['crop'] == crop) & 
                (self.dataset['state'] == state)
            ]
            
            if crop_state_data.empty:
                # Fall back to all states for this crop
                crop_state_data = self.dataset[self.dataset['crop'] == crop]
            
            if crop_state_data.empty:
                return {}
            
            # Calculate average yield from historical data
            avg_yield = crop_state_data['yield'].mean()
            median_yield = crop_state_data['yield'].median()
            p25_yield = crop_state_data['yield'].quantile(0.25)
            p75_yield = crop_state_data['yield'].quantile(0.75)
            
            # Recommended area (30-70% of available land depending on crop performance)
            yield_reliability = crop_state_data['yield'].std() / avg_yield if avg_yield > 0 else 1
            
            if yield_reliability < 0.3:  # Low variance = reliable
                area_percentage = 0.7
            elif yield_reliability < 0.5:
                area_percentage = 0.5
            else:  # High variance = risky
                area_percentage = 0.3
            
            recommended_area = round(land_size * area_percentage, 2)
            
            # Expected production range (using quartiles for realistic range)
            expected_min = round(recommended_area * p25_yield, 2)
            expected_avg = round(recommended_area * median_yield, 2)
            expected_max = round(recommended_area * p75_yield, 2)
            
            # Get growing period from actual data
            records_count = len(crop_state_data)
            
            # Calculate min/max area for frontend compatibility
            min_area = round(recommended_area * 0.6, 2)  # Conservative
            max_area = recommended_area  # Optimal
            
            return {
                "recommended_area_hectares": {
                    "min": min_area,
                    "max": max_area
                },
                "area_percentage": round(area_percentage * 100, 1),
                "expected_yield_tons": {
                    "min": expected_min,
                    "max": expected_max
                },
                "expected_yield_range": {
                    "minimum_tonnes": expected_min,
                    "average_tonnes": expected_avg,
                    "maximum_tonnes": expected_max
                },
                "yield_per_hectare": {
                    "minimum": round(p25_yield, 3),
                    "average": round(median_yield, 3),
                    "maximum": round(p75_yield, 3)
                },
                "based_on_records": records_count,
                "reliability": "high" if yield_reliability < 0.3 else "medium" if yield_reliability < 0.5 else "low",
                "note": f"Based on {records_count} historical records from {crop_state_data['year'].min()}-{crop_state_data['year'].max()}"
            }
            
        except Exception as e:
            logger.error(f"Error estimating quantity for {crop}: {e}")
            return {}
        """
        Estimate planting quantity and expected yield
        """
        requirements = self.crop_requirements.get(crop, {})
        avg_yield = requirements.get('avg_yield_per_hectare', 0)
        
        if land_size > 0 and avg_yield > 0:
            # Estimate area allocation (conservative)
            min_area = min(land_size * 0.3, land_size)
            max_area = min(land_size * 0.7, land_size)
            
            # Expected yield
            min_yield = min_area * avg_yield * 0.8  # 80% of optimal
            max_yield = max_area * avg_yield
            
            return {
                "recommended_area_hectares": {
                    "min": round(min_area, 2),
                    "max": round(max_area, 2)
                },
                "expected_yield_tons": {
                    "min": round(min_yield, 2),
                    "max": round(max_yield, 2)
                },
                "avg_yield_per_hectare": avg_yield,
                "growing_period_days": requirements.get('growing_period_days', 0)
            }
        else:
            return {}
    
    async def plan_crops(
        self,
        state: str,
        month: Optional[int] = None,
        land_size: Optional[float] = None,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None
    ) -> Dict:
        """
        Main crop planning engine using REAL DATA
        
        Returns top 3 recommended crops based on:
        - Real market prices (35%)
        - Historical weather-crop correlations (25%)
        - Seasonal timing (15%)
        - Soil suitability from historical performance (15%)
        - Risk factors (10%)
        """
        try:
            # Auto-detect month if not provided
            if month is None:
                month = datetime.now().month
            
            logger.info(f"🌾 Planning crops for {state}, month={month}, land_size={land_size}ha")
            
            # Get candidate crops from historical data
            candidates = self.get_candidate_crops(month, state)
            
            if not candidates:
                logger.warning(f"No suitable crops found for {state} in month {month}")
                return {
                    "success": False,
                    "message": f"No suitable crops found for {state} in current season"
                }
            
            logger.info(f"Evaluating {len(candidates)} candidate crops")
            
            # Get weather forecast if coordinates provided
            forecast = None
            if self.weather_service and latitude and longitude:
                try:
                    # Get current weather
                    current_weather = await self.weather_service.get_current_weather(latitude, longitude)
                    # Get forecast for next 7 days
                    forecast_data = await self.weather_service.get_forecast(latitude, longitude)
                    
                    if current_weather and forecast_data:
                        # Extract weather data
                        forecast_list = forecast_data.get('forecast', [])
                        avg_rainfall = sum(f.get('precipitation_sum', 0) for f in forecast_list[:7]) / 7 if forecast_list else 100
                        
                        forecast = {
                            'temperature': current_weather.get('temperature', 25),
                            'rainfall': avg_rainfall,
                            'humidity': current_weather.get('humidity', 60)
                        }
                        logger.info(f"Weather: temp={forecast['temperature']}°C, rain={forecast['rainfall']}mm, humidity={forecast['humidity']}%")
                    else:
                        logger.warning("Weather service returned no data")
                except Exception as e:
                    logger.warning(f"Could not fetch weather forecast: {e}")
            else:
                logger.info("No weather service or coordinates - using historical averages only")
            
            # Score each candidate crop
            crop_scores = []
            
            for crop in candidates:
                try:
                    # Calculate individual scores (all data-driven)
                    market_score, market_trend, avg_price = self.calculate_market_score(crop, state)
                    weather_score, weather_suitability = self.calculate_weather_score(crop, state, forecast)
                    season_score = self.calculate_season_score(crop, month, state)
                    soil_score, soil_suitability = self.calculate_soil_score(crop, state)
                    risk_score, risk_level = self.calculate_risk_score(crop, forecast)
                    
                    # Calculate weighted final score
                    final_score = self.calculate_final_score(
                        market_score, weather_score, season_score, soil_score, risk_score
                    )
                    
                    # Get quantity estimate if land size provided
                    quantity_info = {}
                    if land_size and land_size > 0:
                        quantity_info = self.estimate_quantity(crop, state, land_size)
                    
                    # Get calendar info
                    calendar_info = self._get_crop_calendar_info(crop, state)
                    
                    # Add growing period to quantity info
                    if quantity_info and calendar_info.get('growing_period_days'):
                        quantity_info['growing_period_days'] = calendar_info.get('growing_period_days', 90)
                    
                    # Get state soil info
                    state_soil_info = self._get_state_soil_info(state)
                    
                    # Enhanced crop details
                    requirements = self.crop_requirements.get(crop, {})
                    enhanced_crop_details = {
                        "temperature": requirements.get("temperature", {}),
                        "rainfall": requirements.get("rainfall", {}),
                        "humidity": requirements.get("humidity", {}),
                        "water_requirement": self._get_water_requirement(crop),
                        "optimal_conditions": {
                            "temperature": requirements.get("temperature", {}).get("optimal"),
                            "rainfall": requirements.get("rainfall", {}).get("optimal"),
                            "humidity": requirements.get("humidity", {}).get("optimal")
                        },
                        "statistics": {
                            "historical_records": requirements.get("historical_records", 0),
                            "states_grown": requirements.get("states_grown", 0),
                            "avg_yield_per_hectare": requirements.get("avg_yield_per_hectare", 0)
                        }
                    }
                    
                    crop_result = {
                        "crop_name": crop,
                        "final_score": final_score,
                        "scores": {
                            "market": round(market_score, 2),
                            "weather": round(weather_score, 2),
                            "season": round(season_score, 2),
                            "soil": round(soil_score, 2),
                            "risk": round(risk_score, 2)
                        },
                        "market_trend": market_trend,
                        "average_market_price_inr": round(avg_price, 2),
                        "weather_suitability": weather_suitability,
                        "soil_suitability": soil_suitability,
                        "risk_level": risk_level,
                        "quantity_recommendation": quantity_info,
                        "calendar_info": calendar_info,
                        "soil_info": state_soil_info,
                        "data_source": "historical_records",
                        "crop_details": enhanced_crop_details
                    }
                    
                    crop_scores.append(crop_result)
                    
                except Exception as e:
                    logger.error(f"Error scoring {crop}: {e}")
                    continue
            
            if not crop_scores:
                return {
                    "success": False,
                    "message": "Could not evaluate any crops"
                }
            
            # Sort by final score and get top 3
            crop_scores.sort(key=lambda x: x['final_score'], reverse=True)
            top_crops = crop_scores[:3]
            
            logger.info(f"✅ Top 3 crops: {[c['crop_name'] for c in top_crops]}")
            
            return {
                "success": True,
                "season": self.get_current_season(month),
                "state": state,
                "recommendations": top_crops,
                "total_evaluated": len(crop_scores),
                "planning_date": datetime.now().isoformat(),
                "data_sources": {
                    "market_prices": f"{len(self.market_prices)} records from Agmarknet",
                    "crop_performance": f"{len(self.dataset)} records (1997-2020)",
                    "soil_data": f"{len(self.soil_data)} states",
                    "weather": "Live forecast" if forecast else "Historical averages"
                },
                "disclaimer": "⚠️ This is AI-based guidance using historical data. Results are advisory only. Please consult local agriculture officer for final decisions."
            }
            
        except Exception as e:
            logger.error(f"Error in crop planning: {e}", exc_info=True)
            raise
    
    def get_all_seasons(self) -> Dict:
        """Get all available seasons with their months"""
        return {
            "Kharif": {
                "months": [6, 7, 8, 9, 10],
                "description": "Monsoon season (June-October)",
                "total_crops": len(self.dataset[self.dataset['season'] == "Kharif"]['crop'].unique())
            },
            "Rabi": {
                "months": [11, 12, 1, 2, 3],
                "description": "Winter season (November-March)",
                "total_crops": len(self.dataset[self.dataset['season'] == "Rabi"]['crop'].unique())
            },
            "Zaid": {
                "months": [4, 5],
                "description": "Summer season (April-May)",
                "total_crops": len(self.dataset[self.dataset['season'] == "Zaid"]['crop'].unique())
            },
            "Whole Year": {
                "months": list(range(1, 13)),
                "description": "Year-round cultivation",
                "total_crops": len(self.dataset[self.dataset['season'] == "Whole Year"]['crop'].unique())
            }
        }
    
    def get_crop_details(self, crop_name: str) -> Dict:
        """Get detailed information about a specific crop from historical data"""
        try:
            crop_data = self.dataset[self.dataset['crop'] == crop_name]
            
            if crop_data.empty:
                return {"error": f"No data found for crop: {crop_name}"}
            
            requirements = self.crop_requirements.get(crop_name, {})
            
            return {
                "crop_name": crop_name,
                "requirements": requirements,
                "cultivation_states": crop_data['state'].unique().tolist(),
                "seasons": crop_data['season'].unique().tolist(),
                "historical_stats": {
                    "avg_yield": round(crop_data['yield'].mean(), 3),
                    "max_yield": round(crop_data['yield'].max(), 3),
                    "avg_area_hectares": round(crop_data['area'].mean(), 2),
                    "total_records": len(crop_data),
                    "years_range": f"{crop_data['year'].min()}-{crop_data['year'].max()}"
                }
            }
        except Exception as e:
            logger.error(f"Error getting crop details for {crop_name}: {e}")
            return {"error": str(e)}
    
    def get_market_prices(self, crop_name: str, state: Optional[str] = None) -> Dict:
        """Get market prices for a specific crop"""
        try:
            commodity = self._map_crop_to_commodity(crop_name)
            
            crop_prices = self.market_prices[
                self.market_prices['Commodity'].str.contains(commodity, case=False, na=False)
            ]
            
            if crop_prices.empty:
                return {
                    "crop": crop_name,
                    "message": "No market price data available",
                    "prices": []
                }
            
            # Filter by state if provided
            if state:
                state_prices = crop_prices[crop_prices['State'].str.contains(state, case=False, na=False)]
                if not state_prices.empty:
                    crop_prices = state_prices
            
            # Get recent prices (last 20 records)
            recent_prices = crop_prices.sort_values('Arrival_Date', ascending=False).head(20)
            
            prices_list = []
            for _, row in recent_prices.iterrows():
                prices_list.append({
                    "state": row['State'],
                    "district": row['District'],
                    "market": row['Market'],
                    "date": row['Arrival_Date'].strftime('%Y-%m-%d'),
                    "min_price": row['Min Price'],
                    "max_price": row['Max Price'],
                    "modal_price": row['Modal Price']
                })
            
            return {
                "crop": crop_name,
                "commodity": commodity,
                "total_records": len(crop_prices),
                "average_modal_price": round(crop_prices['Modal Price'].mean(), 2),
                "price_range": {
                    "min": crop_prices['Min Price'].min(),
                    "max": crop_prices['Max Price'].max()
                },
                "recent_prices": prices_list
            }
            
        except Exception as e:
            logger.error(f"Error getting market prices for {crop_name}: {e}")
            return {"error": str(e)}


def get_crop_planning_service():
    """Dependency injection for crop planning service"""
    from app.services.weather_service import get_weather_service
    weather_service = get_weather_service()
    return CropPlanningService(weather_service=weather_service)
