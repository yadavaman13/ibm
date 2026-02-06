"""
Soil Analysis Service

Provides soil suitability analysis and crop recommendations
"""

from typing import Optional, Dict, List
import logging
from functools import lru_cache

from app.core.data_loader import DataLoader, get_data_loader

logger = logging.getLogger(__name__)


class SoilAnalysisService:
    """Soil analysis and crop recommendation service"""
    
    def __init__(self, data_loader: DataLoader):
        self.data_loader = data_loader
        
        # Load datasets if not loaded
        if data_loader.soil_data is None:
            data_loader.load_datasets()
        
        # Crop requirements (pH range, N range, P range, K range)
        self.crop_requirements = {
            'Rice': {'pH': (5.5, 7.0), 'N': (60, 120), 'P': (15, 35), 'K': (20, 40)},
            'Wheat': {'pH': (6.0, 7.5), 'N': (80, 120), 'P': (20, 40), 'K': (25, 50)},
            'Cotton': {'pH': (6.0, 7.5), 'N': (60, 100), 'P': (15, 30), 'K': (20, 40)},
            'Sugarcane': {'pH': (6.0, 7.5), 'N': (100, 150), 'P': (25, 55), 'K': (30, 50)},
            'Maize': {'pH': (5.5, 7.5), 'N': (60, 100), 'P': (20, 40), 'K': (25, 45)},
            'Potato': {'pH': (4.8, 6.5), 'N': (70, 110), 'P': (20, 40), 'K': (30, 50)},
            'Tomato': {'pH': (6.0, 7.0), 'N': (70, 100), 'P': (25, 45), 'K': (30, 50)},
            'Onion': {'pH': (6.0, 7.0), 'N': (60, 90), 'P': (20, 35), 'K': (25, 40)},
        }
    
    def get_soil_data(self, state: str) -> Optional[Dict]:
        """Get soil data for a specific state"""
        soil_data = self.data_loader.get_soil_data_for_state(state)
        
        if soil_data is None:
            return None
        
        # Add interpretation
        soil_data['interpretation'] = self._interpret_soil_data(soil_data)
        
        return soil_data
    
    def check_suitability(self, state: str, crop: str) -> Dict:
        """Check soil suitability for a crop"""
        soil_data = self.data_loader.get_soil_data_for_state(state)
        
        if soil_data is None:
            return {
                'suitable': False,
                'error': f'No soil data available for state: {state}',
                'available_states': self.get_available_states()
            }
        
        if crop not in self.crop_requirements:
            return {
                'suitable': False,
                'error': f'Crop requirements not defined for: {crop}',
                'available_crops': list(self.crop_requirements.keys())
            }
        
        requirements = self.crop_requirements[crop]
        
        # Check each parameter
        suitability_checks = {
            'pH': self._check_range(soil_data.get('pH', 0), requirements['pH']),
            'N': self._check_range(soil_data.get('N', 0), requirements['N']),
            'P': self._check_range(soil_data.get('P', 0), requirements['P']),
            'K': self._check_range(soil_data.get('K', 0), requirements['K'])
        }
        
        # Overall suitability
        suitable_count = sum(1 for check in suitability_checks.values() if check['suitable'])
        overall_suitable = suitable_count >= 3  # At least 3 out of 4 must be suitable
        
        result = {
            'state': state,
            'crop': crop,
            'suitable': overall_suitable,
            'suitability_score': round(suitable_count / 4 * 100, 1),
            'soil_data': soil_data,
            'requirements': requirements,
            'checks': suitability_checks,
            'recommendations': self._generate_suitability_recommendations(
                suitability_checks, soil_data, requirements
            )
        }
        
        return result
    
    def check_enhanced_suitability(self, state: str, crop: str, **enhanced_params) -> Dict:
        """Enhanced soil suitability check with additional farming parameters"""
        # Get basic suitability first
        basic_result = self.check_suitability(state=state, crop=crop)
        
        if 'error' in basic_result:
            return basic_result
        
        # Extract enhanced parameters
        field_size = enhanced_params.get('field_size')
        irrigation_type = enhanced_params.get('irrigation_type')
        previous_crop = enhanced_params.get('previous_crop')
        water_quality = enhanced_params.get('water_quality')
        
        # Enhance the analysis
        enhanced_result = basic_result.copy()
        
        # Add irrigation compatibility
        irrigation_compatibility = self._assess_irrigation_compatibility(crop, irrigation_type)
        enhanced_result['irrigation_analysis'] = irrigation_compatibility
        
        # Add water quality impact
        water_impact = self._assess_water_quality_impact(crop, water_quality)
        enhanced_result['water_quality_impact'] = water_impact
        
        # Add crop rotation benefits
        rotation_analysis = self._assess_crop_rotation(crop, previous_crop)
        enhanced_result['rotation_analysis'] = rotation_analysis
        
        # Generate scaled input recommendations
        if field_size:
            input_recommendations = self._generate_scaled_recommendations(
                crop, state, field_size
            )
            enhanced_result['input_recommendations'] = input_recommendations
        

        
        # Calculate enhanced suitability score
        enhanced_score = self._calculate_enhanced_suitability_score(
            basic_result.get('suitability_score', 0),
            irrigation_compatibility,
            water_impact,
            rotation_analysis
        )
        enhanced_result['enhanced_suitability_score'] = enhanced_score
        
        return enhanced_result
    
    def _assess_irrigation_compatibility(self, crop: str, irrigation_type: Optional[str]) -> Dict:
        """Assess crop compatibility with irrigation type"""
        if not irrigation_type:
            return {"status": "no_info", "message": "No irrigation information provided"}
        
        # Water requirement mapping (simplified)
        water_requirements = {
            'Rice': 'high',
            'Sugarcane': 'high', 
            'Cotton(lint)': 'medium',
            'Wheat': 'medium',
            'Maize': 'medium',
            'Bajra': 'low',
            'Jowar': 'low'
        }
        
        crop_water_need = water_requirements.get(crop, 'medium')
        
        compatibility_matrix = {
            'rainfed': {'high': 'poor', 'medium': 'fair', 'low': 'good'},
            'drip': {'high': 'excellent', 'medium': 'excellent', 'low': 'good'},
            'sprinkler': {'high': 'good', 'medium': 'excellent', 'low': 'good'},
            'flood': {'high': 'excellent', 'medium': 'fair', 'low': 'poor'},
            'mixed': {'high': 'good', 'medium': 'good', 'low': 'good'}
        }
        
        compatibility = compatibility_matrix.get(irrigation_type, {}).get(crop_water_need, 'fair')
        
        messages = {
            'excellent': f"Excellent match! {irrigation_type.title()} irrigation is ideal for {crop}",
            'good': f"Good compatibility between {irrigation_type} irrigation and {crop}",
            'fair': f"Acceptable, but consider optimizing {irrigation_type} irrigation for {crop}",
            'poor': f"Poor match. {crop} may struggle with {irrigation_type} irrigation"
        }
        
        return {
            'compatibility': compatibility,
            'message': messages.get(compatibility, 'No specific recommendation'),
            'crop_water_requirement': crop_water_need
        }
    
    def _assess_water_quality_impact(self, crop: str, water_quality: Optional[str]) -> Dict:
        """Assess impact of water quality on crop suitability"""
        if not water_quality or water_quality == 'unknown':
            return {"status": "no_info", "message": "No water quality information provided"}
        
        # Salt tolerance mapping (simplified)
        salt_tolerance = {
            'Rice': 'medium',
            'Cotton(lint)': 'high',
            'Wheat': 'medium', 
            'Barley': 'high',
            'Coconut': 'high',
            'Bajra': 'medium',
            'Gram': 'low',
            'Arhar/Tur': 'low'
        }
        
        crop_tolerance = salt_tolerance.get(crop, 'medium')
        
        impact_matrix = {
            'sweet': {'high': 'excellent', 'medium': 'excellent', 'low': 'excellent'},
            'slightlySalty': {'high': 'good', 'medium': 'fair', 'low': 'poor'},
            'verySalty': {'high': 'fair', 'medium': 'poor', 'low': 'very_poor'}
        }
        
        impact = impact_matrix.get(water_quality, {}).get(crop_tolerance, 'fair')
        
        messages = {
            'excellent': "Water quality is perfect for this crop",
            'good': "Water quality is suitable, minor yield impact possible",
            'fair': "Water quality may moderately affect yield. Consider soil amendments",
            'poor': "Water quality is problematic. Significant yield reduction expected",
            'very_poor': "Water quality is unsuitable. Consider alternative crops"
        }
        
        return {
            'impact': impact,
            'message': messages.get(impact, 'No specific recommendation'),
            'crop_salt_tolerance': crop_tolerance
        }
    
    def _assess_crop_rotation(self, current_crop: str, previous_crop: Optional[str]) -> Dict:
        """Assess crop rotation benefits/issues"""
        if not previous_crop or previous_crop == 'none':
            return {
                'status': 'new_field',
                'message': 'No rotation history. Good for soil health assessment.',
                'benefit': 'neutral'
            }
        
        # Simplified rotation benefits
        legumes = ['Gram', 'Arhar/Tur', 'Moong(Green Gram)', 'Urad', 'Masoor']
        cereals = ['Rice', 'Wheat', 'Maize', 'Jowar', 'Bajra'] 
        cash_crops = ['Cotton(lint)', 'Sugarcane', 'Groundnut', 'Sunflower']
        
        def get_crop_category(crop):
            if crop in legumes: return 'legume'
            elif crop in cereals: return 'cereal' 
            elif crop in cash_crops: return 'cash_crop'
            else: return 'other'
        
        prev_category = get_crop_category(previous_crop)
        curr_category = get_crop_category(current_crop)
        
        # Rotation benefit logic
        if prev_category == 'legume' and curr_category == 'cereal':
            return {
                'benefit': 'excellent',
                'message': f'Excellent rotation! {previous_crop} (legume) will provide nitrogen for {current_crop}',
                'nitrogen_bonus': True
            }
        elif prev_category == curr_category:
            return {
                'benefit': 'poor', 
                'message': f'Same crop category repeated. May increase pest/disease risk and deplete specific nutrients',
                'risk_warning': True
            }
        else:
            return {
                'benefit': 'good',
                'message': f'Good rotation diversity between {previous_crop} and {current_crop}',
                'nitrogen_bonus': False
            }
    
    def _generate_scaled_recommendations(self, crop: str, state: str, field_size: float) -> Dict:
        """Generate input recommendations scaled to field size and budget"""
        # Get basic soil data
        soil_data = self.data_loader.get_soil_data_for_state(state)
        if not soil_data:
            return {"error": "No soil data available for scaling recommendations"}
        
        # Base fertilizer recommendations per hectare (kg/ha)
        base_fertilizer = {
            'Rice': {'N': 80, 'P': 40, 'K': 40},
            'Wheat': {'N': 120, 'P': 60, 'K': 40}, 
            'Maize': {'N': 150, 'P': 60, 'K': 50},
            'Cotton(lint)': {'N': 160, 'P': 80, 'K': 80},
            'Sugarcane': {'N': 200, 'P': 100, 'K': 100}
        }
        
        crop_fertilizer = base_fertilizer.get(crop, {'N': 100, 'P': 50, 'K': 50})
        
        # Scale to field size
        total_fertilizer = {
            nutrient: amount * field_size 
            for nutrient, amount in crop_fertilizer.items()
        }

        # Estimated costs (simplified)
        cost_per_kg = {'N': 20, 'P': 25, 'K': 18}  # Approximate costs in INR
        total_cost = sum(
            total_fertilizer[nutrient] * cost_per_kg[nutrient]
            for nutrient in total_fertilizer
        )
        
        return {
            'field_size_hectares': field_size,
            'fertilizer_recommendations': {
                'per_hectare': crop_fertilizer,
                'total_field': total_fertilizer
            },
            'estimated_cost': {
                'total_inr': round(total_cost, 2),
                'per_hectare_inr': round(total_cost / field_size, 2) if field_size > 0 else 0
            },
            'application_timing': self._get_application_timing(crop)
        }
    
    def _get_application_timing(self, crop: str) -> List[str]:
        """Get fertilizer application timing recommendations"""
        timing_map = {
            'Rice': ['50% N + full P&K at planting', '25% N at tillering', '25% N at flowering'],
            'Wheat': ['50% N + full P&K at sowing', '50% N at crown root initiation'],
            'Maize': ['25% N + full P&K at planting', '50% N at knee-high stage', '25% N at tasseling'],
            'Cotton(lint)': ['25% N + full P&K at planting', '50% N at squaring', '25% N at flowering']
        }
        return timing_map.get(crop, ['Apply in 2-3 split doses during crop growth'])
    

    
    def _calculate_enhanced_suitability_score(self, base_score: float, irrigation_compat: Dict, 
                                            water_impact: Dict, rotation_analysis: Dict) -> float:
        """Calculate enhanced suitability score considering all factors"""
        score = base_score
        
        # Irrigation compatibility adjustment
        irrigation_adjustments = {
            'excellent': 0.15,
            'good': 0.10,
            'fair': 0.0,
            'poor': -0.15
        }
        irrigation_compat_level = irrigation_compat.get('compatibility', 'fair')
        score += irrigation_adjustments.get(irrigation_compat_level, 0)
        
        # Water quality adjustment
        water_adjustments = {
            'excellent': 0.10,
            'good': 0.05,
            'fair': 0.0,
            'poor': -0.10,
            'very_poor': -0.20
        }
        water_impact_level = water_impact.get('impact', 'fair')
        score += water_adjustments.get(water_impact_level, 0)
        
        # Rotation benefit adjustment
        rotation_adjustments = {
            'excellent': 0.10,
            'good': 0.05,
            'neutral': 0.0,
            'poor': -0.05
        }
        rotation_benefit = rotation_analysis.get('benefit', 'neutral')
        score += rotation_adjustments.get(rotation_benefit, 0)
        
        # Ensure score stays within bounds
        return max(0.0, min(1.0, score))
    
    def get_crop_recommendations(self, state: str) -> Dict:
        """Get crop recommendations based on soil"""
        soil_data = self.data_loader.get_soil_data_for_state(state)
        
        if soil_data is None:
            return {
                'error': f'No soil data available for state: {state}',
                'available_states': self.get_available_states()
            }
        
        # Check suitability for all crops
        recommendations = []
        
        for crop, requirements in self.crop_requirements.items():
            suitability = self.check_suitability(state, crop)
            
            if suitability.get('suitable', False):
                recommendations.append({
                    'crop': crop,
                    'suitability_score': suitability['suitability_score'],
                    'reason': self._generate_recommendation_reason(suitability['checks'])
                })
        
        # Sort by suitability score
        recommendations.sort(key=lambda x: x['suitability_score'], reverse=True)
        
        return {
            'state': state,
            'soil_data': soil_data,
            'recommended_crops': recommendations[:5],  # Top 5
            'total_suitable_crops': len(recommendations)
        }
    
    def get_available_states(self) -> List[str]:
        """Get list of states with soil data"""
        if self.data_loader.soil_data is None:
            return []
        return sorted(self.data_loader.soil_data['state'].unique().tolist())
    
    def _check_range(self, value: float, requirement) -> Dict:
        """Check if value is within required range - handles both dict and tuple formats"""
        
        # Handle different input formats
        if isinstance(requirement, dict):
            # Enhanced format with min/max/ideal keys
            min_val = requirement.get('min', 0)
            max_val = requirement.get('max', float('inf'))
        elif isinstance(requirement, (tuple, list)) and len(requirement) == 2:
            # Basic format as (min, max) tuple
            min_val, max_val = requirement
        else:
            # Default fallback
            min_val, max_val = 0, float('inf')
        
        suitable = min_val <= value <= max_val
        
        result = {
            'value': value,
            'requirement': {'min': min_val, 'max': max_val} if not isinstance(requirement, dict) else requirement,
            'suitable': suitable,
            'status': 'Good' if suitable else 'Needs adjustment'
        }
        
        # Add deviation calculation
        if not suitable:
            if value < min_val:
                result['issue'] = 'too_low'
                result['adjustment_needed'] = round(min_val - value, 2)
                result['deviation'] = {'type': 'low', 'amount': min_val - value}
            else:
                result['issue'] = 'too_high' 
                result['adjustment_needed'] = round(value - max_val, 2)
                result['deviation'] = {'type': 'high', 'amount': value - max_val}
        else:
            result['deviation'] = {'type': 'optimal', 'amount': 0}
        
        return result
    
    def _interpret_soil_data(self, soil_data: Dict) -> Dict:
        """Interpret soil data"""
        interpretation = {}
        
        # pH interpretation
        pH = soil_data.get('pH', 0)
        if pH < 5.5:
            interpretation['pH'] = 'Acidic - may need liming'
        elif pH > 7.5:
            interpretation['pH'] = 'Alkaline - may need sulfur treatment'
        else:
            interpretation['pH'] = 'Optimal for most crops'
        
        # NPK interpretation
        N = soil_data.get('N', 0)
        interpretation['N'] = 'Low' if N < 40 else 'Medium' if N < 80 else 'High'
        
        P = soil_data.get('P', 0)
        interpretation['P'] = 'Low' if P < 15 else 'Medium' if P < 30 else 'High'
        
        K = soil_data.get('K', 0)
        interpretation['K'] = 'Low' if K < 20 else 'Medium' if K < 40 else 'High'
        
        return interpretation
    
    def _generate_suitability_recommendations(
        self, 
        checks: Dict, 
        soil_data: Dict, 
        requirements: Dict
    ) -> List[str]:
        """Generate recommendations based on suitability checks"""
        recommendations = []
        
        # pH recommendations
        if not checks['pH']['suitable']:
            if checks['pH']['issue'] == 'too_low':
                recommendations.append(f"⚠️ Soil pH is too acidic. Add lime to increase pH by {checks['pH']['adjustment_needed']:.1f} units")
            else:
                recommendations.append(f"⚠️ Soil pH is too alkaline. Add sulfur to decrease pH by {checks['pH']['adjustment_needed']:.1f} units")
        
        # NPK recommendations
        for nutrient in ['N', 'P', 'K']:
            if not checks[nutrient]['suitable']:
                if checks[nutrient]['issue'] == 'too_low':
                    recommendations.append(
                        f"Add {nutrient} fertilizer to increase {nutrient} by {checks[nutrient]['adjustment_needed']:.0f} units"
                    )
                else:
                    recommendations.append(
                        f"Reduce {nutrient} fertilizer application"
                    )
        
        if not recommendations:
            recommendations.append("✅ Soil conditions are optimal for this crop")
        
        return recommendations
    
    def _generate_recommendation_reason(self, checks: Dict) -> str:
        """Generate reason for crop recommendation"""
        suitable_params = [param for param, check in checks.items() if check['suitable']]
        
        if len(suitable_params) == 4:
            return "Perfect soil match for all parameters"
        else:
            return f"Good match - {', '.join(suitable_params)} levels are optimal"


@lru_cache()
def get_soil_service() -> SoilAnalysisService:
    """Get singleton instance of soil analysis service"""
    data_loader = get_data_loader()
    return SoilAnalysisService(data_loader)
