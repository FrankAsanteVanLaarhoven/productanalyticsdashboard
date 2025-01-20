# services/product_service.py
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text
import os
from datetime import datetime

class ProductService:
    """Service to interact with product recommendations view"""
    
    DATA_PATH = '/app/data'
    DATA_FILES = {
        "Amazon Sales": "Amazon Sale Report.csv",
        "International Sales": "International sale Report.csv",
        "Monthly Sales": "May-2022.csv",
        "Sale Report": "Sale Report.csv",
        "Cloud Warehouse": "Cloud Warehouse Compersion Chart.csv",
        "Expense Report": "Expense IIGF.csv",
        "P&L Report": "P  L March 2021.csv"
    }

    DB_CONFIG = {
        'host': os.getenv('POSTGRES_HOST', 'postgres'),
        'port': os.getenv('POSTGRES_PORT', '5432'),
        'database': os.getenv('POSTGRES_DB', 'airflow'),
        'user': os.getenv('POSTGRES_USER', 'airflow'),
        'password': os.getenv('POSTGRES_PASSWORD', 'airflow'),
        'schema': 'meap'
    }

    @staticmethod
    def get_recommendations(source_type: str = "Database View") -> pd.DataFrame:
        """Get recommendations from view"""
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
                conn.execute(text(f"SET search_path TO {ProductService.DB_CONFIG['schema']}, public;"))
                query = "SELECT * FROM meap.vw_product_recommendations;"
                
                df = pd.read_sql(text(query), conn)
                
                if df.empty:
                    st.warning("No data found in view")
                else:
                    st.success(f"Loaded {len(df)} recommendations")
                    
                return df
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
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
                st.success("Database connected")
            return True
        except Exception as e:
            st.error(f"Connection failed: {str(e)}")
            return False

    @staticmethod
    def load_data(file_path: str) -> pd.DataFrame:
        """Load and transform file data to match view structure"""
        try:
            if not os.path.exists(file_path):
                st.error(f"File not found: {file_path}")
                return pd.DataFrame()
            
            df = pd.read_csv(file_path)
            st.write("Original columns:", df.columns.tolist())
            
            column_mappings = {
                'Category': 'category',
                'Product Category': 'category',
                'Price': 'avg_price',
                'Amount': 'avg_price',
                'Quantity': 'total_units',
                'Units': 'total_units'
            }
            
            for old_col, new_col in column_mappings.items():
                if old_col in df.columns:
                    df[new_col] = df[old_col]
            
            df_grouped = df.groupby('category').agg({
                'avg_price': 'mean',
                'total_units': 'sum'
            }).reset_index()
            
            df_grouped['price_rating'] = pd.cut(
                df_grouped['avg_price'],
                bins=[-float('inf'), 30, 50, 70, float('inf')],
                labels=['B', 'A', 'AA', 'AAA']
            )
            
            df_grouped['volume_rating'] = pd.cut(
                df_grouped['total_units'],
                bins=[-float('inf'), 20, 30, float('inf')],
                labels=['Standard Volume', 'Medium Volume', 'High Volume']
            )
            
            df_grouped['price_strategy'] = df_grouped['price_rating'].map({
                'AAA': 'Maintain premium pricing',
                'AA': 'Consider price optimization',
                'A': 'Review pricing strategy',
                'B': 'Evaluate market position'
            })
            
            df_grouped['volume_strategy'] = df_grouped['volume_rating'].map({
                'High Volume': 'Maintain inventory levels',
                'Medium Volume': 'Monitor stock levels',
                'Standard Volume': 'Review stock strategy'
            })
            
            df_grouped['created_at'] = datetime.now()
            
            st.success(f"Successfully loaded {len(df_grouped)} categories from file")
            return df_grouped
            
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
            return pd.DataFrame()