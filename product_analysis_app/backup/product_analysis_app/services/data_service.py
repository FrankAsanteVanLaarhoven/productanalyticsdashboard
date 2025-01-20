# services/data_service.py
import pandas as pd
import streamlit as st
from utils.database import DatabaseConnection

class ProductRecommendationService:
    """Service class to handle product recommendations from the view"""
    
    @staticmethod
    @st.cache_data(ttl=300)
    def get_recommendations():
        """Fetch recommendations from the view"""
        query = """
        SELECT 
            category,
            avg_price,
            total_units,
            price_rating,
            volume_rating,
            price_strategy,  -- Added from the view
            volume_strategy  -- Added from the view
        FROM meap.vw_product_recommendations
        ORDER BY 
            CASE price_rating
                WHEN 'AAA' THEN 1
                WHEN 'AA' THEN 2
                WHEN 'A' THEN 3
                ELSE 4
            END,
            category;
        """
        return DatabaseConnection.execute_query(query)

    @staticmethod
    def get_rating_levels():
        """Get rating level configurations"""
        return {
            'price_ratings': ['AAA', 'AA', 'A', 'B'],
            'volume_ratings': ['High Volume', 'Medium Volume', 'Standard Volume']
        }

    @staticmethod
    def get_strategy_mappings():
        """Get strategy mappings from the view definition"""
        return {
            'price_strategies': {
                'AAA': 'Maintain premium pricing',
                'AA': 'Consider price optimization',
                'A': 'Review pricing strategy',
                'default': 'Evaluate market position'
            },
            'volume_strategies': {
                'High Volume': 'Maintain inventory levels',
                'Medium Volume': 'Monitor stock levels',
                'default': 'Review stock strategy'
            }
        }

    @staticmethod
    def verify_data_pipeline():
        """Verify data consistency between source and recommendations"""
        verification_query = """
        SELECT 
            (SELECT COUNT(*) FROM meap.vw_product_ratings) as source_count,
            (SELECT COUNT(*) FROM meap.vw_product_recommendations) as recommendations_count
        """
        result = DatabaseConnection.execute_query(verification_query)
        return {
            'source_records': result['source_count'].iloc[0],
            'recommendation_records': result['recommendations_count'].iloc[0]
        }