import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { Sprout, Menu, X } from 'lucide-react';
import LanguageSelector from './LanguageSelector';
import '../styles/navbar.css';

const Navbar = () => {
    const { t, ready } = useTranslation('navigation');
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

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
        <nav className="navbar shadow-">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-16">
                    {/* Logo */}
                    <Link to="/" className="flex items-center space-x-2">
                        <Sprout className="w-6 h-6 navbar-logo-icon" />
                        <span className="text-xl font-bold navbar-brand">
                            <span className="navbar-fasal">Fasal</span><span className="navbar-mitra">Mitra</span>
                        </span>
                    </Link>

                    {/* Desktop Navigation */}
                    <div className="hidden md:flex items-center space-x-4">
                        <div className="flex items-center space-x-1">
                            {navItems.map((item) => (
                                <Link
                                    key={item.path}
                                    to={item.path}
                                    className="navbar-link px-3 py-2 rounded-md text-sm font-medium text-gray-700 transition-colors"
                                >
                                    {item.name}
                                </Link>
                            ))}
                        </div>
                        <LanguageSelector />
                    </div>

                    {/* Mobile Menu Button */}
                    <button
                        onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                        className="navbar-mobile-btn md:hidden p-2 rounded-md text-gray-700 focus:outline-none"
                        aria-label="Toggle menu"
                    >
                        {isMobileMenuOpen ? (
                            <X className="h-6 w-6" />
                        ) : (
                            <Menu className="h-6 w-6" />
                        )}
                    </button>
                </div>
            </div>

            {/* Mobile Menu */}
            {isMobileMenuOpen && (
                <div className="navbar-mobile-menu md:hidden">
                    <div className="px-2 pt-2 pb-3 space-y-1">
                        {navItems.map((item) => (
                            <Link
                                key={item.path}
                                to={item.path}
                                className="navbar-link block px-3 py-2 rounded-md text-base font-medium text-gray-700 transition-colors"
                                onClick={() => setIsMobileMenuOpen(false)}
                            >
                                {item.name}
                            </Link>
                        ))}
                        <div className="px-3 py-2">
                            <LanguageSelector />
                        </div>
                    </div>
                </div>
            )}
        </nav>
    );
};

export default Navbar;
