/**
 * Soil Analysis Service
 * API integration for soil data, suitability checks, and crop recommendations
 */

const API_BASE_URL = 'http://localhost:8000/api/v1';

/**
 * Get soil data for a specific state
 * @param {string} state - State name
 * @returns {Promise<Object>} Soil composition (N, P, K, pH)
 */
export const getSoilData = async (state) => {
    try {
        const response = await fetch(`${API_BASE_URL}/soil/data/${encodeURIComponent(state)}`);
        
        if (!response.ok) {
            throw new Error(`Failed to fetch soil data: ${response.status}`);
        }
        
        const result = await response.json();
        // Backend returns { success, message, data: { ... } }
        return result.data || {};
    } catch (error) {
        console.error('Error fetching soil data:', error);
        throw error;
    }
};

/**
 * Check soil suitability for a specific crop
 * @param {Object} data - { state: string, crop: string }
 * @returns {Promise<Object>} Suitability score and analysis
 */
export const checkSoilSuitability = async (data) => {
    try {
        // Backend expects query parameters, not JSON body
        const params = new URLSearchParams({
            state: data.state,
            crop: data.crop
        });
        
        const response = await fetch(`${API_BASE_URL}/soil/suitability?${params}`, {
            method: 'POST'
        });
        
        if (!response.ok) {
            throw new Error(`Failed to check suitability: ${response.status}`);
        }
        
        const result = await response.json();
        // Backend returns { success, message, data: { ... } }
        return result.data || {};
    } catch (error) {
        console.error('Error checking soil suitability:', error);
        throw error;
    }
};

/**
 * Get recommended crops for a state's soil
 * @param {string} state - State name
 * @returns {Promise<Object>} Recommended crops data
 */
export const getRecommendedCrops = async (state) => {
    try {
        const response = await fetch(`${API_BASE_URL}/soil/recommendations/${encodeURIComponent(state)}`);
        
        if (!response.ok) {
            throw new Error(`Failed to fetch recommendations: ${response.status}`);
        }
        
        const result = await response.json();
        // Backend returns { success, message, data: { ... } }
        return result.data || {};
    } catch (error) {
        console.error('Error fetching crop recommendations:', error);
        throw error;
    }
};

/**
 * Get list of available crops
 * @returns {Promise<Array>} List of crop names
 */
export const getCrops = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/yield/crops`);
        
        if (!response.ok) {
            throw new Error(`Failed to fetch crops: ${response.status}`);
        }
        
        const result = await response.json();
        // Backend returns { success, message, data: { crops: [...] } }
        return result.data?.crops || [];
    } catch (error) {
        console.error('Error fetching crops:', error);
        throw error;
    }
};

/**
 * Get list of available states
 * @returns {Promise<Array>} List of state names
 */
export const getStates = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/yield/states`);
        
        if (!response.ok) {
            throw new Error(`Failed to fetch states: ${response.status}`);
        }
        
        const result = await response.json();
        // Backend returns { success, message, data: { states: [...] } }
        return result.data?.states || [];
    } catch (error) {
        console.error('Error fetching states:', error);
        throw error;
    }
};

/**
 * Check if backend server is running
 * @returns {Promise<boolean>} Server health status
 */
export const checkServerHealth = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        return response.ok;
    } catch (error) {
        console.error('Server health check failed:', error);
        return false;
    }
};
