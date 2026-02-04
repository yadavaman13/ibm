# FasalMitra API Documentation for Frontend Developers

**Version:** 1.0.0  
**Base URL:** `http://localhost:8000/api/v1`  
**Documentation:** http://localhost:8000/docs (Swagger UI)

---

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Response Format](#response-format)
4. [Error Handling](#error-handling)
5. [API Endpoints](#api-endpoints)
   - [Health & System Info](#health--system-info)
   - [Yield Prediction](#yield-prediction)
   - [Weather Services](#weather-services)
   - [Soil Analysis](#soil-analysis)
   - [Disease Detection](#disease-detection)
   - [AI Chatbot](#ai-chatbot)
6. [Data Models](#data-models)
7. [Usage Examples](#usage-examples)

---

## Overview

FasalMitra Smart Farming Assistant API provides AI-powered agricultural advisory services including:

- 🌾 **Yield Prediction** - ML-based crop yield forecasting (97.5% accuracy)
- 📊 **Gap Analysis** - Compare yields with benchmarks (pre/post-harvest scenarios)
- 🌤️ **Weather Forecasting** - Real-time weather with farming recommendations
- 🧪 **Soil Analysis** - NPK levels, pH, and crop suitability
- 🦠 **Disease Detection** - AI image-based crop disease identification
- 💬 **AI Chatbot** - Google Gemini powered farming assistant

**Tech Stack:**
- Backend: FastAPI + Python 3.13
- ML: Scikit-learn Random Forest Regressor
- AI: Google Generative AI (Gemini)
- External APIs: Open-Meteo (weather)

---

## Authentication

Currently **no authentication required**. All endpoints are open.

> ⚠️ **Production Note:** Implement JWT/API key authentication before deploying to production.

---

## Response Format

All API responses follow a **standard envelope format**:

### Success Response

```json
{
  "success": true,
  "message": "Operation successful",
  "data": { /* actual response data */ },
  "timestamp": "2024-01-15T10:30:00"
}
```

### Error Response

```json
{
  "success": false,
  "message": "Error description",
  "data": null,
  "timestamp": "2024-01-15T10:30:00"
}
```

**OR** (FastAPI default error format):

```json
{
  "detail": "Error message"
}
```

---

## Error Handling

| Status Code | Meaning |
|-------------|---------|
| `200` | Success |
| `400` | Bad Request - Invalid input |
| `404` | Not Found - Resource doesn't exist |
| `422` | Validation Error - Pydantic validation failed |
| `500` | Internal Server Error |

### Validation Error Format (422)

```json
{
  "detail": [
    {
      "loc": ["body", "crop"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## API Endpoints

### Health & System Info

#### 1. Health Check

**GET** `/health`

Check if API is running.

**Response:**
```json
{
  "status": "healthy",
  "environment": "development",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:30:00"
}
```

---

#### 2. System Information

**GET** `/info`

Get complete system info, available datasets, and feature status.

**Response:**
```json
{
  "success": true,
  "message": "System information retrieved",
  "data": {
    "app_name": "FasalMitra - Smart Farming Assistant API",
    "version": "1.0.0",
    "environment": "development",
    "python_version": "3.13.5",
    "datasets": {
      "records": {
        "crop_data": 19689,
        "soil_data": 30,
        "weather_data": 720,
        "price_data": 23093
      },
      "available_crops": ["Rice", "Wheat", "Cotton", "Sugarcane", ...],  // 55 crops
      "available_states": ["Andhra Pradesh", "Punjab", ...],  // 30 states
      "available_seasons": ["Kharif", "Rabi", "Summer", "Whole Year", "Autumn", "Winter"]
    },
    "features": {
      "disease_detection": true,
      "yield_prediction": true,
      "yield_gap_analysis": true,
      "multi_scenario": true,
      "weather_forecast": true,
      "soil_analysis": true,
      "chatbot": true,  // false if GEMINI_API_KEY not configured
      "translation": true
    }
  }
}
```

**Frontend Usage:**
- Display available crops in dropdowns
- Show available states for filtering
- Check if chatbot is operational
- Display dataset statistics

---

#### 3. Statistics

**GET** `/stats`

Get dataset statistics summary.

**Response:**
```json
{
  "success": true,
  "message": "Statistics retrieved",
  "data": {
    "total_records": {
      "crop_data": 19689,
      "soil_data": 30,
      "weather_data": 720,
      "price_data": 23093
    },
    "available_crops": 55,
    "available_states": 30,
    "available_seasons": 6,
    "crops_list": ["Rice", "Wheat", "Cotton", ...],  // First 10
    "states_list": ["Andhra Pradesh", "Punjab", ...],  // First 10
    "seasons_list": ["Kharif", "Rabi", "Summer", "Whole Year", "Autumn", "Winter"]
  }
}
```

---

### Yield Prediction

#### 4. Predict Yield

**POST** `/yield/predict`

Predict crop yield based on farming inputs using ML model (97.5% accuracy).

**Request Body:**
```json
{
  "crop": "Rice",
  "state": "Punjab",
  "season": "Kharif",
  "area": 100.0,
  "fertilizer": 25000.0,
  "pesticide": 500.0,
  
  // Optional weather parameters
  "avg_temp_c": 28.5,
  "total_rainfall_mm": 850.0,
  "avg_humidity_percent": 75.0
}
```

**Field Constraints:**
- `crop`: String (must be in available crops list)
- `state`: String (must be in available states list)
- `season`: String (Kharif/Rabi/Summer/Whole Year/Autumn/Winter)
- `area`: Float > 0 (hectares)
- `fertilizer`: Float >= 0 (kg/ha)
- `pesticide`: Float >= 0 (kg/ha)

**Response:**
```json
{
  "success": true,
  "message": "Yield predicted successfully",
  "data": {
    "prediction_id": "pred_1705315800_abc123",
    "timestamp": "2024-01-15T10:30:00",
    "input_params": { /* echoed request */ },
    "predicted_yield": 3.45,  // tons/hectare
    "confidence_interval": {
      "lower": 3.12,
      "upper": 3.78
    },
    "factors_affecting": [
      {
        "factor": "fertilizer",
        "impact": "positive",
        "contribution_percent": 35
      },
      {
        "factor": "rainfall",
        "impact": "positive",
        "contribution_percent": 25
      }
    ],
    "recommendations": [
      "Current inputs suggest good yield potential",
      "Consider maintaining fertilizer levels",
      "Monitor soil moisture during critical growth stages"
    ],
    "model_confidence": 0.975
  }
}
```

**Frontend Usage:**
- Create form with crop, state, season dropdowns
- Input fields for area, fertilizer, pesticide
- Display predicted yield prominently
- Show confidence interval as range
- List recommendations as bullet points

---

#### 5. Yield Gap Analysis (Dual Scenario)

**POST** `/yield/gap-analysis`

Compare yield against benchmarks. Supports **two scenarios**:

##### Scenario 1: Post-Harvest Analysis (Actual Yield Known)

Use this **after harvest** when farmer knows the actual yield.

**Request Body:**
```json
{
  "crop": "Wheat",
  "state": "Punjab",
  "season": "Rabi",
  "actual_yield": 2.1  // Farmer's actual harvested yield
}
```

##### Scenario 2: Pre-Harvest Planning (Prediction-Based)

Use this **before/during season** for planning and optimization.

**Request Body:**
```json
{
  "crop": "Wheat",
  "state": "Punjab",
  "season": "Rabi",
  "area": 50,
  "fertilizer": 20000,
  "pesticide": 300
}
```

**Response (Both Scenarios):**
```json
{
  "success": true,
  "message": "Yield gap analysis completed",
  "data": {
    "analysis_type": "post_harvest",  // or "pre_harvest"
    "yield_analyzed": 2.1,
    "current_yield": 2.1,
    "predicted_yield": null,  // For post_harvest
    "actual_yield": 2.1,      // For post_harvest
    "potential_yield": 4.2,   // Top 10% benchmark
    "average_yield": 3.1,
    "gap_percentage": 50.0,   // Gap vs top 10%
    "gap_vs_average": -32.26, // Negative = below average
    "performance_level": "Below Average",
    
    "benchmarks": {
      "average": 3.1,
      "top_25_percent": 3.8,
      "top_10_percent": 4.2,
      "maximum": 4.8
    },
    
    "top_performers": {
      "yield": 4.2,
      "practices": [
        "Optimal fertilizer timing and split application",
        "Integrated pest management",
        "Precision irrigation scheduling",
        "High-quality seed varieties"
      ]
    },
    
    "improvement_steps": [
      "⚠️ Your yield is below regional average",
      "Review fertilizer and pesticide application rates",
      "💡 Consider increasing fertilizer application gradually",
      "💡 Consult with agricultural extension officers",
      "💡 Consider soil testing for precise nutrient management"
    ],
    
    "estimated_increase": 2.1,  // Potential increase in tons/ha
    "yield_potential_percentage": 50.0  // Current as % of top 10%
  }
}
```

**Frontend Usage:**
- Create tab/toggle for "Post-Harvest Analysis" vs "Pre-Harvest Planning"
- Post-harvest form: crop, state, season, actual_yield
- Pre-harvest form: crop, state, season, area, fertilizer, pesticide
- Display gap visualization (gauge/progress bar)
- Show performance level with color coding (red/yellow/green)
- List benchmarks as comparison table
- Display improvement steps as actionable checklist

---

#### 6. Get Benchmarks

**POST** `/yield/benchmarks`

Get statistical benchmarks for a crop in a region.

**Request Body:**
```json
{
  "crop": "Rice",
  "state": "Punjab",
  "season": "Kharif"  // Optional
}
```

**Response:**
```json
{
  "success": true,
  "message": "Benchmarks retrieved successfully",
  "data": {
    "crop": "Rice",
    "state": "Punjab",
    "season": "Kharif",
    "total_records": 1250,
    "years_covered": "1997-2020",
    "average_yield": 3.45,
    "median_yield": 3.38,
    "top_10_percent": 4.82,
    "top_25_percent": 4.21,
    "max_yield_achieved": 5.12,
    "yield_std": 0.87
  }
}
```

---

#### 7. Get Available Crops

**GET** `/yield/crops`

Get list of all crops supported for yield prediction.

**Response:**
```json
{
  "success": true,
  "message": "Found 55 crops",
  "data": {
    "crops": [
      "Rice", "Wheat", "Cotton", "Sugarcane", "Maize", "Bajra",
      "Jowar", "Groundnut", "Sunflower", "Soyabean", ...
    ]
  }
}
```

---

### Weather Services

#### 8. Get Current Weather

**POST** `/weather/current`

Get real-time weather with farming recommendations.

**Request Body:**
```json
{
  "latitude": 30.7333,   // -90 to 90
  "longitude": 76.7794   // -180 to 180
}
```

**Response:**
```json
{
  "success": true,
  "message": "Current weather retrieved",
  "data": {
    "latitude": 30.7333,
    "longitude": 76.7794,
    "location_name": "Chandigarh, Punjab, India",
    "temperature": 28.5,        // °C
    "humidity": 65.0,           // %
    "wind_speed": 12.5,         // km/h
    "precipitation": 0.0,       // mm
    "weather_code": 0,
    "weather_description": "Clear sky",
    "observation_time": "2024-01-15T10:30:00",
    "recommendations": [
      "✅ Good conditions for spraying pesticides",
      "☀️ Ideal for field work",
      "💧 Consider irrigation if soil is dry"
    ]
  }
}
```

**Weather Codes:**
- `0` - Clear sky
- `1-3` - Partly cloudy
- `45, 48` - Fog
- `51-57` - Drizzle
- `61-67` - Rain
- `71-77` - Snow
- `80-82` - Rain showers
- `95-99` - Thunderstorm

**Frontend Usage:**
- Display weather card with icon based on weather_code
- Show temperature, humidity, wind speed
- List recommendations as alerts/tips
- Use geolocation API to get user's coordinates

---

#### 9. Get Weather Forecast

**POST** `/weather/forecast`

Get multi-day weather forecast with farming alerts.

**Request Body:**
```json
{
  "latitude": 30.7333,
  "longitude": 76.7794,
  "days": 7  // 1-16, default: 7
}
```

**Response:**
```json
{
  "success": true,
  "message": "7-day forecast retrieved",
  "data": {
    "latitude": 30.7333,
    "longitude": 76.7794,
    "location_name": "Chandigarh, Punjab, India",
    
    "forecast": [
      {
        "date": "2024-01-15",
        "temp_max": 32.5,
        "temp_min": 18.2,
        "precipitation_sum": 0.0,
        "wind_speed_max": 15.3,
        "weather_code": 1,
        "weather_description": "Partly cloudy"
      },
      {
        "date": "2024-01-16",
        "temp_max": 30.1,
        "temp_min": 17.8,
        "precipitation_sum": 5.2,
        "wind_speed_max": 20.1,
        "weather_code": 61,
        "weather_description": "Light rain"
      }
      // ... 5 more days
    ],
    
    "farming_recommendations": [
      "☀️ Days 1-2: Good for fieldwork",
      "🌧️ Day 2: Rain expected, avoid spraying",
      "💧 Days 3-5: Irrigation may be needed",
      "🌡️ Temperature favorable for current crops"
    ],
    
    "alerts": [
      "⚠️ Heavy rain expected on Day 2",
      "💨 Strong winds on Day 3 - secure equipment"
    ]
  }
}
```

**Frontend Usage:**
- Display forecast as cards/list (7 days)
- Show daily weather icons
- Highlight days with rain/extreme conditions
- Display alerts prominently
- Show farming recommendations as timeline

---

#### 10. Get Location Name

**GET** `/weather/location/{lat}/{lon}`

Reverse geocoding - convert coordinates to location name.

**Example:** `/weather/location/30.7333/76.7794`

**Response:**
```json
{
  "success": true,
  "message": "Location retrieved",
  "data": {
    "latitude": 30.7333,
    "longitude": 76.7794,
    "location_name": "Chandigarh",
    "country": "India",
    "state": "Punjab",
    "district": "Chandigarh"
  }
}
```

---

### Soil Analysis

#### 11. Get Soil Data

**GET** `/soil/data/{state}`

Get soil composition (N, P, K, pH) for a state.

**Example:** `/soil/data/Punjab`

**Response:**
```json
{
  "success": true,
  "message": "Soil data retrieved for Punjab",
  "data": {
    "state": "Punjab",
    "nitrogen_n": 215.5,      // kg/ha
    "phosphorus_p": 45.2,     // kg/ha
    "potassium_k": 185.3,     // kg/ha
    "ph_level": 7.8,
    "organic_carbon": 0.52,   // %
    "soil_type": "Alluvial",
    "data_source": "Indian Soil Survey",
    "last_updated": "2020"
  }
}
```

**Status Codes:**
- `200` - Success
- `404` - State not found

---

#### 12. Check Soil Suitability

**POST** `/soil/suitability`

Check if soil is suitable for a specific crop.

**Query Parameters:**
- `state`: State name (required)
- `crop`: Crop name (required)

**Example:** `/soil/suitability?state=Punjab&crop=Wheat`

**Response:**
```json
{
  "success": true,
  "message": "Suitability analysis completed",
  "data": {
    "state": "Punjab",
    "crop": "Wheat",
    "soil_data": {
      "nitrogen_n": 215.5,
      "phosphorus_p": 45.2,
      "potassium_k": 185.3,
      "ph_level": 7.8
    },
    "crop_requirements": {
      "nitrogen_min": 120,
      "nitrogen_max": 250,
      "phosphorus_min": 30,
      "phosphorus_max": 60,
      "potassium_min": 100,
      "potassium_max": 200,
      "ph_min": 6.5,
      "ph_max": 8.0
    },
    "suitability_score": 0.92,  // 0-1
    "is_suitable": true,
    "assessment": "Highly Suitable",
    "recommendations": [
      "✅ Soil NPK levels are ideal for Wheat",
      "✅ pH is within optimal range",
      "💡 Maintain organic matter through crop rotation",
      "💡 Consider split nitrogen application"
    ],
    "limitations": [],
    "improvements": [
      "Regular soil testing recommended",
      "Add farmyard manure for long-term fertility"
    ]
  }
}
```

**Frontend Usage:**
- Display suitability score as percentage/gauge
- Show NPK comparison chart (actual vs required)
- Color-code assessment (green/yellow/red)
- List recommendations as action items

---

#### 13. Get Crop Recommendations

**GET** `/soil/recommendations/{state}`

Get recommended crops based on soil composition.

**Example:** `/soil/recommendations/Punjab`

**Response:**
```json
{
  "success": true,
  "message": "Crop recommendations generated",
  "data": {
    "state": "Punjab",
    "soil_data": {
      "nitrogen_n": 215.5,
      "phosphorus_p": 45.2,
      "potassium_k": 185.3,
      "ph_level": 7.8
    },
    "recommended_crops": [
      {
        "crop": "Wheat",
        "suitability_score": 0.95,
        "reason": "Optimal NPK and pH for Wheat cultivation",
        "season": "Rabi",
        "expected_yield_range": "3.5-4.5 tons/ha"
      },
      {
        "crop": "Rice",
        "suitability_score": 0.92,
        "reason": "High nitrogen suitable for Rice",
        "season": "Kharif",
        "expected_yield_range": "4.0-5.0 tons/ha"
      },
      {
        "crop": "Cotton",
        "suitability_score": 0.88,
        "reason": "Good potassium levels for Cotton",
        "season": "Kharif",
        "expected_yield_range": "1.5-2.0 tons/ha"
      }
    ],
    "not_recommended": [
      {
        "crop": "Tea",
        "reason": "pH too high (requires acidic soil 4.5-6.0)"
      }
    ]
  }
}
```

**Frontend Usage:**
- Display as ranked list (top recommendations first)
- Show suitability score as stars/percentage
- Group by season (Kharif/Rabi)
- Highlight top 3 recommendations

---

#### 14. Get Available States

**GET** `/soil/states`

Get list of states with soil data.

**Response:**
```json
{
  "success": true,
  "message": "Found 30 states",
  "data": {
    "states": [
      "Andhra Pradesh", "Assam", "Bihar", "Chhattisgarh",
      "Gujarat", "Haryana", "Karnataka", "Kerala", "Maharashtra",
      "Punjab", "Tamil Nadu", "Uttar Pradesh", "West Bengal", ...
    ]
  }
}
```

---

### Disease Detection

#### 15. Detect Disease from Image

**POST** `/disease/detect`

Upload crop image to detect disease using AI.

**Request:** `multipart/form-data`
- `file`: Image file (JPG, PNG, WEBP) - **Required**
- `crop_type`: String (e.g., "Rice") - **Required**
- `location`: String (optional)

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/disease/detect" \
  -F "file=@crop_image.jpg" \
  -F "crop_type=Rice" \
  -F "location=Punjab"
```

**JavaScript Example:**
```javascript
const formData = new FormData();
formData.append('file', imageFile);
formData.append('crop_type', 'Rice');
formData.append('location', 'Punjab');

const response = await fetch('http://localhost:8000/api/v1/disease/detect', {
  method: 'POST',
  body: formData
});
```

**Response:**
```json
{
  "success": true,
  "message": "Disease detected successfully",
  "data": {
    "detection_id": "det_1705315800_xyz789",
    "timestamp": "2024-01-15T10:30:00",
    "crop_type": "Rice",
    "location": "Punjab",
    
    "detected_disease": {
      "disease_id": "rice_blast_001",
      "name": "Rice Blast",
      "confidence": 0.87,
      "severity": "moderate",
      
      "symptoms": [
        "Diamond-shaped lesions on leaves",
        "Gray centers with brown margins",
        "Wilting of young leaves"
      ],
      
      "causes": [
        "Fungal infection (Magnaporthe oryzae)",
        "High humidity and moisture",
        "Dense planting",
        "Excessive nitrogen fertilization"
      ],
      
      "treatments": {
        "organic": {
          "treatments": [
            "Neem oil spray (5ml/liter)",
            "Remove infected plants",
            "Improve field drainage"
          ],
          "cost_estimate": 500
        },
        "chemical": {
          "treatments": [
            "Tricyclazole 75% WP @ 0.6g/liter",
            "Carbendazim 50% WP @ 1g/liter",
            "Apply at 7-10 day intervals"
          ],
          "cost_estimate": 1500
        },
        "biological": {
          "treatments": [
            "Pseudomonas fluorescens spray",
            "Trichoderma viride application"
          ],
          "cost_estimate": 800
        }
      },
      
      "prevention": [
        "Use resistant varieties",
        "Maintain proper plant spacing",
        "Avoid excessive nitrogen fertilizer",
        "Ensure good field drainage",
        "Seed treatment before sowing"
      ],
      
      "crops_affected": ["Rice", "Wheat", "Barley"]
    },
    
    "recommendations": [
      "🚨 Immediate action required - moderate severity",
      "Start with organic treatment (Neem oil)",
      "If no improvement in 7 days, use chemical treatment",
      "Improve drainage in affected area"
    ],
    
    "estimated_severity": "moderate",
    
    "treatment_plan": {
      "treatments": [
        "Immediate: Remove heavily infected plants",
        "Week 1: Apply Neem oil spray",
        "Week 2: Apply chemical fungicide if needed",
        "Ongoing: Monitor new growth"
      ],
      "cost_estimate": 1200
    },
    
    "next_steps": [
      "Take action within 24-48 hours",
      "Document treatment and response",
      "Monitor neighboring plants",
      "Consider preventive measures for next season"
    ]
  }
}
```

**Severity Levels:**
- `mild` - Early stage, easy to control
- `moderate` - Spreading, needs treatment
- `severe` - Advanced, significant crop damage

**Frontend Usage:**
- File upload with preview
- Display disease name with confidence badge
- Show severity with color coding (green/yellow/red)
- Expandable sections: Symptoms, Causes, Treatments, Prevention
- Treatment comparison table (organic vs chemical vs biological)
- Action plan as timeline/checklist

---

#### 16. List Known Diseases

**GET** `/disease/diseases`

Get list of all known diseases (optional filter by crop).

**Query Parameters:**
- `crop_type`: Optional filter (e.g., "Rice")

**Example:** `/disease/diseases?crop_type=Rice`

**Response:**
```json
{
  "success": true,
  "message": "Found 15 diseases",
  "data": [
    {
      "disease_id": "rice_blast_001",
      "name": "Rice Blast",
      "crops_affected": ["Rice"],
      "common_symptoms": ["Diamond-shaped lesions", "Gray centers"],
      "severity_range": "mild to severe"
    },
    {
      "disease_id": "rice_blight_002",
      "name": "Bacterial Leaf Blight",
      "crops_affected": ["Rice"],
      "common_symptoms": ["Yellow to white lesions", "Wilting"],
      "severity_range": "moderate to severe"
    }
    // ... more diseases
  ]
}
```

---

#### 17. Detection History

**GET** `/disease/history?limit=10`

Get recent disease detections (placeholder - requires database).

**Response:**
```json
{
  "success": true,
  "message": "History retrieved",
  "data": {
    "history": [],
    "total": 0,
    "note": "History tracking will be implemented with database integration"
  }
}
```

---

### AI Chatbot

#### 18. Ask Question

**POST** `/chatbot/query`

Ask farming-related questions to AI chatbot (Google Gemini powered).

**Request Body:**
```json
{
  "question": "When is the best time to plant wheat in Punjab?",
  "context": "I have 50 hectares of land",  // Optional
  "language": "en",  // Default: "en"
  "session_id": "user_12345"  // Optional
}
```

**Field Constraints:**
- `question`: 3-500 characters (required)
- `language`: Language code (en, hi, etc.)
- `session_id`: For conversation tracking (optional)

**Response:**
```json
{
  "success": true,
  "message": "Question answered",
  "data": {
    "response_id": "resp_1705315800_abc456",
    "timestamp": "2024-01-15T10:30:00",
    "question": "When is the best time to plant wheat in Punjab?",
    
    "answer": "The best time to plant wheat in Punjab is from late October to mid-November (Rabi season). Here's a detailed timeline:\n\n1. **Optimal Sowing Window**: November 1-15\n2. **Soil Temperature**: 20-25°C ideal\n3. **Moisture**: Ensure adequate soil moisture before sowing\n4. **Variety Selection**: Choose varieties like PBW-725, HD-3086 for Punjab\n\nFor your 50 hectares, plan accordingly:\n- Prepare land in October\n- Complete sowing by November 15\n- Irrigate 4-6 times during growth period\n- Harvest in April (150-160 days after sowing)",
    
    "language": "en",
    "confidence": 0.92,
    
    "related_topics": [
      "Wheat varieties for Punjab",
      "Fertilizer schedule for Wheat",
      "Irrigation management in Rabi season",
      "Wheat pest control"
    ],
    
    "sources": [
      "Punjab Agricultural University guidelines",
      "Indian Council of Agricultural Research",
      "Crop production best practices"
    ],
    
    "session_id": "user_12345"
  }
}
```

**Frontend Usage:**
- Chat interface with message bubbles
- Display answer with markdown formatting
- Show related topics as clickable chips/tags
- Display sources as footnotes
- Save session_id for conversation continuity

---

#### 19. Explain Term

**POST** `/chatbot/explain`

Get detailed explanation of farming/agricultural terms.

**Request Body:**
```json
{
  "term": "NPK ratio",
  "language": "en",
  "context": "fertilizer bag label"  // Optional
}
```

**Response:**
```json
{
  "success": true,
  "message": "Term 'NPK ratio' explained",
  "data": {
    "term": "NPK ratio",
    
    "explanation": "NPK ratio represents the proportion of three primary nutrients in fertilizer:\n- **N (Nitrogen)**: Promotes leaf and stem growth\n- **P (Phosphorus)**: Supports root development and flowering\n- **K (Potassium)**: Improves disease resistance and overall plant health\n\nThe ratio is shown as three numbers (e.g., 10-20-10), indicating percentage by weight.",
    
    "examples": [
      "10-20-10: Balanced for general use",
      "20-10-10: High nitrogen for leafy crops",
      "5-10-15: High potassium for fruiting plants"
    ],
    
    "related_terms": [
      "Macronutrients",
      "Fertilizer grade",
      "Micronutrients",
      "Soil testing"
    ],
    
    "language": "en",
    
    "measurement_method": "Chemical analysis of fertilizer composition",
    
    "learning_resources": [
      "Soil testing laboratories",
      "Agricultural extension services",
      "Fertilizer manufacturer guidelines"
    ]
  }
}
```

**Frontend Usage:**
- Glossary/dictionary feature
- Tooltip explanations in forms
- "Learn more" popups
- Display examples as list
- Link related terms

---

#### 20. Get Conversation History

**GET** `/chatbot/conversation/{session_id}`

Get chat history for a session (placeholder - requires database).

**Example:** `/chatbot/conversation/user_12345`

**Response:**
```json
{
  "success": true,
  "message": "Conversation history",
  "data": {
    "session_id": "user_12345",
    "messages": [],
    "note": "Conversation tracking will be implemented with database integration"
  }
}
```

---

#### 21. Chatbot Status

**GET** `/chatbot/status`

Check if chatbot service is operational.

**Response:**
```json
{
  "success": true,
  "message": "Chatbot status",
  "data": {
    "status": "operational",  // or "fallback_mode"
    "api_configured": true,
    "model": "gemini-pro",
    "capabilities": [
      "question_answering",
      "term_explanation",
      "multilingual_support"
    ],
    "supported_languages": ["en", "hi", "mr", "ta", "te"]
  }
}
```

**Status Values:**
- `operational` - Gemini API working
- `fallback_mode` - API key missing, using fallback responses

---

## Data Models

### Available Data Lists

#### Crops (55 total)
```
Rice, Wheat, Cotton, Sugarcane, Maize, Bajra, Jowar, Groundnut, 
Sunflower, Soyabean, Rapeseed & Mustard, Arhar/Tur, Gram, Masoor, 
Moong, Urad, Sesamum, Safflower, Castor seed, Linseed, Nigerseed, 
Barley, Ragi, Small millets, Coriander, Potato, Onion, Tapioca, 
Sweet potato, Coconut, Arecanut, Cashewnut, Dry chillies, Garlic, 
Ginger, Turmeric, Black pepper, Dry ginger, Cardamom, Banana, 
Papaya, Khesari, Jute, Mesta, Tobacco, Tea, Coffee, Rubber, 
Peas & beans, Tomato, Brinjal, Cabbage, Cauliflower, Pumpkin, 
Bitter Gourd
```

#### States (30 total)
```
Andhra Pradesh, Assam, Bihar, Chhattisgarh, Gujarat, Haryana, 
Himachal Pradesh, Jammu and Kashmir, Jharkhand, Karnataka, 
Kerala, Madhya Pradesh, Maharashtra, Manipur, Meghalaya, 
Nagaland, Odisha, Punjab, Rajasthan, Sikkim, Tamil Nadu, 
Telangana, Tripura, Uttar Pradesh, Uttarakhand, West Bengal, 
Andaman and Nicobar Islands, Dadra and Nagar Haveli, Goa, 
Puducherry
```

#### Seasons (6 total)
```
Kharif, Rabi, Summer, Whole Year, Autumn, Winter
```

---

## Usage Examples

### Complete React Integration Example

```javascript
// api.js - API service layer
const API_BASE_URL = 'http://localhost:8000/api/v1';

export const api = {
  // System Info
  async getSystemInfo() {
    const response = await fetch(`${API_BASE_URL}/info`);
    return response.json();
  },
  
  // Yield Prediction
  async predictYield(data) {
    const response = await fetch(`${API_BASE_URL}/yield/predict`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  },
  
  // Gap Analysis
  async analyzeYieldGap(data) {
    const response = await fetch(`${API_BASE_URL}/yield/gap-analysis`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  },
  
  // Weather
  async getCurrentWeather(latitude, longitude) {
    const response = await fetch(`${API_BASE_URL}/weather/current`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ latitude, longitude })
    });
    return response.json();
  },
  
  // Disease Detection
  async detectDisease(imageFile, cropType, location) {
    const formData = new FormData();
    formData.append('file', imageFile);
    formData.append('crop_type', cropType);
    if (location) formData.append('location', location);
    
    const response = await fetch(`${API_BASE_URL}/disease/detect`, {
      method: 'POST',
      body: formData
    });
    return response.json();
  },
  
  // Chatbot
  async askChatbot(question, sessionId) {
    const response = await fetch(`${API_BASE_URL}/chatbot/query`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question, session_id: sessionId })
    });
    return response.json();
  }
};
```

### React Component Example - Yield Prediction

```jsx
import React, { useState, useEffect } from 'react';
import { api } from './api';

function YieldPredictor() {
  const [crops, setCrops] = useState([]);
  const [formData, setFormData] = useState({
    crop: '',
    state: '',
    season: 'Kharif',
    area: '',
    fertilizer: '',
    pesticide: ''
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  
  useEffect(() => {
    // Load available crops on mount
    api.getSystemInfo().then(res => {
      setCrops(res.data.datasets.available_crops);
    });
  }, []);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    const response = await api.predictYield({
      ...formData,
      area: parseFloat(formData.area),
      fertilizer: parseFloat(formData.fertilizer),
      pesticide: parseFloat(formData.pesticide)
    });
    
    if (response.success) {
      setResult(response.data);
    }
    setLoading(false);
  };
  
  return (
    <div className="yield-predictor">
      <h2>Yield Prediction</h2>
      
      <form onSubmit={handleSubmit}>
        <select 
          value={formData.crop}
          onChange={(e) => setFormData({...formData, crop: e.target.value})}
          required
        >
          <option value="">Select Crop</option>
          {crops.map(crop => (
            <option key={crop} value={crop}>{crop}</option>
          ))}
        </select>
        
        {/* Add more inputs for state, season, area, etc. */}
        
        <button type="submit" disabled={loading}>
          {loading ? 'Predicting...' : 'Predict Yield'}
        </button>
      </form>
      
      {result && (
        <div className="result">
          <h3>Predicted Yield: {result.predicted_yield} tons/hectare</h3>
          <p>Confidence: {(result.model_confidence * 100).toFixed(1)}%</p>
          
          <div className="recommendations">
            <h4>Recommendations:</h4>
            <ul>
              {result.recommendations.map((rec, i) => (
                <li key={i}>{rec}</li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}
```

---

## Frontend Development Checklist

### 1. Initial Setup
- [ ] Create React app
- [ ] Setup API service layer (`api.js`)
- [ ] Configure base URL (environment variable)
- [ ] Add CORS handling if needed
- [ ] Setup error boundary

### 2. Core Features
- [ ] **Dashboard**: System info, statistics
- [ ] **Yield Prediction**: Form + Results display
- [ ] **Gap Analysis**: Dual scenario (tabs/toggle)
- [ ] **Weather**: Current + 7-day forecast
- [ ] **Soil Analysis**: State selection + suitability check
- [ ] **Disease Detection**: Image upload + results
- [ ] **Chatbot**: Chat interface with history

### 3. UI Components Needed
- [ ] Dropdown (crops, states, seasons)
- [ ] Number inputs (area, fertilizer, pesticide)
- [ ] File upload (image)
- [ ] Results cards
- [ ] Gauge/progress bar (gap analysis)
- [ ] Weather cards
- [ ] Chart/graph (benchmarks comparison)
- [ ] Chat bubble component
- [ ] Loading spinners
- [ ] Error messages

### 4. Data Management
- [ ] Fetch available crops/states on app load
- [ ] Cache system info to avoid repeated calls
- [ ] Local storage for session_id (chatbot)
- [ ] Form validation
- [ ] Error handling for API failures

### 5. User Experience
- [ ] Responsive design (mobile-friendly)
- [ ] Loading states
- [ ] Empty states
- [ ] Error states (404, 500, validation errors)
- [ ] Success feedback
- [ ] Tooltips for field explanations
- [ ] Help/documentation links

### 6. Optional Enhancements
- [ ] Dark mode
- [ ] Multi-language support
- [ ] Export results (PDF/CSV)
- [ ] Share functionality
- [ ] Comparison tool (multiple predictions)
- [ ] Historical data charts
- [ ] Geolocation for weather
- [ ] Voice input for chatbot

---

## Testing Recommendations

### Unit Tests
- Test API service layer functions
- Test form validation
- Test data transformations

### Integration Tests
- Test complete user flows
- Test error scenarios
- Test loading states

### API Testing Tools
- **Swagger UI**: http://localhost:8000/docs
- **Postman**: Import OpenAPI schema
- **cURL**: Command-line testing

### Sample Test Data

```json
// Valid Yield Prediction
{
  "crop": "Rice",
  "state": "Punjab",
  "season": "Kharif",
  "area": 100,
  "fertilizer": 25000,
  "pesticide": 500
}

// Valid Gap Analysis (Post-Harvest)
{
  "crop": "Wheat",
  "state": "Punjab",
  "season": "Rabi",
  "actual_yield": 3.2
}

// Valid Weather Request
{
  "latitude": 30.7333,
  "longitude": 76.7794
}
```

---

## Performance Considerations

1. **API Response Times**
   - Health/Info: ~50ms
   - Yield Prediction: ~200ms (ML inference)
   - Weather: ~500ms (external API call)
   - Chatbot: ~2-5s (AI generation)
   - Disease Detection: ~3-8s (image processing + AI)

2. **Optimization Tips**
   - Cache `/info` response (crops/states lists)
   - Debounce chatbot input
   - Show loading indicators for slow endpoints
   - Implement request cancellation for rapid inputs
   - Use pagination for large datasets

3. **Rate Limiting**
   - Currently no rate limits
   - Implement frontend throttling for chatbot
   - Avoid rapid-fire API calls

---

## Common Issues & Troubleshooting

### Issue: CORS Error
**Solution:** Backend already has CORS enabled. Ensure frontend uses correct URL.

### Issue: 422 Validation Error
**Cause:** Missing required fields or invalid data types  
**Solution:** Check request body matches Pydantic models exactly

### Issue: Chatbot returns "fallback_mode"
**Cause:** GEMINI_API_KEY not configured  
**Solution:** Check backend `.env` file, restart server

### Issue: Crop/State not found in dropdown
**Cause:** Typo or using wrong case  
**Solution:** Use exact names from `/info` endpoint

### Issue: Disease detection fails
**Cause:** Invalid image format or size  
**Solution:** Ensure JPG/PNG/WEBP, max 10MB

---

## API Versioning

Current version: **v1**

All endpoints prefixed with `/api/v1/`

Future versions will use `/api/v2/`, etc. without breaking v1.

---

## Support & Contact

- **API Documentation (Interactive)**: http://localhost:8000/docs
- **GitHub Issues**: [Your Repo Link]
- **Email**: [Your Email]

---

## Changelog

### Version 1.0.0 (Current)
- Initial API release
- 23 endpoints across 6 categories
- ML-based yield prediction
- AI-powered chatbot
- Real-time weather integration
- Disease detection with treatment plans

---

## License

[Your License Here]

---

**Last Updated:** January 2024  
**Maintained By:** FasalMitra Development Team

---

## Quick Reference Card

| Feature | Endpoint | Method | Key Fields |
|---------|----------|--------|------------|
| **System Info** | `/info` | GET | crops, states, features |
| **Predict Yield** | `/yield/predict` | POST | crop, state, season, area, fertilizer |
| **Gap Analysis** | `/yield/gap-analysis` | POST | crop, state, actual_yield OR area/fertilizer |
| **Current Weather** | `/weather/current` | POST | latitude, longitude |
| **Forecast** | `/weather/forecast` | POST | latitude, longitude, days |
| **Soil Data** | `/soil/data/{state}` | GET | state (path param) |
| **Suitability** | `/soil/suitability` | POST | state, crop (query params) |
| **Detect Disease** | `/disease/detect` | POST | file, crop_type (form-data) |
| **Ask Chatbot** | `/chatbot/query` | POST | question, session_id |
| **Explain Term** | `/chatbot/explain` | POST | term, language |

---

**Happy Coding! 🚀🌾**
