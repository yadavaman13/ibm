@echo off
cls
echo ===================================================================
echo             DISEASE DETECTION - QUICK FIX
echo ===================================================================
echo.
echo This will install TensorFlow and fix the disease detection feature.
echo Estimated time: 10-15 minutes
echo.
pause

cd /d "%~dp0"

echo.
echo [1/3] Activating virtual environment...
call C:\Users\Aman\Desktop\ibm\.venv\Scripts\activate.bat

echo.
echo [2/3] Installing TensorFlow (this may take 5-10 minutes)...
echo Please wait...
pip install --upgrade tensorflow>=2.15.0

echo.
echo [3/3] Verifying installation...
python -c "import tensorflow as tf; print('✅ TensorFlow version:', tf.__version__)"

echo.
echo ===================================================================
echo                     FIX COMPLETE!
echo ===================================================================
echo.
echo Next steps:
echo 1. Start the server: python run.py
echo 2. Keep the server running
echo 3. Test the disease detection feature
echo.
echo Press any key to exit...
pause > nul
