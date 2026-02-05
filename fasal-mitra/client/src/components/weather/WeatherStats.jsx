import React from 'react';
import { useTranslation } from 'react-i18next';

export const WeatherStats = ({ currentWeather, airQuality, weatherData }) => {
  const { t } = useTranslation('common');
  // Handle both old prop structure and new weatherData structure
  const data = weatherData || currentWeather;
  
  const formatWindSpeed = (speed) => {
    // Convert from m/s to km/h if needed
    const kmh = typeof speed === 'number' ? Math.round(speed * 3.6) : parseInt(speed) || 24;
    return `${kmh} km/h`;
  };

  const formatAirQuality = (aq) => {
    if (weatherData?.airQuality) {
      return `${weatherData.airQuality.aqi || 103} ${weatherData.airQuality.level || t('weather.moderate')}`;
    }
    if (airQuality) {
      return `${airQuality.aqi || 103} ${airQuality.category || t('weather.moderate')}`;
    }
    return `103 ${t('weather.moderate')}`;
  };

  const getPrecipitation = () => {
    if (weatherData?.main?.precipitation) return `${weatherData.main.precipitation}%`;
    if (data?.clouds) return `${data.clouds}%`;
    return '40%';
  };

  const getHumidity = () => {
    if (weatherData?.main?.humidity) return `${weatherData.main.humidity}%`;
    if (data?.humidity) return `${data.humidity}%`;
    return '49%';
  };

  const getWindSpeed = () => {
    if (weatherData?.wind?.speed) return formatWindSpeed(weatherData.wind.speed);
    if (data?.windSpeed) return `${data.windSpeed} km/h`;
    return '24 km/h';
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