import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import WeatherSummaryCard from './WeatherSummaryCard';
import WeeklyForecast from './WeeklyForecast';
import WeatherStats from './WeatherStats';
import { 
  getCurrentWeather, 
  getWeeklyForecast, 
  getAirQuality,
  getCachedWeather,
  setCachedWeather,
  getCacheAge
} from '../../services/weatherService';
import './weather-dashboard.css';

const WeatherDashboard = () => {
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

  // Fetch data on component mount and location change
  useEffect(() => {
    fetchWeatherData(); // Will check cache first
  }, [location]);

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
    
    if (minutes < 10) return 'status-fresh'; // Green
    if (minutes < 20) return 'status-good'; // Yellow
    return 'status-old'; // Orange
  };

  if (loading && !currentWeather) {
    return (
      <div className="weather-dashboard">
        <div className="dashboard-container">
          <div className="weather-left-column">
            <div className="weather-loading">
              <div className="loading-spinner"></div>
              <p>Loading weather data...</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error && !currentWeather) {
    return (
      <div className="weather-dashboard">
        <div className="dashboard-container">
          <div className="weather-left-column">
            <div className="weather-error">
              <p>Error: {error}</p>
              <button onClick={() => fetchWeatherData(true)} className="retry-btn">
                Try Again
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="weather-dashboard">
      <div className="dashboard-container">
        {/* Weather Cards Column */}
        <div className="weather-left-column">
          {/* Main Weather Card with integrated stats */}
          <WeatherSummaryCard 
            currentWeather={currentWeather}
            location={location}
            isCelsius={isCelsius}
            onToggleUnit={() => setIsCelsius(!isCelsius)}
            onRefresh={handleRefresh}
            isRefreshing={isRefreshing}
            lastUpdated={lastUpdated}
            getLastUpdatedText={getLastUpdatedText}
            getUpdateStatusClass={getUpdateStatusClass}
          />
          
          {/* Weekly Forecast Card */}
          <WeeklyForecast 
            weeklyForecast={weeklyForecast}
            isCelsius={isCelsius}
          />
        </div>
      </div>
    </div>
  );
};

export default WeatherDashboard;