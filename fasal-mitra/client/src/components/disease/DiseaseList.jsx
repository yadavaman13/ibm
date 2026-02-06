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
                <h2 className="database-title">
                    Disease Database <span className="disease-count">({filteredDiseases.length} diseases)</span>
                </h2>
                
                <div className="database-controls">
                    {/* Search */}
                    <div className="search-container">
                        <Search className="search-icon" />
                        <input
                            type="text"
                            placeholder="Search diseases..."
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                            className="search-input"
                        />
                    </div>
                    
                    {/* Crop Filter */}
                    <div className="filter-container">
                        <Filter className="filter-icon" />
                        <select
                            value={selectedCrop}
                            onChange={(e) => handleCropFilter(e.target.value)}
                            className="filter-select"
                        >
                            <option value="">All Crops</option>
                            {cropOptions.map(crop => (
                                <option key={crop} value={crop}>{crop}</option>
                            ))}
                        </select>
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
                    <div className="empty-state">
                        <Search className="empty-icon" />
                        <h3 className="empty-title">
                            No diseases found
                        </h3>
                        <p className="empty-text">
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
            <h3 className="disease-card-title">{disease.name}</h3>
            
            {/* Crops Affected */}
            <div className="disease-card-section">
                <p className="disease-card-label">AFFECTS:</p>
                <div className="crops-tags">
                    {disease.crops_affected.slice(0, 3).map((crop, index) => (
                        <span key={index} className="crop-tag">{crop}</span>
                    ))}
                    {disease.crops_affected.length > 3 && (
                        <span className="crop-tag crop-tag-more">+{disease.crops_affected.length - 3} more</span>
                    )}
                </div>
            </div>
            
            {/* Symptoms Preview */}
            <div className="disease-card-section">
                <p className="disease-card-label">SYMPTOMS:</p>
                <ul className="symptoms-list">
                    {disease.symptoms.slice(0, isExpanded ? disease.symptoms.length : 2).map((symptom, index) => (
                        <li key={index} className="symptom-item">
                            <span className="symptom-bullet">•</span>
                            <span>{symptom}</span>
                        </li>
                    ))}
                </ul>
                
                {disease.symptoms.length > 2 && (
                    <button
                        onClick={() => setIsExpanded(!isExpanded)}
                        className="show-more-btn"
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