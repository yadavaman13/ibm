import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { TrendingUp } from 'lucide-react';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import YieldPrediction from './pages/YieldPrediction';
import DiseaseDetection from './pages/DiseaseDetection';
import SoilAnalysis from './pages/SoilAnalysis';
import YieldGapAnalysis from './pages/YieldGapAnalysis';
import MarketIntelligence from './pages/MarketIntelligence';
import CropPlanning from './pages/CropPlanning';
import './i18n'; // Initialize i18n
import './styles/pages.css';

const App = () => {
  return (
    <Router>
      <div className="min-h-screen page-container">
        <Navbar />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/yield-prediction" element={<YieldPrediction />} />
          <Route path="/disease-detection" element={<DiseaseDetection />} />
          <Route path="/soil-analysis" element={<SoilAnalysis />} />
          <Route path="/gap-analysis" element={<YieldGapAnalysis />} />
          <Route path="/market-intelligence" element={<MarketIntelligence />} />
          <Route path="/crop-planning" element={<CropPlanning />} />
        </Routes>
      </div>
    </Router>
  );
};

// Temporary placeholder component for unimplemented pages
const ComingSoon = ({ title, icon: Icon }) => (
  <div className="min-h-screen page-container flex items-center justify-center">
    <div className="text-center">
      <div className="flex justify-center mb-4">
        <Icon className="coming-soon-icon" />
      </div>
      <h1 className="text-3xl font-bold text-gray-800 mb-2">{title}</h1>
      <p className="text-gray-600">This feature will be implemented soon</p>
    </div>
  </div>
);

export default App;
