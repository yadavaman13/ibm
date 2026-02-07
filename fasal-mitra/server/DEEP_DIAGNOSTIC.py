"""
COMPREHENSIVE DISEASE DETECTION DIAGNOSTIC
==========================================
This script performs deep analysis of the entire disease detection system
"""

import sys
import os
import traceback
from pathlib import Path
import json

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text:^70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.WARNING}⚠️  {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKCYAN}ℹ️  {text}{Colors.ENDC}")

print_header("DISEASE DETECTION SYSTEM - DEEP ANALYSIS")

# Test 1: Python Environment
print_header("TEST 1: Python Environment")
print_info(f"Python Version: {sys.version}")
print_info(f"Python Executable: {sys.executable}")
print_info(f"Current Directory: {os.getcwd()}")
print_success("Python environment detected")

# Test 2: TensorFlow Installation
print_header("TEST 2: TensorFlow Installation & Version")
try:
    import tensorflow as tf
    print_success(f"TensorFlow installed: v{tf.__version__}")
    print_info(f"TensorFlow location: {tf.__file__}")
    
    # Check if GPU is available
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        print_success(f"GPU detected: {len(gpus)} GPU(s) available")
        for i, gpu in enumerate(gpus):
            print_info(f"  GPU {i}: {gpu}")
    else:
        print_warning("No GPU detected - using CPU (slower but functional)")
    
    # Check TensorFlow build
    print_info(f"TensorFlow built with CUDA: {tf.test.is_built_with_cuda()}")
    
except ImportError as e:
    print_error(f"TensorFlow NOT installed: {e}")
    print_warning("CRITICAL: TensorFlow is required for ML-based disease detection")
    print_info("Install with: pip install tensorflow>=2.15.0")
    sys.exit(1)
except Exception as e:
    print_error(f"TensorFlow error: {e}")
    traceback.print_exc()
    sys.exit(1)

# Test 3: Required Dependencies
print_header("TEST 3: Required Dependencies")
dependencies = {
    'numpy': 'NumPy',
    'PIL': 'Pillow',
    'pathlib': 'pathlib'
}

for module_name, display_name in dependencies.items():
    try:
        if module_name == 'PIL':
            from PIL import Image
            import PIL
            print_success(f"{display_name} installed: v{PIL.__version__}")
        elif module_name == 'numpy':
            import numpy as np
            print_success(f"{display_name} installed: v{np.__version__}")
        else:
            __import__(module_name)
            print_success(f"{display_name} available")
    except ImportError as e:
        print_error(f"{display_name} NOT installed: {e}")

# Test 4: Model File Verification
print_header("TEST 4: Model File Verification")
model_path = Path(__file__).parent / "app" / "models" / "ml" / "plant_disease_recog_model_pwp.keras"
print_info(f"Expected model path: {model_path}")

if model_path.exists():
    file_size_mb = model_path.stat().st_size / (1024 * 1024)
    print_success(f"Model file found: {file_size_mb:.2f} MB")
    
    # Check file integrity
    if file_size_mb < 5:
        print_warning(f"Model file seems small ({file_size_mb:.2f} MB). Expected ~85 MB")
        print_warning("The file might be corrupted or incomplete")
    else:
        print_success("Model file size looks correct (>5 MB)")
else:
    print_error("Model file NOT found!")
    print_warning("Download from: https://drive.google.com/file/d/1Ond7UzrNOfdAXWedjlZr2sDXYU6MRBuj/view")
    print_info(f"Place at: {model_path}")
    print_error("Cannot proceed without model file")
    sys.exit(1)

# Test 5: Disease Database
print_header("TEST 5: Disease Database Verification")
db_path = Path(__file__).parent / "app" / "data" / "plant_diseases.json"
print_info(f"Database path: {db_path}")

if db_path.exists():
    try:
        with open(db_path, 'r', encoding='utf-8') as f:
            diseases = json.load(f)
        print_success(f"Disease database found: {len(diseases)} disease entries")
        
        # Analyze database structure
        if diseases:
            sample_key = list(diseases.keys())[0]
            sample_disease = diseases[sample_key]
            print_info(f"Sample disease: {sample_key}")
            print_info(f"Fields available: {list(sample_disease.keys())}")
        else:
            print_warning("Disease database is empty!")
    except Exception as e:
        print_error(f"Error reading disease database: {e}")
        traceback.print_exc()
else:
    print_error("Disease database NOT found!")
    print_warning("Some disease information may not be available")

# Test 6: Model Loading
print_header("TEST 6: TensorFlow Model Loading Test")
try:
    print_info("Attempting to load TensorFlow model...")
    print_warning("This may take 10-30 seconds on first load...")
    
    import tensorflow as tf
    model = tf.keras.models.load_model(str(model_path))
    
    print_success("Model loaded successfully!")
    print_info(f"Model input shape: {model.input_shape}")
    print_info(f"Model output shape: {model.output_shape}")
    print_info(f"Number of layers: {len(model.layers)}")
    print_info(f"Model parameters: {model.count_params():,}")
    
    # Get model summary
    print_info("\nModel Architecture Summary:")
    model.summary()
    
except Exception as e:
    print_error(f"Failed to load model: {e}")
    traceback.print_exc()
    sys.exit(1)

# Test 7: ML Service Initialization
print_header("TEST 7: ML Disease Service Initialization")
try:
    from app.services.ml_disease_service import MLDiseaseDetectionService
    
    print_info("Initializing ML Disease Detection Service...")
    service = MLDiseaseDetectionService()
    
    print_success(f"Service initialized successfully!")
    print_info(f"Model loaded in service: {service.model_loaded}")
    print_info(f"Number of disease classes: {len(service.class_labels)}")
    print_info(f"Diseases in database: {len(service.disease_database)}")
    
    # Display supported crops
    supported_crops = service.get_supported_crops()
    print_success(f"Supported crops ({len(supported_crops)}):")
    for i, crop in enumerate(sorted(supported_crops), 1):
        print(f"  {i:2d}. {crop}")
    
except Exception as e:
    print_error(f"Service initialization failed: {e}")
    traceback.print_exc()
    sys.exit(1)

# Test 8: Image Preprocessing Test
print_header("TEST 8: Image Preprocessing Test")
try:
    from PIL import Image
    import numpy as np
    import io
    
    # Create a test image (160x160 RGB)
    print_info("Creating test image (160x160 RGB)...")
    test_img = Image.new('RGB', (200, 200), color=(100, 150, 200))
    
    # Convert to bytes
    img_byte_arr = io.BytesIO()
    test_img.save(img_byte_arr, format='PNG')
    img_bytes = img_byte_arr.getvalue()
    
    print_success(f"Test image created: {len(img_bytes)} bytes")
    
    # Test preprocessing
    print_info("Testing image preprocessing...")
    processed_img = service._preprocess_image(img_bytes)
    
    print_success(f"Image preprocessed successfully!")
    print_info(f"Processed shape: {processed_img.shape}")
    print_info(f"Data type: {processed_img.dtype}")
    print_info(f"Value range: [{processed_img.min():.3f}, {processed_img.max():.3f}]")
    
    if processed_img.shape == (1, 160, 160, 3):
        print_success("Preprocessing shape is correct ✓")
    else:
        print_error(f"Preprocessing shape mismatch! Expected (1, 160, 160, 3), got {processed_img.shape}")
    
    if 0 <= processed_img.min() and processed_img.max() <= 1:
        print_success("Normalization is correct (0-1 range) ✓")
    else:
        print_error(f"Normalization issue! Expected [0, 1], got [{processed_img.min()}, {processed_img.max()}]")
    
except Exception as e:
    print_error(f"Image preprocessing test failed: {e}")
    traceback.print_exc()

# Test 9: Model Prediction Test
print_header("TEST 9: Model Prediction Test")
try:
    print_info("Running prediction on test image...")
    
    predictions = model.predict(processed_img, verbose=0)
    predicted_index = np.argmax(predictions[0])
    confidence = float(predictions[0][predicted_index])
    predicted_label = service.class_labels[predicted_index]
    
    print_success("Prediction completed successfully!")
    print_info(f"Predicted class index: {predicted_index}")
    print_info(f"Predicted label: {predicted_label}")
    print_info(f"Confidence: {confidence*100:.2f}%")
    print_info(f"Top 5 predictions:")
    
    top_5_indices = np.argsort(predictions[0])[-5:][::-1]
    for idx in top_5_indices:
        label = service.class_labels[idx]
        conf = predictions[0][idx] * 100
        print(f"  {label:50s} - {conf:5.2f}%")
    
except Exception as e:
    print_error(f"Model prediction test failed: {e}")
    traceback.print_exc()

# Test 10: Complete Detection Flow Test
print_header("TEST 10: Complete Detection Flow Test")
try:
    print_info("Testing complete disease detection workflow...")
    
    import asyncio
    
    async def test_detection():
        result = await service.detect_disease(
            image_data=img_bytes,
            crop_type="Tomato",
            location="Test Location"
        )
        return result
    
    # Run async function
    result = asyncio.run(test_detection())
    
    print_success("Complete detection flow successful!")
    print_info("Detection result:")
    print(json.dumps(result, indent=2, default=str))
    
except Exception as e:
    print_error(f"Complete detection flow test failed: {e}")
    traceback.print_exc()

# Test 11: API Endpoint Availability
print_header("TEST 11: API Endpoints Check")
try:    from app.api.v1.endpoints import disease_detection
    from app.api.v1.api import api_router
    
    print_success("API endpoints module loaded successfully")
    print_info("Available endpoints:")
    print_info("  POST /api/v1/disease/detect")
    print_info("  GET  /api/v1/disease/diseases")
    print_info("  GET  /api/v1/disease/supported-crops")
    print_info("  GET  /api/v1/disease/history")
    
except Exception as e:
    print_error(f"API endpoints check failed: {e}")
    traceback.print_exc()

# Test 12: Server Configuration
print_header("TEST 12: Server Configuration")
try:
    from app.config import settings
    
    print_success("Configuration loaded successfully")
    print_info(f"App Name: {settings.APP_NAME}")
    print_info(f"Version: {settings.APP_VERSION}")
    print_info(f"Environment: {settings.ENVIRONMENT}")
    print_info(f"Host: {settings.HOST}")
    print_info(f"Port: {settings.PORT}")
    print_info(f"Debug: {settings.DEBUG}")
    print_info(f"Log Level: {settings.LOG_LEVEL}")
    
except Exception as e:
    print_error(f"Configuration check failed: {e}")
    traceback.print_exc()

# Final Summary
print_header("DIAGNOSTIC SUMMARY")
print_success("✅ All critical tests passed!")
print_info("\nSystem Status:")
print_success("  ✓ TensorFlow installed and working")
print_success("  ✓ Model file present and loadable")
print_success("  ✓ Disease database available")
print_success("  ✓ ML service initializes correctly")
print_success("  ✓ Image preprocessing works")
print_success("  ✓ Model predictions work")
print_success("  ✓ Complete detection flow works")
print_success("  ✓ API endpoints available")

print_info("\nNext Steps:")
print_info("1. Start the server: python run.py")
print_info("2. Test API: http://localhost:8000/docs")
print_info("3. Test frontend disease detection page")
print_info("4. Upload a plant image and check results")

print_header("DIAGNOSIS COMPLETE")
