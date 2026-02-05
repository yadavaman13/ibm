/**
 * Field Helper Utilities
 * 
 * Utilities to identify agriculture-related fields and generate
 * contextual help prompts for the chatbot
 */

/**
 * List of agriculture/domain-specific field names
 * These fields will have the help icon
 */
export const AGRICULTURE_FIELDS = new Set([
    // Yield Prediction fields
    'crop', 'season', 'area', 'fertilizer', 'pesticide',
    
    // Soil related
    'soil_type', 'soil_moisture', 'soil_ph', 'nitrogen', 'phosphorus', 'potassium',
    'N', 'P', 'K', 'npk',
    
    // Crop stages and conditions
    'crop_stage', 'crop_health', 'crop_age', 'growth_stage',
    
    // Disease related
    'disease_severity', 'pest_severity', 'leaf_discoloration', 
    'symptoms', 'infection_level',
    
    // Irrigation and water
    'irrigation_method', 'water_source', 'drainage',
    
    // Climate and weather
    'humidity_level', 'temperature', 'rainfall',
    
    // Farming practices
    'tillage_method', 'seed_variety', 'planting_density',
    'harvest_method', 'crop_rotation'
]);

/**
 * Generic fields that should NOT have help icons
 */
export const GENERIC_FIELDS = new Set([
    'state', 'city', 'district', 'village', 'location', 'address',
    'name', 'farmer_name', 'phone', 'phone_number', 'mobile', 'email',
    'id', 'user_id', 'farm_id'
]);

/**
 * Check if a field should have contextual help
 * @param {string} fieldName - The name/id of the input field
 * @returns {boolean} - True if field needs help icon
 */
export const shouldShowHelp = (fieldName) => {
    if (!fieldName) return false;
    
    const normalizedName = fieldName.toLowerCase().trim();
    
    // Don't show for generic fields
    if (GENERIC_FIELDS.has(normalizedName)) {
        return false;
    }
    
    // Show for agriculture-specific fields
    if (AGRICULTURE_FIELDS.has(normalizedName)) {
        return true;
    }
    
    // Check for partial matches (e.g., "soil_moisture_level" contains "soil_moisture")
    for (const agriField of AGRICULTURE_FIELDS) {
        if (normalizedName.includes(agriField)) {
            return true;
        }
    }
    
    return false;
};

/**
 * Generate a farmer-friendly prompt for field explanation
 * @param {string} fieldLabel - The display label of the field
 * @param {string} fieldName - The name/id of the field
 * @returns {string} - Structured prompt for the chatbot
 */
export const generateFieldPrompt = (fieldLabel, fieldName = '') => {
    const cleanLabel = fieldLabel.replace(/\*/g, '').trim(); // Remove required asterisks
    
    return `Explain what "${cleanLabel}" means in very simple language for farmers.

Please include:
1. A clear, beginner-friendly explanation (avoid technical jargon)
2. Practical ways a farmer can find or measure this value manually
3. Why this is important for farming
4. Common values or ranges if applicable
5. Simple tips or recommendations

Keep the explanation short, friendly, and focused on practical farming knowledge.`;
};

/**
 * Get user-friendly field description for display
 * @param {string} fieldName - The name/id of the field
 * @returns {string} - Brief description
 */
export const getFieldDescription = (fieldName) => {
    const descriptions = {
        crop: 'The type of crop you are growing',
        season: 'The agricultural season (Kharif, Rabi, etc.)',
        area: 'Total land area used for cultivation',
        fertilizer: 'Amount of fertilizer applied to the crop',
        pesticide: 'Amount of pesticide used for pest control',
        soil_type: 'Type of soil in your field',
        soil_moisture: 'Water content in the soil',
        soil_ph: 'Acidity or alkalinity level of soil',
        nitrogen: 'Nitrogen content in soil (essential nutrient)',
        phosphorus: 'Phosphorus content in soil (essential nutrient)',
        potassium: 'Potassium content in soil (essential nutrient)',
        irrigation_method: 'How you provide water to crops',
        humidity_level: 'Moisture content in the air',
        crop_stage: 'Current growth phase of the crop',
        pest_severity: 'How serious the pest infestation is',
    };
    
    return descriptions[fieldName.toLowerCase()] || 'Agricultural parameter';
};

/**
 * Format field label for chatbot context
 * @param {string} label - Original label text
 * @returns {string} - Cleaned label
 */
export const cleanFieldLabel = (label) => {
    return label
        .replace(/\*/g, '')           // Remove asterisks
        .replace(/\(.*?\)/g, '')       // Remove content in parentheses
        .trim();
};
