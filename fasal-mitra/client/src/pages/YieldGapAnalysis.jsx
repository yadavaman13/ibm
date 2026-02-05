import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { TrendingUp, AlertCircle, Target, BarChart3, Award, Lightbulb, ArrowUp, ArrowDown, Minus } from 'lucide-react';
import '../styles/yield-gap-analysis.css';
import { analyzeYieldGap, getCrops, getStates, getSeasons } from '../services/gapAnalysisService';

const YieldGapAnalysis = () => {
    const { t } = useTranslation(['pages', 'common']);
    const [analysisMode, setAnalysisMode] = useState('post-harvest'); // 'post-harvest' or 'pre-harvest'
    const [formData, setFormData] = useState({
        crop: '',
        state: '',
        season: '',
        // Post-harvest fields
        actual_yield: '',
        // Pre-harvest fields
        area: '',
        fertilizer: '',
        pesticide: '',
    });

    const [crops, setCrops] = useState([]);
    const [states, setStates] = useState([]);
    const [seasons, setSeasons] = useState([]);
    const [results, setResults] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    // Load dropdown data
    useEffect(() => {
        const loadData = async () => {
            try {
                const [cropsData, statesData, seasonsData] = await Promise.all([
                    getCrops(),
                    getStates(),
                    getSeasons()
                ]);
                setCrops(cropsData);
                setStates(statesData);
                setSeasons(seasonsData);
            } catch (err) {
                console.error('Error loading data:', err);
                setError('Failed to load form data');
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

    const handleModeChange = (mode) => {
        setAnalysisMode(mode);
        setResults(null);
        setError(null);
        // Clear mode-specific fields
        if (mode === 'post-harvest') {
            setFormData(prev => ({ ...prev, area: '', fertilizer: '', pesticide: '' }));
        } else {
            setFormData(prev => ({ ...prev, actual_yield: '' }));
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        setResults(null);

        try {
            // Prepare payload based on mode
            const payload = {
                crop: formData.crop,
                state: formData.state,
                season: formData.season || null,
            };

            if (analysisMode === 'post-harvest') {
                payload.actual_yield = parseFloat(formData.actual_yield);
            } else {
                payload.area = parseFloat(formData.area);
                payload.fertilizer = parseFloat(formData.fertilizer);
                payload.pesticide = parseFloat(formData.pesticide);
            }

            const result = await analyzeYieldGap(payload);
            setResults(result);
        } catch (err) {
            setError(err.message || 'Failed to analyze yield gap');
        } finally {
            setLoading(false);
        }
    };

    const getPerformanceColor = (level) => {
        switch (level) {
            case 'Excellent': return 'excellent';
            case 'Good': return 'good';
            case 'Below Average': return 'below-average';
            default: return 'neutral';
        }
    };

    const getGapIcon = (gapVsAvg) => {
        if (gapVsAvg > 10) return <ArrowUp className="gap-icon positive" />;
        if (gapVsAvg < -10) return <ArrowDown className="gap-icon negative" />;
        return <Minus className="gap-icon neutral" />;
    };

    return (
        <div className="page-container">
            {/* Header */}
            <div className="page-header">
                <TrendingUp className="page-header-icon" />
                <div>
                    <h1 className="page-header-title">{t('yieldGapAnalysis.title')}</h1>
                    <p className="page-header-subtitle">{t('yieldGapAnalysis.subtitle')}</p>
                </div>
            </div>

            {/* Mode Selector */}
            <div className="mode-selector">
                <button
                    className={`mode-button ${analysisMode === 'post-harvest' ? 'active' : ''}`}
                    onClick={() => handleModeChange('post-harvest')}
                >
                    <Award className="mode-icon" />
                    <div className="mode-content">
                        <span className="mode-title">{t('yieldGapAnalysis.postHarvest')}</span>
                        <span className="mode-description">{t('yieldGapAnalysis.actualYieldKnown')}</span>
                    </div>
                </button>
                <button
                    className={`mode-button ${analysisMode === 'pre-harvest' ? 'active' : ''}`}
                    onClick={() => handleModeChange('pre-harvest')}
                >
                    <Target className="mode-icon" />
                    <div className="mode-content">
                        <span className="mode-title">{t('yieldGapAnalysis.preHarvest')}</span>
                        <span className="mode-description">{t('yieldGapAnalysis.predictAndPlan')}</span>
                    </div>
                </button>
            </div>

            {/* Analysis Form */}
            <div className="analysis-form-card">
                <form onSubmit={handleSubmit} className="analysis-form">
                    {/* Basic Information Row */}
                    <div className="form-row">
                        <div className="form-group">
                            <label htmlFor="crop">{t('yieldGapAnalysis.crop')} *</label>
                            <select
                                id="crop"
                                name="crop"
                                value={formData.crop}
                                onChange={handleInputChange}
                                required
                            >
                                <option value="">{t('pages:yieldGapAnalysis.selectCrop')}</option>
                                {crops.map(crop => (
                                    <option key={crop} value={crop}>{t(`common:crops.${crop}`)}</option>
                                ))}
                            </select>
                        </div>

                        <div className="form-group">
                            <label htmlFor="state">{t('yieldGapAnalysis.state')} *</label>
                            <select
                                id="state"
                                name="state"
                                value={formData.state}
                                onChange={handleInputChange}
                                required
                            >
                                <option value="">{t('pages:yieldGapAnalysis.selectState')}</option>
                                {states.map(state => (
                                    <option key={state} value={state}>{t(`common:states.${state}`)}</option>
                                ))}
                            </select>
                        </div>

                        <div className="form-group">
                            <label htmlFor="season">{t('yieldGapAnalysis.season')}</label>
                            <select
                                id="season"
                                name="season"
                                value={formData.season}
                                onChange={handleInputChange}
                            >
                                <option value="">{t('pages:yieldGapAnalysis.selectSeason')}</option>
                                {seasons.map(season => (
                                    <option key={season} value={season}>{t(`common:seasons.${season}`)}</option>
                                ))}
                            </select>
                        </div>
                    </div>

                    {/* Mode-Specific Fields */}
                    {analysisMode === 'post-harvest' ? (
                        <div className="form-row">
                            <div className="form-group full-width">
                                <label htmlFor="actual_yield">{t('yieldGapAnalysis.actualYield')} *</label>
                                <input
                                    type="number"
                                    id="actual_yield"
                                    name="actual_yield"
                                    value={formData.actual_yield}
                                    onChange={handleInputChange}
                                    placeholder="e.g., 2.5"
                                    step="0.01"
                                    min="0"
                                    required
                                />
                            </div>
                        </div>
                    ) : (
                        <div className="form-row">
                            <div className="form-group">
                                <label htmlFor="area">{t('yieldGapAnalysis.area')} *</label>
                                <input
                                    type="number"
                                    id="area"
                                    name="area"
                                    value={formData.area}
                                    onChange={handleInputChange}
                                    placeholder="e.g., 50"
                                    step="0.01"
                                    min="0"
                                    required
                                />
                            </div>

                            <div className="form-group">
                                <label htmlFor="fertilizer">{t('yieldGapAnalysis.fertilizer')} *</label>
                                <input
                                    type="number"
                                    id="fertilizer"
                                    name="fertilizer"
                                    value={formData.fertilizer}
                                    onChange={handleInputChange}
                                    placeholder="e.g., 20000"
                                    step="1"
                                    min="0"
                                    required
                                />
                            </div>

                            <div className="form-group">
                                <label htmlFor="pesticide">{t('yieldGapAnalysis.pesticide')} *</label>
                                <input
                                    type="number"
                                    id="pesticide"
                                    name="pesticide"
                                    value={formData.pesticide}
                                    onChange={handleInputChange}
                                    placeholder="e.g., 300"
                                    step="1"
                                    min="0"
                                    required
                                />
                            </div>
                        </div>
                    )}

                    {/* Error Message */}
                    {error && (
                        <div className="error-message">
                            <AlertCircle className="error-icon" />
                            <span>{error}</span>
                        </div>
                    )}

                    {/* Submit Button */}
                    <button type="submit" className="submit-button" disabled={loading}>
                        {loading ? (
                            <>
                                <div className="spinner"></div>
                                <span>{t('yieldGapAnalysis.analyzing')}</span>
                            </>
                        ) : (
                            <>
                                <BarChart3 className="button-icon" />
                                <span>{t('yieldGapAnalysis.analyzeYieldGap')}</span>
                            </>
                        )}
                    </button>
                </form>
            </div>

            {/* Results */}
            {results && (
                <div className="results-section">
                    {/* Performance Overview */}
                    <div className="result-card">
                        <div className="card-header">
                            <Target className="header-icon" />
                            <h3 className="card-title">Performance Overview</h3>
                        </div>

                        <div className="overview-grid">
                            <div className="overview-item">
                                <span className="overview-label">
                                    {results.analysis_type === 'post_harvest' ? 'Actual Yield' : 'Predicted Yield'}
                                </span>
                                <span className="overview-value">{results.yield_analyzed} t/ha</span>
                            </div>

                            <div className="overview-item">
                                <span className="overview-label">Regional Average</span>
                                <span className="overview-value">{results.average_yield} t/ha</span>
                            </div>

                            <div className="overview-item">
                                <span className="overview-label">Top 10% Yield</span>
                                <span className="overview-value highlight">{results.potential_yield} t/ha</span>
                            </div>

                            <div className="overview-item">
                                <span className="overview-label">Performance Level</span>
                                <span className={`performance-badge ${getPerformanceColor(results.performance_level)}`}>
                                    {results.performance_level}
                                </span>
                            </div>
                        </div>
                    </div>

                    {/* Gap Analysis */}
                    <div className="result-card">
                        <div className="card-header">
                            <BarChart3 className="header-icon" />
                            <h3 className="card-title">Gap Analysis</h3>
                        </div>

                        <div className="gap-metrics">
                            <div className="gap-metric">
                                <div className="gap-metric-header">
                                    {getGapIcon(results.gap_vs_average)}
                                    <span className="gap-metric-label">vs. Regional Average</span>
                                </div>
                                <span className={`gap-metric-value ${results.gap_vs_average > 0 ? 'positive' : 'negative'}`}>
                                    {results.gap_vs_average > 0 ? '+' : ''}{results.gap_vs_average.toFixed(1)}%
                                </span>
                            </div>

                            <div className="gap-metric">
                                <div className="gap-metric-header">
                                    {getGapIcon(-results.gap_percentage)}
                                    <span className="gap-metric-label">vs. Top 10% Performers</span>
                                </div>
                                <span className={`gap-metric-value ${results.gap_percentage > 0 ? 'negative' : 'positive'}`}>
                                    {results.gap_percentage > 0 ? '-' : '+'}{Math.abs(results.gap_percentage).toFixed(1)}%
                                </span>
                            </div>

                            <div className="gap-metric">
                                <div className="gap-metric-header">
                                    <Target className="gap-icon" />
                                    <span className="gap-metric-label">Yield Potential</span>
                                </div>
                                <span className="gap-metric-value neutral">
                                    {results.yield_potential_percentage.toFixed(1)}%
                                </span>
                            </div>

                            <div className="gap-metric">
                                <div className="gap-metric-header">
                                    <ArrowUp className="gap-icon" />
                                    <span className="gap-metric-label">Potential Increase</span>
                                </div>
                                <span className="gap-metric-value highlight">
                                    +{results.estimated_increase.toFixed(2)} t/ha
                                </span>
                            </div>
                        </div>
                    </div>

                    {/* Benchmarks */}
                    <div className="result-card">
                        <div className="card-header">
                            <Award className="header-icon" />
                            <h3 className="card-title">Regional Benchmarks</h3>
                        </div>

                        <div className="benchmarks-list">
                            <div className="benchmark-item">
                                <span className="benchmark-label">Average Yield</span>
                                <div className="benchmark-bar">
                                    <div 
                                        className="benchmark-fill average"
                                        style={{ width: `${(results.benchmarks.average / results.benchmarks.maximum) * 100}%` }}
                                    ></div>
                                </div>
                                <span className="benchmark-value">{results.benchmarks.average} t/ha</span>
                            </div>

                            <div className="benchmark-item">
                                <span className="benchmark-label">Top 25% Yield</span>
                                <div className="benchmark-bar">
                                    <div 
                                        className="benchmark-fill good"
                                        style={{ width: `${(results.benchmarks.top_25_percent / results.benchmarks.maximum) * 100}%` }}
                                    ></div>
                                </div>
                                <span className="benchmark-value">{results.benchmarks.top_25_percent} t/ha</span>
                            </div>

                            <div className="benchmark-item">
                                <span className="benchmark-label">Top 10% Yield</span>
                                <div className="benchmark-bar">
                                    <div 
                                        className="benchmark-fill excellent"
                                        style={{ width: `${(results.benchmarks.top_10_percent / results.benchmarks.maximum) * 100}%` }}
                                    ></div>
                                </div>
                                <span className="benchmark-value">{results.benchmarks.top_10_percent} t/ha</span>
                            </div>

                            <div className="benchmark-item">
                                <span className="benchmark-label">Maximum Achieved</span>
                                <div className="benchmark-bar">
                                    <div className="benchmark-fill maximum" style={{ width: '100%' }}></div>
                                </div>
                                <span className="benchmark-value">{results.benchmarks.maximum} t/ha</span>
                            </div>
                        </div>
                    </div>

                    {/* Top Performers */}
                    <div className="result-card">
                        <div className="card-header">
                            <Award className="header-icon" />
                            <h3 className="card-title">Top Performer Practices</h3>
                        </div>

                        <div className="practices-grid">
                            {results.top_performers.practices.map((practice, index) => (
                                <div key={index} className="practice-item">
                                    <Lightbulb className="practice-icon" />
                                    <span className="practice-text">{practice}</span>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Recommendations */}
                    <div className="result-card full-width">
                        <div className="card-header">
                            <Lightbulb className="header-icon" />
                            <h3 className="card-title">Improvement Recommendations</h3>
                        </div>

                        <div className="recommendations-list">
                            {results.improvement_steps.map((step, index) => (
                                <div key={index} className="recommendation-item">
                                    <div className="recommendation-number">{index + 1}</div>
                                    <span className="recommendation-text">{step}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default YieldGapAnalysis;
