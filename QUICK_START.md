# ⚡ Quick Reference - Testing Your New Backend

## 🚀 Start Server (3 Steps)

```powershell
# 1. Navigate to server
cd c:\Users\Aman\Desktop\ibm\fasal-mitra\server

# 2. Activate virtual environment (use existing one)
& c:\Users\Aman\Desktop\ibm\.venv\Scripts\Activate.ps1

# 3. Start server
python run.py
```

**Server will run at**: http://localhost:8000

---

## 🧪 Test APIs (Choose One Method)

### Method 1: Swagger UI (Easiest) ⭐
1. Open browser: http://localhost:8000/docs
2. Click on any endpoint (e.g., "GET /api/v1/health")
3. Click "Try it out"
4. Click "Execute"
5. See response below

### Method 2: Test Script
```powershell
# While server is running, in a new terminal:
cd c:\Users\Aman\Desktop\ibm\fasal-mitra\server
python test_api.py
```

### Method 3: cURL Commands
```powershell
# Health check
curl http://localhost:8000/api/v1/health

# System info
curl http://localhost:8000/api/v1/info

# Predict yield
curl -X POST http://localhost:8000/api/v1/yield/predict `
  -H "Content-Type: application/json" `
  -d '{\"crop\":\"Rice\",\"state\":\"Punjab\",\"season\":\"Kharif\",\"area\":100,\"fertilizer\":25000,\"pesticide\":500}'
```

---

## 📋 Must-Try Endpoints

### 1. Health Check ✅
**URL**: http://localhost:8000/api/v1/health  
**Method**: GET  
**Expected**: `{"status": "healthy", ...}`

### 2. System Info 📊
**URL**: http://localhost:8000/api/v1/info  
**Method**: GET  
**Expected**: Full system information with dataset stats

### 3. Predict Yield 🌾
**URL**: http://localhost:8000/api/v1/yield/predict  
**Method**: POST  
**Body**:
```json
{
  "crop": "Rice",
  "state": "Punjab",
  "season": "Kharif",
  "area": 100,
  "fertilizer": 25000,
  "pesticide": 500
}
```
**Expected**: Yield prediction with confidence interval

### 4. Current Weather 🌦️
**URL**: http://localhost:8000/api/v1/weather/current  
**Method**: POST  
**Body**:
```json
{
  "latitude": 28.6139,
  "longitude": 77.2090
}
```
**Expected**: Current weather for New Delhi

### 5. Ask Chatbot 🤖
**URL**: http://localhost:8000/api/v1/chatbot/query  
**Method**: POST  
**Body**:
```json
{
  "question": "What is the best fertilizer for wheat?",
  "language": "en"
}
```
**Expected**: AI-generated answer

---

## 🎯 What to Look For

### ✅ Success Indicators
- Server starts without errors
- Health endpoint returns 200 status
- Info endpoint shows your dataset counts
- Yield prediction returns a number
- Weather API returns temperature data
- Chatbot status shows "operational"

### ❌ Common Issues

**Server won't start:**
- Check if data files exist in `../data/raw/`
- Install dependencies: `pip install -r requirements.txt`

**Import errors:**
- Activate virtual environment first
- Check Python version (3.9+)

**API errors:**
- Check logs in `server/logs/app.log`
- Verify `.env` file exists

---

## 📊 Expected Test Results

When you run `python test_api.py`:

```
🌾🌾🌾🌾🌾🌾🌾🌾🌾🌾🌾🌾🌾🌾🌾
          FasalMitra API Test Suite
🌾🌾🌾🌾🌾🌾🌾🌾🌾🌾🌾🌾🌾🌾🌾

Testing Health Endpoint       ✅ PASS
Testing System Info            ✅ PASS
Testing Yield Prediction       ✅ PASS
Testing Yield Benchmarks       ✅ PASS
Testing Weather Service        ✅ PASS
Testing Soil Data              ✅ PASS
Testing Soil Suitability       ✅ PASS
Testing Chatbot Status         ✅ PASS
Testing Chatbot Query          ✅ PASS

Results: 9/9 tests passed
🎉 All tests passed! Backend is working correctly.
```

---

## 📖 Documentation Links

- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Server README**: `fasal-mitra/server/README.md`
- **Backend Guide**: `fasal-mitra/BACKEND_COMPLETE.md`
- **Migration Plan**: `REACT_FASTAPI_MIGRATION_PLAN.md`

---

## 🎓 Next Steps After Testing

### If Everything Works ✅
1. You can proceed to React frontend development
2. Or make any backend adjustments you need
3. Or deploy the backend independently

### If Issues Found ❌
1. Check the error messages
2. Review logs in `server/logs/app.log`
3. Consult documentation
4. Ask for help with specific error

---

## 💡 Pro Tips

1. **Use Swagger UI** - It's the easiest way to test
2. **Check logs** - All errors are logged to `server/logs/app.log`
3. **Test incrementally** - Start with simple endpoints (health, info)
4. **Keep server running** - Use separate terminals for testing
5. **Read responses** - All errors include helpful messages

---

**Ready to test? Start the server and open http://localhost:8000/docs!** 🚀
