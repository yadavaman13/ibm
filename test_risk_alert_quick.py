"""
Risk Alert System - Quick Test

Automated test without user input.
"""

import pandas as pd
from datetime import datetime

def load_crop_calendar():
    """Load the cleaned crop calendar data."""
    df = pd.read_csv('data/processed/crop_calendar_cleaned.csv')
    return df

def parse_date_period(date_str):
    """Parse date strings like "15th June - 15th Aug" into month ranges."""
    if pd.isna(date_str) or date_str == '':
        return None
    
    months = {
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
        'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
    }
    
    date_str_lower = date_str.lower()
    found_months = []
    for month_name, month_num in months.items():
        if month_name in date_str_lower:
            found_months.append(month_num)
    
    if len(found_months) >= 2:
        return (found_months[0], found_months[1])
    elif len(found_months) == 1:
        return (found_months[0], found_months[0])
    
    return None

def get_current_season():
    """Determine current season based on month."""
    month = datetime.now().month
    
    if month in [6, 7, 8, 9]:
        return "Kharif"
    elif month in [10, 11, 12, 1, 2, 3]:
        return "Rabi"
    elif month in [4, 5]:
        return "Summer"
    else:
        return "Unknown"

def check_sowing_risk(crop, state, df):
    """Check if it's the right time to sow a crop."""
    
    query = (df['crop'].str.lower() == crop.lower()) & (df['state'].str.lower() == state.lower())
    results = df[query]
    
    if len(results) == 0:
        return None
    
    current_month = datetime.now().month
    current_season = get_current_season()
    
    alerts = []
    
    for _, row in results.head(3).iterrows():  # Show first 3 districts
        sowing_range = parse_date_period(row['sowing_period'])
        season = row['season']
        district_name = row['district']
        
        alert = {
            'district': district_name,
            'season': season,
            'sowing_period': row['sowing_period'],
            'harvesting_period': row['harvesting_period'],
            'status': 'UNKNOWN',
            'message': '',
            'risk_level': 'MEDIUM'
        }
        
        if sowing_range:
            start_month, end_month = sowing_range
            
            if start_month <= end_month:
                in_window = start_month <= current_month <= end_month
            else:
                in_window = current_month >= start_month or current_month <= end_month
            
            if in_window:
                alert['status'] = 'OPTIMAL'
                alert['message'] = f"✅ OPTIMAL TIME! You're within the sowing window for {season} season"
                alert['risk_level'] = 'LOW'
            elif current_month < start_month:
                months_to_wait = start_month - current_month
                alert['status'] = 'TOO_EARLY'
                alert['message'] = f"⚠️ TOO EARLY! Wait {months_to_wait} month(s) before sowing"
                alert['risk_level'] = 'MEDIUM'
            else:
                alert['status'] = 'TOO_LATE'
                alert['message'] = f"⚠️ TOO LATE! Sowing window has passed for {season} season"
                alert['risk_level'] = 'HIGH'
        
        alerts.append(alert)
    
    return {
        'crop': crop,
        'state': state,
        'current_month': datetime.now().strftime('%B'),
        'current_season': current_season,
        'alerts': alerts
    }

def main():
    print("\n" + "="*70)
    print("🌾 RISK ALERT SYSTEM - AUTOMATED TEST")
    print("="*70 + "\n")
    
    # Load data
    df = load_crop_calendar()
    print(f"📊 Loaded crop calendar data:")
    print(f"   Records: {len(df):,}")
    print(f"   States: {df['state'].nunique()}")
    print(f"   Districts: {df['district'].nunique()}")
    print(f"   Crops: {df['crop'].nunique()}")
    print(f"\n   Current Date: {datetime.now().strftime('%B %d, %Y')}")
    print(f"   Current Season: {get_current_season()}")
    print("\n" + "="*70 + "\n")
    
    # Test cases
    test_cases = [
        ("Rice", "Bihar"),
        ("Wheat", "UP"),
        ("Maize", "MP"),
        ("Cotton", "Gujarat"),
        ("Groundnut", "Gujarat")
    ]
    
    for i, (crop, state) in enumerate(test_cases, 1):
        print(f"\n{'='*70}")
        print(f"TEST {i}/5: {crop.upper()} in {state.upper()}")
        print('='*70 + "\n")
        
        result = check_sowing_risk(crop, state, df)
        
        if result is None:
            print(f"❌ No data found for {crop} in {state}\n")
            continue
        
        for alert in result['alerts']:
            print(f"📍 District: {alert['district']}")
            print(f"   Season: {alert['season']}")
            print(f"   Sowing Period: {alert['sowing_period']}")
            print(f"   Harvesting Period: {alert['harvesting_period']}")
            print(f"\n   {alert['message']}")
            
            if alert['risk_level'] == 'LOW':
                print(f"   🟢 Risk Level: LOW - Proceed with sowing")
            elif alert['risk_level'] == 'MEDIUM':
                print(f"   🟡 Risk Level: MEDIUM - Monitor conditions")
            else:
                print(f"   🔴 Risk Level: HIGH - Not recommended")
            print()
    
    print("\n" + "="*70)
    print("✅ RISK ALERT SYSTEM TEST COMPLETE!")
    print("="*70)
    print("\n💡 Key Features Demonstrated:")
    print("   ✅ Sowing time validation")
    print("   ✅ Risk level assessment")
    print("   ✅ Season-based recommendations")
    print("   ✅ District-level information")
    print("   ✅ Multi-season crop support")
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    main()
