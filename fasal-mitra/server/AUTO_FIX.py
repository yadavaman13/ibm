"""
================================================================================
        DISEASE DETECTION SYSTEM - AUTO-FIX SCRIPT
================================================================================
This script will automatically diagnose and fix all issues with the
disease detection feature.

ROOT CAUSE IDENTIFIED: TensorFlow is NOT installed
Evidence: Server logs show "No module named 'tensorflow'"

This script will:
1. Install TensorFlow and dependencies
2. Verify model file integrity
3. Test ML service initialization
4. Provide next steps to start the server
================================================================================
"""

import subprocess
import sys
from pathlib import Path
import json
import time

class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    print(f"\n{Bcolors.HEADER}{Bcolors.BOLD}{'='*80}{Bcolors.ENDC}")
    print(f"{Bcolors.HEADER}{Bcolors.BOLD} {text}{Bcolors.ENDC}")
    print(f"{Bcolors.HEADER}{Bcolors.BOLD}{'='*80}{Bcolors.ENDC}\n")

def print_step(step_num, total_steps, description):
    print(f"\n{Bcolors.OKCYAN}{Bcolors.BOLD}[Step {step_num}/{total_steps}] {description}{Bcolors.ENDC}")
    print(f"{Bcolors.OKCYAN}{'-'*80}{Bcolors.ENDC}")

def print_success(text):
    print(f"{Bcolors.OKGREEN}✅ {text}{Bcolors.ENDC}")

def print_error(text):
    print(f"{Bcolors.FAIL}❌ {text}{Bcolors.ENDC}")

def print_warning(text):
    print(f"{Bcolors.WARNING}⚠️  {text}{Bcolors.ENDC}")

def print_info(text):
    print(f"   {text}")

def run_command(command, description):
    """Run a command and return success status"""
    print_info(f"Running: {description}")
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout
        )
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
    except subprocess.TimeoutExpired:
        return False, "Command timed out"
    except Exception as e:
        return False, str(e)

# Main execution
print_header("DISEASE DETECTION AUTO-FIX SCRIPT")
print_info("This script will fix all issues with the disease detection feature")
print_info("Estimated time: 10-15 minutes")
print_info("")
input(f"{Bcolors.WARNING}Press ENTER to start the auto-fix process...{Bcolors.ENDC}")

TOTAL_STEPS = 8

# Step 1: Check Python Environment
print_step(1, TOTAL_STEPS, "Checking Python Environment")
print_info(f"Python: {sys.version}")
print_info(f"Executable: {sys.executable}")
print_success("Python environment OK")

# Step 2: Check Current Package Status
print_step(2, TOTAL_STEPS, "Checking Current Packages")
success, output = run_command("pip list", "List installed packages")
if "tensorflow" in output.lower():
    print_warning("TensorFlow appears to be installed, but may not be working correctly")
    print_info("Will attempt to reinstall...")
else:
    print_warning("TensorFlow NOT installed (this is the root cause)")

# Step 3: Install/Upgrade TensorFlow
print_step(3, TOTAL_STEPS, "Installing TensorFlow")
print_warning("This will download ~500MB and may take 5-10 minutes...")
print_info("Please wait...")

success, output = run_command(
    "pip install --upgrade tensorflow>=2.15.0",
    "Install TensorFlow"
)

if success:
    print_success("Tensor Flow installed successfully!")
else:
    print_error(f"TensorFlow installation failed: {output}")
    print_info("Trying alternative installation method...")
    
    success, output = run_command(
        "pip install tensorflow==2.15.0",
        "Install TensorFlow (specific version)"
    )
    
    if success:
        print_success("TensorFlow installed successfully (alternative method)!")
    else:
        print_error("Installation failed. Please install manually:")
        print_info("  pip install tensorflow>=2.15.0")
        sys.exit(1)

# Step 4: Verify TensorFlow Installation
print_step(4, TOTAL_STEPS, "Verifying TensorFlow Installation")
try:
    import tensorflow as tf
    print_success(f"TensorFlow version: {tf.__version__}")
    print_info(f"Location: {tf.__file__}")
except ImportError as e:
    print_error(f"TensorFlow import failed: {e}")
    print_warning("Please restart your terminal and try again")
    sys.exit(1)

# Step 5: Verify Dependencies
print_step(5, TOTAL_STEPS, "Verifying Dependencies")
dependencies = ["numpy", "PIL", "pathlib"]
all_ok = True

for dep_name in dependencies:
    try:
        if dep_name == "PIL":
            from PIL import Image
            import PIL
            version = PIL.__version__
        elif dep_name == "numpy":
            import numpy as np
            version = np.__version__
        else:
            __import__(dep_name)
            version = "OK"
        print_success(f"{dep_name}: {version}")
    except ImportError:
        print_error(f"{dep_name} NOT installed")
        all_ok = False

if not all_ok:
    print_warning("Installing missing dependencies...")
    run_command("pip install pillow numpy", "Install dependencies")

# Step 6: Check Model File
print_step(6, TOTAL_STEPS, "Checking Model File")
model_path = Path("app/models/ml/plant_disease_recog_model_pwp.keras")

if model_path.exists():
    size_mb = model_path.stat().st_size / (1024 * 1024)
    print_success(f"Model file found: {size_mb:.2f} MB")
    
    if size_mb < 10:
        print_warning(f"Model file seems small ({size_mb:.2f} MB)")
        print_warning("Expected size: ~85 MB")
        print_error("The file might be corrupted or incomplete!")
        print_info("Please download it again from:")
        print_info("https://drive.google.com/file/d/1Ond7UzrNOfdAXWedjlZr2sDXYU6MRBuj/view")
    else:
        print_success("Model file size looks correct")
else:
    print_error("Model file NOT found!")
    print_info(f"Expected location: {model_path.absolute()}")
    print_warning("Download from: https://drive.google.com/file/d/1Ond7UzrNOfdAXWedjlZr2sDXYU6MRBuj/view")
    print_error("Cannot proceed without model file")
    sys.exit(1)

# Step 7: Test ML Service Initialization
print_step(7, TOTAL_STEPS, "Testing ML Service Initialization")
try:
    print_info("Importing ML service...")
    from app.services.ml_disease_service import MLDiseaseDetectionService
    
    print_info("Initializing service... (may take 10-30 seconds)")
    service = MLDiseaseDetectionService()
    
    if service.model_loaded:
        print_success("ML Service initialized successfully!")
        print_success(f"Model loaded: {service.model_loaded}")
        print_info(f"Disease classes: {len(service.class_labels)}")
        print_info(f"Disease database entries: {len(service.disease_database)}")
        
        # Show supported crops
        crops = service.get_supported_crops()
        print_success(f"Supported crops: {len(crops)}")
        print_info(f"  {', '.join(sorted(crops)[:5])}... (and {len(crops)-5} more)")
    else:
        print_error("ML Service initialized but model NOT loaded!")
        print_warning("Check previous errors")
        sys.exit(1)
        
except Exception as e:
    print_error(f"ML Service initialization failed: {e}")
    import traceback
    print_info(traceback.format_exc())
    sys.exit(1)

# Step 8: Final Verification
print_step(8, TOTAL_STEPS, "Final System Verification")

checks = [
    ("TensorFlow installed", True),
    ("Model file exists", model_path.exists()),
    ("ML Service working", service.model_loaded if 'service' in locals() else False),
]

all_passed = all(status for _, status in checks)

for check_name, status in checks:
    if status:
        print_success(check_name)
    else:
        print_error(check_name)

# Summary and Next Steps
print_header("AUTO-FIX COMPLETE!")

if all_passed:
    print_success("✅ All checks passed! System is ready to use.")
    print("")
    print(f"{Bcolors.OKGREEN}{Bcolors.BOLD}NEXT STEPS:{Bcolors.ENDC}")
    print(f"{Bcolors.OKBLUE}1. Start the backend server:{Bcolors.ENDC}")
    print(f"   {Bcolors.BOLD}python run.py{Bcolors.ENDC}")
    print("")
    print(f"{Bcolors.OKBLUE}2. Keep the server running (don't close the terminal){Bcolors.ENDC}")
    print("")
    print(f"{Bcolors.OKBLUE}3. Open your browser and test:{Bcolors.ENDC}")
    print(f"   - API Docs: {Bcolors.UNDERLINE}http://localhost:8000/docs{Bcolors.ENDC}")
    print(f"   - Disease Detection: Upload a plant image")
    print("")
    print(f"{Bcolors.OKBLUE}4. Expected behavior:{Bcolors.ENDC}")
    print(f"   - Upload image → Click 'Analyze' → Results in 2-5 seconds")
    print(f"   - Shows disease name, confidence, treatment, recommendations")
    print("")
    print(f"{Bcolors.WARNING}Need help? Check the logs:{Bcolors.ENDC}")
    print(f"   logs/app.log")
    print("")
else:
    print_error("Some checks failed. Please review errors above.")
    print_warning("Common fixes:")
    print_info("1. Restart your terminal/PowerShell")
    print_info("2. Reactivate virtual environment")
    print_info("3. Run this script again")

print_header("END OF AUTO-FIX")
