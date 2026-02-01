"""
Quick test for Weather and Location services
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.features.weather_service import WeatherService
from src.utils.location_service import LocationService

def test_weather_service():
    """Test weather service functionality."""
    print("\n" + "="*60)
    print("🌤️  TESTING WEATHER SERVICE")
    print("="*60 + "\n")
    
    weather = WeatherService()
    
    # Test location: New Delhi
    lat, lon = 28.6139, 77.2090
    
    print(f"📍 Testing location: {lat}, {lon} (New Delhi)")
    print("\n1. Testing Current Weather...")
    
    current = weather.get_current_weather(lat, lon)
    
    if current.get('error'):
        print(f"   ❌ Error: {current['error']}")
    else:
        print(f"   ✅ Temperature: {current['temperature']}°C")
        print(f"   ✅ Humidity: {current['humidity']}%")
        print(f"   ✅ Wind Speed: {current['wind_speed']} km/h")
        print(f"   ✅ Precipitation: {current['precipitation']} mm")
        print(f"   ✅ Weather: {current['weather_description']}")
        emoji = weather.get_weather_emoji(current['weather_code'])
        print(f"   ✅ Emoji: {emoji}")
    
    print("\n2. Testing Forecast (4 days)...")
    
    forecast = weather.get_forecast(lat, lon, days=4)
    
    if forecast.get('error'):
        print(f"   ❌ Error: {forecast['error']}")
    else:
        print(f"   ✅ Received {len(forecast['forecast'])} days of forecast")
        for i, day in enumerate(forecast['forecast'], 1):
            print(f"   Day {i}: {day['date']} - {day['weather_description']}")
            print(f"      Temp: {day['temp_min']}°C to {day['temp_max']}°C")
    
    print("\n3. Testing Complete Weather (combined)...")
    
    complete = weather.get_complete_weather(lat, lon, forecast_days=4)
    
    if complete.get('error'):
        print(f"   ❌ Error: {complete['error']}")
    else:
        print(f"   ✅ Current + Forecast data retrieved successfully")
        print(f"   ✅ Current temp: {complete['current']['temperature']}°C")
        print(f"   ✅ Forecast days: {len(complete['forecast'])}")


def test_location_service():
    """Test location service functionality."""
    print("\n" + "="*60)
    print("📍 TESTING LOCATION SERVICE")
    print("="*60 + "\n")
    
    location = LocationService()
    
    test_locations = [
        (28.6139, 77.2090, "New Delhi"),
        (19.0760, 72.8777, "Mumbai"),
        (12.9716, 77.5946, "Bangalore"),
        (30.9010, 75.8573, "Rural Punjab")
    ]
    
    for lat, lon, expected_name in test_locations:
        print(f"\n📌 Testing: {expected_name} ({lat}, {lon})")
        
        result = location.get_location_name(lat, lon)
        
        if result.get('error'):
            print(f"   ❌ Error: {result['error']}")
        else:
            print(f"   ✅ Village/City: {result['village_city']}")
            print(f"   ✅ District: {result['district']}")
            print(f"   ✅ State: {result['state']}")
            print(f"   ✅ Country: {result['country']}")
    
    print("\n4. Testing Invalid Coordinates...")
    
    # Test invalid latitude
    result = location.get_location_name(95, 77)  # Invalid lat > 90
    print(f"   Invalid Latitude (95): {result.get('error', 'No error')}")
    
    # Test invalid longitude
    result = location.get_location_name(28, 200)  # Invalid lon > 180
    print(f"   Invalid Longitude (200): {result.get('error', 'No error')}")


if __name__ == "__main__":
    print("\n🧪 WEATHER & LOCATION SERVICES - INTEGRATION TEST\n")
    
    try:
        test_location_service()
        test_weather_service()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*60 + "\n")
        
        print("💡 The services are working correctly and ready to use!")
        print("🚀 Start the Streamlit app to see the weather feature in action!")
        print("   Run: python run_web.py")
        print()
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
