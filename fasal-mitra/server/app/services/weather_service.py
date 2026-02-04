"""
Weather Service API

Ports logic from src/features/weather_service.py
"""

import requests
from typing import Dict, List, Optional
from datetime import datetime
import logging
from functools import lru_cache

logger = logging.getLogger(__name__)


class WeatherServiceAPI:
    """Service for fetching weather data using Open-Meteo API"""
    
    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1/forecast"
        self.geocoding_url = "https://geocoding-api.open-meteo.com/v1/reverse"
        self.timeout = 15
        
        # WMO Weather codes mapping
        self.weather_codes = {
            0: "Clear sky",
            1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
            45: "Foggy", 48: "Depositing rime fog",
            51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
            61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
            71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
            77: "Snow grains",
            80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
            85: "Slight snow showers", 86: "Heavy snow showers",
            95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
        }
    
    async def get_current_weather(self, latitude: float, longitude: float) -> Dict:
        """Get current weather conditions"""
        try:
            params = {
                'latitude': latitude,
                'longitude': longitude,
                'current': [
                    'temperature_2m',
                    'relative_humidity_2m',
                    'precipitation',
                    'wind_speed_10m',
                    'weather_code'
                ],
                'timezone': 'auto'
            }
            
            response = requests.get(
                self.base_url,
                params=params,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                current = data.get('current', {})
                
                weather_code = current.get('weather_code', 0)
                location_name = self.get_location_name(latitude, longitude).get('location_name', 'Unknown')
                
                result = {
                    'latitude': latitude,
                    'longitude': longitude,
                    'location_name': location_name,
                    'temperature': current.get('temperature_2m', 0),
                    'humidity': current.get('relative_humidity_2m', 0),
                    'wind_speed': current.get('wind_speed_10m', 0),
                    'precipitation': current.get('precipitation', 0),
                    'weather_code': weather_code,
                    'weather_description': self.weather_codes.get(weather_code, 'Unknown'),
                    'observation_time': datetime.fromisoformat(current.get('time', datetime.now().isoformat())),
                    'recommendations': self._generate_weather_recommendations(current)
                }
                
                return result
            else:
                raise Exception(f"Weather API error: {response.status_code}")
        
        except Exception as e:
            logger.error(f"Error fetching current weather: {str(e)}")
            raise
    
    async def get_forecast(self, latitude: float, longitude: float, days: int = 7) -> Dict:
        """Get weather forecast"""
        try:
            params = {
                'latitude': latitude,
                'longitude': longitude,
                'daily': [
                    'temperature_2m_max',
                    'temperature_2m_min',
                    'precipitation_sum',
                    'wind_speed_10m_max',
                    'weather_code'
                ],
                'timezone': 'auto',
                'forecast_days': min(days, 16)
            }
            
            response = requests.get(
                self.base_url,
                params=params,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                daily = data.get('daily', {})
                
                forecast = []
                for i in range(len(daily.get('time', []))):
                    weather_code = daily['weather_code'][i]
                    forecast.append({
                        'date': daily['time'][i],
                        'temp_max': daily['temperature_2m_max'][i],
                        'temp_min': daily['temperature_2m_min'][i],
                        'precipitation_sum': daily['precipitation_sum'][i],
                        'wind_speed_max': daily['wind_speed_10m_max'][i],
                        'weather_code': weather_code,
                        'weather_description': self.weather_codes.get(weather_code, 'Unknown')
                    })
                
                location_name = self.get_location_name(latitude, longitude).get('location_name', 'Unknown')
                
                result = {
                    'latitude': latitude,
                    'longitude': longitude,
                    'location_name': location_name,
                    'forecast': forecast,
                    'farming_recommendations': self._generate_farming_recommendations(forecast),
                    'alerts': self._generate_alerts(forecast)
                }
                
                return result
            else:
                raise Exception(f"Forecast API error: {response.status_code}")
        
        except Exception as e:
            logger.error(f"Error fetching forecast: {str(e)}")
            raise
    
    def get_location_name(self, latitude: float, longitude: float) -> Dict:
        """Get location name from coordinates (reverse geocoding)"""
        try:
            params = {
                'latitude': latitude,
                'longitude': longitude,
                'format': 'json'
            }
            
            response = requests.get(
                self.geocoding_url,
                params=params,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                
                if results:
                    location = results[0]
                    return {
                        'latitude': latitude,
                        'longitude': longitude,
                        'location_name': location.get('name', 'Unknown'),
                        'country': location.get('country', None),
                        'state': location.get('admin1', None),
                        'district': location.get('admin2', None)
                    }
            
            return {
                'latitude': latitude,
                'longitude': longitude,
                'location_name': f"Location {latitude:.2f}, {longitude:.2f}"
            }
        
        except Exception as e:
            logger.warning(f"Error in reverse geocoding: {str(e)}")
            return {
                'latitude': latitude,
                'longitude': longitude,
                'location_name': f"Location {latitude:.2f}, {longitude:.2f}"
            }
    
    def _generate_weather_recommendations(self, current: Dict) -> List[str]:
        """Generate farming recommendations based on current weather"""
        recommendations = []
        
        temp = current.get('temperature_2m', 0)
        humidity = current.get('relative_humidity_2m', 0)
        precipitation = current.get('precipitation', 0)
        
        if temp > 35:
            recommendations.append("🌡️ High temperature - ensure adequate irrigation")
        elif temp < 10:
            recommendations.append("❄️ Low temperature - protect sensitive crops")
        
        if humidity > 80:
            recommendations.append("💧 High humidity - monitor for fungal diseases")
        
        if precipitation > 10:
            recommendations.append("🌧️ Heavy rain expected - ensure proper drainage")
        
        return recommendations
    
    def _generate_farming_recommendations(self, forecast: List[Dict]) -> List[str]:
        """Generate farming recommendations based on forecast"""
        recommendations = []
        
        # Check for rain in next 3 days
        rain_days = sum(1 for f in forecast[:3] if f['precipitation_sum'] > 5)
        if rain_days >= 2:
            recommendations.append("🌧️ Rain expected in next 3 days - postpone irrigation")
        
        # Check for high temperatures
        hot_days = sum(1 for f in forecast[:7] if f['temp_max'] > 35)
        if hot_days >= 3:
            recommendations.append("🌡️ Hot weather ahead - plan for increased irrigation")
        
        # Check for extreme weather
        if any(f['weather_code'] >= 95 for f in forecast[:3]):
            recommendations.append("⚠️ Thunderstorms expected - secure equipment and crops")
        
        return recommendations
    
    def _generate_alerts(self, forecast: List[Dict]) -> List[str]:
        """Generate weather alerts"""
        alerts = []
        
        for f in forecast[:3]:
            if f['weather_code'] >= 95:
                alerts.append(f"⚠️ Thunderstorm alert for {f['date']}")
            elif f['precipitation_sum'] > 50:
                alerts.append(f"🌧️ Heavy rain alert for {f['date']}")
            elif f['temp_max'] > 40:
                alerts.append(f"🌡️ Extreme heat alert for {f['date']}")
        
        return alerts


@lru_cache()
def get_weather_service() -> WeatherServiceAPI:
    """Get singleton instance of weather service"""
    return WeatherServiceAPI()
