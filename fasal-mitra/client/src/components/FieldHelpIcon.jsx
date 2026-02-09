import React from 'react';
import { Zap } from 'lucide-react';
import { shouldShowHelp } from '../utils/fieldHelpers';
import '../styles/field-help-icon.css';

/**
 * FieldHelpIcon Component
 * 
 * Clickable "Ask AI" button with lightning icon that appears next to agriculture-related input fields
 * Opens the FieldHelpModal when clicked
 */
const FieldHelpIcon = ({ fieldName, onClick }) => {
    // Only render if this field should have help
    if (!shouldShowHelp(fieldName)) {
        return null;
    }

    const handleClick = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (onClick) {
            onClick(e);
        }
    };

    return (
        <button
            type="button"
            className="field-help-btn"
            onClick={handleClick}
            aria-label="Ask AI for help about this field"
            title="Click to ask AI for help"
        >
            <Zap className="lightning-icon" />
            <span className="ask-sigma-text">Ask AI</span>
        </button>
    );
};

export default FieldHelpIcon;
