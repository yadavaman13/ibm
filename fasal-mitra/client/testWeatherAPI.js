/**
 * Test script to verify OpenWeatherMap API integration
 * Tests free-tier endpoints: Current Weather API 2.5, Geocoding, and 5-Day Forecast
 * 
 * Setup: Create a .env file with VITE_OPENWEATHER_API_KEY=your_key_here
 * Run: node testWeatherAPI.js
 * 
 * Expected Results:
 * ✅ All 3 tests pass: API key is active and working
 * ❌ 401 errors: API key not activated yet (wait up to 2 hours)
 * ❌ Other errors: Check API key validity
 */

// Load environment variables from .env file
require('dotenv').config();

const API_KEY = process.env.VITE_OPENWEATHER_API_KEY;

async function testCurrentWeather() {
    console.log('\n🌤️  Testing Current Weather API...');
    
    try {
        const response = await fetch(
            `https://api.openweathermap.org/data/2.5/weather?q=Ahmedabad,IN&units=metric&appid=${API_KEY}`
        );
        
        if (!response.ok) {
            throw new Error(`API Error: ${response.status} - ${response.statusText}`);
        }
        
        const data = await response.json();
        console.log('✅ Current Weather API - SUCCESS');
        console.log(`   City: ${data.name}, ${data.sys.country}`);
        console.log(`   Temperature: ${Math.round(data.main.temp)}°C`);
        console.log(`   Condition: ${data.weather[0].main} - ${data.weather[0].description}`);
        console.log(`   Humidity: ${data.main.humidity}%`);
        console.log(`   Wind Speed: ${Math.round(data.wind.speed * 3.6)} km/h`);
        return true;
    } catch (error) {
        console.log('❌ Current Weather API - FAILED');
        console.error('   Error:', error.message);
        return false;
    }
}

async function testGeocodingAPI() {
    console.log('\n📍 Testing Geocoding API...');
    
    try {
        const response = await fetch(
            `https://api.openweathermap.org/geo/1.0/direct?q=Ahmedabad,IN&limit=1&appid=${API_KEY}`
        );
        
        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }
        
        const data = await response.json();
        if (data && data.length > 0) {
            console.log('✅ Geocoding API - SUCCESS');
            console.log(`   Location: ${data[0].name}, ${data[0].country}`);
            console.log(`   Coordinates: ${data[0].lat}, ${data[0].lon}`);
            return data[0];
        }
        throw new Error('No location data found');
    } catch (error) {
        console.log('❌ Geocoding API - FAILED');
        console.error('   Error:', error.message);
        return null;
    }
}

async function testForecastAPI(lat, lon) {
    console.log('\n📅 Testing Forecast API...');
    
    try {
        const response = await fetch(
            `https://api.openweathermap.org/data/2.5/forecast?lat=${lat}&lon=${lon}&units=metric&appid=${API_KEY}`
        );
        
        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('✅ Forecast API - SUCCESS');
        console.log(`   Location: ${data.city.name}`);
        console.log(`   Forecast entries: ${data.list.length}`);
        console.log(`   Next forecast: ${data.list[0].dt_txt}`);
        console.log(`   Temp: ${Math.round(data.list[0].main.temp)}°C`);
        return true;
    } catch (error) {
        console.log('❌ Forecast API - FAILED');
        console.error('   Error:', error.message);
        return false;
    }
}

async function runTests() {
    console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('  OpenWeatherMap API Integration Test');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    
    if (!API_KEY) {
        console.log('❌ ERROR: API key not found!');
        console.log('   Please ensure VITE_OPENWEATHER_API_KEY is set in .env file\n');
        return;
    }
    
    console.log(`  API Key: ${API_KEY.substring(0, 8)}...${API_KEY.substring(API_KEY.length - 4)}`);
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    
    const test1 = await testCurrentWeather();
    const geoData = await testGeocodingAPI();
    const test3 = geoData ? await testForecastAPI(geoData.lat, geoData.lon) : false;
    
    console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('  Test Results:');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log(`  Current Weather: ${test1 ? '✅ PASS' : '❌ FAIL'}`);
    console.log(`  Geocoding:       ${geoData ? '✅ PASS' : '❌ FAIL'}`);
    console.log(`  Forecast:        ${test3 ? '✅ PASS' : '❌ FAIL'}`);
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    
    if (test1 && geoData && test3) {
        console.log('🎉 All tests passed! Weather widget is ready to use.\n');
        console.log('Next steps:');
        console.log('1. Restart dev server: npm run dev');
        console.log('2. Open http://localhost:5173');
        console.log('3. Check weather widget shows real data\n');
    } else {
        console.log('⚠️  Some tests failed. Troubleshooting:\n');
        if (!test1 || !geoData || !test3) {
            console.log('401 Unauthorized Error Solutions:');
            console.log('├─ 1. Verify email confirmation');
            console.log('├─ 2. Check API key status: https://home.openweathermap.org/api_keys');
            console.log('├─ 3. Wait up to 2 hours for new key activation');
            console.log('├─ 4. Ensure key shows "Active" status (green)');
            console.log('└─ 5. Try generating a new API key if issue persists\n');
        }
    }
}

runTests();
