# /Users/frankvanlaarhoven/airflow_project/product_analysis_app/services/product_service.py
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
import os

class ProductService:
    """Service to interact with product recommendations view"""
    
    @staticmethod
    @st.cache_resource
    def get_db_connection():
        try:
            database_url = os.getenv('DATABASE_URL', 'postgresql://airflow:airflow@postgres:5432/airflow')
            return create_engine(database_url)
        except Exception as e:
            st.error(f"Database connection failed: {str(e)}")
            return None

    @staticmethod
    @st.cache_data(ttl=300)
    def get_recommendations():
        """Fetch data from meap.vw_product_recommendations view"""
        engine = ProductService.get_db_connection()
        if engine:
            try:
                # Query matching the exact view output
                query = """
                SELECT 
                    category,
                    avg_price,
                    total_units,
                    price_rating,
                    volume_rating,
                    created_at,
                    price_strategy,
                    volume_strategy
                FROM meap.vw_product_recommendations
                ORDER BY category;
                """
                df = pd.read_sql(query, engine)
                
                # Convert timestamp to datetime
                df['created_at'] = pd.to_datetime(df['created_at'])
                
                if df.empty:
                    st.warning("No data found in the recommendations view")
                return df
            except Exception as e:
                st.error(f"Failed to fetch recommendations: {str(e)}")
                return None
            finally:
                engine.dispose()