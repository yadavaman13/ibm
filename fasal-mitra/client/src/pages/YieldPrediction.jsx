import React from 'react';
import { Sprout } from 'lucide-react';
import '../styles/pages.css';

const YieldPrediction = () => {
    return (
        <div className="page-container">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <h1 className="page-header-title">Yield Prediction</h1>
                <p className="page-header-subtitle">
                    Predict your crop yield based on farming inputs
                </p>

                {/* Placeholder for future implementation */}
                <div className="coming-soon-card">
                    <div className="flex justify-center mb-4">
                        <Sprout className="coming-soon-icon" />
                    </div>
                    <h2 className="text-xl font-semibold text-gray-700 mb-2">
                        Coming Soon
                    </h2>
                    <p className="text-gray-500">
                        This feature will be implemented next
                    </p>
                </div>
            </div>
        </div>
    );
};

export default YieldPrediction;
