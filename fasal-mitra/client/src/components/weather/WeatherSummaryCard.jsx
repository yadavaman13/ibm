import React from 'react';
import { useTranslation } from 'react-i18next';
import { MapPin, RefreshCw, Cloud, Sun, CloudRain, Snowflake, Zap, CloudDrizzle, Navigation, Loader, AlertCircle } from 'lucide-react';
import { WeatherStats } from './WeatherStats';

const WeatherSummaryCard = ({ 
  currentWeather,
  airQuality,
  location, 
  isCelsius, 
  onToggleUnit, 
  onRefresh, 
  isRefreshing, 
  lastUpdated,
  getLastUpdatedText,
  getUpdateStatusClass,
  isUsingGeolocation,
  locationLoading,
  locationError,
  onRequestLocation,
  permissionState,
  loading,
  selectedDayIndex
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
    // If showing forecast day, show that day's date
    if (selectedDayIndex !== null && currentWeather?.timestamp) {
      const date = new Date(currentWeather.timestamp);
      const dayName = date.toLocaleString('en-US', { weekday: 'long' });
      const dateStr = date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
      const translatedDay = t(`days.${dayName}`, dayName);
      return `${translatedDay}, ${dateStr}`;
    }
    
    // Current weather - show time
    if (!currentWeather?.timestamp) {
      const date = new Date();
      const dayName = date.toLocaleString('en-US', { weekday: 'long' });
      const time = date.toLocaleString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true });
      const translatedDay = t(`days.${dayName}`, dayName);
      return `${translatedDay} ${time}`;
    }
    
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
      // Keep precipitation in mm (actual rainfall amount)
      precipitation: currentWeather.precipitation
    },
    wind: {
      speed: currentWeather.windSpeed
    },
    // Pass actual air quality data from parent
    airQuality: airQuality
  } : null;
  
  console.log('💨 WeatherSummaryCard passing to WeatherStats:');
  console.log('  - airQuality prop:', airQuality);
  console.log('  - weatherData:', weatherData);

  return (
    <div className="weather-summary-card">
      {/* Header with location and time */}
      <div className="weather-header-info">
        <div className="weather-location-info">
          <MapPin className="weather-location-icon" />
          <span>{location.city}, {location.country}</span>
          {isUsingGeolocation && selectedDayIndex === null && <span className="location-live-badge">live</span>}
          
          {/* Show location button only if permission is not granted and showing current weather */}
          {permissionState !== 'granted' && !isUsingGeolocation && selectedDayIndex === null && (
            <button
              className="location-detect-btn"
              onClick={onRequestLocation}
              disabled={locationLoading}
              title="Use my location"
            >
              {locationLoading ? (
                <>
                  <Loader className="location-detect-icon spinning" size={14} />
                  <span className="location-detect-text">Detecting...</span>
                </>
              ) : (
                <>
                  <Navigation className="location-detect-icon" size={14} />
                  <span className="location-detect-text">Use my location</span>
                </>
              )}
            </button>
          )}
        </div>
        <div className="weather-time">
          {getFormattedDateTime()}
        </div>
      </div>
      
      {/* Location error/info message */}
      {locationError && permissionState === 'denied' && (
        <div className="location-info-message">
          <AlertCircle size={12} />
          <span>{locationError}</span>
        </div>
      )}
      {locationError && permissionState !== 'denied' && (
        <div className="location-error-message">
          <AlertCircle size={12} />
          <span>{locationError}</span>
        </div>
      )}

      {/* Main weather display */}
      <div className="weather-main-display">
        <div className="weather-main-left">
          {loading && !currentWeather ? (
            <>
              <div className="skeleton skeleton-icon"></div>
              <div className="skeleton skeleton-temp"></div>
            </>
          ) : (
            <>
              {getWeatherIcon(currentWeather?.condition, currentWeather?.icon)}
              <span className="weather-temp-value">{currentTemp || '--'}°</span>
            </>
          )}
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
          {currentWeather?.condition ? t(`conditions.${currentWeather.condition}`, currentWeather.condition) : '-'}
        </h3>
        
        {/* Only show "Updated" badge for current weather, not forecast */}
        {lastUpdated && selectedDayIndex === null && (
          <div className="weather-status-badge">
            {getLastUpdatedText()}
          </div>
        )}
      </div>

      {/* Light separator */}
      <div className="weather-separator"></div>

      {/* Weather stats integrated */}
      {loading && !currentWeather ? (
        <div className="weather-stats-grid">
          <div className="weather-stat-item">
            <div className="skeleton skeleton-stat"></div>
          </div>
          <div className="weather-stat-item">
            <div className="skeleton skeleton-stat"></div>
          </div>
          <div className="weather-stat-item">
            <div className="skeleton skeleton-stat"></div>
          </div>
          <div className="weather-stat-item">
            <div className="skeleton skeleton-stat"></div>
          </div>
        </div>
      ) : (
        <WeatherStats weatherData={weatherData} />
      )}
    </div>
  );
};

export default WeatherSummaryCard;