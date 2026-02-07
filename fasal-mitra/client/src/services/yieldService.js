/**
 * Yield Prediction API Service
 * Handles all API calls to the backend yield prediction endpoints
 */

const API_BASE_URL = import.meta.env.VITE_API_URL ? `${import.meta.env.VITE_API_URL.replace(/\/$/, '')}/api/v1` : 'http://localhost:8000/api/v1';
console.log('🌾 Yield Service - Using API URL:', API_BASE_URL);

/**
 * Predict crop yield
 * @param {Object} data - Prediction request data
 * @returns {Promise<Object>} Prediction response
 */
export const predictYield = async (data) => {
    const response = await fetch(`${API_BASE_URL}/yield/predict`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();

    if (!response.ok) {
        throw new Error(result.message || `HTTP error! status: ${response.status}`);
    }

    return result;
};

/**
 * Get yield benchmarks
 * @param {Object} data - Benchmark request data
 * @returns {Promise<Object>} Benchmark response
 */
export const getYieldBenchmarks = async (data) => {
    const response = await fetch(`${API_BASE_URL}/yield/benchmarks`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();

    if (!response.ok) {
        throw new Error(result.message || `HTTP error! status: ${response.status}`);
    }

    return result;
};

/**
 * Analyze yield gap
 * @param {Object} data - Gap analysis request data
 * @returns {Promise<Object>} Gap analysis response
 */
export const analyzeYieldGap = async (data) => {
    const response = await fetch(`${API_BASE_URL}/yield/gap-analysis`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();

    if (!response.ok) {
        throw new Error(result.message || `HTTP error! status: ${response.status}`);
    }

    return result;
};

/**
 * Check if backend server is available
 * @returns {Promise<boolean>} True if server is available
 */
export const checkServerHealth = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/health`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        return response.ok;
    } catch (error) {
        return false;
    }
};
