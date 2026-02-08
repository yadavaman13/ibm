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
            <nav className="navbar">
                <div className="navbar-container">
                    <div className="navbar-content">
                        <Link to="/" className="navbar-logo">
                            <Sprout className="navbar-logo-icon" />
                            <span className="navbar-logo-text">
                                Fasal<span className="navbar-brand">Mitra</span>
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
        { name: 'Market Intelligence', path: '/market-intelligence' },
    ];

    return (
        <nav className="navbar">
            <div className="navbar-container">
                <div className="navbar-content">
                    {/* Logo */}
                    <Link to="/" className="navbar-logo">
                        <Sprout className="navbar-logo-icon" />
                        <span className="navbar-logo-text">
                            Fasal<span className="navbar-brand">Mitra</span>
                        </span>
                    </Link>

                    {/* Desktop Navigation - Always visible except on small screens */}
                    <div className="navbar-desktop-menu">
                        {navItems.map((item) => (
                            <Link
                                key={item.path}
                                to={item.path}
                                className="navbar-link"
                            >
                                {item.name}
                            </Link>
                        ))}
                        <LanguageSelector />
                    </div>

                    {/* Mobile Menu Button - Only on small screens */}
                    <button
                        onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                        className="navbar-mobile-btn"
                        aria-label="Toggle menu"
                    >
                        {isMobileMenuOpen ? (
                            <X className="navbar-icon" />
                        ) : (
                            <Menu className="navbar-icon" />
                        )}
                    </button>
                </div>
            </div>

            {/* Mobile Menu - Only visible on small screens */}
            {isMobileMenuOpen && (
                <div className="navbar-mobile-menu">
                    <div className="navbar-mobile-menu-content">
                        {navItems.map((item) => (
                            <Link
                                key={item.path}
                                to={item.path}
                                className="navbar-link navbar-link-mobile"
                                onClick={() => setIsMobileMenuOpen(false)}
                            >
                                {item.name}
                            </Link>
                        ))}
                        <div className="navbar-mobile-language">
                            <LanguageSelector />
                        </div>
                    </div>
                </div>
            )}
        </nav>
    );
};

export default Navbar;
