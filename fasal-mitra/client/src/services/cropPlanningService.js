/**
 * Crop Planning Service
 * 
 * API calls for crop recommendation engine
 */

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const BASE_URL = `${API_URL}/api/v1/crop-planning`;

/**
 * Get crop recommendations
 */
export const planCrops = async (planningData) => {
    try {
        const response = await fetch(`${BASE_URL}/plan`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(planningData),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error planning crops:', error);
        throw error;
    }
};

/**
 * Get all season information
 */
export const getSeasons = async () => {
    try {
        const response = await fetch(`${BASE_URL}/seasons`);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching seasons:', error);
        throw error;
    }
};

/**
 * Get details for a specific crop
 */
export const getCropDetails = async (cropName) => {
    try {
        const response = await fetch(`${BASE_URL}/crops/${encodeURIComponent(cropName)}`);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error(`Error fetching crop details for ${cropName}:`, error);
        throw error;
    }
};

/**
 * Get market prices for a crop
 */
export const getMarketPrices = async (cropName, state = null) => {
    try {
        const url = state 
            ? `${BASE_URL}/market-prices/${encodeURIComponent(cropName)}?state=${encodeURIComponent(state)}`
            : `${BASE_URL}/market-prices/${encodeURIComponent(cropName)}`;

        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error(`Error fetching market prices for ${cropName}:`, error);
        throw error;
    }
};

/**
 * Check server health for crop planning service
 */
export const checkCropPlanningHealth = async () => {
    try {
        const response = await fetch(`${API_URL}/api/v1/health`);
        return response.ok;
    } catch (error) {
        console.error('Crop planning service health check failed:', error);
        return false;
    }
};

/**
 * Generate AI-powered crop analysis using backend Gemini integration
 */
export const generateCropAnalysis = async (analysisData) => {
    try {
        const response = await fetch(`${API_URL}/api/v1/ai/crop-analysis`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                crop: analysisData.crop,
                country: analysisData.country,
                state: analysisData.state,
                district: analysisData.district,
                month_name: analysisData.monthName,
                season: analysisData.season,
                land_size: analysisData.land_size
            }),
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error generating AI crop analysis:', error);
        throw error;
    }
};
