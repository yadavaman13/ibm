# FasalMitra - Complete Start Guide

**For Fresh Copilot Chats & New Team Members**

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Quick Start (5 Minutes)](#quick-start-5-minutes)
3. [Server Setup](#server-setup)
4. [Client Setup](#client-setup)
5. [Testing](#testing)
6. [Important Documents](#important-documents)
7. [Development Workflow](#development-workflow)
8. [Troubleshooting](#troubleshooting)

---

## Project Overview

**FasalMitra** is a Smart Farming Assistant with AI-powered agricultural advisory services.

### Architecture
```
Fasal-Mitra/           # Root directory
├── data/              # Datasets (at root level)
│   ├── raw/           # Original CSV files
│   ├── processed/     # Cleaned datasets
│   ├── gujarat/       # Gujarat-specific data
│   └── external/      # External data sources
│
└── fasal-mitra/       # Main application folder
    ├── server/        # FastAPI Backend (Python 3.13)
    │   ├── app/       # API application
    │   └── tests/     # Test files
    │
    └── client/        # React Frontend (Vite + Tailwind)
        └── src/       # React application
```

### Tech Stack
- **Backend:** FastAPI 0.104+, Python 3.13.5, Scikit-learn, Pandas
- **Frontend:** React 19.1.0, Vite 7.0.4, Tailwind CSS 4.1.18
- **ML/AI:** Random Forest (97.5% accuracy), Google Gemini AI
- **External APIs:** Open-Meteo (weather)

---

## Quick Start (5 Minutes)

### Prerequisites
- Python 3.13+ installed
- Node.js 18+ installed
- Git installed

### Clone Repository
```bash
git clone <repository-url>
cd Fasal-Mitra
```

### Start Backend (Terminal 1)
```bash
cd Fasal-Mitra
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux/Mac

cd fasal-mitra/server
pip install -r requirements.txt
python run.py
```

Backend runs at: **http://localhost:8000**

### Start Frontend (Terminal 2)
```bash
cd fasal-mitra/client
npm install
npm run dev
```

Frontend runs at: **http://localhost:5173**

---

## Server Setup

### Step 1: Create Virtual Environment

```bash
cd fasal-mitra/server
python -m venv .venv
```

**Location:** `D:/Code/Fasal-Mitra/.venv/`

### Step 2: Activate Virtual Environment

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Key Packages:**
- fastapi==0.104.0+
- uvicorn[standard]
- scikit-learn
- pandas
- python-dotenv
- google-generativeai
- httpx

### Step 4: Configure Environment

Create `.env` file in `server/` directory:

```env
# Server Configuration
APP_NAME=FasalMitra - Smart Farming Assistant API
APP_VERSION=1.0.0
ENVIRONMENT=development

# API Keys
GEMINI_API_KEY=your_gemini_api_key_here

# CORS
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

**Important:** Get Gemini API key from: https://makersuite.google.com/app/apikey

### Step 5: Verify Data Files

Ensure these CSV files exist in `data/raw/`:
- `crop_yield.csv` (19,689 records)
- `state_soil_data.csv` (30 states)
- `state_weather_data_1997_2020.csv` (720 records)
- `Price_Agriculture_commodities_Week.csv` (23,093 records)

### Step 6: Run Server

```bash
python run.py
```

**OR using uvicorn:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Verify:**
- Server: http://localhost:8000
- API Docs (Swagger): http://localhost:8000/docs
- Health Check: http://localhost:8000/api/v1/health

---

## Client Setup

### Step 1: Install Dependencies

```bash
cd fasal-mitra/client
npm install
```

**Key Packages:**
- react 19.1.0
- react-router-dom
- tailwindcss 4.1.18
- lucide-react
- vite 7.0.4

### Step 2: Configure Environment (Optional)

Create `.env` in `client/` directory:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

### Step 3: Start Development Server

```bash
npm run dev
```

**Verify:**
- Frontend: http://localhost:5173
- Dashboard should load with 6 feature cards

---

## Testing

### Backend Testing

#### 1. Run Complete Test Suite

```bash
cd fasal-mitra/server
D:/Code/Fasal-Mitra/.venv/Scripts/python.exe test_complete.py
```

**Expected:** ✅ 17/17 tests passing (100%)

#### 2. Run Quick API Test

```bash
D:/Code/Fasal-Mitra/.venv/Scripts/python.exe test_api.py
```

**Expected:** ✅ 9/9 tests passing

#### 3. Test Gap Analysis (Both Scenarios)

```bash
python test_gap_analysis_both.py
```

**Tests:**
- Post-harvest scenario (with actual_yield)
- Pre-harvest scenario (with farming inputs)

#### 4. Manual Testing via Swagger UI

1. Open http://localhost:8000/docs
2. Try these endpoints:
   - `GET /api/v1/health` - Server status
   - `GET /api/v1/info` - System information
   - `POST /api/v1/yield/predict` - Yield prediction
   - `POST /api/v1/chatbot/query` - AI chatbot

**Important:** Always use the virtual environment's Python:
```bash
D:/Code/Fasal-Mitra/.venv/Scripts/python.exe <script_name>
```

### Frontend Testing

Currently no automated tests. Manual testing:

1. Navigate to http://localhost:5173
2. Check dashboard loads
3. Click feature cards to verify routing
4. Test mobile responsive design (Chrome DevTools)
5. Check navbar menu on mobile

---

## Important Documents

### 📚 Must Read (In This Order)

#### For Backend Development:
1. **`server/API_DOCUMENTATION.md`** (88KB, comprehensive)
   - All 23 API endpoints documented
   - Request/response examples
   - React integration examples
   - Error handling guide

2. **`server/BACKEND_COMPLETE.md`**
   - Backend architecture overview
   - API endpoint summary
   - Testing guide

3. **`server/app/config.py`**
   - Environment configuration
   - API key setup

#### For Frontend Development:
1. **`client/DEVELOPMENT_GUIDELINES.md`** (THIS IS CRITICAL)
   - CSS variable system (NO inline styles!)
   - Component structure
   - Mobile-first design
   - Accessibility requirements

2. **`server/API_DOCUMENTATION.md`**
   - For API integration

#### For Complete Understanding:
1. **`START_GUIDE.md`** (this file)
2. **`PROJECT_STATUS.md`** - Current status
3. **`.github/copilot-instructions.md`** - AI rules

### 📁 Data Documentation

- **`data/raw/README.md`** - Dataset descriptions
- **`data/processed/README.md`** - Cleaned data info

---

## Development Workflow

### For New Features

#### Backend Feature:
1. Create endpoint in `server/app/api/v1/endpoints/`
2. Define Pydantic models in `server/app/models/`
3. Implement business logic in `server/app/services/`
4. Test with `test_api.py` or `test_complete.py`
5. Document in `API_DOCUMENTATION.md`

#### Frontend Feature:
1. Create component in `client/src/components/` or page in `client/src/pages/`
2. Create CSS file in `client/src/styles/` (use CSS variables!)
3. Add route in `client/src/App.jsx`
4. Test responsive design (mobile → tablet → desktop)
5. Verify accessibility (keyboard navigation, ARIA labels)

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/yield-prediction-ui

# Make changes, commit
git add .
git commit -m "feat: add yield prediction form"

# Push and create PR
git push origin feature/yield-prediction-ui
```

**Commit Message Format:**
- `feat:` New feature
- `fix:` Bug fix
- `refactor:` Code improvement
- `docs:` Documentation
- `style:` CSS/design changes

---

## Troubleshooting

### Server Issues

#### Problem: Module not found
**Solution:**
```bash
# Ensure virtual environment is activated
.venv\Scripts\activate
pip install -r requirements.txt
```

#### Problem: GEMINI_API_KEY not loading
**Solution:**
1. Check `.env` file exists in `server/` directory
2. Verify `GEMINI_API_KEY=your_key_here` (no quotes)
3. Restart server after changing `.env`

**Verify:**
```bash
curl http://localhost:8000/api/v1/chatbot/status
```
Should show `"status": "operational"`

#### Problem: Tests failing
**Solution:**
```bash
# Always use virtual environment Python
D:/Code/Fasal-Mitra/.venv/Scripts/python.exe test_complete.py
```

#### Problem: Empty dataset lists
**Solution:**
- Verify CSV files are in `D:/Code/Fasal-Mitra/data/raw/`
- Check `app/config.py` has correct `DATA_DIR` path
- Restart server

### Client Issues

#### Problem: npm install fails
**Solution:**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### Problem: Vite server won't start
**Solution:**
```bash
# Check if port 5173 is in use
netstat -ano | findstr :5173

# Kill process or use different port
npm run dev -- --port 3000
```

#### Problem: Styles not applying
**Solution:**
1. Check CSS file is imported in component
2. Verify CSS variables in `src/index.css`
3. Clear browser cache (Ctrl+Shift+R)
4. Check Tailwind classes are correct

#### Problem: API calls failing (CORS error)
**Solution:**
1. Backend must be running on port 8000
2. Check `.env` in server: `ALLOWED_ORIGINS=http://localhost:5173`
3. Restart backend server

---

## Environment Setup Checklist

### Before Starting Development:

- [ ] Python 3.13+ installed and in PATH
- [ ] Node.js 18+ installed
- [ ] Virtual environment created at `D:/Code/Fasal-Mitra/.venv/`
- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] Frontend dependencies installed (`npm install`)
- [ ] `.env` file created in `server/` with GEMINI_API_KEY
- [ ] Data files present in `data/raw/` directory
- [ ] Backend running at http://localhost:8000
- [ ] Frontend running at http://localhost:5173
- [ ] All tests passing (17/17)

### Before First Commit:

- [ ] Read `DEVELOPMENT_GUIDELINES.md` completely
- [ ] Read `API_DOCUMENTATION.md` for API endpoints
- [ ] Code follows guidelines (no inline styles, mobile-first, etc.)
- [ ] Tested locally on mobile view
- [ ] No `console.log` statements in code
- [ ] Proper commit message format

---

## API Quick Reference

### Base URL
```
http://localhost:8000/api/v1
```

### Common Endpoints

| Feature | Endpoint | Method |
|---------|----------|--------|
| Health Check | `/health` | GET |
| System Info | `/info` | GET |
| Yield Prediction | `/yield/predict` | POST |
| Gap Analysis | `/yield/gap-analysis` | POST |
| Weather Current | `/weather/current` | POST |
| Soil Data | `/soil/data/{state}` | GET |
| Disease Detection | `/disease/detect` | POST |
| AI Chatbot | `/chatbot/query` | POST |

**Full documentation:** `server/API_DOCUMENTATION.md`

---

## File Structure Overview

```
Fasal-Mitra/                        # Root directory
├── data/                           # ⭐ Datasets (at root level)
│   ├── raw/                        # Original CSV files
│   │   ├── crop_yield.csv
│   │   ├── state_soil_data.csv
│   │   ├── state_weather_data_1997_2020.csv
│   │   └── Price_Agriculture_commodities_Week.csv
│   ├── processed/                  # Cleaned datasets
│   ├── gujarat/                    # Gujarat-specific data
│   └── external/                   # External data sources
│
├── .venv/                          # ⭐ Virtual environment (at root level)
│
└── fasal-mitra/                    # Main application folder
    ├── server/
    │   ├── app/
    │   │   ├── api/v1/endpoints/   # API endpoints
    │   │   ├── core/               # Data loader, farming system
    │   │   ├── models/             # Pydantic schemas
    │   │   ├── services/           # Business logic
    │   │   ├── middleware/         # Error handling
    │   │   └── main.py             # FastAPI app
    │   ├── test_api.py             # Quick tests (9)
    │   ├── test_complete.py        # Full tests (17)
    │   ├── run.py                  # Server startup
    │   ├── requirements.txt        # Python deps
    │   ├── .env                    # Environment vars
    │   └── API_DOCUMENTATION.md    # ⭐ API docs
    │
    ├── client/
    │   ├── src/
    │   │   ├── components/         # Reusable components
    │   │   │   ├── Navbar.jsx
    │   │   │   └── FeatureCard.jsx
    │   │   ├── pages/              # Route components
    │   │   │   ├── Dashboard.jsx
    │   │   │   └── YieldPrediction.jsx
    │   │   ├── styles/             # ⭐ CSS files (use CSS vars!)
    │   │   │   ├── navbar.css
    │   │   │   ├── feature-card.css
    │   │   │   ├── dashboard.css
    │   │   │   └── pages.css
    │   │   ├── App.jsx             # Routes
    │   │   ├── main.jsx            # Entry point
    │   │   └── index.css           # ⭐ Theme variables
    │   ├── package.json
    │   └── DEVELOPMENT_GUIDELINES.md  # ⭐ Frontend rules
    │
    ├── START_GUIDE.md              # ⭐ This file
    └── PROMPT.txt                  # Copilot training prompt
```

---

## Key Principles

### 🚨 Critical Rules

1. **NO INLINE STYLES** - Use CSS variables in `index.css`
2. **Mobile-First** - Design for mobile, enhance for desktop
3. **Test Before Commit** - Run tests, verify locally
4. **Read Documentation** - Before asking questions
5. **Virtual Environment** - Always use `.venv` Python for server

### 💡 Development Tips

- Keep components small (<150 lines)
- Use semantic HTML for accessibility
- Follow naming conventions (see guidelines)
- Commit message format: `feat:`, `fix:`, `docs:`, etc.
- Ask for help after reading docs

---

## Contact & Support

### When You Need Help:

1. **Check Documentation:**
   - `START_GUIDE.md` (setup issues)
   - `DEVELOPMENT_GUIDELINES.md` (frontend standards)
   - `API_DOCUMENTATION.md` (API integration)

2. **Debugging Steps:**
   - Read error messages carefully
   - Check browser/terminal console
   - Verify virtual environment is activated
   - Ensure both servers are running

3. **Ask Team Lead:**
   - Architecture decisions
   - Design clarifications
   - Complex bug assistance

---

## Next Steps

### After Setup:

1. ✅ Verify both servers running
2. ✅ Run all tests (17/17 passing)
3. ✅ Read `DEVELOPMENT_GUIDELINES.md`
4. ✅ Read `API_DOCUMENTATION.md`
5. ✅ Explore code structure
6. ✅ Try manual testing in Swagger UI
7. ✅ Create first feature branch

### Ready to Code?

Pick a task from the project board and follow the development workflow above!

---

**Good luck with development! 🚀🌾**

For fresh Copilot chat setup, see `PROMPT.txt`
