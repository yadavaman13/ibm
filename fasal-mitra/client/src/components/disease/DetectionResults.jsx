import React from 'react';
import { AlertTriangle, CheckCircle, Clock, Bug, Search, AlertCircle as VirusIcon, Sprout, Shield, Sparkles, Eye, Lightbulb, BookOpen } from 'lucide-react';
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
    const llmAdvice = result.llm_advice; // New: AI-generated personalized advice
    const simpleExplanation = result.simple_explanation; // Farmer-friendly explanation
    const howToSpot = result.how_to_spot; // Visual identification guide
    const preventionTips = result.prevention_tips; // Prevention measures
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
                    <span className="ml-2 text-gray-800">{cropType}</span>
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

            {/* Understanding the Disease - Simple Explanation (FARMERS FRIENDLY) */}
            {simpleExplanation && (
                <div className="info-section bg-gradient-to-r from-green-50 to-emerald-50 border-2 border-green-300">
                    <h3 className="info-title text-green-800 flex items-center gap-2">
                        <BookOpen className="info-icon text-green-600" />
                        Understanding the Disease
                        <span className="text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded-full">Easy to Understand</span>
                    </h3>
                    <p className="text-gray-800 text-base leading-relaxed">{simpleExplanation}</p>
                </div>
            )}

            {/* How to Identify/Spot - Visual Symptoms (FARMERS FRIENDLY) */}
            {howToSpot && !isHealthy && (
                <div className="info-section bg-gradient-to-r from-yellow-50 to-amber-50 border-2 border-yellow-300">
                    <h3 className="info-title text-yellow-900 flex items-center gap-2">
                        <Eye className="info-icon text-yellow-600" />
                        How to Identify This Disease
                        <span className="text-xs bg-yellow-100 text-yellow-700 px-2 py-0.5 rounded-full">Look for These Signs</span>
                    </h3>
                    <p className="text-gray-800 text-base leading-relaxed">{howToSpot}</p>
                </div>
            )}

            {/* Prevention Tips (FARMERS FRIENDLY) */}
            {preventionTips && (
                <div className="info-section bg-gradient-to-r from-blue-50 to-cyan-50 border-2 border-blue-300">
                    <h3 className="info-title text-blue-900 flex items-center gap-2">
                        <Lightbulb className="info-icon text-blue-600" />
                        Prevention Tips
                        <span className="text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full">Protect Your Crop</span>
                    </h3>
                    <p className="text-gray-800 text-base leading-relaxed">{preventionTips}</p>
                </div>
            )}

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

            {/* AI-Generated Personalized Advice (NEW) */}
            {llmAdvice && !isHealthy && (
                <div className="info-section bg-gradient-to-r from-purple-50 to-blue-50 border-2 border-purple-300">
                    <h3 className="info-title text-purple-800 flex items-center gap-2">
                        <Sparkles className="info-icon text-purple-600 animate-pulse" />
                        AI-Powered Personalized Treatment Advice
                        <span className="text-xs bg-purple-100 text-purple-700 px-2 py-0.5 rounded-full">New</span>
                    </h3>
                    <div className="prose prose-sm max-w-none text-gray-700 whitespace-pre-line">
                        {llmAdvice}
                    </div>
                    <div className="mt-3 text-xs text-purple-600 flex items-center gap-1">
                        <VirusIcon className="w-3 h-3" />
                        <span>Generated by AI - Always consult local agricultural experts for serious issues</span>
                    </div>
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
            {/* Causes */}
            {detected_disease.causes && detected_disease.causes.length > 0 && (
                <div className="info-section">
                    <h3 className="info-title">
                        <VirusIcon className="info-icon" />
                        Causes
                    </h3>
                    <ul className="info-list">
                        {diseaseData.causes.map((cause, index) => (
                        {detected_disease.causes.map((cause, index) => (
                            <li key={index}>{cause}</li>
                        ))}
                    </ul>
                </div>
            )}

            {/* Affected Crops */}
            {diseaseData.crops_affected && diseaseData.crops_affected.length > 0 && (
            {detected_disease.crops_affected && detected_disease.crops_affected.length > 0 && (
                <div className="info-section">
                    <h3 className="info-title">
                        <Sprout className="info-icon" />
                        Commonly Affects
                    </h3>
                    <div className="flex flex-wrap gap-1">
                        {diseaseData.crops_affected.map((crop, index) => (
                        {detected_disease.crops_affected.map((crop, index) => (
                            <span key={index} className="crop-tag">{crop}</span>
                        ))}
                    </div>
                </div>
            )}

            {/* Prevention */}
            {diseaseData.prevention && diseaseData.prevention.length > 0 && (
            {detected_disease.prevention && detected_disease.prevention.length > 0 && (
                <div className="info-section">
                    <h3 className="info-title">
                        <Shield className="info-icon" />
                        Prevention
                    </h3>
                    <ul className="info-list">
                        {diseaseData.prevention.map((prevention, index) => (
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