import React, { useState, useEffect } from 'react';
import { MapPin, RefreshCw } from 'lucide-react';
import { getCurrentWeather, getWeeklyForecast, getAirQuality } from '../services/weatherService';
import '../styles/weather-widget.css';

const WeatherWidget = () => {
    const [isCelsius, setIsCelsius] = useState(true);
    const [location, setLocation] = useState({ city: 'Ahmedabad', country: 'IN' });
    const [currentWeather, setCurrentWeather] = useState(null);
    const [weeklyForecast, setWeeklyForecast] = useState([]);
    const [airQuality, setAirQuality] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Fetch weather data
    const fetchWeatherData = async () => {
        setLoading(true);
        setError(null);
        
        try {
            const [current, forecast, aqi] = await Promise.all([
                getCurrentWeather(location.city, location.country),
                getWeeklyForecast(location.city, location.country),
                getAirQuality()
            ]);

            setCurrentWeather(current);
            setWeeklyForecast(forecast);
            setAirQuality(aqi);
        } catch (err) {
            console.error('Error fetching weather data:', err);
            setError('Unable to fetch weather data');
        } finally {
            setLoading(false);
        }
    };

    // Fetch data on component mount and location change
    useEffect(() => {
        fetchWeatherData();
    }, [location]);

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
                                onClick={fetchWeatherData}
                                disabled={loading}
                                title="Refresh weather data"
                            >
                                <RefreshCw className={`weather-refresh-icon ${loading ? 'weather-refresh-spinning' : ''}`} />
                            </button>
                        </div>
                        <p className="weather-datetime">{getFormattedDateTime()}</p>
                        <p className="weather-condition">
                            {currentWeather?.condition || 'Loading...'}
                            <span className="weather-location">
                                <MapPin className="weather-location-icon" />
                                {location.city}
                            </span>
                        </p>
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
