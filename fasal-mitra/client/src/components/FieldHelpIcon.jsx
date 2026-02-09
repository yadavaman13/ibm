import React from 'react';
import geminiLogo from '../assets/gemini-ai--v2-removebg-preview.png';
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

    return (
        <button
            type="button"
            className="field-help-btn"
            onClick={onClick}
            aria-label="Ask AI for help about this field"
            title="Click to ask AI for help"
        >
            <img src={geminiLogo} alt="Gemini AI Logo" className="gemini-ai-logo" />
            <span className="ask-sigma-text">Ask AI</span>
        </button>
    );
};

export default FieldHelpIcon;
