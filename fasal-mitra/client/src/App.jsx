import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Beaker, Bug, TrendingUp } from 'lucide-react';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import YieldPrediction from './pages/YieldPrediction';
import './styles/pages.css';

const App = () => {
  return (
    <Router>
      <div className="min-h-screen page-container">
        <Navbar />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/yield-prediction" element={<YieldPrediction />} />
          
          {/* Placeholder routes - will create pages later */}
          <Route path="/soil-analysis" element={<ComingSoon title="Soil Analysis" icon={Beaker} />} />
          <Route path="/disease-detection" element={<ComingSoon title="Disease Detection" icon={Bug} />} />
          <Route path="/gap-analysis" element={<ComingSoon title="Gap Analysis" icon={TrendingUp} />} />
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
