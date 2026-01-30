"""
Clean and Validate Extracted Crop Calendar Data

This script cleans the extracted crop calendar data and prepares it for use
in the farming advisory system.
"""

import pandas as pd
import os

def clean_crop_calendar():
    """
    Clean and validate the extracted crop calendar data.
    """
    
    print("\n" + "="*70)
    print("🧹 CLEANING CROP CALENDAR DATA")
    print("="*70 + "\n")
    
    # Load extracted data
    df = pd.read_csv('data/processed/crop_calendar_extracted.csv')
    print(f"📂 Loaded {len(df):,} rows")
    
    # Remove the header row (row index 0 which has "From To")
    df = df[df['Sl. No.'] != '']
    df = df[~df['State'].isna()]
    
    # Remove rows where State is empty or district code is missing
    initial_rows = len(df)
    df = df.dropna(subset=['State', 'Crop'])
    print(f"🗑️  Removed {initial_rows - len(df)} empty rows")
    
    # Rename columns for easier access
    df = df.rename(columns={
        'Sl. No.': 'sl_no',
        'State': 'state',
        'Name of the district (All districts)': 'district',
        'District code': 'district_code',
        'Crop': 'crop',
        'Season': 'season',
        'Sowing Period': 'sowing_period',
        'Harvesting period': 'harvesting_period'
    })
    
    # Clean text fields
    for col in ['state', 'district', 'crop', 'season']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
    
    # Remove duplicates
    initial_rows = len(df)
    df = df.drop_duplicates(subset=['state', 'district', 'crop', 'season'], keep='first')
    print(f"🗑️  Removed {initial_rows - len(df)} duplicate rows")
    
    print(f"\n✅ Cleaned data: {len(df):,} rows")
    
    # Show statistics
    print(f"\n📊 STATISTICS:")
    print("="*70)
    print(f"   States covered: {df['state'].nunique()}")
    print(f"   Districts covered: {df['district'].nunique()}")
    print(f"   Crops covered: {df['crop'].nunique()}")
    print(f"   Seasons: {df['season'].unique()}")
    
    # Show top crops
    print(f"\n🌾 TOP 10 CROPS BY ENTRIES:")
    print("="*70)
    top_crops = df['crop'].value_counts().head(10)
    for crop, count in top_crops.items():
        print(f"   {crop:30} {count:4} entries")
    
    # Show states
    print(f"\n🗺️  STATES COVERED:")
    print("="*70)
    states = df['state'].value_counts()
    for state, count in states.items():
        print(f"   {state:30} {count:4} entries")
    
    # Save cleaned data
    output_file = 'data/processed/crop_calendar_cleaned.csv'
    df.to_csv(output_file, index=False)
    print(f"\n💾 Saved cleaned data to: {output_file}")
    
    # Show sample
    print(f"\n📋 SAMPLE DATA (first 10 rows):")
    print("="*70)
    print(df[['state', 'district', 'crop', 'season', 'sowing_period', 'harvesting_period']].head(10).to_string(index=False))
    
    return df

def create_summary():
    """
    Create a summary of the crop calendar data.
    """
    
    df = pd.read_csv('data/processed/crop_calendar_cleaned.csv')
    
    print("\n" + "="*70)
    print("📋 CROP CALENDAR SUMMARY")
    print("="*70 + "\n")
    
    summary = {
        'Total Entries': len(df),
        'States': df['state'].nunique(),
        'Districts': df['district'].nunique(),
        'Crops': df['crop'].nunique(),
        'Unique State-Crop Combinations': df.groupby(['state', 'crop']).ngroups
    }
    
    for key, value in summary.items():
        print(f"   {key:35} {value:,}")
    
    # Create state-wise summary
    state_summary = df.groupby('state').agg({
        'district': 'nunique',
        'crop': 'nunique',
        'sl_no': 'count'
    }).rename(columns={
        'district': 'districts',
        'crop': 'crops',
        'sl_no': 'total_entries'
    })
    
    print(f"\n📊 STATE-WISE BREAKDOWN:")
    print("="*70)
    print(state_summary.to_string())
    
    # Save summary
    state_summary.to_csv('data/processed/crop_calendar_state_summary.csv')
    print(f"\n💾 State summary saved to: data/processed/crop_calendar_state_summary.csv")

def main():
    """
    Main execution.
    """
    
    # Clean data
    df = clean_crop_calendar()
    
    # Create summary
    create_summary()
    
    print("\n" + "="*70)
    print("✅ CROP CALENDAR DATA READY!")
    print("="*70)
    print(f"\n📁 Files created:")
    print(f"   1. data/processed/crop_calendar_cleaned.csv - Clean data ({len(df):,} rows)")
    print(f"   2. data/processed/crop_calendar_state_summary.csv - State-wise summary")
    print(f"\n🎯 This data can now be used for:")
    print(f"   - Risk alert system")
    print(f"   - Sowing period recommendations")
    print(f"   - Harvesting time predictions")
    print(f"   - Season-based crop suggestions")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
