"""
Quick Status Check - Disease Detection System
"""
import sys
from pathlib import Path

print("="*60)
print("QUICK STATUS CHECK")
print("="*60)

# 1. Check TensorFlow
print("\n[1] TensorFlow Status:")
try:
    import tensorflow as tf
    print(f"✅ Installed: {tf.__version__}")
except ImportError:
    print("❌ NOT INSTALLED - This is the root cause!")
    print("   Fix: pip install tensorflow>=2.15.0")
    sys.exit(1)

# 2. Check Model File
print("\n[2] Model File:")
model_path = Path("app/models/ml/plant_disease_recog_model_pwp.keras")
if model_path.exists():
    size_mb = model_path.stat().st_size / (1024*1024)
    print(f"✅ Found: {size_mb:.1f} MB")
else:
    print(f"❌ NOT FOUND at {model_path}")

# 3. Check Disease Database
print("\n[3] Disease Database:")
db_path = Path("app/data/plant_diseases.json")
if db_path.exists():
    import json
    with open(db_path) as f:
        db = json.load(f)
    print(f"✅ Found: {len(db)} diseases")
else:
    print("❌ NOT FOUND")

# 4. Try to initialize service
print("\n[4] ML Service:")
try:
    from app.services.ml_disease_service import MLDiseaseDetectionService
    service = MLDiseaseDetectionService()
    print(f"✅ Initialized")
    print(f"   Model loaded: {service.model_loaded}")
    
    if not service.model_loaded:
        print("⚠️  Model NOT loaded - server will use fallback")
except Exception as e:
    print(f"❌ Failed: {e}")

# 5. Check if server can start
print("\n[5] Server Config:")
try:
    from app.config import settings
    print(f"✅ Port: {settings.PORT}")
    print(f"✅ Host: {settings.HOST}")
except Exception as e:
    print(f"❌ Config error: {e}")

print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print("\nIf all checks passed (✅), the system is ready.")
print("If any failed (❌), fix those issues first.")
print("\nTo start server: python run.py")
print("="*60)
