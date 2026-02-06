/**
 * Weather Service - OpenWeatherMap API Integration
 * 
 * API Tier: Free Tier (Current Weather API 2.5)
 * Documentation: https://openweathermap.org/current
 * Forecast Documentation: https://openweathermap.org/forecast5
 * 
 * Free Tier Includes:
 * - Current weather data (1,000 calls/day)
 * - 5-day forecast with 3-hour step
 * - Geocoding API
 * 
 * Note: One Call API 3.0 requires separate "One Call by Call" subscription
 * 
 * Required API Key: Get from https://home.openweathermap.org/api_keys
 * Set in .env file: VITE_OPENWEATHER_API_KEY=your_api_key_here
 * 
 * API Key Activation: New keys may take up to 2 hours to activate after creation
 */

const API_KEY = import.meta.env.VITE_OPENWEATHER_API_KEY || '';
const BASE_URL = 'https://api.openweathermap.org/data/2.5';
const GEO_URL = 'https://api.openweathermap.org/geo/1.0';

// Cache configuration
const CACHE_DURATION = 30 * 60 * 1000; // 30 minutes in milliseconds
const CACHE_KEY_CURRENT = 'fasalmitra_weather_current';
const CACHE_KEY_FORECAST = 'fasalmitra_weather_forecast';
const CACHE_KEY_TIMESTAMP = 'fasalmitra_weather_timestamp';

/**
 * Check if cached data is still valid
 * @returns {boolean} True if cache is fresh (< 30 minutes old)
 */
const isCacheValid = () => {
    const timestamp = localStorage.getItem(CACHE_KEY_TIMESTAMP);
    if (!timestamp) return false;
    
    const age = Date.now() - parseInt(timestamp);
    return age < CACHE_DURATION;
};

/**
 * Get cached weather data if available and fresh
 * @returns {Object|null} Cached weather data or null
 */
export const getCachedWeather = () => {
    if (!isCacheValid()) return null;
    
    try {
        const current = localStorage.getItem(CACHE_KEY_CURRENT);
        const forecast = localStorage.getItem(CACHE_KEY_FORECAST);
        const timestamp = localStorage.getItem(CACHE_KEY_TIMESTAMP);
        
        if (current && forecast) {
            return {
                current: JSON.parse(current),
                forecast: JSON.parse(forecast),
                timestamp: parseInt(timestamp)
            };
        }
    } catch (error) {
        console.error('Error reading cache:', error);
    }
    
    return null;
};

/**
 * Store weather data in cache with timestamp
 * @param {Object} current - Current weather data
 * @param {Array} forecast - Weekly forecast data
 */
export const setCachedWeather = (current, forecast) => {
    try {
        const timestamp = Date.now();
        localStorage.setItem(CACHE_KEY_CURRENT, JSON.stringify(current));
        localStorage.setItem(CACHE_KEY_FORECAST, JSON.stringify(forecast));
        localStorage.setItem(CACHE_KEY_TIMESTAMP, timestamp.toString());
    } catch (error) {
        console.error('Error setting cache:', error);
    }
};

/**
 * Clear all cached weather data
 */
export const clearWeatherCache = () => {
    localStorage.removeItem(CACHE_KEY_CURRENT);
    localStorage.removeItem(CACHE_KEY_FORECAST);
    localStorage.removeItem(CACHE_KEY_TIMESTAMP);
};

/**
 * Get cache age in minutes
 * @returns {number|null} Age in minutes or null if no cache
 */
export const getCacheAge = () => {
    const timestamp = localStorage.getItem(CACHE_KEY_TIMESTAMP);
    if (!timestamp) return null;
    
    const age = Date.now() - parseInt(timestamp);
    return Math.floor(age / 60000); // Convert to minutes
};

/**
 * Get current weather for a location
 * @param {string} city - City name (e.g., "Ahmedabad")
 * @param {string} countryCode - Country code (e.g., "IN")
 * @returns {Promise<Object>} Weather data
 */
export const getCurrentWeather = async (city = 'Ahmedabad', countryCode = 'IN') => {
    if (!API_KEY) {
        console.error('❌ OpenWeather API key not found in environment variables');
        console.warn('⚠️  Using mock data. Add VITE_OPENWEATHER_API_KEY to .env file');
        return getMockCurrentWeather();
    }

    try {
        const response = await fetch(
            `${BASE_URL}/weather?q=${city},${countryCode}&units=metric&appid=${API_KEY}`
        );

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            if (response.status === 401) {
                console.error('❌ API Key Error: Invalid or inactive API key');
            } else if (response.status === 404) {
                console.error(`❌ City "${city}" not found`);
            } else {
                console.error(`❌ Weather API Error: ${response.status}`);
            }
            throw new Error(`API Error: ${response.status}`);
        }

        const data = await response.json();
        return parseCurrentWeather(data);
    } catch (error) {
        console.error('⚠️  Falling back to mock weather data');
        return getMockCurrentWeather();
    }
};

/**
 * Get 7-day weather forecast for a location
 * @param {string} city - City name
 * @param {string} countryCode - Country code
 * @returns {Promise<Object>} Forecast data
 */
export const getWeeklyForecast = async (city = 'Ahmedabad', countryCode = 'IN') => {
    if (!API_KEY) {
        console.warn('OpenWeather API key not found. Using mock data.');
        return getMockWeeklyForecast();
    }

    try {
        // First get coordinates for the city using Geocoding API
        const geoResponse = await fetch(
            `${GEO_URL}/direct?q=${city},${countryCode}&limit=1&appid=${API_KEY}`
        );
        
        if (!geoResponse.ok) {
            const errorData = await geoResponse.json().catch(() => ({}));
            if (geoResponse.status === 401) {
                console.error('❌ Geocoding API: Invalid API key');
            }
            throw new Error(`Geocoding Error: ${geoResponse.status}`);
        }
        
        const geoData = await geoResponse.json();
        
        if (!geoData || geoData.length === 0) {
            console.error(`❌ Location "${city}, ${countryCode}" not found`);
            throw new Error('City not found');
        }

        const { lat, lon } = geoData[0];

        // Get 5-day forecast (free tier - provides 40 forecasts in 3-hour intervals)
        const response = await fetch(
            `${BASE_URL}/forecast?lat=${lat}&lon=${lon}&units=metric&appid=${API_KEY}`
        );

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            console.error(`❌ Forecast API Error: ${response.status} - ${errorData.message || response.statusText}`);
            throw new Error(`Forecast Error: ${response.status}`);
        }

        const data = await response.json();
        return parseWeeklyForecast(data);
    } catch (error) {
        console.error('⚠️  Falling back to mock forecast data');
        return getMockWeeklyForecast();
    }
};

/**
 * Parse OpenWeatherMap current weather response
 */
const parseCurrentWeather = (data) => {
    const weatherIcon = getWeatherIcon(data.weather[0].id, data.weather[0].icon);
    
    // Get precipitation data (rain or snow in last hour)
    let precipitation = 0;
    if (data.rain && data.rain['1h']) {
        precipitation = Math.round(data.rain['1h']); // Rain in mm
    } else if (data.snow && data.snow['1h']) {
        precipitation = Math.round(data.snow['1h']); // Snow in mm
    }
    
    return {
        temp: Math.round(data.main.temp),
        tempF: Math.round((data.main.temp * 9/5) + 32),
        feelsLike: Math.round(data.main.feels_like),
        condition: data.weather[0].main,
        description: data.weather[0].description,
        icon: weatherIcon,
        humidity: data.main.humidity,
        windSpeed: Math.round(data.wind.speed * 3.6), // m/s to km/h
        pressure: data.main.pressure,
        visibility: Math.round(data.visibility / 1000), // meters to km
        clouds: data.clouds.all,
        precipitation: precipitation, // Rain/snow in mm
        timestamp: new Date(data.dt * 1000)
    };
};

/**
 * Parse OpenWeatherMap 5-day forecast response to get daily data
 * Free tier provides 5-day forecast with 3-hour intervals (40 data points)
 */
const parseWeeklyForecast = (data) => {
    const dailyData = {};
    
    // Group forecasts by day (YYYY-MM-DD)
    data.list.forEach(item => {
        const date = new Date(item.dt * 1000);
        const dateKey = date.toLocaleDateString('en-US', { year: 'numeric', month: '2-digit', day: '2-digit' });
        const dayName = date.toLocaleDateString('en-US', { weekday: 'short' });
        
        if (!dailyData[dateKey]) {
            dailyData[dateKey] = {
                day: dayName,
                date: date,
                temps: [],
                icons: [],
                weatherIds: [],
                conditions: [],
                humidity: [],
                windSpeed: [],
                precipitation: [],
                fullData: [] // Store full item data
            };
        }
        
        dailyData[dateKey].temps.push(item.main.temp);
        dailyData[dateKey].weatherIds.push(item.weather[0].id);
        dailyData[dateKey].icons.push(item.weather[0].icon);
        dailyData[dateKey].conditions.push(item.weather[0].main);
        dailyData[dateKey].humidity.push(item.main.humidity);
        dailyData[dateKey].windSpeed.push(item.wind.speed);
        
        // Extract precipitation
        let precip = 0;
        if (item.rain && item.rain['3h']) {
            precip = item.rain['3h'];
        } else if (item.snow && item.snow['3h']) {
            precip = item.snow['3h'];
        }
        dailyData[dateKey].precipitation.push(precip);
        dailyData[dateKey].fullData.push(item);
    });

    // Convert to array and ensure we have 7 days (pad with estimates if needed)
    const forecastDays = Object.values(dailyData).map(day => {
        const high = Math.round(Math.max(...day.temps));
        const low = Math.round(Math.min(...day.temps));
        const icon = getMostCommonIcon(day.weatherIds, day.icons);
        
        // Calculate averages for detailed view
        const avgTemp = Math.round(day.temps.reduce((a, b) => a + b, 0) / day.temps.length);
        const avgHumidity = Math.round(day.humidity.reduce((a, b) => a + b, 0) / day.humidity.length);
        const avgWindSpeed = Math.round((day.windSpeed.reduce((a, b) => a + b, 0) / day.windSpeed.length) * 3.6); // m/s to km/h
        const totalPrecipitation = Math.round(day.precipitation.reduce((a, b) => a + b, 0));
        
        // Get most common condition
        const conditionCounts = {};
        day.conditions.forEach(c => {
            conditionCounts[c] = (conditionCounts[c] || 0) + 1;
        });
        const condition = Object.keys(conditionCounts).reduce((a, b) => 
            conditionCounts[a] > conditionCounts[b] ? a : b
        );
        
        return {
            day: day.day,
            date: day.date,
            high,
            low,
            icon,
            // Detailed data for when day is clicked
            temp: avgTemp,
            tempF: Math.round((avgTemp * 9/5) + 32),
            condition: condition,
            humidity: avgHumidity,
            windSpeed: avgWindSpeed,
            precipitation: totalPrecipitation,
            timestamp: day.date
        };
    });

    // Pad to 7 days if we have fewer (extend pattern from last day)
    while (forecastDays.length < 7) {
        const lastDay = forecastDays[forecastDays.length - 1];
        const daysOfWeek = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
        const currentDayIndex = daysOfWeek.indexOf(lastDay.day);
        const nextDayIndex = (currentDayIndex + 1) % 7;
        
        // Create next day's date
        const nextDate = new Date(lastDay.date);
        nextDate.setDate(nextDate.getDate() + 1);
        
        forecastDays.push({
            day: daysOfWeek[nextDayIndex],
            date: nextDate,
            high: lastDay.high,
            low: lastDay.low,
            icon: lastDay.icon,
            // Copy detailed data from last day for padding
            temp: lastDay.temp,
            tempF: lastDay.tempF,
            condition: lastDay.condition,
            humidity: lastDay.humidity,
            windSpeed: lastDay.windSpeed,
            precipitation: lastDay.precipitation,
            timestamp: nextDate
        });
    }

    return forecastDays.slice(0, 7);
};

/**
 * Get weather icon emoji based on OpenWeatherMap condition code
 */
const getWeatherIcon = (weatherId, iconCode) => {
    const iconMap = {
        // Thunderstorm
        2: '⛈️',
        // Drizzle
        3: '🌧️',
        // Rain
        5: '🌧️',
        // Snow
        6: '❄️',
        // Atmosphere (mist, fog, etc.)
        7: '🌫️',
        // Clear
        800: iconCode.includes('d') ? '☀️' : '🌙',
        // Clouds
        801: iconCode.includes('d') ? '⛅' : '☁️',
        802: '☁️',
        803: '☁️',
        804: '☁️'
    };

    // Check for exact match
    if (iconMap[weatherId]) {
        return iconMap[weatherId];
    }

    // Check for range match (e.g., 200-299 for thunderstorm)
    const range = Math.floor(weatherId / 100);
    return iconMap[range] || '☀️';
};

/**
 * Get most common weather icon from a list
 */
const getMostCommonIcon = (weatherIds, icons) => {
    // Count occurrences
    const counts = {};
    weatherIds.forEach((id, index) => {
        const key = `${id}_${icons[index]}`;
        counts[key] = (counts[key] || 0) + 1;
    });

    // Find most common
    let maxCount = 0;
    let mostCommon = weatherIds[0];
    let mostCommonIconCode = icons[0];
    
    Object.keys(counts).forEach(key => {
        if (counts[key] > maxCount) {
            maxCount = counts[key];
            const [id, iconCode] = key.split('_');
            mostCommon = parseInt(id);
            mostCommonIconCode = iconCode;
        }
    });

    return getWeatherIcon(mostCommon, mostCommonIconCode);
};

/**
 * Mock data for when API key is not available
 */
const getMockCurrentWeather = () => ({
    temp: 28,
    tempF: 82,
    feelsLike: 30,
    condition: 'Sunny',
    description: 'clear sky',
    icon: '☀️',
    humidity: 31,
    windSpeed: 10,
    pressure: 1013,
    visibility: 10,
    clouds: 0,
    precipitation: 0,
    timestamp: new Date()
});

const getMockWeeklyForecast = () => [
    { day: 'Wed', icon: '☀️', high: 29, low: 20 },
    { day: 'Thu', icon: '☀️', high: 30, low: 20 },
    { day: 'Fri', icon: '☀️', high: 31, low: 19 },
    { day: 'Sat', icon: '☀️', high: 30, low: 18 },
    { day: 'Sun', icon: '☀️', high: 30, low: 18 },
    { day: 'Mon', icon: '☀️', high: 29, low: 18 },
    { day: 'Tue', icon: '☀️', high: 29, low: 18 }
];

/**
 * Get air quality index from OpenWeather Air Pollution API
 * @param {number} lat - Latitude (required)
 * @param {number} lon - Longitude (required)
 * @returns {Object|null} Air quality data with AQI and category, or null if coordinates not provided
 */
export const getAirQuality = async (lat, lon) => {
    // Return null if no coordinates provided
    if (!lat || !lon) {
        console.warn('⚠️ Air Quality: No coordinates provided');
        return null;
    }
    
    if (!API_KEY) {
        console.warn('⚠️ Air Quality: No API key');
        return null;
    }

    try {
        const url = `${BASE_URL}/air_pollution?lat=${lat}&lon=${lon}&appid=${API_KEY}`;
        console.log(`🌬️ Fetching Air Quality for coordinates: ${lat}, ${lon}`);
        
        const response = await fetch(url);

        if (!response.ok) {
            console.error(`❌ Air Quality API Error: ${response.status}`);
            throw new Error(`API Error: ${response.status}`);
        }

        const data = await response.json();
        console.log('Air Quality API Response:', data);
        
        if (data.list && data.list.length > 0) {
            const aqi = data.list[0].main.aqi;
            
            // Map AQI scale (1-5) to categories
            const categories = {
                1: { category: 'Good', color: 'green' },
                2: { category: 'Fair', color: 'lightgreen' },
                3: { category: 'Moderate', color: 'yellow' },
                4: { category: 'Poor', color: 'orange' },
                5: { category: 'Very Poor', color: 'red' }
            };
            
            const aqiInfo = categories[aqi] || categories[3];
            
            const result = {
                aqi: aqi,
                category: aqiInfo.category,
                color: aqiInfo.color,
                components: data.list[0].components // PM2.5, PM10, etc.
            };
            
            console.log(`✅ Air Quality: ${result.aqi} (${result.category})`);
            return result;
        }
        
        throw new Error('No air quality data available');
    } catch (error) {
        console.error('❌ Error fetching air quality data:', error.message);
        return null;
    }
};
