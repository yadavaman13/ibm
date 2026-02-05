import React, { useState, useEffect } from 'react';
import { MapPin, RefreshCw, Info } from 'lucide-react';
import { 
    getCurrentWeather, 
    getWeeklyForecast, 
    getAirQuality,
    getCachedWeather,
    setCachedWeather,
    getCacheAge
} from '../services/weatherService';
import '../styles/weather-widget.css';

const WeatherWidget = () => {
    const [isCelsius, setIsCelsius] = useState(true);
    const [location, setLocation] = useState({ city: 'Ahmedabad', country: 'IN' });
    const [currentWeather, setCurrentWeather] = useState(null);
    const [weeklyForecast, setWeeklyForecast] = useState([]);
    const [airQuality, setAirQuality] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [isRefreshing, setIsRefreshing] = useState(false);
    const [lastUpdated, setLastUpdated] = useState(null);
    const [isUsingGeolocation, setIsUsingGeolocation] = useState(false);
    const [locationReady, setLocationReady] = useState(false);

    // Fetch weather data from API
    const fetchWeatherDataFromAPI = async () => {
        try {
            const [current, forecast, aqi] = await Promise.all([
                getCurrentWeather(location.city, location.country),
                getWeeklyForecast(location.city, location.country),
                getAirQuality()
            ]);

            setCurrentWeather(current);
            setWeeklyForecast(forecast);
            setAirQuality(aqi);
            setLastUpdated(Date.now());
            
            // Cache the data
            setCachedWeather(current, forecast);
            
            return true;
        } catch (err) {
            console.error('Error fetching weather data:', err);
            setError('Unable to fetch weather data');
            return false;
        }
    };

    // Smart fetch: Check cache first, then API if needed
    const fetchWeatherData = async (forceRefresh = false) => {
        setLoading(true);
        setError(null);
        
        // Try to use cached data first (unless force refresh)
        if (!forceRefresh) {
            const cached = getCachedWeather();
            if (cached) {
                console.log('✅ Using cached weather data (age: ' + getCacheAge() + ' mins)');
                setCurrentWeather(cached.current);
                setWeeklyForecast(cached.forecast);
                setLastUpdated(cached.timestamp);
                
                // Still fetch air quality (not cached)
                getAirQuality().then(aqi => setAirQuality(aqi));
                
                setLoading(false);
                return;
            }
        }
        
        // No cache or force refresh - fetch from API
        console.log(forceRefresh ? '🔄 Force refresh from API' : '📡 No cache found, fetching from API');
        await fetchWeatherDataFromAPI();
        setLoading(false);
    };

    // Handle manual refresh button click
    const handleRefresh = async () => {
        setIsRefreshing(true);
        await fetchWeatherData(true); // Force refresh from API
        setIsRefreshing(false);
    };

    // Get user's geolocation on component mount
    useEffect(() => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                // Success callback
                async (position) => {
                    const { latitude, longitude, accuracy } = position.coords;
                    console.log('📍 Geolocation coordinates:', { latitude, longitude, accuracy: accuracy + 'm' });
                    try {
                        // Use reverse geocoding to get city name from coordinates
                        const response = await fetch(
                            `https://api.openweathermap.org/geo/1.0/reverse?lat=${latitude}&lon=${longitude}&limit=1&appid=${import.meta.env.VITE_OPENWEATHER_API_KEY}`
                        );
                        const data = await response.json();
                        
                        if (data && data.length > 0) {
                            console.log('🏙️ Detected city:', data[0].name, ',', data[0].country);
                            setIsUsingGeolocation(true);
                            setLocation({
                                city: data[0].name,
                                country: data[0].country,
                                lat: latitude,
                                lon: longitude
                            });
                        } else {
                            console.log('⚠️ No city found for coordinates, using default');
                        }
                    } catch (err) {
                        console.log('Reverse geocoding failed, using default location');
                    } finally {
                        setLocationReady(true);
                    }
                },
                // Error callback
                (error) => {
                    console.log('Geolocation error:', error.message);
                    // Keep default location (Ahmedabad)
                    setLocationReady(true);
                },
                // Options
                {
                    enableHighAccuracy: true,  // Use GPS for precise location
                    timeout: 10000,            // 10 seconds (GPS needs more time)
                    maximumAge: 0              // Don't use cached position, get fresh location
                }
            );
        } else {
            // Browser doesn't support geolocation
            setLocationReady(true);
        }
    }, []);

    // Fetch data only after location is determined
    useEffect(() => {
        if (locationReady) {
            fetchWeatherData(); // Will check cache first
        }
    }, [location, locationReady]);

    // Format last updated time
    const getLastUpdatedText = () => {
        if (!lastUpdated) return '';
        
        const minutes = Math.floor((Date.now() - lastUpdated) / 60000);
        
        if (minutes < 1) return 'Updated just now';
        if (minutes === 1) return 'Updated 1 min ago';
        if (minutes < 60) return `Updated ${minutes} mins ago`;
        
        const hours = Math.floor(minutes / 60);
        if (hours === 1) return 'Updated 1 hour ago';
        return `Updated ${hours} hours ago`;
    };

    // Get color class based on data age
    const getUpdateStatusClass = () => {
        if (!lastUpdated) return '';
        
        const minutes = Math.floor((Date.now() - lastUpdated) / 60000);
        
        if (minutes < 10) return 'weather-update-fresh'; // Green
        if (minutes < 20) return 'weather-update-good'; // Yellow
        return 'weather-update-old'; // Orange
    };

    // Format date and time
    const getFormattedDateTime = () => {
        if (!currentWeather?.timestamp) return 'Loading...';
        
        const date = new Date(currentWeather.timestamp);
        const options = { weekday: 'long', hour: 'numeric', minute: '2-digit', hour12: true };
        return date.toLocaleString('en-US', options);
    };

    if (loading && !currentWeather) {
        return (
            <div className="weather-widget">
                <div className="weather-widget-container">
                    <div className="weather-loading">
                        <RefreshCw className="weather-loading-icon" />
                        <p>Loading weather data...</p>
                    </div>
                </div>
            </div>
        );
    }

    const currentTemp = isCelsius ? currentWeather?.temp : currentWeather?.tempF;
    const tempUnit = isCelsius ? '°C' : '°F';

    return (
        <div className="weather-widget">
            <div className="weather-widget-container">
                {/* Top Card - Current Weather */}
                <div className="weather-main-card">
                    <div className="weather-main-left">
                        <div className="weather-icon-large">{currentWeather?.icon || '☀️'}</div>
                        <div className="weather-temp-section">
                            <div className="weather-temp-display">
                                <span className="weather-temp-value">{currentTemp || '--'}</span>
                                <button 
                                    className="weather-temp-toggle"
                                    onClick={() => setIsCelsius(!isCelsius)}
                                    title="Toggle temperature unit"
                                >
                                    {tempUnit}
                                </button>
                            </div>
                        </div>
                    </div>
                    <div className="weather-main-right">
                        <div className="weather-title-row">
                            <h2 className="weather-title">Weather</h2>
                            <button 
                                className="weather-refresh-btn"
                                onClick={handleRefresh}
                                disabled={isRefreshing}
                                title="Refresh weather data"
                            >
                                <RefreshCw className={`weather-refresh-icon ${isRefreshing ? 'weather-refresh-spinning' : ''}`} />
                            </button>
                        </div>
                        <div className="weather-location-row">
                            <span className="weather-location">
                                <MapPin className="weather-location-icon" />
                                {location.city}, {location.country}
                            </span>
                            {!isUsingGeolocation && locationReady && (
                                <div className="location-permission-info">
                                    <Info className="info-icon" size={14} />
                                    <span>Allow location to see your weather</span>
                                </div>
                            )}
                        </div>
                        <p className="weather-datetime">{getFormattedDateTime()}</p>
                        <p className="weather-condition">
                            {currentWeather?.condition || 'Loading...'}
                        </p>
                        {lastUpdated && (
                            <span className={`weather-last-updated ${getUpdateStatusClass()}`}>
                                {getLastUpdatedText()}
                            </span>
                        )}
                    </div>
                </div>

                {/* Bottom Cards - Forecast and Details */}
                <div className="weather-bottom-cards">
                    {/* Left Card - 7 Day Forecast */}
                    <div className="weather-forecast-card">
                        <div className="weather-forecast-7days">
                            {weeklyForecast.length > 0 ? (
                                weeklyForecast.map((d, i) => (
                                    <div key={i} className={`weather-forecast-day${i === 0 ? ' weather-forecast-day-active' : ''}`}>
                                        <div className="weather-forecast-day-label">{d.day}</div>
                                        <div className="weather-forecast-day-icon">{d.icon}</div>
                                        <div className="weather-forecast-day-temps">
                                            <span>{d.high}°</span>
                                            <span className="weather-forecast-day-sep"> </span>
                                            <span>{d.low}°</span>
                                        </div>
                                    </div>
                                ))
                            ) : (
                                <div className="weather-forecast-loading">Loading forecast...</div>
                            )}
                        </div>
                    </div>

                    {/* Right Card - Weather Details */}
                    <div className="weather-details-card">
                        <div className="weather-details-grid">
                            <div className="weather-detail-box">
                                <span className="weather-detail-label">precipitation</span>
                                <span className="weather-detail-value">{currentWeather?.clouds || 0}%</span>
                            </div>
                            <div className="weather-detail-box">
                                <span className="weather-detail-label">wind speed</span>
                                <span className="weather-detail-value">{currentWeather?.windSpeed || 0} km/h</span>
                            </div>
                            <div className="weather-detail-box">
                                <span className="weather-detail-label">humidity</span>
                                <span className="weather-detail-value">{currentWeather?.humidity || 0}%</span>
                            </div>
                            <div className="weather-detail-box">
                                <span className="weather-detail-label">Air quality</span>
                                <span className="weather-detail-value">
                                    {airQuality ? `${airQuality.aqi} · ${airQuality.category}` : 'N/A'}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default WeatherWidget;
