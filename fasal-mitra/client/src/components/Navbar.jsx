import React from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { Sprout } from 'lucide-react';
import LanguageSelector from './LanguageSelector';
import '../styles/navbar.css';

const Navbar = () => {
    const { t, ready } = useTranslation('navigation');

    // Show a minimal navbar while i18n loads
    if (!ready) {
        return (
            <nav className="navbar shadow-sm">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between items-center h-16">
                        <Link to="/" className="flex items-center space-x-2">
                            <Sprout className="w-6 h-6 navbar-logo-icon" />
                            <span className="text-xl font-bold navbar-brand">
                                <span className="navbar-fasal">Fasal</span><span className="navbar-mitra">Mitra</span>
                            </span>
                        </Link>
                        <LanguageSelector />
                    </div>
                </div>
            </nav>
        );
    }

    const navItems = [
        { name: t('home'), path: '/' },
        { name: t('yieldPrediction'), path: '/yield-prediction' },
        { name: t('soilAnalysis'), path: '/soil-analysis' },
        { name: t('diseaseDetection'), path: '/disease-detection' },
        { name: t('yieldGapAnalysis'), path: '/gap-analysis' },
    ];

    return (
        <nav className="navbar shadow-sm">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-16">
                    {/* Logo */}
                    <Link to="/" className="flex items-center space-x-2">
                        <Sprout className="w-6 h-6 navbar-logo-icon" />
                        <span className="text-xl font-bold navbar-brand">
                            <span className="navbar-fasal">Fasal</span><span className="navbar-mitra">Mitra</span>
                        </span>
                    </Link>

                    {/* Navigation Items - Always Visible */}
                    <div className="flex items-center space-x-6">
                        {/* Navigation Links */}
                        <div className="flex items-center space-x-4">
                            {navItems.map((item) => (
                                <Link
                                    key={item.path}
                                    to={item.path}
                                    className="navbar-link text-sm font-medium transition-colors hover:text-white"
                                >
                                    {item.name}
                                </Link>
                            ))}
                        </div>
                        
                        {/* Language Selector */}
                        <div className="flex items-center">
                            <LanguageSelector />
                        </div>
                    </div>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
