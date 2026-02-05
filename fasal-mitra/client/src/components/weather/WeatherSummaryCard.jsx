import React from 'react';
import { useTranslation } from 'react-i18next';
import { MapPin, RefreshCw, Cloud, Sun, CloudRain, Snowflake, Zap, CloudDrizzle } from 'lucide-react';
import { WeatherStats } from './WeatherStats';

const WeatherSummaryCard = ({ 
  currentWeather, 
  location, 
  isCelsius, 
  onToggleUnit, 
  onRefresh, 
  isRefreshing, 
  lastUpdated,
  getLastUpdatedText,
  getUpdateStatusClass 
}) => {
  const { t } = useTranslation('common');
  const currentTemp = isCelsius ? currentWeather?.temp : currentWeather?.tempF;

  // Get weather icon based on condition
  const getWeatherIcon = (condition, iconCode) => {
    if (!condition) return <Sun className="weather-icon-main" />;
    
    const conditionLower = condition.toLowerCase();
    
    if (conditionLower.includes('rain') || conditionLower.includes('drizzle')) {
      return <CloudRain className="weather-icon-main" />;
    }
    if (conditionLower.includes('cloud')) {
      return <Cloud className="weather-icon-main" />;
    }
    if (conditionLower.includes('snow')) {
      return <Snowflake className="weather-icon-main" />;
    }
    if (conditionLower.includes('thunder') || conditionLower.includes('storm')) {
      return <Zap className="weather-icon-main" />;
    }
    if (conditionLower.includes('mist') || conditionLower.includes('fog') || conditionLower.includes('haze') || conditionLower.includes('smoke')) {
      return <CloudDrizzle className="weather-icon-main" />;
    }
    
    return <Sun className="weather-icon-main" />;
  };

  const getFormattedDateTime = () => {
    if (!currentWeather?.timestamp) return t('loading');
    
    const date = new Date(currentWeather.timestamp);
    const dayName = date.toLocaleString('en-US', { weekday: 'long' });
    const time = date.toLocaleString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true });
    
    // Translate the day name
    const translatedDay = t(`days.${dayName}`, dayName);
    
    return `${translatedDay} ${time}`;
  };

  // Create weatherData object compatible with WeatherStats
  const weatherData = currentWeather ? {
    main: {
      humidity: currentWeather.humidity,
      // Convert precipitation from mm to percentage for display
      precipitation: currentWeather.precipitation ? Math.min(100, Math.round(currentWeather.precipitation * 10)) : 0
    },
    wind: {
      speed: currentWeather.windSpeed
    },
    // Add air quality data if available
    airQuality: currentWeather.airQuality || { aqi: 103, level: 'Moderate' }
  } : null;

  return (
    <div className="weather-summary-card">
      {/* Header with location and time */}
      <div className="weather-header-info">
        <div className="weather-location-info">
          <MapPin className="weather-location-icon" />
          <span>{location.city}, {location.country}</span>
        </div>
        <div className="weather-time">
          {getFormattedDateTime()}
        </div>
      </div>

      {/* Main weather display */}
      <div className="weather-main-display">
        <div className="weather-main-left">
          {getWeatherIcon(currentWeather?.condition, currentWeather?.icon)}
          <span className="weather-temp-value">{currentTemp || '--'}°</span>
        </div>
        
        <button 
          className="weather-refresh-btn"
          onClick={onRefresh}
          disabled={isRefreshing}
          title={t('weather.refreshWeather')}
        >
          <RefreshCw className={`weather-refresh-icon ${isRefreshing ? 'weather-refresh-spinning' : ''}`} />
        </button>
      </div>

      {/* Condition and status */}
      <div className="weather-condition-row">
        <h3 className="weather-condition">
          {currentWeather?.condition ? t(`conditions.${currentWeather.condition}`, currentWeather.condition) : t('loading')}
        </h3>
        
        {lastUpdated && (
          <div className="weather-status-badge">
            {getLastUpdatedText()}
          </div>
        )}
      </div>

      {/* Light separator */}
      <div className="weather-separator"></div>

      {/* Weather stats integrated */}
      {weatherData && <WeatherStats weatherData={weatherData} />}
    </div>
  );
};

export default WeatherSummaryCard;