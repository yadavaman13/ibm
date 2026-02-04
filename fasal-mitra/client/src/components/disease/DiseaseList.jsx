import React, { useState } from 'react';
import { Search, Filter } from 'lucide-react';

const DiseaseList = ({ diseases, onFilterChange, cropOptions }) => {
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedCrop, setSelectedCrop] = useState('');
    
    const filteredDiseases = diseases.filter(disease => {
        const matchesSearch = disease.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                            disease.symptoms.some(symptom => 
                                symptom.toLowerCase().includes(searchTerm.toLowerCase())
                            );
        return matchesSearch;
    });

    const handleCropFilter = (crop) => {
        setSelectedCrop(crop);
        onFilterChange(crop || null);
    };

    return (
        <div className="disease-database">
            {/* Header */}
            <div className="disease-database-header">
                <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
                    <h2 className="text-xl font-semibold text-gray-800">
                        Disease Database ({filteredDiseases.length} diseases)
                    </h2>
                    
                    <div className="flex flex-col sm:flex-row gap-3 w-full sm:w-auto">
                        {/* Search */}
                        <div className="relative">
                            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                            <input
                                type="text"
                                placeholder="Search diseases..."
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                                className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 w-full sm:w-64"
                            />
                        </div>
                        
                        {/* Crop Filter */}
                        <div className="relative database-filter">
                            <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                            <select
                                value={selectedCrop}
                                onChange={(e) => handleCropFilter(e.target.value)}
                                className="pl-10 pr-8 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 appearance-none bg-white w-full"
                            >
                                <option value="">All Crops</option>
                                {cropOptions.map(crop => (
                                    <option key={crop} value={crop}>{crop}</option>
                                ))}
                            </select>
                        </div>
                    </div>
                </div>
            </div>

            {/* Disease Grid */}
            <div className="disease-grid">
                {filteredDiseases.length > 0 ? (
                    filteredDiseases.map((disease, index) => (
                        <DiseaseCard key={disease.disease_id || index} disease={disease} />
                    ))
                ) : (
                    <div className="col-span-full text-center py-12">
                        <div className="text-gray-400 mb-2">
                            <Search className="w-12 h-12 mx-auto mb-3" />
                        </div>
                        <h3 className="text-lg font-medium text-gray-500 mb-2">
                            No diseases found
                        </h3>
                        <p className="text-gray-400">
                            {searchTerm || selectedCrop 
                                ? 'Try adjusting your search or filter criteria'
                                : 'No diseases available in the database'
                            }
                        </p>
                    </div>
                )}
            </div>
        </div>
    );
};

const DiseaseCard = ({ disease }) => {
    const [isExpanded, setIsExpanded] = useState(false);
    
    return (
        <div className="disease-card">
            <div className="disease-card-title">{disease.name}</div>
            
            {/* Crops Affected */}
            <div className="crops-affected">
                <p className="text-xs font-medium text-gray-600 mb-2">AFFECTS:</p>
                <div className="flex flex-wrap gap-1">
                    {disease.crops_affected.slice(0, 3).map((crop, index) => (
                        <span key={index} className="crop-tag">{crop}</span>
                    ))}
                    {disease.crops_affected.length > 3 && (
                        <span className="crop-tag">+{disease.crops_affected.length - 3} more</span>
                    )}
                </div>
            </div>
            
            {/* Symptoms Preview */}
            <div className="mb-4">
                <p className="text-xs font-medium text-gray-600 mb-2">SYMPTOMS:</p>
                <ul className="text-sm text-gray-600 space-y-1">
                    {disease.symptoms.slice(0, isExpanded ? disease.symptoms.length : 2).map((symptom, index) => (
                        <li key={index} className="flex items-start">
                            <span className="text-green-600 mr-2">•</span>
                            <span>{symptom}</span>
                        </li>
                    ))}
                </ul>
                
                {disease.symptoms.length > 2 && (
                    <button
                        onClick={() => setIsExpanded(!isExpanded)}
                        className="text-green-600 text-sm mt-2 hover:text-green-700 transition-colors"
                    >
                        {isExpanded 
                            ? `Show less` 
                            : `Show ${disease.symptoms.length - 2} more symptoms`
                        }
                    </button>
                )}
            </div>
        </div>
    );
};

export default DiseaseList;