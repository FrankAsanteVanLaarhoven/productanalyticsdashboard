# product_analysis_app/utils/data_loader.py

import pandas as pd
import os
import streamlit as st

def load_csv(file_path: str) -> pd.DataFrame:
    """Load a CSV file into a DataFrame."""
    try:
        if not os.path.exists(file_path):
            st.error(f"File not found: {file_path}")
            return pd.DataFrame()
        
        df = pd.read_csv(file_path)
        st.success(f"Loaded data from {file_path}")
        return df
    except Exception as e:
        st.error(f"Error loading CSV: {str(e)}")
        return pd.DataFrame()

def list_files(directory: str) -> list:
    """List all files in a directory."""
    try:
        files = os.listdir(directory)
        st.write(f"Files in {directory}: {files}")
        return files
    except Exception as e:
        st.error(f"Error listing files: {str(e)}")
        return []

    @staticmethod
    def _process_sales_data(amazon_df, sales_df, international_df):
        """Process sales data to match the view structure"""
        try:
            # Combine all sales data
            dfs = [amazon_df, sales_df, international_df]
            combined = pd.concat(dfs, ignore_index=True)
            
            # Calculate metrics to match the view
            result = (combined.groupby('category')
                     .agg({
                         'price': ['mean', 'count'],
                         'quantity': 'sum'
                     })
                     .reset_index())
            
            # Rename columns
            result.columns = ['category', 'avg_price', 'total_orders', 'total_units']
            
            # Add ratings based on the same logic as the view
            result['price_rating'] = result['avg_price'].apply(
                lambda x: 'AAA' if x >= 70 else 
                         'AA' if x >= 50 else 
                         'A' if x >= 30 else 'B'
            )
            
            result['volume_rating'] = result['total_units'].apply(
                lambda x: 'High Volume' if x >= 30 else
                         'Medium Volume' if x >= 20 else
                         'Standard Volume'
            )
            
            # Add strategies using the same CASE logic as the view
            result['price_strategy'] = result['price_rating'].map({
                'AAA': 'Maintain premium pricing',
                'AA': 'Consider price optimization',
                'A': 'Review pricing strategy',
                'B': 'Evaluate market position'
            })
            
            result['volume_strategy'] = result['volume_rating'].map({
                'High Volume': 'Maintain inventory levels',
                'Medium Volume': 'Monitor stock levels',
                'Standard Volume': 'Review stock strategy'
            })
            
            return result
            
        except Exception as e:
            st.error(f"Error processing sales data: {str(e)}")
            return None