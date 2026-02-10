import React from 'react';
import { useTranslation } from 'react-i18next';
import { Sprout, Beaker, Bug, TrendingUp, Leaf } from 'lucide-react';
import FeatureCard from '../components/FeatureCard';
import { WeatherDashboard } from '../components/weather';
// import WeatherDashboard from '../components/WeatherWidget';
import ChatbotWidget from '../components/ChatbotWidget';
import '../styles/dashboard.css';

const Dashboard = () => {
    const { t, i18n, ready } = useTranslation('pages');

    // Wait for i18n to be ready
    if (!ready) {
        return (
            <div className="dashboard-container">
                <div className="flex items-center justify-center min-h-screen">
                    <div className="text-center">
                        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900 mx-auto"></div>
                        <p className="mt-4 text-gray-600">Loading...</p>
                    </div>
                </div>
            </div>
        );
    }

    const features = [
        {
            icon: Leaf,
            title: t('dashboard.features.cropPlanning.title'),
            description: t('dashboard.features.cropPlanning.description'),
            path: '/crop-planning',
        },
        {
            icon: Sprout,
            title: t('dashboard.features.cropYield.title'),
            description: t('dashboard.features.cropYield.description'),
            path: '/yield-prediction',
        },
        {
            icon: Beaker,
            title: t('dashboard.features.soilCheck.title'),
            description: t('dashboard.features.soilCheck.description'),
            path: '/soil-analysis',
        },
        {
            icon: Bug,
            title: t('dashboard.features.diseaseHelp.title'),
            description: t('dashboard.features.diseaseHelp.description'),
            path: '/disease-detection',
        },
        {
            icon: TrendingUp,
            title: t('dashboard.features.yieldGapAnalysis.title'),
            description: t('dashboard.features.yieldGapAnalysis.description'),
            path: '/gap-analysis',
        },
    ];

    return (
        <div className="dashboard-container">
            {/* Main Content - Weather + Features */}
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                <div className="dashboard-main-layout">
                    {/* Left - Weather Section */}
                    <div className="dashboard-weather-section">
                        <WeatherDashboard />
                    </div>

                    {/* Right - Features Section */}
                    <div className="dashboard-features-section">
                        <div className="features-header">
                            <h2 className="features-title">
                                {t('dashboard.farmTools.title')}
                            </h2>
                            <p className="features-subtitle">
                                {t('dashboard.farmTools.subtitle')}
                            </p>
                        </div>

                        <div className="features-grid">
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
                </div>
            </div>

            {/* Stats Section */}
            <div className="dashboard-stats-section">
                <div className="dashboard-stats-row">
                    <div className="dashboard-stat">
                        <div className="dashboard-stats-value">55+</div>
                        <div className="dashboard-stats-label">{t('dashboard.stats.cropsSupported')}</div>
                    </div>
                    <div className="dashboard-stat">
                        <div className="dashboard-stats-value">30+</div>
                        <div className="dashboard-stats-label">{t('dashboard.stats.statesCovered')}</div>
                    </div>
                    <div className="dashboard-stat">
                        <div className="dashboard-stats-value">97.5%</div>
                        <div className="dashboard-stats-label">{t('dashboard.stats.mlAccuracy')}</div>
                    </div>
                    <div className="dashboard-stat">
                        <div className="dashboard-stats-value">24/7</div>
                        <div className="dashboard-stats-label">{t('dashboard.stats.aiSupport')}</div>
                    </div>
                </div>
            </div>

            {/* Chatbot Widget */}
            <ChatbotWidget />
        </div>
    );
};

export default Dashboard;
