import React from 'react';
import { HelpCircle } from 'lucide-react';
import { shouldShowHelp } from '../utils/fieldHelpers';
import '../styles/field-help-icon.css';

/**
 * FieldHelpIcon Component
 * 
 * Small clickable help icon that appears next to agriculture-related input fields
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
            className="field-help-icon-btn"
            onClick={onClick}
            aria-label="Get help about this field"
            title="Click for explanation"
        >
            <HelpCircle className="field-help-icon" />
        </button>
    );
};

export default FieldHelpIcon;
