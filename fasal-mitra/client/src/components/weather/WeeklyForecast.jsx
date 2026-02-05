import React from 'react';
import { useTranslation } from 'react-i18next';
import { Sun, Cloud, CloudRain, Snowflake, Zap, CloudDrizzle, Moon } from 'lucide-react';

const WeeklyForecast = ({ weeklyForecast, isCelsius }) => {
  const { t } = useTranslation('common');
  // Get appropriate weather icon
  const getWeatherIcon = (condition, isNight = false) => {
    if (isNight) {
      return <Moon className="weather-forecast-icon" />;
    }
    
    if (!condition) return <Sun className="weather-forecast-icon" />;
    
    const conditionLower = condition.toLowerCase();
    
    if (conditionLower.includes('rain') || conditionLower.includes('drizzle')) {
      return <CloudRain className="weather-forecast-icon" />;
    }
    if (conditionLower.includes('cloud')) {
      return <Cloud className="weather-forecast-icon" />;
    }
    if (conditionLower.includes('snow')) {
      return <Snowflake className="weather-forecast-icon" />;
    }
    if (conditionLower.includes('thunder') || conditionLower.includes('storm')) {
      return <Zap className="weather-forecast-icon" />;
    }
    if (conditionLower.includes('mist') || conditionLower.includes('fog') || conditionLower.includes('haze')) {
      return <CloudDrizzle className="weather-forecast-icon" />;
    }
    
    return <Sun className="weather-forecast-icon" />;
  };

  if (!weeklyForecast || weeklyForecast.length === 0) {
    return (
      <div className="weekly-forecast-card">
        <div className="forecast-loading">
          <p>Loading forecast...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="weekly-forecast-card">
      <div className="forecast-grid">
        {weeklyForecast.map((day, index) => {
          // First day gets highlighted style
          const isToday = index === 0;
          // Some days might be night (you can enhance this logic)
          const isNight = day.condition && day.condition.toLowerCase().includes('night');
          
          return (
            <div 
              key={index} 
              className={`forecast-day ${isToday ? 'forecast-day-today' : ''}`}
            >
              <div className="forecast-day-name">{t(`dayAbbr.${day.day}`, day.day)}</div>
              <div className="forecast-icon-container">
                {getWeatherIcon(day.condition, isNight)}
              </div>
              <div className="forecast-temps">
                <span className="forecast-high">{day.high}°</span>
                <span className="forecast-low">{day.low}°</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default WeeklyForecast;