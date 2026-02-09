"""
Test script to verify API functionality
"""

import requests
import json
from pprint import pprint

BASE_URL = "http://localhost:8000/api/v1"


def test_health():
    """Test health endpoint"""
    print("\n" + "="*60)
    print("Testing Health Endpoint")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    pprint(response.json())
    return response.status_code == 200


def test_info():
    """Test info endpoint"""
    print("\n" + "="*60)
    print("Testing Info Endpoint")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/info")
    print(f"Status Code: {response.status_code}")
    data = response.json()
    pprint(data)
    return response.status_code == 200


def test_yield_prediction():
    """Test yield prediction"""
    print("\n" + "="*60)
    print("Testing Yield Prediction")
    print("="*60)
    
    payload = {
        "crop": "Rice",
        "state": "Punjab",
        "season": "Kharif",
        "area": 100,
        "fertilizer": 25000,
        "pesticide": 500
    }
    
    response = requests.post(f"{BASE_URL}/yield/predict", json=payload)
    print(f"Status Code: {response.status_code}")
    pprint(response.json())
    return response.status_code == 200


def test_yield_benchmarks():
    """Test yield benchmarks"""
    print("\n" + "="*60)
    print("Testing Yield Benchmarks")
    print("="*60)
    
    payload = {
        "crop": "Wheat",
        "state": "Punjab",
        "season": "Rabi"
    }
    
    response = requests.post(f"{BASE_URL}/yield/benchmarks", json=payload)
    print(f"Status Code: {response.status_code}")
    pprint(response.json())
    return response.status_code == 200


def test_weather():
    """Test weather endpoint"""
    print("\n" + "="*60)
    print("Testing Weather (New Delhi)")
    print("="*60)
    
    payload = {
        "latitude": 28.6139,
        "longitude": 77.2090
    }
    
    response = requests.post(f"{BASE_URL}/weather/current", json=payload)
    print(f"Status Code: {response.status_code}")
    pprint(response.json())
    return response.status_code == 200


def test_soil_data():
    """Test soil data endpoint"""
    print("\n" + "="*60)
    print("Testing Soil Data (Punjab)")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/soil/data/Punjab")
    print(f"Status Code: {response.status_code}")
    pprint(response.json())
    return response.status_code == 200


def test_soil_suitability():
    """Test soil suitability"""
    print("\n" + "="*60)
    print("Testing Soil Suitability (Punjab - Rice)")
    print("="*60)
    
    response = requests.post(
        f"{BASE_URL}/soil/suitability",
        params={"state": "Punjab", "crop": "Rice"}
    )
    print(f"Status Code: {response.status_code}")
    pprint(response.json())
    return response.status_code == 200


def test_chatbot():
    """Test chatbot endpoint"""
    print("\n" + "="*60)
    print("Testing Chatbot")
    print("="*60)
    
    payload = {
        "question": "What is the best fertilizer for wheat?",
        "language": "en"
    }
    
    response = requests.post(f"{BASE_URL}/chatbot/query", json=payload)
    print(f"Status Code: {response.status_code}")
    pprint(response.json())
    return response.status_code == 200


def test_chatbot_status():
    """Test chatbot status"""
    print("\n" + "="*60)
    print("Testing Chatbot Status")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/chatbot/status")
    print(f"Status Code: {response.status_code}")
    pprint(response.json())
    return response.status_code == 200


def main():
    """Run all tests"""
    print("\n" + "🌾"*30)
    print(" " * 10 + "FasalMitra API Test Suite")
    print("🌾"*30)
    
    try:
        tests = [
            ("Health Check", test_health),
            ("System Info", test_info),
            ("Yield Prediction", test_yield_prediction),
            ("Yield Benchmarks", test_yield_benchmarks),
            ("Weather Service", test_weather),
            ("Soil Data", test_soil_data),
            ("Soil Suitability", test_soil_suitability),
            ("Chatbot Status", test_chatbot_status),
            ("Chatbot Query", test_chatbot),
        ]
        
        results = []
        for name, test_func in tests:
            try:
                success = test_func()
                results.append((name, success))
            except Exception as e:
                print(f"\n❌ Error in {name}: {str(e)}")
                results.append((name, False))
        
        # Print summary
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        
        passed = sum(1 for _, success in results if success)
        total = len(results)
        
        for name, success in results:
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{status} - {name}")
        
        print("\n" + "-"*60)
        print(f"Results: {passed}/{total} tests passed")
        print("="*60)
        
        if passed == total:
            print("\n🎉 All tests passed! Backend is working correctly.")
        else:
            print(f"\n⚠️  {total - passed} test(s) failed. Check the logs above.")
    
    except requests.exceptions.ConnectionError:
        print("\n❌ Cannot connect to API server!")
        print("Make sure the server is running:")
        print("  cd fasal-mitra/server")
        print("  python run.py")


if __name__ == "__main__":
    main()
