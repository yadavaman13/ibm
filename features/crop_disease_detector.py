"""
AI-Powered Crop Disease Detection System

Uses computer vision to identify crop diseases, assess severity, and provide treatment recommendations.
"""

import numpy as np
import pandas as pd
from datetime import datetime
import random
from PIL import Image
import io

class CropDiseaseDetector:
    """AI-powered crop disease detection and treatment recommendation system."""
    
    def __init__(self, data_loader=None):
        self.data_loader = data_loader
        
        # Disease database with comprehensive information
        self.disease_database = {
            'leaf_spot': {
                'name': 'Leaf Spot Disease',
                'crops_affected': ['Rice', 'Wheat', 'Cotton', 'Tomato', 'Potato'],
                'symptoms': ['Brown/black spots on leaves', 'Yellowing around spots', 'Premature leaf drop'],
                'causes': ['Fungal infection', 'High humidity', 'Poor air circulation'],
                'severity_indicators': {
                    'mild': 'Few scattered spots (1-5% leaf area)',
                    'moderate': 'Multiple spots covering 5-25% leaf area',
                    'severe': 'Extensive spotting >25% leaf area, leaf yellowing'
                },
                'treatments': {
                    'mild': ['Copper-based fungicide spray', 'Improve air circulation', 'Remove affected leaves'],
                    'moderate': ['Systemic fungicide (Propiconazole)', 'Weekly spraying for 3 weeks', 'Reduce irrigation frequency'],
                    'severe': ['Immediate fungicide treatment', 'Remove severely affected plants', 'Soil treatment with beneficial microbes']
                },
                'prevention': [
                    'Crop rotation with non-host crops',
                    'Proper spacing for air circulation',
                    'Avoid overhead irrigation',
                    'Regular field sanitation',
                    'Use resistant varieties'
                ],
                'cost_estimate': {'mild': 500, 'moderate': 1500, 'severe': 3000}
            },
            
            'bacterial_blight': {
                'name': 'Bacterial Blight',
                'crops_affected': ['Rice', 'Cotton', 'Beans', 'Citrus'],
                'symptoms': ['Water-soaked lesions', 'Yellow halos around spots', 'Wilting of leaves'],
                'causes': ['Bacterial infection', 'Wounds from insects/tools', 'Wet conditions'],
                'severity_indicators': {
                    'mild': 'Few lesions on lower leaves',
                    'moderate': 'Spread to middle leaves, some yellowing',
                    'severe': 'Extensive wilting, plant death possible'
                },
                'treatments': {
                    'mild': ['Copper hydroxide spray', 'Remove infected debris', 'Improve drainage'],
                    'moderate': ['Streptomycin antibiotic', 'Copper-based bactericide', 'Enhanced sanitation'],
                    'severe': ['Immediate plant removal', 'Soil sterilization', 'Quarantine affected area']
                },
                'prevention': [
                    'Use certified disease-free seeds',
                    'Sterilize tools between plants',
                    'Avoid working in wet conditions',
                    'Control insect vectors',
                    'Proper field drainage'
                ],
                'cost_estimate': {'mild': 800, 'moderate': 2000, 'severe': 4000}
            },
            
            'powdery_mildew': {
                'name': 'Powdery Mildew',
                'crops_affected': ['Wheat', 'Barley', 'Cotton', 'Grapes', 'Cucumber'],
                'symptoms': ['White powdery coating on leaves', 'Stunted growth', 'Reduced yield'],
                'causes': ['Fungal spores', 'High humidity with dry conditions', 'Poor air circulation'],
                'severity_indicators': {
                    'mild': 'Light dusting on few leaves',
                    'moderate': 'Moderate coverage on 10-30% of plant',
                    'severe': 'Heavy white coating, leaf distortion'
                },
                'treatments': {
                    'mild': ['Sulfur-based spray', 'Baking soda solution (1%)', 'Improve air flow'],
                    'moderate': ['Systemic fungicide (Myclobutanil)', 'Weekly applications', 'Remove infected leaves'],
                    'severe': ['Triazole fungicides', 'Destroy heavily infected plants', 'Soil treatment']
                },
                'prevention': [
                    'Plant resistant varieties',
                    'Ensure proper plant spacing',
                    'Avoid late evening irrigation',
                    'Regular monitoring',
                    'Balanced fertilization'
                ],
                'cost_estimate': {'mild': 400, 'moderate': 1200, 'severe': 2500}
            },
            
            'rust_disease': {
                'name': 'Rust Disease',
                'crops_affected': ['Wheat', 'Corn', 'Coffee', 'Beans'],
                'symptoms': ['Orange/brown pustules on leaves', 'Yellowing leaves', 'Reduced photosynthesis'],
                'causes': ['Rust fungi', 'Moderate temperatures', 'High moisture'],
                'severity_indicators': {
                    'mild': 'Few pustules on lower leaves',
                    'moderate': 'Pustules on middle leaves, some yellowing',
                    'severe': 'Extensive pustules, significant yellowing'
                },
                'treatments': {
                    'mild': ['Preventive fungicide spray', 'Remove infected leaves', 'Monitor spread'],
                    'moderate': ['Triazole fungicides', 'Bi-weekly applications', 'Enhanced monitoring'],
                    'severe': ['Emergency fungicide program', 'Consider replanting', 'Quarantine measures']
                },
                'prevention': [
                    'Use rust-resistant varieties',
                    'Timely planting',
                    'Proper field sanitation',
                    'Monitor weather conditions',
                    'Balanced nutrition'
                ],
                'cost_estimate': {'mild': 600, 'moderate': 1800, 'severe': 3500}
            },
            
            'viral_mosaic': {
                'name': 'Viral Mosaic',
                'crops_affected': ['Tobacco', 'Tomato', 'Cucumber', 'Pepper'],
                'symptoms': ['Mosaic pattern on leaves', 'Stunted growth', 'Malformed fruits'],
                'causes': ['Viral infection', 'Insect vectors (aphids)', 'Contaminated tools'],
                'severity_indicators': {
                    'mild': 'Light mosaic on few leaves',
                    'moderate': 'Visible mosaic, slight stunting',
                    'severe': 'Severe mosaic, significant stunting'
                },
                'treatments': {
                    'mild': ['Remove infected plants', 'Control insect vectors', 'Tool sterilization'],
                    'moderate': ['Intensive vector control', 'Quarantine affected area', 'Remove all infected plants'],
                    'severe': ['Destroy entire crop if >30% infected', 'Soil treatment', 'Extended quarantine']
                },
                'prevention': [
                    'Use virus-free seeds/seedlings',
                    'Control aphid populations',
                    'Sterilize tools between plants',
                    'Remove weed hosts',
                    'Use reflective mulches'
                ],
                'cost_estimate': {'mild': 1000, 'moderate': 2500, 'severe': 5000}
            }
        }
        
        # Nutrient deficiency symptoms (often confused with diseases)
        self.nutrient_deficiencies = {
            'nitrogen_deficiency': {
                'name': 'Nitrogen Deficiency',
                'symptoms': ['Yellowing of older leaves', 'Stunted growth', 'Poor yield'],
                'treatment': 'Apply nitrogen fertilizer (Urea 20-30 kg/acre)',
                'cost': 800
            },
            'potassium_deficiency': {
                'name': 'Potassium Deficiency', 
                'symptoms': ['Brown leaf edges', 'Weak stems', 'Poor fruit quality'],
                'treatment': 'Apply potassium fertilizer (MOP 15-20 kg/acre)',
                'cost': 600
            }
        }
    
    def aggregate_multi_photo_analysis(self, analyses):
        """Aggregate results from multiple photo analyses for better accuracy."""
        
        if len(analyses) == 1:
            return analyses[0]
        
        # Combine confidence scores (weighted average)
        total_confidence = sum(a['confidence_score'] for a in analyses) / len(analyses)
        
        # Aggregate diseases (merge and deduplicate)
        all_diseases = {}
        for analysis in analyses:
            for disease in analysis['diseases_detected']:
                disease_id = disease['disease_id']
                if disease_id in all_diseases:
                    # Average confidence for same disease
                    all_diseases[disease_id]['confidence'] = (
                        all_diseases[disease_id]['confidence'] + disease['confidence']
                    ) / 2
                    # Take highest severity
                    severity_order = {'mild': 1, 'moderate': 2, 'severe': 3}
                    current_severity = severity_order.get(all_diseases[disease_id]['severity'], 0)
                    new_severity = severity_order.get(disease['severity'], 0)
                    if new_severity > current_severity:
                        all_diseases[disease_id]['severity'] = disease['severity']
                else:
                    all_diseases[disease_id] = disease.copy()
        
        # Create aggregated analysis
        base_analysis = analyses[0].copy()
        base_analysis.update({
            'confidence_score': total_confidence,
            'diseases_detected': list(all_diseases.values()),
            'analysis_type': 'multi_photo',
            'photo_count': len(analyses),
            'image_quality': {
                'score': 'Excellent' if total_confidence > 0.8 else 'Good',
                'rating': total_confidence * 10
            }
        })
        
        return base_analysis
    
    def get_enhanced_treatment_plan(self, disease_id, severity, crop_type, location=None):
        """Get enhanced treatment plan with location-specific recommendations."""
        
        if disease_id not in self.disease_database:
            return {
                'immediate_actions': ['Consult agricultural expert', 'Monitor plant closely'],
                'treatments': ['General fungicide application'],
                'cost_estimate': 1000
            }
        
        disease_info = self.disease_database[disease_id]
        treatment_plan = {
            'immediate_actions': disease_info['treatments'].get(severity, disease_info['treatments']['mild']),
            'prevention': disease_info['prevention'],
            'cost_estimate': disease_info['cost_estimate'].get(severity, 1000)
        }
        
        # Add location-specific recommendations
        if location:
            location_lower = location.lower()
            if 'punjab' in location_lower or 'haryana' in location_lower:
                treatment_plan['regional_note'] = 'High humidity region - increase fungicide frequency'
            elif 'rajasthan' in location_lower:
                treatment_plan['regional_note'] = 'Arid region - focus on water management'
            elif 'maharashtra' in location_lower:
                treatment_plan['regional_note'] = 'Variable climate - monitor weather closely'
        
        # Add crop-specific recommendations
        if crop_type.lower() == 'rice' and 'leaf_spot' in disease_id:
            treatment_plan['crop_specific'] = [
                'Maintain 2-3 cm water level',
                'Apply silicon-based fertilizer',
                'Use certified disease-free seeds'
            ]
        elif crop_type.lower() == 'wheat' and 'rust' in disease_id:
            treatment_plan['crop_specific'] = [
                'Apply at tillering stage',
                'Use resistant varieties next season',
                'Monitor temperature closely'
            ]
        
        return treatment_plan

    def analyze_image(self, image_data, crop_type="Unknown", location="Unknown"):
        """
        Enhanced AI analysis of crop disease image with realistic simulation and image validation.
        Only analyzes images that actually contain crops/plants.
        """
        
        # Simulate image processing time
        import time
        time.sleep(1.5)
        
        # Analyze actual image properties and validate if it contains crops
        try:
            from PIL import Image
            import io
            image = Image.open(io.BytesIO(image_data))
            image_width, image_height = image.size
            
            # First, validate if this image actually contains crops/plants
            is_crop_image, validation_result = self._validate_crop_image(image)
            
            if not is_crop_image:
                # Return validation failure result instead of disease prediction
                return {
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'crop_type': crop_type,
                    'location': location,
                    'image_validation': validation_result,
                    'is_valid_crop_image': False,
                    'validation_message': validation_result['message'],
                    'suggestions': validation_result['suggestions']
                }
            
            # Calculate image quality based on size and format
            image_quality = self._assess_realistic_image_quality(image)
            
            # More sophisticated disease detection based on image properties
            detected_diseases = self._advanced_disease_simulation(crop_type, image_quality, location)
            
        except Exception as e:
            # Return error for invalid image files
            return {
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'crop_type': crop_type,
                'location': location,
                'is_valid_crop_image': False,
                'validation_message': "Invalid image file or format not supported",
                'suggestions': ["Please upload a clear image in JPG, PNG, or JPEG format", "Ensure the image file is not corrupted"]
            }
        
        # Generate comprehensive analysis report with enhanced data
        analysis_report = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'crop_type': crop_type,
            'location': location,
            'image_quality': image_quality,
            'image_validation': validation_result,
            'is_valid_crop_image': True,
            'diseases_detected': detected_diseases,
            'confidence_score': self._calculate_overall_confidence(detected_diseases, image_quality),
            'environmental_factors': self._assess_environmental_risk(crop_type, location),
            'urgency_level': self._calculate_urgency(detected_diseases),
            'analysis_method': 'Enhanced AI Simulation with Image Validation',
            'recommendations': self._generate_general_recommendations(crop_type, detected_diseases)
        }
        
        return analysis_report
    
    def _validate_crop_image(self, image):
        """
        Ultra-robust validation to ensure only genuine crop/plant images are analyzed.
        Uses multiple strict validation layers with weighted scoring.
        Returns (is_valid, validation_details)
        """
        import numpy as np
        
        # Convert PIL image to RGB array for analysis
        img_array = np.array(image.convert('RGB'))
        height, width, channels = img_array.shape
        
        # Initialize validation system with strict scoring
        validation_scores = {
            'green_content': 0,
            'organic_shapes': 0, 
            'natural_texture': 0,
            'color_diversity': 0,
            'edge_patterns': 0,
            'plant_structure': 0,
            'background_analysis': 0,
            'artificial_patterns': 0
        }
        
        validation_details = []
        rejection_flags = []
        
        # === STRICT VALIDATION CHECKS ===
        
        # 1. ENHANCED GREEN CONTENT ANALYSIS (HSV-based)
        green_score, green_details = self._advanced_green_analysis(img_array)
        validation_scores['green_content'] = green_score
        validation_details.extend(green_details)
        
        # 2. PLANT STRUCTURE DETECTION
        structure_score, structure_details = self._detect_plant_structures(img_array)
        validation_scores['plant_structure'] = structure_score
        validation_details.extend(structure_details)
        
        # 3. ARTIFICIAL PATTERN REJECTION
        artificial_score, artificial_details = self._detect_artificial_patterns(img_array)
        validation_scores['artificial_patterns'] = artificial_score
        validation_details.extend(artificial_details)
        if artificial_score < -2:  # Strong artificial indicators
            rejection_flags.append("Strong artificial/synthetic patterns detected")
        
        # 4. BACKGROUND ANALYSIS
        bg_score, bg_details = self._analyze_background_type(img_array)
        validation_scores['background_analysis'] = bg_score
        validation_details.extend(bg_details)
        
        # 5. ENHANCED ORGANIC SHAPE ANALYSIS
        organic_score, organic_details = self._advanced_organic_analysis(img_array)
        validation_scores['organic_shapes'] = organic_score
        validation_details.extend(organic_details)
        
        # 6. SOPHISTICATED TEXTURE ANALYSIS
        texture_score, texture_details = self._advanced_texture_analysis(img_array)
        validation_scores['natural_texture'] = texture_score
        validation_details.extend(texture_details)
        
        # 7. ENHANCED COLOR DIVERSITY
        color_score, color_details = self._advanced_color_analysis(img_array)
        validation_scores['color_diversity'] = color_score
        validation_details.extend(color_details)
        
        # 8. ADVANCED EDGE PATTERN ANALYSIS
        edge_score, edge_details = self._advanced_edge_analysis(img_array)
        validation_scores['edge_patterns'] = edge_score
        validation_details.extend(edge_details)
        
        # === WEIGHTED SCORING SYSTEM ===
        weights = {
            'green_content': 0.25,      # Most important - plants are green
            'plant_structure': 0.20,    # Second most important
            'artificial_patterns': 0.15, # Strong rejection indicator
            'organic_shapes': 0.15,     # Natural vs artificial shapes
            'natural_texture': 0.10,    # Texture analysis
            'background_analysis': 0.10, # Background type
            'color_diversity': 0.03,    # Color variation
            'edge_patterns': 0.02       # Edge characteristics
        }
        
        # Calculate weighted final score
        final_score = sum(validation_scores[key] * weights[key] for key in weights.keys())
        
        # === STRICT DECISION LOGIC ===
        
        # Immediate rejection conditions
        if rejection_flags:
            return False, {
                'is_valid': False,
                'confidence': 0.95,
                'final_score': final_score,
                'details': validation_details,
                'rejection_reasons': rejection_flags,
                'detected_content': self._classify_non_crop_image_advanced(img_array, validation_scores),
                'message': f"❌ Image rejected: {'; '.join(rejection_flags)}",
                'suggestions': [
                    "📸 Upload a photo of real crops, plants, or agricultural fields",
                    "🌿 Ensure the image shows natural plant matter (leaves, stems, flowers)",
                    "☀️ Use natural lighting and avoid processed/filtered images",
                    "🔍 Get close enough to show plant details clearly",
                    "🚫 Avoid uploading icons, logos, graphics, or non-plant objects"
                ]
            }
        
        # Strict thresholds - require multiple strong positive indicators
        min_score_required = 0.6  # Increased from previous threshold
        min_green_required = 0.3  # Must have substantial green content
        min_plant_structure = 0.2  # Must show some plant-like structures
        
        is_valid = (
            final_score >= min_score_required and
            validation_scores['green_content'] >= min_green_required and
            validation_scores['plant_structure'] >= min_plant_structure and
            validation_scores['artificial_patterns'] >= -1  # Not too artificial
        )
        
        if is_valid:
            validation_result = {
                'is_valid': True,
                'confidence': min(0.95, 0.7 + (final_score * 0.3)),
                'final_score': round(final_score, 2),
                'individual_scores': validation_scores,
                'details': validation_details,
                'message': "✅ Valid crop/plant image detected - suitable for disease analysis"
            }
        else:
            # Provide specific reasons for rejection
            failure_reasons = []
            if final_score < min_score_required:
                failure_reasons.append(f"Overall plant-likeness score too low ({final_score:.2f} < {min_score_required})")
            if validation_scores['green_content'] < min_green_required:
                failure_reasons.append(f"Insufficient plant-like green content ({validation_scores['green_content']:.2f})")
            if validation_scores['plant_structure'] < min_plant_structure:
                failure_reasons.append("No clear plant structures detected")
                
            validation_result = {
                'is_valid': False,
                'confidence': 0.90,
                'final_score': round(final_score, 2),
                'individual_scores': validation_scores,
                'details': validation_details,
                'failure_reasons': failure_reasons,
                'detected_content': self._classify_non_crop_image_advanced(img_array, validation_scores),
                'message': f"❌ Not a valid crop image - {'; '.join(failure_reasons)}",
                'suggestions': [
                    "📱 Take a clear photo of actual crop plants or leaves",
                    "🌾 Ensure substantial green plant matter is visible",
                    "🔍 Focus on areas showing plant structures (leaves, stems, branches)",
                    "☀️ Use good natural lighting conditions",
                    "❌ Avoid icons, graphics, logos, or heavily processed images"
                ]
            }
        
        return is_valid, validation_result
    
    def _advanced_green_analysis(self, img_array):
        """Advanced green content analysis using HSV color space for better plant detection."""
        try:
            # Convert RGB to HSV for better color analysis
            rgb_normalized = img_array.astype(float) / 255.0
            
            # Manual RGB to HSV conversion (simplified)
            r, g, b = rgb_normalized[:,:,0], rgb_normalized[:,:,1], rgb_normalized[:,:,2]
            
            # Green detection in multiple ways
            # 1. Simple green dominance
            green_dominant = (g > r) & (g > b) & (g > 0.25)
            
            # 2. Plant-like green colors (HSV approximation)
            # Plants typically have hue 60-180 degrees (green-yellow to blue-green)
            max_rgb = np.maximum(np.maximum(r, g), b)
            min_rgb = np.minimum(np.minimum(r, g), b)
            delta = max_rgb - min_rgb
            
            # Avoid division by zero
            safe_delta = np.where(delta == 0, 1, delta)
            
            # Simplified hue calculation for green detection
            hue_green_like = np.where(
                (max_rgb == g) & (delta > 0.1),  # Green is dominant with sufficient saturation
                True,
                False
            )
            
            # 3. Vegetation indices (simplified NDVI-like)
            # Plants reflect more in near-infrared, but we approximate with green vs red
            vegetation_index = (g - r) / np.maximum(g + r, 0.01)
            high_vegetation = vegetation_index > 0.1
            
            # Combine all green indicators
            plant_green_pixels = green_dominant | hue_green_like | high_vegetation
            green_percentage = np.sum(plant_green_pixels) / plant_green_pixels.size
            
            # Score based on green content percentage
            if green_percentage > 0.4:  # >40% plant-like pixels
                score = 3.0
                detail = f"✅ Excellent plant green content ({green_percentage:.1%})"
            elif green_percentage > 0.25:  # >25% plant-like pixels
                score = 2.0
                detail = f"✅ Good plant green content ({green_percentage:.1%})"
            elif green_percentage > 0.15:  # >15% plant-like pixels
                score = 1.0
                detail = f"⚠️ Moderate green content ({green_percentage:.1%})"
            elif green_percentage > 0.05:  # >5% plant-like pixels
                score = 0.5
                detail = f"⚠️ Low green content ({green_percentage:.1%})"
            else:
                score = 0.0
                detail = f"❌ Very low/no plant green content ({green_percentage:.1%})"
                
            return score, [detail]
            
        except Exception:
            return 0.5, ["⚠️ Green analysis failed - using default"]
    
    def _detect_plant_structures(self, img_array):
        """Detect plant-like structures: leaves, stems, branches, veins."""
        try:
            # Convert to grayscale for structural analysis
            gray = np.mean(img_array, axis=2).astype(np.uint8)
            
            # Detect linear structures (stems/branches)
            linear_score = self._detect_linear_structures(gray)
            
            # Detect leaf-like shapes (oval/elongated structures)
            leaf_score = self._detect_leaf_shapes(gray)
            
            # Detect vein-like patterns
            vein_score = self._detect_vein_patterns(gray)
            
            # Detect clustered organic structures
            cluster_score = self._detect_organic_clusters(gray)
            
            total_structure_score = (linear_score + leaf_score + vein_score + cluster_score) / 4
            
            details = []
            if linear_score > 0.3:
                details.append("✅ Linear plant structures detected (stems/branches)")
            if leaf_score > 0.3:
                details.append("✅ Leaf-like shapes identified")
            if vein_score > 0.3:
                details.append("✅ Vein-like patterns found")
            if cluster_score > 0.3:
                details.append("✅ Organic clustering patterns detected")
            
            if total_structure_score < 0.1:
                details.append("❌ No clear plant structures identified")
            elif total_structure_score < 0.3:
                details.append("⚠️ Weak plant structural indicators")
                
            return total_structure_score * 3, details  # Scale up for scoring
            
        except Exception:
            return 0.0, ["❌ Plant structure analysis failed"]
    
    def _detect_artificial_patterns(self, img_array):
        """Detect artificial patterns that indicate non-plant images."""
        try:
            artificial_indicators = 0
            details = []
            
            # 1. Check for solid color blocks (logos/icons)
            solid_blocks = self._detect_solid_blocks(img_array)
            if solid_blocks > 0.3:
                artificial_indicators += 2
                details.append("❌ Solid color blocks detected (logo/icon pattern)")
            
            # 2. Check for perfect geometric shapes
            geometric_shapes = self._detect_geometric_shapes(img_array)
            if geometric_shapes > 0.4:
                artificial_indicators += 2
                details.append("❌ Perfect geometric shapes detected")
            
            # 3. Check for limited color palette (graphics)
            color_palette_size = self._estimate_color_palette(img_array)
            if color_palette_size < 50:  # Very limited colors
                artificial_indicators += 1
                details.append("❌ Very limited color palette (graphic/icon)")
            
            # 4. Check for artificial edges (perfect lines)
            artificial_edges = self._detect_artificial_edges(img_array)
            if artificial_edges > 0.5:
                artificial_indicators += 1
                details.append("❌ Artificial/perfect edge patterns")
            
            # 5. Check for text/symbols
            text_patterns = self._detect_text_patterns(img_array)
            if text_patterns > 0.3:
                artificial_indicators += 2
                details.append("❌ Text or symbol patterns detected")
            
            # Return negative score for artificial patterns (penalty)
            return -artificial_indicators, details
            
        except Exception:
            return 0, ["⚠️ Artificial pattern analysis failed"]
    
    def _detect_solid_blocks(self, img_array):
        """Detect large solid color areas typical of logos/icons."""
        # Calculate local color variance
        height, width = img_array.shape[:2]
        block_size = min(20, height//10, width//10)
        
        if block_size < 5:
            return 0
        
        solid_area = 0
        total_area = 0
        
        for i in range(0, height - block_size, block_size):
            for j in range(0, width - block_size, block_size):
                block = img_array[i:i+block_size, j:j+block_size]
                variance = np.var(block)
                
                if variance < 50:  # Very low variance = solid color
                    solid_area += block_size * block_size
                total_area += block_size * block_size
        
        return solid_area / max(total_area, 1)
    
    def _detect_geometric_shapes(self, img_array):
        """Detect perfect circles, rectangles, triangles."""
        # Simplified geometric shape detection
        gray = np.mean(img_array, axis=2).astype(np.uint8)
        
        # Edge detection (simplified)
        edges_x = np.abs(np.diff(gray, axis=1))
        edges_y = np.abs(np.diff(gray, axis=0))
        
        # Count perfect horizontal/vertical lines
        horizontal_lines = np.sum(np.max(edges_x, axis=1) > 50)
        vertical_lines = np.sum(np.max(edges_y, axis=0) > 50)
        
        total_lines = horizontal_lines + vertical_lines
        image_perimeter = 2 * (gray.shape[0] + gray.shape[1])
        
        return min(1.0, total_lines / max(image_perimeter * 0.1, 1))
    
    def _estimate_color_palette(self, img_array):
        """Estimate the number of distinct colors in the image."""
        # Reduce precision to count meaningful color differences
        reduced = img_array // 8  # Reduce to 32 levels per channel
        reshaped = reduced.reshape(-1, 3)
        
        # Count unique colors
        unique_colors = np.unique(reshaped, axis=0)
        return len(unique_colors)
    
    def _detect_artificial_edges(self, img_array):
        """Detect perfectly straight edges typical of graphics."""
        gray = np.mean(img_array, axis=2).astype(np.uint8)
        
        # Simple edge detection
        edges_x = np.abs(np.diff(gray, axis=1))
        edges_y = np.abs(np.diff(gray, axis=0))
        
        # Count very strong edges (artificial)
        strong_edges = np.sum(edges_x > 100) + np.sum(edges_y > 100)
        total_pixels = gray.size
        
        return min(1.0, strong_edges / (total_pixels * 0.05))
    
    def _detect_text_patterns(self, img_array):
        """Detect text-like patterns in the image."""
        # Simplified text detection based on edge patterns
        gray = np.mean(img_array, axis=2).astype(np.uint8)
        
        # Text typically has high horizontal edge density
        edges_x = np.abs(np.diff(gray, axis=1))
        
        # Look for rows with many edge transitions (text lines)
        row_edges = np.sum(edges_x > 30, axis=1)
        text_like_rows = np.sum(row_edges > len(edges_x[0]) * 0.2)
        
        return min(1.0, text_like_rows / max(gray.shape[0] * 0.3, 1))
    
    def _detect_linear_structures(self, gray):
        """Detect linear structures like plant stems."""
        edges = np.abs(np.diff(gray, axis=0)) + np.abs(np.diff(gray.T, axis=0)).T
        linear_strength = np.mean(edges > 20)
        return min(1.0, linear_strength * 2)
    
    def _detect_leaf_shapes(self, gray):
        """Detect oval/leaf-like shapes."""
        # Simplified leaf detection based on edge curvature
        edges_x = np.abs(np.diff(gray, axis=1))
        edges_y = np.abs(np.diff(gray, axis=0))
        
        curved_edges = np.sum((edges_x > 15) & (edges_x < 80)) + np.sum((edges_y > 15) & (edges_y < 80))
        total_edges = np.sum(edges_x > 10) + np.sum(edges_y > 10)
        
        if total_edges == 0:
            return 0
        return min(1.0, curved_edges / total_edges)
    
    def _detect_vein_patterns(self, gray):
        """Detect vein-like patterns in leaves."""
        # Look for thin linear structures
        fine_edges = np.abs(np.diff(gray, axis=1))
        vein_like = np.sum((fine_edges > 10) & (fine_edges < 40))
        return min(1.0, vein_like / (gray.size * 0.1))
    
    def _detect_organic_clusters(self, gray):
        """Detect organic clustering patterns."""
        # Simple clustering based on local variance
        local_variance = np.var(gray)
        normalized_variance = min(1.0, local_variance / 1000)
        return normalized_variance
    
    def _analyze_background_type(self, img_array):
        """Analyze if background is natural (soil/sky) vs artificial (white/solid)."""
        try:
            # Sample border pixels to analyze background
            border_pixels = np.concatenate([
                img_array[0, :].flatten(),    # top
                img_array[-1, :].flatten(),   # bottom  
                img_array[:, 0].flatten(),    # left
                img_array[:, -1].flatten()    # right
            ])
            
            # Reshape for analysis
            border_colors = border_pixels.reshape(-1, 3)
            
            # Check for artificial backgrounds
            mean_border = np.mean(border_colors, axis=0)
            std_border = np.std(border_colors, axis=0)
            
            details = []
            score = 0
            
            # Natural soil colors (browns/earth tones)
            if np.mean(mean_border) < 150 and std_border.max() > 20:
                score += 1
                details.append("✅ Natural background detected (soil/earth)")
            
            # Sky/vegetation background
            elif mean_border[2] > mean_border[0] and mean_border[1] > mean_border[0]:  # Blue or green tint
                score += 1
                details.append("✅ Natural background (sky/vegetation)")
            
            # Pure white/artificial background
            elif np.all(mean_border > 240):
                score -= 1
                details.append("❌ Artificial white background")
            
            # Solid color background
            elif np.all(std_border < 10):
                score -= 1
                details.append("❌ Solid color background (artificial)")
            else:
                details.append("⚠️ Background analysis inconclusive")
            
            return score, details
            
        except Exception:
            return 0, ["⚠️ Background analysis failed"]
    
    def _advanced_organic_analysis(self, img_array):
        """Advanced organic shape analysis with multiple methods."""
        try:
            gray = np.mean(img_array, axis=2).astype(np.uint8)
            
            # Multiple organic indicators
            scores = []
            details = []
            
            # 1. Edge complexity (organic shapes have complex edges)
            edge_complexity = self._calculate_edge_complexity(gray)
            if edge_complexity > 0.6:
                scores.append(1.0)
                details.append("✅ Complex organic edge patterns")
            elif edge_complexity > 0.4:
                scores.append(0.5)
                details.append("⚠️ Moderate edge complexity")
            else:
                scores.append(0.0)
                details.append("❌ Simple geometric edges")
            
            # 2. Shape irregularity
            irregularity = self._calculate_shape_irregularity(gray)
            if irregularity > 0.5:
                scores.append(1.0)
                details.append("✅ High shape irregularity (organic)")
            else:
                scores.append(0.0)
                details.append("❌ Regular geometric shapes")
            
            return np.mean(scores) * 2, details  # Scale for scoring system
            
        except Exception:
            return 0, ["❌ Organic analysis failed"]
    
    def _calculate_edge_complexity(self, gray):
        """Calculate edge complexity for organic vs geometric distinction."""
        edges = np.abs(np.diff(gray, axis=1)) + np.abs(np.diff(gray.T, axis=1)).T
        strong_edges = edges > 30
        
        if np.sum(strong_edges) == 0:
            return 0
        
        # Measure edge direction changes (complexity)
        edge_changes = np.sum(np.abs(np.diff(strong_edges.astype(int), axis=0))) + \
                      np.sum(np.abs(np.diff(strong_edges.astype(int), axis=1)))
        
        return min(1.0, edge_changes / (gray.size * 0.1))
    
    def _calculate_shape_irregularity(self, gray):
        """Calculate shape irregularity."""
        # Simple approximation of shape irregularity
        edges = np.abs(np.diff(gray, axis=1)) + np.abs(np.diff(gray.T, axis=1)).T
        edge_variance = np.var(edges)
        return min(1.0, edge_variance / 2000)
    
    def _advanced_texture_analysis(self, img_array):
        """Advanced texture analysis for natural vs artificial surfaces."""
        try:
            gray = np.mean(img_array, axis=2).astype(np.uint8)
            
            # Calculate multiple texture measures
            local_variance = self._calculate_local_variance(gray)
            texture_uniformity = self._calculate_texture_uniformity(gray)
            
            score = 0
            details = []
            
            if local_variance > 0.3 and texture_uniformity < 0.7:
                score = 2.0
                details.append("✅ Natural texture patterns detected")
            elif local_variance > 0.15:
                score = 1.0  
                details.append("⚠️ Moderate texture variation")
            else:
                score = 0.0
                details.append("❌ Smooth/artificial texture")
            
            return score, details
            
        except Exception:
            return 0, ["❌ Texture analysis failed"]
    
    def _calculate_local_variance(self, gray):
        """Calculate local variance for texture measurement."""
        if gray.size < 100:
            return 0
        
        kernel_size = min(9, gray.shape[0]//5, gray.shape[1]//5)
        if kernel_size < 3:
            return 0
        
        variances = []
        step = max(1, kernel_size//2)
        
        for i in range(0, gray.shape[0] - kernel_size, step):
            for j in range(0, gray.shape[1] - kernel_size, step):
                patch = gray[i:i+kernel_size, j:j+kernel_size]
                variances.append(np.var(patch))
        
        return np.mean(variances) / 255.0 if variances else 0
    
    def _calculate_texture_uniformity(self, gray):
        """Calculate texture uniformity."""
        hist = np.histogram(gray, bins=32)[0]
        hist = hist / np.sum(hist)
        entropy = -np.sum(hist * np.log2(hist + 1e-10))
        return entropy / 5.0  # Normalize
    
    def _advanced_color_analysis(self, img_array):
        """Advanced color analysis for natural vs artificial images."""
        try:
            # Analyze color distribution
            colors_per_channel = []
            for channel in range(3):
                hist = np.histogram(img_array[:,:,channel], bins=64)[0]
                colors_per_channel.append(np.sum(hist > 0))
            
            avg_colors = np.mean(colors_per_channel)
            
            score = 0
            details = []
            
            if avg_colors > 40:
                score = 1.0
                details.append("✅ Rich color diversity")
            elif avg_colors > 20:
                score = 0.5
                details.append("⚠️ Moderate color range")
            else:
                score = 0.0
                details.append("❌ Limited color palette")
            
            return score, details
            
        except Exception:
            return 0, ["❌ Color analysis failed"]
    
    def _advanced_edge_analysis(self, img_array):
        """Advanced edge pattern analysis."""
        try:
            gray = np.mean(img_array, axis=2).astype(np.uint8)
            
            edges_x = np.abs(np.diff(gray, axis=1))
            edges_y = np.abs(np.diff(gray, axis=0))
            
            # Natural edges are typically moderate strength
            natural_edges = np.sum((edges_x > 10) & (edges_x < 60)) + np.sum((edges_y > 10) & (edges_y < 60))
            artificial_edges = np.sum(edges_x > 100) + np.sum(edges_y > 100)
            
            if natural_edges > artificial_edges * 2:
                return 1.0, ["✅ Natural edge patterns"]
            else:
                return 0.0, ["❌ Artificial/sharp edges"]
                
        except Exception:
            return 0, ["❌ Edge analysis failed"]
    
    def _classify_non_crop_image_advanced(self, img_array, scores):
        """Advanced classification of non-crop image types."""
        
        if scores.get('artificial_patterns', 0) < -1:
            if img_array.shape[0] < 200 and img_array.shape[1] < 200:
                return "a small icon or symbol"
            elif scores.get('color_diversity', 0) < 0.3:
                return "a logo or graphic design"
            else:
                return "an artificial graphic or illustration"
        
        elif scores.get('green_content', 0) < 0.1:
            if np.mean(img_array) > 200:
                return "a bright/white background image"
            elif np.mean(img_array) < 50:
                return "a dark/black image"
            else:
                return "a non-plant object or scene"
        
        elif scores.get('plant_structure', 0) < 0.1:
            return "a natural scene without clear plant structures"
        
        else:
            return "an image that doesn't clearly show crop plants"

    def _assess_realistic_image_quality(self, image):
        """Assess image quality based on actual image properties."""
        width, height = image.size
        total_pixels = width * height
        
        # Quality assessment based on resolution
        if total_pixels > 2000000:  # 2MP+
            quality_score = "Excellent"
            rating = random.uniform(8.5, 10.0)
        elif total_pixels > 1000000:  # 1MP+
            quality_score = "Good"
            rating = random.uniform(7.0, 8.5)
        elif total_pixels > 500000:  # 0.5MP+
            quality_score = "Fair"
            rating = random.uniform(5.5, 7.0)
        else:
            quality_score = "Poor"
            rating = random.uniform(3.0, 5.5)
        
        # Check if image is too small or too large
        quality_notes = []
        if width < 300 or height < 300:
            quality_notes.append("Image resolution is low")
            rating *= 0.8
        if total_pixels > 5000000:
            quality_notes.append("High resolution - excellent for analysis")
            rating = min(rating * 1.1, 10.0)
        
        return {
            'score': quality_score,
            'rating': round(rating, 1),
            'resolution': f"{width}x{height}",
            'megapixels': round(total_pixels / 1000000, 1),
            'notes': quality_notes
        }
    
    def _advanced_disease_simulation(self, crop_type, image_quality, location):
        """Advanced disease simulation based on multiple factors."""
        
        # Base disease mapping
        crop_disease_mapping = {
            'Rice': [
                ('leaf_spot', 'Brown Leaf Spot', 0.25),
                ('bacterial_blight', 'Bacterial Leaf Blight', 0.20),
                ('blast_disease', 'Rice Blast', 0.15),
                ('sheath_rot', 'Sheath Rot', 0.10)
            ],
            'Wheat': [
                ('rust_disease', 'Yellow Rust', 0.30),
                ('powdery_mildew', 'Powdery Mildew', 0.25),
                ('leaf_spot', 'Leaf Spot', 0.20),
                ('fusarium_head', 'Fusarium Head Blight', 0.15)
            ],
            'Cotton': [
                ('bacterial_blight', 'Bacterial Blight', 0.25),
                ('leaf_spot', 'Leaf Spot', 0.20),
                ('verticillium_wilt', 'Verticillium Wilt', 0.18),
                ('bollworm', 'Bollworm Damage', 0.15)
            ],
            'Tomato': [
                ('late_blight', 'Late Blight', 0.30),
                ('early_blight', 'Early Blight', 0.25),
                ('leaf_spot', 'Septoria Leaf Spot', 0.20),
                ('viral_mosaic', 'Mosaic Virus', 0.15)
            ],
            'Potato': [
                ('late_blight', 'Late Blight', 0.35),
                ('early_blight', 'Early Blight', 0.25),
                ('scab', 'Common Scab', 0.15),
                ('black_scurf', 'Black Scurf', 0.10)
            ],
            'Corn': [
                ('corn_rust', 'Common Rust', 0.30),
                ('leaf_blight', 'Northern Corn Leaf Blight', 0.25),
                ('gray_leaf_spot', 'Gray Leaf Spot', 0.20),
                ('smut', 'Common Smut', 0.10)
            ]
        }
        
        # Get diseases for crop type
        possible_diseases = crop_disease_mapping.get(crop_type, [
            ('leaf_spot', 'General Leaf Spot', 0.30),
            ('fungal_infection', 'Fungal Infection', 0.25),
            ('bacterial_disease', 'Bacterial Disease', 0.20)
        ])
        
        # Adjust probabilities based on image quality
        quality_multiplier = 1.0
        if image_quality['rating'] < 5.0:
            quality_multiplier = 0.7  # Lower quality = less confident detection
        elif image_quality['rating'] > 8.5:
            quality_multiplier = 1.2  # Higher quality = better detection
        
        # Location-based risk factors
        location_risk = 1.0
        if location and location.lower() != 'unknown':
            location_lower = location.lower()
            if any(state in location_lower for state in ['punjab', 'haryana', 'west bengal']):
                location_risk = 1.3  # High humidity regions
            elif any(state in location_lower for state in ['rajasthan', 'gujarat']):
                location_risk = 0.8  # Arid regions
        
        # Simulate detection
        healthy_chance = random.uniform(0.15, 0.35)  # 15-35% chance of healthy plant
        
        if random.random() < healthy_chance:
            return [{
                'disease_id': 'healthy',
                'name': 'Healthy Plant',
                'severity': 'none',
                'confidence': round(random.uniform(0.85, 0.95), 2),
                'description': 'No disease symptoms detected. Plant appears healthy.',
                'risk_level': 'None',
                'treatment_cost': 0
            }]
        
        # Select diseases based on weighted probabilities
        detected = []
        num_diseases = random.choices([1, 2], weights=[75, 25])[0]  # Mostly 1 disease
        
        # Sort by probability and select top diseases
        sorted_diseases = sorted(possible_diseases, key=lambda x: x[2], reverse=True)
        
        for i in range(min(num_diseases, len(sorted_diseases))):
            disease_id, disease_name, base_prob = sorted_diseases[i]
            
            # Adjust probability
            final_prob = base_prob * quality_multiplier * location_risk
            
            if random.random() < final_prob:
                severity_options = ['mild', 'moderate', 'severe']
                severity_weights = [50, 35, 15]  # Most diseases are mild to moderate
                severity = random.choices(severity_options, weights=severity_weights)[0]
                
                confidence = round(random.uniform(0.75, 0.92) * quality_multiplier, 2)
                confidence = min(confidence, 0.95)  # Cap at 95%
                
                detected.append({
                    'disease_id': disease_id,
                    'name': disease_name,
                    'severity': severity,
                    'confidence': confidence,
                    'description': self._get_disease_description(disease_id, severity),
                    'risk_level': self._calculate_risk_level(severity, crop_type),
                    'treatment_cost': self._estimate_treatment_cost(disease_id, severity),
                    'affected_area': f"{random.randint(5, 40)}% of visible area"
                })
        
        return detected if detected else [{
            'disease_id': 'healthy',
            'name': 'Healthy Plant',
            'severity': 'none',
            'confidence': 0.88,
            'description': 'No clear disease symptoms visible.',
            'risk_level': 'None',
            'treatment_cost': 0
        }]
    
    def _get_disease_description(self, disease_id, severity):
        """Get detailed description of the disease."""
        descriptions = {
            'leaf_spot': {
                'mild': 'Small brown spots visible on few leaves',
                'moderate': 'Multiple brown spots with yellow halos on several leaves',
                'severe': 'Extensive spotting with leaf yellowing and drop'
            },
            'bacterial_blight': {
                'mild': 'Water-soaked lesions on leaf edges',
                'moderate': 'Expanding lesions with bacterial ooze',
                'severe': 'Widespread leaf necrosis and plant wilting'
            },
            'rust_disease': {
                'mild': 'Small orange pustules on leaf surface',
                'moderate': 'Numerous rust pustules covering leaves',
                'severe': 'Severe rust infection causing leaf death'
            }
        }
        
        return descriptions.get(disease_id, {}).get(severity, 'Disease symptoms detected on plant')
    
    def _calculate_risk_level(self, severity, crop_type):
        """Calculate risk level based on severity and crop type."""
        if severity == 'severe':
            return 'High'
        elif severity == 'moderate':
            return 'Medium'
        else:
            return 'Low'
    
    def _estimate_treatment_cost(self, disease_id, severity):
        """Estimate treatment cost based on disease and severity."""
        base_costs = {
            'leaf_spot': 800,
            'bacterial_blight': 1200,
            'rust_disease': 1000,
            'powdery_mildew': 600,
            'late_blight': 1500,
            'early_blight': 900
        }
        
        base_cost = base_costs.get(disease_id, 800)
        
        severity_multipliers = {
            'mild': 0.8,
            'moderate': 1.0,
            'severe': 1.5
        }
        
        return int(base_cost * severity_multipliers.get(severity, 1.0))
    
    def _calculate_overall_confidence(self, diseases, image_quality):
        """Calculate overall analysis confidence."""
        if not diseases or diseases[0]['disease_id'] == 'healthy':
            base_confidence = 0.88
        else:
            avg_disease_confidence = sum(d['confidence'] for d in diseases) / len(diseases)
            base_confidence = avg_disease_confidence
        
        # Adjust based on image quality
        quality_factor = min(image_quality['rating'] / 10.0, 1.0)
        final_confidence = base_confidence * (0.7 + 0.3 * quality_factor)
        
        return round(min(final_confidence, 0.95), 2)
    
    def _generate_general_recommendations(self, crop_type, diseases):
        """Generate general recommendations based on analysis."""
        recommendations = []
        
        if diseases[0]['disease_id'] == 'healthy':
            recommendations = [
                'Continue regular monitoring',
                'Maintain proper irrigation schedule',
                'Ensure adequate nutrition',
                'Practice good field hygiene'
            ]
        else:
            severe_count = sum(1 for d in diseases if d['severity'] == 'severe')
            if severe_count > 0:
                recommendations.append('Immediate action required - treat within 24 hours')
            
            recommendations.extend([
                'Monitor weather conditions closely',
                'Consider preventive treatments for healthy plants',
                'Document disease progression with photos',
                'Consult local agricultural extension officer'
            ])
        
        return recommendations

    def _simulate_disease_detection(self, crop_type):
        """Simulate realistic disease detection based on crop type and season."""
        
        # Common diseases by crop type
        crop_disease_mapping = {
            'Rice': ['leaf_spot', 'bacterial_blight'],
            'Wheat': ['rust_disease', 'powdery_mildew', 'leaf_spot'],
            'Cotton': ['bacterial_blight', 'leaf_spot'],
            'Tomato': ['leaf_spot', 'bacterial_blight', 'viral_mosaic'],
            'Potato': ['leaf_spot'],
            'Corn': ['rust_disease'],
            'Unknown': ['leaf_spot', 'powdery_mildew']
        }
        
        possible_diseases = crop_disease_mapping.get(crop_type, crop_disease_mapping['Unknown'])
        
        # Randomly select 1-2 diseases (simulate real detection)
        num_diseases = random.choices([0, 1, 2], weights=[10, 70, 20])[0]
        
        if num_diseases == 0:
            return [{'disease_id': 'healthy', 'name': 'No Disease Detected', 'severity': 'none', 'confidence': 0.9}]
        
        detected = []
        selected_diseases = random.sample(possible_diseases, min(num_diseases, len(possible_diseases)))
        
        for disease_id in selected_diseases:
            if disease_id in self.disease_database:
                severity = random.choices(['mild', 'moderate', 'severe'], weights=[50, 35, 15])[0]
                detected.append({
                    'disease_id': disease_id,
                    'name': self.disease_database[disease_id]['name'],
                    'severity': severity,
                    'confidence': round(random.uniform(0.7, 0.95), 2)
                })
        
        return detected
    
    def _assess_image_quality(self):
        """Assess the quality of the uploaded image."""
        quality_scores = ['Excellent', 'Good', 'Fair', 'Poor']
        quality = random.choices(quality_scores, weights=[20, 50, 25, 5])[0]
        
        quality_feedback = {
            'Excellent': 'Perfect lighting and focus for accurate analysis',
            'Good': 'Good image quality, analysis highly reliable', 
            'Fair': 'Acceptable quality, consider retaking in better light',
            'Poor': 'Poor image quality may affect accuracy - please retake'
        }
        
        return {
            'score': quality,
            'feedback': quality_feedback[quality]
        }
    
    def _assess_environmental_risk(self, crop_type, location="Unknown"):
        """Assess environmental factors affecting disease risk based on crop type and location."""
        current_month = datetime.now().month
        
        # Base seasonal risk factors
        risk_factors = []
        
        if current_month in [6, 7, 8, 9]:  # Monsoon season
            base_season = 'Monsoon'
            risk_factors.extend(['High humidity', 'Excessive moisture', 'Poor drainage'])
        elif current_month in [10, 11, 12, 1]:  # Post-monsoon/winter
            base_season = 'Winter'
            risk_factors.extend(['Temperature fluctuation', 'Dew formation'])
        else:  # Summer
            base_season = 'Summer'
            risk_factors.extend(['Heat stress', 'Drought conditions'])
        
        # Add location-specific risk factors
        if location and location.lower() != 'unknown':
            location_lower = location.lower()
            
            # High humidity regions
            if any(state in location_lower for state in ['punjab', 'haryana', 'west bengal', 'kerala', 'assam']):
                risk_factors.extend(['High regional humidity', 'Disease-favorable climate'])
                risk_level_weight = 1.2
            
            # Arid/semi-arid regions  
            elif any(state in location_lower for state in ['rajasthan', 'gujarat', 'maharashtra']):
                risk_factors.extend(['Water stress', 'Heat damage risk'])
                risk_level_weight = 0.8
                
            # Coastal regions
            elif any(state in location_lower for state in ['goa', 'karnataka', 'tamil nadu', 'andhra pradesh']):
                risk_factors.extend(['Coastal humidity', 'Salt spray effects'])
                risk_level_weight = 1.1
                
            # Hill stations/cooler regions
            elif any(region in location_lower for region in ['himachal', 'uttarakhand', 'kashmir']):
                risk_factors.extend(['Cool temperatures', 'Frost risk'])
                risk_level_weight = 0.9
            else:
                risk_level_weight = 1.0
        else:
            risk_level_weight = 1.0
        
        # Calculate weighted risk level
        base_risk_levels = ['Low', 'Medium', 'High']
        base_weights = [30, 50, 20]  # Default distribution
        
        # Adjust weights based on location
        if risk_level_weight > 1.1:
            adjusted_weights = [15, 35, 50]  # Higher risk
        elif risk_level_weight < 0.9:
            adjusted_weights = [50, 35, 15]  # Lower risk
        else:
            adjusted_weights = base_weights
        
        risk_level = random.choices(base_risk_levels, weights=adjusted_weights)[0]
        
        return {
            'season': base_season,
            'risk_factors': risk_factors,
            'risk_level': risk_level,
            'location_factor': location if location != "Unknown" else "Not specified",
            'overall_assessment': self._get_environmental_summary(base_season, risk_level, location)
        }
    
    def _get_environmental_summary(self, season, risk_level, location):
        """Generate environmental risk summary."""
        summaries = {
            'Monsoon': {
                'High': f"High disease risk due to monsoon conditions in {location}. Monitor closely for fungal diseases.",
                'Medium': f"Moderate risk during monsoon season in {location}. Maintain preventive measures.", 
                'Low': f"Lower risk despite monsoon - good drainage in {location} helps."
            },
            'Winter': {
                'High': f"Winter conditions in {location} favor certain diseases. Watch for frost damage.",
                'Medium': f"Moderate winter risk in {location}. Temperature variations may stress plants.",
                'Low': f"Low disease risk during winter in {location}. Good season for crop health."
            },
            'Summer': {
                'High': f"High heat stress risk in {location}. Ensure adequate irrigation.",
                'Medium': f"Moderate summer stress in {location}. Monitor water requirements.",
                'Low': f"Manageable summer conditions in {location}. Maintain regular care."
            }
        }
        
        return summaries.get(season, {}).get(risk_level, "Environmental assessment completed.")

    def _calculate_urgency(self, diseases):
        """Calculate urgency level based on detected diseases."""
        if not diseases or diseases[0]['disease_id'] == 'healthy':
            return 'None'
        
        max_severity = max([d.get('severity', 'mild') for d in diseases])
        
        urgency_map = {
            'mild': 'Low',
            'moderate': 'Medium', 
            'severe': 'High'
        }
        
        return urgency_map.get(max_severity, 'Low')
    
    def get_treatment_plan(self, disease_id, severity, crop_type):
        """Get detailed treatment plan for detected disease."""
        
        if disease_id == 'healthy' or disease_id not in self.disease_database:
            return {
                'immediate_actions': ['Continue regular monitoring', 'Maintain good field hygiene'],
                'treatments': [],
                'timeline': 'No treatment needed',
                'cost_estimate': 0,
                'success_rate': 100
            }
        
        disease = self.disease_database[disease_id]
        treatments = disease['treatments'].get(severity, disease['treatments']['mild'])
        cost = disease['cost_estimate'].get(severity, 500)
        
        # Generate timeline based on severity
        timeline_map = {
            'mild': '1-2 weeks',
            'moderate': '2-4 weeks', 
            'severe': '4-6 weeks'
        }
        
        success_rates = {
            'mild': random.randint(85, 95),
            'moderate': random.randint(70, 85),
            'severe': random.randint(50, 70)
        }
        
        return {
            'immediate_actions': treatments[:2],
            'treatments': treatments,
            'timeline': timeline_map.get(severity, '2-3 weeks'),
            'cost_estimate': cost,
            'success_rate': success_rates.get(severity, 75),
            'follow_up': 'Monitor weekly and document progress'
        }
    
    def get_prevention_strategies(self, crop_type, location="Unknown"):
        """Get comprehensive prevention strategies for crop health."""
        
        # Generic prevention strategies
        general_strategies = [
            '🌱 **Seed Selection**: Use certified, disease-resistant varieties',
            '🚰 **Water Management**: Implement proper irrigation scheduling', 
            '🧹 **Field Sanitation**: Remove crop debris and weeds regularly',
            '🔄 **Crop Rotation**: Follow 2-3 year rotation with non-host crops',
            '⚖️ **Balanced Nutrition**: Maintain optimal NPK levels',
            '🔍 **Regular Monitoring**: Weekly field inspections for early detection',
            '🛡️ **Integrated Pest Management**: Use biological and chemical controls wisely',
            '📅 **Timely Operations**: Follow recommended planting and harvesting schedules'
        ]
        
        # Crop-specific strategies
        crop_specific = {
            'Rice': [
                '💧 Maintain proper water levels in fields',
                '🌾 Use short-duration varieties in disease-prone areas',
                '🦆 Consider duck farming for integrated pest control'
            ],
            'Wheat': [
                '❄️ Follow recommended sowing dates to avoid rust',
                '💨 Ensure proper air circulation between plants',
                '🌡️ Monitor weather for rust-favorable conditions'
            ],
            'Cotton': [
                '🐛 Implement bollworm management strategies',
                '🌿 Use trap crops around main cotton fields',
                '💧 Avoid water stress during flowering'
            ]
        }
        
        strategies = general_strategies.copy()
        if crop_type in crop_specific:
            strategies.extend(crop_specific[crop_type])
        
        return {
            'general_strategies': general_strategies,
            'crop_specific': crop_specific.get(crop_type, []),
            'seasonal_calendar': self._generate_seasonal_calendar(crop_type),
            'monitoring_checklist': self._generate_monitoring_checklist()
        }
    
    def _generate_seasonal_calendar(self, crop_type):
        """Generate seasonal disease management calendar."""
        calendar = {
            'Pre-Planting (15-30 days before)': [
                'Soil treatment with beneficial microbes',
                'Field preparation and debris removal',
                'Seed treatment with fungicides'
            ],
            'Planting Stage (0-15 days)': [
                'Use certified disease-free seeds',
                'Optimal spacing for air circulation',
                'Soil moisture management'
            ],
            'Vegetative Stage (15-45 days)': [
                'Weekly disease monitoring',
                'Balanced fertilizer application',
                'Preventive fungicide sprays if needed'
            ],
            'Reproductive Stage (45-75 days)': [
                'Intensive monitoring for diseases',
                'Water stress management',
                'Targeted disease control measures'
            ],
            'Maturity & Harvest (75+ days)': [
                'Pre-harvest disease assessment',
                'Proper harvesting techniques',
                'Post-harvest field sanitation'
            ]
        }
        
        return calendar
    
    def _generate_monitoring_checklist(self):
        """Generate weekly monitoring checklist."""
        return [
            '👀 **Visual Inspection**: Check for spots, lesions, or unusual coloration',
            '🍃 **Leaf Health**: Examine both upper and lower leaf surfaces',
            '🌿 **Plant Vigor**: Assess overall plant health and growth',
            '💧 **Moisture Conditions**: Check soil moisture and drainage',
            '🌡️ **Weather Monitoring**: Track temperature and humidity',
            '📸 **Photo Documentation**: Record suspicious symptoms',
            '📝 **Record Keeping**: Document findings and actions taken',
            '🔄 **Treatment Follow-up**: Monitor effectiveness of treatments'
        ]
    
    def generate_expert_consultation_request(self, analysis_report):
        """Generate a structured request for expert consultation."""
        
        diseases = analysis_report['diseases_detected']
        severe_diseases = [d for d in diseases if d.get('severity') == 'severe']
        
        consultation_needed = (
            len(severe_diseases) > 0 or
            analysis_report['urgency_level'] == 'High' or
            analysis_report['confidence_score'] < 0.8
        )
        
        if not consultation_needed:
            return {'needed': False, 'message': 'Current analysis sufficient for management'}
        
        expert_request = {
            'needed': True,
            'priority': 'High' if severe_diseases else 'Medium',
            'summary': f"Disease detected in {analysis_report['crop_type']} crop",
            'key_concerns': [
                f"Detected: {', '.join([d['name'] for d in diseases])}",
                f"Severity: {', '.join([d['severity'] for d in diseases])}",
                f"Confidence: {analysis_report['confidence_score']}"
            ],
            'questions_for_expert': [
                'Please confirm the disease identification',
                'Are the recommended treatments appropriate?',
                'Any additional management strategies needed?',
                'Prevention measures for future crops?'
            ],
            'estimated_consultation_fee': random.randint(500, 1500),
            'recommended_expert_types': ['Plant Pathologist', 'Agricultural Extension Officer']
        }
        
        return expert_request