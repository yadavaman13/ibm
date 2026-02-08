/**
 * Soil Analysis Service
 * API integration for soil data, suitability checks, and crop recommendations
 */

const API_BASE_URL = import.meta.env.VITE_API_URL ? `${import.meta.env.VITE_API_URL.replace(/\/$/, '')}/api/v1` : 'http://localhost:8000/api/v1';
console.log('🌱 Soil Service - Using API URL:', API_BASE_URL);

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
 * Check soil suitability for a specific crop with enhanced parameters
 * @param {Object} data - { state: string, crop: string, fieldSize?: number, irrigationType?: string, previousCrop?: string, waterQuality?: string }
 * @returns {Promise<Object>} Enhanced suitability score and analysis
 */
export const checkSoilSuitability = async (data) => {
    try {
        // Backend expects query parameters, not JSON body
        const params = new URLSearchParams({
            state: data.state,
            crop: data.crop
        });
        
        // Add optional enhanced parameters
        if (data.fieldSize) params.append('field_size', data.fieldSize.toString());
        if (data.irrigationType) params.append('irrigation_type', data.irrigationType);
        if (data.previousCrop) params.append('previous_crop', data.previousCrop);
        if (data.waterQuality) params.append('water_quality', data.waterQuality);
        
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

/**
 * Analyze soil using both image and traditional data
 * @param {Object} data - Analysis parameters including image file
 * @returns {Promise<Object>} Combined image and traditional analysis results
 */
export const analyzeSoilWithImage = async (data) => {
    try {
        // Create FormData for multipart/form-data request
        const formData = new FormData();
        
        // Add required fields
        formData.append('state', data.state);
        formData.append('crop', data.crop);
        formData.append('image', data.soilImage);
        
        // Add optional enhanced parameters
        if (data.fieldSize) formData.append('field_size', data.fieldSize.toString());
        if (data.irrigationType) formData.append('irrigation_type', data.irrigationType);
        if (data.previousCrop) formData.append('previous_crop', data.previousCrop);
        if (data.waterQuality) formData.append('water_quality', data.waterQuality);
        
        const response = await fetch(`${API_BASE_URL}/soil/analyze-image`, {
            method: 'POST',
            body: formData
            // Note: Don't set Content-Type header for FormData, browser will set it automatically
        });
        
        if (!response.ok) {
            throw new Error(`Failed to analyze soil image: ${response.status}`);
        }
        
        const result = await response.json();
        return result.data || {};
    } catch (error) {
        console.error('Error in image-based soil analysis:', error);
        throw error;
    }
};
