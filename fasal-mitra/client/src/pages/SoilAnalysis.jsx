import React, { useState, useEffect, useRef } from 'react';
import { useTranslation } from 'react-i18next';
import { Sprout, Droplets, TestTube, CheckCircle, AlertCircle, Loader, TrendingUp, MapPin, Navigation, Volume2, VolumeX, Play, Pause, Square } from 'lucide-react';
import '../styles/soil-analysis-clean.css';
import * as soilService from '../services/soilService';
import worldIcon from '../assets/744483-removebg-preview.png';

const SoilAnalysis = () => {
    const { t } = useTranslation(['pages', 'common']);
    const [formData, setFormData] = useState({
        state: '',
        crop: ''
    });

    const [states, setStates] = useState([]);
    const [crops, setCrops] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [serverStatus, setServerStatus] = useState(null);
    const [results, setResults] = useState(null);
    
    // Location state
    const [location, setLocation] = useState({ latitude: null, longitude: null });
    const [locationLoading, setLocationLoading] = useState(false);
    const [locationError, setLocationError] = useState(null);
    const [stateAutoDetected, setStateAutoDetected] = useState(false);

    // Load states and crops on mount
    useEffect(() => {
        const loadData = async () => {
            try {
                const [statesData, cropsData, serverHealth] = await Promise.all([
                    soilService.getStates(),
                    soilService.getCrops(),
                    soilService.checkServerHealth()
                ]);
                
                // Service now returns arrays directly
                setStates(statesData);
                setCrops(cropsData);
                setServerStatus(serverHealth);
            } catch (err) {
                console.error('Failed to load initial data:', err);
                setStates([]);
                setCrops([]);
                setServerStatus(false);
            }
        };
        
        loadData();
    }, []);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            // Fetch all data in parallel
            const [soilData, suitabilityData, recommendations] = await Promise.all([
                soilService.getSoilData(formData.state),
                soilService.checkSoilSuitability(formData),
                soilService.getRecommendedCrops(formData.state)
            ]);

            // Services now return the data directly
            setResults({
                soil: soilData,
                suitability: suitabilityData,
                recommendations: recommendations
            });
        } catch (err) {
            setError(err.message || 'Failed to analyze soil. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const resetForm = () => {
        setFormData({ state: '', crop: '' });
        setResults(null);
        setError(null);
        setLocation({ latitude: null, longitude: null });
        setLocationError(null);
        setStateAutoDetected(false);
    };

    // Crop icon mapping
    const getCropIcon = (cropName) => {
        const iconMap = {
            'rice': '🌾',
            'wheat': '🌾', 
            'maize': '🌽',
            'corn': '🌽',
            'cotton': '☁️',
            'sugarcane': '🎋',
            'potato': '🥔',
            'tomato': '🍅',
            'onion': '🧅',
            'soybean': '🫘',
            'groundnut': '🥜',
            'sunflower': '🌻',
            'mustard': '🌿',
            'barley': '🌾',
            'jowar': '🌾',
            'bajra': '🌾',
            'ragi': '🌾',
            'gram': '🫘',
            'arhar': '🫘',
            'moong': '🫘',
            'urad': '🫘',
            'linseed': '🌰',
            'castor': '🌰',
            'sesame': '🌰',
            'coconut': '🥥',
            'banana': '🍌',
            'mango': '🥭',
            'apple': '🍎',
            'orange': '🍊',
            'papaya': '🍈',
            'guava': '🍈',
            'pomegranate': '🍈',
            'grapes': '🍇',
            'watermelon': '🍉',
            'cucumber': '🥒',
            'brinjal': '🍆',
            'okra': '🥒',
            'cabbage': '🥬',
            'cauliflower': '🥬',
            'carrot': '🥕',
            'radish': '🥕',
            'ginger': '🫚',
            'turmeric': '🫚',
            'chili': '🌶️',
            'coriander': '🌿',
            'fenugreek': '🌿',
            'spinach': '🥬'
        };
        
        const normalizedName = cropName.toLowerCase().trim();
        return iconMap[normalizedName] || '🌱';
    };

    // Get suggested crops (mix of popular crops)
    const getSuggestedCrops = () => {
        const popularCrops = ['rice', 'maize', 'cotton', 'sugarcane', 'potato'];
        return popularCrops.filter(crop => 
            crops.some(availableCrop => 
                availableCrop.toLowerCase().includes(crop.toLowerCase())
            )
        ).slice(0, 5);
    };

    // Map coordinates to Indian states
    const getStateFromCoordinates = (latitude, longitude) => {
        const stateData = [
            { name: 'Andhra Pradesh', bounds: { minLat: 12.6, maxLat: 19.9, minLng: 77.0, maxLng: 84.8 } },
            { name: 'Arunachal Pradesh', bounds: { minLat: 26.6, maxLat: 29.5, minLng: 91.2, maxLng: 97.4 } },
            { name: 'Assam', bounds: { minLat: 24.1, maxLat: 28.2, minLng: 89.7, maxLng: 96.0 } },
            { name: 'Bihar', bounds: { minLat: 24.3, maxLat: 27.5, minLng: 83.3, maxLng: 88.1 } },
            { name: 'Chhattisgarh', bounds: { minLat: 17.8, maxLat: 24.1, minLng: 80.3, maxLng: 84.4 } },
            { name: 'Delhi', bounds: { minLat: 28.4, maxLat: 28.9, minLng: 76.8, maxLng: 77.3 } },
            { name: 'Goa', bounds: { minLat: 14.9, maxLat: 15.8, minLng: 73.7, maxLng: 74.3 } },
            { name: 'Gujarat', bounds: { minLat: 20.1, maxLat: 24.7, minLng: 68.2, maxLng: 74.5 } },
            { name: 'Haryana', bounds: { minLat: 27.7, maxLat: 30.9, minLng: 74.4, maxLng: 77.4 } },
            { name: 'Himachal Pradesh', bounds: { minLat: 30.4, maxLat: 33.2, minLng: 75.6, maxLng: 79.0 } },
            { name: 'Jharkhand', bounds: { minLat: 21.9, maxLat: 25.3, minLng: 83.3, maxLng: 87.9 } },
            { name: 'Karnataka', bounds: { minLat: 11.5, maxLat: 18.5, minLng: 74.1, maxLng: 78.6 } },
            { name: 'Kerala', bounds: { minLat: 8.2, maxLat: 12.8, minLng: 74.9, maxLng: 77.4 } },
            { name: 'Madhya Pradesh', bounds: { minLat: 21.1, maxLat: 26.9, minLng: 74.0, maxLng: 82.8 } },
            { name: 'Maharashtra', bounds: { minLat: 15.6, maxLat: 22.0, minLng: 72.6, maxLng: 80.9 } },
            { name: 'Manipur', bounds: { minLat: 23.8, maxLat: 25.7, minLng: 93.0, maxLng: 94.8 } },
            { name: 'Meghalaya', bounds: { minLat: 25.0, maxLat: 26.1, minLng: 89.7, maxLng: 92.8 } },
            { name: 'Mizoram', bounds: { minLat: 21.9, maxLat: 24.6, minLng: 92.2, maxLng: 93.7 } },
            { name: 'Nagaland', bounds: { minLat: 25.2, maxLat: 27.0, minLng: 93.3, maxLng: 95.8 } },
            { name: 'Odisha', bounds: { minLat: 17.8, maxLat: 22.6, minLng: 81.4, maxLng: 87.5 } },
            { name: 'Punjab', bounds: { minLat: 29.5, maxLat: 32.5, minLng: 73.9, maxLng: 76.9 } },
            { name: 'Rajasthan', bounds: { minLat: 23.3, maxLat: 30.1, minLng: 69.5, maxLng: 78.3 } },
            { name: 'Sikkim', bounds: { minLat: 27.0, maxLat: 28.1, minLng: 88.0, maxLng: 88.9 } },
            { name: 'Tamil Nadu', bounds: { minLat: 8.1, maxLat: 13.6, minLng: 76.2, maxLng: 80.3 } },
            { name: 'Telangana', bounds: { minLat: 15.8, maxLat: 19.9, minLng: 77.3, maxLng: 81.8 } },
            { name: 'Tripura', bounds: { minLat: 22.9, maxLat: 24.5, minLng: 91.0, maxLng: 92.7 } },
            { name: 'Uttar Pradesh', bounds: { minLat: 23.9, maxLat: 30.4, minLng: 77.1, maxLng: 84.6 } },
            { name: 'Uttarakhand', bounds: { minLat: 28.4, maxLat: 31.5, minLng: 77.6, maxLng: 81.1 } },
            { name: 'West Bengal', bounds: { minLat: 21.2, maxLat: 27.2, minLng: 85.8, maxLng: 89.9 } },
            { name: 'Jammu and Kashmir', bounds: { minLat: 32.3, maxLat: 37.1, minLng: 73.3, maxLng: 80.3 } },
            { name: 'Ladakh', bounds: { minLat: 32.3, maxLat: 37.1, minLng: 75.9, maxLng: 79.9 } }
        ];

        for (const state of stateData) {
            const { bounds } = state;
            if (latitude >= bounds.minLat && latitude <= bounds.maxLat &&
                longitude >= bounds.minLng && longitude <= bounds.maxLng) {
                
                // Check if this state is available in our states list with better matching
                const normalizedStateName = state.name.toLowerCase().replace(/[^a-z]/g, '');
                const availableState = states.find(s => {
                    const normalizedAvailable = s.toLowerCase().replace(/[^a-z]/g, '');
                    return normalizedAvailable.includes(normalizedStateName) ||
                           normalizedStateName.includes(normalizedAvailable) ||
                           s.toLowerCase() === state.name.toLowerCase();
                });
                
                return availableState || null;
            }
        }
        
        return null;
    };

    // Handle crop suggestion click
    const handleCropSuggestionClick = (suggestedCrop) => {
        // Find the actual crop name from the available crops
        const actualCrop = crops.find(crop => 
            crop.toLowerCase().includes(suggestedCrop.toLowerCase())
        );
        
        if (actualCrop) {
            setFormData(prev => ({ ...prev, crop: actualCrop }));
        }
    };

    const detectLocation = () => {
        if (!navigator.geolocation) {
            setLocationError(t('soilAnalysis.location.errors.notSupported'));
            return;
        }

        setLocationLoading(true);
        setLocationError(null);

        const options = {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 600000 // 10 minutes
        };

        navigator.geolocation.getCurrentPosition(
            (position) => {
                const newLocation = {
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude
                };
                
                setLocation(newLocation);
                setLocationLoading(false);
                
                // Auto-select state based on coordinates
                const detectedState = getStateFromCoordinates(
                    newLocation.latitude, 
                    newLocation.longitude
                );
                
                if (detectedState) {
                    setFormData(prev => ({ ...prev, state: detectedState }));
                    setStateAutoDetected(true);
                    
                    // Clear auto-detection indicator after 3 seconds
                    setTimeout(() => {
                        setStateAutoDetected(false);
                    }, 3000);
                    
                    console.log(`Location detected! Auto-selected state: ${detectedState}`);
                } else {
                    console.log('Location detected but state could not be determined automatically');
                }
                
                setLocationError(null);
            },
            (error) => {
                setLocationLoading(false);
                let errorMessage;
                
                switch (error.code) {
                    case error.PERMISSION_DENIED:
                        errorMessage = t('soilAnalysis.location.errors.permissionDenied');
                        break;
                    case error.POSITION_UNAVAILABLE:
                        errorMessage = t('soilAnalysis.location.errors.unavailable');
                        break;
                    case error.TIMEOUT:
                        errorMessage = t('soilAnalysis.location.errors.timeout');
                        break;
                    default:
                        errorMessage = t('soilAnalysis.location.errors.unknown');
                        break;
                }
                
                setLocationError(errorMessage);
            },
            options
        );
    };

    const getSuitabilityLevel = (score) => {
        if (score >= 80) return { label: 'Excellent', class: 'excellent' };
        if (score >= 60) return { label: 'Good', class: 'good' };
        if (score >= 40) return { label: 'Fair', class: 'fair' };
        return { label: 'Poor', class: 'poor' };
    };

    const getpHLevel = (pH) => {
        if (pH < 6.5) return { label: 'Acidic', class: 'acidic' };
        if (pH <= 7.5) return { label: 'Neutral', class: 'neutral' };
        return { label: 'Alkaline', class: 'alkaline' };
    };

    const getNPKLevel = (value, type) => {
        // Typical NPK ranges (simplified)
        const ranges = {
            N: { low: 200, high: 400 },
            P: { low: 20, high: 50 },
            K: { low: 100, high: 300 }
        };

        const range = ranges[type];
        if (!range) return 50;

        const percentage = ((value - 0) / (range.high * 1.5)) * 100;
        return Math.min(Math.max(percentage, 0), 100);
    };

    return (
        <div className="soil-analysis-page">
            <div className="page-container">
                {/* Clean Page Header */}
                <div className="page-header">
                    <h1 className="page-title">{t('soilAnalysis.title')}</h1>
                    <p className="page-subtitle">
                        {t('soilAnalysis.subtitle')}
                    </p>
                </div>

                {serverStatus === false && (
                    <div className="server-alert">
                        <AlertCircle className="alert-icon" />
                        <span>Backend server is not running. Please start the server at http://localhost:8000</span>
                    </div>
                )}

                {/* Main Form Card */}
                <div className="main-form-card">
                    <form onSubmit={handleSubmit} className="clean-form">
                        
                        {/* Location Detection Section */}
                        <div className="location-detection-section">
                            <div className="location-icon-wrapper">
                                <img src={worldIcon} alt="World Globe" className="world-icon" />
                            </div>
                            <h3 className="location-heading">Allow location access</h3>
                            <p className="location-privacy-text">
                                We use your location only to analyze soil and climate for your region.
                            </p>
                            
                            <button
                                type="button"
                                onClick={detectLocation}
                                disabled={locationLoading}
                                className="get-location-btn"
                            >
                                {locationLoading ? (
                                    <>
                                        <Loader className="btn-icon spin" />
                                        Detecting...
                                    </>
                                ) : (
                                    'Get Location'
                                )}
                            </button>
                            
                            {stateAutoDetected && (
                                <div className="state-detected-msg">
                                    <CheckCircle className="success-icon" />
                                    <span>{t('soilAnalysis.location.stateDetected')}</span>
                                </div>
                            )}
                            
                            {locationError && (
                                <div className="location-error-msg">
                                    <AlertCircle className="error-icon" />
                                    <span>{locationError}</span>
                                </div>
                            )}
                        </div>

                        {/* Form Fields */}
                        <div className="form-fields">
                            {/* Expected State */}
                            <div className="form-field-wrapper">
                                <div className="form-field">
                                    <label className="field-label">Expected State</label>
                                    <select
                                        name="state"
                                        value={formData.state}
                                        onChange={handleInputChange}
                                        required
                                        className="field-input"
                                    >
                                        <option value="">{t('pages:soilAnalysis.selectState')}</option>
                                        {states.map(state => (
                                            <option key={state} value={state}>{t(`common:states.${state}`)}</option>
                                        ))}
                                    </select>
                                </div>
                                
                                {/* Coordinates Display below State */}
                                {location.latitude && location.longitude && (
                                    <div className="coordinates-display-inline">
                                        <span className="coordinate">
                                            <strong>Latitude:</strong> {location.latitude.toFixed(6)}
                                        </span>
                                        <span className="coordinate-separator">|</span>
                                        <span className="coordinate">
                                            <strong>Longitude:</strong> {location.longitude.toFixed(6)}
                                        </span>
                                    </div>
                                )}
                            </div>

                            {/* Analyze Crop */}
                            <div className="form-field-wrapper">
                                <div className="form-field">
                                    <label className="field-label">Analyze Crop</label>
                                    <select
                                        name="crop"
                                        value={formData.crop}
                                        onChange={handleInputChange}
                                        required
                                        className="field-input"
                                    >
                                        <option value="">{t('pages:soilAnalysis.selectCrop')}</option>
                                        {crops.map(crop => (
                                            <option key={crop} value={crop}>{t(`common:crops.${crop}`)}</option>
                                        ))}
                                    </select>
                                </div>
                                
                                {/* Crop Suggestions below Crop dropdown */}
                                <div className="crop-suggestions-inline">
                                    <span className="try-text">Try:</span>
                                    <div className="crop-icons">
                                        {getSuggestedCrops().map((crop) => {
                                            const actualCrop = crops.find(c => c.toLowerCase().includes(crop.toLowerCase()));
                                            const isSelected = actualCrop && formData.crop === actualCrop;
                                            
                                            return (
                                                <div
                                                    key={crop}
                                                    className="crop-suggestion"
                                                >
                                                    <div 
                                                        className={`crop-icon-container ${isSelected ? 'active' : ''}`}
                                                        onClick={() => handleCropSuggestionClick(crop)}
                                                    >
                                                        <div className="crop-icon">{getCropIcon(crop)}</div>
                                                    </div>
                                                    <span className="crop-name">{crop.charAt(0).toUpperCase() + crop.slice(1)}</span>
                                                </div>
                                            );
                                        })}
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Action Buttons */}
                        <div className="action-buttons">
                            <button
                                type="submit"
                                disabled={loading}
                                className="analyze-btn"
                            >
                                {loading ? (
                                    <>
                                        <Loader className="btn-icon spin" />
                                        Analyzing...
                                    </>
                                ) : (
                                    'Analyze Soil'
                                )}
                            </button>
                            <button
                                type="button"
                                onClick={resetForm}
                                className="reset-btn"
                                disabled={loading}
                            >
                                Reset
                            </button>
                        </div>
                    </form>
                </div>

                {/* Error Display */}
                {error && (
                    <div className="error-alert">
                        <AlertCircle className="alert-icon" />
                        <div>
                            <h3 className="alert-title">Error</h3>
                            <p className="alert-message">{error}</p>
                        </div>
                    </div>
                )}

                {/* Results Section */}
                {results && (
                    <>
                        {/* Results content remains the same for now */}
                        <div className="results-grid">
                            {/* Soil Composition Card */}
                            <div className="result-card soil-composition-card">
                                <div className="card-header">
                                    <div className="card-icon-wrapper">
                                        <Droplets className="header-icon" />
                                    </div>
                                    <h3 className="card-title">🌱 Soil Health Report</h3>
                                </div>
                                <p className="card-description">Your soil nutrients analysis</p>

                                <div className="npk-grid">
                                    {/* Nitrogen */}
                                    <div className="npk-item">
                                        <div className="npk-header">
                                            <div className="npk-info">
                                                <span className="npk-label">Nitrogen (N)</span>
                                                <span className="npk-description">For green growth</span>
                                            </div>
                                            <span className="npk-value">{results.soil.N || 0}</span>
                                        </div>
                                        <div className="progress-bar-container">
                                            <div className="progress-bar">
                                                <div
                                                    className="progress-bar-fill nitrogen"
                                                    style={{ width: `${getNPKLevel(results.soil.N || 0, 'N')}%` }}
                                                ></div>
                                            </div>
                                            <span className="nutrient-status">
                                                {getNPKLevel(results.soil.N || 0, 'N') > 60 ? '✅ Good' : 
                                                 getNPKLevel(results.soil.N || 0, 'N') > 30 ? '⚠️ Fair' : '❌ Low'}
                                            </span>
                                        </div>
                                    </div>

                                    {/* Phosphorus */}
                                    <div className="npk-item">
                                        <div className="npk-header">
                                            <div className="npk-info">
                                                <span className="npk-label">Phosphorus (P)</span>
                                                <span className="npk-description">For root strength</span>
                                            </div>
                                            <span className="npk-value">{results.soil.P || 0}</span>
                                        </div>
                                        <div className="progress-bar-container">
                                            <div className="progress-bar">
                                                <div
                                                    className="progress-bar-fill phosphorus"
                                                    style={{ width: `${getNPKLevel(results.soil.P || 0, 'P')}%` }}
                                                ></div>
                                            </div>
                                            <span className="nutrient-status">
                                                {getNPKLevel(results.soil.P || 0, 'P') > 60 ? '✅ Good' : 
                                                 getNPKLevel(results.soil.P || 0, 'P') > 30 ? '⚠️ Fair' : '❌ Low'}
                                            </span>
                                        </div>
                                    </div>

                                    {/* Potassium */}
                                    <div className="npk-item">
                                        <div className="npk-header">
                                            <div className="npk-info">
                                                <span className="npk-label">Potassium (K)</span>
                                                <span className="npk-description">For disease resistance</span>
                                            </div>
                                            <span className="npk-value">{results.soil.K || 0}</span>
                                        </div>
                                        <div className="progress-bar-container">
                                            <div className="progress-bar">
                                                <div
                                                    className="progress-bar-fill potassium"
                                                    style={{ width: `${getNPKLevel(results.soil.K || 0, 'K')}%` }}
                                                ></div>
                                            </div>
                                            <span className="nutrient-status">
                                                {getNPKLevel(results.soil.K || 0, 'K') > 60 ? '✅ Good' : 
                                                 getNPKLevel(results.soil.K || 0, 'K') > 30 ? '⚠️ Fair' : '❌ Low'}
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* Suitability Score Card */}
                            <div className="result-card suitability-card">
                                <div className="card-header">
                                    <div className="card-icon-wrapper">
                                        <TrendingUp className="header-icon" />
                                    </div>
                                    <h3 className="card-title">📊 Crop Suitability</h3>
                                </div>
                                <p className="card-description">How suitable is your soil for {formData.crop}?</p>

                                <div className="suitability-content">
                                    <div className={`score-circle ${getSuitabilityLevel(results.suitability?.suitability_score || 0).class}`}>
                                        <div className="score-value">
                                            {Math.round(results.suitability?.suitability_score || 0)}
                                        </div>
                                        <div className="score-max">/100</div>
                                    </div>

                                    <div className={`suitability-badge ${getSuitabilityLevel(results.suitability?.suitability_score || 0).class}`}>
                                        {getSuitabilityLevel(results.suitability?.suitability_score || 0).label.toUpperCase()}
                                    </div>

                                    <div className="suitability-message">
                                        <p className="suitability-description">
                                            <strong>{formData.crop}</strong> cultivation is <strong>{getSuitabilityLevel(results.suitability?.suitability_score || 0).label.toLowerCase()}</strong> in <strong>{formData.state}</strong>
                                        </p>
                                        <div className="recommendation-tip">
                                            {getSuitabilityLevel(results.suitability?.suitability_score || 0).class === 'poor' && 
                                                "💡 Consider soil treatment or choose recommended crops below"
                                            }
                                            {getSuitabilityLevel(results.suitability?.suitability_score || 0).class === 'fair' && 
                                                "💡 Soil amendments may improve crop yield"
                                            }
                                            {getSuitabilityLevel(results.suitability?.suitability_score || 0).class === 'good' && 
                                                "👍 Good conditions for healthy crop growth"
                                            }
                                            {getSuitabilityLevel(results.suitability?.suitability_score || 0).class === 'excellent' && 
                                                "🌟 Excellent conditions for maximum yield"
                                            }
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Recommended Crops Card */}
                        <div className="result-card full-width recommendations-card">
                            <div className="card-header">
                                <div className="card-icon-wrapper">
                                    <Sprout className="header-icon" />
                                </div>
                                <h3 className="card-title">🌾 Best Crops for {formData.state}</h3>
                            </div>
                            <p className="card-description">Crops that grow well in your soil conditions</p>

                            <div className="recommendations-grid">
                                {(results.recommendations?.recommended_crops || []).slice(0, 6).map((item, index) => {
                                    const suitabilityLevel = getSuitabilityLevel(item.suitability_score);
                                    return (
                                        <div key={index} className={`recommendation-item ${suitabilityLevel.class}`}>
                                            <div className="crop-icon">
                                                {item.crop === 'Rice' ? '🌾' :
                                                 item.crop === 'Wheat' ? '🌾' :
                                                 item.crop === 'Maize' ? '🌽' :
                                                 item.crop === 'Cotton' ? '🌿' :
                                                 item.crop === 'Sugarcane' ? '🎋' :
                                                 item.crop === 'Potato' ? '🥔' :
                                                 item.crop === 'Tomato' ? '🍅' :
                                                 item.crop === 'Onion' ? '🧅' : '🌱'}
                                            </div>
                                            <div className="recommendation-content">
                                                <span className="recommendation-text">{item.crop}</span>
                                                <div className="crop-suitability">
                                                    <span className="recommendation-score">{item.suitability_score}%</span>
                                                    <span className={`crop-rating ${suitabilityLevel.class}`}>
                                                        {suitabilityLevel.label}
                                                    </span>
                                                </div>
                                            </div>
                                            <CheckCircle className="check-icon" />
                                        </div>
                                    );
                                })}
                            </div>

                            {results.recommendations?.recommended_crops && results.recommendations.recommended_crops.length > 6 && (
                                <div className="recommendations-note">
                                    <p>✨ <strong>{results.recommendations.recommended_crops.length - 6} more crops</strong> are suitable for your soil!</p>
                                </div>
                            )}
                        </div>
                    </>
                )}
            </div>
        </div>
    );
};

export default SoilAnalysis;