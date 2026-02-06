import React from 'react';
import { AlertTriangle, CheckCircle, Clock, Bug, Search, AlertCircle as VirusIcon, Sprout, Shield } from 'lucide-react';

const DetectionResults = ({ result }) => {
    if (!result) return null;

    const { detected_disease, estimated_severity, crop_type, location, timestamp } = result;
    
    const getSeverityIcon = (severity) => {
        switch (severity) {
            case 'mild':
                return <CheckCircle className="w-4 h-4" />;
            case 'moderate':
                return <Clock className="w-4 h-4" />;
            case 'severe':
                return <AlertTriangle className="w-4 h-4" />;
            default:
                return <Bug className="w-4 h-4" />;
        }
    };

    const formatDate = (dateString) => {
        return new Date(dateString).toLocaleDateString('en-IN', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    return (
        <div className="detection-results-card">
            <div className="disease-header">
                <div>
                    <h2 className="disease-name">{detected_disease.name}</h2>
                    <div className="flex flex-wrap gap-2 mt-2">
                        <span className={`severity-badge severity-${estimated_severity}`}>
                            {getSeverityIcon(estimated_severity)}
                            <span className="ml-1 capitalize">{estimated_severity}</span>
                        </span>
                        <span className="confidence-badge">
                            {Math.round(detected_disease.confidence * 100)}% Confidence
                        </span>
                    </div>
                </div>
            </div>

            {/* Detection Info */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6 text-sm">
                <div>
                    <span className="font-medium text-gray-600">Crop:</span>
                    <span className="ml-2 text-gray-800">{crop_type}</span>
                </div>
                {location && (
                    <div>
                        <span className="font-medium text-gray-600">Location:</span>
                        <span className="ml-2 text-gray-800">{location}</span>
                    </div>
                )}
                <div className="md:col-span-2">
                    <span className="font-medium text-gray-600">Detected:</span>
                    <span className="ml-2 text-gray-800">{formatDate(timestamp)}</span>
                </div>
            </div>

            {/* Symptoms */}
            {detected_disease.symptoms && detected_disease.symptoms.length > 0 && (
                <div className="info-section">
                    <h3 className="info-title">
                        <Search className="info-icon" />
                        Symptoms
                    </h3>
                    <ul className="info-list">
                        {detected_disease.symptoms.map((symptom, index) => (
                            <li key={index}>{symptom}</li>
                        ))}
                    </ul>
                </div>
            )}

            {/* Causes */}
            {detected_disease.causes && detected_disease.causes.length > 0 && (
                <div className="info-section">
                    <h3 className="info-title">
                        <VirusIcon className="info-icon" />
                        Causes
                    </h3>
                    <ul className="info-list">
                        {detected_disease.causes.map((cause, index) => (
                            <li key={index}>{cause}</li>
                        ))}
                    </ul>
                </div>
            )}

            {/* Affected Crops */}
            {detected_disease.crops_affected && detected_disease.crops_affected.length > 0 && (
                <div className="info-section">
                    <h3 className="info-title">
                        <Sprout className="info-icon" />
                        Commonly Affects
                    </h3>
                    <div className="flex flex-wrap gap-1">
                        {detected_disease.crops_affected.map((crop, index) => (
                            <span key={index} className="crop-tag">{crop}</span>
                        ))}
                    </div>
                </div>
            )}

            {/* Prevention */}
            {detected_disease.prevention && detected_disease.prevention.length > 0 && (
                <div className="info-section">
                    <h3 className="info-title">
                        <Shield className="info-icon" />
                        Prevention
                    </h3>
                    <ul className="info-list">
                        {detected_disease.prevention.map((prevention, index) => (
                            <li key={index}>{prevention}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default DetectionResults;