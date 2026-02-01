"""
Weather Service Module

Provides weather data fetching using free Open-Meteo API (no API key required).
Supports current weather conditions and multi-day forecast.
"""

import requests
from typing import Dict, List, Optional
from datetime import datetime, timedelta


class WeatherService:
    """Service for fetching weather data using Open-Meteo API (free, no API key needed)."""
    
    def __init__(self):
        """Initialize the weather service."""
        self.base_url = "https://api.open-meteo.com/v1/forecast"
        self.timeout = 15  # seconds
        
    def get_current_weather(self, latitude: float, longitude: float) -> Dict:
        """
        Get current weather conditions for a location.
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            
        Returns:
            Dictionary containing current weather data:
                - temperature: Current temperature in °C
                - humidity: Relative humidity in %
                - wind_speed: Wind speed in km/h
                - precipitation: Precipitation in mm
                - weather_code: WMO weather code
                - weather_description: Human-readable weather description
                - time: Observation time
                - error: Error message if request fails
        """
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
                return self._parse_current_weather(data)
            else:
                return self._error_response(f"API error: {response.status_code}")
                
        except requests.Timeout:
            return self._error_response("Request timed out. Please try again.")
        except requests.ConnectionError:
            return self._error_response("Connection error. Check internet connection.")
        except Exception as e:
            return self._error_response(f"Unexpected error: {str(e)}")
    
    def get_forecast(self, latitude: float, longitude: float, days: int = 4) -> Dict:
        """
        Get weather forecast for the next N days.
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            days: Number of forecast days (default: 4)
            
        Returns:
            Dictionary containing:
                - forecast: List of daily forecast dictionaries
                - error: Error message if request fails
        """
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
                'forecast_days': days
            }
            
            response = requests.get(
                self.base_url,
                params=params,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_forecast(data)
            else:
                return self._error_response(f"API error: {response.status_code}")
                
        except requests.Timeout:
            return self._error_response("Request timed out. Please try again.")
        except requests.ConnectionError:
            return self._error_response("Connection error. Check internet connection.")
        except Exception as e:
            return self._error_response(f"Unexpected error: {str(e)}")
    
    def get_complete_weather(self, latitude: float, longitude: float, forecast_days: int = 4) -> Dict:
        """
        Get both current weather and forecast in a single call.
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            forecast_days: Number of days for forecast
            
        Returns:
            Dictionary with both current weather and forecast data
        """
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
                'daily': [
                    'temperature_2m_max',
                    'temperature_2m_min',
                    'precipitation_sum',
                    'wind_speed_10m_max',
                    'weather_code'
                ],
                'timezone': 'auto',
                'forecast_days': forecast_days
            }
            
            response = requests.get(
                self.base_url,
                params=params,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                current = self._parse_current_weather(data)
                forecast = self._parse_forecast(data)
                
                return {
                    'current': current,
                    'forecast': forecast['forecast'] if 'forecast' in forecast else [],
                    'error': None
                }
            else:
                return self._error_response(f"API error: {response.status_code}")
                
        except Exception as e:
            return self._error_response(f"Error fetching weather: {str(e)}")
    
    def _parse_current_weather(self, data: dict) -> Dict:
        """Parse current weather data from API response."""
        try:
            current = data.get('current', {})
            
            weather_code = current.get('weather_code', 0)
            
            return {
                'temperature': current.get('temperature_2m', 0),
                'humidity': current.get('relative_humidity_2m', 0),
                'wind_speed': current.get('wind_speed_10m', 0),
                'precipitation': current.get('precipitation', 0),
                'weather_code': weather_code,
                'weather_description': self._get_weather_description(weather_code),
                'time': current.get('time', ''),
                'error': None
            }
        except Exception as e:
            return self._error_response(f"Error parsing current weather: {str(e)}")
    
    def _parse_forecast(self, data: dict) -> Dict:
        """Parse forecast data from API response."""
        try:
            daily = data.get('daily', {})
            times = daily.get('time', [])
            
            forecast_list = []
            for i in range(len(times)):
                weather_code = daily['weather_code'][i] if i < len(daily.get('weather_code', [])) else 0
                
                forecast_day = {
                    'date': times[i],
                    'temp_max': daily['temperature_2m_max'][i] if i < len(daily.get('temperature_2m_max', [])) else 0,
                    'temp_min': daily['temperature_2m_min'][i] if i < len(daily.get('temperature_2m_min', [])) else 0,
                    'precipitation': daily['precipitation_sum'][i] if i < len(daily.get('precipitation_sum', [])) else 0,
                    'wind_speed': daily['wind_speed_10m_max'][i] if i < len(daily.get('wind_speed_10m_max', [])) else 0,
                    'weather_code': weather_code,
                    'weather_description': self._get_weather_description(weather_code)
                }
                forecast_list.append(forecast_day)
            
            return {
                'forecast': forecast_list,
                'error': None
            }
        except Exception as e:
            return self._error_response(f"Error parsing forecast: {str(e)}")
    
    def _get_weather_description(self, code: int) -> str:
        """
        Convert WMO weather code to human-readable description.
        
        WMO Weather interpretation codes (WW):
        https://open-meteo.com/en/docs
        """
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            77: "Snow grains",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail"
        }
        
        return weather_codes.get(code, "Unknown")
    
    def _error_response(self, error_message: str) -> Dict:
        """Create error response dictionary."""
        return {
            'error': error_message,
            'temperature': None,
            'humidity': None,
            'wind_speed': None,
            'precipitation': None
        }
    
    def get_weather_emoji(self, weather_code: int) -> str:
        """Get emoji representing weather condition."""
        emoji_map = {
            0: "☀️",   # Clear sky
            1: "🌤️",   # Mainly clear
            2: "⛅",   # Partly cloudy
            3: "☁️",   # Overcast
            45: "🌫️",  # Fog
            48: "🌫️",  # Rime fog
            51: "🌦️",  # Drizzle
            53: "🌦️",  # Drizzle
            55: "🌦️",  # Dense drizzle
            61: "🌧️",  # Slight rain
            63: "🌧️",  # Moderate rain
            65: "🌧️",  # Heavy rain
            71: "❄️",   # Snow
            73: "❄️",   # Snow
            75: "❄️",   # Heavy snow
            77: "❄️",   # Snow grains
            80: "🌦️",  # Rain showers
            81: "🌧️",  # Rain showers
            82: "🌧️",  # Violent showers
            85: "🌨️",  # Snow showers
            86: "🌨️",  # Heavy snow showers
            95: "⛈️",   # Thunderstorm
            96: "⛈️",   # Thunderstorm with hail
            99: "⛈️"    # Heavy thunderstorm
        }
        return emoji_map.get(weather_code, "🌍")
