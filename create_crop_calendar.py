"""
Crop Calendar Template Generator

Creates a structured crop calendar dataset needed for:
- Feature #2: Risk Alert System
- Feature #1: Crop & Weather Decision Advice

This dataset defines when crops should be sown and harvested in each state.
"""

import pandas as pd
import os

def create_crop_calendar_template():
    """
    Generate template CSV for crop calendar data.
    Includes sample data for major crops.
    """
    
    # Sample data for 15 major crops
    sample_data = [
        # Kharif crops (June-October)
        {
            'crop': 'Rice',
            'state': 'Punjab',
            'sowing_start_month': 6,  # June
            'sowing_end_month': 7,    # July
            'harvest_start_month': 10, # October
            'harvest_end_month': 11,   # November
            'growth_days': 120,
            'optimal_temp_min': 20,
            'optimal_temp_max': 35,
            'optimal_rainfall_min': 1200,
            'optimal_rainfall_max': 1800,
            'drought_threshold': 800,
            'flood_threshold': 2500,
            'critical_growth_stages': 'Transplanting, Flowering, Grain filling'
        },
        {
            'crop': 'Cotton',
            'state': 'Maharashtra',
            'sowing_start_month': 6,
            'sowing_end_month': 7,
            'harvest_start_month': 10,
            'harvest_end_month': 12,
            'growth_days': 150,
            'optimal_temp_min': 21,
            'optimal_temp_max': 35,
            'optimal_rainfall_min': 600,
            'optimal_rainfall_max': 1200,
            'drought_threshold': 400,
            'flood_threshold': 1500,
            'critical_growth_stages': 'Sowing, Flowering, Boll formation'
        },
        {
            'crop': 'Maize',
            'state': 'Karnataka',
            'sowing_start_month': 6,
            'sowing_end_month': 7,
            'harvest_start_month': 9,
            'harvest_end_month': 10,
            'growth_days': 90,
            'optimal_temp_min': 18,
            'optimal_temp_max': 32,
            'optimal_rainfall_min': 500,
            'optimal_rainfall_max': 900,
            'drought_threshold': 350,
            'flood_threshold': 1200,
            'critical_growth_stages': 'Germination, Tasseling, Grain filling'
        },
        
        # Rabi crops (October-March)
        {
            'crop': 'Wheat',
            'state': 'Punjab',
            'sowing_start_month': 11,
            'sowing_end_month': 12,
            'harvest_start_month': 3,
            'harvest_end_month': 4,
            'growth_days': 120,
            'optimal_temp_min': 10,
            'optimal_temp_max': 25,
            'optimal_rainfall_min': 300,
            'optimal_rainfall_max': 600,
            'drought_threshold': 200,
            'flood_threshold': 800,
            'critical_growth_stages': 'Germination, Crown root stage, Heading'
        },
        {
            'crop': 'Chickpea',
            'state': 'Madhya Pradesh',
            'sowing_start_month': 10,
            'sowing_end_month': 11,
            'harvest_start_month': 2,
            'harvest_end_month': 3,
            'growth_days': 110,
            'optimal_temp_min': 15,
            'optimal_temp_max': 30,
            'optimal_rainfall_min': 350,
            'optimal_rainfall_max': 650,
            'drought_threshold': 250,
            'flood_threshold': 900,
            'critical_growth_stages': 'Flowering, Pod formation'
        },
        
        # Year-round / Zaid crops
        {
            'crop': 'Tomato',
            'state': 'Karnataka',
            'sowing_start_month': 1,  # Multiple seasons
            'sowing_end_month': 3,
            'harvest_start_month': 4,
            'harvest_end_month': 6,
            'growth_days': 80,
            'optimal_temp_min': 18,
            'optimal_temp_max': 30,
            'optimal_rainfall_min': 200,
            'optimal_rainfall_max': 600,
            'drought_threshold': 150,
            'flood_threshold': 800,
            'critical_growth_stages': 'Transplanting, Flowering, Fruit set'
        },
        {
            'crop': 'Sugarcane',
            'state': 'Uttar Pradesh',
            'sowing_start_month': 2,
            'sowing_end_month': 4,
            'harvest_start_month': 12,
            'harvest_end_month': 3,  # Next year
            'growth_days': 360,
            'optimal_temp_min': 20,
            'optimal_temp_max': 35,
            'optimal_rainfall_min': 1500,
            'optimal_rainfall_max': 2500,
            'drought_threshold': 1000,
            'flood_threshold': 3000,
            'critical_growth_stages': 'Germination, Grand growth, Maturity'
        },
    ]
    
    df = pd.DataFrame(sample_data)
    
    # Add metadata columns
    df['data_source'] = 'Manual entry - Agriculture dept. guidelines'
    df['last_updated'] = pd.Timestamp.now().strftime('%Y-%m-%d')
    df['verified'] = 'Yes'
    
    # Create templates directory
    os.makedirs('data/templates', exist_ok=True)
    output_path = 'data/templates/crop_calendar_template.csv'
    
    df.to_csv(output_path, index=False)
    
    print("=" * 70)
    print("🌱 CROP CALENDAR TEMPLATE GENERATED")
    print("=" * 70)
    print(f"✅ File: {output_path}")
    print(f"📊 Rows: {len(df)} (sample data for major crops)")
    print(f"📋 Columns: {len(df.columns)}")
    print("\n📝 Column Descriptions:")
    print("-" * 70)
    print("crop                    : Crop name (must match crop_yield.csv)")
    print("state                   : State name (must match other datasets)")
    print("sowing_start_month      : Month when sowing begins (1-12)")
    print("sowing_end_month        : Month when sowing ends (1-12)")
    print("harvest_start_month     : Month when harvest begins (1-12)")
    print("harvest_end_month       : Month when harvest ends (1-12)")
    print("growth_days             : Total crop duration in days")
    print("optimal_temp_min        : Minimum optimal temperature (°C)")
    print("optimal_temp_max        : Maximum optimal temperature (°C)")
    print("optimal_rainfall_min    : Minimum optimal rainfall (mm)")
    print("optimal_rainfall_max    : Maximum optimal rainfall (mm)")
    print("drought_threshold       : Rainfall below this = drought risk (mm)")
    print("flood_threshold         : Rainfall above this = flood risk (mm)")
    print("critical_growth_stages  : Key stages when weather matters most")
    print("-" * 70)
    
    print("\n📌 NEXT STEPS:")
    print("-" * 70)
    print("1. Review the sample data in the CSV")
    print("2. Add more crop-state combinations (target: 200-500 rows)")
    print("3. Verify data from state agriculture department websites:")
    print("   - Punjab: https://agri.punjab.gov.in/")
    print("   - Maharashtra: https://krishi.maharashtra.gov.in/")
    print("   - Karnataka: https://raitamitra.karnataka.gov.in/")
    print("4. Cross-check with ICAR guidelines")
    print("5. Save final version as: data/crop_calendar.csv")
    print("-" * 70)
    
    print("\n🎯 PRIORITY CROPS TO ADD (use crop_yield.csv for full list):")
    print("-" * 70)
    
    # Read existing crop yield data to show which crops need calendar data
    if os.path.exists('crop_yield.csv'):
        cy = pd.read_csv('crop_yield.csv')
        all_crops = cy['crop'].unique()
        current_crops = df['crop'].unique()
        missing_crops = [c for c in all_crops if c not in current_crops]
        
        print(f"Total crops in dataset: {len(all_crops)}")
        print(f"Crops with calendar data: {len(current_crops)}")
        print(f"Missing calendar data: {len(missing_crops)}")
        print(f"\nTop 20 missing crops: {missing_crops[:20]}")
    
    print("\n" + "=" * 70)
    
    return df


def create_data_directories():
    """Create organized folder structure for data files."""
    
    directories = [
        'data/raw',           # Original downloaded files
        'data/processed',     # Cleaned, merged data
        'data/sample',        # Mock data for demos
        'data/templates',     # Templates to fill
        'data/external',      # Weather API cache, etc.
    ]
    
    for dir_path in directories:
        os.makedirs(dir_path, exist_ok=True)
        
        # Create README in each folder
        readme_path = os.path.join(dir_path, 'README.md')
        with open(readme_path, 'w') as f:
            if 'raw' in dir_path:
                f.write("# Raw Data\n\nOriginal files downloaded from sources.\n"
                       "Do not modify. Use processing scripts to clean.")
            elif 'processed' in dir_path:
                f.write("# Processed Data\n\nCleaned and merged datasets.\n"
                       "These are used by the application.")
            elif 'sample' in dir_path:
                f.write("# Sample Data\n\nMock data for testing and demos.\n"
                       "Replace with real data before production.")
            elif 'templates' in dir_path:
                f.write("# Templates\n\nCSV templates to fill with real data.\n"
                       "Follow column descriptions carefully.")
            elif 'external' in dir_path:
                f.write("# External Data\n\nAPI responses, cached weather data.\n"
                       "Auto-generated, can be deleted.")
    
    print("✅ Data directory structure created:")
    for d in directories:
        print(f"   📁 {d}/")


if __name__ == '__main__':
    print("\n🌾 Crop Calendar Generator\n")
    
    create_data_directories()
    print()
    df = create_crop_calendar_template()
    
    print("\n✅ Setup complete! You can now:")
    print("   1. Open: data/templates/crop_calendar_template.csv")
    print("   2. Add more crop-state combinations")
    print("   3. Use this data in your risk alert system")
