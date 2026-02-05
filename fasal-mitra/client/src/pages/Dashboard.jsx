import React from 'react';
import { Sprout, Beaker, Bug, TrendingUp } from 'lucide-react';
import FeatureCard from '../components/FeatureCard';
import WeatherWidget from '../components/WeatherWidget';
import ChatbotWidget from '../components/ChatbotWidget';
import '../styles/dashboard.css';

const Dashboard = () => {
    const features = [
        {
            icon: Sprout,
            title: 'Yield Prediction',
            description: 'Predict crop yield based on your farming inputs using AI-powered ML models with 97.5% accuracy.',
            path: '/yield-prediction',
        },
        {
            icon: Beaker,
            title: 'Soil Analysis',
            description: 'Check soil suitability for crops and get personalized recommendations based on NPK levels.',
            path: '/soil-analysis',
        },
        {
            icon: Bug,
            title: 'Disease Detection',
            description: 'Upload crop images to detect diseases instantly and get treatment plans with cost estimates.',
            path: '/disease-detection',
        },
        {
            icon: TrendingUp,
            title: 'Yield Gap Analysis',
            description: 'Compare your yield with benchmarks and discover opportunities for improvement.',
            path: '/gap-analysis',
        },
    ];

    return (
        <div className="dashboard-container">
            {/* Weather Section */}
            <WeatherWidget />

            {/* Features Grid */}
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
                <div className="mb-8">
                    <h2 className="text-2xl font-bold text-gray-800 mb-2">
                        Explore Features
                    </h2>
                    <p className="text-gray-600">
                        Choose a tool to get started with smart farming decisions
                    </p>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                    {features.map((feature, index) => (
                        <FeatureCard
                            key={index}
                            icon={feature.icon}
                            title={feature.title}
                            description={feature.description}
                            path={feature.path}
                        />
                    ))}
                </div>
            </div>

            {/* Stats Section */}
            <div className="bg-white border-t border-gray-200">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
                        <div>
                            <div className="dashboard-stats-value">55+</div>
                            <div className="dashboard-stats-label">Crops Supported</div>
                        </div>
                        <div>
                            <div className="dashboard-stats-value">30+</div>
                            <div className="dashboard-stats-label">States Covered</div>
                        </div>
                        <div>
                            <div className="dashboard-stats-value">97.5%</div>
                            <div className="dashboard-stats-label">ML Accuracy</div>
                        </div>
                        <div>
                            <div className="dashboard-stats-value">24/7</div>
                            <div className="dashboard-stats-label">AI Support</div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Chatbot Widget */}
            <ChatbotWidget />
        </div>
    );
};

export default Dashboard;
