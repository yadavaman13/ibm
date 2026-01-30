"""
Script to download Agmarknet (Mandi) price data for market trend feature.

Required for Feature #4: Market Price Trend Advice

Usage:
    python download_agmarknet.py --years 2022,2023,2024 --crops Rice,Wheat,Cotton
"""

import requests
import pandas as pd
import time
from datetime import datetime, timedelta
import os

# Agmarknet API endpoint (Note: This is a template - actual API may require authentication)
# Visit: https://agmarknet.gov.in/ for official API access

BASE_URL = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
API_KEY = "YOUR_API_KEY_HERE"  # Get from https://data.gov.in/

def download_price_data(years, crops, states):
    """
    Download mandi price data from government sources.
    
    Args:
        years: List of years (e.g., [2022, 2023, 2024])
        crops: List of crop names (e.g., ['Rice', 'Wheat'])
        states: List of state names (e.g., ['Punjab', 'Haryana'])
    
    Returns:
        DataFrame with columns: date, state, market, crop, price_min, price_max, price_modal
    """
    
    print("=" * 60)
    print("AGMARKNET DATA DOWNLOADER")
    print("=" * 60)
    print(f"Years: {years}")
    print(f"Crops: {crops}")
    print(f"States: {states}")
    print("=" * 60)
    
    all_data = []
    
    for year in years:
        for crop in crops:
            for state in states:
                print(f"Downloading: {crop} - {state} - {year}...")
                
                # Example API call (adjust based on actual Agmarknet API)
                params = {
                    'api-key': API_KEY,
                    'format': 'json',
                    'filters[state]': state,
                    'filters[commodity]': crop,
                    'filters[year]': year,
                    'limit': 10000
                }
                
                try:
                    # Note: This is a template. Replace with actual API endpoint
                    # response = requests.get(BASE_URL, params=params, timeout=30)
                    # data = response.json()
                    
                    # For now, create sample data structure
                    print(f"  ⚠️  API integration pending - use manual CSV download")
                    print(f"  Visit: https://agmarknet.gov.in/")
                    print(f"  Download CSV for {crop} in {state} for year {year}")
                    
                    time.sleep(0.5)  # Rate limiting
                    
                except Exception as e:
                    print(f"  ❌ Error: {e}")
                    continue
    
    # If we had real data:
    # df = pd.DataFrame(all_data)
    # df.to_csv('data/mandi_prices.csv', index=False)
    
    print("\n" + "=" * 60)
    print("MANUAL DOWNLOAD INSTRUCTIONS:")
    print("=" * 60)
    print("1. Visit: https://agmarknet.gov.in/")
    print("2. Navigate to: 'Price & Arrivals' > 'Daily Prices'")
    print("3. Select:")
    print("   - State: (your target states)")
    print("   - Commodity: (your crops)")
    print("   - Date Range: Last 2-3 years")
    print("4. Download CSV")
    print("5. Save to: data/raw/mandi_prices_raw.csv")
    print("6. Run: python scripts/clean_mandi_data.py")
    print("=" * 60)


def create_sample_price_data():
    """
    Create sample/mock price data for demo purposes.
    Use this for initial MVP testing before real data is acquired.
    """
    print("\n📦 Creating SAMPLE price data for demo...")
    
    crops = ['Rice', 'Wheat', 'Cotton', 'Sugarcane', 'Tomato']
    states = ['Punjab', 'Haryana', 'Maharashtra', 'Uttar Pradesh', 'Tamil Nadu']
    
    # Generate 90 days of sample data
    dates = pd.date_range(end=datetime.now(), periods=90, freq='D')
    
    sample_data = []
    for crop in crops:
        base_price = {
            'Rice': 2500, 'Wheat': 2000, 'Cotton': 6000,
            'Sugarcane': 300, 'Tomato': 800
        }[crop]
        
        for state in states:
            for date in dates:
                # Add random variation
                import random
                variation = random.uniform(-0.15, 0.15)
                trend = (date - dates[0]).days * 2  # Slight upward trend
                
                price_modal = base_price + trend + (base_price * variation)
                price_min = price_modal * 0.9
                price_max = price_modal * 1.1
                
                sample_data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'state': state,
                    'market': f'{state} Mandi',
                    'crop': crop,
                    'price_min': round(price_min, 2),
                    'price_max': round(price_max, 2),
                    'price_modal': round(price_modal, 2),
                    'arrivals_tonnes': random.randint(50, 500)
                })
    
    df = pd.DataFrame(sample_data)
    
    # Create data directory
    os.makedirs('data/sample', exist_ok=True)
    output_path = 'data/sample/mandi_prices_sample.csv'
    df.to_csv(output_path, index=False)
    
    print(f"✅ Sample data created: {output_path}")
    print(f"   Rows: {len(df)}")
    print(f"   Crops: {len(crops)}")
    print(f"   States: {len(states)}")
    print(f"   Date Range: {df['date'].min()} to {df['date'].max()}")
    print("\n⚠️  NOTE: This is MOCK data for testing only!")
    print("   Replace with real Agmarknet data before production deployment.")
    
    return df


def main():
    print("\n🌾 Mandi Price Data Acquisition Tool\n")
    
    choice = input("Choose option:\n"
                   "1. Download real data (requires API key)\n"
                   "2. Generate sample data for demo\n"
                   "Enter choice (1 or 2): ")
    
    if choice == '1':
        print("\n⚠️  Real API integration requires:")
        print("   1. Register at https://data.gov.in/")
        print("   2. Get API key for Agmarknet dataset")
        print("   3. Update API_KEY in this script")
        print("   4. Review API documentation for correct endpoints")
        
        proceed = input("\nHave you completed above steps? (yes/no): ")
        if proceed.lower() == 'yes':
            years = [2022, 2023, 2024]
            crops = ['Rice', 'Wheat', 'Cotton', 'Sugarcane', 'Maize']
            states = ['Punjab', 'Haryana', 'Maharashtra', 'Uttar Pradesh']
            download_price_data(years, crops, states)
        else:
            print("\n👉 Complete setup steps first, then run this script again.")
    
    elif choice == '2':
        df = create_sample_price_data()
        print("\n✅ You can now use this sample data for MVP development!")
        print("   Load it with: pd.read_csv('data/sample/mandi_prices_sample.csv')")
    
    else:
        print("Invalid choice.")


if __name__ == '__main__':
    main()
