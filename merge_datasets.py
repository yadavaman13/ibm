"""
Dataset Merger - Combine all datasets for ML model training

This script merges crop_yield, soil, and weather data into one master dataset
ready for ML model training.
"""

import pandas as pd
import os

def merge_datasets():
    """
    Merge all 3 datasets on state and year.
    Creates a master dataset with all features.
    """
    
    print("\n" + "="*70)
    print("🔄 MERGING DATASETS")
    print("="*70 + "\n")
    
    # Load datasets
    print("📂 Loading datasets...")
    crop = pd.read_csv('crop_yield.csv')
    soil = pd.read_csv('state_soil_data.csv')
    weather = pd.read_csv('state_weather_data_1997_2020.csv')
    
    print(f"✅ crop_yield.csv: {len(crop):,} rows")
    print(f"✅ state_soil_data.csv: {len(soil):,} rows")
    print(f"✅ state_weather_data.csv: {len(weather):,} rows")
    
    # Merge crop with weather (on state + year)
    print("\n🔗 Merging crop + weather data (on state, year)...")
    merged = crop.merge(weather, on=['state', 'year'], how='left')
    print(f"   Result: {len(merged):,} rows")
    
    # Merge with soil (on state only - soil data is constant across years)
    print("🔗 Merging + soil data (on state)...")
    merged = merged.merge(soil, on='state', how='left')
    print(f"   Result: {len(merged):,} rows")
    
    # Check for missing values
    missing = merged.isna().sum().sum()
    if missing > 0:
        print(f"\n⚠️ Warning: {missing} missing values detected")
        print("\nMissing values by column:")
        print(merged.isna().sum()[merged.isna().sum() > 0])
    else:
        print(f"\n✅ No missing values - perfect merge!")
    
    # Save merged dataset
    os.makedirs('data/processed', exist_ok=True)
    output_path = 'data/processed/merged_dataset.csv'
    merged.to_csv(output_path, index=False)
    
    print(f"\n💾 Saved to: {output_path}")
    print(f"   Rows: {len(merged):,}")
    print(f"   Columns: {len(merged.columns)}")
    
    # Show column summary
    print("\n📋 MERGED DATASET COLUMNS:")
    print("-"*70)
    for i, col in enumerate(merged.columns, 1):
        print(f"{i:2}. {col:30} | Type: {merged[col].dtype}")
    
    # Show sample
    print("\n📊 SAMPLE ROWS (first 3):")
    print("-"*70)
    print(merged.head(3).to_string(index=False))
    
    # Statistics
    print("\n📈 DATASET STATISTICS:")
    print("-"*70)
    print(f"   Total records: {len(merged):,}")
    print(f"   Unique crops: {merged['crop'].nunique()}")
    print(f"   Unique states: {merged['state'].nunique()}")
    print(f"   Years: {merged['year'].min()} - {merged['year'].max()}")
    print(f"   Seasons: {merged['season'].unique().tolist()}")
    print(f"   Avg yield: {merged['yield'].mean():.2f} quintal/ha")
    print(f"   Avg rainfall: {merged['total_rainfall_mm'].mean():.2f} mm/year")
    print(f"   Avg temperature: {merged['avg_temp_c'].mean():.2f} °C")
    
    print("\n" + "="*70)
    print("✅ MERGE COMPLETE!")
    print("="*70)
    print("\n🎯 Next step: Use this dataset to train ML models")
    print("   Example: python train_yield_model.py")
    
    return merged


def create_feature_subsets(merged_df):
    """
    Create feature subsets for different ML tasks.
    """
    
    print("\n" + "="*70)
    print("🎯 CREATING FEATURE SUBSETS")
    print("="*70 + "\n")
    
    # For yield prediction
    yield_features = [
        'crop', 'state', 'season', 'area', 'fertilizer', 'pesticide',
        'avg_temp_c', 'total_rainfall_mm', 'avg_humidity_percent',
        'N', 'P', 'K', 'pH'
    ]
    yield_target = 'yield'
    
    print("1️⃣ YIELD PREDICTION MODEL")
    print(f"   Features ({len(yield_features)}): {', '.join(yield_features)}")
    print(f"   Target: {yield_target}")
    
    # For production prediction
    production_features = yield_features.copy()
    production_target = 'production'
    
    print("\n2️⃣ PRODUCTION PREDICTION MODEL")
    print(f"   Features ({len(production_features)}): {', '.join(production_features)}")
    print(f"   Target: {production_target}")
    
    # For fertilizer optimization
    fertilizer_features = [
        'crop', 'state', 'season', 'area', 'N', 'P', 'K', 'pH',
        'avg_temp_c', 'total_rainfall_mm'
    ]
    fertilizer_target = 'fertilizer'
    
    print("\n3️⃣ FERTILIZER OPTIMIZATION MODEL")
    print(f"   Features ({len(fertilizer_features)}): {', '.join(fertilizer_features)}")
    print(f"   Target: {fertilizer_target}")
    
    print("\n" + "="*70)


if __name__ == '__main__':
    print("\n🌾 Dataset Merger Tool\n")
    
    # Check if datasets exist
    required_files = [
        'crop_yield.csv',
        'state_soil_data.csv',
        'state_weather_data_1997_2020.csv'
    ]
    
    missing = [f for f in required_files if not os.path.exists(f)]
    if missing:
        print(f"❌ Missing files: {missing}")
        print("   Please ensure all datasets are in the current directory.")
        exit(1)
    
    # Merge datasets
    merged = merge_datasets()
    
    # Create feature subsets guide
    create_feature_subsets(merged)
    
    print("\n✅ All done! You can now:")
    print("   1. Open data/processed/merged_dataset.csv in Excel/Pandas")
    print("   2. Use it for ML model training")
    print("   3. Perform exploratory data analysis")
    print()
