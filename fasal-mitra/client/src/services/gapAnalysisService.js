/**
 * Yield Gap Analysis Service
 * API integration for yield gap analysis features
 */

const API_BASE_URL = import.meta.env.VITE_API_URL ? `${import.meta.env.VITE_API_URL.replace(/\/$/, '')}/api/v1` : 'http://localhost:8000/api/v1';
console.log('📊 Gap Analysis Service - Using API URL:', API_BASE_URL);

/**
 * Analyze yield gap - supports both post-harvest and pre-harvest scenarios
 * 
 * Scenario 1 (Post-Harvest): Provide actual_yield
 * Scenario 2 (Pre-Harvest): Provide area, fertilizer, pesticide
 */
export const analyzeYieldGap = async (data) => {
    try {
        const response = await fetch(`${API_BASE_URL}/yield/gap-analysis`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to analyze yield gap');
        }

        const result = await response.json();
        return result.data || {};
    } catch (error) {
        console.error('Error analyzing yield gap:', error);
        throw error;
    }
};

/**
 * Get yield benchmarks for a crop and state
 */
export const getYieldBenchmarks = async (crop, state, season = null) => {
    try {
        const payload = { crop, state };
        if (season) payload.season = season;

        const response = await fetch(`${API_BASE_URL}/yield/benchmarks`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to get benchmarks');
        }

        const result = await response.json();
        return result.data || {};
    } catch (error) {
        console.error('Error getting benchmarks:', error);
        throw error;
    }
};

/**
 * Get available crops
 */
export const getCrops = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/yield/crops`);
        
        if (!response.ok) {
            throw new Error('Failed to fetch crops');
        }

        const result = await response.json();
        return result.data?.crops || [];
    } catch (error) {
        console.error('Error fetching crops:', error);
        throw error;
    }
};

/**
 * Get available states
 */
export const getStates = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/yield/states`);
        
        if (!response.ok) {
            throw new Error('Failed to fetch states');
        }

        const result = await response.json();
        return result.data?.states || [];
    } catch (error) {
        console.error('Error fetching states:', error);
        throw error;
    }
};

/**
 * Get available seasons
 */
export const getSeasons = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/yield/seasons`);
        
        if (!response.ok) {
            throw new Error('Failed to fetch seasons');
        }

        const result = await response.json();
        return result.data?.seasons || [];
    } catch (error) {
        console.error('Error fetching seasons:', error);
        throw error;
    }
};

/**
 * Check server health
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
