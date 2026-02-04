# Weather Widget Setup Guide

## Overview

The Weather Widget displays real-time weather data and 7-day forecasts using the OpenWeatherMap API.

## Features

✅ **Current Weather Display**
- Real-time temperature with °C/°F toggle
- Weather condition and icon
- Location display
- Date and time
- Refresh button

✅ **7-Day Forecast**
- Daily high/low temperatures
- Weather icons for each day
- Horizontal scrollable layout
- Responsive design

✅ **Weather Details**
- Cloud coverage (precipitation)
- Wind speed
- Humidity
- Air quality index

## API Setup

### API Tier Information

**Free Tier (Current Weather API 2.5):**
- ✅ Current weather data (1,000 calls/day)
- ✅ 5-day forecast with 3-hour intervals  
- ✅ Geocoding API
- ✅ No credit card required

**⚠️ Important:** This app uses free-tier endpoints only. One Call API 3.0 requires a separate paid subscription.

### Step 1: Get OpenWeatherMap API Key

1. **Sign up** at [OpenWeatherMap](https://openweathermap.org/)
2. **Verify your email** (REQUIRED for API key activation)
3. **Navigate** to [API Keys](https://home.openweathermap.org/api_keys)
4. **Copy** your default API key (automatically created)

**⏱️ Activation Time:** New API keys take **10 minutes to 2 hours** to activate after email verification.

### Step 2: Configure Environment Variable

1. **Copy** the example environment file:
   ```bash
   cd client
   cp .env.example .env
   ```

2. **Edit** `.env` file and add your API key:
   ```env
   VITE_OPENWEATHER_API_KEY=your_actual_api_key_here
   ```

3. **Restart** the development server (required for Vite to load .env):
   ```bash
   npm run dev
   ```

### Step 3: Verify Setup

1. Open http://localhost:5173
2. Check the weather widget on the dashboard
3. Look for real weather data for Ahmedabad, India
4. Click the refresh button to fetch latest data

## Fallback Behavior

If no API key is configured, the widget will:
- Display **mock weather data**
- Show a **console warning** in browser DevTools
- Continue functioning with placeholder information

## Customization

### Change Default Location

Edit [`src/components/WeatherWidget.jsx`](../src/components/WeatherWidget.jsx):

```javascript
const [location, setLocation] = useState({ 
    city: 'YourCity',    // Change this
    country: 'CountryCode'  // e.g., 'IN' for India, 'US' for USA
});
```

### Add Location Selector

You can add a dropdown or input field to let users change the location dynamically.

## API Usage & Limits

### Free Tier (Current)
- **Calls per day:** 1,000
- **Current weather:** ✅ Included
- **5-day forecast:** ✅ Included (3-hour intervals)
- **Rate limit:** 60 calls/minute

### API Endpoints Used

1. **Current Weather:**
   ```
   GET https://api.openweathermap.org/data/2.5/weather
   ```

2. **Geocoding (for coordinates):**
   ```
   GET http://api.openweathermap.org/geo/1.0/direct
   ```

3. **5-Day Forecast:**
   ```
   GET https://api.openweathermap.org/data/2.5/forecast
   ```

## Troubleshooting

### Problem: 401 Unauthorized Error

**Symptoms:**
- Console shows "❌ API Key Error: Invalid or inactive API key"
- Weather data not loading
- DevTools Network tab shows 401 status

**Solutions:**
1. **Email Verification:** Check your email and verify your OpenWeatherMap account
2. **Wait for Activation:** New API keys take 10 minutes to 2 hours to activate
3. **Check API Key Status:**
   - Visit [API Keys Dashboard](https://home.openweathermap.org/api_keys)
   - Ensure key shows "Active" status (green indicator)
4. **Verify .env Configuration:**
   ```bash
   # Check .env file exists in client/ directory
   cat client/.env
   # Should show: VITE_OPENWEATHER_API_KEY=your_key_here
   ```
5. **Restart Dev Server:**
   ```bash
   # Stop current server (Ctrl+C)
   npm run dev
   ```

### Problem: "Loading weather data..." stuck

**Solutions:**
1. Check if API key is correctly set in `.env`
2. Open browser console (F12) to see error messages
3. Check DevTools Network tab for API request status
4. Ensure internet connection is active
5. Try the test script:
   ```bash
   node testWeatherAPI.js
   ```

### Problem: API key not working

**Solutions:**
1. Verify `.env` file is in `client/` directory (not root)
2. Check variable name is exactly: `VITE_OPENWEATHER_API_KEY`
3. No spaces around the `=` sign
4. No quotes around the API key value
5. Restart dev server after adding/changing `.env`
6. Clear browser cache and reload page

### Problem: Wrong location showing

**Solutions:**
1. Update location in `WeatherWidget.jsx`
2. Ensure city name is spelled correctly
3. Use proper country code (ISO 3166-1 alpha-2)
4. Example valid codes: `IN` (India), `US` (USA), `GB` (UK)

## File Structure

```
client/
├── .env                          # Your API key (DO NOT COMMIT)
├── .env.example                  # Template file
├── src/
│   ├── components/
│   │   └── WeatherWidget.jsx    # Main widget component
│   ├── services/
│   │   └── weatherService.js    # API integration logic
│   └── styles/
│       └── weather-widget.css   # Widget styles
```

## Security Notes

⚠️ **Important:**
- Never commit `.env` file to Git
- `.env` is already in `.gitignore`
- Share API keys only through secure channels
- Regenerate API key if accidentally exposed

## Support

For OpenWeatherMap API issues:
- [API Documentation](https://openweathermap.org/api)
- [FAQ](https://openweathermap.org/faq)
- [Support](https://openweathermap.org/support)

For FasalMitra project issues:
- Check `START_GUIDE.md` in project root
- Contact team lead

---

**Last Updated:** February 4, 2026
