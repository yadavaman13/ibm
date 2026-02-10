import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import {
    Leaf, TrendingUp, TrendingDown, Minus, AlertCircle, CheckCircle,
    Loader, MapPin, Calendar, Maximize2, CloudRain, Thermometer,
    DollarSign, AlertTriangle, Info, Sparkles, Target, ShoppingCart, BarChart3,
    Droplets, Sprout, Database, Navigation, IndianRupee
} from 'lucide-react';
import { planCrops, checkCropPlanningHealth, getCropDetails, generateCropAnalysis } from '../services/cropPlanningService';
import * as soilService from '../services/soilService';
import { compareMarkets, getCommodityInsights } from '../services/marketService';
import FieldHelpIcon from '../components/FieldHelpIcon';
import FieldHelpModal from '../components/FieldHelpModal';
import worldIcon from '../assets/744483-removebg-preview.png';
import locationIcon from '../assets/location-icon-pictogram_764382-14294-removebg-preview.png';
import '../styles/crop-planning.css';
import '../styles/soil-analysis-clean.css';

const CropPlanning = () => {
    const { t } = useTranslation(['pages', 'common']);

    const [formData, setFormData] = useState({
        country: '',
        state: '',
        district: '',
        month: new Date().getMonth() + 1,
        land_size: '',
        latitude: '',
        longitude: '',
        crop: ''
    });

    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);
    const [serverStatus, setServerStatus] = useState(null);
    const [locationLoading, setLocationLoading] = useState(false);

    // help modal
    const [helpModalOpen, setHelpModalOpen] = useState(false);
    const [helpFieldLabel, setHelpFieldLabel] = useState('');
    const [helpFieldName, setHelpFieldName] = useState('');

    // market
    const [marketData, setMarketData] = useState({});
    const [expandedCrop, setExpandedCrop] = useState(null);
    const [loadingMarket, setLoadingMarket] = useState(false);

    // states & crops list
    const [states, setStates] = useState([]);
    const [crops, setCrops] = useState([]);
    const [countries, setCountries] = useState([]);
    const [districts, setDistricts] = useState([]);
    const [allDistricts] = useState({
        'Andhra Pradesh': ['Anantapur', 'Chittoor', 'East Godavari', 'Guntur', 'Krishna', 'Kurnool', 'Nellore', 'Prakasam', 'Srikakulam', 'Visakhapatnam', 'Vizianagaram', 'West Godavari', 'YSR Kadapa'],
        'Arunachal Pradesh': ['Anjaw', 'Changlang', 'Dibang Valley', 'East Kameng', 'East Siang', 'Kamle', 'Kra Daadi', 'Kurung Kumey', 'Lepa Rada', 'Lohit', 'Longding', 'Lower Dibang Valley', 'Lower Siang', 'Lower Subansiri', 'Namsai', 'Pakke Kessang', 'Papum Pare', 'Shi Yomi', 'Siang', 'Tawang', 'Tirap', 'Upper Siang', 'Upper Subansiri', 'West Kameng', 'West Siang'],
        'Gujarat': ['Ahmedabad', 'Amreli', 'Anand', 'Aravalli', 'Banaskantha', 'Bharuch', 'Bhavnagar', 'Botad', 'Chhota Udaipur', 'Dahod', 'Dang', 'Devbhoomi Dwarka', 'Gandhinagar', 'Gir Somnath', 'Jamnagar', 'Junagadh', 'Kheda', 'Kutch', 'Mahisagar', 'Mehsana', 'Morbi', 'Narmada', 'Navsari', 'Panchmahal', 'Patan', 'Porbandar', 'Rajkot', 'Sabarkantha', 'Surat', 'Surendranagar', 'Tapi', 'Vadodara', 'Valsad'],
        'Maharashtra': ['Ahmednagar', 'Akola', 'Amravati', 'Aurangabad', 'Beed', 'Bhandara', 'Buldhana', 'Chandrapur', 'Dhule', 'Gadchiroli', 'Gondia', 'Hingoli', 'Jalgaon', 'Jalna', 'Kolhapur', 'Latur', 'Mumbai City', 'Mumbai Suburban', 'Nagpur', 'Nanded', 'Nandurbar', 'Nashik', 'Osmanabad', 'Palghar', 'Parbhani', 'Pune', 'Raigad', 'Ratnagiri', 'Sangli', 'Satara', 'Sindhudurg', 'Solapur', 'Thane', 'Wardha', 'Washim', 'Yavatmal'],
        'Karnataka': ['Bagalkot', 'Ballari', 'Belagavi', 'Bengaluru Rural', 'Bengaluru Urban', 'Bidar', 'Chamarajanagar', 'Chikballapur', 'Chikkamagaluru', 'Chitradurga', 'Dakshina Kannada', 'Davanagere', 'Dharwad', 'Gadag', 'Hassan', 'Haveri', 'Kalaburagi', 'Kodagu', 'Kolar', 'Koppal', 'Mandya', 'Mysuru', 'Raichur', 'Ramanagara', 'Shivamogga', 'Tumakuru', 'Udupi', 'Uttara Kannada', 'Vijayapura', 'Yadgir'],
        'Punjab': ['Amritsar', 'Barnala', 'Bathinda', 'Faridkot', 'Fatehgarh Sahib', 'Fazilka', 'Ferozepur', 'Gurdaspur', 'Hoshiarpur', 'Jalandhar', 'Kapurthala', 'Ludhiana', 'Malerkotla', 'Mansa', 'Moga', 'Mohali', 'Muktsar', 'Pathankot', 'Patiala', 'Rupnagar', 'Sangrur', 'Shaheed Bhagat Singh Nagar', 'Tarn Taran'],
        'Rajasthan': ['Ajmer', 'Alwar', 'Banswara', 'Baran', 'Barmer', 'Bharatpur', 'Bhilwara', 'Bikaner', 'Bundi', 'Chittorgarh', 'Churu', 'Dausa', 'Dholpur', 'Dungarpur', 'Ganganagar', 'Hanumangarh', 'Jaipur', 'Jaisalmer', 'Jalore', 'Jhalawar', 'Jhunjhunu', 'Jodhpur', 'Karauli', 'Kota', 'Nagaur', 'Pali', 'Pratapgarh', 'Rajsamand', 'Sawai Madhopur', 'Sikar', 'Sirohi', 'Tonk', 'Udaipur'],
        'Tamil Nadu': ['Ariyalur', 'Chengalpattu', 'Chennai', 'Coimbatore', 'Cuddalore', 'Dharmapuri', 'Dindigul', 'Erode', 'Kallakurichi', 'Kanchipuram', 'Kanyakumari', 'Karur', 'Krishnagiri', 'Madurai', 'Mayiladuthurai', 'Nagapattinam', 'Namakkal', 'Nilgiris', 'Perambalur', 'Pudukkottai', 'Ramanathapuram', 'Ranipet', 'Salem', 'Sivaganga', 'Tenkasi', 'Thanjavur', 'Theni', 'Thoothukudi', 'Tiruchirappalli', 'Tirunelveli', 'Tirupathur', 'Tiruppur', 'Tiruvallur', 'Tiruvannamalai', 'Tiruvarur', 'Vellore', 'Viluppuram', 'Virudhunagar'],
        'Uttar Pradesh': ['Agra', 'Aligarh', 'Prayagraj', 'Ambedkar Nagar', 'Amethi', 'Amroha', 'Auraiya', 'Ayodhya', 'Azamgarh', 'Baghpat', 'Bahraich', 'Ballia', 'Balrampur', 'Banda', 'Barabanki', 'Bareilly', 'Basti', 'Bhadohi', 'Bijnor', 'Budaun', 'Bulandshahr', 'Chandauli', 'Chitrakoot', 'Deoria', 'Etah', 'Etawah', 'Farrukhabad', 'Fatehpur', 'Firozabad', 'Gautam Buddha Nagar', 'Ghaziabad', 'Ghazipur', 'Gonda', 'Gorakhpur', 'Hamirpur', 'Hapur', 'Hardoi', 'Hathras', 'Jalaun', 'Jaunpur', 'Jhansi', 'Kannauj', 'Kanpur Dehat', 'Kanpur Nagar', 'Kasganj', 'Kaushambi', 'Kheri', 'Kushinagar', 'Lalitpur', 'Lucknow', 'Maharajganj', 'Mahoba', 'Mainpuri', 'Mathura', 'Mau', 'Meerut', 'Mirzapur', 'Moradabad', 'Muzaffarnagar', 'Pilibhit', 'Pratapgarh', 'Raebareli', 'Rampur', 'Saharanpur', 'Sambhal', 'Sant Kabir Nagar', 'Shahjahanpur', 'Shamli', 'Shravasti', 'Siddharthnagar', 'Sitapur', 'Sonbhadra', 'Sultanpur', 'Unnao', 'Varanasi'],
        'West Bengal': ['Alipurduar', 'Bankura', 'Birbhum', 'Cooch Behar', 'Dakshin Dinajpur', 'Darjeeling', 'Hooghly', 'Howrah', 'Jalpaiguri', 'Jhargram', 'Kalimpong', 'Kolkata', 'Malda', 'Murshidabad', 'Nadia', 'North 24 Parganas', 'Paschim Bardhaman', 'Paschim Medinipur', 'Purba Bardhaman', 'Purba Medinipur', 'Purulia', 'South 24 Parganas', 'Uttar Dinajpur'],
        'Delhi': ['Central Delhi', 'East Delhi', 'New Delhi', 'North Delhi', 'North East Delhi', 'North West Delhi', 'Shahdara', 'South Delhi', 'South East Delhi', 'South West Delhi', 'West Delhi']
    });

    // crop review and AI suggestions
    const [cropReview, setCropReview] = useState(null);
    const [detailedReview, setDetailedReview] = useState(null);
    const [aiSuggestions, setAiSuggestions] = useState([]);
    const [aiLoading, setAiLoading] = useState(false);
    const [aiAnalysis, setAiAnalysis] = useState(null);
    const [analysisLoading, setAnalysisLoading] = useState(false);
    const [analysisError, setAnalysisError] = useState(null);

    // location detection helpers
    const [locationAutoDetected, setLocationAutoDetected] = useState(false);
    const [detectedStateName, setDetectedStateName] = useState(null);
    const [locationError, setLocationError] = useState(null);

    // Helper function to format AI analysis into styled sections
    const formatAIAnalysis = (text) => {
        if (!text) return null;
        
        const sections = [];
        const lines = text.split('\n');
        let currentSection = null;
        let currentContent = [];
        
        const sectionConfig = {
            'suitability': { icon: Target, color: 'var(--color-primary)', title: 'Suitability Analysis' },
            'benefits': { icon: CheckCircle, color: 'var(--color-primary)', title: 'Key Benefits' },
            'risks': { icon: AlertCircle, color: 'var(--color-primary)', title: 'Risks & Challenges' },
            'recommendations': { icon: Sparkles, color: 'var(--color-primary)', title: 'Recommendations' },
            'timeline': { icon: Calendar, color: 'var(--color-primary)', title: 'Expected Timeline' }
        };
        
        const detectSection = (line) => {
            const lower = line.toLowerCase();
            if (lower.includes('suitability')) return 'suitability';
            if (lower.includes('benefit')) return 'benefits';
            if (lower.includes('risk') || lower.includes('challenge')) return 'risks';
            if (lower.includes('recommend')) return 'recommendations';
            if (lower.includes('timeline') || lower.includes('schedule')) return 'timeline';
            return null;
        };
        
        lines.forEach((line) => {
            const trimmed = line.trim();
            if (!trimmed) return;
            
            // Check if this is a section header (starts with # or number)
            if (trimmed.match(/^(#{1,3}|\d+\.)\s/) || trimmed.match(/^\*\*\d+\./)) {
                // Save previous section
                if (currentSection && currentContent.length > 0) {
                    sections.push({ type: currentSection, content: [...currentContent] });
                }
                currentSection = detectSection(trimmed);
                currentContent = [];
            } else if (currentSection) {
                // Clean the line - remove markdown bold markers
                const cleanLine = trimmed.replace(/\*\*/g, '').replace(/^\*\s*/, '• ').replace(/^-\s*/, '• ');
                if (cleanLine) currentContent.push(cleanLine);
            }
        });
        
        // Don't forget last section
        if (currentSection && currentContent.length > 0) {
            sections.push({ type: currentSection, content: [...currentContent] });
        }
        
        // If no sections detected, show as simple formatted text
        if (sections.length === 0) {
            return (
                <div style={{ fontSize: '0.85rem', lineHeight: '1.6', color: '#374151' }}>
                    {text.split('\n').map((line, i) => (
                        <p key={i} style={{ margin: '0.3rem 0' }}>{line.replace(/\*\*/g, '')}</p>
                    ))}
                </div>
            );
        }
        
        return (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                {sections.map((section, idx) => {
                    const config = sectionConfig[section.type] || sectionConfig['recommendations'];
                    return (
                        <div key={idx} style={{
                            backgroundColor: 'white',
                            border: '1px solid #e5e7eb',
                            borderRadius: '0.5rem',
                            padding: '1rem',
                            borderLeft: `4px solid ${config.color}`,
                            boxShadow: '0 1px 2px rgba(0, 0, 0, 0.05)'
                        }}>
                            <div style={{
                                fontWeight: '600',
                                fontSize: '0.85rem',
                                color: config.color,
                                marginBottom: '0.5rem',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '0.5rem'
                            }}>
                                <span>{config.icon}</span>
                                <span>{config.title}</span>
                            </div>
                            <div style={{
                                fontSize: '0.85rem',
                                lineHeight: '1.7',
                                color: '#374151'
                            }}>
                                {section.content.map((item, i) => (
                                    <p key={i} style={{ margin: '0.4rem 0', paddingLeft: '0.5rem' }}>
                                        {item.replace(/^•\s*/, '')}
                                    </p>
                                ))}
                            </div>
                        </div>
                    );
                })}
            </div>
        );
    };

    useEffect(() => {
        const checkHealth = async () => {
            const isHealthy = await checkCropPlanningHealth();
            setServerStatus(isHealthy);
        };
        checkHealth();

        // load states and crops
        const loadInitial = async () => {
            try {
                const [statesData, cropsData] = await Promise.all([
                    soilService.getStates(),
                    soilService.getCrops()
                ]);
                if (Array.isArray(statesData)) setStates(statesData);
                if (Array.isArray(cropsData)) setCrops(cropsData);
                
                // Set comprehensive list of countries (top 60 countries)
                setCountries([
                    'India', 'United States', 'China', 'Japan', 'Germany', 'United Kingdom', 'France', 'Brazil', 'Italy', 'Canada',
                    'Russia', 'South Korea', 'Australia', 'Spain', 'Mexico', 'Indonesia', 'Netherlands', 'Saudi Arabia', 'Turkey', 'Switzerland',
                    'Poland', 'Belgium', 'Sweden', 'Ireland', 'Austria', 'Norway', 'United Arab Emirates', 'Israel', 'Singapore', 'Malaysia',
                    'Denmark', 'South Africa', 'Philippines', 'Colombia', 'Pakistan', 'Chile', 'Finland', 'Bangladesh', 'Egypt', 'Vietnam',
                    'Czech Republic', 'Romania', 'Portugal', 'Peru', 'New Zealand', 'Greece', 'Qatar', 'Algeria', 'Hungary', 'Kazakhstan',
                    'Kuwait', 'Morocco', 'Slovakia', 'Ecuador', 'Ethiopia', 'Kenya', 'Angola', 'Oman', 'Guatemala', 'Bulgaria'
                ]);
            } catch (err) {
                console.error('Failed to load states/crops:', err);
            }
        };
        loadInitial();
    }, []);

    // Update districts when state changes
    useEffect(() => {
        if (formData.state && allDistricts[formData.state]) {
            setDistricts(allDistricts[formData.state]);
        } else {
            setDistricts([]);
        }
    }, [formData.state, allDistricts]);

    const months = [
        { value: 1, label: 'January' }, { value: 2, label: 'February' }, { value: 3, label: 'March' },
        { value: 4, label: 'April' }, { value: 5, label: 'May' }, { value: 6, label: 'June' },
        { value: 7, label: 'July' }, { value: 8, label: 'August' }, { value: 9, label: 'September' },
        { value: 10, label: 'October' }, { value: 11, label: 'November' }, { value: 12, label: 'December' }
    ];

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => {
            const updates = { [name]: value };
            // Clear district when state changes
            if (name === 'state' && value !== prev.state) {
                updates.district = '';
            }
            return { ...prev, ...updates };
        });
        setError(null);
    };

    // Get location details using reverse geocoding (OpenStreetMap Nominatim)
    const getLocationDetails = async (latitude, longitude) => {
        try {
            const response = await fetch(
                `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}&zoom=10&addressdetails=1`,
                { headers: { 'Accept-Language': 'en' } }
            );
            if (!response.ok) throw new Error('Geocoding failed');
            const data = await response.json();
            const address = data.address || {};
            return {
                country: address.country || 'India',
                state: address.state || '',
                district: address.state_district || address.county || address.district || ''
            };
        } catch (err) {
            console.error('Error fetching location details:', err);
            return { country: 'India', state: '', district: '' };
        }
    };

    // Map coordinates to Indian states using bounding boxes (same logic as SoilAnalysis)
    const getStateFromCoordinates = (latitude, longitude) => {
        const stateData = [
            { name: 'Andhra Pradesh', bounds: { minLat: 12.6, maxLat: 19.9, minLng: 77.0, maxLng: 84.8 } },
            { name: 'Arunachal Pradesh', bounds: { minLat: 26.6, maxLat: 29.5, minLng: 91.2, maxLng: 97.4 } },
            { name: 'Assam', bounds: { minLat: 24.1, maxLat: 28.2, minLng: 89.7, maxLng: 96.0 } },
            { name: 'Bihar', bounds: { minLat: 24.3, maxLat: 27.5, minLng: 83.3, maxLng: 88.1 } },
            { name: 'Chhattisgarh', bounds: { minLat: 17.8, maxLat: 24.1, minLng: 80.3, maxLng: 84.4 } },
            { name: 'Delhi', bounds: { minLat: 28.4, maxLat: 28.9, minLng: 76.8, maxLng: 77.3 } },
            { name: 'Goa', bounds: { minLat: 14.9, maxLat: 15.8, minLng: 73.7, maxLng: 74.3 } },
            { name: 'Gujarat', bounds: { minLat: 20.1, maxLat: 24.7, minLng: 68.2, maxLng: 74.5 } },
            { name: 'Haryana', bounds: { minLat: 27.7, maxLat: 30.9, minLng: 74.4, maxLng: 77.4 } },
            { name: 'Himachal Pradesh', bounds: { minLat: 30.4, maxLat: 33.2, minLng: 75.6, maxLng: 79.0 } },
            { name: 'Jharkhand', bounds: { minLat: 21.9, maxLat: 25.3, minLng: 83.3, maxLng: 87.9 } },
            { name: 'Karnataka', bounds: { minLat: 11.5, maxLat: 18.5, minLng: 74.1, maxLng: 78.6 } },
            { name: 'Kerala', bounds: { minLat: 8.2, maxLat: 12.8, minLng: 74.9, maxLng: 77.4 } },
            { name: 'Madhya Pradesh', bounds: { minLat: 21.1, maxLat: 26.9, minLng: 74.0, maxLng: 82.8 } },
            { name: 'Maharashtra', bounds: { minLat: 15.6, maxLat: 22.0, minLng: 72.6, maxLng: 80.9 } },
            { name: 'Manipur', bounds: { minLat: 23.8, maxLat: 25.7, minLng: 93.0, maxLng: 94.8 } },
            { name: 'Meghalaya', bounds: { minLat: 25.0, maxLat: 26.1, minLng: 89.7, maxLng: 92.8 } },
            { name: 'Mizoram', bounds: { minLat: 21.9, maxLat: 24.6, minLng: 92.2, maxLng: 93.7 } },
            { name: 'Nagaland', bounds: { minLat: 25.2, maxLat: 27.0, minLng: 93.3, maxLng: 95.8 } },
            { name: 'Odisha', bounds: { minLat: 17.8, maxLat: 22.6, minLng: 81.4, maxLng: 87.5 } },
            { name: 'Punjab', bounds: { minLat: 29.5, maxLat: 32.5, minLng: 73.9, maxLng: 76.9 } },
            { name: 'Rajasthan', bounds: { minLat: 23.3, maxLat: 30.1, minLng: 69.5, maxLng: 78.3 } },
            { name: 'Sikkim', bounds: { minLat: 27.0, maxLat: 28.1, minLng: 88.0, maxLng: 88.9 } },
            { name: 'Tamil Nadu', bounds: { minLat: 8.1, maxLat: 13.6, minLng: 76.2, maxLng: 80.3 } },
            { name: 'Telangana', bounds: { minLat: 15.8, maxLat: 19.9, minLng: 77.3, maxLng: 81.8 } },
            { name: 'Tripura', bounds: { minLat: 22.9, maxLat: 24.5, minLng: 91.0, maxLng: 92.7 } },
            { name: 'Uttar Pradesh', bounds: { minLat: 23.9, maxLat: 30.4, minLng: 77.1, maxLng: 84.6 } },
            { name: 'Uttarakhand', bounds: { minLat: 28.4, maxLat: 31.5, minLng: 77.6, maxLng: 81.1 } },
            { name: 'West Bengal', bounds: { minLat: 21.2, maxLat: 27.2, minLng: 85.8, maxLng: 89.9 } },
            { name: 'Jammu and Kashmir', bounds: { minLat: 32.3, maxLat: 37.1, minLng: 73.3, maxLng: 80.3 } },
            { name: 'Ladakh', bounds: { minLat: 32.3, maxLat: 37.1, minLng: 75.9, maxLng: 79.9 } }
        ];

        for (const state of stateData) {
            const { bounds } = state;
            if (latitude >= bounds.minLat && latitude <= bounds.maxLat &&
                longitude >= bounds.minLng && longitude <= bounds.maxLng) {

                // Try exact match first (case-insensitive)
                const exactMatch = states.find(s => s.toLowerCase() === state.name.toLowerCase());
                if (exactMatch) {
                    return { detectedName: state.name, matchedState: exactMatch };
                }

                // Try normalized match
                const normalizedStateName = state.name.toLowerCase().replace(/[^a-z]/g, '');
                const normalizedMatch = states.find(s => {
                    const normalizedAvailable = s.toLowerCase().replace(/[^a-z]/g, '');
                    return normalizedAvailable === normalizedStateName;
                });

                if (normalizedMatch) {
                    return { detectedName: state.name, matchedState: normalizedMatch };
                }

                // Try partial match
                const partialMatch = states.find(s => {
                    const sLower = s.toLowerCase();
                    const stateLower = state.name.toLowerCase();
                    return sLower.includes(stateLower) || stateLower.includes(sLower);
                });

                if (partialMatch) {
                    return { detectedName: state.name, matchedState: partialMatch };
                }

                return { detectedName: state.name, matchedState: null };
            }
        }

        return { detectedName: null, matchedState: null };
    };

    const detectLocation = () => {
        if (!navigator.geolocation) {
            setLocationError('Geolocation is not supported by your browser');
            return;
        }

        setLocationLoading(true);
        setLocationError(null);

        const options = { enableHighAccuracy: true, timeout: 10000, maximumAge: 600000 };

        navigator.geolocation.getCurrentPosition(
            async (position) => {
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;

                setFormData(prev => ({ ...prev, latitude: latitude.toFixed(6), longitude: longitude.toFixed(6) }));

                try {
                    const locationDetails = await getLocationDetails(latitude, longitude);
                    const { detectedName, matchedState } = getStateFromCoordinates(latitude, longitude);
                    setDetectedStateName(detectedName);

                    const updates = {};
                    let hasDetectedLocation = false;

                    if (locationDetails.country) { updates.country = locationDetails.country; hasDetectedLocation = true; }
                    if (locationDetails.district) { updates.district = locationDetails.district; hasDetectedLocation = true; }

                    if (matchedState) {
                        updates.state = matchedState;
                        hasDetectedLocation = true;
                        setLocationError(null);
                    } else if (detectedName) {
                        // Use detected state name directly (it's a valid state from our stateData)
                        updates.state = detectedName;
                        hasDetectedLocation = true;
                        setLocationError(null);
                    } else {
                        setLocationError('Could not determine state from your location. Please select manually.');
                    }

                    if (hasDetectedLocation) {
                        setLocationAutoDetected(true);
                        setTimeout(() => setLocationAutoDetected(false), 5000);
                    }

                    if (Object.keys(updates).length > 0) setFormData(prev => ({ ...prev, ...updates }));
                } catch (err) {
                    console.error('Error processing location:', err);
                    setLocationError('Error detecting location details. Please enter manually.');
                }

                setLocationLoading(false);
            },
            (error) => {
                setLocationLoading(false);
                setLocationError('Unable to retrieve your location');
            },
            options
        );
    };

    // Generate Gemini AI Analysis
    const generateAIAnalysis = async (cropData) => {
        try {
            // Use backend API for Gemini integration (Python SDK works reliably)
            const response = await generateCropAnalysis(cropData);
            
            if (response.success && response.data?.analysis) {
                return response.data.analysis;
            } else {
                throw new Error(response.message || 'Failed to generate AI analysis');
            }
        } catch (error) {
            console.error('AI Analysis Error:', error);
            throw error;
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        setResult(null);
        setAiAnalysis(null);
        setCropReview(null);
        setDetailedReview(null);

        try {
            const requestData = {
                state: formData.state,
                month: parseInt(formData.month),
                land_size: formData.land_size ? parseFloat(formData.land_size) : null,
                latitude: formData.latitude ? parseFloat(formData.latitude) : null,
                longitude: formData.longitude ? parseFloat(formData.longitude) : null,
                crop: formData.crop || null
            };

            const data = await planCrops(requestData);
            if (data.success) setResult(data.data);
            else setError(data.message || 'Failed to get crop recommendations');

            // If a specific crop is selected, generate AI analysis
            if (formData.crop) {
                setAnalysisLoading(true);
                setAnalysisError(null);
                
                // Build detailed review info
                const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
                const selectedMonth = months[parseInt(formData.month) - 1] || 'Selected month';
                const monthNum = parseInt(formData.month);
                let season = 'Kharif';
                if (monthNum >= 10 || monthNum <= 3) season = 'Rabi';
                else if (monthNum >= 4 && monthNum <= 6) season = 'Summer';

                setDetailedReview({
                    cropName: formData.crop,
                    month: selectedMonth,
                    monthNum: monthNum,
                    state: formData.state,
                    season: season,
                    country: formData.country,
                    district: formData.district
                });

                // Get crop details from backend
                try {
                    const details = await getCropDetails(formData.crop);
                    if (details && details.success) setCropReview(details.data || details);
                    else setCropReview(details || null);
                } catch (err) {
                    console.error('Failed to fetch crop details:', err);
                }

                // Generate AI analysis using Gemini
                const analysisData = {
                    crop: formData.crop,
                    country: formData.country,
                    state: formData.state,
                    district: formData.district,
                    monthName: selectedMonth,
                    season: season,
                    land_size: formData.land_size
                };
                
                try {
                    const analysis = await generateAIAnalysis(analysisData);
                    if (analysis) {
                        setAiAnalysis(analysis);
                    } else {
                        setAnalysisError('AI analysis returned no data. Please try again.');
                    }
                } catch (aiError) {
                    console.error('AI Analysis Error:', aiError);
                    setAnalysisError('Failed to generate AI analysis. ' + (aiError.message || 'Please check your API key and try again.'));
                } finally {
                    setAnalysisLoading(false);
                }
            }
        } catch (err) {
            console.error('Error:', err);
            setError(err.message || 'Network error. Please ensure the backend server is running.');
        } finally {
            setLoading(false);
        }
    };

    const resetForm = () => {
        setFormData({ country: '', state: '', district: '', month: new Date().getMonth() + 1, land_size: '', latitude: '', longitude: '', crop: '' });
        setResult(null);
        setError(null);
        setCropReview(null);
        setAiSuggestions([]);
        setDetailedReview(null);
        setLocationAutoDetected(false);
        setLocationError(null);
        setAiAnalysis(null);
        setAnalysisError(null);
    };

    const handleHelpClick = (fieldName, fieldLabel) => {
        setHelpFieldName(fieldName);
        setHelpFieldLabel(fieldLabel);
        setHelpModalOpen(true);
    };

    const loadMarketData = async (cropName, cropIndex) => {
        if (expandedCrop === cropIndex) { setExpandedCrop(null); return; }
        if (marketData[cropName]) { setExpandedCrop(cropIndex); return; }

        setLoadingMarket(true);
        try {
            const [marketsData, insightsData] = await Promise.all([
                compareMarkets(cropName, null, formData.state || null, null),
                getCommodityInsights(cropName, 30)
            ]);

            setMarketData(prev => ({ ...prev, [cropName]: { markets: marketsData.markets || [], insights: insightsData || null } }));
            setExpandedCrop(cropIndex);
        } catch (err) {
            console.error('Error loading market data:', err);
            setExpandedCrop(cropIndex);
        } finally {
            setLoadingMarket(false);
        }
    };

    const getTrendIcon = (trend) => {
        if (trend === 'up') return <TrendingUp className="trend-icon up" />;
        if (trend === 'down') return <TrendingDown className="trend-icon down" />;
        return <Minus className="trend-icon stable" />;
    };

    const getWeatherBadge = (suitability) => {
        const badges = { good: <span className="badge good">Good</span>, moderate: <span className="badge moderate">Moderate</span>, poor: <span className="badge poor">Poor</span> };
        return badges[suitability] || badges.moderate;
    };

    const getRiskBadge = (risk) => {
        const badges = { low: <span className="badge risk-low">Low Risk</span>, medium: <span className="badge risk-medium">Medium Risk</span>, high: <span className="badge risk-high">High Risk</span> };
        return badges[risk] || badges.medium;
    };

    const getScoreClass = (score) => {
        if (score >= 75) return 'score-excellent';
        if (score >= 60) return 'score-good';
        if (score >= 45) return 'score-moderate';
        return 'score-poor';
    };

    return (
        <div className="page-container">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {serverStatus === false && (
                    <div className="server-alert"><AlertCircle className="alert-icon" /><span>Server not running. Please start the backend service.</span></div>
                )}

                <div className="crop-planning-card">
                    {/* Location Detection Section - At the start */}
                    <div className="location-detection-section">
                        <div className="location-icon-wrapper">
                            <img src={worldIcon} alt="World Globe" className="world-icon" />
                        </div>
                        <h3 className="location-heading">Allow location access</h3>
                        <p className="location-privacy-text">
                            We use your location only to analyze soil and climate for your region.
                        </p>

                        <button
                            type="button"
                            onClick={detectLocation}
                            disabled={locationLoading}
                            className="get-location-btn"
                        >
                            <img src={locationIcon} alt="Location Icon" className="location-btn-icon" />
                            {locationLoading ? (
                                <>
                                    <Loader className="btn-icon spin" />
                                    Detecting...
                                </>
                            ) : (
                                'Get Location'
                            )}
                        </button>

                        {formData.latitude && formData.longitude && (
                            <div className="coordinates-display-plain">
                                <span className="coordinate">
                                    <strong>Latitude:</strong> {parseFloat(formData.latitude).toFixed(6)}
                                </span>
                                <span className="coordinate-separator">|</span>
                                <span className="coordinate">
                                    <strong>Longitude:</strong> {parseFloat(formData.longitude).toFixed(6)}
                                </span>
                            </div>
                        )}

                        {locationAutoDetected && (
                            <div className="state-detected-msg">
                                <CheckCircle className="success-icon" />
                                Location detected successfully!
                            </div>
                        )}
                        {locationError && (
                            <div className="location-error-msg">
                                <AlertCircle className="error-icon" />
                                <span>{locationError}</span>
                            </div>
                        )}
                    </div>

                    {/* Detailed Crop Review Card (Location & Season Based) */}

                    {/* AI suggestions intentionally hidden per request */}

                    <form onSubmit={handleSubmit} className="planning-form">
                        <div className="form-grid">
                            {/* Left Column */}
                            <div className="form-column">
                                {/* Country */}
                                <div className="form-group">
                                    <label htmlFor="country" className="form-label">
                                        <MapPin className="label-icon" /> Country
                                    </label>
                                    <select id="country" name="country" value={formData.country} onChange={handleInputChange} className="form-select">
                                        <option value="">Select your country</option>
                                        {countries.map(c => <option key={c} value={c}>{c}</option>)}
                                    </select>
                                </div>

                                {/* State */}
                                <div className="form-group">
                                    <label htmlFor="state" className="form-label">
                                        <MapPin className="label-icon" /> State <span className="required">*</span>
                                        <FieldHelpIcon fieldName="state" onClick={() => handleHelpClick('state', 'State')} />
                                    </label>
                                    <select id="state" name="state" value={formData.state} onChange={handleInputChange} required className="form-select">
                                        <option value="">Select your state</option>
                                        {states.map(s => <option key={s} value={s}>{s}</option>)}
                                    </select>
                                </div>

                                {/* District */}
                                <div className="form-group">
                                    <label htmlFor="district" className="form-label">
                                        <MapPin className="label-icon" /> District
                                    </label>
                                    <select id="district" name="district" value={formData.district} onChange={handleInputChange} className="form-select" disabled={!formData.state}>
                                        <option value="">Select your district</option>
                                        {districts.map(d => <option key={d} value={d}>{d}</option>)}
                                    </select>
                                    {!formData.state && <p className="input-hint">Please select a state first</p>}
                                </div>

                                {/* Month */}
                                <div className="form-group">
                                    <label htmlFor="month" className="form-label"><Calendar className="label-icon" /> Planning Month <span className="required">*</span></label>
                                    <select id="month" name="month" value={formData.month} onChange={handleInputChange} required className="form-select">
                                        {months.map(m => <option key={m.value} value={m.value}>{m.label}</option>)}
                                    </select>
                                </div>
                            </div>

                            {/* Right Column */}
                            <div className="form-column">
                                {/* Crop selection */}
                                <div className="form-group">
                                    <label htmlFor="crop" className="form-label"><Sprout className="label-icon" /> Select Crop</label>
                                    <select id="crop" name="crop" value={formData.crop} onChange={handleInputChange} className="form-select">
                                        <option value="">Choose a crop</option>
                                        {crops.map(c => <option key={c} value={c}>{c}</option>)}
                                    </select>
                                </div>

                                {/* Land size */}
                                <div className="form-group">
                                    <label htmlFor="land_size" className="form-label"><Maximize2 className="label-icon" /> Land Size (hectares)</label>
                                    <input type="number" id="land_size" name="land_size" value={formData.land_size} onChange={handleInputChange} min="0.1" step="0.1" placeholder="e.g., 5.0" className="form-input" />
                                    <p className="input-hint">Optional: For quantity recommendations</p>
                                </div>
                            </div>
                        </div>

                        <div className="form-actions">
                            <button type="submit" disabled={loading} className="btn-primary">{loading ? (<><Loader className="btn-icon spin" /> Analyzing...</>) : (<><Sparkles className="btn-icon" /> Get Crop Recommendations</>)}</button>
                            <button type="button" onClick={resetForm} className="btn-secondary" disabled={loading}>Reset</button>
                        </div>
                    </form>

                    {/* Detailed Crop Review Card (Location & Season Based) - Show only after submission */}
                    {detailedReview && formData.crop && result && (
                        <div className="detailed-review-card">
                            <div className="review-header">
                                <h3 className="review-title">{detailedReview.cropName} — Detailed Viability Report</h3>
                                <p className="review-subtitle">Customized analysis for {detailedReview.state} in {detailedReview.month} ({detailedReview.season} season)</p>
                            </div>

                            <div className="review-summary">
                                <div className="summary-item">
                                    <strong>Crop:</strong> {detailedReview.cropName}
                                </div>
                                <div className="summary-item">
                                    <strong>Season:</strong> {detailedReview.season}
                                </div>
                                <div className="summary-item">
                                    <strong>Region:</strong> {detailedReview.state}
                                </div>
                                <div className="summary-item">
                                    <strong>Planting Month:</strong> {detailedReview.month}
                                </div>
                            </div>

                            {/* AI-Generated Analysis Section */}
                            {analysisLoading ? (
                                <div className="review-section">
                                    <div style={{ textAlign: 'center', padding: '1.5rem' }}>
                                        <Loader className="spin" style={{ width: '1.5rem', height: '1.5rem', margin: '0 auto 0.75rem', color: '#10b981' }} />
                                        <p style={{ color: '#6b7280', fontSize: '0.85rem' }}>Generating AI analysis...</p>
                                    </div>
                                </div>
                            ) : aiAnalysis ? (
                                <div className="review-section">
                                    <h4 className="section-heading" style={{ fontSize: '0.9rem', marginBottom: '0.75rem' }}>🤖 AI-Powered Analysis</h4>
                                    {formatAIAnalysis(aiAnalysis)}
                                </div>
                            ) : analysisError ? (
                                <div className="review-section">
                                    <h4 className="section-heading" style={{ fontSize: '0.9rem' }}>🤖 AI-Powered Analysis</h4>
                                    <div style={{ 
                                        backgroundColor: '#fef2f2', 
                                        padding: '0.75rem', 
                                        borderRadius: '0.5rem',
                                        border: '1px solid #fca5a5',
                                        color: '#991b1b',
                                        fontSize: '0.8rem'
                                    }}>
                                        <p style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '0.5rem' }}><AlertCircle size={16} /> {analysisError}</p>
                                    </div>
                                </div>
                            ) : null}

                            {/* Performance Metrics (Optional) */}
                            {/* {cropReview && (
                                <div className="review-section">
                                    <h4 className="section-heading" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}><BarChart3 size={18} /> Performance Metrics</h4>
                                    <div className="metrics-grid">
                                        {cropReview.avg_yield && (
                                            <div className="metric-card">
                                                <span className="metric-label">Average Yield</span>
                                                <span className="metric-value">{cropReview.avg_yield}</span>
                                                <span className="metric-unit">t/ha</span>
                                            </div>
                                        )}
                                        {cropReview.avg_price && (
                                            <div className="metric-card">
                                                <span className="metric-label">Market Price</span>
                                                <span className="metric-value">₹{cropReview.avg_price}</span>
                                            </div>
                                        )}
                                        {cropReview.statistics?.historical_records && (
                                            <div className="metric-card">
                                                <span className="metric-label">Data Points</span>
                                                <span className="metric-value">{cropReview.statistics.historical_records.toLocaleString()}</span>
                                            </div>
                                        )}
                                        {cropReview.statistics?.states_grown && (
                                            <div className="metric-card">
                                                <span className="metric-label">Grown in States</span>
                                                <span className="metric-value">{cropReview.statistics.states_grown}</span>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            )} */}

                            {cropReview?.reliability && (
                                <div className="review-footer">
                                    <CheckCircle className="w-5 h-5" style={{ color: '#10b981' }} />
                                    <span>This analysis is based on <strong>{cropReview.reliability}</strong> historical agricultural data</span>
                                </div>
                            )}
                        </div>
                    )}
                </div>

                {/* Results Section (unchanged layout) */}
                {result && (
                    <>
                        <div className="results-header">
                            <div className="results-divider"><div className="divider-line"></div><span className="divider-text" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}><Target size={20} /> Top {result.recommendations?.length || 0} Recommendations</span><div className="divider-line"></div></div>
                            <div className="season-badge"><Calendar className="season-icon" /><span>Season: <strong>{result.season}</strong></span></div>
                        </div>

                        <div className="recommendations-grid">
                            {result.recommendations?.map((crop, index) => (
                                <div key={crop.crop_name} className="crop-card">
                                    <div className="rank-badge">#{index + 1}</div>
                                    <div className="crop-header"><div className="crop-title-section"><h3 className="crop-name">{crop.crop_name}</h3><div className={`crop-score ${getScoreClass(crop.final_score)}`}>{crop.final_score}/100</div></div></div>

                                    <div className="score-breakdown">
                                        <div className="score-item"><IndianRupee className="score-icon market" /><div className="score-details"><span className="score-label">Market</span><div className="score-value-row"><span className="score-value">{crop.scores?.market || '—'}</span>{getTrendIcon(crop.market_trend)}</div></div></div>

                                        <div className="score-item"><CloudRain className="score-icon weather" /><div className="score-details"><span className="score-label">Weather</span><div className="score-value-row"><span className="score-value">{crop.scores?.weather || '—'}</span>{getWeatherBadge(crop.weather_suitability)}</div></div></div>

                                        <div className="score-item"><Calendar className="score-icon season" /><div className="score-details"><span className="score-label">Season</span><span className="score-value">{crop.scores?.season || '—'}</span></div></div>

                                        <div className="score-item"><Leaf className="score-icon soil" /><div className="score-details"><span className="score-label">Soil</span><div className="score-value-row"><span className="score-value">{crop.scores?.soil || '—'}</span>{getWeatherBadge(crop.soil_suitability)}</div></div></div>

                                        <div className="score-item"><AlertTriangle className="score-icon risk" /><div className="score-details"><span className="score-label">Risk</span><div className="score-value-row"><span className="score-value">{crop.scores?.risk || '—'}</span>{getRiskBadge(crop.risk_level)}</div></div></div>
                                    </div>

                                    <div className="market-info-section">
                                        {crop.average_market_price_inr > 0 && (<div className="market-price"><IndianRupee className="price-icon" /><div className="price-details"><span className="price-label">Avg. Market Price</span><span className="price-value">₹{crop.average_market_price_inr.toLocaleString()}/quintal</span></div></div>)}
                                    </div>

                                    {expandedCrop === index && marketData[crop.crop_name] && (
                                        <div className="market-expansion">
                                            <div className="market-expansion-header"><BarChart3 className="w-5 h-5" /><h4>Real-Time Market Insights for {crop.crop_name}</h4></div>

                                            {marketData[crop.crop_name].insights && (
                                                <div className="market-stats-mini">
                                                    <div className="stat-mini"><span className="stat-label">Price Trend</span><span className={`stat-value trend-${marketData[crop.crop_name].insights.trend?.direction}`}>{marketData[crop.crop_name].insights.trend?.direction === 'rising' && <TrendingUp className="w-4 h-4" />}{marketData[crop.crop_name].insights.trend?.direction === 'falling' && <TrendingDown className="w-4 h-4" />}{marketData[crop.crop_name].insights.trend?.direction === 'stable' && <Minus className="w-4 h-4" />}{marketData[crop.crop_name].insights.trend?.direction || 'N/A'}</span></div>
                                                    <div className="stat-mini"><span className="stat-label">Markets</span><span className="stat-value">{marketData[crop.crop_name].insights.markets?.total_markets || 0}</span></div>
                                                    <div className="stat-mini"><span className="stat-label">Avg. Daily Supply</span><span className="stat-value">{marketData[crop.crop_name].insights.arrival_stats?.avg_daily.toFixed(1) || 0} MT</span></div>
                                                </div>
                                            )}

                                            {marketData[crop.crop_name].markets && marketData[crop.crop_name].markets.length > 0 && (
                                                <div className="top-markets-section">
                                                    <h5 className="top-markets-title">🏆 Top 5 Markets (Best Prices)</h5>
                                                    <div className="markets-list">
                                                        {marketData[crop.crop_name].markets.slice(0, 5).map((market, idx) => (
                                                            <div key={idx} className="market-item"><div className="market-rank">#{idx + 1}</div><div className="market-details"><div className="market-name">{market.market}</div><div className="market-location">{market.district}</div></div><div className="market-price-info"><div className="market-price-value">₹{market.modal_price.toLocaleString()}</div><div className="market-arrival">{market.arrival_quantity.toFixed(1)} MT</div></div></div>
                                                        ))}
                                                    </div>
                                                    <p className="market-note" style={{ display: 'flex', alignItems: 'flex-start', gap: '0.5rem' }}><Info size={16} style={{ flexShrink: 0, marginTop: '0.125rem' }} /> Based on real government mandi data. Consider transport costs when choosing markets.</p>
                                                </div>
                                            )}
                                        </div>
                                    )}

                                    {crop.quantity_recommendation && Object.keys(crop.quantity_recommendation).length > 0 && (
                                        <div className="quantity-section">
                                            <h4 className="quantity-title" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}><BarChart3 size={18} /> Recommended Allocation</h4>
                                            <div className="quantity-grid">
                                                <div className="quantity-item"><span className="quantity-label">Area</span><span className="quantity-value">{crop.quantity_recommendation.recommended_area_hectares?.min || crop.quantity_recommendation.recommended_area_hectares} - {crop.quantity_recommendation.recommended_area_hectares?.max || crop.quantity_recommendation.recommended_area_hectares} ha</span></div>
                                                <div className="quantity-item"><span className="quantity-label">Expected Yield</span><span className="quantity-value">{crop.quantity_recommendation.expected_yield_tons?.min || crop.quantity_recommendation.expected_yield_range?.minimum_tonnes} - {crop.quantity_recommendation.expected_yield_tons?.max || crop.quantity_recommendation.expected_yield_range?.maximum_tonnes} tons</span></div>
                                                <div className="quantity-item"><span className="quantity-label">Growing Period</span><span className="quantity-value">{crop.quantity_recommendation.growing_period_days || crop.calendar_info?.growing_period_days || 90} days</span></div>
                                            </div>
                                            {crop.quantity_recommendation.reliability && (<div className="quantity-note"><Info className="w-4 h-4" /><span>Reliability: <strong>{crop.quantity_recommendation.reliability}</strong> ({crop.quantity_recommendation.based_on_records} historical records)</span></div>)}
                                        </div>
                                    )}

                                    {crop.crop_details && (
                                        <div className="crop-details">
                                            <div className="detail-row"><Thermometer className="detail-icon" /><span>Temp: {crop.crop_details.temperature?.min}°C - {crop.crop_details.temperature?.max}°C</span></div>
                                            <div className="detail-row"><CloudRain className="detail-icon" /><span>Rainfall: {crop.crop_details.rainfall?.min}-{crop.crop_details.rainfall?.max} mm</span></div>
                                            {crop.crop_details.humidity && (<div className="detail-row"><Droplets className="detail-icon" /><span>Humidity: {crop.crop_details.humidity?.min}-{crop.crop_details.humidity?.max}%</span></div>)}
                                            <div className="detail-row"><Info className="detail-icon" /><span>Water: {crop.crop_details.water_requirement}</span></div>
                                        </div>
                                    )}

                                    {crop.calendar_info && crop.calendar_info.sowing_period && (
                                        <div className="calendar-section"><h4 className="section-title" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}><Calendar size={18} /> Growing Calendar</h4><div className="calendar-grid"><div className="calendar-item"><span className="calendar-label" style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}><Sprout size={14} /> Sowing</span><span className="calendar-value">{crop.calendar_info.sowing_period}</span></div><div className="calendar-item"><span className="calendar-label" style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}><Leaf size={14} /> Harvesting</span><span className="calendar-value">{crop.calendar_info.harvesting_period}</span></div>{crop.calendar_info.season_name && (<div className="calendar-item"><span className="calendar-label" style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}><Calendar size={14} /> Season</span><span className="calendar-value">{crop.calendar_info.season_name}</span></div>)}</div></div>
                                    )}

                                    {crop.crop_details?.optimal_conditions && (
                                        <div className="optimal-section"><h4 className="section-title" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}><Target size={18} /> Optimal Conditions</h4><div className="optimal-grid">{crop.crop_details.optimal_conditions.temperature && (<div className="optimal-item"><Thermometer className="optimal-icon" /><div className="optimal-details"><span className="optimal-label">Temperature</span><span className="optimal-value">{crop.crop_details.optimal_conditions.temperature}°C</span></div></div>)}{crop.crop_details.optimal_conditions.rainfall && (<div className="optimal-item"><CloudRain className="optimal-icon" /><div className="optimal-details"><span className="optimal-label">Rainfall</span><span className="optimal-value">{crop.crop_details.optimal_conditions.rainfall} mm</span></div></div>)}{crop.crop_details.optimal_conditions.humidity && (<div className="optimal-item"><Droplets className="optimal-icon" /><div className="optimal-details"><span className="optimal-label">Humidity</span><span className="optimal-value">{crop.crop_details.optimal_conditions.humidity}%</span></div></div>)}</div></div>
                                    )}

                                    {crop.soil_info && Object.keys(crop.soil_info).length > 0 && (
                                        <div className="soil-section"><h4 className="section-title">🌱 Soil Requirements ({result.state})</h4><div className="soil-grid">{crop.soil_info.ph && (<div className="soil-item"><span className="soil-label">pH Level</span><span className="soil-value">{crop.soil_info.ph}</span></div>)}{crop.soil_info.nitrogen_n && (<div className="soil-item"><span className="soil-label">Nitrogen (N)</span><span className="soil-value">{crop.soil_info.nitrogen_n} kg/ha</span></div>)}{crop.soil_info.phosphorus_p && (<div className="soil-item"><span className="soil-label">Phosphorus (P)</span><span className="soil-value">{crop.soil_info.phosphorus_p} kg/ha</span></div>)}{crop.soil_info.potassium_k && (<div className="soil-item"><span className="soil-label">Potassium (K)</span><span className="soil-value">{crop.soil_info.potassium_k} kg/ha</span></div>)}</div></div>
                                    )}

                                    {crop.crop_details?.statistics && crop.crop_details.statistics.historical_records > 0 && (
                                        <div className="stats-section"><h4 className="section-title" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}><Database size={18} /> Historical Data</h4><div className="stats-grid"><div className="stat-item"><Database className="stat-icon" /><div className="stat-details"><span className="stat-label">Records</span><span className="stat-value">{crop.crop_details.statistics.historical_records.toLocaleString()}</span></div></div><div className="stat-item"><MapPin className="stat-icon" /><div className="stat-details"><span className="stat-label">States</span><span className="stat-value">{crop.crop_details.statistics.states_grown}</span></div></div><div className="stat-item"><Sprout className="stat-icon" /><div className="stat-details"><span className="stat-label">Avg. Yield</span><span className="stat-value">{crop.crop_details.statistics.avg_yield_per_hectare.toFixed(2)} t/ha</span></div></div></div></div>
                                    )}
                                </div>
                            ))}
                        </div>

                        <div className="disclaimer"><AlertCircle className="disclaimer-icon" /><div><p className="disclaimer-title">Important Notice</p><p className="disclaimer-text">{result.disclaimer || "This is AI-based guidance. Please consult local agriculture officer."}</p></div></div>
                    </>
                )}

                {error && (
                    <div className="alert-error"><AlertCircle className="alert-icon" /><div><h3 className="alert-title">Error</h3><p className="alert-message">{error}</p></div></div>
                )}
            </div>

            <FieldHelpModal isOpen={helpModalOpen} onClose={() => setHelpModalOpen(false)} fieldLabel={helpFieldLabel} fieldName={helpFieldName} />
        </div>
    );
};

export default CropPlanning;
