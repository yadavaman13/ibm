import React from 'react';
import { AlertTriangle, CheckCircle, Clock, Bug, Search, AlertCircle as VirusIcon, Sprout, Shield } from 'lucide-react';

const DetectionResults = ({ result }) => {
    if (!result) return null;

    // Handle both old and new API response structures
    const isNewMLFormat = result.disease_name && !result.detected_disease;
    
    const diseaseData = isNewMLFormat ? {
        name: result.disease_name,
        confidence: result.confidence / 100, // Convert from percentage back to decimal
        symptoms: result.cause ? [result.cause] : [],
        causes: result.cause ? [result.cause] : [],
        crops_affected: result.detected_crop ? [result.detected_crop] : [],
        prevention: []
    } : result.detected_disease;

    const severity = isNewMLFormat ? result.severity : result.estimated_severity;
    const cropType = result.crop_type || result.detected_crop;
    const location = result.location;
    const timestamp = result.timestamp;
    const isHealthy = result.is_healthy;
    const treatment = result.treatment;
    const recommendations = result.recommendations;
    const nextSteps = result.next_steps;
    
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
            {/* Health Status Banner for Healthy Plants */}
            {isHealthy && (
                <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-4">
                    <div className="flex items-center gap-2">
                        <CheckCircle className="w-6 h-6 text-green-600" />
                        <div>
                            <h3 className="font-semibold text-green-800">Plant is Healthy!</h3>
                            <p className="text-sm text-green-700">No disease detected. Continue good care practices.</p>
                        </div>
                    </div>
                </div>
            )}

            <div className="disease-header">
                <div>
                    <h2 className="disease-name">{diseaseData.name}</h2>
                    <div className="flex flex-wrap gap-2 mt-2">
                        {severity && severity !== 'none' && (
                            <span className={`severity-badge severity-${severity}`}>
                                {getSeverityIcon(severity)}
                                <span className="ml-1 capitalize">{severity}</span>
                            </span>
                        )}
                        <span className="confidence-badge">
                            {Math.round(diseaseData.confidence * 100)}% Confidence
                        </span>
                    </div>
                </div>
            </div>

            {/* Detection Info */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6 text-sm">
                <div>
                    <span className="font-medium text-gray-600">Crop:</span>
                    <span className="ml-2 text-gray-800">{cropType}</span>
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

            {/* Treatment (New ML Format) */}
            {treatment && !isHealthy && (
                <div className="info-section bg-blue-50 border border-blue-200">
                    <h3 className="info-title text-blue-800">
                        <Shield className="info-icon text-blue-600" />
                        Treatment
                    </h3>
                    <p className="text-gray-700">{treatment}</p>
                </div>
            )}

            {/* Symptoms */}
            {diseaseData.symptoms && diseaseData.symptoms.length > 0 && (
                <div className="info-section">
                    <h3 className="info-title">
                        <Search className="info-icon" />
                        Symptoms / Cause
                    </h3>
                    <ul className="info-list">
                        {diseaseData.symptoms.map((symptom, index) => (
                            <li key={index}>{symptom}</li>
                        ))}
                    </ul>
                </div>
            )}

            {/* Recommendations (New ML Format) */}
            {recommendations && recommendations.length > 0 && (
                <div className="info-section">
                    <h3 className="info-title">
                        <AlertTriangle className="info-icon" />
                        Recommendations
                    </h3>
                    <ul className="info-list">
                        {recommendations.map((recommendation, index) => (
                            <li key={index}>{recommendation}</li>
                        ))}
                    </ul>
                </div>
            )}

            {/* Next Steps (New ML Format) */}
            {nextSteps && nextSteps.length > 0 && (
                <div className="info-section bg-amber-50 border border-amber-200">
                    <h3 className="info-title text-amber-800">
                        <Clock className="info-icon text-amber-600" />
                        Next Steps
                    </h3>
                    <ol className="info-list list-decimal pl-5">
                        {nextSteps.map((step, index) => (
                            <li key={index} className="text-gray-700">{step}</li>
                        ))}
                    </ol>
                </div>
            )}

            {/* Causes (Old Format - keep for backward compatibility) */}
            {diseaseData.causes && diseaseData.causes.length > 0 && diseaseData.causes !== diseaseData.symptoms && (
                <div className="info-section">
                    <h3 className="info-title">
                        <VirusIcon className="info-icon" />
                        Causes
                    </h3>
                    <ul className="info-list">
                        {diseaseData.causes.map((cause, index) => (
                            <li key={index}>{cause}</li>
                        ))}
                    </ul>
                </div>
            )}

            {/* Affected Crops */}
            {diseaseData.crops_affected && diseaseData.crops_affected.length > 0 && (
                <div className="info-section">
                    <h3 className="info-title">
                        <Sprout className="info-icon" />
                        Commonly Affects
                    </h3>
                    <div className="flex flex-wrap gap-1">
                        {diseaseData.crops_affected.map((crop, index) => (
                            <span key={index} className="crop-tag">{crop}</span>
                        ))}
                    </div>
                </div>
            )}

            {/* Prevention */}
            {diseaseData.prevention && diseaseData.prevention.length > 0 && (
                <div className="info-section">
                    <h3 className="info-title">
                        <Shield className="info-icon" />
                        Prevention
                    </h3>
                    <ul className="info-list">
                        {diseaseData.prevention.map((prevention, index) => (
                            <li key={index}>{prevention}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default DetectionResults;