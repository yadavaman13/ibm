import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import '../styles/feature-card.css';

const FeatureCard = ({ icon: Icon, title, description, path }) => {
    return (
        <Link to={path} className="feature-card">
            {/* Icon Container */}
            <div className="feature-card-icon inline-flex items-center justify-center w-12 h-12 rounded-lg mb-4 transition-colors">
                <Icon className="w-6 h-6" />
            </div>

            {/* Title */}
            <h3 className="text-lg font-semibold text-gray-800 mb-2 transition-colors">
                {title}
            </h3>

            {/* Description */}
            <p className="text-sm text-gray-600 leading-relaxed">
                {description}
            </p>

            {/* Arrow Icon */}
            <div className="feature-card-arrow mt-4 flex items-center text-sm font-medium transition-opacity">
                <span>Get Started</span>
                <ArrowRight className="ml-2 w-4 h-4 transition-transform" />
            </div>
        </Link>
    );
};

export default FeatureCard;
