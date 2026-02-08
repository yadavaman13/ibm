"""
Quick Test Script for Market Intelligence API

Run this to test if the Market Intelligence endpoints are working correctly.
"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1/market"

def test_health():
    """Test Market Intelligence service health"""
    print("\n🔍 Testing service health...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        data = response.json()
        print(f"✓ Status: {response.status_code}")
        print(f"✓ Available commodities: {data['data']['available_commodities']}")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_get_commodities():
    """Test getting available commodities"""
    print("\n🌾 Testing get commodities...")
    try:
        response = requests.get(f"{BASE_URL}/commodities")
        data = response.json()
        print(f"✓ Status: {response.status_code}")
        print(f"✓ Total commodities: {data['data']['total_count']}")
        print(f"✓ Sample: {data['data']['commodities'][:3]}")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_forecast():
    """Test price forecasting"""
    print("\n📈 Testing price forecast for Cotton...")
    try:
        response = requests.post(
            f"{BASE_URL}/forecast",
            json={
                "commodity": "Cotton",
                "days": 7
            }
        )
        data = response.json()
        print(f"✓ Status: {response.status_code}")
        print(f"✓ Current price: ₹{data['data']['current_price']}")
        print(f"✓ Trend: {data['data']['trend']['direction']}")
        print(f"✓ Forecast days: {len(data['data']['forecast'])}")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_market_comparison():
    """Test market comparison"""
    print("\n💰 Testing market comparison for Wheat...")
    try:
        response = requests.post(
            f"{BASE_URL}/compare",
            json={
                "commodity": "Wheat"
            }
        )
        data = response.json()
        print(f"✓ Status: {response.status_code}")
        print(f"✓ Total markets: {data['data']['total_markets']}")
        if data['data']['markets']:
            best = data['data']['markets'][0]
            print(f"✓ Best market: {best['market']} - ₹{best['modal_price']}")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_recommendation():
    """Test market recommendation"""
    print("\n🎯 Testing recommendation for Potato...")
    try:
        response = requests.post(
            f"{BASE_URL}/recommend",
            json={
                "commodity": "Potato",
                "user_district": "Ahmedabad",
                "quantity": 5
            }
        )
        data = response.json()
        print(f"✓ Status: {response.status_code}")
        print(f"✓ Best market: {data['data']['best_market']['market']}")
        print(f"✓ Price: ₹{data['data']['best_market']['modal_price']}")
        print(f"✓ Premium: {data['data']['premium_percent']}%")
        if 'potential_total_profit' in data['data']:
            print(f"✓ Potential profit: ₹{data['data']['potential_total_profit']}")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_insights():
    """Test commodity insights"""
    print("\n📊 Testing insights for Cotton...")
    try:
        response = requests.get(f"{BASE_URL}/insights/Cotton?days=30")
        data = response.json()
        print(f"✓ Status: {response.status_code}")
        print(f"✓ Total records: {data['data']['total_records']}")
        print(f"✓ Current avg price: ₹{data['data']['price_stats']['current_avg']}")
        print(f"✓ Avg daily arrival: {data['data']['arrival_stats']['avg_daily']} MT")
        print(f"✓ Total markets: {data['data']['markets']['total_markets']}")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("="*60)
    print("🚀 MARKET INTELLIGENCE API TEST SUITE")
    print("="*60)
    
    tests = [
        test_health,
        test_get_commodities,
        test_forecast,
        test_market_comparison,
        test_recommendation,
        test_insights
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        if test():
            passed += 1
        else:
            failed += 1
    
    print("\n" + "="*60)
    print(f"📋 TEST RESULTS: {passed} passed, {failed} failed")
    print("="*60)


if __name__ == "__main__":
    print("\n⚠️  Make sure the FastAPI backend is running on http://localhost:8000")
    print("   Run: python run.py (or uvicorn app.main:app --reload)")
    input("\nPress Enter to start tests...")
    
    run_all_tests()
