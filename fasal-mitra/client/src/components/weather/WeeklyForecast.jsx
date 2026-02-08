import React from 'react';
import { useTranslation } from 'react-i18next';
import { Sun, Cloud, CloudRain, Snowflake, Zap, CloudDrizzle, Moon } from 'lucide-react';

const WeeklyForecast = ({ weeklyForecast, isCelsius, loading, selectedDayIndex, onDayClick }) => {
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

  // Show skeleton if loading with no cached data
  if (loading && (!weeklyForecast || weeklyForecast.length === 0)) {
    return (
      <div className="weekly-forecast-card">
        <div className="forecast-grid">
          {[...Array(7)].map((_, index) => (
            <div key={index} className="forecast-day">
              <div className="skeleton skeleton-forecast-day"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  // Show empty forecast cards if no data (but not loading)
  const displayForecast = weeklyForecast && weeklyForecast.length > 0 
    ? weeklyForecast 
    : [
        { day: 'Mon', condition: null, high: '--', low: '--' },
        { day: 'Tue', condition: null, high: '--', low: '--' },
        { day: 'Wed', condition: null, high: '--', low: '--' },
        { day: 'Thu', condition: null, high: '--', low: '--' },
        { day: 'Fri', condition: null, high: '--', low: '--' },
        { day: 'Sat', condition: null, high: '--', low: '--' },
        { day: 'Sun', condition: null, high: '--', low: '--' }
      ];

  return (
    <div className="weekly-forecast-card">
      <div className="forecast-grid">
        {displayForecast.map((day, index) => {
          // First day (today) gets highlighted style when selected OR when showing current weather (selectedDayIndex === null)
          const isToday = index === 0;
          const isTodayAndSelected = isToday && (selectedDayIndex === null || selectedDayIndex === 0);
          const isOtherDaySelected = index !== 0 && selectedDayIndex === index;
          // Some days might be night (you can enhance this logic)
          const isNight = day.condition && day.condition.toLowerCase().includes('night');
          
          return (
            <div 
              key={index} 
              className={`forecast-day ${isTodayAndSelected ? 'forecast-day-today' : ''} ${isOtherDaySelected ? 'forecast-day-selected' : ''}`}
              onClick={() => onDayClick && onDayClick(index)}
              style={{ cursor: 'pointer' }}
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