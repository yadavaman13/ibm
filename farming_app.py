"""
Farming Advisory System - User Interface
Simple console-based farmer-friendly interface

Run: python farming_app.py
"""

from farming_system import initialize_system, ExplainableAI
import sys

def print_header():
    """Print application header"""
    print("\n" + "=" * 70)
    print(" 🌾 FARMING ADVISORY SYSTEM 🌾")
    print(" Your Smart Farming Companion")
    print("=" * 70)

def print_menu():
    """Print main menu"""
    print("\n📋 MAIN MENU:")
    print("=" * 70)
    print(" 1️⃣  Check Soil Suitability")
    print(" 2️⃣  Predict Crop Yield")
    print(" 3️⃣  Find Best Season")
    print(" 4️⃣  Optimize Fertilizer Usage")
    print(" 5️⃣  Compare Crops")
    print(" 6️⃣  Check Market Prices")
    print(" 7️⃣  Get Weather Risk Alerts")
    print(" 8️⃣  Complete Farm Analysis (All Features)")
    print(" 9️⃣  List Available Crops/States")
    print(" 0️⃣  Exit")
    print("=" * 70)

def get_available_items(system):
    """Show available crops and states"""
    print("\n📊 AVAILABLE DATA:")
    print("=" * 70)
    
    crops = sorted(system['data']['crop_yield']['crop'].unique())
    states = sorted(system['data']['crop_yield']['state'].unique())
    commodities = sorted(system['data']['prices']['Commodity'].unique())
    
    print(f"\n🌾 Crops ({len(crops)} available):")
    print(", ".join(crops[:20]) + "...")
    
    print(f"\n📍 States ({len(states)} available):")
    print(", ".join(states))
    
    print(f"\n💰 Price Data Commodities ({len(commodities)} available):")
    print(", ".join(commodities[:30]) + "...")
    print("=" * 70)

def feature_soil_suitability(system):
    """Feature 1: Soil Suitability Check"""
    print("\n" + "=" * 70)
    print(" 1️⃣  SOIL SUITABILITY CHECK")
    print("=" * 70)
    
    state = input("\nEnter your state: ").strip()
    crop = input("Enter crop name: ").strip()
    
    result = system['soil_checker'].check(state, crop)
    
    if not result['suitable'] and 'message' in result:
        print(f"\n❌ {result['message']}")
        return
    
    print(f"\n{'✅ SUITABLE' if result['suitable'] else '⚠️ NEEDS IMPROVEMENT'}")
    print(f"Suitability Score: {result['score']:.1f}%\n")
    
    # Explain
    explanation = ExplainableAI.explain_soil_suitability(result, crop, state)
    print(explanation)
    print("=" * 70)

def feature_yield_prediction(system):
    """Feature 2: Yield Prediction"""
    print("\n" + "=" * 70)
    print(" 2️⃣  CROP YIELD PREDICTION")
    print("=" * 70)
    
    try:
        crop = input("\nEnter crop name: ").strip()
        state = input("Enter state: ").strip()
        season = input("Enter season (Kharif/Rabi/Whole Year): ").strip()
        
        # Get soil data for state
        soil_data = system['data']['soil'][system['data']['soil']['state'] == state]
        if soil_data.empty:
            print(f"\n❌ No soil data for {state}")
            return
        
        soil = soil_data.iloc[0]
        
        # Get weather data
        weather_data = system['data']['weather'][system['data']['weather']['state'] == state]
        if weather_data.empty:
            print(f"\n❌ No weather data for {state}")
            return
        
        weather = weather_data.mean()
        
        # Get typical values
        area = float(input("Enter cultivated area (hectares): ") or "100")
        fertilizer = float(input("Enter fertilizer amount (kg): ") or "10000")
        pesticide = float(input("Enter pesticide amount (kg): ") or "100")
        
        # Predict
        predicted_yield = system['yield_predictor'].predict(
            crop, state, season, area, fertilizer, pesticide,
            weather['avg_temp_c'], weather['total_rainfall_mm'], 
            weather['avg_humidity_percent'],
            soil['N'], soil['P'], soil['K'], soil['pH']
        )
        
        if predicted_yield is None:
            print("\n❌ Could not predict yield. Please check crop/state names.")
            return
        
        print(f"\n📊 PREDICTED YIELD: {predicted_yield:.2f} quintals/hectare")
        
        # Explain
        explanation = ExplainableAI.explain_yield_prediction(
            predicted_yield, crop, state, season
        )
        print(f"\n{explanation}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    print("=" * 70)

def feature_best_season(system):
    """Feature 3: Season Recommendation"""
    print("\n" + "=" * 70)
    print(" 3️⃣  BEST SEASON RECOMMENDATION")
    print("=" * 70)
    
    crop = input("\nEnter crop name: ").strip()
    state = input("Enter state: ").strip()
    
    result = system['season_recommender'].recommend(crop, state)
    
    if result is None:
        print(f"\n❌ No data for {crop} in {state}")
        return
    
    print(f"\n🌟 BEST SEASON: {result['best_season']}")
    print(f"📊 Average Yield: {result['avg_yield']:.2f} quintals/hectare")
    print(f"📈 Based on {result['num_records']} historical records")
    
    print("\n📋 All Seasons Performance:")
    for season in result['all_seasons']:
        print(f"   {season['season']:15} - Avg: {season['mean']:7.2f} quintals/ha "
              f"(Records: {int(season['count'])})")
    
    print("=" * 70)

def feature_fertilizer_optimizer(system):
    """Feature 4: Fertilizer Optimization"""
    print("\n" + "=" * 70)
    print(" 4️⃣  FERTILIZER OPTIMIZER")
    print("=" * 70)
    
    crop = input("\nEnter crop name: ").strip()
    state = input("Enter state: ").strip()
    target_yield = float(input("Enter target yield (quintals/hectare): ") or "30")
    
    result = system['fertilizer_optimizer'].optimize(crop, state, target_yield)
    
    if result is None:
        print(f"\n❌ No data for {crop} in {state}")
        return
    
    print(f"\n💡 RECOMMENDATIONS:")
    print(f"   Fertilizer: {result['recommended_fertilizer']:.2f} kg")
    print(f"   Pesticide: {result['recommended_pesticide']:.2f} kg")
    print(f"   Expected Yield: {result['expected_yield']:.2f} quintals/hectare")
    print(f"   Based on: {result['num_similar_cases']} similar cases")
    
    print(f"\n📊 Fertilizer Range: {result['fertilizer_range'][0]:.0f} - "
          f"{result['fertilizer_range'][1]:.0f} kg")
    
    print("\n🧠 Explanation:")
    print(f"   These recommendations are based on {result['num_similar_cases']} historical")
    print(f"   cases where farmers achieved yields close to your target of {target_yield} quintals/ha.")
    
    print("=" * 70)

def feature_crop_comparison(system):
    """Feature 5: Crop Comparison"""
    print("\n" + "=" * 70)
    print(" 5️⃣  CROP PERFORMANCE COMPARISON")
    print("=" * 70)
    
    state = input("\nEnter state: ").strip()
    season = input("Enter season (optional, press Enter to skip): ").strip() or None
    
    result = system['crop_comparator'].compare(state, season=season)
    
    if result is None:
        print(f"\n❌ No data for {state}")
        return
    
    print(f"\n📊 TOP 10 CROPS IN {state}:")
    print(f"{'Rank':<6} {'Crop':<25} {'Avg Yield':<12} {'Records':<10}")
    print("-" * 70)
    
    for i, crop in enumerate(result[:10], 1):
        print(f"{i:<6} {crop['crop']:<25} {crop['avg_yield']:<12.2f} {int(crop['num_records']):<10}")
    
    print("\n💡 Insight: Crops are ranked by average yield (quintals/hectare)")
    print("=" * 70)

def feature_market_prices(system):
    """Feature 6: Market Price Analysis"""
    print("\n" + "=" * 70)
    print(" 6️⃣  MARKET PRICE ANALYSIS")
    print("=" * 70)
    
    commodity = input("\nEnter commodity name (e.g., Potato, Wheat, Tomato): ").strip()
    state = input("Enter state (optional, press Enter for all states): ").strip() or None
    
    result = system['price_analyzer'].analyze_trend(commodity, state)
    
    if result is None:
        print(f"\n❌ No price data for {commodity}")
        print("\n💡 Try: Potato, Onion, Tomato, Wheat, Rice, etc.")
        return
    
    explanation = ExplainableAI.explain_price_trend(result)
    print(f"\n{explanation}")
    
    if result['states_available']:
        print(f"\n📍 Price data available for states:")
        print(f"   {', '.join(result['states_available'][:10])}")
    
    print("=" * 70)

def feature_risk_alerts(system):
    """Feature 7: Risk Alerts"""
    print("\n" + "=" * 70)
    print(" 7️⃣  WEATHER RISK ALERTS")
    print("=" * 70)
    
    crop = input("\nEnter crop name: ").strip()
    state = input("Enter state: ").strip()
    season = input("Enter season: ").strip()
    
    alerts = system['risk_alerts'].check_risks(crop, state, season)
    
    if not alerts:
        print(f"\n✅ No significant weather risks detected for {crop} in {state}")
        print("   However, always monitor local weather forecasts!")
    else:
        print(f"\n⚠️  RISK ALERTS FOR {crop} in {state}:")
        for i, alert in enumerate(alerts, 1):
            print(f"\n{i}. [{alert['level']}] {alert['type']}")
            print(f"   {alert['message']}")
    
    print("=" * 70)

def feature_complete_analysis(system):
    """Feature 8: Complete Farm Analysis"""
    print("\n" + "=" * 70)
    print(" 8️⃣  COMPLETE FARM ANALYSIS")
    print("=" * 70)
    
    print("\n📝 Please provide your farm details:")
    crop = input("Crop name: ").strip()
    state = input("State: ").strip()
    season = input("Season: ").strip()
    area = float(input("Cultivated area (hectares): ") or "100")
    
    print("\n" + "=" * 70)
    print(f" 🌾 COMPLETE ANALYSIS FOR {crop} IN {state}")
    print("=" * 70)
    
    # 1. Soil Suitability
    print("\n1️⃣ SOIL SUITABILITY:")
    print("-" * 70)
    soil_result = system['soil_checker'].check(state, crop)
    if soil_result['suitable']:
        print(f"✅ Soil is suitable ({soil_result['score']:.1f}% match)")
    else:
        print(f"⚠️ Soil needs improvement ({soil_result['score']:.1f}% match)")
    
    # 2. Best Season
    print("\n2️⃣ BEST SEASON:")
    print("-" * 70)
    season_result = system['season_recommender'].recommend(crop, state)
    if season_result:
        print(f"🌟 Best: {season_result['best_season']} "
              f"(Avg: {season_result['avg_yield']:.2f} quintals/ha)")
    
    # 3. Fertilizer Recommendation
    print("\n3️⃣ FERTILIZER RECOMMENDATION:")
    print("-" * 70)
    fert_result = system['fertilizer_optimizer'].optimize(crop, state, 30)
    if fert_result:
        print(f"💡 Fertilizer: {fert_result['recommended_fertilizer']:.0f} kg")
        print(f"   Expected Yield: {fert_result['expected_yield']:.2f} quintals/ha")
    
    # 4. Market Price
    print("\n4️⃣ MARKET PRICE TREND:")
    print("-" * 70)
    price_result = system['price_analyzer'].analyze_trend(crop, state)
    if price_result:
        print(f"💰 Current: ₹{price_result['current_price']:.2f}/quintal")
        print(f"   Trend: {price_result['trend']}")
        print(f"   {price_result['advice']}")
    else:
        print("ℹ️  No price data available for this crop")
    
    # 5. Risk Alerts
    print("\n5️⃣ WEATHER RISK ALERTS:")
    print("-" * 70)
    alerts = system['risk_alerts'].check_risks(crop, state, season)
    if alerts:
        for alert in alerts:
            print(f"   {alert['message']}")
    else:
        print("✅ No significant risks detected")
    
    print("\n" + "=" * 70)
    print(" ✅ ANALYSIS COMPLETE")
    print("=" * 70)

def main():
    """Main application loop"""
    
    # Initialize system
    try:
        system = initialize_system()
    except Exception as e:
        print(f"\n❌ Error initializing system: {e}")
        print("   Please ensure all CSV files are present in the directory.")
        sys.exit(1)
    
    while True:
        print_header()
        print_menu()
        
        choice = input("\n👉 Enter your choice (0-9): ").strip()
        
        if choice == '0':
            print("\n👋 Thank you for using Farming Advisory System!")
            print("   Happy Farming! 🌾")
            break
        
        elif choice == '1':
            feature_soil_suitability(system)
        
        elif choice == '2':
            feature_yield_prediction(system)
        
        elif choice == '3':
            feature_best_season(system)
        
        elif choice == '4':
            feature_fertilizer_optimizer(system)
        
        elif choice == '5':
            feature_crop_comparison(system)
        
        elif choice == '6':
            feature_market_prices(system)
        
        elif choice == '7':
            feature_risk_alerts(system)
        
        elif choice == '8':
            feature_complete_analysis(system)
        
        elif choice == '9':
            get_available_items(system)
        
        else:
            print("\n❌ Invalid choice. Please try again.")
        
        input("\n📌 Press Enter to continue...")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
