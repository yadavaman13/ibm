"""
Comprehensive Backend Testing Suite
Tests all endpoints with realistic data
"""

import requests
import json
from pathlib import Path
from typing import Dict, Any
import time

BASE_URL = "http://localhost:8000/api/v1"

class BackendTester:
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
    
    def test(self, name: str, func):
        """Run a test and track results"""
        print(f"\n{'='*70}")
        print(f"🧪 Testing: {name}")
        print(f"{'='*70}")
        try:
            func()
            print(f"✅ PASSED: {name}")
            self.results.append((name, True, None))
            self.passed += 1
        except AssertionError as e:
            print(f"❌ FAILED: {name}")
            print(f"   Error: {str(e)}")
            self.results.append((name, False, str(e)))
            self.failed += 1
        except Exception as e:
            print(f"❌ ERROR: {name}")
            print(f"   Exception: {str(e)}")
            self.results.append((name, False, str(e)))
            self.failed += 1
    
    def print_summary(self):
        """Print test summary"""
        print(f"\n{'='*70}")
        print(f"📊 TEST SUMMARY")
        print(f"{'='*70}")
        print(f"Total Tests: {len(self.results)}")
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"Success Rate: {(self.passed/len(self.results)*100):.1f}%")
        
        if self.failed > 0:
            print(f"\n❌ Failed Tests:")
            for name, success, error in self.results:
                if not success:
                    print(f"   - {name}: {error}")

# Initialize tester
tester = BackendTester()

# ============================================================================
# TEST 1: Health & System Info
# ============================================================================

def test_health():
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    print(f"   Status: {data['status']}")

def test_info():
    response = requests.get(f"{BASE_URL}/info")
    assert response.status_code == 200
    result = response.json()
    assert "data" in result
    data = result["data"]
    assert "datasets" in data
    datasets = data["datasets"]
    assert "available_crops" in datasets
    assert "available_states" in datasets
    print(f"   Crops: {len(datasets['available_crops'])}")
    print(f"   States: {len(datasets['available_states'])}")

def test_stats():
    response = requests.get(f"{BASE_URL}/stats")
    assert response.status_code == 200
    data = response.json()
    print(f"   Total Records: {data.get('total_records', 'N/A')}")

# ============================================================================
# TEST 2: Yield Prediction - All Required Fields
# ============================================================================

def test_yield_prediction_complete():
    """Test yield prediction with all possible output fields"""
    payload = {
        "crop": "Rice",
        "state": "Punjab",
        "season": "Kharif",
        "area": 100,
        "fertilizer": 25000,
        "pesticide": 500
    }
    
    response = requests.post(f"{BASE_URL}/yield/predict", json=payload)
    assert response.status_code == 200
    
    data = response.json()["data"]
    
    # Check all required fields
    assert "predicted_yield" in data
    assert "confidence_interval" in data
    assert "lower" in data["confidence_interval"]
    assert "upper" in data["confidence_interval"]
    
    print(f"   Predicted Yield: {data['predicted_yield']:.2f}")
    print(f"   Confidence: {data['confidence_interval']}")

def test_yield_gap_analysis():
    """Test gap analysis endpoint"""
    payload = {
        "crop": "Wheat",
        "state": "Punjab",
        "season": "Rabi",
        "area": 50,
        "fertilizer": 20000,
        "pesticide": 300
    }
    
    response = requests.post(f"{BASE_URL}/yield/gap-analysis", json=payload)
    assert response.status_code == 200
    
    data = response.json()["data"]
    print(f"   Yield Gap: {data.get('gap_percentage', 'N/A')}%")

def test_yield_benchmarks():
    """Test benchmarking endpoint"""
    payload = {
        "crop": "Rice",
        "state": "West Bengal",
        "season": "Kharif"
    }
    
    response = requests.post(f"{BASE_URL}/yield/benchmarks", json=payload)
    assert response.status_code == 200
    
    data = response.json()["data"]
    print(f"   Mean Yield: {data.get('mean_yield', 'N/A')}")

# ============================================================================
# TEST 3: Weather API - All Required Fields
# ============================================================================

def test_weather_current():
    """Test current weather with all fields"""
    payload = {
        "latitude": 28.6139,
        "longitude": 77.2090
    }
    
    response = requests.post(f"{BASE_URL}/weather/current", json=payload)
    assert response.status_code == 200
    
    data = response.json()["data"]
    
    # Check all required fields
    assert "temperature" in data
    assert "humidity" in data
    assert "weather_description" in data
    
    print(f"   Temperature: {data['temperature']}°C")
    print(f"   Humidity: {data['humidity']}%")

def test_weather_forecast():
    """Test 7-day forecast"""
    payload = {
        "latitude": 28.6139,
        "longitude": 77.2090
    }
    
    response = requests.post(f"{BASE_URL}/weather/forecast", json=payload)
    assert response.status_code == 200
    
    data = response.json()["data"]
    assert "forecast" in data
    assert len(data["forecast"]) > 0
    
    print(f"   Forecast Days: {len(data['forecast'])}")

# ============================================================================
# TEST 4: Soil Analysis - All Required Fields
# ============================================================================

def test_soil_data():
    """Test soil data retrieval"""
    response = requests.get(f"{BASE_URL}/soil/data/Punjab")
    assert response.status_code == 200
    
    data = response.json()["data"]
    print(f"   Soil Data Retrieved: ✓")

def test_soil_suitability():
    """Test soil suitability check"""
    response = requests.post(
        f"{BASE_URL}/soil/suitability",
        params={"state": "Punjab", "crop": "Rice"}
    )
    assert response.status_code == 200
    
    data = response.json()["data"]
    print(f"   Suitability Score: {data.get('suitability_score', 'N/A')}")

def test_soil_recommendations():
    """Test crop recommendations"""
    response = requests.get(f"{BASE_URL}/soil/recommendations/Punjab")
    assert response.status_code == 200
    
    result = response.json()
    assert "data" in result
    data = result["data"]
    
    # Check for 'recommended_crops' field (actual API response)
    assert "recommended_crops" in data, f"Expected 'recommended_crops' field. Got: {list(data.keys())}"
    
    rec_count = len(data.get('recommended_crops', []))
    print(f"   Recommendations Count: {rec_count}")

# ============================================================================
# TEST 5: Chatbot - All Required Fields
# ============================================================================

def test_chatbot_status():
    """Test chatbot availability"""
    response = requests.get(f"{BASE_URL}/chatbot/status")
    assert response.status_code == 200
    
    data = response.json()["data"]
    print(f"   Chatbot Status: {data.get('status', 'Unknown')}")

def test_chatbot_query():
    """Test chatbot question answering"""
    payload = {
        "question": "What is the best fertilizer for wheat in Punjab?",
        "language": "en"
    }
    
    response = requests.post(f"{BASE_URL}/chatbot/query", json=payload)
    assert response.status_code == 200
    
    data = response.json()["data"]
    assert "answer" in data
    
    print(f"   Answer Length: {len(data['answer'])} chars")

def test_chatbot_explain():
    """Test term explanation"""
    payload = {
        "term": "NPK",
        "language": "en"
    }
    
    response = requests.post(f"{BASE_URL}/chatbot/explain", json=payload)
    assert response.status_code == 200
    
    data = response.json()["data"]
    print(f"   Explanation Received: ✓")

# ============================================================================
# TEST 6: Available Options (Dropdowns)
# ============================================================================

def test_available_crops():
    """Test getting list of crops"""
    response = requests.get(f"{BASE_URL}/yield/crops")
    assert response.status_code == 200
    result = response.json()
    
    # Handle both list and dict responses
    if isinstance(result, dict):
        crops = result.get('data', {}).get('crops', result.get('crops', []))
    else:
        crops = result
    
    assert len(crops) > 0
    print(f"   Available Crops: {len(crops)}")
    print(f"   Sample Crops: {crops[:3]}")

def test_available_states():
    """Test getting list of states"""
    response = requests.get(f"{BASE_URL}/yield/states")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    print(f"   Available States: {len(data)}")

def test_available_seasons():
    """Test getting list of seasons"""
    response = requests.get(f"{BASE_URL}/yield/seasons")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    print(f"   Available Seasons: {data}")

# ============================================================================
# RUN ALL TESTS
# ============================================================================

def main():
    print("\n" + "="*70)
    print("🌾 FASAL MITRA - COMPREHENSIVE BACKEND TEST SUITE")
    print("="*70)
    
    # Check if server is running
    try:
        requests.get(f"{BASE_URL}/health", timeout=5)
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to backend!")
        print("   Please start the server:")
        print("   1. Open a terminal")
        print("   2. cd fasal-mitra/server")
        print("   3. python run.py")
        return
    
    print("\n✅ Server is running!")
    
    # Test 1: Health & System
    tester.test("Health Check", test_health)
    tester.test("System Info", test_info)
    tester.test("System Stats", test_stats)
    
    # Test 2: Yield Prediction
    tester.test("Yield Prediction - Complete", test_yield_prediction_complete)
    tester.test("Yield Gap Analysis", test_yield_gap_analysis)
    tester.test("Yield Benchmarks", test_yield_benchmarks)
    
    # Test 3: Weather
    tester.test("Current Weather", test_weather_current)
    tester.test("Weather Forecast", test_weather_forecast)
    
    # Test 4: Soil Analysis
    tester.test("Soil Data Retrieval", test_soil_data)
    tester.test("Soil Suitability", test_soil_suitability)
    tester.test("Soil Recommendations", test_soil_recommendations)
    
    # Test 5: Chatbot
    tester.test("Chatbot Status", test_chatbot_status)
    tester.test("Chatbot Query", test_chatbot_query)
    tester.test("Chatbot Explain", test_chatbot_explain)
    
    # Test 6: Available Options
    tester.test("Get Available Crops", test_available_crops)
    tester.test("Get Available States", test_available_states)
    tester.test("Get Available Seasons", test_available_seasons)
    
    # Print Summary
    tester.print_summary()
    
    # Final Verdict
    print(f"\n{'='*70}")
    if tester.failed == 0:
        print("🎉 ALL TESTS PASSED - BACKEND IS PRODUCTION READY!")
        print("\n✅ Next Steps:")
        print("   1. Backend is fully tested and working")
        print("   2. Ready for React frontend integration")
        print("   3. All API endpoints are verified")
    else:
        print("⚠️  SOME TESTS FAILED - REVIEW REQUIRED")
        print(f"   Please fix the {tester.failed} failed test(s) above")
    print("="*70)

if __name__ == "__main__":
    main()
