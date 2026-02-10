import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import {
    Leaf, TrendingUp, TrendingDown, Minus, AlertCircle, CheckCircle,
    Loader, MapPin, Calendar, Maximize2, CloudRain, Thermometer,
    DollarSign, AlertTriangle, Info, Sparkles, Target, ShoppingCart, BarChart3,
    Droplets, Sprout, Database
} from 'lucide-react';
import { planCrops, checkCropPlanningHealth, getCropDetails } from '../services/cropPlanningService';
import * as soilService from '../services/soilService';
import { compareMarkets, getCommodityInsights } from '../services/marketService';
import FieldHelpIcon from '../components/FieldHelpIcon';
import FieldHelpModal from '../components/FieldHelpModal';
import '../styles/crop-planning.css';

const CropPlanning = () => {
    const { t } = useTranslation(['pages', 'common']);

    const [formData, setFormData] = useState({
        state: '',
        month: new Date().getMonth() + 1,
        land_size: '',
        latitude: '',
        longitude: '',
        crop: ''
    });

    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);
    const [serverStatus, setServerStatus] = useState(null);
    const [locationLoading, setLocationLoading] = useState(false);

    // help modal
    const [helpModalOpen, setHelpModalOpen] = useState(false);
    const [helpFieldLabel, setHelpFieldLabel] = useState('');
    const [helpFieldName, setHelpFieldName] = useState('');

    // market
    const [marketData, setMarketData] = useState({});
    const [expandedCrop, setExpandedCrop] = useState(null);
    const [loadingMarket, setLoadingMarket] = useState(false);

    // states & crops list
    const [states, setStates] = useState([]);
    const [crops, setCrops] = useState([]);

    // crop review and AI suggestions
    const [cropReview, setCropReview] = useState(null);
    const [detailedReview, setDetailedReview] = useState(null);
    const [aiSuggestions, setAiSuggestions] = useState([]);
    const [aiLoading, setAiLoading] = useState(false);

    // location detection helpers
    const [locationAutoDetected, setLocationAutoDetected] = useState(false);
    const [detectedStateName, setDetectedStateName] = useState(null);
    const [locationError, setLocationError] = useState(null);

    useEffect(() => {
        const checkHealth = async () => {
            const isHealthy = await checkCropPlanningHealth();
            setServerStatus(isHealthy);
        };
        checkHealth();

        // load states and crops
        const loadInitial = async () => {
            try {
                const [statesData, cropsData] = await Promise.all([
                    soilService.getStates(),
                    soilService.getCrops()
                ]);
                if (Array.isArray(statesData)) setStates(statesData);
                if (Array.isArray(cropsData)) setCrops(cropsData);
            } catch (err) {
                console.error('Failed to load states/crops:', err);
            }
        };
        loadInitial();
    }, []);

    const months = [
        { value: 1, label: 'January' }, { value: 2, label: 'February' }, { value: 3, label: 'March' },
        { value: 4, label: 'April' }, { value: 5, label: 'May' }, { value: 6, label: 'June' },
        { value: 7, label: 'July' }, { value: 8, label: 'August' }, { value: 9, label: 'September' },
        { value: 10, label: 'October' }, { value: 11, label: 'November' }, { value: 12, label: 'December' }
    ];

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
        setError(null);
    };

    // Get location details using reverse geocoding (OpenStreetMap Nominatim)
    const getLocationDetails = async (latitude, longitude) => {
        try {
            const response = await fetch(
                `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}&zoom=10&addressdetails=1`,
                { headers: { 'Accept-Language': 'en' } }
            );
            if (!response.ok) throw new Error('Geocoding failed');
            const data = await response.json();
            const address = data.address || {};
            return {
                country: address.country || 'India',
                state: address.state || '',
                district: address.state_district || address.county || address.district || ''
            };
        } catch (err) {
            console.error('Error fetching location details:', err);
            return { country: 'India', state: '', district: '' };
        }
    };

    // Map coordinates to Indian states using bounding boxes (same logic as SoilAnalysis)
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

                // Try exact match first (case-insensitive)
                const exactMatch = states.find(s => s.toLowerCase() === state.name.toLowerCase());
                if (exactMatch) {
                    return { detectedName: state.name, matchedState: exactMatch };
                }

                // Try normalized match
                const normalizedStateName = state.name.toLowerCase().replace(/[^a-z]/g, '');
                const normalizedMatch = states.find(s => {
                    const normalizedAvailable = s.toLowerCase().replace(/[^a-z]/g, '');
                    return normalizedAvailable === normalizedStateName;
                });

                if (normalizedMatch) {
                    return { detectedName: state.name, matchedState: normalizedMatch };
                }

                // Try partial match
                const partialMatch = states.find(s => {
                    const sLower = s.toLowerCase();
                    const stateLower = state.name.toLowerCase();
                    return sLower.includes(stateLower) || stateLower.includes(sLower);
                });

                if (partialMatch) {
                    return { detectedName: state.name, matchedState: partialMatch };
                }

                return { detectedName: state.name, matchedState: null };
            }
        }

        return { detectedName: null, matchedState: null };
    };

    const detectLocation = () => {
        if (!navigator.geolocation) {
            setLocationError('Geolocation is not supported by your browser');
            return;
        }

        setLocationLoading(true);
        setLocationError(null);

        const options = { enableHighAccuracy: true, timeout: 10000, maximumAge: 600000 };

        navigator.geolocation.getCurrentPosition(
            async (position) => {
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;

                setFormData(prev => ({ ...prev, latitude: latitude.toFixed(6), longitude: longitude.toFixed(6) }));

                try {
                    const locationDetails = await getLocationDetails(latitude, longitude);
                    const { detectedName, matchedState } = getStateFromCoordinates(latitude, longitude);
                    setDetectedStateName(detectedName);

                    const updates = {};
                    let hasDetectedLocation = false;

                    if (locationDetails.country) { updates.country = locationDetails.country; hasDetectedLocation = true; }
                    if (locationDetails.district) { updates.district = locationDetails.district; hasDetectedLocation = true; }

                    if (matchedState) {
                        updates.state = matchedState;
                        hasDetectedLocation = true;
                        setLocationError(null);
                    } else if (detectedName) {
                        setLocationError(`Location detected: ${detectedName}. Please select your state manually.`);
                    } else {
                        setLocationError('Could not determine state from your location. Please select manually.');
                    }

                    if (hasDetectedLocation) {
                        setLocationAutoDetected(true);
                        setTimeout(() => setLocationAutoDetected(false), 5000);
                    }

                    if (Object.keys(updates).length > 0) setFormData(prev => ({ ...prev, ...updates }));
                } catch (err) {
                    console.error('Error processing location:', err);
                    setLocationError('Error detecting location details. Please enter manually.');
                }

                setLocationLoading(false);
            },
            (error) => {
                setLocationLoading(false);
                setLocationError('Unable to retrieve your location');
            },
            options
        );
    };

    // When crop is selected, load detailed analysis and AI top-3 suggestions
    useEffect(() => {
        const loadCropInfo = async () => {
            if (!formData.crop) {
                setCropReview(null);
                setDetailedReview(null);
                setAiSuggestions([]);
                return;
            }

            try {
                const details = await getCropDetails(formData.crop);
                if (details && details.success) setCropReview(details.data || details);
                else setCropReview(details || null);
            } catch (err) {
                console.error('Failed to fetch crop details:', err);
                setCropReview(null);
            }

            // Build detailed review based on location, season, and crop
            const buildDetailedReview = () => {
                const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
                const selectedMonth = months[parseInt(formData.month) - 1] || 'Selected month';
                const selectedState = formData.state || 'your region';

                // Determine season from month
                const monthNum = parseInt(formData.month);
                let season = 'Kharif';
                if (monthNum >= 10 || monthNum <= 3) season = 'Rabi';
                else if (monthNum >= 4 && monthNum <= 6) season = 'Summer';

                return {
                    cropName: formData.crop,
                    month: selectedMonth,
                    monthNum: monthNum,
                    state: selectedState,
                    season: season,
                    location: { latitude: formData.latitude, longitude: formData.longitude }
                };
            };

            setDetailedReview(buildDetailedReview());

            // Ask backend AI for top recommendations for the current location/month
            setAiLoading(true);
            try {
                const req = {
                    state: formData.state || null,
                    month: parseInt(formData.month) || null,
                    land_size: formData.land_size ? parseFloat(formData.land_size) : null,
                    latitude: formData.latitude ? parseFloat(formData.latitude) : null,
                    longitude: formData.longitude ? parseFloat(formData.longitude) : null,
                    crop: formData.crop
                };

                const resp = await planCrops(req);
                if (resp && resp.success && resp.data && Array.isArray(resp.data.recommendations)) {
                    setAiSuggestions(resp.data.recommendations.slice(0, 3));
                } else {
                    setAiSuggestions([]);
                }
            } catch (err) {
                console.error('AI suggestions failed:', err);
                setAiSuggestions([]);
            } finally {
                setAiLoading(false);
            }
        };

        loadCropInfo();
    }, [formData.crop, formData.state, formData.month, formData.latitude, formData.longitude, formData.land_size]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        setResult(null);

        try {
            const requestData = {
                state: formData.state,
                month: parseInt(formData.month),
                land_size: formData.land_size ? parseFloat(formData.land_size) : null,
                latitude: formData.latitude ? parseFloat(formData.latitude) : null,
                longitude: formData.longitude ? parseFloat(formData.longitude) : null,
                crop: formData.crop || null
            };

            const data = await planCrops(requestData);
            if (data.success) setResult(data.data);
            else setError(data.message || 'Failed to get crop recommendations');
        } catch (err) {
            console.error('Error:', err);
            setError(err.message || 'Network error. Please ensure the backend server is running.');
        } finally {
            setLoading(false);
        }
    };

    const resetForm = () => {
        setFormData({ state: '', month: new Date().getMonth() + 1, land_size: '', latitude: '', longitude: '', crop: '' });
        setResult(null);
        setError(null);
        setCropReview(null);
        setAiSuggestions([]);
    };

    const handleHelpClick = (fieldName, fieldLabel) => {
        setHelpFieldName(fieldName);
        setHelpFieldLabel(fieldLabel);
        setHelpModalOpen(true);
    };

    const loadMarketData = async (cropName, cropIndex) => {
        if (expandedCrop === cropIndex) { setExpandedCrop(null); return; }
        if (marketData[cropName]) { setExpandedCrop(cropIndex); return; }

        setLoadingMarket(true);
        try {
            const [marketsData, insightsData] = await Promise.all([
                compareMarkets(cropName, null, formData.state || null, null),
                getCommodityInsights(cropName, 30)
            ]);

            setMarketData(prev => ({ ...prev, [cropName]: { markets: marketsData.markets || [], insights: insightsData || null } }));
            setExpandedCrop(cropIndex);
        } catch (err) {
            console.error('Error loading market data:', err);
            setExpandedCrop(cropIndex);
        } finally {
            setLoadingMarket(false);
        }
    };

    const getTrendIcon = (trend) => {
        if (trend === 'up') return <TrendingUp className="trend-icon up" />;
        if (trend === 'down') return <TrendingDown className="trend-icon down" />;
        return <Minus className="trend-icon stable" />;
    };

    const getWeatherBadge = (suitability) => {
        const badges = { good: <span className="badge good">Good</span>, moderate: <span className="badge moderate">Moderate</span>, poor: <span className="badge poor">Poor</span> };
        return badges[suitability] || badges.moderate;
    };

    const getRiskBadge = (risk) => {
        const badges = { low: <span className="badge risk-low">Low Risk</span>, medium: <span className="badge risk-medium">Medium Risk</span>, high: <span className="badge risk-high">High Risk</span> };
        return badges[risk] || badges.medium;
    };

    const getScoreClass = (score) => {
        if (score >= 75) return 'score-excellent';
        if (score >= 60) return 'score-good';
        if (score >= 45) return 'score-moderate';
        return 'score-poor';
    };

    return (
        <div className="page-container">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {/* Header */}
                <div className="page-header">
                    <Leaf className="page-header-icon" />
                    <div>
                        <h1 className="page-header-title">🌱 Crop Planning Engine</h1>
                        <p className="page-header-subtitle">AI-powered crop selection based on market, weather, and seasonal factors</p>
                    </div>
                </div>

                {serverStatus === false && (
                    <div className="server-alert"><AlertCircle className="alert-icon" /><span>Server not running. Please start the backend service.</span></div>
                )}

                <div className="crop-planning-card">
                    <div className="form-header">
                        <Target className="form-header-icon" />
                        <div>
                            <h2 className="card-title">Plan Your Crop</h2>
                            <p className="card-subtitle">Tell us about your location and farmland to get personalized recommendations</p>
                        </div>
                    </div>

                    {/* Detailed Crop Review Card (Location & Season Based) */}
                    {detailedReview && cropReview && (
                        <div className="detailed-review-card">
                            <div className="review-header">
                                <h3 className="review-title">{detailedReview.cropName} — Detailed Viability Report</h3>
                                <p className="review-subtitle">Customized analysis for {detailedReview.state} in {detailedReview.month} ({detailedReview.season} season)</p>
                            </div>

                            <div className="review-summary">
                                <div className="summary-item">
                                    <strong>Crop:</strong> {detailedReview.cropName}
                                </div>
                                <div className="summary-item">
                                    <strong>Season:</strong> {detailedReview.season}
                                </div>
                                <div className="summary-item">
                                    <strong>Region:</strong> {detailedReview.state}
                                </div>
                                <div className="summary-item">
                                    <strong>Planting Month:</strong> {detailedReview.month}
                                </div>
                            </div>

                            {/* Performance Metrics */}
                            <div className="review-section">
                                <h4 className="section-heading">📊 Performance Metrics</h4>
                                <div className="metrics-grid">
                                    {cropReview.avg_yield && (
                                        <div className="metric-card">
                                            <span className="metric-label">Average Yield</span>
                                            <span className="metric-value">{cropReview.avg_yield}</span>
                                            <span className="metric-unit">t/ha</span>
                                        </div>
                                    )}
                                    {cropReview.avg_price && (
                                        <div className="metric-card">
                                            <span className="metric-label">Market Price</span>
                                            <span className="metric-value">₹{cropReview.avg_price}</span>
                                        </div>
                                    )}
                                    {cropReview.statistics?.historical_records && (
                                        <div className="metric-card">
                                            <span className="metric-label">Data Points</span>
                                            <span className="metric-value">{cropReview.statistics.historical_records.toLocaleString()}</span>
                                        </div>
                                    )}
                                    {cropReview.statistics?.states_grown && (
                                        <div className="metric-card">
                                            <span className="metric-label">Grown in States</span>
                                            <span className="metric-value">{cropReview.statistics.states_grown}</span>
                                        </div>
                                    )}
                                </div>
                            </div>

                            {/* Environmental Requirements */}
                            <div className="review-section">
                                <h4 className="section-heading">🌡️ Environmental Requirements</h4>
                                <div className="requirements-grid">
                                    {cropReview.crop_details?.temperature && (
                                        <div className="requirement-item">
                                            <span className="req-icon">🌡️</span>
                                            <div className="req-details">
                                                <span className="req-name">Temperature</span>
                                                <span className="req-value">{cropReview.crop_details.temperature.min}°C - {cropReview.crop_details.temperature.max}°C</span>
                                            </div>
                                        </div>
                                    )}
                                    {cropReview.crop_details?.rainfall && (
                                        <div className="requirement-item">
                                            <span className="req-icon">🌧️</span>
                                            <div className="req-details">
                                                <span className="req-name">Rainfall</span>
                                                <span className="req-value">{cropReview.crop_details.rainfall.min} - {cropReview.crop_details.rainfall.max} mm</span>
                                            </div>
                                        </div>
                                    )}
                                    {cropReview.crop_details?.humidity && (
                                        <div className="requirement-item">
                                            <span className="req-icon">💧</span>
                                            <div className="req-details">
                                                <span className="req-name">Humidity</span>
                                                <span className="req-value">{cropReview.crop_details.humidity.min} - {cropReview.crop_details.humidity.max}%</span>
                                            </div>
                                        </div>
                                    )}
                                    {cropReview.calendar_info?.growing_period_days && (
                                        <div className="requirement-item">
                                            <span className="req-icon">📅</span>
                                            <div className="req-details">
                                                <span className="req-name">Growing Period</span>
                                                <span className="req-value">{cropReview.calendar_info.growing_period_days} days</span>
                                            </div>
                                        </div>
                                    )}
                                </div>
                            </div>

                            {/* Soil Requirements */}
                            {cropReview.soil_info && Object.keys(cropReview.soil_info).length > 0 && (
                                <div className="review-section">
                                    <h4 className="section-heading">🌱 Soil Requirements</h4>
                                    <div className="soil-requirements">
                                        {cropReview.soil_info.ph && <div className="soil-item"><strong>pH Level:</strong> {cropReview.soil_info.ph}</div>}
                                        {cropReview.soil_info.nitrogen_n && <div className="soil-item"><strong>Nitrogen (N):</strong> {cropReview.soil_info.nitrogen_n} kg/ha</div>}
                                        {cropReview.soil_info.phosphorus_p && <div className="soil-item"><strong>Phosphorus (P):</strong> {cropReview.soil_info.phosphorus_p} kg/ha</div>}
                                        {cropReview.soil_info.potassium_k && <div className="soil-item"><strong>Potassium (K):</strong> {cropReview.soil_info.potassium_k} kg/ha</div>}
                                    </div>
                                </div>
                            )}

                            {/* Sowing & Harvesting Calendar */}
                            {cropReview.calendar_info && (
                                <div className="review-section">
                                    <h4 className="section-heading">📆 Sowing & Harvesting</h4>
                                    <div className="calendar-info">
                                        {cropReview.calendar_info.sowing_period && <div className="calendar-item"><strong>🌱 Sowing Period:</strong> {cropReview.calendar_info.sowing_period}</div>}
                                        {cropReview.calendar_info.harvesting_period && <div className="calendar-item"><strong>🌾 Harvesting Period:</strong> {cropReview.calendar_info.harvesting_period}</div>}
                                        {cropReview.calendar_info.season_name && <div className="calendar-item"><strong>Primary Season:</strong> {cropReview.calendar_info.season_name}</div>}
                                    </div>
                                </div>
                            )}

                            {/* Data Quality Badge */}
                            {cropReview.reliability && (
                                <div className="review-footer">
                                    <CheckCircle className="w-5 h-5" style={{ color: '#10b981' }} />
                                    <span>This analysis is based on <strong>{cropReview.reliability}</strong> historical agricultural data</span>
                                </div>
                            )}
                        </div>
                    )}

                    {/* Detailed Crop Analysis (based on dataset) */}
                    {cropReview && (
                        <div className="crop-analysis-card" style={{ display: 'none' }}>
                            <h3 className="analysis-title">{cropReview.name || formData.crop} — Detailed Analysis</h3>
                            {cropReview.summary && <p className="analysis-summary">{cropReview.summary}</p>}

                            <div className="analysis-grid">
                                {/* Key metrics */}
                                <div className="analysis-metrics">
                                    {cropReview.avg_yield && <div className="metric"><strong>Avg. Yield:</strong> {cropReview.avg_yield} t/ha</div>}
                                    {cropReview.avg_price && <div className="metric"><strong>Avg. Price:</strong> ₹{cropReview.avg_price}</div>}
                                    {cropReview.common_states && <div className="metric"><strong>Common States:</strong> {cropReview.common_states.join(', ')}</div>}
                                    {cropReview.reliability && <div className="metric"><strong>Data Reliability:</strong> {cropReview.reliability}</div>}
                                </div>

                                {/* Environmental / calendar */}
                                <div className="analysis-environment">
                                    {cropReview.crop_details?.temperature && <div><strong>Temperature:</strong> {cropReview.crop_details.temperature.min}°C - {cropReview.crop_details.temperature.max}°C</div>}
                                    {cropReview.crop_details?.rainfall && <div><strong>Rainfall:</strong> {cropReview.crop_details.rainfall.min} - {cropReview.crop_details.rainfall.max} mm</div>}
                                    {cropReview.crop_details?.humidity && <div><strong>Humidity:</strong> {cropReview.crop_details.humidity.min} - {cropReview.crop_details.humidity.max}%</div>}
                                    {cropReview.calendar_info?.sowing_period && <div><strong>Sowing:</strong> {cropReview.calendar_info.sowing_period}</div>}
                                    {cropReview.calendar_info?.harvesting_period && <div><strong>Harvesting:</strong> {cropReview.calendar_info.harvesting_period}</div>}
                                </div>

                                {/* Soil requirements */}
                                <div className="analysis-soil">
                                    <h4>Soil Requirements</h4>
                                    {cropReview.soil_info?.ph && <div><strong>pH:</strong> {cropReview.soil_info.ph}</div>}
                                    {cropReview.soil_info?.nitrogen_n && <div><strong>N:</strong> {cropReview.soil_info.nitrogen_n} kg/ha</div>}
                                    {cropReview.soil_info?.phosphorus_p && <div><strong>P:</strong> {cropReview.soil_info.phosphorus_p} kg/ha</div>}
                                    {cropReview.soil_info?.potassium_k && <div><strong>K:</strong> {cropReview.soil_info.potassium_k} kg/ha</div>}
                                </div>
                            </div>

                            {/* Statistical summary if available */}
                            {cropReview.statistics && (
                                <div className="analysis-stats">
                                    <h4>Statistical Summary</h4>
                                    <div className="stat-row"><strong>Historical Records:</strong> {cropReview.statistics.historical_records?.toLocaleString()}</div>
                                    <div className="stat-row"><strong>Avg. Yield / ha:</strong> {cropReview.statistics.avg_yield_per_hectare?.toFixed(2)} t/ha</div>
                                    <div className="stat-row"><strong>States Grown:</strong> {cropReview.statistics.states_grown}</div>
                                </div>
                            )}

                            {/* Data-driven notes / insights */}
                            {cropReview.insights && (
                                <div className="analysis-insights">
                                    <h4>Data Insights</h4>
                                    <ul>
                                        {cropReview.insights.map((note, i) => (
                                            <li key={i}>{note}</li>
                                        ))}
                                    </ul>
                                </div>
                            )}
                        </div>
                    )}

                    {/* AI top-3 suggestions (when crop selected) */}
                    {formData.crop && (
                        <div className="ai-suggestions-card">
                            <h4>Top 3 AI Suggestions</h4>
                            {aiLoading ? (
                                <div><Loader className="btn-icon spin" /> Thinking...</div>
                            ) : aiSuggestions.length > 0 ? (
                                <div className="ai-list">
                                    {aiSuggestions.map((c, idx) => (
                                        <div key={c.crop_name || idx} className="ai-item">
                                            <div className="ai-rank">#{idx + 1}</div>
                                            <div className="ai-name">{c.crop_name}</div>
                                            <div className="ai-score">Score: {c.final_score || c.score || '—'}/100</div>
                                        </div>
                                    ))}
                                </div>
                            ) : (
                                <div className="muted">No AI suggestions available.</div>
                            )}
                        </div>
                    )}

                    <form onSubmit={handleSubmit} className="planning-form">
                        <div className="form-grid">
                            <div className="form-column">
                                {/* State */}
                                <div className="form-group">
                                    <label htmlFor="state" className="form-label">
                                        <MapPin className="label-icon" /> State <span className="required">*</span>
                                        <FieldHelpIcon fieldName="state" onClick={() => handleHelpClick('state', 'State')} />
                                    </label>
                                    <select id="state" name="state" value={formData.state} onChange={handleInputChange} required className="form-select">
                                        <option value="">Select your state</option>
                                        {states.map(s => <option key={s} value={s}>{s}</option>)}
                                    </select>
                                </div>

                                {/* Month */}
                                <div className="form-group">
                                    <label htmlFor="month" className="form-label"><Calendar className="label-icon" /> Planning Month <span className="required">*</span></label>
                                    <select id="month" name="month" value={formData.month} onChange={handleInputChange} required className="form-select">
                                        {months.map(m => <option key={m.value} value={m.value}>{m.label}</option>)}
                                    </select>
                                </div>

                                {/* Crop selection */}
                                <div className="form-group">
                                    <label htmlFor="crop" className="form-label"><Sprout className="label-icon" /> Select Crop</label>
                                    <select id="crop" name="crop" value={formData.crop} onChange={handleInputChange} className="form-select">
                                        <option value="">Choose a crop</option>
                                        {crops.map(c => <option key={c} value={c}>{c}</option>)}
                                    </select>
                                </div>

                                {/* Land size */}
                                <div className="form-group">
                                    <label htmlFor="land_size" className="form-label"><Maximize2 className="label-icon" /> Land Size (hectares)</label>
                                    <input type="number" id="land_size" name="land_size" value={formData.land_size} onChange={handleInputChange} min="0.1" step="0.1" placeholder="e.g., 5.0" className="form-input" />
                                    <p className="input-hint">Optional: For quantity recommendations</p>
                                </div>
                            </div>

                            <div className="form-column">
                                <div className="location-section">
                                    <h3 className="section-title"><MapPin className="section-icon" /> Weather Forecast (Optional)</h3>
                                    <p className="section-description">Provide your coordinates for weather-based recommendations</p>

                                    <button type="button" onClick={detectLocation} disabled={locationLoading} className="detect-location-btn">
                                        {locationLoading ? (<><Loader className="btn-icon spin" /> Detecting...</>) : (<><MapPin className="btn-icon" /> Auto-Detect Location</>)}
                                    </button>

                                    {locationAutoDetected && (
                                        <div className="state-detected-msg"><CheckCircle className="success-icon" /> Location detected successfully!</div>
                                    )}
                                    {locationError && (
                                        <div className="location-error-msg"><AlertCircle className="error-icon" /> <span>{locationError}</span></div>
                                    )}

                                    <div className="coords-grid">
                                        <div className="form-group">
                                            <label htmlFor="latitude" className="form-label-small">Latitude</label>
                                            <input type="number" id="latitude" name="latitude" value={formData.latitude} onChange={handleInputChange} step="0.000001" placeholder="e.g., 30.7333" className="form-input-small" />
                                        </div>
                                        <div className="form-group">
                                            <label htmlFor="longitude" className="form-label-small">Longitude</label>
                                            <input type="number" id="longitude" name="longitude" value={formData.longitude} onChange={handleInputChange} step="0.000001" placeholder="e.g., 76.7794" className="form-input-small" />
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className="form-actions">
                            <button type="submit" disabled={loading} className="btn-primary">{loading ? (<><Loader className="btn-icon spin" /> Analyzing...</>) : (<><Sparkles className="btn-icon" /> Get Crop Recommendations</>)}</button>
                            <button type="button" onClick={resetForm} className="btn-secondary" disabled={loading}>Reset</button>
                        </div>
                    </form>
                </div>

                {/* Results Section (unchanged layout) */}
                {result && (
                    <>
                        <div className="results-header">
                            <div className="results-divider"><div className="divider-line"></div><span className="divider-text">🎯 Top {result.recommendations?.length || 0} Recommendations</span><div className="divider-line"></div></div>
                            <div className="season-badge"><Calendar className="season-icon" /><span>Season: <strong>{result.season}</strong></span></div>
                        </div>

                        <div className="recommendations-grid">
                            {result.recommendations?.map((crop, index) => (
                                <div key={crop.crop_name} className="crop-card">
                                    <div className="rank-badge">#{index + 1}</div>
                                    <div className="crop-header"><div className="crop-title-section"><h3 className="crop-name">{crop.crop_name}</h3><div className={`crop-score ${getScoreClass(crop.final_score)}`}>{crop.final_score}/100</div></div></div>

                                    <div className="score-breakdown">
                                        <div className="score-item"><DollarSign className="score-icon market" /><div className="score-details"><span className="score-label">Market</span><div className="score-value-row"><span className="score-value">{crop.scores?.market || '—'}</span>{getTrendIcon(crop.market_trend)}</div></div></div>

                                        <div className="score-item"><CloudRain className="score-icon weather" /><div className="score-details"><span className="score-label">Weather</span><div className="score-value-row"><span className="score-value">{crop.scores?.weather || '—'}</span>{getWeatherBadge(crop.weather_suitability)}</div></div></div>

                                        <div className="score-item"><Calendar className="score-icon season" /><div className="score-details"><span className="score-label">Season</span><span className="score-value">{crop.scores?.season || '—'}</span></div></div>

                                        <div className="score-item"><Leaf className="score-icon soil" /><div className="score-details"><span className="score-label">Soil</span><div className="score-value-row"><span className="score-value">{crop.scores?.soil || '—'}</span>{getWeatherBadge(crop.soil_suitability)}</div></div></div>

                                        <div className="score-item"><AlertTriangle className="score-icon risk" /><div className="score-details"><span className="score-label">Risk</span><div className="score-value-row"><span className="score-value">{crop.scores?.risk || '—'}</span>{getRiskBadge(crop.risk_level)}</div></div></div>
                                    </div>

                                    <div className="market-info-section">
                                        {crop.average_market_price_inr > 0 && (<div className="market-price"><DollarSign className="price-icon" /><div className="price-details"><span className="price-label">Avg. Market Price</span><span className="price-value">₹{crop.average_market_price_inr.toLocaleString()}/quintal</span></div></div>)}

                                        <button className="btn-market-view" onClick={() => loadMarketData(crop.crop_name, index)} disabled={loadingMarket}>{loadingMarket && expandedCrop === index ? (<><Loader className="w-4 h-4 animate-spin" /> Loading...</>) : (<><ShoppingCart className="w-4 h-4" /> View Market Prices</>)}</button>
                                    </div>

                                    {expandedCrop === index && marketData[crop.crop_name] && (
                                        <div className="market-expansion">
                                            <div className="market-expansion-header"><BarChart3 className="w-5 h-5" /><h4>Real-Time Market Insights for {crop.crop_name}</h4></div>

                                            {marketData[crop.crop_name].insights && (
                                                <div className="market-stats-mini">
                                                    <div className="stat-mini"><span className="stat-label">Price Trend</span><span className={`stat-value trend-${marketData[crop.crop_name].insights.trend?.direction}`}>{marketData[crop.crop_name].insights.trend?.direction === 'rising' && <TrendingUp className="w-4 h-4" />}{marketData[crop.crop_name].insights.trend?.direction === 'falling' && <TrendingDown className="w-4 h-4" />}{marketData[crop.crop_name].insights.trend?.direction === 'stable' && <Minus className="w-4 h-4" />}{marketData[crop.crop_name].insights.trend?.direction || 'N/A'}</span></div>
                                                    <div className="stat-mini"><span className="stat-label">Markets</span><span className="stat-value">{marketData[crop.crop_name].insights.markets?.total_markets || 0}</span></div>
                                                    <div className="stat-mini"><span className="stat-label">Avg. Daily Supply</span><span className="stat-value">{marketData[crop.crop_name].insights.arrival_stats?.avg_daily.toFixed(1) || 0} MT</span></div>
                                                </div>
                                            )}

                                            {marketData[crop.crop_name].markets && marketData[crop.crop_name].markets.length > 0 && (
                                                <div className="top-markets-section">
                                                    <h5 className="top-markets-title">🏆 Top 5 Markets (Best Prices)</h5>
                                                    <div className="markets-list">
                                                        {marketData[crop.crop_name].markets.slice(0, 5).map((market, idx) => (
                                                            <div key={idx} className="market-item"><div className="market-rank">#{idx + 1}</div><div className="market-details"><div className="market-name">{market.market}</div><div className="market-location">{market.district}</div></div><div className="market-price-info"><div className="market-price-value">₹{market.modal_price.toLocaleString()}</div><div className="market-arrival">{market.arrival_quantity.toFixed(1)} MT</div></div></div>
                                                        ))}
                                                    </div>
                                                    <p className="market-note">💡 Based on real government mandi data. Consider transport costs when choosing markets.</p>
                                                </div>
                                            )}
                                        </div>
                                    )}

                                    {crop.quantity_recommendation && Object.keys(crop.quantity_recommendation).length > 0 && (
                                        <div className="quantity-section">
                                            <h4 className="quantity-title">📊 Recommended Allocation</h4>
                                            <div className="quantity-grid">
                                                <div className="quantity-item"><span className="quantity-label">Area</span><span className="quantity-value">{crop.quantity_recommendation.recommended_area_hectares?.min || crop.quantity_recommendation.recommended_area_hectares} - {crop.quantity_recommendation.recommended_area_hectares?.max || crop.quantity_recommendation.recommended_area_hectares} ha</span></div>
                                                <div className="quantity-item"><span className="quantity-label">Expected Yield</span><span className="quantity-value">{crop.quantity_recommendation.expected_yield_tons?.min || crop.quantity_recommendation.expected_yield_range?.minimum_tonnes} - {crop.quantity_recommendation.expected_yield_tons?.max || crop.quantity_recommendation.expected_yield_range?.maximum_tonnes} tons</span></div>
                                                <div className="quantity-item"><span className="quantity-label">Growing Period</span><span className="quantity-value">{crop.quantity_recommendation.growing_period_days || crop.calendar_info?.growing_period_days || 90} days</span></div>
                                            </div>
                                            {crop.quantity_recommendation.reliability && (<div className="quantity-note"><Info className="w-4 h-4" /><span>Reliability: <strong>{crop.quantity_recommendation.reliability}</strong> ({crop.quantity_recommendation.based_on_records} historical records)</span></div>)}
                                        </div>
                                    )}

                                    {crop.crop_details && (
                                        <div className="crop-details">
                                            <div className="detail-row"><Thermometer className="detail-icon" /><span>Temp: {crop.crop_details.temperature?.min}°C - {crop.crop_details.temperature?.max}°C</span></div>
                                            <div className="detail-row"><CloudRain className="detail-icon" /><span>Rainfall: {crop.crop_details.rainfall?.min}-{crop.crop_details.rainfall?.max} mm</span></div>
                                            {crop.crop_details.humidity && (<div className="detail-row"><Droplets className="detail-icon" /><span>Humidity: {crop.crop_details.humidity?.min}-{crop.crop_details.humidity?.max}%</span></div>)}
                                            <div className="detail-row"><Info className="detail-icon" /><span>Water: {crop.crop_details.water_requirement}</span></div>
                                        </div>
                                    )}

                                    {crop.calendar_info && crop.calendar_info.sowing_period && (
                                        <div className="calendar-section"><h4 className="section-title">📅 Growing Calendar</h4><div className="calendar-grid"><div className="calendar-item"><span className="calendar-label">🌱 Sowing</span><span className="calendar-value">{crop.calendar_info.sowing_period}</span></div><div className="calendar-item"><span className="calendar-label">🌾 Harvesting</span><span className="calendar-value">{crop.calendar_info.harvesting_period}</span></div>{crop.calendar_info.season_name && (<div className="calendar-item"><span className="calendar-label">🍂 Season</span><span className="calendar-value">{crop.calendar_info.season_name}</span></div>)}</div></div>
                                    )}

                                    {crop.crop_details?.optimal_conditions && (
                                        <div className="optimal-section"><h4 className="section-title">🎯 Optimal Conditions</h4><div className="optimal-grid">{crop.crop_details.optimal_conditions.temperature && (<div className="optimal-item"><Thermometer className="optimal-icon" /><div className="optimal-details"><span className="optimal-label">Temperature</span><span className="optimal-value">{crop.crop_details.optimal_conditions.temperature}°C</span></div></div>)}{crop.crop_details.optimal_conditions.rainfall && (<div className="optimal-item"><CloudRain className="optimal-icon" /><div className="optimal-details"><span className="optimal-label">Rainfall</span><span className="optimal-value">{crop.crop_details.optimal_conditions.rainfall} mm</span></div></div>)}{crop.crop_details.optimal_conditions.humidity && (<div className="optimal-item"><Droplets className="optimal-icon" /><div className="optimal-details"><span className="optimal-label">Humidity</span><span className="optimal-value">{crop.crop_details.optimal_conditions.humidity}%</span></div></div>)}</div></div>
                                    )}

                                    {crop.soil_info && Object.keys(crop.soil_info).length > 0 && (
                                        <div className="soil-section"><h4 className="section-title">🌱 Soil Requirements ({result.state})</h4><div className="soil-grid">{crop.soil_info.ph && (<div className="soil-item"><span className="soil-label">pH Level</span><span className="soil-value">{crop.soil_info.ph}</span></div>)}{crop.soil_info.nitrogen_n && (<div className="soil-item"><span className="soil-label">Nitrogen (N)</span><span className="soil-value">{crop.soil_info.nitrogen_n} kg/ha</span></div>)}{crop.soil_info.phosphorus_p && (<div className="soil-item"><span className="soil-label">Phosphorus (P)</span><span className="soil-value">{crop.soil_info.phosphorus_p} kg/ha</span></div>)}{crop.soil_info.potassium_k && (<div className="soil-item"><span className="soil-label">Potassium (K)</span><span className="soil-value">{crop.soil_info.potassium_k} kg/ha</span></div>)}</div></div>
                                    )}

                                    {crop.crop_details?.statistics && crop.crop_details.statistics.historical_records > 0 && (
                                        <div className="stats-section"><h4 className="section-title">📊 Historical Data</h4><div className="stats-grid"><div className="stat-item"><Database className="stat-icon" /><div className="stat-details"><span className="stat-label">Records</span><span className="stat-value">{crop.crop_details.statistics.historical_records.toLocaleString()}</span></div></div><div className="stat-item"><MapPin className="stat-icon" /><div className="stat-details"><span className="stat-label">States</span><span className="stat-value">{crop.crop_details.statistics.states_grown}</span></div></div><div className="stat-item"><Sprout className="stat-icon" /><div className="stat-details"><span className="stat-label">Avg. Yield</span><span className="stat-value">{crop.crop_details.statistics.avg_yield_per_hectare.toFixed(2)} t/ha</span></div></div></div></div>
                                    )}
                                </div>
                            ))}
                        </div>

                        <div className="disclaimer"><AlertCircle className="disclaimer-icon" /><div><p className="disclaimer-title">Important Notice</p><p className="disclaimer-text">{result.disclaimer || "This is AI-based guidance. Please consult local agriculture officer."}</p></div></div>
                    </>
                )}

                {error && (
                    <div className="alert-error"><AlertCircle className="alert-icon" /><div><h3 className="alert-title">Error</h3><p className="alert-message">{error}</p></div></div>
                )}
            </div>

            <FieldHelpModal isOpen={helpModalOpen} onClose={() => setHelpModalOpen(false)} fieldLabel={helpFieldLabel} fieldName={helpFieldName} />
        </div>
    );
};

export default CropPlanning;
