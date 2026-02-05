import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { Bug, AlertCircle, CheckCircle, Loader2, MessageCircle, ExternalLink } from 'lucide-react';
import ImageUpload from '../components/disease/ImageUpload';
import DetectionResults from '../components/disease/DetectionResults';
import DiseaseList from '../components/disease/DiseaseList';
import TreatmentPlan from '../components/disease/TreatmentPlan';
import FieldHelpIcon from '../components/FieldHelpIcon';
import FieldHelpModal from '../components/FieldHelpModal';
import { VoiceSummary } from '../components/voice';
import '../styles/disease-detection.css';
import '../styles/pages.css';

const DiseaseDetection = () => {
    const { t } = useTranslation(['pages', 'common']);
    const [activeTab, setActiveTab] = useState('detect');
    const [selectedImage, setSelectedImage] = useState(null);
    const [cropType, setCropType] = useState('Rice');
    const [location, setLocation] = useState('');
    const [isDetecting, setIsDetecting] = useState(false);
    const [detectionResult, setDetectionResult] = useState(null);
    const [error, setError] = useState(null);
    const [diseases, setDiseases] = useState([]);
    
    // Field help modal state
    const [helpModalOpen, setHelpModalOpen] = useState(false);
    const [helpFieldLabel, setHelpFieldLabel] = useState('');
    const [helpFieldName, setHelpFieldName] = useState('');

    const cropOptions = [
        'Rice', 'Wheat', 'Cotton', 'Tomato', 'Potato', 'Maize', 'Sugarcane',
        'Soybean', 'Barley', 'Mustard', 'Groundnut', 'Sunflower'
    ];

    // Fetch diseases on component mount
    useEffect(() => {
        fetchDiseases();
    }, []);

    const fetchDiseases = async (filterCrop = null) => {
        try {
            const url = filterCrop 
                ? `http://localhost:8000/api/v1/disease/diseases?crop_type=${encodeURIComponent(filterCrop)}`
                : 'http://localhost:8000/api/v1/disease/diseases';
            
            const response = await fetch(url);
            const data = await response.json();
            
            if (data.success) {
                setDiseases(data.data);
            }
        } catch (err) {
            console.error('Failed to fetch diseases:', err);
        }
    };

    const handleImageSelect = (file) => {
        setSelectedImage(file);
        setDetectionResult(null);
        setError(null);
    };

    const handleDetectDisease = async () => {
        if (!selectedImage) {
            setError('Please select an image first');
            return;
        }

        setIsDetecting(true);
        setError(null);

        try {
            const formData = new FormData();
            formData.append('file', selectedImage);
            formData.append('crop_type', cropType);
            if (location.trim()) {
                formData.append('location', location);
            }

            const response = await fetch('http://localhost:8000/api/v1/disease/detect', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                setDetectionResult(data.data);
            } else {
                setError(data.message || 'Detection failed');
            }
        } catch (err) {
            setError('Failed to detect disease. Please try again.');
            console.error('Detection error:', err);
        } finally {
            setIsDetecting(false);
        }
    };

    const handleReset = () => {
        setSelectedImage(null);
        setDetectionResult(null);
        setError(null);
        setLocation('');
    };
    
    // Handle help icon click
    const handleHelpClick = (fieldName, fieldLabel) => {
        setHelpFieldName(fieldName);
        setHelpFieldLabel(fieldLabel);
        setHelpModalOpen(true);
    };

    return (
        <div className="page-container">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {/* Header */}
                <div className="text-center mb-8">
                    <h1 className="page-header-title">
                        <Bug className="inline-block w-8 h-8 mr-3 text-green-600" />
                        {t('diseaseDetection.title')}
                    </h1>
                    <p className="page-header-subtitle">
                        {t('diseaseDetection.subtitle')}
                    </p>
                </div>

                {/* Tab Navigation */}
                <div className="disease-tabs mb-8">
                    <button
                        className={`tab-button ${activeTab === 'detect' ? 'tab-active' : ''}`}
                        onClick={() => setActiveTab('detect')}
                    >
                        🔬 Disease Detection
                    </button>
                    <button
                        className={`tab-button ${activeTab === 'database' ? 'tab-active' : ''}`}
                        onClick={() => setActiveTab('database')}
                    >
                        📚 Disease Database
                    </button>
                    <button
                        className={`tab-button ${activeTab === 'aiagent' ? 'tab-active' : ''}`}
                        onClick={() => setActiveTab('aiagent')}
                    >
                        🤖 AI Agent
                    </button>
                </div>

                {/* Tab Content */}
                {activeTab === 'aiagent' ? (
                    <div className="ai-agent-section">
                        <div className="ai-agent-card">
                            <div className="ai-agent-icon">
                                <MessageCircle className="w-16 h-16" />
                            </div>
                            <h2 className="ai-agent-title">Disease Detection AI Agent</h2>
                            <p className="ai-agent-description">
                                Get instant disease detection and expert farming advice through our intelligent Telegram bot. 
                                Available 24/7 to answer your questions, analyze crop images, and provide personalized recommendations.
                            </p>
                            
                            <div className="ai-agent-features">
                                <div className="feature-item">
                                    <CheckCircle className="w-5 h-5" />
                                    <span>Instant image-based disease detection</span>
                                </div>
                                <div className="feature-item">
                                    <CheckCircle className="w-5 h-5" />
                                    <span>24/7 expert farming assistance</span>
                                </div>
                                <div className="feature-item">
                                    <CheckCircle className="w-5 h-5" />
                                    <span>Personalized crop recommendations</span>
                                </div>
                                <div className="feature-item">
                                    <CheckCircle className="w-5 h-5" />
                                    <span>Multi-language support</span>
                                </div>
                            </div>

                            <a 
                                href="https://t.me/fasalmitra_ai_bot" 
                                target="_blank" 
                                rel="noopener noreferrer"
                                className="telegram-bot-button"
                            >
                                <MessageCircle className="w-5 h-5" />
                                <span>Open Telegram Bot</span>
                                <ExternalLink className="w-4 h-4" />
                            </a>

                            <div className="ai-agent-note">
                                <AlertCircle className="w-4 h-4" />
                                <span>Note: You need Telegram installed on your device to use this service.</span>
                            </div>
                        </div>
                    </div>
                ) : activeTab === 'detect' ? (
                    <div className="disease-detection-content">
                        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                            {/* Left Column - Input Section */}
                            <div className="detection-input-section">
                                <div className="input-card">
                                    <h2 className="section-title">Upload Image</h2>
                                    <ImageUpload
                                        onImageSelect={handleImageSelect}
                                        selectedImage={selectedImage}
                                    />

                                    {/* Crop Selection */}
                                    <div className="form-group">
                                        <label className="form-label">
                                            Crop Type
                                            <FieldHelpIcon 
                                                fieldName="crop" 
                                                onClick={() => handleHelpClick('crop', 'Crop Type')} 
                                            />
                                        </label>
                                        <select
                                            value={cropType}
                                            onChange={(e) => setCropType(e.target.value)}
                                            className="form-select"
                                        >
                                            {cropOptions.map(crop => (
                                                <option key={crop} value={crop}>{crop}</option>
                                            ))}
                                        </select>
                                    </div>

                                    {/* Location (Optional) */}
                                    <div className="form-group">
                                        <label className="form-label">Location (Optional)</label>
                                        <input
                                            type="text"
                                            value={location}
                                            onChange={(e) => setLocation(e.target.value)}
                                            placeholder="e.g., Punjab, Maharashtra"
                                            className="form-input"
                                        />
                                    </div>

                                    {/* Action Buttons */}
                                    <div className="action-buttons">
                                        <button
                                            onClick={handleDetectDisease}
                                            disabled={!selectedImage || isDetecting}
                                            className="detect-button"
                                        >
                                            {isDetecting ? (
                                                <>
                                                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                                                    Analyzing...
                                                </>
                                            ) : (
                                                <>
                                                    <Bug className="w-4 h-4 mr-2" />
                                                    Detect Disease
                                                </>
                                            )}
                                        </button>

                                        <button
                                            onClick={handleReset}
                                            className="reset-button"
                                        >
                                            Reset
                                        </button>
                                    </div>

                                    {/* Error Display */}
                                    {error && (
                                        <div className="error-message">
                                            <AlertCircle className="w-4 h-4 mr-2" />
                                            {error}
                                        </div>
                                    )}
                                </div>
                            </div>

                            {/* Right Column - Results Section */}
                            <div className="detection-results-section">
                                {detectionResult ? (
                                    <div className="space-y-6">
                                        <DetectionResults result={detectionResult} />
                                        <TreatmentPlan 
                                            treatmentPlan={detectionResult.treatment_plan}
                                            severity={detectionResult.estimated_severity}
                                            recommendations={detectionResult.recommendations}
                                        />
                                        
                                        {/* Voice Summary for Disease Detection Results */}
                                        <VoiceSummary
                                            result={detectionResult}
                                            resultType="diseaseDetection"
                                            title="🎧 Disease Analysis Summary"
                                            className="disease-voice-summary"
                                            onSpeechStart={() => console.log('Started reading disease detection summary')}
                                            onSpeechEnd={() => console.log('Finished reading disease detection summary')}
                                            onSpeechError={(error) => console.error('Disease speech error:', error)}
                                        />
                                    </div>
                                ) : (
                                    <div className="results-placeholder">
                                        <div className="placeholder-icon">
                                            <Bug className="w-16 h-16 text-gray-300" />
                                        </div>
                                        <h3 className="text-lg font-medium text-gray-500 mb-2">
                                            No Detection Yet
                                        </h3>
                                        <p className="text-gray-400 text-center">
                                            Upload an image and click "Detect Disease" to see results here
                                        </p>
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>
                ) : (
                    <DiseaseList 
                        diseases={diseases} 
                        onFilterChange={fetchDiseases}
                        cropOptions={cropOptions}
                    />
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

export default DiseaseDetection;