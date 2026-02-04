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
    
    def _check_range(self, value: float, required_range: tuple) -> Dict:
        """Check if value is within required range"""
        min_val, max_val = required_range
        suitable = min_val <= value <= max_val
        
        result = {
            'current_value': value,
            'required_range': required_range,
            'suitable': suitable
        }
        
        if not suitable:
            if value < min_val:
                result['issue'] = 'too_low'
                result['adjustment_needed'] = round(min_val - value, 2)
            else:
                result['issue'] = 'too_high'
                result['adjustment_needed'] = round(value - max_val, 2)
        
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
