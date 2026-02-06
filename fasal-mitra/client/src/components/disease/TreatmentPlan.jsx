import React from 'react';
import { IndianRupee, CheckCircle, AlertTriangle, Clock, Pill, Lightbulb } from 'lucide-react';

const TreatmentPlan = ({ treatmentPlan, severity, recommendations }) => {
    if (!treatmentPlan) return null;

    const getSeverityColor = (severity) => {
        switch (severity) {
            case 'mild':
                return 'text-green-600 bg-green-50';
            case 'moderate':
                return 'text-yellow-600 bg-yellow-50';
            case 'severe':
                return 'text-red-600 bg-red-50';
            default:
                return 'text-gray-600 bg-gray-50';
        }
    };

    const getSeverityIcon = (severity) => {
        switch (severity) {
            case 'mild':
                return <CheckCircle className="w-4 h-4" />;
            case 'moderate':
                return <Clock className="w-4 h-4" />;
            case 'severe':
                return <AlertTriangle className="w-4 h-4" />;
            default:
                return <AlertTriangle className="w-4 h-4" />;
        }
    };

    return (
        <div className="treatment-card">
            {/* Header */}
            <div className="treatment-header">
                <div className={`flex items-center px-3 py-1 rounded-full ${getSeverityColor(severity)}`}>
                    {getSeverityIcon(severity)}
                    <span className="ml-2 font-medium text-sm capitalize">
                        {severity} Treatment Plan
                    </span>
                </div>
            </div>

            {/* Cost Estimate */}
            {treatmentPlan.cost_estimate && (
                <div className="cost-estimate">
                    <div className="flex items-center justify-between">
                        <span className="text-sm font-medium text-gray-600">
                            Estimated Treatment Cost:
                        </span>
                        <div className="flex items-center cost-amount">
                            <IndianRupee className="w-4 h-4 mr-1" />
                            <span>{treatmentPlan.cost_estimate}</span>
                        </div>
                    </div>
                </div>
            )}

            {/* Treatment Steps */}
            {treatmentPlan.treatments && treatmentPlan.treatments.length > 0 && (
                <div className="info-section">
                    <h3 className="info-title">
                        <Pill className="info-icon" />
                        Treatment Steps
                    </h3>
                    <div className="space-y-3">
                        {treatmentPlan.treatments.map((treatment, index) => (
                            <div key={index} className="flex items-start">
                                <div className="flex-shrink-0 w-6 h-6 bg-green-100 text-green-600 rounded-full flex items-center justify-center text-sm font-medium mr-3">
                                    {index + 1}
                                </div>
                                <p className="text-sm text-gray-700 leading-relaxed">{treatment}</p>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Recommendations */}
            {recommendations && recommendations.length > 0 && (
                <div className="info-section">
                    <h3 className="info-title">
                        <Lightbulb className="info-icon" />
                        Additional Recommendations
                    </h3>
                    <ul className="info-list">
                        {recommendations.map((recommendation, index) => (
                            <li key={index}>{recommendation}</li>
                        ))}
                    </ul>
                </div>
            )}

            {/* Urgency Indicator */}
            <div className={`mt-4 p-3 rounded-lg ${getSeverityColor(severity)}`}>
                <div className="flex items-center">
                    {getSeverityIcon(severity)}
                    <div className="ml-3">
                        <p className="text-sm font-medium">
                            {severity === 'mild' && 'Monitor and take preventive action'}
                            {severity === 'moderate' && 'Start treatment within 2-3 days'}
                            {severity === 'severe' && 'Immediate treatment required!'}
                        </p>
                        <p className="text-xs mt-1 opacity-75">
                            {severity === 'mild' && 'Disease is manageable with proper care'}
                            {severity === 'moderate' && 'Early intervention can prevent spread'}
                            {severity === 'severe' && 'Delay may cause significant crop loss'}
                        </p>
                    </div>
                </div>
            </div>

            {/* Action Buttons */}
            <div className="mt-4 flex gap-3">
                <button className="flex-1 bg-green-600 text-white py-2 px-4 rounded-lg hover:bg-green-700 transition-colors text-sm font-medium">
                    Save Treatment Plan
                </button>
                <button className="flex-1 border border-gray-300 text-gray-700 py-2 px-4 rounded-lg hover:bg-gray-50 transition-colors text-sm font-medium">
                    Share with Expert
                </button>
            </div>

            {/* Footer Note */}
            <div className="mt-4 text-xs text-gray-500 text-center border-t pt-3">
                <p>⚠️ Consult with local agricultural experts before applying treatments</p>
            </div>
        </div>
    );
};

export default TreatmentPlan;