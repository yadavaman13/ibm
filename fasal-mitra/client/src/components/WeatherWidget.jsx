import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { MapPin, RefreshCw, Info, Navigation, Loader, AlertCircle, Trash2 } from 'lucide-react';
import { 
    getCurrentWeather, 
    getWeeklyForecast, 
    getAirQuality,
    getCachedWeather,
    setCachedWeather,
    getCacheAge,
    clearWeatherCache
} from '../services/weatherService';
import '../styles/weather-widget.css';

const WeatherWidget = () => {
    const { t } = useTranslation('common');
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
    const [locationReady, setLocationReady] = useState(true);
    const [locationLoading, setLocationLoading] = useState(false);
    const [locationError, setLocationError] = useState('');

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
            console.error('❌ Error fetching weather data');
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
        await fetchWeatherDataFromAPI();
        setLoading(false);
    };

    // Handle manual refresh button click
    const handleRefresh = async () => {
        setIsRefreshing(true);
        await fetchWeatherData(true); // Force refresh from API
        setIsRefreshing(false);
    };

    // Clear cache and fetch fresh data
    const handleClearCache = async () => {
        clearWeatherCache();
        setIsRefreshing(true);
        await fetchWeatherData(true);
        setIsRefreshing(false);
    };

    // Manual location detection (triggered by user)
    const requestLocation = () => {
        if (!navigator.geolocation) {
            setLocationError('Geolocation not supported by your browser');
            return;
        }

        setLocationLoading(true);
        setLocationError('');

        navigator.geolocation.getCurrentPosition(
            // Success callback
            async (position) => {
                const { latitude, longitude } = position.coords;
                try {
                    // Use reverse geocoding to get city name from coordinates
                    const response = await fetch(
                        `https://api.openweathermap.org/geo/1.0/reverse?lat=${latitude}&lon=${longitude}&limit=1&appid=${import.meta.env.VITE_OPENWEATHER_API_KEY}`
                    );
                    const data = await response.json();
                    
                    if (data && data.length > 0) {
                        setIsUsingGeolocation(true);
                        setLocation({
                            city: data[0].name,
                            country: data[0].country,
                            lat: latitude,
                            lon: longitude
                        });
                        setLocationError('');
                    } else {
                        setLocationError('Could not determine city from your location');
                    }
                } catch (err) {
                    setLocationError('Failed to get location name');
                } finally {
                    setLocationLoading(false);
                }
            },
            // Error callback
            (error) => {
                let errorMsg = 'Unable to detect your location';
                
                switch(error.code) {
                    case error.PERMISSION_DENIED:
                        errorMsg = 'Location permission denied';
                        break;
                    case error.POSITION_UNAVAILABLE:
                        errorMsg = 'Location information unavailable';
                        break;
                    case error.TIMEOUT:
                        errorMsg = 'Location request timed out';
                        break;
                }
                
                setLocationError(errorMsg);
                setLocationLoading(false);
            },
            // Options
            {
                enableHighAccuracy: true,  // Use GPS for precise location
                timeout: 10000,            // 10 seconds (GPS needs more time)
                maximumAge: 0              // Don't use cached position, get fresh location
            }
        );
    };

    // Initialize with default location on mount
    useEffect(() => {
        // Start with default location immediately
        fetchWeatherData();
    }, []);

    // Fetch data when location changes (user selects new location)
    useEffect(() => {
        if (isUsingGeolocation && location.lat && location.lon) {
            fetchWeatherData(true); // Force refresh with new location
        }
    }, [location.city, location.country]);

    // Format last updated time
    const getLastUpdatedText = () => {
        if (!lastUpdated) return '';
        
        const minutes = Math.floor((Date.now() - lastUpdated) / 60000);
        
        if (minutes < 1) return `${t('updated')} just now`;
        if (minutes === 1) return `${t('updated')} 1 min ${t('ago')}`;
        if (minutes < 60) return `${t('updated')} ${minutes} mins ${t('ago')}`;
        
        const hours = Math.floor(minutes / 60);
        if (hours === 1) return `${t('updated')} 1 hour ${t('ago')}`;
        return `${t('updated')} ${hours} hours ${t('ago')}`;
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
        if (!currentWeather?.timestamp) return t('loading');
        
        const date = new Date(currentWeather.timestamp);
        const dayName = date.toLocaleString('en-US', { weekday: 'long' });
        const time = date.toLocaleString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true });
        
        // Translate the day name
        const translatedDay = t(`days.${dayName}`, dayName);
        
        return `${translatedDay} ${time}`;
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
                            <div className="weather-actions">
                                <button 
                                    className="weather-location-btn"
                                    onClick={requestLocation}
                                    disabled={locationLoading}
                                    title="Use my location"
                                >
                                    {locationLoading ? (
                                        <Loader className="weather-location-icon weather-refresh-spinning" size={16} />
                                    ) : (
                                        <Navigation className="weather-location-icon" size={16} />
                                    )}
                                </button>
                                <button 
                                    className="weather-refresh-btn"
                                    onClick={handleRefresh}
                                    disabled={isRefreshing}
                                    title="Refresh weather data"
                                >
                                    <RefreshCw className={`weather-refresh-icon ${isRefreshing ? 'weather-refresh-spinning' : ''}`} />
                                </button>
                                <button 
                                    className="weather-refresh-btn"
                                    onClick={handleClearCache}
                                    disabled={isRefreshing}
                                    title="Clear cache and reload"
                                >
                                    <Trash2 className="weather-refresh-icon" size={16} />
                                </button>
                            </div>
                        </div>
                        <div className="weather-location-row">
                            <span className="weather-location">
                                <MapPin className="weather-location-icon" />
                                {location.city}, {location.country}
                                {isUsingGeolocation && <span className="location-badge">📍</span>}
                            </span>
                        </div>
                        {locationError && (
                            <div className="weather-location-error">
                                <AlertCircle className="error-icon" size={14} />
                                <span>{locationError}</span>
                            </div>
                        )}
                        <p className="weather-datetime">{getFormattedDateTime()}</p>
                        <p className="weather-condition">
                            {currentWeather?.condition ? t(`conditions.${currentWeather.condition}`, currentWeather.condition) : t('loading')}
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
                                        <div className="weather-forecast-day-label">{t(`dayAbbr.${d.day}`, d.day)}</div>
                                        <div className="weather-forecast-day-icon">{d.icon}</div>
                                        <div className="weather-forecast-day-temps">
                                            <span>{d.high}°</span>
                                            <span className="weather-forecast-day-sep"> </span>
                                            <span>{d.low}°</span>
                                        </div>
                                    </div>
                                ))
                            ) : (
                                <div className="weather-forecast-loading">{t('loading')}</div>
                            )}
                        </div>
                    </div>

                    {/* Right Card - Weather Details */}
                    <div className="weather-details-card">
                        <div className="weather-details-grid">
                            <div className="weather-detail-box">
                                <span className="weather-detail-label">precipitation</span>
                                <span className="weather-detail-value">{currentWeather?.precipitation || 0} mm</span>
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
