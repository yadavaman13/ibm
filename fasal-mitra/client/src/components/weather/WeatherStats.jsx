import React from 'react';
import { useTranslation } from 'react-i18next';

export const WeatherStats = ({ currentWeather, airQuality, weatherData }) => {
  const { t } = useTranslation('common');
  // Handle both old prop structure and new weatherData structure
  const data = weatherData || currentWeather;
  
  // Debug Air Quality data
  console.log('💨 WeatherStats received:');
  console.log('  - airQuality prop:', airQuality);
  console.log('  - weatherData.airQuality:', weatherData?.airQuality);
  
  const formatWindSpeed = (speed) => {
    // Convert from m/s to km/h if needed
    const kmh = typeof speed === 'number' ? Math.round(speed * 3.6) : parseInt(speed) || 24;
    return `${kmh} km/h`;
  };

  const formatAirQuality = (aq) => {
    // Check weatherData structure first
    if (weatherData?.airQuality) {
      const aqi = weatherData.airQuality.aqi;
      const category = weatherData.airQuality.category;
      if (aqi && category) {
        console.log('✅ Displaying AQI from weatherData:', aqi, category);
        return `${aqi} (${category})`;
      }
    }
    // Fallback to direct airQuality prop
    if (airQuality) {
      const aqi = airQuality.aqi;
      const category = airQuality.category;
      if (aqi && category) {
        console.log('✅ Displaying AQI from airQuality prop:', aqi, category);
        return `${aqi} (${category})`;
      }
    }
    console.log('⚠️ No AQI data available');
    return '-';
  };

  const getPrecipitation = () => {
    // Show precipitation in mm (actual rainfall)
    if (weatherData?.main?.precipitation !== undefined && weatherData?.main?.precipitation !== null) {
      return `${weatherData.main.precipitation} mm`;
    }
    if (data?.precipitation !== undefined && data?.precipitation !== null) {
      return `${data.precipitation} mm`;
    }
    return '-';
  };

  const getHumidity = () => {
    if (weatherData?.main?.humidity) return `${weatherData.main.humidity}%`;
    if (data?.humidity) return `${data.humidity}%`;
    return '-';
  };

  const getWindSpeed = () => {
    if (weatherData?.wind?.speed) return formatWindSpeed(weatherData.wind.speed);
    if (data?.windSpeed) return `${data.windSpeed} km/h`;
    return '-';
  };

  return (
    <div className="weather-stats-grid">
      <div className="weather-stat-item">
        <div className="weather-stat-header">
          <img 
            src="/src/assets/precipitation.png" 
            alt="Precipitation" 
            className="weather-stat-icon"
            onError={(e) => {
              // Fallback to a simple div if image fails to load
              e.target.style.display = 'none';
            }}
          />
        </div>
        <p className="weather-stat-value">{getPrecipitation()}</p>
        <p className="weather-stat-label">{t('weather.precipitation')}</p>
      </div>

      <div className="weather-stat-item">
        <div className="weather-stat-header">
          <img 
            src="/src/assets/wind.jpg" 
            alt="Wind Speed" 
            className="weather-stat-icon"
            onError={(e) => {
              e.target.style.display = 'none';
            }}
          />
        </div>
        <p className="weather-stat-value">{getWindSpeed()}</p>
        <p className="weather-stat-label">{t('weather.windSpeed')}</p>
      </div>

      <div className="weather-stat-item">
        <div className="weather-stat-header">
          <img 
            src="/src/assets/humidity.png" 
            alt="Humidity" 
            className="weather-stat-icon"
            onError={(e) => {
              e.target.style.display = 'none';
            }}
          />
        </div>
        <p className="weather-stat-value">{getHumidity()}</p>
        <p className="weather-stat-label">{t('weather.humidity')}</p>
      </div>

      <div className="weather-stat-item">
        <div className="weather-stat-header">
          <img 
            src="/src/assets/air_quality.png" 
            alt="Air Quality" 
            className="weather-stat-icon"
            onError={(e) => {
              e.target.style.display = 'none';
            }}
          />
        </div>
        <p className="weather-stat-value weather-stat-moderate">{formatAirQuality()}</p>
        <p className="weather-stat-label">{t('weather.airQuality')}</p>
      </div>
    </div>
  );
};

export default WeatherStats;