import React from 'react';
import { Sprout, Cloud, Beaker, Bug, TrendingUp, MessageCircle } from 'lucide-react';
import FeatureCard from '../components/FeatureCard';
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
            icon: Cloud,
            title: 'Weather Forecast',
            description: 'Get 7-day weather forecast with farming recommendations and alerts for your location.',
            path: '/weather',
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
            title: 'Gap Analysis',
            description: 'Compare your yield with benchmarks and discover opportunities for improvement.',
            path: '/gap-analysis',
        },
        {
            icon: MessageCircle,
            title: 'AI Assistant',
            description: 'Ask farming questions and get expert advice from our AI-powered chatbot assistant.',
            path: '/chatbot',
        },
    ];

    return (
        <div className="dashboard-container">
            {/* Hero Section */}
            <div className="dashboard-hero">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16">
                    <div className="text-center">
                        <h1 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-gray-900 mb-4">
                            Welcome to <span style={{ color: '#99BC85' }}>FasalMitra</span>
                        </h1>
                        <p className="text-base sm:text-lg text-gray-600 max-w-2xl mx-auto">
                            Your Smart Farming Assistant providing data-driven insights for better crop management and higher yields
                        </p>
                    </div>
                </div>
            </div>

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

                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
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
        </div>
    );
};

export default Dashboard;
