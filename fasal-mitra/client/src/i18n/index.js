import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

// Import translation files
import enCommon from './locales/en/common.json';
import enNavigation from './locales/en/navigation.json';
import enPages from './locales/en/pages.json';
import enDisease from './locales/en/disease.json';

import hiCommon from './locales/hi/common.json';
import hiNavigation from './locales/hi/navigation.json';
import hiPages from './locales/hi/pages.json';
import hiDisease from './locales/hi/disease.json';

import guCommon from './locales/gu/common.json';
import guNavigation from './locales/gu/navigation.json';
import guPages from './locales/gu/pages.json';
import guDisease from './locales/gu/disease.json';

import mrCommon from './locales/mr/common.json';
import mrNavigation from './locales/mr/navigation.json';
import mrPages from './locales/mr/pages.json';
import mrDisease from './locales/mr/disease.json';

import taCommon from './locales/ta/common.json';
import taNavigation from './locales/ta/navigation.json';
import taPages from './locales/ta/pages.json';
import taDisease from './locales/ta/disease.json';

// Language resources
const resources = {
  en: {
    common: enCommon,
    navigation: enNavigation,
    pages: enPages,
    disease: enDisease
  },
  hi: {
    common: hiCommon,
    navigation: hiNavigation,
    pages: hiPages,
    disease: hiDisease
  },
  gu: {
    common: guCommon,
    navigation: guNavigation,
    pages: guPages,
    disease: guDisease
  },
  mr: {
    common: mrCommon,
    navigation: mrNavigation,
    pages: mrPages,
    disease: mrDisease
  },
  ta: {
    common: taCommon,
    navigation: taNavigation,
    pages: taPages,
    disease: taDisease
  }
};

// Supported languages with metadata
export const supportedLanguages = [
  {
    code: 'en',
    name: 'English',
    nativeName: 'English',
    flag: '🇺🇸',
    dir: 'ltr'
  },
  {
    code: 'hi',
    name: 'Hindi',
    nativeName: 'हिंदी',
    flag: '🇮🇳',
    dir: 'ltr'
  },
  {
    code: 'gu',
    name: 'Gujarati',
    nativeName: 'ગુજરાતી',
    flag: '🟨',
    dir: 'ltr'
  },
  {
    code: 'mr',
    name: 'Marathi',
    nativeName: 'मराठी',
    flag: '🟡',
    dir: 'ltr'
  },
  {
    code: 'ta',
    name: 'Tamil',
    nativeName: 'தமிழ்',
    flag: '🔴',
    dir: 'ltr'
  }
];

// Initialize i18n
i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources,
    fallbackLng: 'en',
    defaultNS: 'common',
    ns: ['common', 'navigation', 'pages', 'disease'],
    
    detection: {
      order: ['localStorage', 'cookie', 'navigator', 'htmlTag'],
      caches: ['localStorage', 'cookie'],
      lookupLocalStorage: 'fasal-mitra-language',
      lookupCookie: 'fasal-mitra-language'
    },

    interpolation: {
      escapeValue: false // React already does escaping
    },

    react: {
      useSuspense: false
    }
  });

export default i18n;