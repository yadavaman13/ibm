"""
Direct Data Loading Test - No Server Required

Tests if the Market Intelligence service can load CSV data directly.
Run this to verify data access and loading logic.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath('.'))

from app.services.market_intelligence_service import MarketIntelligenceService

def test_data_access():
    """Test if data files are accessible"""
    print("="*60)
    print("🔍 TESTING DATA FILE ACCESS")
    print("="*60)
    
    service = MarketIntelligenceService()
    print(f"\n📁 Data path: {service.data_path}")
    print(f"   Exists: {service.data_path.exists()}")
    
    if service.data_path.exists():
        csv_files = list(service.data_path.glob("*.csv"))
        print(f"   CSV files found: {len(csv_files)}")
        if csv_files:
            print("\n📋 Sample files:")
            for f in csv_files[:5]:
                print(f"   ✓ {f.name}")
    else:
        print("   ❌ Data directory not found!")
        print(f"   Looking for: {service.data_path.absolute()}")
        return False
    
    return True


def test_get_commodities():
    """Test loading available commodities"""
    print("\n" + "="*60)
    print("🌾 TESTING GET COMMODITIES")
    print("="*60)
    
    try:
        service = MarketIntelligenceService()
        commodities = service.get_available_commodities()
        
        print(f"\n✓ Total commodities loaded: {len(commodities)}")
        
        if commodities:
            print("\n📊 Commodities by category:")
            by_category = {}
            for c in commodities:
                cat = c['category']
                if cat not in by_category:
                    by_category[cat] = []
                by_category[cat].append(c['name'])
            
            for category, items in sorted(by_category.items()):
                print(f"\n   {category}:")
                for item in items:
                    print(f"      • {item}")
            
            print("\n📈 Sample commodity details:")
            sample = commodities[0]
            print(f"   Name: {sample['name']}")
            print(f"   Category: {sample['category']}")
            print(f"   Records: {sample['record_count']}")
            if sample['date_range']:
                print(f"   Date Range: {sample['date_range']['start']} to {sample['date_range']['end']}")
            
            return True
        else:
            print("   ❌ No commodities loaded!")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_load_cotton_data():
    """Test loading specific commodity data"""
    print("\n" + "="*60)
    print("📦 TESTING COTTON DATA LOADING")
    print("="*60)
    
    try:
        service = MarketIntelligenceService()
        df = service._load_commodity_data("Cotton")
        
        if df is not None and len(df) > 0:
            print(f"\n✓ Cotton data loaded: {len(df)} records")
            print(f"\n📋 Columns: {', '.join(df.columns.tolist())}")
            print(f"\n📊 Sample data (first 3 rows):")
            print(df.head(3).to_string())
            
            print(f"\n📈 Price statistics:")
            print(f"   Min Price: ₹{df['Modal Price'].min():.2f}")
            print(f"   Max Price: ₹{df['Modal Price'].max():.2f}")
            print(f"   Avg Price: ₹{df['Modal Price'].mean():.2f}")
            
            print(f"\n📦 Arrival statistics:")
            print(f"   Total Arrival: {df['Arrival Quantity'].sum():.2f} MT")
            print(f"   Avg Daily: {df['Arrival Quantity'].mean():.2f} MT")
            
            return True
        else:
            print("   ❌ No data loaded for Cotton!")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_forecast():
    """Test price forecasting"""
    print("\n" + "="*60)
    print("📈 TESTING PRICE FORECAST")
    print("="*60)
    
    try:
        service = MarketIntelligenceService()
        result = service.simple_forecast("Cotton", days=7)
        
        if 'error' in result:
            print(f"   ❌ Error: {result['error']}")
            return False
        
        print(f"\n✓ Forecast generated!")
        print(f"   Commodity: {result['commodity']}")
        print(f"   Current Price: ₹{result['current_price']:.2f}")
        print(f"   Trend: {result['trend']['direction']}")
        print(f"   Forecast days: {len(result['forecast'])}")
        
        print(f"\n📊 7-Day Forecast:")
        for item in result['forecast']:
            print(f"   {item['date']}: ₹{item['predicted_price']:.2f} "
                  f"(₹{item['lower_bound']:.2f} - ₹{item['upper_bound']:.2f})")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_market_comparison():
    """Test market comparison"""
    print("\n" + "="*60)
    print("💰 TESTING MARKET COMPARISON")
    print("="*60)
    
    try:
        service = MarketIntelligenceService()
        markets = service.get_market_comparison("Wheat")
        
        if not markets:
            print("   ❌ No markets found!")
            return False
        
        print(f"\n✓ Found {len(markets)} markets")
        print(f"\n🏆 Top 5 Markets by Price:")
        for idx, market in enumerate(markets[:5], 1):
            print(f"   {idx}. {market['market']} ({market['district']})")
            print(f"      Price: ₹{market['modal_price']:.2f}")
            print(f"      Arrival: {market['arrival_quantity']:.2f} MT")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all data tests"""
    print("\n" + "="*70)
    print("🚀 MARKET INTELLIGENCE DATA LOADING TEST SUITE")
    print("   Testing WITHOUT server - Direct data access")
    print("="*70)
    
    tests = [
        ("Data Access", test_data_access),
        ("Get Commodities", test_get_commodities),
        ("Load Cotton Data", test_load_cotton_data),
        ("Price Forecast", test_forecast),
        ("Market Comparison", test_market_comparison),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*70)
    print("📋 TEST SUMMARY")
    print("="*70)
    passed = sum(1 for _, result in results if result)
    failed = len(results) - passed
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n🎯 Results: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n✅ All tests passed! Data loading works correctly.")
        print("   If frontend shows empty, the issue is likely:")
        print("   1. Backend not running")
        print("   2. CORS configuration")
        print("   3. Wrong API URL in frontend")
    else:
        print("\n⚠️  Some tests failed. Check data files and paths.")
    
    print("="*70)


if __name__ == "__main__":
    # Change to server directory
    if not os.path.exists('app'):
        print("❌ Error: Must run from fasal-mitra/server directory")
        print(f"   Current directory: {os.getcwd()}")
        print("\nUsage:")
        print("   cd fasal-mitra/server")
        print("   py test_data_loading.py")
        sys.exit(1)
    
    run_all_tests()
