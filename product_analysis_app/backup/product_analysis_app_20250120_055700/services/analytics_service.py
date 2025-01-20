import pandas as pd
from typing import Dict, List

class AnalyticsService:
    @staticmethod
    def calculate_price_metrics(df: pd.DataFrame) -> Dict:
        """Calculate price-related metrics"""
        return {
            'avg_price_by_rating': df.groupby('price_rating')['avg_price'].mean().to_dict(),
            'price_distribution': df['price_rating'].value_counts().to_dict(),
            'total_categories': len(df['category'].unique())
        }
    
    @staticmethod
    def calculate_volume_metrics(df: pd.DataFrame) -> Dict:
        """Calculate volume-related metrics"""
        return {
            'total_units_by_rating': df.groupby('volume_rating')['total_units'].sum().to_dict(),
            'volume_distribution': df['volume_rating'].value_counts().to_dict()
        }