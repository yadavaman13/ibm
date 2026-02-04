# 🌾 FasalMitra - FastAPI Backend

AI-powered Smart Farming Assistant API built with FastAPI.

## 📋 Features

- ✅ **Crop Disease Detection** - AI-powered disease identification from images
- ✅ **Yield Prediction** - ML-based crop yield forecasting
- ✅ **Yield Gap Analysis** - Benchmarking against top performers
- ✅ **Multi-Scenario Analysis** - What-if predictions (coming soon)
- ✅ **Weather Forecast** - 7-day weather predictions with farming recommendations
- ✅ **Soil Analysis** - Soil suitability check and crop recommendations
- ✅ **AI Chatbot** - Farming assistant using Google Gemini AI
- ✅ **Multilingual Support** - Support for multiple languages

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- pip
- Virtual environment (recommended)

### Installation

1. **Create virtual environment**
   ```bash
   cd fasal-mitra/server
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup environment variables**
   ```bash
   # Copy example env file
   copy .env.example .env
   
   # Edit .env and add your API keys
   # GEMINI_API_KEY=your_key_here
   ```

4. **Run the server**
   ```bash
   # Development mode (auto-reload)
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   
   # Or use Python directly
   python -m app.main
   ```

5. **Access the API**
   - API: http://localhost:8000
   - Interactive Docs: http://localhost:8000/docs
   - Alternative Docs: http://localhost:8000/redoc

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api/v1
```

### Main Endpoints

#### Health & Info
- `GET /api/v1/health` - Health check
- `GET /api/v1/info` - System information
- `GET /api/v1/stats` - Dataset statistics

#### Disease Detection
- `POST /api/v1/disease/detect` - Detect disease from image
- `GET /api/v1/disease/diseases` - List all diseases
- `GET /api/v1/disease/history` - Detection history

#### Yield Prediction
- `POST /api/v1/yield/predict` - Predict crop yield
- `POST /api/v1/yield/gap-analysis` - Analyze yield gap
- `POST /api/v1/yield/benchmarks` - Get benchmarks
- `GET /api/v1/yield/crops` - Available crops
- `GET /api/v1/yield/states` - Available states
- `GET /api/v1/yield/seasons` - Available seasons

#### Weather
- `POST /api/v1/weather/current` - Current weather
- `POST /api/v1/weather/forecast` - Weather forecast
- `GET /api/v1/weather/location/{lat}/{lon}` - Location name

#### Soil Analysis
- `GET /api/v1/soil/data/{state}` - Soil data for state
- `POST /api/v1/soil/suitability` - Check soil suitability
- `GET /api/v1/soil/recommendations/{state}` - Crop recommendations
- `GET /api/v1/soil/states` - Available states

#### Chatbot
- `POST /api/v1/chatbot/query` - Ask question
- `POST /api/v1/chatbot/explain` - Explain term
- `GET /api/v1/chatbot/conversation/{id}` - Get conversation
- `GET /api/v1/chatbot/status` - Chatbot status

## 🧪 Testing the API

### Using cURL

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Get system info
curl http://localhost:8000/api/v1/info

# Predict yield
curl -X POST http://localhost:8000/api/v1/yield/predict \
  -H "Content-Type: application/json" \
  -d '{
    "crop": "Rice",
    "state": "Punjab",
    "season": "Kharif",
    "area": 100,
    "fertilizer": 25000,
    "pesticide": 500
  }'

# Get current weather
curl -X POST http://localhost:8000/api/v1/weather/current \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 28.6139,
    "longitude": 77.2090
  }'
```

### Using Python

```python
import requests

# Health check
response = requests.get("http://localhost:8000/api/v1/health")
print(response.json())

# Predict yield
data = {
    "crop": "Wheat",
    "state": "Punjab",
    "season": "Rabi",
    "area": 50,
    "fertilizer": 20000,
    "pesticide": 300
}
response = requests.post("http://localhost:8000/api/v1/yield/predict", json=data)
print(response.json())
```

## 📁 Project Structure

```
server/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/         # API endpoints
│   │       └── api.py             # Router aggregator
│   ├── core/
│   │   └── data_loader.py         # Data loading
│   ├── services/                  # Business logic
│   │   ├── disease_service.py
│   │   ├── yield_service.py
│   │   ├── weather_service.py
│   │   ├── soil_service.py
│   │   └── chatbot_service.py
│   ├── models/                    # Pydantic models
│   ├── middleware/                # Custom middleware
│   ├── utils/                     # Utilities
│   ├── config.py                  # Configuration
│   └── main.py                    # FastAPI app
├── tests/                         # Tests
├── requirements.txt
├── .env.example
└── README.md
```

## 🔧 Configuration

Edit `.env` file:

```env
# API Keys
GEMINI_API_KEY=your_gemini_api_key

# CORS (for React frontend)
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

## 🐳 Docker Deployment

```bash
# Build image
docker build -t fasalmitra-api .

# Run container
docker run -p 8000:8000 \
  -e GEMINI_API_KEY=your_key \
  -v $(pwd)/../data:/app/data \
  fasalmitra-api
```

## 📊 Data Requirements

The API expects data files in the following structure:

```
../data/
├── raw/
│   ├── crop_yield.csv
│   ├── state_soil_data.csv
│   ├── state_weather_data_1997_2020.csv
│   └── Price_Agriculture_commodities_Week.csv
```

## 🧪 Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest tests/

# With coverage
pytest --cov=app tests/
```

## 📝 API Response Format

All endpoints return a standard response format:

```json
{
  "success": true,
  "message": "Success message",
  "data": { ... },
  "timestamp": "2026-02-04T10:30:00"
}
```

Error responses:

```json
{
  "error": true,
  "message": "Error description",
  "details": { ... },
  "status_code": 400
}
```

## 🔐 Security

- CORS enabled for specified origins
- Input validation using Pydantic
- File upload size limits
- Rate limiting (coming soon)
- Authentication (coming soon with JWT)

## 📈 Performance

- Singleton pattern for services
- Data caching with `@lru_cache`
- Async endpoints where applicable
- Model pre-loading on startup

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Write tests
5. Submit pull request

## 📄 License

MIT License

## 🆘 Troubleshooting

### Data not found error
- Ensure data files are in `../data/raw/` directory
- Check file paths in logs

### Gemini API not working
- Verify `GEMINI_API_KEY` in `.env`
- Check internet connection
- API has fallback mode if key is missing

### Port already in use
- Change port in `.env` or command line:
  ```bash
  uvicorn app.main:app --port 8001
  ```

## 📞 Support

For issues and questions:
- Check API documentation: http://localhost:8000/docs
- Review logs in `logs/app.log`
- Create an issue on GitHub

---

**Status**: ✅ Backend Ready for Testing
**Next Steps**: Test APIs → Build React Frontend → Integration
