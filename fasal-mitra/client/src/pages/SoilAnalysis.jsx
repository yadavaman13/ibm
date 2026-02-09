import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { Sprout, Droplets, TestTube, CheckCircle, AlertCircle, Loader, TrendingUp, MapPin, Navigation, Volume2, VolumeX, Play, Pause, Square, Eye, Lightbulb, ThumbsUp, Star, BarChart3, RotateCcw, Wheat, Calendar, IndianRupee, Package, Earth } from 'lucide-react';
import '../styles/pages.css';
import '../styles/soil-analysis-clean.css';
import * as soilService from '../services/soilService';
import FieldHelpIcon from '../components/FieldHelpIcon';
import FieldHelpModal from '../components/FieldHelpModal';
import { VoiceSummary } from '../components/voice';
import worldIcon from '../assets/744483-removebg-preview.png';
import locationIcon from '../assets/location-icon-pictogram_764382-14294-removebg-preview.png';

const SoilAnalysis = () => {
    const { t } = useTranslation(['pages', 'common']);
    const [formData, setFormData] = useState({
        country: '',
        state: '',
        district: '',
        crop: '',
        fieldSize: '',
        irrigationType: '',
        previousCrop: '',
        waterQuality: ''
    });



    const [states, setStates] = useState([]);
    const [countries, setCountries] = useState([]);
    const [districts, setDistricts] = useState([]);
    const [allDistricts] = useState({
        // India State-wise Districts Mapping (700+ districts)
        'Andhra Pradesh': ['Anantapur', 'Chittoor', 'East Godavari', 'Guntur', 'Krishna', 'Kurnool', 'Nellore', 'Prakasam', 'Srikakulam', 'Visakhapatnam', 'Vizianagaram', 'West Godavari', 'YSR Kadapa'],
        'Arunachal Pradesh': ['Anjaw', 'Changlang', 'Dibang Valley', 'East Kameng', 'East Siang', 'Kamle', 'Kra Daadi', 'Kurung Kumey', 'Lepa Rada', 'Lohit', 'Longding', 'Lower Dibang Valley', 'Lower Siang', 'Lower Subansiri', 'Namsai', 'Pakke Kessang', 'Papum Pare', 'Shi Yomi', 'Siang', 'Tawang', 'Tirap', 'Upper Siang', 'Upper Subansiri', 'West Kameng', 'West Siang'],
        'Assam': ['Baksa', 'Barpeta', 'Biswanath', 'Bongaigaon', 'Cachar', 'Charaideo', 'Chirang', 'Darrang', 'Dhemaji', 'Dhubri', 'Dibrugarh', 'Dima Hasao', 'Goalpara', 'Golaghat', 'Hailakandi', 'Hojai', 'Jorhat', 'Kamrup', 'Kamrup Metropolitan', 'Karbi Anglong', 'Karimganj', 'Kokrajhar', 'Lakhimpur', 'Majuli', 'Morigaon', 'Nagaon', 'Nalbari', 'Sivasagar', 'Sonitpur', 'South Salmara-Mankachar', 'Tinsukia', 'Udalguri', 'West Karbi Anglong'],
        'Bihar': ['Araria', 'Arwal', 'Aurangabad', 'Banka', 'Begusarai', 'Bhagalpur', 'Bhojpur', 'Buxar', 'Darbhanga', 'East Champaran', 'Gaya', 'Gopalganj', 'Jamui', 'Jehanabad', 'Kaimur', 'Katihar', 'Khagaria', 'Kishanganj', 'Lakhisarai', 'Madhepura', 'Madhubani', 'Munger', 'Muzaffarpur', 'Nalanda', 'Nawada', 'Patna', 'Purnia', 'Rohtas', 'Saharsa', 'Samastipur', 'Saran', 'Sheikhpura', 'Sheohar', 'Sitamarhi', 'Siwan', 'Supaul', 'Vaishali', 'West Champaran'],
        'Chhattisgarh': ['Balod', 'Baloda Bazar', 'Balrampur', 'Bastar', 'Bemetara', 'Bijapur', 'Bilaspur', 'Dantewada', 'Dhamtari', 'Durg', 'Gariaband', 'Gaurela Pendra Marwahi', 'Janjgir Champa', 'Jashpur', 'Kabirdham', 'Kanker', 'Kondagaon', 'Korba', 'Koriya', 'Mahasamund', 'Mungeli', 'Narayanpur', 'Raigarh', 'Raipur', 'Rajnandgaon', 'Sukma', 'Surajpur', 'Surguja'],
        'Goa': ['North Goa', 'South Goa'],
        'Gujarat': ['Ahmedabad', 'Amreli', 'Anand', 'Aravalli', 'Banaskantha', 'Bharuch', 'Bhavnagar', 'Botad', 'Chhota Udaipur', 'Dahod', 'Dang', 'Devbhoomi Dwarka', 'Gandhinagar', 'Gir Somnath', 'Jamnagar', 'Junagadh', 'Kheda', 'Kutch', 'Mahisagar', 'Mehsana', 'Morbi', 'Narmada', 'Navsari', 'Panchmahal', 'Patan', 'Porbandar', 'Rajkot', 'Sabarkantha', 'Surat', 'Surendranagar', 'Tapi', 'Vadodara', 'Valsad'],
        'Haryana': ['Ambala', 'Bhiwani', 'Charkhi Dadri', 'Faridabad', 'Fatehabad', 'Gurugram', 'Hisar', 'Jhajjar', 'Jind', 'Kaithal', 'Karnal', 'Kurukshetra', 'Mahendragarh', 'Nuh', 'Palwal', 'Panchkula', 'Panipat', 'Rewari', 'Rohtak', 'Sirsa', 'Sonipat', 'Yamunanagar'],
        'Himachal Pradesh': ['Bilaspur', 'Chamba', 'Hamirpur', 'Kangra', 'Kinnaur', 'Kullu', 'Lahaul and Spiti', 'Mandi', 'Shimla', 'Sirmaur', 'Solan', 'Una'],
        'Jharkhand': ['Bokaro', 'Chatra', 'Deoghar', 'Dhanbad', 'Dumka', 'East Singhbhum', 'Garhwa', 'Giridih', 'Godda', 'Gumla', 'Hazaribagh', 'Jamtara', 'Khunti', 'Koderma', 'Latehar', 'Lohardaga', 'Pakur', 'Palamu', 'Ramgarh', 'Ranchi', 'Sahebganj', 'Seraikela Kharsawan', 'Simdega', 'West Singhbhum'],
        'Karnataka': ['Bagalkot', 'Ballari', 'Belagavi', 'Bengaluru Rural', 'Bengaluru Urban', 'Bidar', 'Chamarajanagar', 'Chikballapur', 'Chikkamagaluru', 'Chitradurga', 'Dakshina Kannada', 'Davanagere', 'Dharwad', 'Gadag', 'Hassan', 'Haveri', 'Kalaburagi', 'Kodagu', 'Kolar', 'Koppal', 'Mandya', 'Mysuru', 'Raichur', 'Ramanagara', 'Shivamogga', 'Tumakuru', 'Udupi', 'Uttara Kannada', 'Vijayapura', 'Yadgir'],
        'Kerala': ['Alappuzha', 'Ernakulam', 'Idukki', 'Kannur', 'Kasaragod', 'Kollam', 'Kottayam', 'Kozhikode', 'Malappuram', 'Palakkad', 'Pathanamthitta', 'Thiruvananthapuram', 'Thrissur', 'Wayanad'],
        'Madhya Pradesh': ['Agar Malwa', 'Alirajpur', 'Anuppur', 'Ashoknagar', 'Balaghat', 'Barwani', 'Betul', 'Bhind', 'Bhopal', 'Burhanpur', 'Chhatarpur', 'Chhindwara', 'Damoh', 'Datia', 'Dewas', 'Dhar', 'Dindori', 'Guna', 'Gwalior', 'Harda', 'Hoshangabad', 'Indore', 'Jabalpur', 'Jhabua', 'Katni', 'Khandwa', 'Khargone', 'Maihar', 'Mandla', 'Mandsaur', 'Morena', 'Narsinghpur', 'Neemuch', 'Niwari', 'Panna', 'Raisen', 'Rajgarh', 'Ratlam', 'Rewa', 'Sagar', 'Satna', 'Sehore', 'Seoni', 'Shahdol', 'Shajapur', 'Sheopur', 'Shivpuri', 'Sidhi', 'Singrauli', 'Tikamgarh', 'Ujjain', 'Umaria', 'Vidisha'],
        'Maharashtra': ['Ahmednagar', 'Akola', 'Amravati', 'Aurangabad', 'Beed', 'Bhandara', 'Buldhana', 'Chandrapur', 'Dhule', 'Gadchiroli', 'Gondia', 'Hingoli', 'Jalgaon', 'Jalna', 'Kolhapur', 'Latur', 'Mumbai City', 'Mumbai Suburban', 'Nagpur', 'Nanded', 'Nandurbar', 'Nashik', 'Osmanabad', 'Palghar', 'Parbhani', 'Pune', 'Raigad', 'Ratnagiri', 'Sangli', 'Satara', 'Sindhudurg', 'Solapur', 'Thane', 'Wardha', 'Washim', 'Yavatmal'],
        'Manipur': ['Bishnupur', 'Chandel', 'Churachandpur', 'Imphal East', 'Imphal West', 'Jiribam', 'Kakching', 'Kamjong', 'Kangpokpi', 'Noney', 'Pherzawl', 'Senapati', 'Tamenglong', 'Tengnoupal', 'Thoubal', 'Ukhrul'],
        'Meghalaya': ['East Garo Hills', 'East Jaintia Hills', 'East Khasi Hills', 'North Garo Hills', 'Ri Bhoi', 'South Garo Hills', 'South West Garo Hills', 'South West Khasi Hills', 'West Garo Hills', 'West Jaintia Hills', 'West Khasi Hills'],
        'Mizoram': ['Aizawl', 'Champhai', 'Hnahthial', 'Khawzawl', 'Kolasib', 'Lawngtlai', 'Lunglei', 'Mamit', 'Saiha', 'Saitual', 'Serchhip'],
        'Nagaland': ['Chumukedima', 'Dimapur', 'Kiphire', 'Kohima', 'Longleng', 'Mokokchung', 'Mon', 'Niuland', 'Noklak', 'Peren', 'Phek', 'Shamator', 'Tseminyu', 'Tuensang', 'Wokha', 'Zunheboto'],
        'Odisha': ['Angul', 'Balangir', 'Balasore', 'Bargarh', 'Bhadrak', 'Boudh', 'Cuttack', 'Deogarh', 'Dhenkanal', 'Gajapati', 'Ganjam', 'Jagatsinghpur', 'Jajpur', 'Jharsuguda', 'Kalahandi', 'Kandhamal', 'Kendrapara', 'Kendujhar', 'Khordha', 'Koraput', 'Malkangiri', 'Mayurbhanj', 'Nabarangpur', 'Nayagarh', 'Nuapada', 'Puri', 'Rayagada', 'Sambalpur', 'Subarnapur', 'Sundargarh'],
        'Punjab': ['Amritsar', 'Barnala', 'Bathinda', 'Faridkot', 'Fatehgarh Sahib', 'Fazilka', 'Ferozepur', 'Gurdaspur', 'Hoshiarpur', 'Jalandhar', 'Kapurthala', 'Ludhiana', 'Malerkotla', 'Mansa', 'Moga', 'Mohali', 'Muktsar', 'Pathankot', 'Patiala', 'Rupnagar', 'Sangrur', 'Shaheed Bhagat Singh Nagar', 'Tarn Taran'],
        'Rajasthan': ['Ajmer', 'Alwar', 'Banswara', 'Baran', 'Barmer', 'Bharatpur', 'Bhilwara', 'Bikaner', 'Bundi', 'Chittorgarh', 'Churu', 'Dausa', 'Dholpur', 'Dungarpur', 'Ganganagar', 'Hanumangarh', 'Jaipur', 'Jaisalmer', 'Jalore', 'Jhalawar', 'Jhunjhunu', 'Jodhpur', 'Karauli', 'Kota', 'Nagaur', 'Pali', 'Pratapgarh', 'Rajsamand', 'Sawai Madhopur', 'Sikar', 'Sirohi', 'Tonk', 'Udaipur'],
        'Sikkim': ['East Sikkim', 'North Sikkim', 'South Sikkim', 'West Sikkim'],
        'Tamil Nadu': ['Ariyalur', 'Chengalpattu', 'Chennai', 'Coimbatore', 'Cuddalore', 'Dharmapuri', 'Dindigul', 'Erode', 'Kallakurichi', 'Kanchipuram', 'Kanyakumari', 'Karur', 'Krishnagiri', 'Madurai', 'Mayiladuthurai', 'Nagapattinam', 'Namakkal', 'Nilgiris', 'Perambalur', 'Pudukkottai', 'Ramanathapuram', 'Ranipet', 'Salem', 'Sivaganga', 'Tenkasi', 'Thanjavur', 'Theni', 'Thoothukudi', 'Tiruchirappalli', 'Tirunelveli', 'Tirupathur', 'Tiruppur', 'Tiruvallur', 'Tiruvannamalai', 'Tiruvarur', 'Vellore', 'Viluppuram', 'Virudhunagar'],
        'Telangana': ['Adilabad', 'Bhadradri Kothagudem', 'Hyderabad', 'Jagtial', 'Jangaon', 'Jayashankar Bhupalpally', 'Jogulamba Gadwal', 'Kamareddy', 'Karimnagar', 'Khammam', 'Komaram Bheem', 'Mahabubabad', 'Mahbubnagar', 'Mancherial', 'Medak', 'Medchal Malkajgiri', 'Mulugu', 'Nagarkurnool', 'Nalgonda', 'Narayanpet', 'Nirmal', 'Nizamabad', 'Peddapalli', 'Rajanna Sircilla', 'Rangareddy', 'Sangareddy', 'Siddipet', 'Suryapet', 'Vikarabad', 'Wanaparthy', 'Warangal Rural', 'Warangal Urban', 'Yadadri Bhuvanagiri'],
        'Tripura': ['Dhalai', 'Gomati', 'Khowai', 'North Tripura', 'Sepahijala', 'South Tripura', 'Unakoti', 'West Tripura'],
        'Uttar Pradesh': ['Agra', 'Aligarh', 'Ambedkar Nagar', 'Amethi', 'Amroha', 'Auraiya', 'Ayodhya', 'Azamgarh', 'Baghpat', 'Bahraich', 'Ballia', 'Balrampur', 'Banda', 'Barabanki', 'Bareilly', 'Basti', 'Bhadohi', 'Bijnor', 'Budaun', 'Bulandshahr', 'Chandauli', 'Chitrakoot', 'Deoria', 'Etah', 'Etawah', 'Farrukhabad', 'Fatehpur', 'Firozabad', 'Gautam Buddha Nagar', 'Ghaziabad', 'Ghazipur', 'Gonda', 'Gorakhpur', 'Hamirpur', 'Hapur', 'Hardoi', 'Hathras', 'Jalaun', 'Jaunpur', 'Jhansi', 'Kannauj', 'Kanpur Dehat', 'Kanpur Nagar', 'Kasganj', 'Kaushambi', 'Kheri', 'Kushinagar', 'Lalitpur', 'Lucknow', 'Maharajganj', 'Mahoba', 'Mainpuri', 'Mathura', 'Mau', 'Meerut', 'Mirzapur', 'Moradabad', 'Muzaffarnagar', 'Pilibhit', 'Pratapgarh', 'Prayagraj', 'Raebareli', 'Rampur', 'Saharanpur', 'Sambhal', 'Sant Kabir Nagar', 'Shahjahanpur', 'Shamli', 'Shravasti', 'Siddharthnagar', 'Sitapur', 'Sonbhadra', 'Sultanpur', 'Unnao', 'Varanasi'],
        'Uttarakhand': ['Almora', 'Bageshwar', 'Chamoli', 'Champawat', 'Dehradun', 'Haridwar', 'Nainital', 'Pauri Garhwal', 'Pithoragarh', 'Rudraprayag', 'Tehri Garhwal', 'Udham Singh Nagar', 'Uttarkashi'],
        'West Bengal': ['Alipurduar', 'Bankura', 'Birbhum', 'Cooch Behar', 'Dakshin Dinajpur', 'Darjeeling', 'Hooghly', 'Howrah', 'Jalpaiguri', 'Jhargram', 'Kalimpong', 'Kolkata', 'Malda', 'Murshidabad', 'Nadia', 'North 24 Parganas', 'Paschim Bardhaman', 'Paschim Medinipur', 'Purba Bardhaman', 'Purba Medinipur', 'Purulia', 'South 24 Parganas', 'Uttar Dinajpur'],
        'Andaman and Nicobar Islands': ['Nicobar', 'North and Middle Andaman', 'South Andaman'],
        'Chandigarh': ['Chandigarh'],
        'Dadra and Nagar Haveli and Daman and Diu': ['Dadra and Nagar Haveli', 'Daman', 'Diu'],
        'Delhi': ['Central Delhi', 'East Delhi', 'New Delhi', 'North Delhi', 'North East Delhi', 'North West Delhi', 'Shahdara', 'South Delhi', 'South East Delhi', 'South West Delhi', 'West Delhi'],
        'Jammu and Kashmir': ['Anantnag', 'Bandipora', 'Baramulla', 'Budgam', 'Doda', 'Ganderbal', 'Jammu', 'Kathua', 'Kishtwar', 'Kulgam', 'Kupwara', 'Poonch', 'Pulwama', 'Rajouri', 'Ramban', 'Reasi', 'Samba', 'Shopian', 'Srinagar', 'Udhampur'],
        'Ladakh': ['Kargil', 'Leh'],
        'Lakshadweep': ['Lakshadweep'],
        'Puducherry': ['Karaikal', 'Mahe', 'Puducherry', 'Yanam']
    });
    const [crops, setCrops] = useState([]);
 
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [serverStatus, setServerStatus] = useState(null);
    const [results, setResults] = useState(null);

    // Location state
    const [location, setLocation] = useState({ latitude: null, longitude: null });
    const [locationLoading, setLocationLoading] = useState(false);
    const [locationError, setLocationError] = useState(null);
    const [locationAutoDetected, setLocationAutoDetected] = useState(false);
    const [detectedStateName, setDetectedStateName] = useState(null);

    // Field help modal state
    const [helpModalOpen, setHelpModalOpen] = useState(false);
    const [helpFieldLabel, setHelpFieldLabel] = useState('');
    const [helpFieldName, setHelpFieldName] = useState('');
    
    // Custom field size state
    const [isCustomFieldSize, setIsCustomFieldSize] = useState(false);
    // eslint-disable-next-line no-unused-vars
    const [_customFieldSize, _setCustomFieldSize] = useState('');

    // Load states and crops on mount
    useEffect(() => {
        const loadData = async () => {
            try {
                const [statesData, cropsData, serverHealth] = await Promise.all([
                    soilService.getStates(),
                    soilService.getCrops(),
                    soilService.checkServerHealth()
                ]);

                // Service now returns arrays directly
                setStates(statesData);
                setCrops(cropsData);
                setServerStatus(serverHealth);
                
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
                console.error('Failed to load initial data:', err);
                setStates([]);
                setCrops([]);
                setServerStatus(false);
            }
        };

        loadData();
    }, []);

    // Update districts when state changes
    useEffect(() => {
        if (formData.state && allDistricts[formData.state]) {
            setDistricts(allDistricts[formData.state]);
        } else {
            setDistricts([]);
        }
    }, [formData.state, allDistricts]);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => {
            const updates = { [name]: value };
            // Clear district when state changes (they'll need to pick a new district)
            if (name === 'state' && value !== prev.state) {
                updates.district = '';
            }
            return { ...prev, ...updates };
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            // Prepare form data for traditional analysis
            const analysisData = {
                state: formData.state,
                crop: formData.crop,
                ...(formData.fieldSize && { fieldSize: parseFloat(formData.fieldSize) }),
                ...(formData.irrigationType && { irrigationType: formData.irrigationType }),
                ...(formData.previousCrop && { previousCrop: formData.previousCrop }),
                ...(formData.waterQuality && { waterQuality: formData.waterQuality })
            };

            // Traditional analysis
            const [traditionalAnalysis, recommendations] = await Promise.all([
                soilService.analyzeSoil(analysisData),
                soilService.getRecommendedCrops(formData.state)
            ]);

            const result = {
                ...traditionalAnalysis,
                recommendations,
                analysisType: 'traditional'
            };

            setResults(result);
        } catch (err) {
            setError(err.message || 'Failed to analyze soil. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const resetForm = () => {
        setFormData({
            country: '',
            state: '',
            district: '',
            crop: '',
            fieldSize: '',
            irrigationType: '',
            previousCrop: '',
            waterQuality: ''
        });
        setResults(null);
        setError(null);
        setLocation({ latitude: null, longitude: null });
        setLocationError(null);
        setLocationAutoDetected(false);
    };

    // Handle help icon click
    const handleHelpClick = (fieldName, fieldLabel) => {
        setHelpFieldName(fieldName);
        setHelpFieldLabel(fieldLabel);
        setHelpModalOpen(true);
    };

    // Crop icon mapping
    const getCropIcon = (cropName) => {
        const iconMap = {
            'rice': '🌾',
            'wheat': '🌾',
            'maize': '🌽',
            'corn': '🌽',
            'cotton': '☁️',
            'sugarcane': '🎋',
            'potato': '🥔',
            'tomato': '🍅',
            'onion': '🧅',
            'soybean': '🫘',
            'groundnut': '🥜',
            'sunflower': '🌻',
            'mustard': '🌿',
            'barley': '🌾',
            'jowar': '🌾',
            'bajra': '🌾',
            'ragi': '🌾',
            'gram': '🫘',
            'arhar': '🫘',
            'moong': '🫘',
            'urad': '🫘',
            'linseed': '🌰',
            'castor': '🌰',
            'sesame': '🌰',
            'coconut': '🥥',
            'banana': '🍌',
            'mango': '🥭',
            'apple': '🍎',
            'orange': '🍊',
            'papaya': '🍈',
            'guava': '🍈',
            'pomegranate': '🍈',
            'grapes': '🍇',
            'watermelon': '🍉',
            'cucumber': '🥒',
            'brinjal': '🍆',
            'okra': '🥒',
            'cabbage': '🥬',
            'cauliflower': '🥬',
            'carrot': '🥕',
            'radish': '🥕',
            'ginger': '🫚',
            'turmeric': '🫚',
            'chili': '🌶️',
            'coriander': '🌿',
            'fenugreek': '🌿',
            'spinach': '🥬'
        };

        const normalizedName = cropName.toLowerCase().trim();
        return iconMap[normalizedName] || '🌱';
    };

    // Get suggested crops (mix of popular crops)
    const getSuggestedCrops = () => {
        const popularCrops = ['rice', 'maize', 'cotton', 'sugarcane', 'potato'];
        return popularCrops.filter(crop =>
            crops.some(availableCrop =>
                availableCrop.toLowerCase().includes(crop.toLowerCase())
            )
        ).slice(0, 5);
    };

    // Get location details using reverse geocoding
    const getLocationDetails = async (latitude, longitude) => {
        try {
            // Use OpenStreetMap Nominatim reverse geocoding (free, no API key needed)
            const response = await fetch(
                `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}&zoom=10&addressdetails=1`,
                {
                    headers: {
                        'Accept-Language': 'en'
                    }
                }
            );

            if (!response.ok) {
                throw new Error('Geocoding failed');
            }

            const data = await response.json();
            const address = data.address || {};

            return {
                country: address.country || 'India',
                state: address.state || '',
                district: address.state_district || address.county || address.district || ''
            };
        } catch (error) {
            console.error('Error fetching location details:', error);
            // Fallback to coordinate-based detection
            return {
                country: 'India', // Default for Indian coordinates
                state: '',
                district: ''
            };
        }
    };

    // Map coordinates to Indian states
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

        console.log('🔍 Detecting state for coordinates:', { latitude, longitude });
        console.log('📋 Available states from backend:', states);

        for (const state of stateData) {
            const { bounds } = state;
            if (latitude >= bounds.minLat && latitude <= bounds.maxLat &&
                longitude >= bounds.minLng && longitude <= bounds.maxLng) {

                console.log('📍 Detected geographic state:', state.name);

                // Try exact match first (case-insensitive)
                const exactMatch = states.find(s => 
                    s.toLowerCase() === state.name.toLowerCase()
                );

                if (exactMatch) {
                    console.log('✅ Exact match found:', exactMatch);
                    return { detectedName: state.name, matchedState: exactMatch };
                }

                // Try normalized match (remove spaces and special characters)
                const normalizedStateName = state.name.toLowerCase().replace(/[^a-z]/g, '');
                const normalizedMatch = states.find(s => {
                    const normalizedAvailable = s.toLowerCase().replace(/[^a-z]/g, '');
                    return normalizedAvailable === normalizedStateName;
                });

                if (normalizedMatch) {
                    console.log('✅ Normalized match found:', normalizedMatch);
                    return { detectedName: state.name, matchedState: normalizedMatch };
                }

                // Try partial match
                const partialMatch = states.find(s => {
                    const sLower = s.toLowerCase();
                    const stateLower = state.name.toLowerCase();
                    return sLower.includes(stateLower) || stateLower.includes(sLower);
                });

                if (partialMatch) {
                    console.log('✅ Partial match found:', partialMatch);
                    return { detectedName: state.name, matchedState: partialMatch };
                }

                console.log('⚠️ State detected but not available in backend:', state.name);
                return { detectedName: state.name, matchedState: null };
            }
        }

        console.log('❌ No state found for coordinates');
        return { detectedName: null, matchedState: null };
    };

    // Handle crop suggestion click
    const handleCropSuggestionClick = (suggestedCrop) => {
        // Find the actual crop name from the available crops
        const actualCrop = crops.find(crop =>
            crop.toLowerCase().includes(suggestedCrop.toLowerCase())
        );

        if (actualCrop) {
            setFormData(prev => ({ ...prev, crop: actualCrop }));
        }
    };

    const detectLocation = () => {
        if (!navigator.geolocation) {
            setLocationError(t('soilAnalysis.location.errors.notSupported'));
            return;
        }

        setLocationLoading(true);
        setLocationError(null);

        const options = {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 600000 // 10 minutes
        };

        navigator.geolocation.getCurrentPosition(
            async (position) => {
                const newLocation = {
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude
                };

                setLocation(newLocation);

                try {
                    // Get detailed location information
                    const locationDetails = await getLocationDetails(
                        newLocation.latitude,
                        newLocation.longitude
                    );

                    // Auto-select state based on coordinates
                    const { detectedName, matchedState } = getStateFromCoordinates(
                        newLocation.latitude,
                        newLocation.longitude
                    );

                    setDetectedStateName(detectedName);

                    // Update form data with all detected information
                    const updates = {};
                    let hasDetectedLocation = false;
                    
                    // Country
                    if (locationDetails.country) {
                        updates.country = locationDetails.country;
                        hasDetectedLocation = true;
                    }

                    // District
                    if (locationDetails.district) {
                        updates.district = locationDetails.district;
                        hasDetectedLocation = true;
                    }

                    // State
                    if (matchedState) {
                        updates.state = matchedState;
                        hasDetectedLocation = true;
                        setLocationError(null);
                        console.log(`✅ Location detected! Auto-selected state: ${matchedState}`);
                    } else if (detectedName) {
                        console.log(`⚠️ Location detected (${detectedName}) but not available in the system. Please select your state manually.`);
                        setLocationError(`Location detected: ${detectedName}. Please select your state manually.`);
                    } else {
                        console.log('❌ Could not determine state from your location.');
                        setLocationError('Could not determine state from your location. Please select manually.');
                    }

                    // Show single success message if any location field was detected
                    if (hasDetectedLocation) {
                        setLocationAutoDetected(true);
                        setTimeout(() => setLocationAutoDetected(false), 5000);
                    }

                    // Apply all updates at once
                    if (Object.keys(updates).length > 0) {
                        setFormData(prev => ({ ...prev, ...updates }));
                        console.log('📍 Location details detected:', updates);
                    }

                } catch (error) {
                    console.error('Error processing location:', error);
                    setLocationError('Error detecting location details. Please enter manually.');
                }

                setLocationLoading(false);
            },
            (error) => {
                setLocationLoading(false);
                let errorMessage;

                switch (error.code) {
                    case error.PERMISSION_DENIED:
                        errorMessage = t('soilAnalysis.location.errors.permissionDenied');
                        break;
                    case error.POSITION_UNAVAILABLE:
                        errorMessage = t('soilAnalysis.location.errors.unavailable');
                        break;
                    case error.TIMEOUT:
                        errorMessage = t('soilAnalysis.location.errors.timeout');
                        break;
                    default:
                        errorMessage = t('soilAnalysis.location.errors.unknown');
                        break;
                }

                setLocationError(errorMessage);
            },
            options
        );
    };

    const getSuitabilityLevel = (score) => {
        if (score >= 80) return { label: t('pages:soilAnalysis.results.excellent'), class: 'excellent' };
        if (score >= 60) return { label: t('pages:soilAnalysis.results.good'), class: 'good' };
        if (score >= 40) return { label: t('pages:soilAnalysis.results.fair'), class: 'fair' };
        return { label: t('pages:soilAnalysis.results.poor'), class: 'poor' };
    };

    // eslint-disable-next-line no-unused-vars
    const _getpHLevel = (pH) => {
        if (pH < 6.5) return { label: 'Acidic', class: 'acidic' };
        if (pH <= 7.5) return { label: 'Neutral', class: 'neutral' };
        return { label: 'Alkaline', class: 'alkaline' };
    };

    const getNPKLevel = (value, type) => {
        // Typical NPK ranges (simplified)
        const ranges = {
            N: { low: 200, high: 400 },
            P: { low: 20, high: 50 },
            K: { low: 100, high: 300 }
        };

        const range = ranges[type];
        if (!range) return 50;

        const percentage = ((value - 0) / (range.high * 1.5)) * 100;
        return Math.min(Math.max(percentage, 0), 100);
    };

    return (
        <div className="soil-analysis-page">
            <div className="page-container">
                {/* Page Header */}
                <div className="page-header">
                    <Sprout className="page-header-icon" />
                    <div>
                        <h1 className="page-header-title">{t('soilAnalysis.title')}</h1>
                        <p className="page-header-subtitle">{t('soilAnalysis.subtitle')}</p>
                    </div>
                </div>

                {serverStatus === false && (
                    <div className="server-alert">
                        <AlertCircle className="alert-icon" />
                        <span>{t('pages:soilAnalysis.serverNotRunning')}</span>
                    </div>
                )}

                {/* Main Form Card */}
                <div className="main-form-card">
                    <form onSubmit={handleSubmit} className="clean-form">

                        {/* Location Detection Section */}
                        <div className="location-detection-section">
                            <div className="location-icon-wrapper">
                                <img src={worldIcon} alt="World Globe" className="world-icon" />
                            </div>
                            <h3 className="location-heading">{t('pages:soilAnalysis.location.allowAccess')}</h3>
                            <p className="location-privacy-text">
                                {t('pages:soilAnalysis.location.privacyText')}
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
                                        {t('pages:soilAnalysis.location.detecting')}
                                    </>
                                ) : (
                                    t('pages:soilAnalysis.location.getLocation')
                                )}
                            </button>

                            {location.latitude && location.longitude && (
                                <div className="coordinates-display-plain">
                                    <span className="coordinate">
                                        <strong>{t('pages:soilAnalysis.latitude')}:</strong> {location.latitude.toFixed(6)}
                                    </span>
                                    <span className="coordinate-separator">|</span>
                                    <span className="coordinate">
                                        <strong>{t('pages:soilAnalysis.longitude')}:</strong> {location.longitude.toFixed(6)}
                                    </span>
                                </div>
                            )}

                            {locationAutoDetected && (
                                <div className="state-detected-msg">
                                    <CheckCircle className="success-icon" />
                                    <span>Location detected successfully!</span>
                                </div>
                            )}

                            {locationError && (
                                <div className="location-error-msg">
                                    <AlertCircle className="error-icon" />
                                    <span>{locationError}</span>
                                </div>
                            )}
                        </div>

                        {/* Form Fields */}
                        <div className="form-fields">
                            {/* Two Column Layout */}
                            <div className="form-columns">
                                {/* Left Column */}
                                <div className="form-column">
                                    {/* Country */}
                                    <div className="form-field-wrapper">
                                        <div className="form-field">
                                            <label className="field-label">
                                                Country
                                            </label>
                                            <select
                                                name="country"
                                                value={formData.country}
                                                onChange={handleInputChange}
                                                className="field-input"
                                            >
                                                <option value="">Select Country</option>
                                                {countries.map(country => (
                                                    <option key={country} value={country}>{country}</option>
                                                ))}
                                            </select>
                                        </div>
                                    </div>

                                    {/* State */}
                                    <div className="form-field-wrapper">
                                        <div className="form-field">
                                            <label className="field-label">
                                                State
                                            </label>
                                            <select
                                                name="state"
                                                value={formData.state}
                                                onChange={handleInputChange}
                                                required
                                                className="field-input"
                                            >
                                                <option value="">Select State</option>
                                                {states.map(state => (
                                                    <option key={state} value={state}>{t(`common:states.${state}`)}</option>
                                                ))}
                                            </select>
                                        </div>
                                    </div>

                                    {/* District */}
                                    <div className="form-field-wrapper">
                                        <div className="form-field">
                                            <label className="field-label">
                                                District
                                            </label>
                                            <select
                                                name="district"
                                                value={formData.district}
                                                onChange={handleInputChange}
                                                className="field-input"
                                                disabled={!formData.state || districts.length === 0}
                                            >
                                                <option value="">
                                                    {!formData.state 
                                                        ? 'Select State First'
                                                        : 'Select District'
                                                    }
                                                </option>
                                                {districts.map(district => (
                                                    <option key={district} value={district}>{district}</option>
                                                ))}
                                            </select>
                                        </div>
                                    </div>

                                    {/* Field Size */}
                                    <div className="form-field-wrapper">
                                        <div className="form-field">
                                            <label className="field-label">
                                                {t('pages:soilAnalysis.fieldSize')}
                                                <FieldHelpIcon
                                                    fieldName="fieldSize"
                                                    onClick={() => handleHelpClick('fieldSize', 'Field Size')}
                                                />
                                            </label>
                                            {!isCustomFieldSize ? (
                                                <select
                                                    name="fieldSize"
                                                    value={formData.fieldSize}
                                                    onChange={(e) => {
                                                        if (e.target.value === 'custom') {
                                                            setIsCustomFieldSize(true);
                                                            setFormData(prev => ({ ...prev, fieldSize: '' }));
                                                        } else {
                                                            handleInputChange(e);
                                                        }
                                                    }}
                                                    className="field-input"
                                                >
                                                    <option value="">{t('pages:soilAnalysis.selectFieldSize')}</option>
                                                    <option value="0.5">0.5 {t('pages:soilAnalysis.hectares')}</option>
                                                    <option value="1">1 {t('pages:soilAnalysis.hectares')}</option>
                                                    <option value="2">2 {t('pages:soilAnalysis.hectares')}</option>
                                                    <option value="3">3 {t('pages:soilAnalysis.hectares')}</option>
                                                    <option value="5">5 {t('pages:soilAnalysis.hectares')}</option>
                                                    <option value="10">10 {t('pages:soilAnalysis.hectares')}</option>
                                                    <option value="15">15 {t('pages:soilAnalysis.hectares')}</option>
                                                    <option value="20">20 {t('pages:soilAnalysis.hectares')}</option>
                                                    <option value="25">25+ {t('pages:soilAnalysis.hectares')}</option>
                                                    <option value="custom">{t('pages:soilAnalysis.customSize')}</option>
                                                </select>
                                            ) : (
                                                <div className="custom-field-size-input">
                                                    <input
                                                        type="number"
                                                        name="fieldSize"
                                                        value={formData.fieldSize}
                                                        onChange={handleInputChange}
                                                        placeholder={t('pages:soilAnalysis.enterCustomSize')}
                                                        className="field-input"
                                                        min="0.1"
                                                        step="0.1"
                                                        autoFocus
                                                    />
                                                    <button
                                                        type="button"
                                                        className="back-to-dropdown-btn"
                                                        onClick={() => {
                                                            setIsCustomFieldSize(false);
                                                            setFormData(prev => ({ ...prev, fieldSize: '' }));
                                                        }}
                                                        title={t('pages:soilAnalysis.backToPresets')}
                                                    >
                                                        ✕
                                                    </button>
                                                </div>
                                            )}
                                        </div>
                                    </div>

                                    {/* Previous Crop */}
                                    <div className="form-field-wrapper">
                                        <div className="form-field">
                                            <label className="field-label">{t('pages:soilAnalysis.previousCrop')}</label>
                                            <select
                                                name="previousCrop"
                                                value={formData.previousCrop}
                                                onChange={handleInputChange}
                                                className="field-input"
                                            >
                                                <option value="">{t('pages:soilAnalysis.selectPreviousCrop')}</option>
                                                <option value="none">{t('pages:soilAnalysis.noPreviousCrop')}</option>
                                                {crops.map(crop => {
                                                    const translatedCrop = t(`common:crops.${crop}`, { defaultValue: crop });
                                                    return (
                                                        <option key={crop} value={crop}>{translatedCrop}</option>
                                                    );
                                                })}
                                            </select>
                                        </div>
                                    </div>
                                </div>

                                {/* Right Column */}
                                <div className="form-column">
                                    {/* Irrigation Type */}
                                    <div className="form-field-wrapper">
                                        <div className="form-field">
                                            <label className="field-label">
                                                {t('pages:soilAnalysis.irrigationType')}
                                                <FieldHelpIcon
                                                    fieldName="irrigationType"
                                                    onClick={() => handleHelpClick('irrigationType', 'Irrigation Type')}
                                                />
                                            </label>
                                            <select
                                                name="irrigationType"
                                                value={formData.irrigationType}
                                                onChange={handleInputChange}
                                                className="field-input"
                                            >
                                                <option value="">{t('pages:soilAnalysis.selectIrrigation')}</option>
                                                <option value="rainfed">{t('pages:soilAnalysis.irrigation.rainfed')}</option>
                                                <option value="drip">{t('pages:soilAnalysis.irrigation.drip')}</option>
                                                <option value="sprinkler">{t('pages:soilAnalysis.irrigation.sprinkler')}</option>
                                                <option value="flood">{t('pages:soilAnalysis.irrigation.flood')}</option>
                                                <option value="mixed">{t('pages:soilAnalysis.irrigation.mixed')}</option>
                                            </select>
                                        </div>
                                    </div>

                                    {/* Water Quality */}
                                    <div className="form-field-wrapper">
                                        <div className="form-field">
                                            <label className="field-label">
                                                {t('pages:soilAnalysis.waterQuality')}
                                                <FieldHelpIcon
                                                    fieldName="waterQuality"
                                                    onClick={() => handleHelpClick('waterQuality', 'Water Quality')}
                                                />
                                            </label>
                                            <select
                                                name="waterQuality"
                                                value={formData.waterQuality}
                                                onChange={handleInputChange}
                                                className="field-input"
                                            >
                                                <option value="">{t('pages:soilAnalysis.selectWaterQuality')}</option>
                                                <option value="sweet">{t('pages:soilAnalysis.waterTypes.sweet')}</option>
                                                <option value="slightlySalty">{t('pages:soilAnalysis.waterTypes.slightlySalty')}</option>
                                                <option value="verySalty">{t('pages:soilAnalysis.waterTypes.verySalty')}</option>
                                                <option value="unknown">{t('pages:soilAnalysis.waterTypes.unknown')}</option>
                                            </select>
                                        </div>
                                    </div>

                                    {/* Analyze Crop */}
                                    <div className="form-field-wrapper">
                                        <div className="form-field">
                                            <label className="field-label">{t('pages:soilAnalysis.analyzeCrop')}</label>
                                            <select
                                                name="crop"
                                                value={formData.crop}
                                                onChange={handleInputChange}
                                                required
                                                className="field-input"
                                            >
                                                <option value="">{t('pages:soilAnalysis.selectCrop')}</option>
                                                {crops.map(crop => {
                                                    const translatedCrop = t(`common:crops.${crop}`, { defaultValue: crop });
                                                    return (
                                                        <option key={crop} value={crop}>{translatedCrop}</option>
                                                    );
                                                })}
                                            </select>
                                        </div>

                                        {/* Crop Suggestions below Crop dropdown */}
                                        <div className="crop-suggestions-inline">
                                            <span className="try-text">{t('pages:soilAnalysis.try')}:</span>
                                            <div className="crop-icons">
                                                {getSuggestedCrops().map((crop) => {
                                                    const actualCrop = crops.find(c => c.toLowerCase().includes(crop.toLowerCase()));
                                                    const isSelected = actualCrop && formData.crop === actualCrop;
                                                    // Use actualCrop for translation if found, otherwise capitalize the crop name
                                                    const cropKey = actualCrop || crop.charAt(0).toUpperCase() + crop.slice(1);
                                                    const translatedCropName = t(`common:crops.${cropKey}`, { defaultValue: crop.charAt(0).toUpperCase() + crop.slice(1) });
                                                    
                                                    return (
                                                        <div
                                                            key={crop}
                                                            className="crop-suggestion"
                                                        >
                                                            <div
                                                                className={`crop-icon-container ${isSelected ? 'active' : ''}`}
                                                                onClick={() => handleCropSuggestionClick(crop)}
                                                            >
                                                                <div className="crop-icon">{getCropIcon(crop)}</div>
                                                            </div>
                                                            <span className="crop-name">{translatedCropName}</span>
                                                        </div>
                                                    );
                                                })}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                        </div>

                        {/* Action Buttons */}
                        <div className="action-buttons">
                            <button
                                type="submit"
                                disabled={loading}
                                className="analyze-btn"
                            >
                                {loading ? (
                                    <>
                                        <Loader className="btn-icon spin" />
                                        {t('pages:soilAnalysis.analyzing')}
                                    </>
                                ) : (
                                    t('pages:soilAnalysis.analyze')
                                )}
                            </button>
                            <button
                                type="button"
                                onClick={resetForm}
                                className="reset-btn"
                                disabled={loading}
                            >
                                {t('common:buttons.reset')}
                            </button>
                        </div>
                    </form>
                </div>

                {/* Error Display */}
                {error && (
                    <div className="error-alert">
                        <AlertCircle className="alert-icon" />
                        <div>
                            <h3 className="alert-title">Error</h3>
                            <p className="alert-message">{error}</p>
                        </div>
                    </div>
                )}

                {/* Results Section */}
                {results && (
                    <>
                        {/* Results Divider */}
                        <div className="results-divider">
                            <div className="divider-line"></div>
                            <span className="divider-text">{t('pages:soilAnalysis.results.title', 'Analysis Results')}</span>
                            <div className="divider-line"></div>
                        </div>

                        {/* Voice Summary - Listen to Results */}
                        <div className="voice-summary-section">
                            <VoiceSummary
                                result={{ ...results, crop: formData.crop, state: formData.state }}
                                resultType="soilAnalysis"
                                title={t('pages:soilAnalysis.listenToSummary', 'Listen to Summary')}
                                showTitle={true}
                                compact={false}
                                className="soil-voice-summary"
                            />
                        </div>

                        {/* Image Analysis Display */}
                        {results.analysisType === 'image_enhanced' && (
                            <div className="image-enhanced-header">
                                <div className="analysis-badge">
                                    <Camera className="badge-icon" />
                                    <span>📸 {t('pages:soilAnalysis.results.aiVisionAnalysis')}</span>
                                </div>
                                <p>{t('pages:soilAnalysis.results.enhancedAnalysis')}</p>
                            </div>
                        )}

                        {/* Image Analysis Results Card */}
                        {results.analysisType === 'image_enhanced' && results.imageAnalysis && (
                            <div className="result-card image-analysis-card">
                                <div className="card-header">
                                    <div className="card-icon-wrapper">
                                        <Eye className="header-icon" />
                                    </div>
                                    <h3 className="card-title">🔍 {t('pages:soilAnalysis.results.visualAssessment')}</h3>
                                </div>
                                <p className="card-description">{t('pages:soilAnalysis.results.aiPoweredAnalysis')}</p>

                                {results.imageAnalysis.analysis_method === 'fallback' ? (
                                    <div className="fallback-notice">
                                        <AlertCircle className="notice-icon" />
                                        <p>{t('pages:soilAnalysis.results.fallbackNotice')}</p>
                                        <ul style={{ margin: '0.5rem 0', paddingLeft: '1.5rem', fontSize: '0.875rem' }}>
                                            <li>{t('pages:soilAnalysis.results.imageQualityIssue')}</li>
                                            <li>{t('pages:soilAnalysis.results.apiUnavailable')}</li>
                                        </ul>
                                        <p style={{ marginTop: '0.5rem' }}>{t('pages:soilAnalysis.results.usingTraditional')}</p>
                                    </div>
                                ) : results.imageAnalysis.structured_analysis && (
                                    <div className="visual-analysis-grid">
                                        <div className="visual-metric">
                                            <span className="metric-label">{t('pages:soilAnalysis.results.soilColor')}</span>
                                            <span className="metric-value">{results.imageAnalysis.structured_analysis.soil_color?.replace('_', ' ') || t('pages:soilAnalysis.results.unknown')}</span>
                                        </div>
                                        <div className="visual-metric">
                                            <span className="metric-label">{t('pages:soilAnalysis.results.textureType')}</span>
                                            <span className="metric-value">{results.imageAnalysis.structured_analysis.texture_type || t('pages:soilAnalysis.results.unknown')}</span>
                                        </div>
                                        <div className="visual-metric">
                                            <span className="metric-label">{t('pages:soilAnalysis.results.moistureLevel')}</span>
                                            <span className="metric-value">{results.imageAnalysis.structured_analysis.moisture_level || t('pages:soilAnalysis.results.unknown')}</span>
                                        </div>
                                        <div className="visual-metric">
                                            <span className="metric-label">{t('pages:soilAnalysis.results.healthScore')}</span>
                                            <span className="metric-value">{results.imageAnalysis.structured_analysis.overall_health_score || 50}/100</span>
                                        </div>
                                    </div>
                                )}
                            </div>
                        )}

                        <div className="results-grid">
                            {/* Show traditional soil composition card only for traditional analysis or when soil data exists */}
                            {(results.analysisType === 'traditional' && results.soil) || (results.analysisType === 'image_enhanced' && results.traditionalAnalysis?.soil_data) ? (
                                <div className="result-card soil-composition-card">
                                    <div className="card-header">
                                        <Sprout className="header-icon" />
                                        <h3 className="card-title">{t('pages:soilAnalysis.results.soilHealthReport')}</h3>
                                    </div>
                                    <p className="card-description">{t('pages:soilAnalysis.results.yourSoilNutrients')}</p>

                                    <div className="npk-grid">
                                        {/* Nitrogen */}
                                        <div className="npk-item">
                                            <div className="npk-header">
                                                <div className="npk-info">
                                                    <span className="npk-label">{t('pages:soilAnalysis.results.nitrogen')}</span>
                                                    <span className="npk-description">{t('pages:soilAnalysis.results.forGreenGrowth')}</span>
                                                </div>
                                                <span className="npk-value">
                                                    {results.analysisType === 'traditional'
                                                        ? (results.soil?.N || 0)
                                                        : (results.traditionalAnalysis?.soil_data?.N || 0)
                                                    }
                                                </span>
                                            </div>
                                            <div className="progress-bar-container">
                                                <div className="progress-bar">
                                                    <div
                                                        className="progress-bar-fill nitrogen"
                                                        style={{
                                                            width: `${getNPKLevel(
                                                                results.analysisType === 'traditional'
                                                                    ? (results.soil?.N || 0)
                                                                    : (results.traditionalAnalysis?.soil_data?.N || 0),
                                                                'N'
                                                            )}%`
                                                        }}
                                                    ></div>
                                                </div>
                                                <span className="nutrient-status">
                                                    {getNPKLevel(
                                                        results.analysisType === 'traditional'
                                                            ? (results.soil?.N || 0)
                                                            : (results.traditionalAnalysis?.soil_data?.N || 0),
                                                        'N'
                                                    ) > 60 ? (
                                                        <><CheckCircle className="status-icon status-good" /> {t('pages:soilAnalysis.results.good')}</>
                                                    ) : getNPKLevel(
                                                        results.analysisType === 'traditional'
                                                            ? (results.soil?.N || 0)
                                                            : (results.traditionalAnalysis?.soil_data?.N || 0),
                                                        'N'
                                                    ) > 30 ? (
                                                        <><AlertCircle className="status-icon status-fair" /> {t('pages:soilAnalysis.results.fair')}</>
                                                    ) : (
                                                        <><AlertCircle className="status-icon status-low" /> {t('pages:soilAnalysis.results.low')}</>
                                                    )}
                                                </span>
                                            </div>
                                        </div>

                                        {/* Phosphorus */}
                                        <div className="npk-item">
                                            <div className="npk-header">
                                                <div className="npk-info">
                                                    <span className="npk-label">{t('pages:soilAnalysis.results.phosphorus')}</span>
                                                    <span className="npk-description">{t('pages:soilAnalysis.results.forRootStrength')}</span>
                                                </div>
                                                <span className="npk-value">
                                                    {results.analysisType === 'traditional'
                                                        ? (results.soil?.P || 0)
                                                        : (results.traditionalAnalysis?.soil_data?.P || 0)
                                                    }
                                                </span>
                                            </div>
                                            <div className="progress-bar-container">
                                                <div className="progress-bar">
                                                    <div
                                                        className="progress-bar-fill phosphorus"
                                                        style={{
                                                            width: `${getNPKLevel(
                                                                results.analysisType === 'traditional'
                                                                    ? (results.soil?.P || 0)
                                                                    : (results.traditionalAnalysis?.soil_data?.P || 0),
                                                                'P'
                                                            )}%`
                                                        }}
                                                    ></div>
                                                </div>
                                                <span className="nutrient-status">
                                                    {getNPKLevel(
                                                        results.analysisType === 'traditional'
                                                            ? (results.soil?.P || 0)
                                                            : (results.traditionalAnalysis?.soil_data?.P || 0),
                                                        'P'
                                                    ) > 60 ? (
                                                        <><CheckCircle className="status-icon status-good" /> {t('pages:soilAnalysis.results.good')}</>
                                                    ) : getNPKLevel(
                                                        results.analysisType === 'traditional'
                                                            ? (results.soil?.P || 0)
                                                            : (results.traditionalAnalysis?.soil_data?.P || 0),
                                                        'P'
                                                    ) > 30 ? (
                                                        <><AlertCircle className="status-icon status-fair" /> {t('pages:soilAnalysis.results.fair')}</>
                                                    ) : (
                                                        <><AlertCircle className="status-icon status-low" /> {t('pages:soilAnalysis.results.low')}</>
                                                    )}
                                                </span>
                                            </div>
                                        </div>

                                        {/* Potassium */}
                                        <div className="npk-item">
                                            <div className="npk-header">
                                                <div className="npk-info">
                                                    <span className="npk-label">{t('pages:soilAnalysis.results.potassium')}</span>
                                                    <span className="npk-description">{t('pages:soilAnalysis.results.forDiseaseResistance')}</span>
                                                </div>
                                                <span className="npk-value">
                                                    {results.analysisType === 'traditional'
                                                        ? (results.soil?.K || 0)
                                                        : (results.traditionalAnalysis?.soil_data?.K || 0)
                                                    }
                                                </span>
                                            </div>
                                            <div className="progress-bar-container">
                                                <div className="progress-bar">
                                                    <div
                                                        className="progress-bar-fill potassium"
                                                        style={{
                                                            width: `${getNPKLevel(
                                                                results.analysisType === 'traditional'
                                                                    ? (results.soil?.K || 0)
                                                                    : (results.traditionalAnalysis?.soil_data?.K || 0),
                                                                'K'
                                                            )}%`
                                                        }}
                                                    ></div>
                                                </div>
                                                <span className="nutrient-status">
                                                    {getNPKLevel(
                                                        results.analysisType === 'traditional'
                                                            ? (results.soil?.K || 0)
                                                            : (results.traditionalAnalysis?.soil_data?.K || 0),
                                                        'K'
                                                    ) > 60 ? (
                                                        <><CheckCircle className="status-icon status-good" /> {t('pages:soilAnalysis.results.good')}</>
                                                    ) : getNPKLevel(
                                                        results.analysisType === 'traditional'
                                                            ? (results.soil?.K || 0)
                                                            : (results.traditionalAnalysis?.soil_data?.K || 0),
                                                        'K'
                                                    ) > 30 ? (
                                                        <><AlertCircle className="status-icon status-fair" /> {t('pages:soilAnalysis.results.fair')}</>
                                                    ) : (
                                                        <><AlertCircle className="status-icon status-low" /> {t('pages:soilAnalysis.results.low')}</>
                                                    )}
                                                </span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            ) : null}

                            {/* Suitability Score Card - Only show for traditional analysis or when suitability data exists */}
                            {((results.analysisType === 'traditional' && results.suitability) || 
                              (results.analysisType === 'image_enhanced' && results.traditionalAnalysis?.basic_suitability)) && (
                            <div className="result-card suitability-card">
                                <div className="card-header">
                                    <div className="card-icon-wrapper">
                                        <TrendingUp className="header-icon" />
                                    </div>
                                    <h3 className="card-title">📊 {t('pages:soilAnalysis.results.cropSuitability')}</h3>
                                </div>
                                <p className="card-description">{t('pages:soilAnalysis.results.howSuitable', { crop: t(`common:crops.${formData.crop}`, { defaultValue: formData.crop }) })}</p>

                                <div className="suitability-content">
                                    <div className={`score-circle ${getSuitabilityLevel(
                                        results.analysisType === 'traditional' 
                                            ? (results.suitability?.suitability_score || 0)
                                            : (results.traditionalAnalysis?.basic_suitability?.suitability_score || 0)
                                    ).class}`}>
                                        <div className="score-value">
                                            {Math.round(
                                                results.analysisType === 'traditional' 
                                                    ? (results.suitability?.suitability_score || 0)
                                                    : (results.traditionalAnalysis?.basic_suitability?.suitability_score || 0)
                                            )}
                                        </div>
                                        <div className="score-max">/100</div>
                                    </div>

                                    <div className="suitability-message">
                                        <p className="suitability-description">
                                            {t('pages:soilAnalysis.results.cultivationIs', { 
                                                crop: t(`common:crops.${formData.crop}`, { defaultValue: formData.crop }), 
                                                level: getSuitabilityLevel(
                                                    results.analysisType === 'traditional' 
                                                        ? (results.suitability?.suitability_score || 0)
                                                        : (results.traditionalAnalysis?.basic_suitability?.suitability_score || 0)
                                                ).label.toLowerCase(),
                                                state: t(`common:states.${formData.state}`, { defaultValue: formData.state })
                                            })}
                                        </p>
                                        <div className="recommendation-tip">
                                            {getSuitabilityLevel(
                                                results.analysisType === 'traditional' 
                                                    ? (results.suitability?.suitability_score || 0)
                                                    : (results.traditionalAnalysis?.basic_suitability?.suitability_score || 0)
                                            ).class === 'poor' && 
                                                `💡 ${t('pages:soilAnalysis.results.tipPoor')}`
                                            }
                                            {getSuitabilityLevel(
                                                results.analysisType === 'traditional' 
                                                    ? (results.suitability?.suitability_score || 0)
                                                    : (results.traditionalAnalysis?.basic_suitability?.suitability_score || 0)
                                            ).class === 'fair' && 
                                                `💡 ${t('pages:soilAnalysis.results.tipFair')}`
                                            }
                                            {getSuitabilityLevel(
                                                results.analysisType === 'traditional' 
                                                    ? (results.suitability?.suitability_score || 0)
                                                    : (results.traditionalAnalysis?.basic_suitability?.suitability_score || 0)
                                            ).class === 'good' && 
                                                `👍 ${t('pages:soilAnalysis.results.tipGood')}`
                                            }
                                            {getSuitabilityLevel(
                                                results.analysisType === 'traditional' 
                                                    ? (results.suitability?.suitability_score || 0)
                                                    : (results.traditionalAnalysis?.basic_suitability?.suitability_score || 0)
                                            ).class === 'excellent' && 
                                                `🌟 ${t('pages:soilAnalysis.results.tipExcellent')}`
                                            }
                                        </div>
                                    </div>
                                </div>
                            </div>
                            )}
                        </div>

                        {/* Enhanced Analysis Cards */}
                        <div className="results-grid-secondary">
                            {((results.analysisType === 'traditional' && results.suitability?.irrigation_analysis) ||
                                (results.analysisType === 'image_enhanced' && results.traditionalAnalysis?.irrigation_analysis)) && (
                                    <div className="result-card enhanced-analysis-card">
                                        <div className="card-header">
                                            <Droplets className="header-icon" />
                                            <h3 className="card-title">{t('pages:soilAnalysis.results.irrigationAnalysis')}</h3>
                                        </div>
                                        <p className="card-description">
                                            {results.analysisType === 'traditional' 
                                                ? results.suitability?.irrigation_analysis?.message 
                                                : results.traditionalAnalysis?.irrigation_analysis?.message}
                                        </p>
                                        
                                        <div className="analysis-detail">
                                            <div className={`compatibility-badge ${
                                                results.analysisType === 'traditional' 
                                                    ? results.suitability?.irrigation_analysis?.compatibility 
                                                    : results.traditionalAnalysis?.irrigation_analysis?.compatibility
                                                    }`}>
                                                    {(
                                                        results.analysisType === 'traditional'
                                                            ? results.suitability?.irrigation_analysis?.compatibility
                                                            : results.traditionalAnalysis?.irrigation_analysis?.compatibility
                                                    )?.toUpperCase() || 'N/A'}
                                                </div>
                                                <p><strong>{t('pages:soilAnalysis.results.waterRequirement')}:</strong> {
                                                    (
                                                        results.analysisType === 'traditional'
                                                            ? results.suitability?.irrigation_analysis?.crop_water_requirement
                                                            : results.traditionalAnalysis?.irrigation_analysis?.crop_water_requirement
                                                    )?.toUpperCase() || 'Medium'
                                                }</p>
                                            </div>
                                        </div>
                                    )}

                            {((results.analysisType === 'traditional' && results.suitability?.water_quality_impact) ||
                                (results.analysisType === 'image_enhanced' && results.traditionalAnalysis?.water_quality_impact)) && (
                                    <div className="result-card enhanced-analysis-card">
                                        <div className="card-header">
                                            <TestTube className="header-icon" />
                                            <h3 className="card-title">{t('pages:soilAnalysis.results.waterQualityImpact')}</h3>
                                        </div>
                                        <p className="card-description">
                                            {results.analysisType === 'traditional' 
                                                ? results.suitability?.water_quality_impact?.message 
                                                : results.traditionalAnalysis?.water_quality_impact?.message}
                                        </p>
                                        
                                        <div className="analysis-detail">
                                            <div className={`impact-badge ${
                                                results.analysisType === 'traditional' 
                                                    ? results.suitability?.water_quality_impact?.impact 
                                                    : results.traditionalAnalysis?.water_quality_impact?.impact
                                                    }`}>
                                                    {(
                                                        results.analysisType === 'traditional'
                                                            ? results.suitability?.water_quality_impact?.impact
                                                            : results.traditionalAnalysis?.water_quality_impact?.impact
                                                    )?.toUpperCase() || 'N/A'}
                                                </div>
                                                <p><strong>{t('pages:soilAnalysis.results.saltTolerance')}:</strong> {
                                                    (
                                                        results.analysisType === 'traditional' 
                                                            ? results.suitability?.water_quality_impact?.crop_salt_tolerance
                                                            : results.traditionalAnalysis?.water_quality_impact?.crop_salt_tolerance
                                                    )?.toUpperCase() || 'Medium'
                                                }</p>
                                            </div>
                                        </div>
                                    )}

                            {((results.analysisType === 'traditional' && results.suitability?.rotation_analysis) ||
                                (results.analysisType === 'image_enhanced' && results.traditionalAnalysis?.rotation_analysis)) && (
                                    <div className="result-card rotation-card">
                                        <div className="card-header">
                                            <RotateCcw className="header-icon" />
                                            <h3 className="card-title">{t('pages:soilAnalysis.results.cropRotationAnalysis')}</h3>
                                        </div>
                                        <p className="card-description">
                                            {results.analysisType === 'traditional'
                                                ? results.suitability?.rotation_analysis?.message
                                                : results.traditionalAnalysis?.rotation_analysis?.message}
                                        </p>

                                        <div className="rotation-benefit">
                                        <div className={`benefit-badge ${
                                            results.analysisType === 'traditional' 
                                                ? results.suitability?.rotation_analysis?.benefit 
                                                : results.traditionalAnalysis?.rotation_analysis?.benefit
                                        }`}>
                                            {(
                                                results.analysisType === 'traditional' 
                                                    ? results.suitability?.rotation_analysis?.benefit 
                                                    : results.traditionalAnalysis?.rotation_analysis?.benefit
                                            )?.toUpperCase() || 'NEUTRAL'}
                                        </div>
                                        {(
                                            results.analysisType === 'traditional' 
                                                ? results.suitability?.rotation_analysis?.nitrogen_bonus
                                                : results.traditionalAnalysis?.rotation_analysis?.nitrogen_bonus
                                        ) && (
                                            <div className="bonus-tag">
                                                🌿 {t('pages:soilAnalysis.results.nitrogenBonus')}
                                            </div>
                                        )}
                                        {(
                                            results.analysisType === 'traditional' 
                                                ? results.suitability?.rotation_analysis?.risk_warning
                                                : results.traditionalAnalysis?.rotation_analysis?.risk_warning
                                        ) && (
                                            <div className="warning-tag">
                                                ⚠️ {t('pages:soilAnalysis.results.increasedPestRisk')}
                                            </div>
                                        )}
                                    </div>
                                </div>
                            )}
                        </div>

                        {/* Fertilizer Plan - Full Width */}
                        {((results.analysisType === 'traditional' && results.suitability?.input_recommendations) ||
                            (results.analysisType === 'image_enhanced' && results.traditionalAnalysis?.input_recommendations)) && (
                                <div className="result-card full-width fertilizer-plan-card">
                                    <div className="card-header">
                                        <Package className="header-icon" />
                                        <h3 className="card-title">Fertilizer Plan</h3>
                                    </div>
                                    <p className="card-description">For {
                                        results.analysisType === 'traditional'
                                            ? results.suitability?.input_recommendations?.field_size_hectares
                                            : results.traditionalAnalysis?.input_recommendations?.field_size_hectares
                                    } hectares</p>

                                    <div className="fertilizer-grid">
                                        <div className="fertilizer-section">
                                            <div className="section-header">
                                                <Sprout className="section-icon" />
                                                <h4>Total Requirements</h4>
                                            </div>
                                            <div className="nutrient-requirements">
                                                <div className="nutrient-item">
                                                    <span className="nutrient-label">{t('pages:soilAnalysis.results.nitrogen')}:</span>
                                                    <span className="nutrient-amount">{
                                                        results.analysisType === 'traditional'
                                                            ? results.suitability?.input_recommendations?.fertilizer_recommendations?.total_field?.N
                                                            : results.traditionalAnalysis?.input_recommendations?.fertilizer_recommendations?.total_field?.N
                                                    } kg</span>
                                                </div>
                                                <div className="nutrient-item">
                                                    <span className="nutrient-label">{t('pages:soilAnalysis.results.phosphorus')}:</span>
                                                    <span className="nutrient-amount">{
                                                        results.analysisType === 'traditional'
                                                            ? results.suitability?.input_recommendations?.fertilizer_recommendations?.total_field?.P
                                                            : results.traditionalAnalysis?.input_recommendations?.fertilizer_recommendations?.total_field?.P
                                                    } kg</span>
                                                </div>
                                                <div className="nutrient-item">
                                                    <span className="nutrient-label">{t('pages:soilAnalysis.results.potassium')}:</span>
                                                    <span className="nutrient-amount">{
                                                        results.analysisType === 'traditional'
                                                            ? results.suitability?.input_recommendations?.fertilizer_recommendations?.total_field?.K
                                                            : results.traditionalAnalysis?.input_recommendations?.fertilizer_recommendations?.total_field?.K
                                                    } kg</span>
                                                </div>
                                            </div>
                                        </div>

                                        <div className="fertilizer-section">
                                            <div className="section-header">
                                                <IndianRupee className="section-icon" />
                                                <h4>Cost Estimate</h4>
                                            </div>
                                            <div className="cost-breakdown">
                                                <div className="cost-item">
                                                    <span>{t('pages:soilAnalysis.results.totalCost')}:</span>
                                                    <span className="cost-value">₹{
                                                        results.analysisType === 'traditional'
                                                            ? results.suitability?.input_recommendations?.estimated_cost?.total_inr
                                                            : results.traditionalAnalysis?.input_recommendations?.estimated_cost?.total_inr
                                                    }</span>
                                                </div>
                                                <div className="cost-item">
                                                    <span>{t('pages:soilAnalysis.results.perHectare')}:</span>
                                                    <span className="cost-value">₹{
                                                        results.analysisType === 'traditional'
                                                            ? results.suitability?.input_recommendations?.estimated_cost?.per_hectare_inr
                                                            : results.traditionalAnalysis?.input_recommendations?.estimated_cost?.per_hectare_inr
                                                    }</span>
                                                </div>
                                            </div>
                                        </div>

                                        <div className="fertilizer-section">
                                            <div className="section-header">
                                                <Calendar className="section-icon" />
                                                <h4>Application Schedule</h4>
                                            </div>
                                            <ul className="timing-list">
                                                {(
                                                    results.analysisType === 'traditional'
                                                        ? results.suitability?.input_recommendations?.application_timing
                                                        : results.traditionalAnalysis?.input_recommendations?.application_timing
                                                )?.map((timing, index) => (
                                                    <li key={index}>
                                                        <CheckCircle className="timing-icon" />
                                                        {timing}
                                                    </li>
                                                )) || []}
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            )}

                        {/* Recommended Crops Card */}
                        <div className="result-card full-width recommendations-card">
                            <div className="card-header">
                                <Wheat className="header-icon" />
                                <h3 className="card-title">Best Crops for {formData.state}</h3>
                            </div>
                            <p className="card-description">Crops that grow well in your soil conditions</p>

                            <div className="recommendations-grid">
                                {(results.recommendations?.recommended_crops || []).slice(0, 6).map((item, index) => {
                                    const suitabilityLevel = getSuitabilityLevel(item.suitability_score);
                                    return (
                                        <div key={index} className={`recommendation-item ${suitabilityLevel.class}`}>
                                            <Sprout className="crop-icon" />
                                            <div className="recommendation-content">
                                                <span className="recommendation-text">{t(`common:crops.${item.crop}`, { defaultValue: item.crop })}</span>
                                                <div className="crop-suitability">
                                                    <span className="recommendation-score">{item.suitability_score}%</span>
                                                    <span className={`crop-rating ${suitabilityLevel.class}`}>
                                                        {t(`pages:soilAnalysis.results.${suitabilityLevel.label.toLowerCase()}`, { defaultValue: suitabilityLevel.label })}
                                                    </span>
                                                </div>
                                            </div>
                                            <CheckCircle className="check-icon" />
                                        </div>
                                    );
                                })}


                            </div>

                            {results.recommendations?.recommended_crops && results.recommendations.recommended_crops.length > 6 && (
                                <div className="recommendations-note">
                                    <Star className="note-icon" />
                                    <p><strong>{results.recommendations.recommended_crops.length - 6} more crops</strong> are suitable for your soil!</p>
                                </div>
                            )}
                        </div>
                    </>
                )}
            </div>

            {/* Field Help Modal */}
            <FieldHelpModal
                isOpen={helpModalOpen}
                onClose={() => setHelpModalOpen(false)}
                fieldLabel={helpFieldLabel}
                fieldName={helpFieldName}
            />
        </div>
    );
};

export default SoilAnalysis;