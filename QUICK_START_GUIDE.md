# 🚀 Quick Start Guide: Building Your Farming Advisory System

**Goal:** Get a working MVP in 2-3 weeks with current datasets

---

## 📦 What You Have vs What You Need

### ✅ READY TO USE (100% complete):
- `crop_yield.csv` - 19,689 records, 55 crops, 30 states, 1997-2020
- `state_soil_data.csv` - 30 states, NPK + pH levels
- `state_weather_data_1997_2020.csv` - 720 records, historical climate
- `crop_calendar_cleaned.csv` - 6,293 records, 230 crops, 12 states, 310 districts ✨ NEW!
- `merged_dataset.csv` - ML-ready merged data (19,689 rows)

### ⚠️ NEED TO ACQUIRE (for full feature set):
- **Mandi price data** (for price trends) - sample data available via `download_agmarknet.py`
- **Weather forecast API** (for real-time advice) - OpenWeatherMap (free tier)

---

## 🎯 Phase 1: MVP with Current Data (Start TODAY)

### Features You Can Build Right Now:

#### 1. Crop-Soil Suitability Matcher ✅
```python
# Example logic:
def check_soil_suitability(crop, state):
    soil = soil_data[soil_data['state'] == state]
    crop_requirements = {
        'Rice': {'pH': (5.5, 7.0), 'N': (60, 120)},
        'Wheat': {'pH': (6.0, 7.5), 'N': (80, 120)},
        # ... add from research
    }
    # Compare and return suitability score
```

**Data sources:**
- `state_soil_data.csv` (N, P, K, pH)
- Crop pH requirements (add manually or from ICAR data)

**Output example:**
> "✅ Your soil (pH 6.5, N:75) is SUITABLE for Wheat in Punjab"

---

#### 2. Yield Prediction Model ✅
```python
# Use Random Forest or Linear Regression
from sklearn.ensemble import RandomForestRegressor

features = ['area', 'production', 'fertilizer', 'pesticide', 
            'avg_temp_c', 'total_rainfall_mm', 'N', 'P', 'K', 'pH']
target = 'yield'

# Train on crop_yield.csv merged with weather + soil data
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Predict yield for user input
predicted_yield = model.predict(user_inputs)
```

**Data sources:**
- Merge all 3 CSVs on `state` + `year`
- Train separate models per crop or use crop as categorical feature

**Output example:**
> "Expected yield: 28.5 quintals/hectare (±3.2)"

---

#### 3. Best Season Recommender ✅
```python
def recommend_season(crop, state):
    historical = crop_yield[
        (crop_yield['crop'] == crop) & 
        (crop_yield['state'] == state)
    ]
    best_season = historical.groupby('season')['yield'].mean().idxmax()
    avg_yield = historical[historical['season'] == best_season]['yield'].mean()
    
    return best_season, avg_yield
```

**Data sources:**
- `crop_yield.csv` (season, yield columns)

**Output example:**
> "🌾 Wheat grows best in **Rabi** season in Punjab (avg yield: 32 quintals/ha)"

---

#### 4. Fertilizer Optimizer ✅
```python
def optimize_fertilizer(crop, state, target_yield):
    # Historical data analysis
    data = crop_yield[
        (crop_yield['crop'] == crop) & 
        (crop_yield['state'] == state)
    ]
    
    # Find fertilizer amount for similar yields
    similar = data[
        (data['yield'] >= target_yield * 0.9) & 
        (data['yield'] <= target_yield * 1.1)
    ]
    
    recommended_fertilizer = similar['fertilizer'].median()
    return recommended_fertilizer
```

**Data sources:**
- `crop_yield.csv` (fertilizer, yield)
- `state_soil_data.csv` (current NPK levels)

**Output example:**
> "💡 For 30 quintal/ha wheat, use 24,500 kg fertilizer (based on 450 similar cases)"

---

#### 5. Explainable AI ✅
```python
def explain_recommendation(recommendation, inputs):
    explanations = {
        'soil_suitable': f"Your soil pH {inputs['pH']} matches the optimal range for {inputs['crop']}",
        'high_yield': f"Historical data shows {inputs['state']} gets {inputs['avg_yield']} quintal/ha",
        'season_match': f"{inputs['season']} season has 85% success rate for this crop"
    }
    return explanations
```

**Output example:**
> **Why this recommendation?**  
> ✓ Your soil pH 6.5 is optimal for wheat (range: 6.0-7.5)  
> ✓ Punjab averages 32 quintal/ha for wheat in Rabi  
> ✓ 1200mm rainfall in your area matches crop requirement

---

#### 6. Risk Alert System ✅ 🎉 COMPLETE!
```python
def check_sowing_risk(crop, state, district=None):
    # Load crop calendar
    calendar = pd.read_csv('data/processed/crop_calendar_cleaned.csv')
    
    # Get current month
    current_month = datetime.now().month
    
    # Find sowing window for crop
    crop_data = calendar[
        (calendar['crop'].str.lower() == crop.lower()) &
        (calendar['state'].str.lower() == state.lower())
    ]
    
    # Check if within sowing window
    # Returns: OPTIMAL, TOO_EARLY, or TOO_LATE
    return risk_assessment
```

**Data sources:**
- `crop_calendar_cleaned.csv` (6,293 sowing/harvesting schedules)
- 12 states, 310 districts, 230 crops

**Output example:**
> ✅ **OPTIMAL TIME!** You're within the sowing window for Kharif season  
> 📍 District: Rajkot | Season: Summer  
> 🌱 Sowing Period: Early Feb | 🌾 Harvesting: Mid May  
> 🟢 Risk Level: LOW - Proceed with sowing

**Testing:**
```bash
python test_risk_alert_system.py
```

---

### Simple UI (Console Version for MVP)
```python
print("🌾 FARMING ADVISORY SYSTEM 🌾")
print("="*50)

state = input("Enter your state: ")
crop = input("Enter crop name: ")
season = input("Enter season (Kharif/Rabi/Zaid): ")

# Feature 1: Soil check
suitability = check_soil_suitability(crop, state)
print(f"\n✅ Soil Suitability: {suitability}")

# Feature 2: Yield prediction
predicted_yield = predict_yield(crop, state, season)
print(f"📊 Expected Yield: {predicted_yield} quintal/ha")

# Feature 3: Best season
if season_is_optimal(crop, state, season):
    print(f"🌟 {season} is the BEST season for {crop}")
else:
    best = get_best_season(crop, state)
    print(f"⚠️ Consider {best} season instead (20% higher yield)")

# Feature 4: Fertilizer
fertilizer = optimize_fertilizer(crop, state, predicted_yield)
print(f"💡 Recommended fertilizer: {fertilizer} kg")

# Feature 5: Explanation
print(f"\n🧠 Why? {explain_recommendation()}")
```

---

## 🛠️ Phase 2: Enhance Features (Week 2-3)

### Step 1: Generate Sample Price Data (Optional)
```bash
python download_agmarknet.py
# Choose option 2 (Generate sample data for demo)
```
This creates: `data/sample/mandi_prices_sample.csv` ✅ Already done!

### Step 2: Crop Calendar ✅ COMPLETE!
```bash
# Already extracted from PDF! See files:
# - data/processed/crop_calendar_cleaned.csv (6,293 records)
# - data/processed/crop_calendar_state_summary.csv

# Test the risk alert system:
python test_risk_alert_system.py
```

**If you get a new crop calendar PDF:**
```bash
python extract_crop_calendar_pdf.py  # Extract from PDF
python clean_crop_calendar.py        # Clean and validate
```

### Step 3: Weather Forecast API
```bash
# Sign up: https://openweathermap.org/api
# Free tier: 1000 calls/day

pip install requests

# Test API:
python scripts/test_weather_api.py
```

---

## 📊 Phase 3: Integrate New Data (Week 3-4)

### Feature 7: Price Trend Analysis
```python
def analyze_price_trend(crop, state, days=30):
    prices = mandi_data[
        (mandi_data['crop'] == crop) & 
        (mandi_data['state'] == state)
    ].tail(days)
    
    # Simple linear regression for trend
    from scipy.stats import linregress
    slope, _, _, _, _ = linregress(range(len(prices)), prices['price_modal'])
    
    if slope > 5:
        trend = "RISING"
        advice = "Wait 5-7 days before selling"
    elif slope < -5:
        trend = "FALLING"
        advice = "Consider selling now"
    else:
        trend = "STABLE"
        advice = "Sell when convenient"
    
    return trend, advice
```

### Feature 8: Weather-Based Decision Advice
```python
def check_weather_risk(crop, state, growth_stage):
    # Get forecast from API
    forecast = get_weather_forecast(state, days=7)
    
    # Get crop calendar
    crop_info = crop_calendar[
        (crop_calendar['crop'] == crop) & 
        (crop_calendar['state'] == state)
    ].iloc[0]
    
    alerts = []
    
    # Heavy rain risk
    if forecast['rainfall'].sum() > crop_info['flood_threshold']:
        alerts.append({
            'level': 'HIGH',
            'message': f"⚠️ Heavy rain ({forecast['rainfall'].sum()}mm) expected. "
                      f"Risk of waterlogging during {growth_stage}."
        })
    
    # Drought risk
    if forecast['rainfall'].sum() < crop_info['drought_threshold']:
        alerts.append({
            'level': 'MEDIUM',
            'message': f"💧 Low rainfall expected. Consider irrigation for {crop}."
        })
    
    return alerts
```

---

## 🎨 Phase 4: Build UI (Week 4-5)

### Option A: Web App (Flask + HTML/CSS)
```bash
pip install flask

# Run:
python app.py
# Visit: http://localhost:5000
```

### Option B: Mobile App (Flutter)
```bash
flutter create farming_app
# Build APK for demo
flutter build apk
```

### Option C: Streamlit (Fastest)
```bash
pip install streamlit

# Run:
streamlit run app_streamlit.py
# Auto-opens in browser
```

**Recommended for MVP:** Streamlit (2-3 days to build UI)

---

## 📁 Project Structure

```
farming-advisory-system/
│
├── data/
│   ├── raw/                    # Original CSVs
│   │   ├── crop_yield.csv
│   │   ├── state_soil_data.csv
│   │   └── state_weather_data_1997_2020.csv
│   │
│   ├── processed/              # Cleaned, merged data
│   │   └── merged_dataset.csv
│   │
│   ├── sample/                 # Mock data for demo
│   │   └── mandi_prices_sample.csv
│   │
│   └── templates/              # To fill manually
│       └── crop_calendar_template.csv
│
├── models/                     # Trained ML models
│   ├── yield_predictor.pkl
│   └── price_trend_model.pkl
│
├── scripts/                    # Data processing
│   ├── download_agmarknet.py
│   ├── create_crop_calendar.py
│   ├── merge_datasets.py
│   └── train_models.py
│
├── app/                        # Application code
│   ├── app.py                  # Main Flask/Streamlit app
│   ├── features.py             # Feature implementations
│   ├── utils.py                # Helper functions
│   └── templates/              # HTML templates
│
├── tests/                      # Unit tests
│   └── test_features.py
│
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
└── DATASET_ANALYSIS_REPORT.md  # This analysis
```

---

## 🐍 Create requirements.txt

```txt
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
scipy>=1.11.0
flask>=3.0.0
streamlit>=1.28.0
requests>=2.31.0
matplotlib>=3.7.0
seaborn>=0.12.0
```

Install all:
```bash
pip install -r requirements.txt
```

---

## ✅ 2-Week Sprint Plan

### Week 1: Core Features ✅ (Risk Alert DONE!)
- **Day 1-2:** ✅ Merge datasets, explore data, extract crop calendar from PDF
- **Day 3:** Build soil suitability + season recommender  
- **Day 4:** Build fertilizer optimizer + train yield prediction model
- **Day 5:** Build explainability + test risk alert system ✅
- **Day 6-7:** Build basic UI (console/Streamlit)

### Week 2: Polish & Deploy
- **Day 8-9:** Build/enhance Streamlit UI with all 7 features
- **Day 10:** Integrate weather API (optional)
- **Day 11:** Add price trend feature (using sample data)
- **Day 12:** End-to-end testing + bug fixes
- **Day 13:** Demo preparation, slides, documentation
- **Day 14:** Practice demo / buffer time

---

## 🏆 Demo Script (for Judges)

```
1. Introduction (1 min)
   "Our app helps farmers make data-driven decisions using 24 years 
    of historical data covering 55 crops and 30 states."

2. Feature Demo (3 min)
   - Input: Punjab, Wheat, Rabi season
   - Show: Soil check → Yield prediction → Fertilizer recommendation
   - Highlight: Explainable AI output

3. Data Transparency (1 min)
   "We analyzed 20,000+ records. Current features use real government 
    data. Price trends use sample data - production version will use 
    live Agmarknet API."

4. Future Roadmap (1 min)
   - Phase 2: Weather forecast integration
   - Phase 3: Live market prices
   - Phase 4: Multi-language support

5. Q&A
```

---

## 🚨 Common Pitfalls to Avoid

1. **Don't over-promise:** Be honest about sample vs real data
2. **Don't build everything:** Focus on 4-5 solid features
3. **Don't skip testing:** Test with all 55 crops
4. **Don't ignore edge cases:** Handle missing states, invalid inputs
5. **Don't hardcode:** Use config files for thresholds

---

## 📞 Need Help?

**Stuck on data merging?**
```python
# Quick merge script:
import pandas as pd

crop = pd.read_csv('crop_yield.csv')
soil = pd.read_csv('state_soil_data.csv')
weather = pd.read_csv('state_weather_data_1997_2020.csv')

# Merge on state + year
merged = crop.merge(weather, on=['state', 'year'], how='left')
merged = merged.merge(soil, on='state', how='left')

merged.to_csv('data/processed/merged_dataset.csv', index=False)
```

**Stuck on model training?**
```python
# Simple yield predictor:
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

X = merged[['area', 'fertilizer', 'pesticide', 'avg_temp_c', 
            'total_rainfall_mm', 'N', 'P', 'K', 'pH']]
y = merged['yield']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

print(f"Model R² Score: {model.score(X_test, y_test):.3f}")
```

---

## ✅ Final Checklist

Before submitting/demoing:

- [x] All datasets loaded and tested ✅
- [x] Crop calendar extracted from PDF (6,293 records) ✅
- [x] Risk alert system built and tested ✅
- [x] Data merged for ML training ✅
- [ ] At least 5 core features working (currently have 7 ready!)
- [ ] Yield prediction model trained
- [ ] UI is intuitive (test with non-technical user)
- [ ] Explainability for every recommendation
- [ ] Error handling (invalid crop/state names)
- [x] README updated with new features ✅
- [x] Requirements.txt with all dependencies ✅
- [ ] Demo script prepared
- [ ] Slides ready (show data sources, methodology)
- [ ] GitHub repo clean and documented

---

**Good luck! 🌾 You have SOLID datasets to build a working MVP.**

**Remember:** Judges value honesty + working demo > flashy features with fake data.
