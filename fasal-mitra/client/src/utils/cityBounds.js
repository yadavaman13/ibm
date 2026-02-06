/**
 * City Bounds Database for Location Validation
 * Contains approximate geographic boundaries for major Indian cities
 */

export const CITY_BOUNDS = [
    // Metro Cities
    { name: 'Mumbai', state: 'Maharashtra', bounds: { minLat: 18.89, maxLat: 19.27, minLng: 72.77, maxLng: 73.03 } },
    { name: 'Delhi', state: 'Delhi', bounds: { minLat: 28.40, maxLat: 28.88, minLng: 76.84, maxLng: 77.35 } },
    { name: 'Bangalore', state: 'Karnataka', bounds: { minLat: 12.83, maxLat: 13.14, minLng: 77.46, maxLng: 77.78 } },
    { name: 'Bengaluru', state: 'Karnataka', bounds: { minLat: 12.83, maxLat: 13.14, minLng: 77.46, maxLng: 77.78 } },
    { name: 'Hyderabad', state: 'Telangana', bounds: { minLat: 17.22, maxLat: 17.56, minLng: 78.25, maxLng: 78.63 } },
    { name: 'Chennai', state: 'Tamil Nadu', bounds: { minLat: 12.83, maxLat: 13.23, minLng: 80.10, maxLng: 80.30 } },
    { name: 'Kolkata', state: 'West Bengal', bounds: { minLat: 22.47, maxLat: 22.65, minLng: 88.30, maxLng: 88.42 } },
    { name: 'Pune', state: 'Maharashtra', bounds: { minLat: 18.41, maxLat: 18.63, minLng: 73.73, maxLng: 73.95 } },
    
    // Gujarat Cities
    { name: 'Ahmedabad', state: 'Gujarat', bounds: { minLat: 22.93, maxLat: 23.13, minLng: 72.48, maxLng: 72.68 } },
    { name: 'Surat', state: 'Gujarat', bounds: { minLat: 21.09, maxLat: 21.26, minLng: 72.73, maxLng: 72.93 } },
    { name: 'Vadodara', state: 'Gujarat', bounds: { minLat: 22.25, maxLat: 22.36, minLng: 73.13, maxLng: 73.24 } },
    { name: 'Rajkot', state: 'Gujarat', bounds: { minLat: 22.24, maxLat: 22.34, minLng: 70.73, maxLng: 70.83 } },
    
    // Rajasthan
    { name: 'Jaipur', state: 'Rajasthan', bounds: { minLat: 26.77, maxLat: 27.03, minLng: 75.68, maxLng: 75.90 } },
    { name: 'Jodhpur', state: 'Rajasthan', bounds: { minLat: 26.20, maxLat: 26.35, minLng: 72.95, maxLng: 73.10 } },
    { name: 'Udaipur', state: 'Rajasthan', bounds: { minLat: 24.52, maxLat: 24.63, minLng: 73.63, maxLng: 73.74 } },
    
    // Uttar Pradesh
    { name: 'Lucknow', state: 'Uttar Pradesh', bounds: { minLat: 26.75, maxLat: 26.95, minLng: 80.80, maxLng: 81.05 } },
    { name: 'Kanpur', state: 'Uttar Pradesh', bounds: { minLat: 26.40, maxLat: 26.52, minLng: 80.27, maxLng: 80.39 } },
    { name: 'Agra', state: 'Uttar Pradesh', bounds: { minLat: 27.13, maxLat: 27.23, minLng: 77.93, maxLng: 78.08 } },
    { name: 'Varanasi', state: 'Uttar Pradesh', bounds: { minLat: 25.26, maxLat: 25.36, minLng: 82.93, maxLng: 83.03 } },
    { name: 'Noida', state: 'Uttar Pradesh', bounds: { minLat: 28.47, maxLat: 28.63, minLng: 77.30, maxLng: 77.43 } },
    
    // Punjab & Haryana
    { name: 'Chandigarh', state: 'Chandigarh', bounds: { minLat: 30.68, maxLat: 30.78, minLng: 76.71, maxLng: 76.81 } },
    { name: 'Amritsar', state: 'Punjab', bounds: { minLat: 31.58, maxLat: 31.68, minLng: 74.82, maxLng: 74.92 } },
    { name: 'Ludhiana', state: 'Punjab', bounds: { minLat: 30.85, maxLat: 30.95, minLng: 75.80, maxLng: 75.90 } },
    { name: 'Gurgaon', state: 'Haryana', bounds: { minLat: 28.40, maxLat: 28.52, minLng: 76.93, maxLng: 77.13 } },
    { name: 'Gurugram', state: 'Haryana', bounds: { minLat: 28.40, maxLat: 28.52, minLng: 76.93, maxLng: 77.13 } },
    { name: 'Faridabad', state: 'Haryana', bounds: { minLat: 28.36, maxLat: 28.46, minLng: 77.27, maxLng: 77.37 } },
    
    // Karnataka
    { name: 'Mysore', state: 'Karnataka', bounds: { minLat: 12.27, maxLat: 12.35, minLng: 76.59, maxLng: 76.69 } },
    { name: 'Mangalore', state: 'Karnataka', bounds: { minLat: 12.86, maxLat: 12.96, minLng: 74.80, maxLng: 74.90 } },
    { name: 'Hubli', state: 'Karnataka', bounds: { minLat: 15.32, maxLat: 15.42, minLng: 75.07, maxLng: 75.17 } },
    
    // Tamil Nadu
    { name: 'Coimbatore', state: 'Tamil Nadu', bounds: { minLat: 10.95, maxLat: 11.08, minLng: 76.90, maxLng: 77.05 } },
    { name: 'Madurai', state: 'Tamil Nadu', bounds: { minLat: 9.88, maxLat: 9.98, minLng: 78.08, maxLng: 78.18 } },
    { name: 'Trichy', state: 'Tamil Nadu', bounds: { minLat: 10.75, maxLat: 10.85, minLng: 78.65, maxLng: 78.75 } },
    
    // Kerala
    { name: 'Kochi', state: 'Kerala', bounds: { minLat: 9.90, maxLat: 10.05, minLng: 76.20, maxLng: 76.35 } },
    { name: 'Thiruvananthapuram', state: 'Kerala', bounds: { minLat: 8.45, maxLat: 8.58, minLng: 76.90, maxLng: 77.05 } },
    { name: 'Kozhikode', state: 'Kerala', bounds: { minLat: 11.22, maxLat: 11.32, minLng: 75.75, maxLng: 75.85 } },
    
    // Maharashtra
    { name: 'Nagpur', state: 'Maharashtra', bounds: { minLat: 21.08, maxLat: 21.20, minLng: 79.00, maxLng: 79.15 } },
    { name: 'Nashik', state: 'Maharashtra', bounds: { minLat: 19.95, maxLat: 20.05, minLng: 73.73, maxLng: 73.83 } },
    { name: 'Aurangabad', state: 'Maharashtra', bounds: { minLat: 19.83, maxLat: 19.93, minLng: 75.28, maxLng: 75.38 } },
    
    // Madhya Pradesh
    { name: 'Indore', state: 'Madhya Pradesh', bounds: { minLat: 22.67, maxLat: 22.77, minLng: 75.80, maxLng: 75.93 } },
    { name: 'Bhopal', state: 'Madhya Pradesh', bounds: { minLat: 23.17, maxLat: 23.30, minLng: 77.35, maxLng: 77.50 } },
    { name: 'Gwalior', state: 'Madhya Pradesh', bounds: { minLat: 26.17, maxLat: 26.27, minLng: 78.15, maxLng: 78.25 } },
    
    // Andhra Pradesh
    { name: 'Visakhapatnam', state: 'Andhra Pradesh', bounds: { minLat: 17.65, maxLat: 17.78, minLng: 83.17, maxLng: 83.35 } },
    { name: 'Vijayawada', state: 'Andhra Pradesh', bounds: { minLat: 16.47, maxLat: 16.55, minLng: 80.58, maxLng: 80.68 } },
    
    // West Bengal
    { name: 'Howrah', state: 'West Bengal', bounds: { minLat: 22.56, maxLat: 22.62, minLng: 88.29, maxLng: 88.37 } },
    { name: 'Durgapur', state: 'West Bengal', bounds: { minLat: 23.50, maxLat: 23.58, minLng: 87.27, maxLng: 87.35 } },
    
    // Bihar
    { name: 'Patna', state: 'Bihar', bounds: { minLat: 25.57, maxLat: 25.67, minLng: 85.08, maxLng: 85.18 } },
    
    // Jharkhand
    { name: 'Ranchi', state: 'Jharkhand', bounds: { minLat: 23.30, maxLat: 23.42, minLng: 85.25, maxLng: 85.37 } },
    { name: 'Jamshedpur', state: 'Jharkhand', bounds: { minLat: 22.77, maxLat: 22.85, minLng: 86.15, maxLng: 86.23 } },
    
    // Odisha
    { name: 'Bhubaneswar', state: 'Odisha', bounds: { minLat: 20.22, maxLat: 20.35, minLng: 85.78, maxLng: 85.88 } },
    { name: 'Cuttack', state: 'Odisha', bounds: { minLat: 20.45, maxLat: 20.52, minLng: 85.85, maxLng: 85.92 } },
    
    // Chhattisgarh
    { name: 'Raipur', state: 'Chhattisgarh', bounds: { minLat: 21.20, maxLat: 21.30, minLng: 81.60, maxLng: 81.70 } },
    
    // Assam
    { name: 'Guwahati', state: 'Assam', bounds: { minLat: 26.10, maxLat: 26.22, minLng: 91.70, maxLng: 91.82 } },
    
    // Uttarakhand
    { name: 'Dehradun', state: 'Uttarakhand', bounds: { minLat: 30.26, maxLat: 30.39, minLng: 77.95, maxLng: 78.10 } },
    
    // Goa
    { name: 'Panaji', state: 'Goa', bounds: { minLat: 15.47, maxLat: 15.52, minLng: 73.80, maxLng: 73.85 } },
];

/**
 * Validate if coordinates fall within a known city's bounds
 * @param {number} latitude - Latitude coordinate
 * @param {number} longitude - Longitude coordinate
 * @returns {Object|null} City object if found, null otherwise
 */
export const getCityFromCoordinates = (latitude, longitude) => {
    for (const city of CITY_BOUNDS) {
        const { bounds } = city;
        if (
            latitude >= bounds.minLat && 
            latitude <= bounds.maxLat &&
            longitude >= bounds.minLng && 
            longitude <= bounds.maxLng
        ) {
            return {
                name: city.name,
                state: city.state,
                latitude,
                longitude
            };
        }
    }
    
    return null;
};

/**
 * Validate if the detected city name matches the coordinates
 * @param {string} cityName - City name from reverse geocoding
 * @param {number} latitude - Latitude coordinate
 * @param {number} longitude - Longitude coordinate
 * @returns {Object} Validation result with isValid flag and detected city
 */
export const validateCityLocation = (cityName, latitude, longitude) => {
    const detectedCity = getCityFromCoordinates(latitude, longitude);
    
    if (!detectedCity) {
        return {
            isValid: false,
            message: 'Location outside known city boundaries',
            detectedCity: null,
            providedCity: cityName
        };
    }
    
    // Normalize city names for comparison
    const normalizeName = (name) => name.toLowerCase().replace(/[^a-z]/g, '');
    const normalizedProvided = normalizeName(cityName);
    const normalizedDetected = normalizeName(detectedCity.name);
    
    // Check if names match (including partial matches)
    const isMatch = 
        normalizedProvided === normalizedDetected ||
        normalizedProvided.includes(normalizedDetected) ||
        normalizedDetected.includes(normalizedProvided);
    
    return {
        isValid: isMatch,
        message: isMatch 
            ? `Location validated: ${detectedCity.name}, ${detectedCity.state}`
            : `Location mismatch: API returned "${cityName}" but coordinates indicate "${detectedCity.name}"`,
        detectedCity,
        providedCity: cityName,
        coordinates: { latitude, longitude }
    };
};

/**
 * Check if a city is in the known cities database
 * @param {string} cityName - City name to check
 * @returns {boolean} True if city is known
 */
export const isKnownCity = (cityName) => {
    const normalized = cityName.toLowerCase().replace(/[^a-z]/g, '');
    return CITY_BOUNDS.some(city => {
        const cityNormalized = city.name.toLowerCase().replace(/[^a-z]/g, '');
        return cityNormalized === normalized || 
               cityNormalized.includes(normalized) || 
               normalized.includes(cityNormalized);
    });
};
