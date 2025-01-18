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
            price_strategy,
            volume_strategy
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
