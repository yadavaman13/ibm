import React, { useState, useEffect } from 'react';
import { Sprout, Droplets, TestTube, CheckCircle, AlertCircle, Loader, TrendingUp } from 'lucide-react';
import '../styles/soil-analysis.css';
import * as soilService from '../services/soilService';

const SoilAnalysis = () => {
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
                    <div className="page-header-content">
                        <div className="page-icon-wrapper">
                            <TestTube className="page-icon" />
                        </div>
                        <h1 className="page-header-title">Soil Analysis</h1>
                    </div>
                    <p className="page-header-subtitle">
                        Analyze soil quality and get crop recommendations based on NPK values and pH levels
                    </p>
                    {serverStatus === false && (
                        <div className="server-alert">
                            <AlertCircle className="alert-icon" />
                            <span>Backend server is not running. Please start the server at http://localhost:8000</span>
                        </div>
                    )}
                </div>

                {/* Input Form */}
                <div className="soil-form-card">
                    <div className="form-header">
                        <h2 className="form-title">Select Location & Crop</h2>
                        <p className="form-subtitle">Choose your state and crop to analyze soil suitability</p>
                    </div>

                    <form onSubmit={handleSubmit} className="soil-form">
                        <div className="form-inputs-grid">
                            {/* State Selection */}
                            <div className="form-group">
                                <label htmlFor="state" className="form-label">
                                    State <span className="required">*</span>
                                </label>
                                <select
                                    id="state"
                                    name="state"
                                    value={formData.state}
                                    onChange={handleInputChange}
                                    required
                                    className="form-select"
                                >
                                    <option value="">Select state...</option>
                                    {states.map(state => (
                                        <option key={state} value={state}>{state}</option>
                                    ))}
                                </select>
                            </div>

                            {/* Crop Selection */}
                            <div className="form-group">
                                <label htmlFor="crop" className="form-label">
                                    Crop <span className="required">*</span>
                                </label>
                                <select
                                    id="crop"
                                    name="crop"
                                    value={formData.crop}
                                    onChange={handleInputChange}
                                    required
                                    className="form-select"
                                >
                                    <option value="">Select crop...</option>
                                    {crops.map(crop => (
                                        <option key={crop} value={crop}>{crop}</option>
                                    ))}
                                </select>
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
                                        <TestTube className="btn-icon" />
                                        Analyze Soil
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

                {/* Results Section */}
                {results && (
                    <>
                        {/* Top Row: Soil Composition & Suitability */}
                        <div className="results-grid">
                            {/* Soil Composition Card */}
                            <div className="result-card">
                                <div className="card-header">
                                    <Droplets className="header-icon" />
                                    <h3 className="card-title">Soil Composition</h3>
                                </div>

                                <div className="npk-grid">
                                    {/* Nitrogen */}
                                    <div className="npk-item">
                                        <div className="npk-header">
                                            <span className="npk-label">Nitrogen (N)</span>
                                            <span className="npk-value">{results.soil.N || 0}</span>
                                        </div>
                                        <div className="progress-bar">
                                            <div
                                                className="progress-bar-fill nitrogen"
                                                style={{ width: `${getNPKLevel(results.soil.N || 0, 'N')}%` }}
                                            ></div>
                                        </div>
                                    </div>

                                    {/* Phosphorus */}
                                    <div className="npk-item">
                                        <div className="npk-header">
                                            <span className="npk-label">Phosphorus (P)</span>
                                            <span className="npk-value">{results.soil.P || 0}</span>
                                        </div>
                                        <div className="progress-bar">
                                            <div
                                                className="progress-bar-fill phosphorus"
                                                style={{ width: `${getNPKLevel(results.soil.P || 0, 'P')}%` }}
                                            ></div>
                                        </div>
                                    </div>

                                    {/* Potassium */}
                                    <div className="npk-item">
                                        <div className="npk-header">
                                            <span className="npk-label">Potassium (K)</span>
                                            <span className="npk-value">{results.soil.K || 0}</span>
                                        </div>
                                        <div className="progress-bar">
                                            <div
                                                className="progress-bar-fill potassium"
                                                style={{ width: `${getNPKLevel(results.soil.K || 0, 'K')}%` }}
                                            ></div>
                                        </div>
                                    </div>

                                    {/* pH Level */}
                                    <div className="ph-section">
                                        <div className="ph-header">
                                            <span className="ph-label">pH Level</span>
                                            <div className="ph-value-wrapper">
                                                <span className="ph-value">{results.soil.pH || 7.0}</span>
                                                <span className={`ph-badge ${getpHLevel(results.soil.pH || 7.0).class}`}>
                                                    {getpHLevel(results.soil.pH || 7.0).label}
                                                </span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* Suitability Score Card */}
                            <div className="result-card">
                                <div className="card-header">
                                    <TrendingUp className="header-icon" />
                                    <h3 className="card-title">Suitability Score</h3>
                                </div>

                                <div className="suitability-content">
                                    <div className={`score-circle ${getSuitabilityLevel(results.suitability?.suitability_score || 0).class}`}>
                                        <div className="score-value">
                                            {Math.round(results.suitability?.suitability_score || 0)}
                                        </div>
                                        <div className="score-max">/100</div>
                                    </div>

                                    <div className={`suitability-badge ${getSuitabilityLevel(results.suitability?.suitability_score || 0).class}`}>
                                        {getSuitabilityLevel(results.suitability?.suitability_score || 0).label}
                                    </div>

                                    <p className="suitability-description">
                                        {formData.crop} is {getSuitabilityLevel(results.suitability?.suitability_score || 0).label.toLowerCase()}
                                        {' '}for cultivation in {formData.state}
                                    </p>
                                </div>
                            </div>
                        </div>

                        {/* Recommended Crops Card */}
                        <div className="result-card full-width">
                            <div className="card-header">
                                <Sprout className="header-icon" />
                                <h3 className="card-title">Recommended Crops for {formData.state}</h3>
                            </div>

                            <div className="recommendations-grid">
                                {(results.recommendations?.recommended_crops || []).slice(0, 6).map((item, index) => (
                                    <div key={index} className="recommendation-item">
                                        <CheckCircle className="recommendation-icon" />
                                        <div className="recommendation-content">
                                            <span className="recommendation-text">{item.crop}</span>
                                            <span className="recommendation-score">{item.suitability_score}% match</span>
                                        </div>
                                    </div>
                                ))}
                            </div>

                            {results.recommendations?.recommended_crops && results.recommendations.recommended_crops.length > 6 && (
                                <p className="recommendations-note">
                                    +{results.recommendations.recommended_crops.length - 6} more crops recommended
                                </p>
                            )}
                        </div>
                    </>
                )}
            </div>
        </div>
    );
};

export default SoilAnalysis;
