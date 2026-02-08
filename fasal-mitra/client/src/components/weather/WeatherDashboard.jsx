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
import { validateCityLocation, getCityFromCoordinates } from '../../utils/cityBounds';
import './weather-dashboard.css';

const WeatherDashboard = () => {
  const { t } = useTranslation('common');
  const [isCelsius, setIsCelsius] = useState(true);
  const [location, setLocation] = useState({ 
    city: '-', 
    country: '-',
    lat: null,
    lon: null
  });
  const [currentWeather, setCurrentWeather] = useState(null);
  const [weeklyForecast, setWeeklyForecast] = useState([]);
  const [airQuality, setAirQuality] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [lastUpdated, setLastUpdated] = useState(null);
  const [isUsingGeolocation, setIsUsingGeolocation] = useState(false);
  const [locationLoading, setLocationLoading] = useState(false);
  const [locationError, setLocationError] = useState('');
  const [permissionState, setPermissionState] = useState('prompt'); // 'granted', 'prompt', 'denied'
  const [hasCheckedPermission, setHasCheckedPermission] = useState(false);
  const [selectedDayIndex, setSelectedDayIndex] = useState(null); // null = current weather, 0-6 = forecast day
  const [locationValidation, setLocationValidation] = useState(null); // Store validation result

  // Fetch weather data from API
  const fetchWeatherDataFromAPI = async () => {
    // Don't fetch if no valid location
    if (!location.city || location.city === '-' || !location.lat || !location.lon) {
      return false;
    }
    
    try {
      const [current, forecast, aqi] = await Promise.all([
        getCurrentWeather(location.city, location.country),
        getWeeklyForecast(location.city, location.country),
        getAirQuality(location.lat, location.lon)
      ]);

      setCurrentWeather(current);
      setWeeklyForecast(forecast);
      setAirQuality(aqi);
      console.log('💨 Air Quality set in state:', aqi);
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
        setCurrentWeather(cached.current);
        setWeeklyForecast(cached.forecast);
        setLastUpdated(cached.timestamp);
        
        // Fetch air quality with coordinates if available
        if (location.lat && location.lon) {
          getAirQuality(location.lat, location.lon).then(aqi => setAirQuality(aqi));
        }
        
        setLoading(false);
        return;
      }
    }
    
    // No cache or force refresh - fetch from API
    await fetchWeatherDataFromAPI();
    setLoading(false);
  };

  // Handle manual refresh button click - same as location button
  const handleRefresh = async () => {
    // Refresh button does the same as location button:
    // - Requests location permission if not granted
    // - Fetches location if granted
    // - Refreshes weather data
    setSelectedDayIndex(null); // Reset to current weather
    await requestLocation();
  };

  // Handle forecast day click
  const handleDayClick = (index) => {
    // If clicking day 0 (today), show current weather
    if (index === 0) {
      setSelectedDayIndex(null);
    } else {
      setSelectedDayIndex(index);
    }
  };

  // Get the weather data to display (current or selected forecast day)
  const getDisplayWeather = () => {
    if (selectedDayIndex === null) {
      return currentWeather;
    }
    if (weeklyForecast && weeklyForecast[selectedDayIndex]) {
      return weeklyForecast[selectedDayIndex];
    }
    return currentWeather;
  };

  // Get air quality (only available for current weather)
  const getDisplayAirQuality = () => {
    return selectedDayIndex === null ? airQuality : null;
  };

  // Fetch location from coordinates
  const fetchLocationFromCoords = async (latitude, longitude) => {
    try {
      // First, check if coordinates are in a known city
      const detectedCity = getCityFromCoordinates(latitude, longitude);
      
      // Fetch city name from reverse geocoding
      const response = await fetch(
        `https://api.openweathermap.org/geo/1.0/reverse?lat=${latitude}&lon=${longitude}&limit=1&appid=${import.meta.env.VITE_OPENWEATHER_API_KEY}`
      );
      const data = await response.json();
      
      if (data && data.length > 0) {
        setIsUsingGeolocation(true);
        const apiCityName = data[0].name;
        const newLocation = {
          city: apiCityName,
          country: data[0].country,
          lat: latitude,
          lon: longitude
        };
        
        // Validate the location
        const validation = validateCityLocation(apiCityName, latitude, longitude);
        setLocationValidation(validation);
        
        // Log validation result
        if (validation.isValid) {
          console.log(`✅ Location validated: ${apiCityName} matches coordinates`);
        } else {
          console.warn(`⚠️ ${validation.message}`);
          
          // If we detected a different city from coordinates, use that instead
          if (detectedCity) {
            newLocation.city = detectedCity.name;
            console.log(`Using detected city: ${detectedCity.name}, ${detectedCity.state}`);
            setLocationError(`Location adjusted to ${detectedCity.name}`);
            // Clear error after 5 seconds
            setTimeout(() => setLocationError(''), 5000);
          }
        }
        
        setLocation(newLocation);
        setLocationError('');
        setPermissionState('granted');
        
        // Immediately fetch weather data for the new location
        // Don't wait for state update, use the new location directly
        try {
          const [current, forecast, aqi] = await Promise.all([
            getCurrentWeather(newLocation.city, newLocation.country),
            getWeeklyForecast(newLocation.city, newLocation.country),
            getAirQuality(latitude, longitude)
          ]);

          setCurrentWeather(current);
          setWeeklyForecast(forecast);
          setAirQuality(aqi);
          console.log('💨 Air Quality set from location coords:', aqi);
          setLastUpdated(Date.now());
          
          // Cache the data
          setCachedWeather(current, forecast);
        } catch (err) {
          console.error('Error fetching weather data for new location');
          setError('Unable to fetch weather data');
        }
        
        return true;
      } else {
        setLocationError('Could not determine city from your location');
        return false;
      }
    } catch (err) {
      setLocationError('Failed to get location name');
      return false;
    }
  };

  // Get current position (shared logic)
  const getCurrentPosition = () => {
    return new Promise((resolve, reject) => {
      if (!navigator.geolocation) {
        reject(new Error('Geolocation not supported by your browser'));
        return;
      }

      navigator.geolocation.getCurrentPosition(
        (position) => resolve(position),
        (error) => reject(error),
        {
          enableHighAccuracy: true,
          timeout: 10000,
          maximumAge: 0
        }
      );
    });
  };

  // Check permission and auto-fetch location if granted
  const checkPermissionAndFetchLocation = async () => {
    try {
      // Check if Permissions API is supported
      if (!navigator.permissions) {
        setHasCheckedPermission(true);
        setLoading(false); // No location to load
        return;
      }

      const permission = await navigator.permissions.query({ name: 'geolocation' });
      setPermissionState(permission.state);

      // Only auto-fetch if permission is ALREADY granted (not prompt)
      // This means user previously allowed location, so we can auto-detect
      if (permission.state === 'granted') {
        setLocationLoading(true);
        try {
          const position = await getCurrentPosition();
          await fetchLocationFromCoords(position.coords.latitude, position.coords.longitude);
        } catch (err) {
          // Silent fail - don't show error on auto-detect
          setIsUsingGeolocation(false);
        } finally {
          setLocationLoading(false);
          setLoading(false); // Done checking
        }
      } else {
        // Permission is 'prompt' or 'denied' - no location to load yet
        // User will need to click the button
        setLoading(false);
      }

      // Listen for permission changes
      permission.addEventListener('change', () => {
        setPermissionState(permission.state);
        if (permission.state === 'granted') {
          checkPermissionAndFetchLocation();
        }
      });

      setHasCheckedPermission(true);
    } catch (err) {
      // Fallback if Permissions API not supported
      setHasCheckedPermission(true);
      setLoading(false); // Stop loading on error
    }
  };

  // Manual location detection (triggered by user button)
  const requestLocation = async () => {
    if (!navigator.geolocation) {
      setLocationError('Geolocation not supported by your browser');
      // Still refresh with default location
      setIsRefreshing(true);
      await fetchWeatherData(true);
      setIsRefreshing(false);
      return;
    }

    setLocationLoading(true);
    setIsRefreshing(true);
    setLocationError('');

    try {
      const position = await getCurrentPosition();
      await fetchLocationFromCoords(position.coords.latitude, position.coords.longitude);
    } catch (error) {
      let errorMsg = 'Unable to detect your location';
      
      if (error.code === 1) {
        errorMsg = 'Allow location permission to see live weather for your area';
        setPermissionState('denied');
      } else if (error.code === 2) {
        errorMsg = 'Location information unavailable';
      } else if (error.code === 3) {
        errorMsg = 'Location request timed out';
      } else if (error.message) {
        errorMsg = error.message;
      }
      
      setLocationError(errorMsg);
      
      // Still refresh weather with current location (default or last known)
      if (location.city !== '-' && location.lat && location.lon) {
        await fetchWeatherData(true);
      }
    } finally {
      setLocationLoading(false);
      setIsRefreshing(false);
    }
  };

  // Check permission on mount
  useEffect(() => {
    checkPermissionAndFetchLocation();
  }, []);

  // Fetch weather data when location changes (only for manual location changes, not auto-detect)
  useEffect(() => {
    // Only fetch if we have a valid location with coordinates
    if (hasCheckedPermission && location.city !== '-' && location.lat && location.lon) {
      fetchWeatherData(); // Will check cache first for valid location
    }
  }, [hasCheckedPermission]);

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
            currentWeather={getDisplayWeather()}
            airQuality={getDisplayAirQuality()}
            location={location}
            isCelsius={isCelsius}
            onToggleUnit={() => setIsCelsius(!isCelsius)}
            onRefresh={handleRefresh}
            isRefreshing={isRefreshing}
            lastUpdated={lastUpdated}
            getLastUpdatedText={getLastUpdatedText}
            getUpdateStatusClass={getUpdateStatusClass}
            isUsingGeolocation={isUsingGeolocation}
            locationLoading={locationLoading}
            locationError={locationError}
            onRequestLocation={requestLocation}
            permissionState={permissionState}
            loading={loading}
            selectedDayIndex={selectedDayIndex}
          />
          
          {/* Weekly Forecast Card */}
          <WeeklyForecast 
            weeklyForecast={weeklyForecast}
            isCelsius={isCelsius}
            loading={loading}
            selectedDayIndex={selectedDayIndex}
            onDayClick={handleDayClick}
          />
        </div>
      </div>
    </div>
  );
};

export default WeatherDashboard;