"""
Location Service Module

Provides reverse geocoding functionality to convert latitude/longitude coordinates
into human-readable location names using free OpenStreetMap Nominatim API.
"""

import requests
from typing import Dict, Optional
import time


class LocationService:
    """Service for reverse geocoding using OpenStreetMap Nominatim (free, no API key)."""
    
    def __init__(self):
        """Initialize the location service."""
        self.base_url = "https://nominatim.openstreetmap.org/reverse"
        # Nominatim requires a user agent for fair use
        self.headers = {
            'User-Agent': 'FarmingAdvisorySystem/1.0'
        }
        self.timeout = 10  # seconds
        
    def get_location_name(self, latitude: float, longitude: float) -> Dict[str, str]:
        """
        Convert latitude and longitude to human-readable location name.
        
        Args:
            latitude: Latitude coordinate (-90 to 90)
            longitude: Longitude coordinate (-180 to 180)
            
        Returns:
            Dictionary containing:
                - village_city: Village or city name
                - district: District name
                - state: State name
                - country: Country name
                - full_address: Complete formatted address
                - error: Error message if geocoding fails
        """
        # Validate coordinates
        if not (-90 <= latitude <= 90):
            return self._error_response("Invalid latitude. Must be between -90 and 90.")
        
        if not (-180 <= longitude <= 180):
            return self._error_response("Invalid longitude. Must be between -180 and 180.")
        
        try:
            # Build request parameters
            params = {
                'lat': latitude,
                'lon': longitude,
                'format': 'json',
                'addressdetails': 1,
                'zoom': 18  # Detailed level
            }
            
            # Make request to Nominatim
            response = requests.get(
                self.base_url,
                params=params,
                headers=self.headers,
                timeout=self.timeout
            )
            
            # Check response
            if response.status_code == 200:
                data = response.json()
                return self._parse_location_data(data)
            elif response.status_code == 429:
                # Rate limit exceeded
                time.sleep(1)  # Wait before retry
                return self._error_response("Rate limit exceeded. Please try again in a moment.")
            else:
                return self._error_response(f"Geocoding service error: {response.status_code}")
                
        except requests.Timeout:
            return self._error_response("Request timed out. Please check your internet connection.")
        except requests.ConnectionError:
            return self._error_response("Connection error. Please check your internet connection.")
        except Exception as e:
            return self._error_response(f"Unexpected error: {str(e)}")
    
    def _parse_location_data(self, data: dict) -> Dict[str, str]:
        """
        Parse location data from Nominatim response.
        
        Args:
            data: JSON response from Nominatim
            
        Returns:
            Structured location dictionary
        """
        if 'error' in data:
            return self._error_response("Location not found for these coordinates.")
        
        address = data.get('address', {})
        
        # Extract location components with fallbacks
        village_city = (
            address.get('village') or 
            address.get('town') or 
            address.get('city') or 
            address.get('municipality') or
            address.get('hamlet') or
            'Unknown'
        )
        
        district = (
            address.get('county') or 
            address.get('state_district') or
            address.get('district') or
            'Unknown'
        )
        
        state = (
            address.get('state') or 
            address.get('province') or
            'Unknown'
        )
        
        country = address.get('country', 'Unknown')
        
        # Get full formatted address
        full_address = data.get('display_name', 'Unknown location')
        
        return {
            'village_city': village_city,
            'district': district,
            'state': state,
            'country': country,
            'full_address': full_address,
            'error': None
        }
    
    def _error_response(self, error_message: str) -> Dict[str, str]:
        """
        Create error response dictionary.
        
        Args:
            error_message: Error description
            
        Returns:
            Error dictionary with 'Unknown' for all location fields
        """
        return {
            'village_city': 'Unknown',
            'district': 'Unknown',
            'state': 'Unknown',
            'country': 'Unknown',
            'full_address': 'Unknown location',
            'error': error_message
        }
    
    def validate_coordinates(self, latitude: float, longitude: float) -> tuple[bool, str]:
        """
        Validate latitude and longitude coordinates.
        
        Args:
            latitude: Latitude to validate
            longitude: Longitude to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not isinstance(latitude, (int, float)):
            return False, "Latitude must be a number"
        
        if not isinstance(longitude, (int, float)):
            return False, "Longitude must be a number"
        
        if not (-90 <= latitude <= 90):
            return False, "Latitude must be between -90 and 90"
        
        if not (-180 <= longitude <= 180):
            return False, "Longitude must be between -180 and 180"
        
        return True, ""


# Example coordinates for testing
EXAMPLE_LOCATIONS = {
    "New Delhi, India": (28.6139, 77.2090),
    "Mumbai, India": (19.0760, 72.8777),
    "Bangalore, India": (12.9716, 77.5946),
    "Chennai, India": (13.0827, 80.2707),
    "Kolkata, India": (22.5726, 88.3639),
    "Rural Punjab, India": (30.9010, 75.8573),
}
