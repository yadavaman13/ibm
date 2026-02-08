/**
 * Market Intelligence Service
 * 
 * Handles API calls for market price forecasting, comparison, and recommendations
 */

const API_BASE_URL = import.meta.env.VITE_API_URL
  ? `${import.meta.env.VITE_API_URL.replace(/\/$/, '')}/api/v1`
  : 'http://localhost:8000/api/v1';

console.log('Market Intelligence Service - Using API URL:', API_BASE_URL);

/**
 * Get all available commodities
 */
export const getAvailableCommodities = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/market/commodities`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const result = await response.json();
    return result.data;
  } catch (error) {
    console.error('Error fetching commodities:', error);
    throw error;
  }
};

/**
 * Get price forecast for a commodity
 * @param {string} commodity - Commodity name
 * @param {number} days - Number of days to forecast (default: 7)
 * @param {string} district - Optional district filter
 */
export const getPriceForecast = async (commodity, days = 7, district = null) => {
  try {
    const response = await fetch(`${API_BASE_URL}/market/forecast`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        commodity,
        days,
        district,
      }),
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }
    
    const result = await response.json();
    return result.data;
  } catch (error) {
    console.error('Error fetching forecast:', error);
    throw error;
  }
};

/**
 * Compare markets for a commodity
 * @param {string} commodity - Commodity name
 * @param {string} date - Optional date (YYYY-MM-DD)
 * @param {string} district - Optional district filter
 * @param {string} variety - Optional variety filter
 */
export const compareMarkets = async (commodity, date = null, district = null, variety = null) => {
  try {
    const response = await fetch(`${API_BASE_URL}/market/compare`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        commodity,
        date,
        district,
        variety,
      }),
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }
    
    const result = await response.json();
    return result.data;
  } catch (error) {
    console.error('Error comparing markets:', error);
    throw error;
  }
};

/**
 * Get market recommendation for selling
 * @param {string} commodity - Commodity name
 * @param {string} userDistrict - User's current district
 * @param {number} quantity - Quantity in Metric Tonnes
 */
export const getMarketRecommendation = async (commodity, userDistrict = null, quantity = null) => {
  try {
    const response = await fetch(`${API_BASE_URL}/market/recommend`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        commodity,
        user_district: userDistrict,
        quantity,
      }),
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }
    
    const result = await response.json();
    return result.data;
  } catch (error) {
    console.error('Error fetching recommendation:', error);
    throw error;
  }
};

/**
 * Get comprehensive insights for a commodity
 * @param {string} commodity - Commodity name
 * @param {number} days - Number of recent days to analyze
 */
export const getCommodityInsights = async (commodity, days = 30) => {
  try {
    const response = await fetch(
      `${API_BASE_URL}/market/insights/${encodeURIComponent(commodity)}?days=${days}`
    );
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }
    
    const result = await response.json();
    return result.data;
  } catch (error) {
    console.error('Error fetching insights:', error);
    throw error;
  }
};

/**
 * Health check for market intelligence service
 */
export const checkMarketServiceHealth = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/market/health`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const result = await response.json();
    return result.data;
  } catch (error) {
    console.error('Market service health check failed:', error);
    throw error;
  }
};
