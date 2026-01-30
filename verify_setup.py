"""
Setup Verification Script

Run this to verify all dependencies and datasets are ready.
"""

import sys
import os

def check_imports():
    """Check if all required packages are installed."""
    print("\n" + "="*70)
    print("📦 CHECKING PACKAGE INSTALLATIONS")
    print("="*70 + "\n")
    
    packages = {
        'pandas': 'Data manipulation',
        'numpy': 'Numerical computing',
        'sklearn': 'Machine learning',
        'scipy': 'Scientific computing',
        'matplotlib': 'Plotting',
        'seaborn': 'Statistical visualization',
        'pdfplumber': 'PDF extraction',
        'PyPDF2': 'PDF processing',
        'openpyxl': 'Excel support'
    }
    
    all_good = True
    for package, description in packages.items():
        try:
            __import__(package)
            print(f"✅ {package:15} - {description}")
        except ImportError:
            print(f"❌ {package:15} - {description} (NOT INSTALLED)")
            all_good = False
    
    return all_good

def check_datasets():
    """Check if all required datasets exist."""
    print("\n" + "="*70)
    print("📊 CHECKING DATASETS")
    print("="*70 + "\n")
    
    datasets = {
        'crop_yield.csv': 'Core crop yield data',
        'state_soil_data.csv': 'Soil NPK and pH data',
        'state_weather_data_1997_2020.csv': 'Historical weather data',
        'data/processed/merged_dataset.csv': 'ML-ready merged data',
        'data/processed/crop_calendar_cleaned.csv': 'Crop calendar (6,293 records)',
        'data/sample/mandi_prices_sample.csv': 'Sample price data'
    }
    
    all_good = True
    for filepath, description in datasets.items():
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"✅ {filepath:45} - {description} ({size:,} bytes)")
        else:
            print(f"❌ {filepath:45} - {description} (NOT FOUND)")
            all_good = False
    
    return all_good

def check_scripts():
    """Check if all helper scripts exist."""
    print("\n" + "="*70)
    print("🐍 CHECKING SCRIPTS")
    print("="*70 + "\n")
    
    scripts = {
        'merge_datasets.py': 'Data merger',
        'extract_crop_calendar_pdf.py': 'PDF extractor',
        'clean_crop_calendar.py': 'Data cleaner',
        'test_risk_alert_system.py': 'Risk alert tester',
        'dataset_overview.py': 'Dataset readiness checker'
    }
    
    all_good = True
    for script, description in scripts.items():
        if os.path.exists(script):
            print(f"✅ {script:40} - {description}")
        else:
            print(f"❌ {script:40} - {description} (NOT FOUND)")
            all_good = False
    
    return all_good

def main():
    """Main verification function."""
    print("\n" + "="*70)
    print("🌾 FARMING ADVISORY SYSTEM - SETUP VERIFICATION")
    print("="*70)
    
    # Check Python version
    print(f"\n🐍 Python Version: {sys.version.split()[0]}")
    if sys.version_info < (3, 8):
        print("⚠️  Warning: Python 3.8+ recommended")
    else:
        print("✅ Python version OK")
    
    # Run checks
    packages_ok = check_imports()
    datasets_ok = check_datasets()
    scripts_ok = check_scripts()
    
    # Final summary
    print("\n" + "="*70)
    print("📋 VERIFICATION SUMMARY")
    print("="*70 + "\n")
    
    if packages_ok:
        print("✅ All packages installed")
    else:
        print("❌ Some packages missing - run: pip install -r requirements.txt")
    
    if datasets_ok:
        print("✅ All datasets present")
    else:
        print("⚠️  Some datasets missing - run setup scripts")
    
    if scripts_ok:
        print("✅ All helper scripts present")
    else:
        print("❌ Some scripts missing")
    
    if packages_ok and datasets_ok and scripts_ok:
        print("\n🎉 SETUP COMPLETE! Ready to build features.")
        print("\n📚 Next steps:")
        print("   1. Read: QUICK_START_GUIDE.md")
        print("   2. Test: python test_risk_alert_system.py")
        print("   3. Build: Start implementing features")
    else:
        print("\n⚠️  Setup incomplete. Fix issues above before continuing.")
    
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    main()
