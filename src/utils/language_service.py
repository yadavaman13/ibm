"""
Language Service Module

Provides comprehensive language management for the farming advisory system.
Handles UI language switching, content translation, and session state management.
"""

import streamlit as st
from pathlib import Path
import sys

# Add parent directory to path to import translator
current_dir = Path(__file__).parent
sys.path.append(str(current_dir.parent))

try:
    from utils.translator import LanguageTranslator
except ImportError:
    # Create a minimal fallback translator
    class LanguageTranslator:
        def __init__(self):
            self.languages = {
                'en': 'English',
                'hi': 'हिंदी (Hindi)',
                'gu': 'ગુજરાતી (Gujarati)',
                'mr': 'मराठी (Marathi)',
                'bn': 'বাংলা (Bengali)'
            }
            self.translations = {
                'app_title': {
                    'en': '🌾 FasalMitra',
                    'hi': '🌾 फसलमित्र',
                    'gu': '🌾 ફસલમિત્ર',
                    'mr': '🌾 फसलमित्र',
                    'bn': '🌾 ফসলমিত্র'
                }
            }
        
        def get_text(self, key, language='en'):
            if key in self.translations:
                return self.translations[key].get(language, self.translations[key]['en'])
            return key
        
        def get_available_languages(self):
            return self.languages


class LanguageService:
    """
    Comprehensive language management service.
    
    Features:
    - Language selection UI component
    - Session state management
    - Integration with translator
    - Dynamic language switching
    """
    
    def __init__(self):
        self.translator = LanguageTranslator()
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        """Initialize language session state if not exists."""
        if 'current_language' not in st.session_state:
            st.session_state.current_language = 'en'  # Default to English
    
    def get_current_language(self):
        """Get currently selected language code."""
        return st.session_state.get('current_language', 'en')
    
    def set_language(self, language_code):
        """Set the current language and trigger update."""
        if language_code in self.translator.get_available_languages():
            st.session_state.current_language = language_code
            # Force UI update
            st.rerun()
            return True
        return False
    
    def get_text(self, key, language=None):
        """
        Get translated text for the current or specified language.
        
        Args:
            key: Translation key
            language: Language code (optional, uses current language if not provided)
        
        Returns:
            Translated text string
        """
        if language is None:
            language = self.get_current_language()
        return self.translator.get_text(key, language)
    
    def get_available_languages(self):
        """Get dictionary of available languages."""
        return self.translator.get_available_languages()
    
    def get_language_name(self, language_code=None):
        """Get the display name of a language."""
        if language_code is None:
            language_code = self.get_current_language()
        return self.get_available_languages().get(language_code, 'English')
    
    def render_language_selector(self, location="sidebar"):
        """
        Render language selection widget.
        
        Args:
            location: Where to render ("sidebar", "header", "inline")
        
        Returns:
            Selected language code
        """
        languages = self.get_available_languages()
        current_lang = self.get_current_language()
        
        # Create selectbox based on location
        if location == "header":
            selected_lang = st.selectbox(
                "🌐 Language",
                options=list(languages.keys()),
                format_func=lambda x: languages[x],
                index=list(languages.keys()).index(current_lang),
                key="header_language_selector",
                help="Select your preferred language"
            )
        else:
            selected_lang = st.selectbox(
                "🌐 Language / भाषा",
                options=list(languages.keys()),
                format_func=lambda x: languages[x],
                index=list(languages.keys()).index(current_lang),
                key="language_selector",
                help="Select your preferred language"
            )
        
        # Update session state if language changed
        if selected_lang != current_lang:
            self.set_language(selected_lang)
        
        return selected_lang


# Global language service instance
_language_service = None

def get_language_service():
    """Get the global language service instance."""
    global _language_service
    if _language_service is None:
        _language_service = LanguageService()
    return _language_service


# Convenience functions for easy access
def get_text(key, language=None):
    """Quick access to translated text."""
    return get_language_service().get_text(key, language)


def get_current_language():
    """Quick access to current language."""
    return get_language_service().get_current_language()


def set_language(language_code):
    """Quick access to set language."""
    return get_language_service().set_language(language_code)


def render_language_selector(location="sidebar"):
    """Quick access to language selector."""
    return get_language_service().render_language_selector(location)