# services/product_service.py
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text
import os
from datetime import datetime
from typing import Optional, Dict, List

class ProductService:
    """Service to interact with product recommendations view and CSV data sources"""
    
    # Database configuration
    DB_CONFIG: Dict[str, str] = {
        'host': os.getenv('POSTGRES_HOST', 'postgres'),
        'port': os.getenv('POSTGRES_PORT', '5432'),
        'database': os.getenv('POSTGRES_DB', 'airflow'),
        'user': os.getenv('POSTGRES_USER', 'airflow'),
        'password': os.getenv('POSTGRES_PASSWORD', 'airflow'),
        'schema': 'meap'
    }

    # Available CSV data files
    DATA_FILES = {
        "Amazon Sales": "Amazon Sale Report.csv",
        "International Sales": "International sale Report.csv",
        "Monthly Sales": "May-2022.csv",
        "Sale Report": "Sale Report.csv",
        "Cloud Warehouse": "Cloud Warehouse Compersion Chart.csv",
        "Expense Report": "Expense IIGF.csv",
        "P&L Report": "P  L March 2021.csv"
    }

    @staticmethod
    def get_data_source_types() -> List[str]:
        """Get available data source types including database view and CSV files"""
        return ["Database View"] + list(ProductService.DATA_FILES.keys())

    @staticmethod
    @st.cache_data(ttl=300)
    def get_recommendations(source_type: str = "Database View") -> pd.DataFrame:
        """Fetch recommendations from either database view or CSV files"""
        if source_type == "Database View":
            return ProductService._get_db_data()
        elif source_type in ProductService.DATA_FILES:
            return ProductService._get_csv_data(ProductService.DATA_FILES[source_type])
        else:
            st.error(f"Unknown data source: {source_type}")
            return pd.DataFrame()

    @staticmethod
    def _get_db_data() -> pd.DataFrame:
        """Get data from database view matching meap.vw_product_recommendations exactly"""
        try:
            conn_string = (
                f"postgresql://{ProductService.DB_CONFIG['user']}:"
                f"{ProductService.DB_CONFIG['password']}@"
                f"{ProductService.DB_CONFIG['host']}:"
                f"{ProductService.DB_CONFIG['port']}/"
                f"{ProductService.DB_CONFIG['database']}"
            )
            
            engine = create_engine(conn_string)
            
            with engine.connect() as conn:
                # Set schema path
                conn.execute(text("SET search_path TO meap, public;"))
                
                # Query matching view exactly
                query = """
                SELECT DISTINCT
                    p.category,
                    p.avg_price,
                    p.total_units,
                    p.price_rating,
                    p.volume_rating,
                    CASE p.price_rating
                        WHEN 'AAA' THEN 'Maintain premium pricing'
                        WHEN 'AA' THEN 'Consider price optimization'
                        WHEN 'A' THEN 'Review pricing strategy'
                        ELSE 'Evaluate market position'
                    END as price_strategy,
                    CASE p.volume_rating
                        WHEN 'High Volume' THEN 'Maintain inventory levels'
                        WHEN 'Medium Volume' THEN 'Monitor stock levels'
                        ELSE 'Review stock strategy'
                    END as volume_strategy,
                    p.created_at
                FROM meap.vw_product_recommendations p;
                """
                
                df = pd.read_sql(text(query), conn)
                
                # Verify required columns
                required_cols = [
                    'category', 'avg_price', 'total_units',
                    'price_rating', 'volume_rating',
                    'price_strategy', 'volume_strategy',
                    'created_at'
                ]
                
                if not all(col in df.columns for col in required_cols):
                    st.error("Missing required columns from view")
                    return pd.DataFrame()
                    
                return df if not df.empty else pd.DataFrame()
                
        except Exception as e:
            st.error(f"Database error: {str(e)}")
            return pd.DataFrame()

    @staticmethod
    def get_available_sources() -> List[str]:
        """Get list of available data sources"""
        try:
            # First verify database connection
            engine = create_engine(
                f"postgresql://{ProductService.DB_CONFIG['user']}:"
                f"{ProductService.DB_CONFIG['password']}@"
                f"{ProductService.DB_CONFIG['host']}:"
                f"{ProductService.DB_CONFIG['port']}/"
                f"{ProductService.DB_CONFIG['database']}"
            )
            
            with engine.connect() as conn:
                # Check if view exists
                query = """
                SELECT EXISTS (
                    SELECT FROM information_schema.views 
                    WHERE table_schema = 'meap' 
                    AND table_name = 'vw_product_recommendations'
                );
                """
                view_exists = pd.read_sql(text(query), conn).iloc[0][0]
                
                if view_exists:
                    return ["Database View (Product Recommendations)"]
                else:
                    st.warning("Product recommendations view not found in database")
                    return []
                    
        except Exception as e:
            st.error(f"Error checking data sources: {str(e)}")
            return []

    @staticmethod
    def _get_csv_data(filename: str) -> pd.DataFrame:
        """Transform CSV data to match view structure exactly"""
        try:
            file_path = os.path.join('/Users/frankvanlaarhoven/airflow_project/data', filename)
            if not os.path.exists(file_path):
                st.error(f"File not found: {filename}")
                return pd.DataFrame()

            # Read CSV file
            df = pd.read_csv(file_path)
            
            # Map columns to view structure
            df_transformed = pd.DataFrame()
            
            # Group by category if exists, otherwise create dummy category
            if 'category' in df.columns:
                group_col = 'category'
            elif 'Category' in df.columns:
                group_col = 'Category'
            else:
                df['category'] = 'Default Category'
                group_col = 'category'

            # Find price column
            price_col = next((col for col in df.columns if 'price' in col.lower()), None)
            if not price_col:
                st.warning(f"No price column found in {filename}")
                return pd.DataFrame()

            # Calculate metrics matching view structure
            df_transformed = df.groupby(group_col).agg({
                price_col: ['mean', 'count']
            }).reset_index()

            # Rename columns to match view
            df_transformed.columns = ['category', 'avg_price', 'total_units']

            # Add ratings matching view CASE logic exactly
            df_transformed['price_rating'] = pd.cut(
                df_transformed['avg_price'],
                bins=[-float('inf'), 30, 50, 70, float('inf')],
                labels=['B', 'A', 'AA', 'AAA']
            )

            df_transformed['volume_rating'] = pd.cut(
                df_transformed['total_units'],
                bins=[-float('inf'), 20, 30, float('inf')],
                labels=['Standard Volume', 'Medium Volume', 'High Volume']
            )

            # Add strategies using exact view CASE logic
            df_transformed['price_strategy'] = df_transformed['price_rating'].map({
                'AAA': 'Maintain premium pricing',
                'AA': 'Consider price optimization',
                'A': 'Review pricing strategy',
                'B': 'Evaluate market position'
            })

            df_transformed['volume_strategy'] = df_transformed['volume_rating'].map({
                'High Volume': 'Maintain inventory levels',
                'Medium Volume': 'Monitor stock levels',
                'Standard Volume': 'Review stock strategy'
            })

            # Add timestamp to match view
            df_transformed['created_at'] = datetime.now()

            # Verify all required columns are present
            required_cols = [
                'category', 'avg_price', 'total_units',
                'price_rating', 'volume_rating',
                'price_strategy', 'volume_strategy',
                'created_at'
            ]
            
            if not all(col in df_transformed.columns for col in required_cols):
                st.error(f"Missing required columns after transformation: {filename}")
                return pd.DataFrame()

            return df_transformed

        except Exception as e:
            st.error(f"Error processing {filename}: {str(e)}")
            return pd.DataFrame()

    @staticmethod
    def test_connection() -> bool:
        """Test database connection"""
        try:
            conn_string = (
                f"postgresql://{ProductService.DB_CONFIG['user']}:"
                f"{ProductService.DB_CONFIG['password']}@"
                f"{ProductService.DB_CONFIG['host']}:"
                f"{ProductService.DB_CONFIG['port']}/"
                f"{ProductService.DB_CONFIG['database']}"
            )
            
            engine = create_engine(conn_string)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            st.error(f"Connection test failed: {str(e)}")
            return False

    @staticmethod
    def validate_data(df: pd.DataFrame) -> bool:
        """Validate data matches view structure exactly"""
        try:
            required_cols = [
                'category', 'avg_price', 'total_units',
                'price_rating', 'volume_rating',
                'price_strategy', 'volume_strategy',
                'created_at'
            ]
            
            if not all(col in df.columns for col in required_cols):
                return False
                
            if df.empty:
                return False
                
            return True
            
        except Exception:
            return False