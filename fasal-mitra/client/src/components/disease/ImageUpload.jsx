import React, { useRef, useState } from 'react';
import { Upload, X, Camera } from 'lucide-react';

const ImageUpload = ({ onImageSelect, selectedImage }) => {
    const [isDragOver, setIsDragOver] = useState(false);
    const fileInputRef = useRef(null);

    const handleDragOver = (e) => {
        e.preventDefault();
        setIsDragOver(true);
    };

    const handleDragLeave = (e) => {
        e.preventDefault();
        setIsDragOver(false);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setIsDragOver(false);
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileSelect(files[0]);
        }
    };

    const handleFileSelect = (file) => {
        if (file && file.type.startsWith('image/')) {
            onImageSelect(file);
        } else {
            alert('Please select a valid image file (JPG, PNG, WEBP)');
        }
    };

    const handleInputChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            handleFileSelect(file);
        }
    };

    const handleClick = () => {
        fileInputRef.current?.click();
    };

    const handleRemoveImage = (e) => {
        e.stopPropagation();
        onImageSelect(null);
        if (fileInputRef.current) {
            fileInputRef.current.value = '';
        }
    };

    return (
        <div className="image-upload-container">
            <div
                className={`image-upload-area ${isDragOver ? 'drag-over' : ''}`}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                onClick={handleClick}
            >
                <input
                    ref={fileInputRef}
                    type="file"
                    accept="image/*"
                    onChange={handleInputChange}
                    className="hidden"
                />
                
                {selectedImage ? (
                    <div className="relative">
                        <img
                            src={URL.createObjectURL(selectedImage)}
                            alt="Selected crop"
                            className="image-preview mx-auto"
                        />
                        <button
                            onClick={handleRemoveImage}
                            className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 hover:bg-red-600 transition-colors"
                            aria-label="Remove image"
                        >
                            <X className="w-4 h-4" />
                        </button>
                        <p className="text-sm text-gray-600 mt-2">
                            {selectedImage.name}
                        </p>
                        <p className="text-xs text-gray-500">
                            Click to change image
                        </p>
                    </div>
                ) : (
                    <div className="flex flex-col items-center">
                        <Upload className="upload-icon mx-auto mb-2" />
                        <p className="text-sm font-medium text-gray-700 mb-1">
                            Click to upload or drag and drop
                        </p>
                        <p className="text-xs text-gray-500 mb-3">
                            JPG, PNG or WEBP (max. 10MB)
                        </p>
                        <div className="flex items-center gap-2 text-xs text-gray-400">
                            <Camera className="w-4 h-4" />
                            <span>Take a clear photo of affected leaves</span>
                        </div>
                    </div>
                )}
            </div>
            
            {/* Help Text */}
            <div className="tips-section">
                <p className="tips-title">
                    <Camera className="tips-icon" />
                    Tips for best results:
                </p>
                <ul className="tips-list">
                    <li>Ensure good lighting and clear focus</li>
                    <li>Show affected areas clearly</li>
                    <li>Include multiple leaves if possible</li>
                    <li>Avoid shadows and reflections</li>
                </ul>
            </div>
        </div>
    );
};

export default ImageUpload;