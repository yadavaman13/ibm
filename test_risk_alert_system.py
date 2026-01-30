"""
Risk Alert System - Test & Demo

This script demonstrates the risk alert system using the extracted crop calendar data.
"""

import pandas as pd
from datetime import datetime
import re

def load_crop_calendar():
    """Load the cleaned crop calendar data."""
    try:
        df = pd.read_csv('data/processed/crop_calendar_cleaned.csv')
        return df
    except FileNotFoundError:
        print("❌ Error: Crop calendar data not found!")
        print("   Run: python clean_crop_calendar.py first")
        return None

def parse_date_period(date_str):
    """
    Parse date strings like "15th June - 15th Aug" into month ranges.
    Returns tuple of (start_month, end_month) or None if can't parse.
    """
    if pd.isna(date_str) or date_str == '':
        return None
    
    # Extract month names
    months = {
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
        'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
    }
    
    date_str_lower = date_str.lower()
    
    # Find all month names in the string
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
    
    # Indian agricultural seasons
    if month in [6, 7, 8, 9]:  # June-September
        return "Kharif"
    elif month in [10, 11, 12, 1, 2, 3]:  # October-March
        return "Rabi"
    elif month in [4, 5]:  # April-May
        return "Summer"
    else:
        return "Unknown"

def check_sowing_risk(crop, state, district=None):
    """
    Check if it's the right time to sow a crop.
    Returns risk alert and recommendation.
    """
    df = load_crop_calendar()
    if df is None:
        return None
    
    # Filter data
    query = (df['crop'].str.lower() == crop.lower()) & (df['state'].str.lower() == state.lower())
    
    if district:
        query = query & (df['district'].str.lower() == district.lower())
    
    results = df[query]
    
    if len(results) == 0:
        return {
            'status': 'NO_DATA',
            'message': f"❌ No crop calendar data found for {crop} in {state}",
            'recommendation': "Try a different crop or check spelling"
        }
    
    # Get current date
    current_month = datetime.now().month
    current_season = get_current_season()
    
    alerts = []
    
    for _, row in results.iterrows():
        sowing_range = parse_date_period(row['sowing_period'])
        harvesting_range = parse_date_period(row['harvesting_period'])
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
            
            # Check if current month is within sowing window
            if start_month <= end_month:
                # Normal range (e.g., June to August)
                in_window = start_month <= current_month <= end_month
            else:
                # Wrapped range (e.g., November to January)
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

def display_risk_alert(result):
    """Display risk alert in a formatted way."""
    
    if result is None:
        return
    
    if result.get('status') == 'NO_DATA':
        print(f"\n{result['message']}")
        print(f"💡 {result['recommendation']}\n")
        return
    
    print("\n" + "="*70)
    print(f"🌾 RISK ALERT: {result['crop'].upper()} in {result['state'].upper()}")
    print("="*70)
    print(f"📅 Current Date: {datetime.now().strftime('%B %d, %Y')}")
    print(f"🌦️  Current Season: {result['current_season']}")
    print("="*70 + "\n")
    
    for i, alert in enumerate(result['alerts'], 1):
        print(f"📍 District: {alert['district']}")
        print(f"   Season: {alert['season']}")
        print(f"   Sowing Period: {alert['sowing_period']}")
        print(f"   Harvesting Period: {alert['harvesting_period']}")
        print(f"\n   {alert['message']}")
        
        # Risk indicator
        if alert['risk_level'] == 'LOW':
            print(f"   🟢 Risk Level: LOW - Proceed with sowing")
        elif alert['risk_level'] == 'MEDIUM':
            print(f"   🟡 Risk Level: MEDIUM - Monitor conditions")
        else:
            print(f"   🔴 Risk Level: HIGH - Not recommended")
        
        print()
    
    print("="*70 + "\n")

def get_crops_for_state(state):
    """Get all available crops for a state."""
    df = load_crop_calendar()
    if df is None:
        return []
    
    crops = df[df['state'].str.lower() == state.lower()]['crop'].unique()
    return sorted(crops)

def get_available_states():
    """Get all available states."""
    df = load_crop_calendar()
    if df is None:
        return []
    
    return sorted(df['state'].unique())

def run_demo():
    """Run demo with example queries."""
    
    print("\n" + "="*70)
    print("🌾 RISK ALERT SYSTEM - DEMO MODE")
    print("="*70 + "\n")
    
    # Example 1: Rice in Bihar
    print("📋 EXAMPLE 1: Checking Rice in Bihar\n")
    result = check_sowing_risk("Rice", "Bihar")
    display_risk_alert(result)
    
    input("Press Enter to continue...")
    
    # Example 2: Wheat in UP
    print("\n📋 EXAMPLE 2: Checking Wheat in Uttar Pradesh\n")
    result = check_sowing_risk("Wheat", "UP")
    display_risk_alert(result)
    
    input("Press Enter to continue...")
    
    # Example 3: Maize in MP
    print("\n📋 EXAMPLE 3: Checking Maize in Madhya Pradesh\n")
    result = check_sowing_risk("Maize", "MP")
    display_risk_alert(result)
    
    input("Press Enter to continue...")
    
    # Example 4: Cotton in Gujarat
    print("\n📋 EXAMPLE 4: Checking Cotton in Gujarat\n")
    result = check_sowing_risk("Cotton", "Gujarat")
    display_risk_alert(result)

def run_interactive():
    """Run interactive mode."""
    
    print("\n" + "="*70)
    print("🌾 RISK ALERT SYSTEM - INTERACTIVE MODE")
    print("="*70 + "\n")
    
    # Show available states
    states = get_available_states()
    print("📍 Available States:")
    for i, state in enumerate(states, 1):
        print(f"   {i}. {state}")
    
    print("\n" + "="*70 + "\n")
    
    while True:
        # Get state
        state = input("Enter state name (or 'quit' to exit): ").strip()
        if state.lower() == 'quit':
            break
        
        # Check if state exists
        if state not in states and state.upper() not in states and state.title() not in states:
            print(f"❌ State '{state}' not found. Please choose from the list above.\n")
            continue
        
        # Show available crops
        crops = get_crops_for_state(state)
        if not crops:
            print(f"❌ No crops found for {state}\n")
            continue
        
        print(f"\n🌾 Available crops in {state}:")
        for i, crop in enumerate(crops[:20], 1):  # Show first 20
            print(f"   {i}. {crop}")
        if len(crops) > 20:
            print(f"   ... and {len(crops) - 20} more")
        
        # Get crop
        crop = input(f"\nEnter crop name: ").strip()
        
        # Check risk
        result = check_sowing_risk(crop, state)
        display_risk_alert(result)
        
        print()

def main():
    """Main function."""
    
    print("\n" + "="*70)
    print("🌾 RISK ALERT SYSTEM - CROP CALENDAR BASED")
    print("="*70)
    print("\nThis system uses real crop calendar data to provide:")
    print("  ✅ Sowing time recommendations")
    print("  ✅ Risk alerts for late/early sowing")
    print("  ✅ Season-based guidance")
    print("  ✅ District-level information")
    print("\n" + "="*70 + "\n")
    
    # Check if data exists
    df = load_crop_calendar()
    if df is None:
        return
    
    print(f"📊 Loaded crop calendar data:")
    print(f"   Total records: {len(df):,}")
    print(f"   States: {df['state'].nunique()}")
    print(f"   Districts: {df['district'].nunique()}")
    print(f"   Crops: {df['crop'].nunique()}")
    print(f"\n" + "="*70 + "\n")
    
    # Ask mode
    print("Choose mode:")
    print("  1. Demo mode (pre-selected examples)")
    print("  2. Interactive mode (enter your own queries)")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == '1':
        run_demo()
    elif choice == '2':
        run_interactive()
    else:
        print("Invalid choice. Running demo mode...\n")
        run_demo()
    
    print("\n" + "="*70)
    print("✅ RISK ALERT SYSTEM TEST COMPLETE!")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
