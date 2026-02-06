/**
 * ResultSummaryGenerator - Converts API results into speech-friendly text
 * Supports multiple languages and different result types
 */

class ResultSummaryGenerator {
    constructor() {
        // Language-specific templates for different result types
        this.templates = {
            // Yield Prediction Templates
            yieldPrediction: {
                en: {
                    intro: "Yield prediction results are ready.",
                    prediction: "Based on your inputs for {crop} in {state} during {season} season, the predicted yield is {yield} tons per hectare.",
                    confidence: "The model confidence for this prediction is {confidence} percent.",
                    factors: "Key factors affecting your yield include {factors}.",
                    recommendations: "Here are the recommendations: {recommendations}",
                    conclusion: "This completes your yield prediction summary."
                },
                hi: {
                    intro: "फसल उत्पादन की भविष्यवाणी के परिणाम तैयार हैं।",
                    prediction: "{state} में {season} सीज़न के दौरान {crop} के लिए, अनुमानित उत्पादन {yield} टन प्रति हेक्टेयर है।",
                    confidence: "इस भविष्यवाणी के लिए मॉडल का विश्वास {confidence} प्रतिशत है।",
                    factors: "आपके उत्पादन को प्रभावित करने वाले मुख्य कारक हैं {factors}।",
                    recommendations: "यहाँ सिफारिशें हैं: {recommendations}",
                    conclusion: "यह आपके फसल उत्पादन की भविष्यवाणी का सारांश पूरा करता है।"
                },
                mr: {
                    intro: "पीक उत्पादन अंदाजाचे निकाल तयार आहेत।",
                    prediction: "{state} मध्ये {season} हंगामादरम्यान {crop} साठी तुमच्या इनपुटच्या आधारे, अंदाजित उत्पादन {yield} टन प्रति हेक्टर आहे।",
                    confidence: "या अंदाजासाठी मॉडेलचा विश्वास {confidence} टक्के आहे।",
                    factors: "तुमच्या उत्पादनावर परिणाम करणारे मुख्य घटक आहेत {factors}।",
                    recommendations: "येथे शिफारशी आहेत: {recommendations}",
                    conclusion: "हे तुमच्या पीक उत्पादन अंदाजाचे सारांश पूर्ण करते।"
                },
                gu: {
                    intro: "પાકના ઉત્પાદનની આગાહીના પરિણામો તૈયાર છે।",
                    prediction: "{state}માં {season} મોસમ દરમિયાન {crop} માટે તમારા ઇનપુટના આધારે, અનુમાનિત ઉત્પાદન {yield} ટન પ્રતિ હેક્ટર છે।",
                    confidence: "આ આગાહી માટે મોડેલનો વિશ્વાસ {confidence} ટકા છે।",
                    factors: "તમારા ઉત્પાદનને અસર કરતા મુખ્ય પરિબળો છે {factors}।",
                    recommendations: "અહીં ભલામણો છે: {recommendations}",
                    conclusion: "આ તમારા પાક ઉત્પાદન આગાહીનો સારાંશ પૂર્ણ કરે છે।"
                },
                ta: {
                    intro: "விளைச்சல் கணிப்பு முடிவுகள் தயாராக உள்ளன।",
                    prediction: "{state}இல் {season} பருவத்தில் {crop}க்கான உங்கள் உள்ளீடுகளின் அடிப்படையில், கணித்த விளைச்சல் ஹெக்டேருக்கு {yield} டன்கள் ஆகும்।",
                    confidence: "இந்த கணிப்புக்கான மாதிரியின் நம்பிக்கை {confidence} சதவீதமாக உள்ளது।",
                    factors: "உங்கள் விளைச்சலை பாதிக்கும் முக்கிய காரணிகள் {factors}.",
                    recommendations: "இங்கே பரிந்துரைகள் உள்ளன: {recommendations}",
                    conclusion: "இது உங்கள் விளைச்சல் கணிப்பு சுருக்கத்தை முடிக்கிறது।"
                }
            },

            // Disease Detection Templates  
            diseaseDetection: {
                en: {
                    intro: "Disease detection analysis is complete.",
                    detection: "The analysis has detected {disease} in your {crop} with {confidence} percent confidence.",
                    severity: "The estimated severity level is {severity}.",
                    symptoms: "Common symptoms include {symptoms}.",
                    causes: "This disease is typically caused by {causes}.",
                    treatment: "Recommended treatments are {treatments}.",
                    conclusion: "Please follow the treatment plan for best results."
                },
                hi: {
                    intro: "रोग पहचान विश्लेषण पूरा हो गया है।",
                    detection: "विश्लेषण में आपके {crop} में {confidence} प्रतिशत विश्वास के साथ {disease} का पता चला है।",
                    severity: "अनुमानित गंभीरता का स्तर {severity} है।",
                    symptoms: "सामान्य लक्षणों में शामिल हैं {symptoms}।",
                    causes: "यह रोग आमतौर पर {causes} के कारण होता है।",
                    treatment: "अनुशंसित उपचार हैं {treatments}।",
                    conclusion: "सर्वोत्तम परिणामों के लिए उपचार योजना का पालन करें।"
                },
                mr: {
                    intro: "रोग ओळख विश्लेषण पूर्ण झाले आहे।",
                    detection: "विश्लेषणात तुमच्या {crop} मध्ये {confidence} टक्के विश्वासासह {disease} आढळले आहे।",
                    severity: "अंदाजित तीव्रतेची पातळी {severity} आहे।",
                    symptoms: "सामान्य लक्षणांमध्ये {symptoms} समाविष्ट आहे।",
                    causes: "हा रोग सामान्यतः {causes} मुळे होतो।",
                    treatment: "शिफारस केलेली उपचारपद्धती {treatments} आहे।",
                    conclusion: "सर्वोत्तम परिणामांसाठी उपचार योजनेचे पालन करा।"
                },
                gu: {
                    intro: "રોગ ઓળખ વિશ્લેષણ પૂર્ણ થયું છે।",
                    detection: "વિશ્લેષણે તમારા {crop}માં {confidence} ટકા વિશ્વાસ સાથે {disease} શોધ્યો છે।",
                    severity: "અંદાજિત તીવ્રતાનું સ્તર {severity} છે।",
                    symptoms: "સામાન્ય લક્ષણોમાં {symptoms} સામેલ છે।",
                    causes: "આ રોગ સામાન્ય રીતે {causes} ના કારણે થાય છે।",
                    treatment: "ભલામણ કરાયેલ સારવાર {treatments} છે।",
                    conclusion: "શ્રેષ્ઠ પરિણામો માટે સારવાર યોજનાનું પાલન કરો।"
                },
                ta: {
                    intro: "நோய் கண்டறிதல் பகுப்பாய்வு முடிந்தது.",
                    detection: "பகுப்பாய்வு உங்கள் {crop}இல் {confidence} சதவீத நம்பிக்கையுடன் {disease}ஐ கண்டறிந்துள்ளது.",
                    severity: "மதிப்பிடப்பட்ட தீவிரத்தன்மை நிலை {severity} ஆகும்.",
                    symptoms: "பொதுவான அறிகுறிகளில் {symptoms} அடங்கும்.",
                    causes: "இந்த நோய் பொதுவாக {causes} காரணமாக ஏற்படுகிறது.",
                    treatment: "பரிந்துரைக்கப்பட்ட சிகிச்சைகள் {treatments} ஆகும்.",
                    conclusion: "சிறந்த முடிவுகளுக்கு சிகிச்சை திட்டத்தைப் பின்பற்றவும்."
                }
            },

            // Soil Analysis Templates
            soilAnalysis: {
                en: {
                    intro: "Soil analysis results are available.",
                    suitability: "For {crop} cultivation, your soil suitability score is {score} out of 10.",
                    nutrients: "Main nutrient levels: {nutrients}.",
                    ph: "The soil pH level is {ph}.",
                    recommendations: "Soil improvement recommendations: {recommendations}",
                    conclusion: "Follow these guidelines for optimal soil health."
                }
                // Add other languages for soil analysis...
            }
        };

        // Language names mapping
        this.languageNames = {
            en: 'English',
            hi: 'हिंदी',
            mr: 'मराठी', 
            gu: 'ગુજરાતી',
            ta: 'தமிழ்'
        };
    }

    /**
     * Generate speech summary for yield prediction results
     * @param {Object} result - Yield prediction result object
     * @param {string} language - Language code
     * @returns {string}
     */
    generateYieldPredictionSummary(result, language = 'en') {
        const template = this.templates.yieldPrediction[language] || this.templates.yieldPrediction.en;
        
        const parts = [];
        
        // Intro
        parts.push(template.intro);
        
        // Main prediction
        const predictionText = template.prediction
            .replace('{crop}', result.input_params?.crop || 'the crop')
            .replace('{state}', result.input_params?.state || 'your area')
            .replace('{season}', result.input_params?.season || 'the season')
            .replace('{yield}', result.predicted_yield?.toFixed(2) || 'unknown');
            
        parts.push(predictionText);
        
        // Confidence
        if (result.model_confidence) {
            const confidenceText = template.confidence
                .replace('{confidence}', Math.round(result.model_confidence * 100));
            parts.push(confidenceText);
        }
        
        // Factors affecting yield
        if (result.factors_affecting && result.factors_affecting.length > 0) {
            const factors = result.factors_affecting.map(f => f.factor || f.name || f).join(', ');
            const factorsText = template.factors.replace('{factors}', factors);
            parts.push(factorsText);
        }
        
        // Recommendations
        if (result.recommendations && result.recommendations.length > 0) {
            const recommendations = result.recommendations.slice(0, 3).join('. '); // Limit to 3 recommendations
            const recommendationsText = template.recommendations.replace('{recommendations}', recommendations);
            parts.push(recommendationsText);
        }
        
        // Conclusion
        parts.push(template.conclusion);
        
        return parts.join(' ');
    }

    /**
     * Generate speech summary for disease detection results
     * @param {Object} result - Disease detection result object
     * @param {string} language - Language code
     * @returns {string}
     */
    generateDiseaseDetectionSummary(result, language = 'en') {
        const template = this.templates.diseaseDetection[language] || this.templates.diseaseDetection.en;
        
        const parts = [];
        
        // Intro
        parts.push(template.intro);
        
        // Detection result
        const detectionText = template.detection
            .replace('{disease}', result.detected_disease?.name || 'a disease')
            .replace('{crop}', result.crop_type || 'your crop')
            .replace('{confidence}', Math.round((result.detected_disease?.confidence || 0) * 100));
        
        parts.push(detectionText);
        
        // Severity
        if (result.estimated_severity) {
            const severityText = template.severity.replace('{severity}', result.estimated_severity);
            parts.push(severityText);
        }
        
        // Symptoms
        if (result.detected_disease?.symptoms && result.detected_disease.symptoms.length > 0) {
            const symptoms = result.detected_disease.symptoms.slice(0, 3).join(', ');
            const symptomsText = template.symptoms.replace('{symptoms}', symptoms);
            parts.push(symptomsText);
        }
        
        // Causes
        if (result.detected_disease?.causes && result.detected_disease.causes.length > 0) {
            const causes = result.detected_disease.causes.slice(0, 2).join(' and ');
            const causesText = template.causes.replace('{causes}', causes);
            parts.push(causesText);
        }
        
        // Treatment
        if (result.treatment_plan?.steps && result.treatment_plan.steps.length > 0) {
            const treatments = result.treatment_plan.steps.slice(0, 3).join(', ');
            const treatmentText = template.treatment.replace('{treatments}', treatments);
            parts.push(treatmentText);
        }
        
        // Conclusion
        parts.push(template.conclusion);
        
        return parts.join(' ');
    }

    /**
     * Generate speech summary for soil analysis results - placeholder for future implementation
     * @param {Object} result - Soil analysis result object  
     * @param {string} language - Language code
     * @returns {string}
     */
    generateSoilAnalysisSummary(result, language = 'en') {
        const template = this.templates.soilAnalysis[language] || this.templates.soilAnalysis.en;
        // Implementation will be added when soil analysis results are available
        return template.intro || 'Soil analysis results are available.';
    }

    /**
     * Generate speech summary based on result type
     * @param {Object} result - Result object from any API endpoint
     * @param {string} resultType - Type of result ('yieldPrediction', 'diseaseDetection', 'soilAnalysis')
     * @param {string} language - Language code
     * @returns {string}
     */
    generateSummary(result, resultType, language = 'en') {
        if (!result) {
            return language === 'hi' ? 'परिणाम उपलब्ध नहीं है।' : 
                   language === 'mr' ? 'निकाल उपलब्ध नाही.' :
                   language === 'gu' ? 'પરિણામ ઉપલબ્ધ નથી.' :
                   language === 'ta' ? 'முடிவு கிடைக்கவில்லை.' :
                   'No results available.';
        }

        try {
            switch (resultType) {
                case 'yieldPrediction':
                    return this.generateYieldPredictionSummary(result, language);
                case 'diseaseDetection':
                    return this.generateDiseaseDetectionSummary(result, language);
                case 'soilAnalysis':
                    return this.generateSoilAnalysisSummary(result, language);
                default:
                    return language === 'hi' ? 'परिणाम तैयार हैं।' :
                           language === 'mr' ? 'निकाल तयार आहेत.' :
                           language === 'gu' ? 'પરિણામો તૈયાર છે.' :
                           language === 'ta' ? 'முடிவுகள் தயாராக உள்ளன.' :
                           'Results are ready.';
            }
        } catch (error) {
            console.error('Error generating summary:', error);
            return language === 'hi' ? 'सारांश बनाने में त्रुटि।' :
                   language === 'mr' ? 'सारांश तयार करण्यात त्रुटी.' :
                   language === 'gu' ? 'સારાંશ બનાવવામાં ભૂલ.' :
                   language === 'ta' ? 'சுருக்கம் உருவாக்குவதில் பிழை.' :
                   'Error generating summary.';
        }
    }

    /**
     * Get available languages
     * @returns {Object}
     */
    getAvailableLanguages() {
        return this.languageNames;
    }

    /**
     * Clean text for better speech synthesis
     * @param {string} text - Text to clean
     * @returns {string}
     */
    cleanTextForSpeech(text) {
        return text
            .replace(/\n/g, ' ') // Replace newlines with spaces
            .replace(/\s+/g, ' ') // Replace multiple spaces with single space
            .replace(/[^\w\s.,!?]/g, '') // Remove special characters except basic punctuation
            .trim();
    }
}

// Create singleton instance
const resultSummaryGenerator = new ResultSummaryGenerator();

export default resultSummaryGenerator;