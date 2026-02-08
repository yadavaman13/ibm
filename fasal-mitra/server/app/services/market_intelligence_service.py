"""
Market Intelligence Service

Provides price forecasting, market comparison, and supply-demand analysis
for Gujarat agricultural commodities.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import logging
from functools import lru_cache
import glob

logger = logging.getLogger(__name__)


class MarketIntelligenceService:
    """Service for market price forecasting and analysis"""
    
    def __init__(self):
        # Path to Gujarat market data (from server directory, go up 2 levels to root)
        self.data_path = Path("../../data/gujarat/market-price-arrival")
        self.cache = {}
        self.data_loaded = False
        
    def _load_commodity_data(self, commodity: str) -> Optional[pd.DataFrame]:
        """Load data for a specific commodity"""
        try:
            # Find CSV file matching commodity name
            pattern = f"{commodity}*Daily Price Arrival Report*.csv"
            files = list(self.data_path.glob(pattern))
            
            if not files:
                logger.warning(f"No data file found for commodity: {commodity}")
                return None
            
            file_path = files[0]
            
            # Read CSV, skip title row
            df = pd.read_csv(file_path, skiprows=1)
            
            # Clean price columns (remove commas, convert to float)
            price_cols = ['Min Price', 'Max Price', 'Modal Price']
            for col in price_cols:
                if col in df.columns:
                    df[col] = df[col].astype(str).str.replace(',', '').astype(float)
            
            # Clean arrival quantity
            if 'Arrival Quantity' in df.columns:
                df['Arrival Quantity'] = df['Arrival Quantity'].astype(str).str.replace(',', '').astype(float)
            
            # Parse dates
            df['Arrival Date'] = pd.to_datetime(df['Arrival Date'], format='%d-%m-%Y')
            
            # Sort by date
            df = df.sort_values('Arrival Date')
            
            logger.info(f"Loaded {len(df)} records for {commodity}")
            return df
            
        except Exception as e:
            logger.error(f"Error loading data for {commodity}: {str(e)}")
            return None
    
    def get_available_commodities(self) -> List[Dict]:
        """Get list of all available commodities with metadata"""
        try:
            commodities = []
            csv_files = list(self.data_path.glob("*Daily Price Arrival Report*.csv"))
            
            for file_path in csv_files:
                # Extract commodity name from filename
                commodity_name = file_path.name.split(' Daily')[0]
                
                # Quick count of records
                try:
                    df = pd.read_csv(file_path, skiprows=1)
                    record_count = len(df)
                    
                    # Get date range
                    df['Arrival Date'] = pd.to_datetime(df['Arrival Date'], format='%d-%m-%Y', errors='coerce')
                    dates = df['Arrival Date'].dropna()
                    
                    if len(dates) > 0:
                        date_range = {
                            'start': dates.min().strftime('%Y-%m-%d'),
                            'end': dates.max().strftime('%Y-%m-%d'),
                            'days': (dates.max() - dates.min()).days
                        }
                    else:
                        date_range = None
                    
                    # Categorize commodity
                    category = self._categorize_commodity(commodity_name)
                    
                    commodities.append({
                        'name': commodity_name,
                        'category': category,
                        'record_count': record_count,
                        'date_range': date_range
                    })
                except Exception as e:
                    logger.error(f"Error processing {commodity_name}: {str(e)}")
                    continue
            
            # Sort by category and name
            commodities.sort(key=lambda x: (x['category'], x['name']))
            return commodities
            
        except Exception as e:
            logger.error(f"Error getting commodities: {str(e)}")
            return []
    
    def _categorize_commodity(self, name: str) -> str:
        """Categorize commodity by type"""
        cereals = ['Bajra', 'Wheat', 'Rice', 'Jowar', 'Maize', 'Barley']
        vegetables = ['Potato', 'Tomato', 'Brinjal', 'Cabbage', 'BeetRoot', 'Capsicum']
        cash_crops = ['Cotton', 'Cotton seed', 'Guar', 'Soyabean']
        fruits = ['Banana', 'Lemon']
        pulses = ['Kabuli Chana']
        spices = ['Ajwan']
        
        if any(c in name for c in cereals):
            return 'Cereals'
        elif any(c in name for c in vegetables):
            return 'Vegetables'
        elif any(c in name for c in cash_crops):
            return 'Cash Crops'
        elif any(c in name for c in fruits):
            return 'Fruits'
        elif any(c in name for c in pulses):
            return 'Pulses'
        elif any(c in name for c in spices):
            return 'Spices'
        else:
            return 'Other'
    
    def get_market_comparison(
        self, 
        commodity: str, 
        date: Optional[str] = None,
        district: Optional[str] = None,
        variety: Optional[str] = None
    ) -> List[Dict]:
        """Compare prices across different markets for a commodity"""
        try:
            df = self._load_commodity_data(commodity)
            if df is None or len(df) == 0:
                return []
            
            # Filter by date (use latest if not specified)
            if date:
                target_date = pd.to_datetime(date)
            else:
                target_date = df['Arrival Date'].max()
            
            # Get data for target date (within 3 days window)
            date_window = timedelta(days=3)
            filtered = df[
                (df['Arrival Date'] >= target_date - date_window) &
                (df['Arrival Date'] <= target_date)
            ]
            
            # Apply additional filters
            if district:
                filtered = filtered[filtered['District'].str.lower() == district.lower()]
            
            if variety:
                filtered = filtered[filtered['Variety'].str.lower() == variety.lower()]
            
            if len(filtered) == 0:
                return []
            
            # Group by market and get latest entry
            latest_by_market = filtered.sort_values('Arrival Date').groupby('Market').tail(1)
            
            # Create comparison list
            markets = []
            for _, row in latest_by_market.iterrows():
                markets.append({
                    'district': row['District'],
                    'market': row['Market'],
                    'variety': row['Variety'],
                    'modal_price': float(row['Modal Price']),
                    'min_price': float(row['Min Price']),
                    'max_price': float(row['Max Price']),
                    'arrival_quantity': float(row['Arrival Quantity']),
                    'date': row['Arrival Date'].strftime('%Y-%m-%d'),
                    'price_unit': row['Price Unit']
                })
            
            # Sort by modal price (descending - best price first)
            markets.sort(key=lambda x: x['modal_price'], reverse=True)
            
            return markets
            
        except Exception as e:
            logger.error(f"Error in market comparison: {str(e)}")
            return []
    
    def get_commodity_insights(self, commodity: str, days: int = 30) -> Dict:
        """Get comprehensive insights for a commodity"""
        try:
            df = self._load_commodity_data(commodity)
            if df is None or len(df) == 0:
                return {}
            
            # Filter to recent data
            latest_date = df['Arrival Date'].max()
            cutoff_date = latest_date - timedelta(days=days)
            recent_df = df[df['Arrival Date'] >= cutoff_date]
            
            # Calculate statistics
            insights = {
                'commodity': commodity,
                'total_records': len(df),
                'recent_records': len(recent_df),
                'date_range': {
                    'start': df['Arrival Date'].min().strftime('%Y-%m-%d'),
                    'end': df['Arrival Date'].max().strftime('%Y-%m-%d')
                },
                'price_stats': {
                    'current_avg': float(recent_df['Modal Price'].tail(5).mean()),
                    'period_avg': float(recent_df['Modal Price'].mean()),
                    'min': float(recent_df['Modal Price'].min()),
                    'max': float(recent_df['Modal Price'].max()),
                    'std': float(recent_df['Modal Price'].std())
                },
                'arrival_stats': {
                    'avg_daily': float(recent_df['Arrival Quantity'].mean()),
                    'total': float(recent_df['Arrival Quantity'].sum()),
                    'min': float(recent_df['Arrival Quantity'].min()),
                    'max': float(recent_df['Arrival Quantity'].max())
                },
                'markets': {
                    'total_districts': int(df['District'].nunique()),
                    'total_markets': int(df['Market'].nunique()),
                    'varieties': df['Variety'].unique().tolist()
                }
            }
            
            # Calculate trend
            if len(recent_df) >= 7:
                recent_prices = recent_df.tail(7)['Modal Price'].values
                trend_slope = np.polyfit(range(len(recent_prices)), recent_prices, 1)[0]
                
                if trend_slope > 50:
                    trend = 'rising'
                elif trend_slope < -50:
                    trend = 'falling'
                else:
                    trend = 'stable'
                
                insights['trend'] = {
                    'direction': trend,
                    'slope': float(trend_slope),
                    'change_percent': float((recent_prices[-1] - recent_prices[0]) / recent_prices[0] * 100)
                }
            
            # Top markets by price
            top_markets = df.groupby('Market').agg({
                'Modal Price': 'mean',
                'Arrival Quantity': 'sum'
            }).sort_values('Modal Price', ascending=False).head(5)
            
            insights['top_markets'] = [
                {
                    'market': market,
                    'avg_price': float(row['Modal Price']),
                    'total_arrival': float(row['Arrival Quantity'])
                }
                for market, row in top_markets.iterrows()
            ]
            
            return insights
            
        except Exception as e:
            logger.error(f"Error getting insights for {commodity}: {str(e)}")
            return {}
    
    def simple_forecast(self, commodity: str, days: int = 7) -> Dict:
        """Simple moving average forecast as baseline"""
        try:
            df = self._load_commodity_data(commodity)
            if df is None or len(df) == 0:
                return {'error': 'No data available'}
            
            # Get recent price data (last 30 days for moving average)
            recent_df = df.tail(30).copy()
            
            if len(recent_df) < 7:
                return {'error': 'Insufficient data for forecasting'}
            
            # Calculate moving averages
            recent_df['MA_7'] = recent_df['Modal Price'].rolling(window=7, min_periods=1).mean()
            recent_df['MA_14'] = recent_df['Modal Price'].rolling(window=14, min_periods=1).mean()
            
            # Get current values
            current_price = float(recent_df['Modal Price'].iloc[-1])
            ma_7 = float(recent_df['MA_7'].iloc[-1])
            ma_14 = float(recent_df['MA_14'].iloc[-1])
            
            # Simple trend calculation
            recent_prices = recent_df['Modal Price'].tail(7).values
            trend_slope = np.polyfit(range(len(recent_prices)), recent_prices, 1)[0]
            
            # Generate forecast
            forecast = []
            last_date = recent_df['Arrival Date'].iloc[-1]
            
            for i in range(1, days + 1):
                forecast_date = last_date + timedelta(days=i)
                # Simple linear projection with damping
                forecast_price = current_price + (trend_slope * i * 0.7)  # 0.7 damping factor
                
                # Add confidence interval (±5%)
                forecast.append({
                    'date': forecast_date.strftime('%Y-%m-%d'),
                    'predicted_price': round(float(forecast_price), 2),
                    'lower_bound': round(float(forecast_price * 0.95), 2),
                    'upper_bound': round(float(forecast_price * 1.05), 2)
                })
            
            # Determine trend direction
            if trend_slope > 50:
                trend = 'rising'
            elif trend_slope < -50:
                trend = 'falling'
            else:
                trend = 'stable'
            
            return {
                'commodity': commodity,
                'current_price': current_price,
                'forecast': forecast,
                'trend': {
                    'direction': trend,
                    'slope': float(trend_slope),
                    'ma_7': ma_7,
                    'ma_14': ma_14
                },
                'model': 'simple_moving_average',
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in forecast for {commodity}: {str(e)}")
            return {'error': str(e)}
    
    def get_best_market_recommendation(
        self, 
        commodity: str,
        user_district: Optional[str] = None,
        quantity: Optional[float] = None
    ) -> Dict:
        """Recommend best markets to sell based on price, supply, and location"""
        try:
            # Get current market comparison
            markets = self.get_market_comparison(commodity)
            
            if not markets:
                return {'error': 'No market data available'}
            
            # Score each market
            for market in markets:
                score = 0
                reasoning = []
                
                # Price score (40% weight) - higher price is better
                max_price = max(m['modal_price'] for m in markets)
                min_price = min(m['modal_price'] for m in markets)
                price_range = max_price - min_price
                
                if price_range > 0:
                    price_score = ((market['modal_price'] - min_price) / price_range) * 40
                    score += price_score
                    
                    if market['modal_price'] >= max_price * 0.95:
                        reasoning.append("Premium price")
                
                # Supply score (30% weight) - lower arrival means better demand
                arrivals = [m['arrival_quantity'] for m in markets if m['arrival_quantity'] > 0]
                if arrivals:
                    avg_arrival = sum(arrivals) / len(arrivals)
                    if market['arrival_quantity'] < avg_arrival:
                        score += 30
                        reasoning.append("Low supply = high demand")
                    elif market['arrival_quantity'] < avg_arrival * 1.2:
                        score += 15
                
                # Location score (30% weight) - same district is better
                if user_district and market['district'].lower() == user_district.lower():
                    score += 30
                    reasoning.append("Local market - low transport cost")
                elif user_district:
                    score += 10
                
                market['score'] = round(score, 2)
                market['reasoning'] = reasoning
            
            # Sort by score
            markets.sort(key=lambda x: x['score'], reverse=True)
            
            # Get top 3
            top_markets = markets[:3]
            
            # Calculate potential profit
            best_price = top_markets[0]['modal_price']
            avg_price = sum(m['modal_price'] for m in markets) / len(markets)
            premium_percent = ((best_price - avg_price) / avg_price) * 100
            
            recommendation = {
                'commodity': commodity,
                'best_market': top_markets[0],
                'alternatives': top_markets[1:],
                'market_average_price': round(avg_price, 2),
                'premium_percent': round(premium_percent, 2),
                'potential_profit_per_quintal': round(best_price - avg_price, 2),
                'insights': []
            }
            
            # Add insights
            if premium_percent > 5:
                recommendation['insights'].append(
                    f"Best market offers {premium_percent:.1f}% premium over average"
                )
            
            if top_markets[0]['arrival_quantity'] < avg_arrival * 0.7:
                recommendation['insights'].append(
                    "Low supply in best market indicates strong demand"
                )
            
            # Calculate total profit if quantity provided
            if quantity:
                # Convert MT to quintals (1 MT = 10 quintals)
                quintals = quantity * 10
                total_profit = (best_price - avg_price) * quintals
                recommendation['potential_total_profit'] = round(total_profit, 2)
                recommendation['quantity_quintals'] = quintals
            
            return recommendation
            
        except Exception as e:
            logger.error(f"Error getting recommendation: {str(e)}")
            return {'error': str(e)}


# Singleton instance
_market_service = None

def get_market_intelligence_service() -> MarketIntelligenceService:
    """Get or create market intelligence service instance"""
    global _market_service
    if _market_service is None:
        _market_service = MarketIntelligenceService()
    return _market_service
