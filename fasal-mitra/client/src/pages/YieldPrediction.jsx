import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { Sprout, TrendingUp, AlertCircle, CheckCircle, Loader, Leaf, Droplets, Bug, Maximize2, PackagePlus, Info } from 'lucide-react';
import { predictYield, checkServerHealth } from '../services/yieldService';
import FieldHelpIcon from '../components/FieldHelpIcon';
import FieldHelpModal from '../components/FieldHelpModal';
import { VoiceSummary } from '../components/voice';
import '../styles/pages.css';
import '../styles/yield-prediction.css';

const YieldPrediction = () => {
    const { t } = useTranslation(['pages', 'common']);
    const [formData, setFormData] = useState({
        crop: '',
        state: '',
        season: '',
        area: '',
        fertilizer: '',
        pesticide: ''
    });
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);
    const [serverStatus, setServerStatus] = useState(null);
    
    // Field help modal state
    const [helpModalOpen, setHelpModalOpen] = useState(false);
    const [helpFieldLabel, setHelpFieldLabel] = useState('');
    const [helpFieldName, setHelpFieldName] = useState('');

    // Check server health on mount
    useEffect(() => {
        const checkHealth = async () => {
            const isHealthy = await checkServerHealth();
            setServerStatus(isHealthy);
        };
        checkHealth();
    }, []);

    // Dropdown options based on backend model
    const crops = ['Rice', 'Wheat', 'Maize', 'Cotton', 'Sugarcane', 'Soybean', 'Groundnut', 'Jowar', 'Bajra', 'Tur'];
    const states = ['Punjab', 'Haryana', 'Uttar Pradesh', 'Maharashtra', 'Gujarat', 'Madhya Pradesh', 'Karnataka', 'Tamil Nadu', 'Andhra Pradesh', 'Telangana'];
    const seasons = ['Kharif', 'Rabi', 'Summer', 'Whole Year', 'Autumn', 'Winter'];

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
        setError(null);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        setResult(null);

        try {
            const requestData = {
                crop: formData.crop,
                state: formData.state,
                season: formData.season,
                area: parseFloat(formData.area),
                fertilizer: parseFloat(formData.fertilizer),
                pesticide: parseFloat(formData.pesticide)
            };

            const data = await predictYield(requestData);

            if (data.success) {
                setResult(data.data);
            } else {
                setError(data.message || 'Failed to get prediction');
            }
        } catch (err) {
            console.error('Error:', err);
            setError(err.message || 'Network error. Please ensure the backend server is running on http://localhost:8000');
        } finally {
            setLoading(false);
        }
    };

    const resetForm = () => {
        setFormData({
            crop: '',
            state: '',
            season: '',
            area: '',
            fertilizer: '',
            pesticide: ''
        });
        setResult(null);
        setError(null);
    };
    
    // Handle help icon click
    const handleHelpClick = (fieldName, fieldLabel) => {
        setHelpFieldName(fieldName);
        setHelpFieldLabel(fieldLabel);
        setHelpModalOpen(true);
    };

    // Get icon for each factor
    const getFactorIcon = (factorName) => {
        const iconMap = {
            'crop': Sprout,
            'N': Leaf,
            'P': Leaf,
            'K': Leaf,
            'pesticide': Bug,
            'area': Maximize2,
            'fertilizer': PackagePlus,
            'avg_temp_c': '🌡️',
            'total_rainfall_mm': Droplets,
            'avg_humidity_percent': Droplets,
            'pH': '⚗️'
        };
        return iconMap[factorName] || Sprout;
    };

    // Get importance color class
    const getImportanceClass = (importance) => {
        if (importance > 0.15) return 'importance-high';
        if (importance > 0.05) return 'importance-medium';
        return 'importance-low';
    };

    // Format factor name for display
    const formatFactorName = (factor) => {
        const nameMap = {
            'crop': 'Crop Type',
            'N': 'Nitrogen (N)',
            'P': 'Phosphorus (P)',
            'K': 'Potassium (K)',
            'pesticide': 'Pesticide',
            'area': 'Farm Area',
            'fertilizer': 'Fertilizer',
            'avg_temp_c': 'Temperature',
            'total_rainfall_mm': 'Rainfall',
            'avg_humidity_percent': 'Humidity',
            'pH': 'Soil pH',
            'state': 'State',
            'season': 'Season'
        };
        return nameMap[factor] || factor;
    };

    return (
        <div className="page-container">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {/* Page Header */}
                <div className="page-header">
                    <div className="flex items-center gap-3 mb-2">
                        <Sprout className="page-icon" />
                        <h1 className="page-header-title">{t('pages:yieldPrediction.title')}</h1>
                    </div>
                    <p className="page-header-subtitle">
                        {t('pages:yieldPrediction.subtitle')}
                    </p>
                    {serverStatus === false && (
                        <div className="server-alert">
                            <AlertCircle className="alert-icon" />
                            <span>Backend server is not running. Please start the server at http://localhost:8000</span>
                        </div>
                    )}
                </div>

                {/* Form Section - Full Width */}
                <div className="yield-form-card">
                    <div className="form-header">
                        <h2 className="yield-card-title">{t('yieldPrediction.farmDetails')}</h2>
                        <p className="yield-card-subtitle">{t('pages:yieldPrediction.farmDetailsSubtitle')}</p>
                    </div>

                    <form onSubmit={handleSubmit} className="yield-form">
                        {/* Two-column input grid */}
                        <div className="form-inputs-grid">
                            {/* Left Column */}
                            <div className="form-column-left">
                                {/* Crop Selection */}
                                <div className="form-group">
                                    <label htmlFor="crop" className="form-label">
                                        Crop Type <span className="required">*</span>
                                        <FieldHelpIcon 
                                            fieldName="crop" 
                                            onClick={() => handleHelpClick('crop', 'Crop Type')} 
                                        />
                                    </label>
                                    <select
                                        id="crop"
                                        name="crop"
                                        value={formData.crop}
                                        onChange={handleInputChange}
                                        required
                                        className="form-select"
                                    >
                                        <option value="">{t('pages:yieldPrediction.selectCrop')}</option>
                                        {crops.map(crop => (
                                            <option key={crop} value={crop}>{t(`common:crops.${crop}`)}</option>
                                        ))}
                                    </select>
                                </div>

                                {/* State Selection */}
                                <div className="form-group">
                                    <label htmlFor="state" className="form-label">
                                        {t('yieldPrediction.state')} <span className="required">*</span>
                                    </label>
                                    <select
                                        id="state"
                                        name="state"
                                        value={formData.state}
                                        onChange={handleInputChange}
                                        required
                                        className="form-select"
                                    >
                                        <option value="">{t('pages:yieldPrediction.selectState')}</option>
                                        {states.map(state => (
                                            <option key={state} value={state}>{t(`common:states.${state}`)}</option>
                                        ))}
                                    </select>
                                </div>

                                {/* Season Selection */}
                                <div className="form-group">
                                    <label htmlFor="season" className="form-label">
                                        Season <span className="required">*</span>
                                        <FieldHelpIcon 
                                            fieldName="season" 
                                            onClick={() => handleHelpClick('season', 'Season')} 
                                        />
                                    </label>
                                    <select
                                        id="season"
                                        name="season"
                                        value={formData.season}
                                        onChange={handleInputChange}
                                        required
                                        className="form-select"
                                    >
                                        <option value="">{t('pages:yieldPrediction.selectSeason')}</option>
                                        {seasons.map(season => (
                                            <option key={season} value={season}>{t(`common:seasons.${season}`)}</option>
                                        ))}
                                    </select>
                                </div>
                            </div>

                            {/* Right Column */}
                            <div className="form-column-right">
                                {/* Area Input */}
                                <div className="form-group">
                                    <label htmlFor="area" className="form-label">
                                        Cultivated Area (hectares) <span className="required">*</span>
                                        <FieldHelpIcon 
                                            fieldName="area" 
                                            onClick={() => handleHelpClick('area', 'Cultivated Area (hectares)')} 
                                        />
                                    </label>
                                    <input
                                        type="number"
                                        id="area"
                                        name="area"
                                        value={formData.area}
                                        onChange={handleInputChange}
                                        required
                                        min="0.01"
                                        step="0.01"
                                        placeholder="e.g., 100"
                                        className="form-input"
                                    />
                                </div>

                                {/* Fertilizer Input */}
                                <div className="form-group">
                                    <label htmlFor="fertilizer" className="form-label">
                                        Fertilizer (kg/hectare) <span className="required">*</span>
                                        <FieldHelpIcon 
                                            fieldName="fertilizer" 
                                            onClick={() => handleHelpClick('fertilizer', 'Fertilizer (kg/hectare)')} 
                                        />
                                    </label>
                                    <input
                                        type="number"
                                        id="fertilizer"
                                        name="fertilizer"
                                        value={formData.fertilizer}
                                        onChange={handleInputChange}
                                        required
                                        min="0"
                                        step="0.1"
                                        placeholder="e.g., 25000"
                                        className="form-input"
                                    />
                                </div>

                                {/* Pesticide Input */}
                                <div className="form-group">
                                    <label htmlFor="pesticide" className="form-label">
                                        Pesticide (kg/hectare) <span className="required">*</span>
                                        <FieldHelpIcon 
                                            fieldName="pesticide" 
                                            onClick={() => handleHelpClick('pesticide', 'Pesticide (kg/hectare)')} 
                                        />
                                    </label>
                                    <input
                                        type="number"
                                        id="pesticide"
                                        name="pesticide"
                                        value={formData.pesticide}
                                        onChange={handleInputChange}
                                        required
                                        min="0"
                                        step="0.1"
                                        placeholder="e.g., 500"
                                        className="form-input"
                                    />
                                </div>
                            </div>
                        </div>

                        {/* Form Actions - Centered below inputs */}
                        <div className="form-actions">
                            <button
                                type="submit"
                                disabled={loading}
                                className="btn-primary"
                            >
                                {loading ? (
                                    <>
                                        <Loader className="btn-icon spin" />
                                        Predicting...
                                    </>
                                ) : (
                                    <>
                                        <TrendingUp className="btn-icon" />
                                        {t('yieldPrediction.predict')}
                                    </>
                                )}
                            </button>
                            <button
                                type="button"
                                onClick={resetForm}
                                className="btn-secondary"
                                disabled={loading}
                            >
                                {t('common.reset')}
                            </button>
                        </div>
                    </form>
                </div>

                {/* Results Section - Match Wireframe Layout */}
                {result && (
                    <>
                        {/* Top Section: 2-Column Layout */}
                        <div className="yield-results-grid">
                            {/* Left Column: Stacked Prediction + Confidence */}
                            <div className="results-left-column">
                                {/* Main Prediction Card */}
                                <div className="yield-card">
                                    <div className="card-header">
                                        <CheckCircle className="header-icon" />
                                        <h3 className="card-title">Prediction Results</h3>
                                    </div>
                                    <div className="prediction-main">
                                        <div className="prediction-label">Predicted Yield</div>
                                        <div className="prediction-value">
                                            {result.predicted_yield.toFixed(2)}
                                            <span className="prediction-unit">tons/hectare</span>
                                        </div>
                                        <div className="prediction-total">
                                            Total Production: <strong>{(result.predicted_yield * parseFloat(formData.area)).toFixed(2)} tons</strong>
                                        </div>
                                    </div>
                                </div>

                                {/* Confidence Card */}
                                {result.confidence_interval && (
                                    <div className="yield-card">
                                        <h3 className="card-title">Confidence Range</h3>
                                        <div className="confidence-grid">
                                            <div className="confidence-item">
                                                <span className="confidence-label">Lower Bound</span>
                                                <span className="confidence-value">{result.confidence_interval.lower.toFixed(2)} t/ha</span>
                                            </div>
                                            <div className="confidence-item">
                                                <span className="confidence-label">Upper Bound</span>
                                                <span className="confidence-value">{result.confidence_interval.upper.toFixed(2)} t/ha</span>
                                            </div>
                                        </div>
                                        <div className="confidence-bar">
                                            <div className="confidence-bar-fill" style={{ width: `${result.model_confidence * 100}%` }}></div>
                                        </div>
                                        <p className="confidence-text">
                                            Model Confidence: {(result.model_confidence * 100).toFixed(1)}%
                                        </p>
                                    </div>
                                )}
                            </div>

                            {/* Right Column: Recommendations Card */}
                            {result.recommendations && result.recommendations.length > 0 && (
                                <div className="yield-card">
                                    <h3 className="card-title">Recommendations</h3>
                                    <ul className="recommendations-list">
                                        {result.recommendations.map((rec, index) => (
                                            <li key={index} className="recommendation-item">
                                                {rec}
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            )}
                        </div>

                        {/* Bottom Section: Full Width Key Factors */}
                        <div className="yield-factors-section">
                            {/* Factors Card */}
                            {result.factors_affecting && result.factors_affecting.length > 0 && (
                                <div className="yield-card">
                                    <h3 className="card-title">Key Factors Influencing Yield</h3>
                                    <p className="card-subtitle">These factors have the most impact on your predicted yield</p>
                                    <div className="factors-list">
                                            {result.factors_affecting.map((factor, index) => {
                                                const Icon = getFactorIcon(factor.factor);
                                                const importance = factor.importance || 0;
                                                const importancePercent = (importance * 100).toFixed(1);
                                                
                                                return (
                                                    <div key={index} className="factor-card">
                                                        <div className="factor-header">
                                                            <div className="factor-icon-wrapper">
                                                                {typeof Icon === 'string' ? (
                                                                    <span className="factor-emoji">{Icon}</span>
                                                                ) : (
                                                                    <Icon className="factor-icon" />
                                                                )}
                                                            </div>
                                                            <div className="factor-info">
                                                                <span className="factor-name">{formatFactorName(factor.factor)}</span>
                                                                <span className="factor-value">{factor.factor}</span>
                                                            </div>
                                                            <div className="factor-importance">
                                                                <span className={`importance-badge ${getImportanceClass(importance)}`}>
                                                                    {importancePercent}%
                                                                </span>
                                                            </div>
                                                        </div>
                                                        <div className="importance-bar">
                                                            <div 
                                                                className={`importance-bar-fill ${getImportanceClass(importance)}`}
                                                                style={{ width: `${importancePercent}%` }}
                                                            >
                                                            </div>
                                                        </div>
                                                    </div>
                                                );
                                            })}
                                        </div>
                                </div>
                            )}
                        </div>
                    </>
                )}

                {/* Voice Summary Section */}
                {result && (
                    <VoiceSummary
                        result={result}
                        resultType="yieldPrediction"
                        title="🎧 Yield Prediction Summary"
                        className="yield-voice-summary"
                        onSpeechStart={() => console.log('Started reading yield prediction summary')}
                        onSpeechEnd={() => console.log('Finished reading yield prediction summary')}
                        onSpeechError={(error) => console.error('Speech error:', error)}
                    />
                )}

                {/* Error Display */}
                {error && (
                    <div className="alert-error">
                        <AlertCircle className="alert-icon" />
                        <div>
                            <h3 className="alert-title">Error</h3>
                            <p className="alert-message">{error}</p>
                        </div>
                    </div>
                )}
            </div>
            
            {/* Field Help Modal */}
            <FieldHelpModal
                isOpen={helpModalOpen}
                onClose={() => setHelpModalOpen(false)}
                fieldLabel={helpFieldLabel}
                fieldName={helpFieldName}
            />
        </div>
    );
};

export default YieldPrediction;
