import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { 
    Leaf, TrendingUp, TrendingDown, Minus, AlertCircle, CheckCircle, 
    Loader, MapPin, Calendar, Maximize2, CloudRain, Thermometer, 
    DollarSign, AlertTriangle, Info, Sparkles, Target, ShoppingCart, BarChart3,
    Droplets, Sprout, Database
} from 'lucide-react';
import { planCrops, checkCropPlanningHealth } from '../services/cropPlanningService';
import { compareMarkets, getCommodityInsights } from '../services/marketService';
import FieldHelpIcon from '../components/FieldHelpIcon';
import FieldHelpModal from '../components/FieldHelpModal';
import '../styles/crop-planning.css';

const CropPlanning = () => {
    const { t } = useTranslation(['pages', 'common']);
    const [formData, setFormData] = useState({
        state: '',
        month: new Date().getMonth() + 1, // Current month
        land_size: '',
        latitude: '',
        longitude: ''
    });
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);
    const [serverStatus, setServerStatus] = useState(null);
    const [locationLoading, setLocationLoading] = useState(false);

    // Field help modal state
    const [helpModalOpen, setHelpModalOpen] = useState(false);
    const [helpFieldLabel, setHelpFieldLabel] = useState('');
    const [helpFieldName, setHelpFieldName] = useState('');

    // Market data state
    const [marketData, setMarketData] = useState({});
    const [expandedCrop, setExpandedCrop] = useState(null);
    const [loadingMarket, setLoadingMarket] = useState(false);

    // Check server health on mount
    useEffect(() => {
        const checkHealth = async () => {
            const isHealthy = await checkCropPlanningHealth();
            setServerStatus(isHealthy);
        };
        checkHealth();
    }, []);

    // Indian states
    const states = [
        'Punjab', 'Haryana', 'Uttar Pradesh', 'Maharashtra', 'Gujarat', 
        'Madhya Pradesh', 'Karnataka', 'Tamil Nadu', 'Andhra Pradesh', 
        'Telangana', 'Rajasthan', 'Bihar', 'West Bengal', 'Odisha'
    ];

    // Months
    const months = [
        { value: 1, label: 'January' },
        { value: 2, label: 'February' },
        { value: 3, label: 'March' },
        { value: 4, label: 'April' },
        { value: 5, label: 'May' },
        { value: 6, label: 'June' },
        { value: 7, label: 'July' },
        { value: 8, label: 'August' },
        { value: 9, label: 'September' },
        { value: 10, label: 'October' },
        { value: 11, label: 'November' },
        { value: 12, label: 'December' }
    ];

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
        setError(null);
    };

    const detectLocation = () => {
        if (!navigator.geolocation) {
            setError('Geolocation is not supported by your browser');
            return;
        }

        setLocationLoading(true);
        navigator.geolocation.getCurrentPosition(
            (position) => {
                setFormData(prev => ({
                    ...prev,
                    latitude: position.coords.latitude.toFixed(6),
                    longitude: position.coords.longitude.toFixed(6)
                }));
                setLocationLoading(false);
            },
            (error) => {
                setError('Unable to retrieve your location');
                setLocationLoading(false);
            }
        );
    };

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
                longitude: formData.longitude ? parseFloat(formData.longitude) : null
            };

            const data = await planCrops(requestData);

            if (data.success) {
                setResult(data.data);
            } else {
                setError(data.message || 'Failed to get crop recommendations');
            }
        } catch (err) {
            console.error('Error:', err);
            setError(err.message || 'Network error. Please ensure the backend server is running.');
        } finally {
            setLoading(false);
        }
    };

    const resetForm = () => {
        setFormData({
            state: '',
            month: new Date().getMonth() + 1,
            land_size: '',
            latitude: '',
            longitude: ''
        });
        setResult(null);
        setError(null);
    };

    const handleHelpClick = (fieldName, fieldLabel) => {
        setHelpFieldName(fieldName);
        setHelpFieldLabel(fieldLabel);
        setHelpModalOpen(true);
    };

    const loadMarketData = async (cropName, cropIndex) => {
        // Toggle if clicking the same crop
        if (expandedCrop === cropIndex) {
            setExpandedCrop(null);
            return;
        }

        // If already loaded, just expand
        if (marketData[cropName]) {
            setExpandedCrop(cropIndex);
            return;
        }

        // Load fresh market data
        setLoadingMarket(true);
        try {
            // Fetch market comparison and insights
            const [marketsData, insightsData] = await Promise.all([
                compareMarkets(cropName, null, formData.state || null, null),
                getCommodityInsights(cropName, 30)
            ]);

            setMarketData(prev => ({
                ...prev,
                [cropName]: {
                    markets: marketsData.markets || [],
                    insights: insightsData || null
                }
            }));
            
            setExpandedCrop(cropIndex);
        } catch (err) {
            console.error('Error loading market data:', err);
            // Still expand to show error or partial data
            setExpandedCrop(cropIndex);
        } finally {
            setLoadingMarket(false);
        }
    };

    // Get trend icon
    const getTrendIcon = (trend) => {
        if (trend === 'up') return <TrendingUp className="trend-icon up" />;
        if (trend === 'down') return <TrendingDown className="trend-icon down" />;
        return <Minus className="trend-icon stable" />;
    };

    // Get weather suitability badge
    const getWeatherBadge = (suitability) => {
        const badges = {
            good: <span className="badge good">Good</span>,
            moderate: <span className="badge moderate">Moderate</span>,
            poor: <span className="badge poor">Poor</span>
        };
        return badges[suitability] || badges.moderate;
    };

    // Get risk badge
    const getRiskBadge = (risk) => {
        const badges = {
            low: <span className="badge risk-low">Low Risk</span>,
            medium: <span className="badge risk-medium">Medium Risk</span>,
            high: <span className="badge risk-high">High Risk</span>
        };
        return badges[risk] || badges.medium;
    };

    // Get score color class
    const getScoreClass = (score) => {
        if (score >= 75) return 'score-excellent';
        if (score >= 60) return 'score-good';
        if (score >= 45) return 'score-moderate';
        return 'score-poor';
    };

    return (
        <div className="page-container">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {/* Page Header */}
                <div className="page-header">
                    <Leaf className="page-header-icon" />
                    <div>
                        <h1 className="page-header-title">🌱 Crop Planning Engine</h1>
                        <p className="page-header-subtitle">
                            AI-powered crop selection based on market, weather, and seasonal factors
                        </p>
                    </div>
                </div>

                {serverStatus === false && (
                    <div className="server-alert">
                        <AlertCircle className="alert-icon" />
                        <span>Server not running. Please start the backend service.</span>
                    </div>
                )}

                {/* Form Section */}
                <div className="crop-planning-card">
                    <div className="form-header">
                        <Target className="form-header-icon" />
                        <div>
                            <h2 className="card-title">Plan Your Crop</h2>
                            <p className="card-subtitle">
                                Tell us about your location and farmland to get personalized recommendations
                            </p>
                        </div>
                    </div>

                    <form onSubmit={handleSubmit} className="planning-form">
                        {/* Two-column layout */}
                        <div className="form-grid">
                            {/* Left Column */}
                            <div className="form-column">
                                {/* State Selection */}
                                <div className="form-group">
                                    <label htmlFor="state" className="form-label">
                                        <MapPin className="label-icon" />
                                        State <span className="required">*</span>
                                        <FieldHelpIcon
                                            fieldName="state"
                                            onClick={() => handleHelpClick('state', 'State')}
                                        />
                                    </label>
                                    <select
                                        id="state"
                                        name="state"
                                        value={formData.state}
                                        onChange={handleInputChange}
                                        required
                                        className="form-select"
                                    >
                                        <option value="">Select your state</option>
                                        {states.map(state => (
                                            <option key={state} value={state}>{state}</option>
                                        ))}
                                    </select>
                                </div>

                                {/* Month Selection */}
                                <div className="form-group">
                                    <label htmlFor="month" className="form-label">
                                        <Calendar className="label-icon" />
                                        Planning Month <span className="required">*</span>
                                        <FieldHelpIcon
                                            fieldName="month"
                                            onClick={() => handleHelpClick('month', 'Planning Month')}
                                        />
                                    </label>
                                    <select
                                        id="month"
                                        name="month"
                                        value={formData.month}
                                        onChange={handleInputChange}
                                        required
                                        className="form-select"
                                    >
                                        {months.map(month => (
                                            <option key={month.value} value={month.value}>
                                                {month.label}
                                            </option>
                                        ))}
                                    </select>
                                </div>

                                {/* Land Size */}
                                <div className="form-group">
                                    <label htmlFor="land_size" className="form-label">
                                        <Maximize2 className="label-icon" />
                                        Land Size (hectares)
                                        <FieldHelpIcon
                                            fieldName="land_size"
                                            onClick={() => handleHelpClick('land_size', 'Land Size')}
                                        />
                                    </label>
                                    <input
                                        type="number"
                                        id="land_size"
                                        name="land_size"
                                        value={formData.land_size}
                                        onChange={handleInputChange}
                                        min="0.1"
                                        step="0.1"
                                        placeholder="e.g., 5.0"
                                        className="form-input"
                                    />
                                    <p className="input-hint">Optional: For quantity recommendations</p>
                                </div>
                            </div>

                            {/* Right Column */}
                            <div className="form-column">
                                {/* Location Section */}
                                <div className="location-section">
                                    <h3 className="section-title">
                                        <MapPin className="section-icon" />
                                        Weather Forecast (Optional)
                                    </h3>
                                    <p className="section-description">
                                        Provide your coordinates for weather-based recommendations
                                    </p>

                                    <button
                                        type="button"
                                        onClick={detectLocation}
                                        disabled={locationLoading}
                                        className="detect-location-btn"
                                    >
                                        {locationLoading ? (
                                            <>
                                                <Loader className="btn-icon spin" />
                                                Detecting...
                                            </>
                                        ) : (
                                            <>
                                                <MapPin className="btn-icon" />
                                                Auto-Detect Location
                                            </>
                                        )}
                                    </button>

                                    <div className="coords-grid">
                                        <div className="form-group">
                                            <label htmlFor="latitude" className="form-label-small">
                                                Latitude
                                            </label>
                                            <input
                                                type="number"
                                                id="latitude"
                                                name="latitude"
                                                value={formData.latitude}
                                                onChange={handleInputChange}
                                                step="0.000001"
                                                placeholder="e.g., 30.7333"
                                                className="form-input-small"
                                            />
                                        </div>
                                        <div className="form-group">
                                            <label htmlFor="longitude" className="form-label-small">
                                                Longitude
                                            </label>
                                            <input
                                                type="number"
                                                id="longitude"
                                                name="longitude"
                                                value={formData.longitude}
                                                onChange={handleInputChange}
                                                step="0.000001"
                                                placeholder="e.g., 76.7794"
                                                className="form-input-small"
                                            />
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Form Actions */}
                        <div className="form-actions">
                            <button
                                type="submit"
                                disabled={loading}
                                className="btn-primary"
                            >
                                {loading ? (
                                    <>
                                        <Loader className="btn-icon spin" />
                                        Analyzing...
                                    </>
                                ) : (
                                    <>
                                        <Sparkles className="btn-icon" />
                                        Get Crop Recommendations
                                    </>
                                )}
                            </button>
                            <button
                                type="button"
                                onClick={resetForm}
                                className="btn-secondary"
                                disabled={loading}
                            >
                                Reset
                            </button>
                        </div>
                    </form>
                </div>

                {/* Results Section */}
                {result && (
                    <>
                        {/* Results Header */}
                        <div className="results-header">
                            <div className="results-divider">
                                <div className="divider-line"></div>
                                <span className="divider-text">
                                    🎯 Top {result.recommendations?.length || 0} Recommendations
                                </span>
                                <div className="divider-line"></div>
                            </div>
                            <div className="season-badge">
                                <Calendar className="season-icon" />
                                <span>Season: <strong>{result.season}</strong></span>
                            </div>
                        </div>

                        {/* Crop Recommendations */}
                        <div className="recommendations-grid">
                            {result.recommendations?.map((crop, index) => (
                                <div key={crop.crop_name} className="crop-card">
                                    {/* Ranking Badge */}
                                    <div className="rank-badge">#{index + 1}</div>

                                    {/* Crop Header */}
                                    <div className="crop-header">
                                        <div className="crop-title-section">
                                            <h3 className="crop-name">{crop.crop_name}</h3>
                                            <div className={`crop-score ${getScoreClass(crop.final_score)}`}>
                                                {crop.final_score}/100
                                            </div>
                                        </div>
                                    </div>

                                    {/* Score Breakdown */}
                                    <div className="score-breakdown">
                                        <div className="score-item">
                                            <DollarSign className="score-icon market" />
                                            <div className="score-details">
                                                <span className="score-label">Market</span>
                                                <div className="score-value-row">
                                                    <span className="score-value">{crop.scores?.market || '—'}</span>
                                                    {getTrendIcon(crop.market_trend)}
                                                </div>
                                            </div>
                                        </div>

                                        <div className="score-item">
                                            <CloudRain className="score-icon weather" />
                                            <div className="score-details">
                                                <span className="score-label">Weather</span>
                                                <div className="score-value-row">
                                                    <span className="score-value">{crop.scores?.weather || '—'}</span>
                                                    {getWeatherBadge(crop.weather_suitability)}
                                                </div>
                                            </div>
                                        </div>

                                        <div className="score-item">
                                            <Calendar className="score-icon season" />
                                            <div className="score-details">
                                                <span className="score-label">Season</span>
                                                <span className="score-value">{crop.scores?.season || '—'}</span>
                                            </div>
                                        </div>

                                        <div className="score-item">
                                            <Leaf className="score-icon soil" />
                                            <div className="score-details">
                                                <span className="score-label">Soil</span>
                                                <div className="score-value-row">
                                                    <span className="score-value">{crop.scores?.soil || '—'}</span>
                                                    {getWeatherBadge(crop.soil_suitability)}
                                                </div>
                                            </div>
                                        </div>

                                        <div className="score-item">
                                            <AlertTriangle className="score-icon risk" />
                                            <div className="score-details">
                                                <span className="score-label">Risk</span>
                                                <div className="score-value-row">
                                                    <span className="score-value">{crop.scores?.risk || '—'}</span>
                                                    {getRiskBadge(crop.risk_level)}
                                                </div>
                                            </div>
                                        </div>
                                    </div>

                                    {/* Market Price & Action */}
                                    <div className="market-info-section">
                                        {crop.average_market_price_inr > 0 && (
                                            <div className="market-price">
                                                <DollarSign className="price-icon" />
                                                <div className="price-details">
                                                    <span className="price-label">Avg. Market Price</span>
                                                    <span className="price-value">₹{crop.average_market_price_inr.toLocaleString()}/quintal</span>
                                                </div>
                                            </div>
                                        )}
                                        
                                        {/* View Market Prices Button */}
                                        <button
                                            className="btn-market-view"
                                            onClick={() => loadMarketData(crop.crop_name, index)}
                                            disabled={loadingMarket}
                                        >
                                            {loadingMarket && expandedCrop === index ? (
                                                <><Loader className="w-4 h-4 animate-spin" /> Loading...</>
                                            ) : (
                                                <><ShoppingCart className="w-4 h-4" /> View Market Prices</>
                                            )}
                                        </button>
                                    </div>

                                    {/* Market Data Expansion */}
                                    {expandedCrop === index && marketData[crop.crop_name] && (
                                        <div className="market-expansion">
                                            <div className="market-expansion-header">
                                                <BarChart3 className="w-5 h-5" />
                                                <h4>Real-Time Market Insights for {crop.crop_name}</h4>
                                            </div>

                                            {/* Market Stats */}
                                            {marketData[crop.crop_name].insights && (
                                                <div className="market-stats-mini">
                                                    <div className="stat-mini">
                                                        <span className="stat-label">Price Trend</span>
                                                        <span className={`stat-value trend-${marketData[crop.crop_name].insights.trend?.direction}`}>
                                                            {marketData[crop.crop_name].insights.trend?.direction === 'rising' && <TrendingUp className="w-4 h-4" />}
                                                            {marketData[crop.crop_name].insights.trend?.direction === 'falling' && <TrendingDown className="w-4 h-4" />}
                                                            {marketData[crop.crop_name].insights.trend?.direction === 'stable' && <Minus className="w-4 h-4" />}
                                                            {marketData[crop.crop_name].insights.trend?.direction || 'N/A'}
                                                        </span>
                                                    </div>
                                                    <div className="stat-mini">
                                                        <span className="stat-label">Markets</span>
                                                        <span className="stat-value">
                                                            {marketData[crop.crop_name].insights.markets?.total_markets || 0}
                                                        </span>
                                                    </div>
                                                    <div className="stat-mini">
                                                        <span className="stat-label">Avg. Daily Supply</span>
                                                        <span className="stat-value">
                                                            {marketData[crop.crop_name].insights.arrival_stats?.avg_daily.toFixed(1) || 0} MT
                                                        </span>
                                                    </div>
                                                </div>
                                            )}

                                            {/* Top Markets */}
                                            {marketData[crop.crop_name].markets && marketData[crop.crop_name].markets.length > 0 && (
                                                <div className="top-markets-section">
                                                    <h5 className="top-markets-title">🏆 Top 5 Markets (Best Prices)</h5>
                                                    <div className="markets-list">
                                                        {marketData[crop.crop_name].markets.slice(0, 5).map((market, idx) => (
                                                            <div key={idx} className="market-item">
                                                                <div className="market-rank">#{idx + 1}</div>
                                                                <div className="market-details">
                                                                    <div className="market-name">{market.market}</div>
                                                                    <div className="market-location">{market.district}</div>
                                                                </div>
                                                                <div className="market-price-info">
                                                                    <div className="market-price-value">₹{market.modal_price.toLocaleString()}</div>
                                                                    <div className="market-arrival">{market.arrival_quantity.toFixed(1)} MT</div>
                                                                </div>
                                                            </div>
                                                        ))}
                                                    </div>
                                                    <p className="market-note">
                                                        💡 Based on real government mandi data. Consider transport costs when choosing markets.
                                                    </p>
                                                </div>
                                            )}
                                        </div>
                                    )}

                                    {/* Quantity Recommendations */}
                                    {crop.quantity_recommendation && Object.keys(crop.quantity_recommendation).length > 0 && (
                                        <div className="quantity-section">
                                            <h4 className="quantity-title">📊 Recommended Allocation</h4>
                                            <div className="quantity-grid">
                                                <div className="quantity-item">
                                                    <span className="quantity-label">Area</span>
                                                    <span className="quantity-value">
                                                        {crop.quantity_recommendation.recommended_area_hectares?.min || crop.quantity_recommendation.recommended_area_hectares} - {crop.quantity_recommendation.recommended_area_hectares?.max || crop.quantity_recommendation.recommended_area_hectares} ha
                                                    </span>
                                                </div>
                                                <div className="quantity-item">
                                                    <span className="quantity-label">Expected Yield</span>
                                                    <span className="quantity-value">
                                                        {crop.quantity_recommendation.expected_yield_tons?.min || crop.quantity_recommendation.expected_yield_range?.minimum_tonnes} - {crop.quantity_recommendation.expected_yield_tons?.max || crop.quantity_recommendation.expected_yield_range?.maximum_tonnes} tons
                                                    </span>
                                                </div>
                                                <div className="quantity-item">
                                                    <span className="quantity-label">Growing Period</span>
                                                    <span className="quantity-value">
                                                        {crop.quantity_recommendation.growing_period_days || crop.calendar_info?.growing_period_days || 90} days
                                                    </span>
                                                </div>
                                            </div>
                                            {crop.quantity_recommendation.reliability && (
                                                <div className="quantity-note">
                                                    <Info className="w-4 h-4" />
                                                    <span>Reliability: <strong>{crop.quantity_recommendation.reliability}</strong> ({crop.quantity_recommendation.based_on_records} historical records)</span>
                                                </div>
                                            )}
                                        </div>
                                    )}

                                    {/* Crop Details */}
                                    {crop.crop_details && (
                                        <div className="crop-details">
                                            <div className="detail-row">
                                                <Thermometer className="detail-icon" />
                                                <span>Temp: {crop.crop_details.temperature?.min}°C - {crop.crop_details.temperature?.max}°C</span>
                                            </div>
                                            <div className="detail-row">
                                                <CloudRain className="detail-icon" />
                                                <span>Rainfall: {crop.crop_details.rainfall?.min}-{crop.crop_details.rainfall?.max} mm</span>
                                            </div>
                                            {crop.crop_details.humidity && (
                                                <div className="detail-row">
                                                    <Droplets className="detail-icon" />
                                                    <span>Humidity: {crop.crop_details.humidity?.min}-{crop.crop_details.humidity?.max}%</span>
                                                </div>
                                            )}
                                            <div className="detail-row">
                                                <Info className="detail-icon" />
                                                <span>Water: {crop.crop_details.water_requirement}</span>
                                            </div>
                                        </div>
                                    )}

                                    {/* Calendar Info */}
                                    {crop.calendar_info && crop.calendar_info.sowing_period && (
                                        <div className="calendar-section">
                                            <h4 className="section-title">📅 Growing Calendar</h4>
                                            <div className="calendar-grid">
                                                <div className="calendar-item">
                                                    <span className="calendar-label">🌱 Sowing</span>
                                                    <span className="calendar-value">{crop.calendar_info.sowing_period}</span>
                                                </div>
                                                <div className="calendar-item">
                                                    <span className="calendar-label">🌾 Harvesting</span>
                                                    <span className="calendar-value">{crop.calendar_info.harvesting_period}</span>
                                                </div>
                                                {crop.calendar_info.season_name && (
                                                    <div className="calendar-item">
                                                        <span className="calendar-label">🍂 Season</span>
                                                        <span className="calendar-value">{crop.calendar_info.season_name}</span>
                                                    </div>
                                                )}
                                            </div>
                                        </div>
                                    )}

                                    {/* Optimal Conditions */}
                                    {crop.crop_details?.optimal_conditions && (
                                        <div className="optimal-section">
                                            <h4 className="section-title">🎯 Optimal Conditions</h4>
                                            <div className="optimal-grid">
                                                {crop.crop_details.optimal_conditions.temperature && (
                                                    <div className="optimal-item">
                                                        <Thermometer className="optimal-icon" />
                                                        <div className="optimal-details">
                                                            <span className="optimal-label">Temperature</span>
                                                            <span className="optimal-value">{crop.crop_details.optimal_conditions.temperature}°C</span>
                                                        </div>
                                                    </div>
                                                )}
                                                {crop.crop_details.optimal_conditions.rainfall && (
                                                    <div className="optimal-item">
                                                        <CloudRain className="optimal-icon" />
                                                        <div className="optimal-details">
                                                            <span className="optimal-label">Rainfall</span>
                                                            <span className="optimal-value">{crop.crop_details.optimal_conditions.rainfall} mm</span>
                                                        </div>
                                                    </div>
                                                )}
                                                {crop.crop_details.optimal_conditions.humidity && (
                                                    <div className="optimal-item">
                                                        <Droplets className="optimal-icon" />
                                                        <div className="optimal-details">
                                                            <span className="optimal-label">Humidity</span>
                                                            <span className="optimal-value">{crop.crop_details.optimal_conditions.humidity}%</span>
                                                        </div>
                                                    </div>
                                                )}
                                            </div>
                                        </div>
                                    )}

                                    {/* Soil Info */}
                                    {crop.soil_info && Object.keys(crop.soil_info).length > 0 && (
                                        <div className="soil-section">
                                            <h4 className="section-title">🌱 Soil Requirements ({result.state})</h4>
                                            <div className="soil-grid">
                                                {crop.soil_info.ph && (
                                                    <div className="soil-item">
                                                        <span className="soil-label">pH Level</span>
                                                        <span className="soil-value">{crop.soil_info.ph}</span>
                                                    </div>
                                                )}
                                                {crop.soil_info.nitrogen_n && (
                                                    <div className="soil-item">
                                                        <span className="soil-label">Nitrogen (N)</span>
                                                        <span className="soil-value">{crop.soil_info.nitrogen_n} kg/ha</span>
                                                    </div>
                                                )}
                                                {crop.soil_info.phosphorus_p && (
                                                    <div className="soil-item">
                                                        <span className="soil-label">Phosphorus (P)</span>
                                                        <span className="soil-value">{crop.soil_info.phosphorus_p} kg/ha</span>
                                                    </div>
                                                )}
                                                {crop.soil_info.potassium_k && (
                                                    <div className="soil-item">
                                                        <span className="soil-label">Potassium (K)</span>
                                                        <span className="soil-value">{crop.soil_info.potassium_k} kg/ha</span>
                                                    </div>
                                                )}
                                            </div>
                                        </div>
                                    )}

                                    {/* Historical Statistics */}
                                    {crop.crop_details?.statistics && crop.crop_details.statistics.historical_records > 0 && (
                                        <div className="stats-section">
                                            <h4 className="section-title">📊 Historical Data</h4>
                                            <div className="stats-grid">
                                                <div className="stat-item">
                                                    <Database className="stat-icon" />
                                                    <div className="stat-details">
                                                        <span className="stat-label">Records</span>
                                                        <span className="stat-value">{crop.crop_details.statistics.historical_records.toLocaleString()}</span>
                                                    </div>
                                                </div>
                                                <div className="stat-item">
                                                    <MapPin className="stat-icon" />
                                                    <div className="stat-details">
                                                        <span className="stat-label">States</span>
                                                        <span className="stat-value">{crop.crop_details.statistics.states_grown}</span>
                                                    </div>
                                                </div>
                                                <div className="stat-item">
                                                    <Sprout className="stat-icon" />
                                                    <div className="stat-details">
                                                        <span className="stat-label">Avg. Yield</span>
                                                        <span className="stat-value">{crop.crop_details.statistics.avg_yield_per_hectare.toFixed(2)} t/ha</span>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    )}
                                </div>
                            ))}
                        </div>

                        {/* Disclaimer */}
                        <div className="disclaimer">
                            <AlertCircle className="disclaimer-icon" />
                            <div>
                                <p className="disclaimer-title">Important Notice</p>
                                <p className="disclaimer-text">
                                    {result.disclaimer || "This is AI-based guidance. Please consult local agriculture officer."}
                                </p>
                            </div>
                        </div>
                    </>
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

export default CropPlanning;
