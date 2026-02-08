import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { 
  TrendingUp, 
  DollarSign, 
  MapPin, 
  Calendar, 
  Package, 
  AlertCircle, 
  Loader, 
  BarChart3,
  TrendingDown,
  Minus,
  CheckCircle,
  Info
} from 'lucide-react';
import {
  getAvailableCommodities,
  getPriceForecast,
  compareMarkets,
  getMarketRecommendation,
  getCommodityInsights
} from '../services/marketService';
import '../styles/pages.css';

const MarketIntelligence = () => {
  const { t } = useTranslation(['pages', 'common']);
  
  // State management
  const [commodities, setCommodities] = useState([]);
  const [selectedCommodity, setSelectedCommodity] = useState('');
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('forecast'); // forecast, comparison, recommendation
  
  // Forecast data
  const [forecast, setForecast] = useState(null);
  const [forecastDays, setForecastDays] = useState(7);
  
  // Market comparison data
  const [markets, setMarkets] = useState([]);
  const [comparisonFilters, setComparisonFilters] = useState({
    district: '',
    variety: ''
  });
  
  // Available filter options
  const [availableDistricts, setAvailableDistricts] = useState([]);
  const [availableVarieties, setAvailableVarieties] = useState([]);
  
  // Recommendation data
  const [recommendation, setRecommendation] = useState(null);
  const [recommendationInputs, setRecommendationInputs] = useState({
    userDistrict: '',
    quantity: ''
  });
  
  // Insights data
  const [insights, setInsights] = useState(null);
  
  const [error, setError] = useState(null);
  
  // Load commodities on mount
  useEffect(() => {
    loadCommodities();
  }, []);
  
  // Load data when commodity changes
  useEffect(() => {
    if (selectedCommodity) {
      loadAllData();
    }
  }, [selectedCommodity]);
  
  const loadCommodities = async () => {
    try {
      const data = await getAvailableCommodities();
      setCommodities(data.commodities || []);
      
      // Auto-select first commodity with good data
      const goodCommodity = data.commodities?.find(c => c.record_count > 500);
      if (goodCommodity) {
        setSelectedCommodity(goodCommodity.name);
      }
    } catch (err) {
      console.error('Error loading commodities:', err);
      setError('Failed to load commodities. Please check if backend is running.');
    }
  };
  
  const loadAllData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Load forecast
      await loadForecast();
      
      // Load market comparison
      await loadMarkets();
      
      // Load insights
      await loadInsights();
    } catch (err) {
      console.error('Error loading data:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };
  
  const loadForecast = async () => {
    try {
      const data = await getPriceForecast(selectedCommodity, forecastDays);
      setForecast(data);
    } catch (err) {
      console.error('Error loading forecast:', err);
    }
  };
  
  const loadMarkets = async () => {
    try {
      const data = await compareMarkets(
        selectedCommodity,
        null,
        comparisonFilters.district || null,
        comparisonFilters.variety || null
      );
      const marketList = data.markets || [];
      setMarkets(marketList);
      
      // Extract unique districts and varieties for filters
      if (marketList.length > 0) {
        const districts = [...new Set(marketList.map(m => m.district))].sort();
        const varieties = [...new Set(marketList.map(m => m.variety))].sort();
        setAvailableDistricts(districts);
        setAvailableVarieties(varieties);
      }
    } catch (err) {
      console.error('Error loading markets:', err);
    }
  };
  
  const loadInsights = async () => {
    try {
      const data = await getCommodityInsights(selectedCommodity, 30);
      setInsights(data);
    } catch (err) {
      console.error('Error loading insights:', err);
    }
  };
  
  const loadRecommendation = async () => {
    setLoading(true);
    try {
      const data = await getMarketRecommendation(
        selectedCommodity,
        recommendationInputs.userDistrict || null,
        recommendationInputs.quantity ? parseFloat(recommendationInputs.quantity) : null
      );
      setRecommendation(data);
    } catch (err) {
      console.error('Error loading recommendation:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };
  
  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0
    }).format(price);
  };
  
  const getTrendIcon = (trend) => {
    if (!trend) return <Minus className="w-5 h-5" />;
    
    switch (trend.direction) {
      case 'rising':
        return <TrendingUp className="w-5 h-5 text-green-600" />;
      case 'falling':
        return <TrendingDown className="w-5 h-5 text-red-600" />;
      default:
        return <Minus className="w-5 h-5 text-gray-600" />;
    }
  };
  
  const getTrendColor = (trend) => {
    if (!trend) return 'text-gray-600';
    
    switch (trend.direction) {
      case 'rising':
        return 'text-green-600';
      case 'falling':
        return 'text-red-600';
      default:
        return 'text-gray-600';
    }
  };
  
  // Group commodities by category
  const groupedCommodities = commodities.reduce((acc, commodity) => {
    const category = commodity.category || 'Other';
    if (!acc[category]) {
      acc[category] = [];
    }
    acc[category].push(commodity);
    return acc;
  }, {});
  
  return (
    <div className="page-container">
      <div className="page-header">
        <TrendingUp className="page-header-icon" />
        <div>
          <h1 className="page-header-title">Market Intelligence</h1>
          <p className="page-header-subtitle">
            AI-Powered Price Forecasting & Market Recommendations
          </p>
        </div>
      </div>
      
      {error && (
        <div className="alert alert-error">
          <AlertCircle className="w-5 h-5" />
          <span>{error}</span>
        </div>
      )}
      
      {/* Commodity Selector */}
      <div className="market-commodity-selector">
        <label className="market-commodity-label">
          <Package className="w-5 h-5" />
          <span>Select Commodity</span>
        </label>
        <select
          className="market-commodity-dropdown"
          value={selectedCommodity}
          onChange={(e) => setSelectedCommodity(e.target.value)}
        >
          <option value="">-- Select Commodity --</option>
          {Object.entries(groupedCommodities).map(([category, items]) => (
            <optgroup key={category} label={category}>
              {items.map((commodity) => (
                <option key={commodity.name} value={commodity.name}>
                  {commodity.name} ({commodity.record_count} records)
                </option>
              ))}
            </optgroup>
          ))}
        </select>
      </div>
      
      {selectedCommodity && (
        <>
          {/* Market Overview Cards */}
          {insights && (
            <div className="market-stats-grid">
              <div className="stats-card">
                <div className="stats-label">Current Price</div>
                <div className="stats-value">
                  {formatPrice(insights.price_stats?.current_avg || 0)}
                </div>
                <div className="stats-change">
                  per quintal
                </div>
              </div>
              
              <div className="stats-card">
                <div className="stats-label">Price Trend</div>
                <div className="flex items-center justify-center">
                  {getTrendIcon(insights.trend)}
                  <span className={`ml-2 text-2xl font-bold ${getTrendColor(insights.trend)}`}>
                    {insights.trend?.direction || 'N/A'}
                  </span>
                </div>
                {insights.trend?.change_percent && (
                  <div className={`stats-change ${insights.trend.change_percent > 0 ? 'text-green-600' : 'text-red-600'}`}>
                    {insights.trend.change_percent.toFixed(1)}% (7 days)
                  </div>
                )}
              </div>
              
              <div className="stats-card">
                <div className="stats-label">Daily Supply</div>
                <div className="stats-value">
                  {insights.arrival_stats?.avg_daily.toFixed(1) || 0} MT
                </div>
                <div className="stats-change">
                  average arrival
                </div>
              </div>
              
              <div className="stats-card">
                <div className="stats-label">Markets Available</div>
                <div className="stats-value">
                  {insights.markets?.total_markets || 0}
                </div>
                <div className="stats-change">
                  {insights.markets?.total_districts || 0} districts
                </div>
              </div>
            </div>
          )}
          
          {/* Tabs */}
          <div className="market-tabs-container">
            <button
              className={`tab-button ${activeTab === 'forecast' ? 'active' : ''}`}
              onClick={() => setActiveTab('forecast')}
            >
              <BarChart3 className="w-4 h-4" />
              Price Forecast
            </button>
            <button
              className={`tab-button ${activeTab === 'comparison' ? 'active' : ''}`}
              onClick={() => setActiveTab('comparison')}
            >
              <DollarSign className="w-4 h-4" />
              Market Comparison
            </button>
            <button
              className={`tab-button ${activeTab === 'recommendation' ? 'active' : ''}`}
              onClick={() => setActiveTab('recommendation')}
            >
              <MapPin className="w-4 h-4" />
              Best Markets
            </button>
          </div>
          
          {/* Forecast Tab */}
          {activeTab === 'forecast' && forecast && (
            <div className="market-card">
              <h3 className="text-xl font-semibold mb-4 flex items-center">
                <TrendingUp className="w-5 h-5 mr-2" />
                {forecastDays}-Day Price Forecast
              </h3>
              
              {/* Forecast Chart - Simple Table View */}
              <div className="market-table-container">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Date
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Predicted Price
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Range
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {forecast.forecast?.map((item, idx) => (
                      <tr key={idx} className={idx === 0 ? 'bg-green-50' : ''}>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                          {new Date(item.date).toLocaleDateString('en-IN', {
                            weekday: 'short',
                            month: 'short',
                            day: 'numeric'
                          })}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-bold text-green-600">
                          {formatPrice(item.predicted_price)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {formatPrice(item.lower_bound)} - {formatPrice(item.upper_bound)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              
              {/* Trend Summary */}
              <div className="mt-6 p-4 bg-blue-50 rounded-lg">
                <div className="flex items-start">
                  <Info className="w-5 h-5 text-blue-600 mr-3 mt-0.5" />
                  <div>
                    <h4 className="font-semibold text-blue-900 mb-2">Market Insight</h4>
                    <p className="text-blue-700">
                      Price trend is <strong>{forecast.trend?.direction}</strong> with a slope of {forecast.trend?.slope.toFixed(2)}.
                      {forecast.trend?.direction === 'rising' && 
                        ' Prices are expected to increase - consider holding stock if possible.'}
                      {forecast.trend?.direction === 'falling' && 
                        ' Prices are expected to decrease - consider selling soon.'}
                      {forecast.trend?.direction === 'stable' && 
                        ' Prices are stable - good time for regular sales.'}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          )}
          
          {/* Market Comparison Tab */}
          {activeTab === 'comparison' && (
            <div className="market-card">
              <h3 className="text-xl font-semibold mb-4 flex items-center">
                <DollarSign className="w-5 h-5 mr-2" />
                Market Price Comparison
              </h3>
              
              {/* Filters */}
              <div className="market-filter-grid">
                <div>
                  <label className="form-label">Filter by District</label>
                  <select
                    className="form-select"
                    value={comparisonFilters.district}
                    onChange={(e) => setComparisonFilters({
                      ...comparisonFilters,
                      district: e.target.value
                    })}
                  >
                    <option value="">All Districts</option>
                    {availableDistricts.map((district) => (
                      <option key={district} value={district}>
                        {district}
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="form-label">Filter by Variety</label>
                  <select
                    className="form-select"
                    value={comparisonFilters.variety}
                    onChange={(e) => setComparisonFilters({
                      ...comparisonFilters,
                      variety: e.target.value
                    })}
                  >
                    <option value="">All Varieties</option>
                    {availableVarieties.map((variety) => (
                      <option key={variety} value={variety}>
                        {variety}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
              
              <button
                onClick={loadMarkets}
                className="btn-primary mb-4"
                disabled={loading}
              >
                {loading ? (
                  <>
                    <Loader className="w-5 h-5 animate-spin mr-2" />
                    Loading...
                  </>
                ) : (
                  'Apply Filters'
                )}
              </button>
              
              {/* Markets Table */}
              {markets.length > 0 ? (
                <div className="market-table-container">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Rank
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          District
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Market
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Modal Price
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Arrival
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Variety
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {markets.slice(0, 10).map((market, idx) => (
                        <tr key={idx} className={idx === 0 ? 'bg-green-50' : ''}>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span className={`inline-flex items-center justify-center w-8 h-8 rounded-full ${
                              idx === 0 ? 'bg-green-600 text-white' : 
                              idx === 1 ? 'bg-green-500 text-white' : 
                              idx === 2 ? 'bg-green-400 text-white' : 
                              'bg-gray-200 text-gray-700'
                            } font-bold text-sm`}>
                              {idx + 1}
                            </span>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                            {market.district}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                            {market.market}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-bold text-green-600">
                            {formatPrice(market.modal_price)}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {market.arrival_quantity.toFixed(1)} MT
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {market.variety}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <div className="text-center py-8 text-gray-500">
                  No markets found. Try adjusting filters.
                </div>
              )}
            </div>
          )}
          
          {/* Recommendation Tab */}
          {activeTab === 'recommendation' && (
            <div className="market-recommendation-container">
              <div className="market-card">
                <h3 className="text-xl font-semibold mb-4 flex items-center">
                  <TrendingUp className="w-5 h-5 mr-2 text-green-600" />
                  Get Smart Recommendations
                </h3>
                
                <div className="market-input-grid">
                  <div>
                    <label className="form-label">Your District (Optional)</label>
                    <select
                      className="form-select"
                      value={recommendationInputs.userDistrict}
                      onChange={(e) => setRecommendationInputs({
                        ...recommendationInputs,
                        userDistrict: e.target.value
                      })}
                    >
                      <option value="">Select your district</option>
                      {availableDistricts.map((district) => (
                        <option key={district} value={district}>
                          {district}
                        </option>
                      ))}
                    </select>
                    <p className="text-sm text-gray-500 mt-1">
                      For local market prioritization
                    </p>
                  </div>
                  <div>
                    <label className="form-label">Quantity in MT (Optional)</label>
                    <input
                      type="number"
                      className="form-input"
                      placeholder="e.g., 5"
                      value={recommendationInputs.quantity}
                      onChange={(e) => setRecommendationInputs({
                        ...recommendationInputs,
                        quantity: e.target.value
                      })}
                    />
                    <p className="text-sm text-gray-500 mt-1">
                      For profit calculation
                    </p>
                  </div>
                </div>
              
              <button
                onClick={loadRecommendation}
                className="btn-primary mb-6"
                disabled={loading}
              >
                {loading ? (
                  <>
                    <Loader className="w-5 h-5 animate-spin mr-2" />
                    Loading...
                  </>
                ) : (
                  'Get Recommendation'
                )}
              </button>
              </div>
              
              {/* Recommendation Result */}
              {recommendation && (
                <div className="market-recommendation-results">
                  {/* Best Market Card */}
                  <div className="market-best-card">
                    <div className="market-best-header">
                      <div>
                        <h4 className="market-best-title">
                          🏆 {recommendation.best_market.market}
                        </h4>
                        <p className="market-best-subtitle">
                          {recommendation.best_market.district} District
                        </p>
                      </div>
                      <div className="market-best-price">
                        <div className="market-price-large">
                          {formatPrice(recommendation.best_market.modal_price)}
                        </div>
                        <div className="text-sm text-green-700">per quintal</div>
                      </div>
                    </div>
                    
                    <div className="market-stats-row">
                      <div className="market-stat-box">
                        <div className="text-sm text-gray-600">Arrival</div>
                        <div className="text-lg font-semibold">
                          {recommendation.best_market.arrival_quantity.toFixed(1)} MT
                        </div>
                      </div>
                      <div className="market-stat-box">
                        <div className="text-sm text-gray-600">Premium</div>
                        <div className="text-lg font-semibold text-green-600">
                          +{recommendation.premium_percent.toFixed(1)}%
                        </div>
                      </div>
                    </div>
                    
                    {recommendation.best_market.reasoning && (
                      <div className="market-reasoning-box">
                        <div className="text-sm font-medium text-gray-700 mb-2">Why This Market?</div>
                        <ul className="space-y-1">
                          {recommendation.best_market.reasoning.map((reason, idx) => (
                            <li key={idx} className="flex items-center text-sm text-gray-600">
                              <CheckCircle className="w-4 h-4 text-green-600 mr-2" />
                              {reason}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                    
                    {recommendation.potential_total_profit && (
                      <div className="market-profit-box">
                        <div className="text-sm mb-1">Potential Extra Profit</div>
                        <div className="market-profit-amount">
                          {formatPrice(recommendation.potential_total_profit)}
                        </div>
                        <div className="text-sm opacity-90">
                          for {recommendation.quantity_quintals} quintals vs market average
                        </div>
                      </div>
                    )}
                  </div>
                  
                  {/* Alternative Markets */}
                  {recommendation.alternatives && recommendation.alternatives.length > 0 && (
                    <div className="market-alternatives-section">
                      <h4 className="font-semibold text-lg mb-3">Alternative Markets</h4>
                      <div className="market-alternatives-list">
                        {recommendation.alternatives.map((market, idx) => (
                          <div key={idx} className="market-alternative-card">
                            <div className="flex justify-between items-start">
                              <div>
                                <div className="font-semibold text-gray-900">{market.market}</div>
                                <div className="text-sm text-gray-600">{market.district}</div>
                              </div>
                              <div className="text-right">
                                <div className="text-xl font-bold text-gray-700">
                                  {formatPrice(market.modal_price)}
                                </div>
                                <div className="text-sm text-gray-500">
                                  {market.arrival_quantity.toFixed(1)} MT
                                </div>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                  
                  {/* Insights */}
                  {recommendation.insights && recommendation.insights.length > 0 && (
                    <div className="market-insights-box">
                      <h4 className="font-semibold text-blue-900 mb-2">💡 Market Insights</h4>
                      <ul className="space-y-1">
                        {recommendation.insights.map((insight, idx) => (
                          <li key={idx} className="text-blue-700 text-sm">
                            • {insight}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </>
      )}
      
      {loading && !forecast && !markets.length && !recommendation && (
        <div className="flex items-center justify-center py-12">
          <Loader className="w-8 h-8 animate-spin text-green-600" />
          <span className="ml-3 text-lg text-gray-600">Loading market data...</span>
        </div>
      )}
    </div>
  );
};

export default MarketIntelligence;
