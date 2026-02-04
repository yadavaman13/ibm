"""
Data Loading and Processing Module for FastAPI

Handles loading and preprocessing of agricultural datasets.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, Dict, List
import logging
from functools import lru_cache

logger = logging.getLogger(__name__)


class DataLoader:
    """Centralized data loading and preprocessing for farming advisory system."""
    
    _instance = None  # Singleton instance
    
    def __new__(cls, data_dir: Optional[Path] = None):
        """Implement singleton pattern"""
        if cls._instance is None:
            cls._instance = super(DataLoader, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, data_dir: Optional[Path] = None):
        """Initialize data loader (only once due to singleton)"""
        if self._initialized:
            return
            
        self.data_dir = data_dir or Path(__file__).parent.parent.parent.parent.parent / "data"
        self.crop_data: Optional[pd.DataFrame] = None
        self.soil_data: Optional[pd.DataFrame] = None
        self.weather_data: Optional[pd.DataFrame] = None
        self.price_data: Optional[pd.DataFrame] = None
        self.merged_data: Optional[pd.DataFrame] = None
        self._initialized = True
        
        logger.info(f"DataLoader initialized with data_dir: {self.data_dir}")
    
    def load_datasets(self) -> Dict[str, bool]:
        """
        Load all core datasets.
        
        Returns:
            Dictionary with loading status for each dataset
        """
        logger.info("Loading agricultural datasets...")
        status = {}
        
        try:
            # Load crop yield data
            crop_file = self.data_dir / "raw/crop_yield.csv"
            if crop_file.exists():
                self.crop_data = pd.read_csv(crop_file)
                # Clean column names and string columns
                self.crop_data.columns = self.crop_data.columns.str.strip()
                for col in ['crop', 'season', 'state']:
                    if col in self.crop_data.columns:
                        self.crop_data[col] = self.crop_data[col].str.strip()
                logger.info(f"✅ Loaded crop data: {len(self.crop_data):,} records")
                status['crop_data'] = True
            else:
                logger.error(f"Crop yield data not found: {crop_file}")
                status['crop_data'] = False
        except Exception as e:
            logger.error(f"Error loading crop data: {e}")
            status['crop_data'] = False
        
        try:
            # Load soil data
            soil_file = self.data_dir / "raw/state_soil_data.csv"
            if soil_file.exists():
                self.soil_data = pd.read_csv(soil_file)
                self.soil_data.columns = self.soil_data.columns.str.strip()
                self.soil_data['state'] = self.soil_data['state'].str.strip()
                logger.info(f"✅ Loaded soil data: {len(self.soil_data):,} records")
                status['soil_data'] = True
            else:
                logger.error(f"Soil data not found: {soil_file}")
                status['soil_data'] = False
        except Exception as e:
            logger.error(f"Error loading soil data: {e}")
            status['soil_data'] = False
        
        try:
            # Load weather data
            weather_file = self.data_dir / "raw/state_weather_data_1997_2020.csv"
            if weather_file.exists():
                self.weather_data = pd.read_csv(weather_file)
                self.weather_data.columns = self.weather_data.columns.str.strip()
                self.weather_data['state'] = self.weather_data['state'].str.strip()
                logger.info(f"✅ Loaded weather data: {len(self.weather_data):,} records")
                status['weather_data'] = True
            else:
                logger.error(f"Weather data not found: {weather_file}")
                status['weather_data'] = False
        except Exception as e:
            logger.error(f"Error loading weather data: {e}")
            status['weather_data'] = False
        
        try:
            # Load price data
            price_file = self.data_dir / "raw/Price_Agriculture_commodities_Week.csv"
            if price_file.exists():
                self.price_data = pd.read_csv(price_file)
                self.price_data.columns = self.price_data.columns.str.strip()
                if 'State' in self.price_data.columns:
                    self.price_data['State'] = self.price_data['State'].str.strip()
                if 'Commodity' in self.price_data.columns:
                    self.price_data['Commodity'] = self.price_data['Commodity'].str.strip()
                logger.info(f"✅ Loaded price data: {len(self.price_data):,} records")
                status['price_data'] = True
            else:
                logger.warning(f"Price data not found: {price_file}")
                status['price_data'] = False
        except Exception as e:
            logger.error(f"Error loading price data: {e}")
            status['price_data'] = False
        
        return status
    
    def merge_datasets(self) -> pd.DataFrame:
        """
        Merge all datasets for ML model training.
        
        Returns:
            Merged DataFrame
        """
        if self.crop_data is None or self.soil_data is None or self.weather_data is None:
            raise ValueError("Datasets not loaded. Call load_datasets() first.")
        
        logger.info("Merging datasets...")
        
        # Merge crop yield with weather
        merged = self.crop_data.merge(
            self.weather_data, 
            on=['state', 'year'], 
            how='left'
        )
        
        # Merge with soil
        merged = merged.merge(
            self.soil_data, 
            on='state', 
            how='left'
        )
        
        self.merged_data = merged
        logger.info(f"✅ Merged dataset: {len(merged):,} rows, {len(merged.columns)} columns")
        
        return merged
    
    def filter_data(
        self,
        crop: Optional[str] = None,
        state: Optional[str] = None,
        season: Optional[str] = None,
        year: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Filter crop data by various parameters.
        
        Args:
            crop: Crop name
            state: State name
            season: Season name
            year: Year
            
        Returns:
            Filtered DataFrame
        """
        if self.crop_data is None:
            raise ValueError("Crop data not loaded")
        
        data = self.crop_data.copy()
        
        if crop:
            data = data[data['crop'].str.lower() == crop.lower()]
        if state:
            data = data[data['state'].str.lower() == state.lower()]
        if season:
            data = data[data['season'].str.lower() == season.lower()]
        if year:
            data = data[data['year'] == year]
        
        return data
    
    def get_available_crops(self) -> List[str]:
        """Get list of available crops"""
        if self.crop_data is None:
            return []
        return sorted(self.crop_data['crop'].unique().tolist())
    
    def get_available_states(self) -> List[str]:
        """Get list of available states"""
        if self.crop_data is None:
            return []
        return sorted(self.crop_data['state'].unique().tolist())
    
    def get_available_seasons(self) -> List[str]:
        """Get list of available seasons"""
        if self.crop_data is None:
            return []
        return sorted(self.crop_data['season'].unique().tolist())
    
    def get_soil_data_for_state(self, state: str) -> Optional[Dict]:
        """Get soil data for a specific state"""
        if self.soil_data is None:
            return None
        
        soil = self.soil_data[self.soil_data['state'].str.lower() == state.lower()]
        if soil.empty:
            return None
        
        return soil.iloc[0].to_dict()
    
    def get_dataset_info(self) -> Dict:
        """Get information about loaded datasets"""
        info = {
            "loaded": {},
            "records": {},
            "available_crops": self.get_available_crops() if self.crop_data is not None else [],
            "available_states": self.get_available_states() if self.crop_data is not None else [],
            "available_seasons": self.get_available_seasons() if self.crop_data is not None else []
        }
        
        if self.crop_data is not None:
            info["loaded"]["crop_data"] = True
            info["records"]["crop_data"] = len(self.crop_data)
        
        if self.soil_data is not None:
            info["loaded"]["soil_data"] = True
            info["records"]["soil_data"] = len(self.soil_data)
        
        if self.weather_data is not None:
            info["loaded"]["weather_data"] = True
            info["records"]["weather_data"] = len(self.weather_data)
        
        if self.price_data is not None:
            info["loaded"]["price_data"] = True
            info["records"]["price_data"] = len(self.price_data)
        
        return info


# Global singleton instance
@lru_cache()
def get_data_loader(data_dir: Optional[Path] = None) -> DataLoader:
    """Get or create singleton DataLoader instance"""
    return DataLoader(data_dir)
