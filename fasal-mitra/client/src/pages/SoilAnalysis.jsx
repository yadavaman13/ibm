import React, { useState, useEffect, useRef } from 'react';
import { useTranslation } from 'react-i18next';
import { Sprout, Droplets, TestTube, CheckCircle, AlertCircle, Loader, TrendingUp, MapPin, Navigation, Volume2, VolumeX, Play, Pause, Square, Camera, Upload, X, Eye, Lightbulb, ThumbsUp, Star, BarChart3, RotateCcw, Wheat, Calendar, IndianRupee, Package, Earth } from 'lucide-react';
import '../styles/pages.css';
import '../styles/soil-analysis-clean.css';
import * as soilService from '../services/soilService';
import FieldHelpIcon from '../components/FieldHelpIcon';
import FieldHelpModal from '../components/FieldHelpModal';
import worldIcon from '../assets/744483-removebg-preview.png';

const SoilAnalysis = () => {
    const { t } = useTranslation(['pages', 'common']);
    const [formData, setFormData] = useState({
        state: '',
        crop: '',
        fieldSize: '',
        irrigationType: '',
        previousCrop: '',
        waterQuality: ''
    });

    // Image upload state
    const [soilImage, setSoilImage] = useState(null);
    const [imagePreview, setImagePreview] = useState(null);
    const [imageAnalyzing, setImageAnalyzing] = useState(false);
    const fileInputRef = useRef(null);

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

    // Field help modal state
    const [helpModalOpen, setHelpModalOpen] = useState(false);
    const [helpFieldLabel, setHelpFieldLabel] = useState('');
    const [helpFieldName, setHelpFieldName] = useState('');

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

    // Image handling functions
    const handleImageUpload = (e) => {
        const file = e.target.files[0];
        if (file) {
            // Validate file type
            if (!file.type.startsWith('image/')) {
                setError('Please select a valid image file');
                return;
            }

            // Validate file size (max 10MB)
            if (file.size > 10 * 1024 * 1024) {
                setError('Image size should be less than 10MB');
                return;
            }

            setSoilImage(file);

            // Create preview
            const reader = new FileReader();
            reader.onload = (e) => {
                setImagePreview(e.target.result);
            };
            reader.readAsDataURL(file);

            setError(null);
        }
    };

    const removeImage = () => {
        setSoilImage(null);
        setImagePreview(null);
        if (fileInputRef.current) {
            fileInputRef.current.value = '';
        }
    };

    const captureFromCamera = () => {
        if (fileInputRef.current) {
            fileInputRef.current.setAttribute('capture', 'environment');
            fileInputRef.current.click();
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            // Prepare enhanced form data
            const analysisData = {
                state: formData.state,
                crop: formData.crop,
                ...(formData.fieldSize && { fieldSize: parseFloat(formData.fieldSize) }),
                ...(formData.irrigationType && { irrigationType: formData.irrigationType }),
                ...(formData.previousCrop && { previousCrop: formData.previousCrop }),
                ...(formData.waterQuality && { waterQuality: formData.waterQuality }),

                ...(soilImage && { soilImage: soilImage })
            };

            // Choose analysis method based on whether image is provided
            if (soilImage) {
                // Image-enhanced analysis
                setImageAnalyzing(true);

                const imageAnalysisResult = await soilService.analyzeSoilWithImage(analysisData);

                // Also get traditional recommendations for comparison
                const recommendations = await soilService.getRecommendedCrops(formData.state);

                setResults({
                    analysisType: 'image_enhanced',
                    imageAnalysis: imageAnalysisResult.image_analysis,
                    traditionalAnalysis: imageAnalysisResult.traditional_analysis,
                    combinedAnalysis: imageAnalysisResult.combined_analysis,
                    recommendations: recommendations
                });

                setImageAnalyzing(false);
            } else {
                // Traditional analysis only
                const [soilData, suitabilityData, recommendations] = await Promise.all([
                    soilService.getSoilData(formData.state),
                    soilService.checkSoilSuitability(analysisData),
                    soilService.getRecommendedCrops(formData.state)
                ]);

                setResults({
                    analysisType: 'traditional',
                    soil: soilData,
                    suitability: suitabilityData,
                    recommendations: recommendations
                });
            }
        } catch (err) {
            setError(err.message || 'Failed to analyze soil. Please try again.');
            setImageAnalyzing(false);
        } finally {
            setLoading(false);
        }
    };

    const resetForm = () => {
        setFormData({
            state: '',
            crop: '',
            fieldSize: '',
            irrigationType: '',
            previousCrop: '',
            waterQuality: '',

        });
        setSoilImage(null);
        setImagePreview(null);
        setImageAnalyzing(false);
        if (fileInputRef.current) {
            fileInputRef.current.value = '';
        }
        setResults(null);
        setError(null);
        setLocation({ latitude: null, longitude: null });
        setLocationError(null);
        setStateAutoDetected(false);
    };

    // Handle help icon click
    const handleHelpClick = (fieldName, fieldLabel) => {
        setHelpFieldName(fieldName);
        setHelpFieldLabel(fieldLabel);
        setHelpModalOpen(true);
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
                {/* Page Header */}
                <div className="page-header">
                    <Sprout className="page-header-icon" />
                    <div>
                        <h1 className="page-header-title">{t('soilAnalysis.title')}</h1>
                        <p className="page-header-subtitle">{t('soilAnalysis.subtitle')}</p>
                    </div>
                </div>

                {serverStatus === false && (
                    <div className="server-alert">
                        <AlertCircle className="alert-icon" />
                        <span>{t('pages:soilAnalysis.serverNotRunning')}</span>
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
                            {/* Two Column Layout */}
                            <div className="form-columns">
                                {/* Left Column */}
                                <div className="form-column">
                                    {/* Expected State */}
                                    <div className="form-field-wrapper">
                                        <div className="form-field">
                                            <label className="field-label">{t('pages:soilAnalysis.expectedState')}</label>
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
                                                    <strong>{t('pages:soilAnalysis.latitude')}:</strong> {location.latitude.toFixed(6)}
                                                </span>
                                                <span className="coordinate-separator">|</span>
                                                <span className="coordinate">
                                                    <strong>{t('pages:soilAnalysis.longitude')}:</strong> {location.longitude.toFixed(6)}
                                                </span>
                                            </div>
                                        )}
                                    </div>

                                    {/* Field Size */}
                                    <div className="form-field-wrapper">
                                        <div className="form-field">
                                            <label className="field-label">
                                                {t('pages:soilAnalysis.fieldSize')}
                                                <FieldHelpIcon
                                                    fieldName="fieldSize"
                                                    onClick={() => handleHelpClick('fieldSize', 'Field Size')}
                                                />
                                            </label>
                                            <input
                                                type="number"
                                                name="fieldSize"
                                                value={formData.fieldSize}
                                                onChange={handleInputChange}
                                                placeholder={t('pages:soilAnalysis.fieldSizePlaceholder')}
                                                className="field-input"
                                                min="0"
                                                step="0.1"
                                            />
                                        </div>
                                    </div>

                                    {/* Previous Crop */}
                                    <div className="form-field-wrapper">
                                        <div className="form-field">
                                            <label className="field-label">{t('pages:soilAnalysis.previousCrop')}</label>
                                            <select
                                                name="previousCrop"
                                                value={formData.previousCrop}
                                                onChange={handleInputChange}
                                                className="field-input"
                                            >
                                                <option value="">{t('pages:soilAnalysis.selectPreviousCrop')}</option>
                                                <option value="none">{t('pages:soilAnalysis.noPreviousCrop')}</option>
                                                {crops.map(crop => {
                                                    const translatedCrop = t(`common:crops.${crop}`, { defaultValue: crop });
                                                    return (
                                                        <option key={crop} value={crop}>{translatedCrop}</option>
                                                    );
                                                })}
                                            </select>
                                        </div>
                                    </div>
                                </div>

                                {/* Right Column */}
                                <div className="form-column">
                                    {/* Irrigation Type */}
                                    <div className="form-field-wrapper">
                                        <div className="form-field">
                                            <label className="field-label">
                                                {t('pages:soilAnalysis.irrigationType')}
                                                <FieldHelpIcon
                                                    fieldName="irrigationType"
                                                    onClick={() => handleHelpClick('irrigationType', 'Irrigation Type')}
                                                />
                                            </label>
                                            <select
                                                name="irrigationType"
                                                value={formData.irrigationType}
                                                onChange={handleInputChange}
                                                className="field-input"
                                            >
                                                <option value="">{t('pages:soilAnalysis.selectIrrigation')}</option>
                                                <option value="rainfed">{t('pages:soilAnalysis.irrigation.rainfed')}</option>
                                                <option value="drip">{t('pages:soilAnalysis.irrigation.drip')}</option>
                                                <option value="sprinkler">{t('pages:soilAnalysis.irrigation.sprinkler')}</option>
                                                <option value="flood">{t('pages:soilAnalysis.irrigation.flood')}</option>
                                                <option value="mixed">{t('pages:soilAnalysis.irrigation.mixed')}</option>
                                            </select>
                                        </div>
                                    </div>

                                    {/* Water Quality */}
                                    <div className="form-field-wrapper">
                                        <div className="form-field">
                                            <label className="field-label">
                                                {t('pages:soilAnalysis.waterQuality')}
                                                <FieldHelpIcon
                                                    fieldName="waterQuality"
                                                    onClick={() => handleHelpClick('waterQuality', 'Water Quality')}
                                                />
                                            </label>
                                            <select
                                                name="waterQuality"
                                                value={formData.waterQuality}
                                                onChange={handleInputChange}
                                                className="field-input"
                                            >
                                                <option value="">{t('pages:soilAnalysis.selectWaterQuality')}</option>
                                                <option value="sweet">{t('pages:soilAnalysis.waterTypes.sweet')}</option>
                                                <option value="slightlySalty">{t('pages:soilAnalysis.waterTypes.slightlySalty')}</option>
                                                <option value="verySalty">{t('pages:soilAnalysis.waterTypes.verySalty')}</option>
                                                <option value="unknown">{t('pages:soilAnalysis.waterTypes.unknown')}</option>
                                            </select>
                                        </div>
                                    </div>

                                    {/* Analyze Crop */}
                                    <div className="form-field-wrapper">
                                        <div className="form-field">
                                            <label className="field-label">{t('pages:soilAnalysis.analyzeCrop')}</label>
                                            <select
                                                name="crop"
                                                value={formData.crop}
                                                onChange={handleInputChange}
                                                required
                                                className="field-input"
                                            >
                                                <option value="">{t('pages:soilAnalysis.selectCrop')}</option>
                                                {crops.map(crop => {
                                                    const translatedCrop = t(`common:crops.${crop}`, { defaultValue: crop });
                                                    return (
                                                        <option key={crop} value={crop}>{translatedCrop}</option>
                                                    );
                                                })}
                                            </select>
                                        </div>

                                        {/* Crop Suggestions below Crop dropdown */}
                                        <div className="crop-suggestions-inline">
                                            <span className="try-text">{t('pages:soilAnalysis.try')}:</span>
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
                            </div>

                            {/* Soil Image Upload - Full Width */}
                            <div className="form-field-wrapper form-field-full-width">
                                <div className="form-field">
                                    <label className="field-label">{t('pages:soilAnalysis.soilImage')}</label>
                                    <div className="image-upload-container">
                                        <input
                                            type="file"
                                            ref={fileInputRef}
                                            onChange={handleImageUpload}
                                            accept="image/*"
                                            className="image-input-hidden"
                                        />

                                        {!imagePreview ? (
                                            <div className="image-upload-area">
                                                <div className="upload-actions">
                                                    <button
                                                        type="button"
                                                        onClick={() => fileInputRef.current?.click()}
                                                        className="upload-btn"
                                                    >
                                                        <Upload className="btn-icon" />
                                                        {t('pages:soilAnalysis.uploadImage')}
                                                    </button>
                                                    <button
                                                        type="button"
                                                        onClick={captureFromCamera}
                                                        className="camera-btn"
                                                    >
                                                        <Camera className="btn-icon" />
                                                        {t('pages:soilAnalysis.captureImage')}
                                                    </button>
                                                </div>
                                                <p className="upload-hint">
                                                    {t('pages:soilAnalysis.imageHint')}
                                                </p>
                                            </div>
                                        ) : (
                                            <div className="image-preview-container">
                                                <div className="image-preview">
                                                    <img
                                                        src={imagePreview}
                                                        alt="Soil sample"
                                                        className="preview-image"
                                                    />
                                                    <button
                                                        type="button"
                                                        onClick={removeImage}
                                                        className="remove-image-btn"
                                                    >
                                                        <X className="btn-icon" />
                                                    </button>
                                                </div>
                                                <div className="image-actions">
                                                    <button
                                                        type="button"
                                                        onClick={() => fileInputRef.current?.click()}
                                                        className="change-image-btn"
                                                    >
                                                        <Upload className="btn-icon" />
                                                        {t('pages:soilAnalysis.changeImage')}
                                                    </button>
                                                    <span className="image-status">
                                                        <Eye className="btn-icon" />
                                                        {t('pages:soilAnalysis.imageReady')}
                                                    </span>
                                                </div>
                                            </div>
                                        )}
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
                                        {t('pages:soilAnalysis.analyzing')}
                                    </>
                                ) : (
                                    t('pages:soilAnalysis.analyze')
                                )}
                            </button>
                            <button
                                type="button"
                                onClick={resetForm}
                                className="reset-btn"
                                disabled={loading}
                            >
                                {t('common:buttons.reset')}
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
                        {/* Image Analysis Display */}
                        {results.analysisType === 'image_enhanced' && (
                            <div className="image-enhanced-header">
                                <div className="analysis-badge">
                                    <Camera className="badge-icon" />
                                    <span>📸 AI Vision + Lab Analysis</span>
                                </div>
                                <p>Enhanced soil analysis with visual assessment</p>
                            </div>
                        )}

                        {/* Image Analysis Results Card */}
                        {results.analysisType === 'image_enhanced' && results.imageAnalysis && (
                            <div className="result-card image-analysis-card">
                                <div className="card-header">
                                    <div className="card-icon-wrapper">
                                        <Eye className="header-icon" />
                                    </div>
                                    <h3 className="card-title">🔍 Visual Soil Assessment</h3>
                                </div>
                                <p className="card-description">AI-powered analysis of your soil sample</p>

                                {results.imageAnalysis.structured_analysis && (
                                    <div className="visual-analysis-grid">
                                        <div className="visual-metric">
                                            <span className="metric-label">Soil Color</span>
                                            <span className="metric-value">{results.imageAnalysis.structured_analysis.soil_color?.replace('_', ' ') || 'Unknown'}</span>
                                        </div>
                                        <div className="visual-metric">
                                            <span className="metric-label">Texture Type</span>
                                            <span className="metric-value">{results.imageAnalysis.structured_analysis.texture_type || 'Unknown'}</span>
                                        </div>
                                        <div className="visual-metric">
                                            <span className="metric-label">Moisture Level</span>
                                            <span className="metric-value">{results.imageAnalysis.structured_analysis.moisture_level || 'Unknown'}</span>
                                        </div>
                                        <div className="visual-metric">
                                            <span className="metric-label">Health Score</span>
                                            <span className="metric-value">{results.imageAnalysis.structured_analysis.overall_health_score || 50}/100</span>
                                        </div>
                                    </div>
                                )}

                                {results.imageAnalysis.analysis_method === 'fallback' && (
                                    <div className="fallback-notice">
                                        <AlertCircle className="notice-icon" />
                                        <p>Visual analysis unavailable. Using lab analysis only.</p>
                                    </div>
                                )}
                            </div>
                        )}

                        <div className="results-grid">
                            {/* Show traditional soil composition card only for traditional analysis or when soil data exists */}
                            {(results.analysisType === 'traditional' && results.soil) || (results.analysisType === 'image_enhanced' && results.traditionalAnalysis?.soil_data) ? (
                                <div className="result-card soil-composition-card">
                                    <div className="card-header">
                                        <Sprout className="header-icon" />
                                        <h3 className="card-title">{t('pages:soilAnalysis.results.soilHealthReport')}</h3>
                                    </div>
                                    <p className="card-description">{t('pages:soilAnalysis.results.yourSoilNutrients')}</p>

                                    <div className="npk-grid">
                                        {/* Nitrogen */}
                                        <div className="npk-item">
                                            <div className="npk-header">
                                                <div className="npk-info">
                                                    <span className="npk-label">{t('pages:soilAnalysis.results.nitrogen')}</span>
                                                    <span className="npk-description">{t('pages:soilAnalysis.results.forGreenGrowth')}</span>
                                                </div>
                                                <span className="npk-value">
                                                    {results.analysisType === 'traditional'
                                                        ? (results.soil?.N || 0)
                                                        : (results.traditionalAnalysis?.soil_data?.N || 0)
                                                    }
                                                </span>
                                            </div>
                                            <div className="progress-bar-container">
                                                <div className="progress-bar">
                                                    <div
                                                        className="progress-bar-fill nitrogen"
                                                        style={{
                                                            width: `${getNPKLevel(
                                                                results.analysisType === 'traditional'
                                                                    ? (results.soil?.N || 0)
                                                                    : (results.traditionalAnalysis?.soil_data?.N || 0),
                                                                'N'
                                                            )}%`
                                                        }}
                                                    ></div>
                                                </div>
                                                <span className="nutrient-status">
                                                    {getNPKLevel(
                                                        results.analysisType === 'traditional'
                                                            ? (results.soil?.N || 0)
                                                            : (results.traditionalAnalysis?.soil_data?.N || 0),
                                                        'N'
                                                    ) > 60 ? (
                                                        <><CheckCircle className="status-icon status-good" /> Good</>
                                                    ) : getNPKLevel(
                                                        results.analysisType === 'traditional'
                                                            ? (results.soil?.N || 0)
                                                            : (results.traditionalAnalysis?.soil_data?.N || 0),
                                                        'N'
                                                    ) > 30 ? (
                                                        <><AlertCircle className="status-icon status-fair" /> {t('pages:soilAnalysis.results.fair')}</>
                                                    ) : (
                                                        <><AlertCircle className="status-icon status-low" /> {t('pages:soilAnalysis.results.low')}</>
                                                    )}
                                                </span>
                                            </div>
                                        </div>

                                        {/* Phosphorus */}
                                        <div className="npk-item">
                                            <div className="npk-header">
                                                <div className="npk-info">
                                                    <span className="npk-label">{t('pages:soilAnalysis.results.phosphorus')}</span>
                                                    <span className="npk-description">{t('pages:soilAnalysis.results.forRootStrength')}</span>
                                                </div>
                                                <span className="npk-value">
                                                    {results.analysisType === 'traditional'
                                                        ? (results.soil?.P || 0)
                                                        : (results.traditionalAnalysis?.soil_data?.P || 0)
                                                    }
                                                </span>
                                            </div>
                                            <div className="progress-bar-container">
                                                <div className="progress-bar">
                                                    <div
                                                        className="progress-bar-fill phosphorus"
                                                        style={{
                                                            width: `${getNPKLevel(
                                                                results.analysisType === 'traditional'
                                                                    ? (results.soil?.P || 0)
                                                                    : (results.traditionalAnalysis?.soil_data?.P || 0),
                                                                'P'
                                                            )}%`
                                                        }}
                                                    ></div>
                                                </div>
                                                <span className="nutrient-status">
                                                    {getNPKLevel(
                                                        results.analysisType === 'traditional'
                                                            ? (results.soil?.P || 0)
                                                            : (results.traditionalAnalysis?.soil_data?.P || 0),
                                                        'P'
                                                    ) > 60 ? (
                                                        <><CheckCircle className="status-icon status-good" /> {t('pages:soilAnalysis.results.good')}</>
                                                    ) : getNPKLevel(
                                                        results.analysisType === 'traditional'
                                                            ? (results.soil?.P || 0)
                                                            : (results.traditionalAnalysis?.soil_data?.P || 0),
                                                        'P'
                                                    ) > 30 ? (
                                                        <><AlertCircle className="status-icon status-fair" /> {t('pages:soilAnalysis.results.fair')}</>
                                                    ) : (
                                                        <><AlertCircle className="status-icon status-low" /> {t('pages:soilAnalysis.results.low')}</>
                                                    )}
                                                </span>
                                            </div>
                                        </div>

                                        {/* Potassium */}
                                        <div className="npk-item">
                                            <div className="npk-header">
                                                <div className="npk-info">
                                                    <span className="npk-label">{t('pages:soilAnalysis.results.potassium')}</span>
                                                    <span className="npk-description">{t('pages:soilAnalysis.results.forDiseaseResistance')}</span>
                                                </div>
                                                <span className="npk-value">
                                                    {results.analysisType === 'traditional'
                                                        ? (results.soil?.K || 0)
                                                        : (results.traditionalAnalysis?.soil_data?.K || 0)
                                                    }
                                                </span>
                                            </div>
                                            <div className="progress-bar-container">
                                                <div className="progress-bar">
                                                    <div
                                                        className="progress-bar-fill potassium"
                                                        style={{
                                                            width: `${getNPKLevel(
                                                                results.analysisType === 'traditional'
                                                                    ? (results.soil?.K || 0)
                                                                    : (results.traditionalAnalysis?.soil_data?.K || 0),
                                                                'K'
                                                            )}%`
                                                        }}
                                                    ></div>
                                                </div>
                                                <span className="nutrient-status">
                                                    {getNPKLevel(
                                                        results.analysisType === 'traditional'
                                                            ? (results.soil?.K || 0)
                                                            : (results.traditionalAnalysis?.soil_data?.K || 0),
                                                        'K'
                                                    ) > 60 ? (
                                                        <><CheckCircle className="status-icon status-good" /> {t('pages:soilAnalysis.results.good')}</>
                                                    ) : getNPKLevel(
                                                        results.analysisType === 'traditional'
                                                            ? (results.soil?.K || 0)
                                                            : (results.traditionalAnalysis?.soil_data?.K || 0),
                                                        'K'
                                                    ) > 30 ? (
                                                        <><AlertCircle className="status-icon status-fair" /> {t('pages:soilAnalysis.results.fair')}</>
                                                    ) : (
                                                        <><AlertCircle className="status-icon status-low" /> {t('pages:soilAnalysis.results.low')}</>
                                                    )}
                                                </span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            ) : null}

                            {/* Suitability Score Card - Only show for traditional analysis or when suitability data exists */}
                            {((results.analysisType === 'traditional' && results.suitability) ||
                                (results.analysisType === 'image_enhanced' && results.traditionalAnalysis?.basic_suitability)) && (
                                    <div className="result-card suitability-card">
                                        <div className="card-header">
                                            <BarChart3 className="header-icon" />
                                            <h3 className="card-title">{t('pages:soilAnalysis.results.cropSuitability')}</h3>
                                        </div>
                                        <p className="card-description">{t('pages:soilAnalysis.results.howSuitableIs')} {t(`common:crops.${formData.crop}`, { defaultValue: formData.crop })}?</p>

                                        <div className="suitability-content">
                                            <div className={`score-circle ${getSuitabilityLevel(
                                                results.analysisType === 'traditional'
                                                    ? (results.suitability?.suitability_score || 0)
                                                    : (results.traditionalAnalysis?.basic_suitability?.suitability_score || 0)
                                            ).class}`}>
                                                <div className="score-value">
                                                    {Math.round(
                                                        results.analysisType === 'traditional'
                                                            ? (results.suitability?.suitability_score || 0)
                                                            : (results.traditionalAnalysis?.basic_suitability?.suitability_score || 0)
                                                    )}
                                                </div>
                                                <div className="score-max">/100</div>
                                            </div>

                                            <div className={`suitability-badge ${getSuitabilityLevel(
                                                results.analysisType === 'traditional'
                                                    ? (results.suitability?.suitability_score || 0)
                                                    : (results.traditionalAnalysis?.basic_suitability?.suitability_score || 0)
                                            ).class}`}>
                                                {t(`pages:soilAnalysis.results.${getSuitabilityLevel(
                                                    results.analysisType === 'traditional'
                                                        ? (results.suitability?.suitability_score || 0)
                                                        : (results.traditionalAnalysis?.basic_suitability?.suitability_score || 0)
                                                ).label.toLowerCase()}`, { defaultValue: getSuitabilityLevel(
                                                    results.analysisType === 'traditional'
                                                        ? (results.suitability?.suitability_score || 0)
                                                        : (results.traditionalAnalysis?.basic_suitability?.suitability_score || 0)
                                                ).label }).toUpperCase()}
                                            </div>

                                            <div className="suitability-message">
                                                <p className="suitability-description">
                                                    <strong>{t(`common:crops.${formData.crop}`, { defaultValue: formData.crop })}</strong> {t('pages:soilAnalysis.results.cultivationIs')} <strong>{t(`pages:soilAnalysis.results.${getSuitabilityLevel(
                                                        results.analysisType === 'traditional'
                                                            ? (results.suitability?.suitability_score || 0)
                                                            : (results.traditionalAnalysis?.basic_suitability?.suitability_score || 0)
                                                    ).label.toLowerCase()}`, { defaultValue: getSuitabilityLevel(
                                                        results.analysisType === 'traditional'
                                                            ? (results.suitability?.suitability_score || 0)
                                                            : (results.traditionalAnalysis?.basic_suitability?.suitability_score || 0)
                                                    ).label })}</strong> {t('pages:soilAnalysis.results.in')} <strong>{t(`common:states.${formData.state}`, { defaultValue: formData.state })}</strong>
                                                </p>
                                                <div className="recommendation-tip">
                                                    {getSuitabilityLevel(
                                                        results.analysisType === 'traditional'
                                                            ? (results.suitability?.suitability_score || 0)
                                                            : (results.traditionalAnalysis?.basic_suitability?.suitability_score || 0)
                                                    ).class === 'poor' && (
                                                            <><Lightbulb className="tip-icon" /> {t('pages:soilAnalysis.results.considerSoilTreatment')}</>
                                                        )}
                                                    {getSuitabilityLevel(
                                                        results.analysisType === 'traditional'
                                                            ? (results.suitability?.suitability_score || 0)
                                                            : (results.traditionalAnalysis?.basic_suitability?.suitability_score || 0)
                                                    ).class === 'fair' && (
                                                            <><Lightbulb className="tip-icon" /> {t('pages:soilAnalysis.results.soilAmendmentsMayImprove')}</>
                                                        )}
                                                    {getSuitabilityLevel(
                                                        results.analysisType === 'traditional'
                                                            ? (results.suitability?.suitability_score || 0)
                                                            : (results.traditionalAnalysis?.basic_suitability?.suitability_score || 0)
                                                    ).class === 'good' && (
                                                            <><ThumbsUp className="tip-icon" /> {t('pages:soilAnalysis.results.goodConditions')}</>
                                                        )}
                                                    {getSuitabilityLevel(
                                                        results.analysisType === 'traditional'
                                                            ? (results.suitability?.suitability_score || 0)
                                                            : (results.traditionalAnalysis?.basic_suitability?.suitability_score || 0)
                                                    ).class === 'excellent' && (
                                                            <><Star className="tip-icon" /> {t('pages:soilAnalysis.results.excellentConditions')}</>
                                                        )}
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                )}
                        </div>

                        {/* Enhanced Analysis Cards */}
                        <div className="results-grid-secondary">
                            {((results.analysisType === 'traditional' && results.suitability?.irrigation_analysis) ||
                                (results.analysisType === 'image_enhanced' && results.traditionalAnalysis?.irrigation_analysis)) && (
                                    <div className="result-card enhanced-analysis-card">
                                        <div className="card-header">
                                            <Droplets className="header-icon" />
                                            <h3 className="card-title">{t('pages:soilAnalysis.results.irrigationAnalysis')}</h3>
                                        </div>
                                        <p className="card-description">
                                            {results.analysisType === 'traditional'
                                                ? results.suitability?.irrigation_analysis?.message
                                                : results.traditionalAnalysis?.irrigation_analysis?.message}
                                        </p>

                                        <div className="analysis-detail">
                                            <div className={`compatibility-badge ${results.analysisType === 'traditional'
                                                ? results.suitability?.irrigation_analysis?.compatibility
                                                : results.traditionalAnalysis?.irrigation_analysis?.compatibility
                                                }`}>
                                                {(
                                                    results.analysisType === 'traditional'
                                                        ? results.suitability?.irrigation_analysis?.compatibility
                                                        : results.traditionalAnalysis?.irrigation_analysis?.compatibility
                                                )?.toUpperCase() || 'N/A'}
                                            </div>
                                            <p><strong>Water Requirement:</strong> {
                                                (
                                                    results.analysisType === 'traditional'
                                                        ? results.suitability?.irrigation_analysis?.crop_water_requirement
                                                        : results.traditionalAnalysis?.irrigation_analysis?.crop_water_requirement
                                                )?.toUpperCase() || 'Medium'
                                            }</p>
                                        </div>
                                    </div>
                                )}

                            {((results.analysisType === 'traditional' && results.suitability?.water_quality_impact) ||
                                (results.analysisType === 'image_enhanced' && results.traditionalAnalysis?.water_quality_impact)) && (
                                    <div className="result-card enhanced-analysis-card">
                                        <div className="card-header">
                                            <TestTube className="header-icon" />
                                            <h3 className="card-title">Water Quality Impact</h3>
                                        </div>
                                        <p className="card-description">
                                            {results.analysisType === 'traditional'
                                                ? results.suitability?.water_quality_impact?.message
                                                : results.traditionalAnalysis?.water_quality_impact?.message}
                                        </p>

                                        <div className="analysis-detail">
                                            <div className={`impact-badge ${results.analysisType === 'traditional'
                                                ? results.suitability?.water_quality_impact?.impact
                                                : results.traditionalAnalysis?.water_quality_impact?.impact
                                                }`}>
                                                {(
                                                    results.analysisType === 'traditional'
                                                        ? results.suitability?.water_quality_impact?.impact
                                                        : results.traditionalAnalysis?.water_quality_impact?.impact
                                                )?.toUpperCase() || 'N/A'}
                                            </div>
                                            <p><strong>Salt Tolerance:</strong> {
                                                (
                                                    results.analysisType === 'traditional'
                                                        ? results.suitability?.water_quality_impact?.crop_salt_tolerance
                                                        : results.traditionalAnalysis?.water_quality_impact?.crop_salt_tolerance
                                                )?.toUpperCase() || 'Medium'
                                            }</p>
                                        </div>
                                    </div>
                                )}

                            {((results.analysisType === 'traditional' && results.suitability?.rotation_analysis) ||
                                (results.analysisType === 'image_enhanced' && results.traditionalAnalysis?.rotation_analysis)) && (
                                    <div className="result-card rotation-card">
                                        <div className="card-header">
                                            <RotateCcw className="header-icon" />
                                            <h3 className="card-title">Crop Rotation Analysis</h3>
                                        </div>
                                        <p className="card-description">
                                            {results.analysisType === 'traditional'
                                                ? results.suitability?.rotation_analysis?.message
                                                : results.traditionalAnalysis?.rotation_analysis?.message}
                                        </p>

                                        <div className="rotation-benefit">
                                            <div className={`benefit-badge ${results.analysisType === 'traditional'
                                                ? results.suitability?.rotation_analysis?.benefit
                                                : results.traditionalAnalysis?.rotation_analysis?.benefit
                                                }`}>
                                                {(
                                                    results.analysisType === 'traditional'
                                                        ? results.suitability?.rotation_analysis?.benefit
                                                        : results.traditionalAnalysis?.rotation_analysis?.benefit
                                                )?.toUpperCase() || 'NEUTRAL'}
                                            </div>


                                            {((results.analysisType === 'traditional' && results.suitability?.rotation_analysis?.nitrogen_bonus) ||
                                                (results.analysisType === 'image_enhanced' && results.traditionalAnalysis?.rotation_analysis?.nitrogen_bonus)) && (
                                                    <div className="bonus-tag">
                                                        <Sprout className="tag-icon" /> {t('pages:soilAnalysis.results.nitrogenBonus')}
                                                    </div>
                                                )}
                                            {((results.analysisType === 'traditional' && results.suitability?.rotation_analysis?.risk_warning) ||
                                                (results.analysisType === 'image_enhanced' && results.traditionalAnalysis?.rotation_analysis?.risk_warning)) && (
                                                    <div className="warning-tag">
                                                        <AlertCircle className="tag-icon" /> Increased Pest Risk
                                                    </div>
                                                )}
                                        </div>
                                    </div>
                                )}
                        </div>

                        {/* Fertilizer Plan - Full Width */}
                        {((results.analysisType === 'traditional' && results.suitability?.input_recommendations) ||
                            (results.analysisType === 'image_enhanced' && results.traditionalAnalysis?.input_recommendations)) && (
                                <div className="result-card full-width fertilizer-plan-card">
                                    <div className="card-header">
                                        <Package className="header-icon" />
                                        <h3 className="card-title">Fertilizer Plan</h3>
                                    </div>
                                    <p className="card-description">For {
                                        results.analysisType === 'traditional'
                                            ? results.suitability?.input_recommendations?.field_size_hectares
                                            : results.traditionalAnalysis?.input_recommendations?.field_size_hectares
                                    } hectares</p>

                                    <div className="fertilizer-grid">
                                        <div className="fertilizer-section">
                                            <div className="section-header">
                                                <Sprout className="section-icon" />
                                                <h4>Total Requirements</h4>
                                            </div>
                                            <div className="nutrient-requirements">
                                                <div className="nutrient-item">
                                                    <span className="nutrient-label">Nitrogen (N):</span>
                                                    <span className="nutrient-amount">{
                                                        results.analysisType === 'traditional'
                                                            ? results.suitability?.input_recommendations?.fertilizer_recommendations?.total_field?.N
                                                            : results.traditionalAnalysis?.input_recommendations?.fertilizer_recommendations?.total_field?.N
                                                    } kg</span>
                                                </div>
                                                <div className="nutrient-item">
                                                    <span className="nutrient-label">Phosphorus (P):</span>
                                                    <span className="nutrient-amount">{
                                                        results.analysisType === 'traditional'
                                                            ? results.suitability?.input_recommendations?.fertilizer_recommendations?.total_field?.P
                                                            : results.traditionalAnalysis?.input_recommendations?.fertilizer_recommendations?.total_field?.P
                                                    } kg</span>
                                                </div>
                                                <div className="nutrient-item">
                                                    <span className="nutrient-label">Potassium (K):</span>
                                                    <span className="nutrient-amount">{
                                                        results.analysisType === 'traditional'
                                                            ? results.suitability?.input_recommendations?.fertilizer_recommendations?.total_field?.K
                                                            : results.traditionalAnalysis?.input_recommendations?.fertilizer_recommendations?.total_field?.K
                                                    } kg</span>
                                                </div>
                                            </div>
                                        </div>

                                        <div className="fertilizer-section">
                                            <div className="section-header">
                                                <IndianRupee className="section-icon" />
                                                <h4>Cost Estimate</h4>
                                            </div>
                                            <div className="cost-breakdown">
                                                <div className="cost-item">
                                                    <span>Total Cost:</span>
                                                    <span className="cost-value">₹{
                                                        results.analysisType === 'traditional'
                                                            ? results.suitability?.input_recommendations?.estimated_cost?.total_inr
                                                            : results.traditionalAnalysis?.input_recommendations?.estimated_cost?.total_inr
                                                    }</span>
                                                </div>
                                                <div className="cost-item">
                                                    <span>Per Hectare:</span>
                                                    <span className="cost-value">₹{
                                                        results.analysisType === 'traditional'
                                                            ? results.suitability?.input_recommendations?.estimated_cost?.per_hectare_inr
                                                            : results.traditionalAnalysis?.input_recommendations?.estimated_cost?.per_hectare_inr
                                                    }</span>
                                                </div>
                                            </div>
                                        </div>

                                        <div className="fertilizer-section">
                                            <div className="section-header">
                                                <Calendar className="section-icon" />
                                                <h4>Application Schedule</h4>
                                            </div>
                                            <ul className="timing-list">
                                                {(
                                                    results.analysisType === 'traditional'
                                                        ? results.suitability?.input_recommendations?.application_timing
                                                        : results.traditionalAnalysis?.input_recommendations?.application_timing
                                                )?.map((timing, index) => (
                                                    <li key={index}>
                                                        <CheckCircle className="timing-icon" />
                                                        {timing}
                                                    </li>
                                                )) || []}
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            )}

                        {/* Recommended Crops Card */}
                        <div className="result-card full-width recommendations-card">\n                            <div className="card-header">
                            <Wheat className="header-icon" />
                            <h3 className="card-title">Best Crops for {formData.state}</h3>
                        </div>
                            <p className="card-description">Crops that grow well in your soil conditions</p>

                            <div className="recommendations-grid">
                                {(results.recommendations?.recommended_crops || []).slice(0, 6).map((item, index) => {
                                    const suitabilityLevel = getSuitabilityLevel(item.suitability_score);
                                    return (
                                        <div key={index} className={`recommendation-item ${suitabilityLevel.class}`}>
                                            <Sprout className="crop-icon" />
                                            <div className="recommendation-content">
                                                <span className="recommendation-text">{t(`common:crops.${item.crop}`, { defaultValue: item.crop })}</span>
                                                <div className="crop-suitability">
                                                    <span className="recommendation-score">{item.suitability_score}%</span>
                                                    <span className={`crop-rating ${suitabilityLevel.class}`}>
                                                        {t(`pages:soilAnalysis.results.${suitabilityLevel.label.toLowerCase()}`, { defaultValue: suitabilityLevel.label })}
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
                                    <Star className="note-icon" />
                                    <p><strong>{results.recommendations.recommended_crops.length - 6} more crops</strong> are suitable for your soil!</p>
                                </div>
                            )}
                        </div>
                    </>
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

export default SoilAnalysis;