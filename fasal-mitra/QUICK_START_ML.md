# 🚀 Quick Start - Disease Detection ML

## Fast Track to Get ML Disease Detection Running

### Prerequisites Check
```bash
✅ Python 3.8+
✅ pip installed
✅ Internet connection (for model download)
✅ ~500MB free disk space
```

---

## ⚡ 3-Minute Setup

### 1. Download Model (2 minutes)
```bash
# Open link in browser
https://drive.google.com/file/d/1Ond7UzrNOfdAXWedjlZr2sDXYU6MRBuj/view

# Click Download
# Wait for download to complete (~80MB)
```

### 2. Place Model File
```bash
# Copy downloaded file to:
fasal-mitra/server/app/models/ml/plant_disease_recog_model_pwp.keras

# Verify:
cd fasal-mitra/server
ls app/models/ml/
# Should show: plant_disease_recog_model_pwp.keras README.md
```

### 3. Install Dependencies (1 minute)
```bash
cd fasal-mitra/server
pip install tensorflow>=2.15.0

# Or faster CPU-only version:
pip install tensorflow-cpu>=2.15.0
```

### 4. Verify Setup (30 seconds)
```bash
python test_ml_integration.py

# Should show:
# ✅ PASS - Imports
# ✅ PASS - Disease Database
# ✅ PASS - Model Path
# ✅ PASS - API Endpoints
# ✅ PASS - Service Initialization
# Results: 5/5 tests passed
```

### 5. Start Server (10 seconds)
```bash
uvicorn app.main:app --reload --port 8000

# Wait for:
# INFO: ML model loaded successfully ✅
# INFO: Uvicorn running on http://127.0.0.1:8000
```

---

## 🎯 Quick Test

### Browser Test
1. Open: http://localhost:8000/docs
2. Find: `POST /api/v1/disease/detect`
3. Click "Try it out"
4. Upload a plant leaf image
5. Enter crop type (e.g., "Tomato")
6. Click "Execute"
7. See ML prediction! 🎉

### Frontend Test
1. Ensure server is running (step 5 above)
2. Start React frontend:
   ```bash
   cd fasal-mitra/client
   npm run dev
   ```
3. Open: http://localhost:5173
4. Navigate to: Disease Detection
5. Upload plant image
6. Get instant ML-based diagnosis! ✅

---

## 🔍 Supported Crops

Upload images of these crops for best results:

- 🍎 Apple
- 🌽 Corn  
- 🍇 Grape
- 🍅 Tomato (9 diseases!)
- 🥔 Potato
- 🍑 Peach
- 🌶️ Pepper
- 🍊 Orange
- 🍓 Strawberry
- 🫐 Blueberry
- And 4 more...

**Total: 14 crop types, 39 disease classes**

---

## ✅ Success Indicators

You're good to go when you see:

1. ✅ Server logs: "ML model loaded successfully"
2. ✅ Test script: "5/5 tests passed"
3. ✅ API docs at `/docs` accessible
4. ✅ Upload image → Get prediction with 80-95% confidence
5. ✅ Treatment recommendations shown

---

## ❌ Common Issues

### Issue: "Model file not found"
**Fix**: Re-download model, ensure filename is exactly `plant_disease_recog_model_pwp.keras`

### Issue: "TensorFlow not installed"
**Fix**: `pip install tensorflow>=2.15.0`

### Issue: "Server won't start"
**Fix**: Check logs, ensure port 8000 is free, try `--port 8001`

### Issue: "Predictions are wrong"
**Fix**: Ensure image is clear, well-lit, and shows affected leaf area

---

## 📞 Need Help?

Check detailed docs:
- `ML_INTEGRATION_SUMMARY.md` - Complete overview
- `DISEASE_DETECTION_ML_INTEGRATION.md` - In-depth guide
- `server/app/models/ml/README.md` - Model setup

---

**Time Investment**: 3 minutes setup → Unlimited ML-powered disease detection! 🌾

*Happy Farming!* 🚜
