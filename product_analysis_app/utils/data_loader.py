# utils/data_loader.py
import pandas as pd
import streamlit as st
from services.product_service import ProductService

class DataLoader:
    """Data loader that handles both database and CSV sources"""
    
    @staticmethod
    def load_data(source="database"):
        """Load data from either database or CSV files"""
        if source == "database":
            service = ProductService()
            return service.get_recommendations()
        elif source == "csv":
            try:
                # Load and combine relevant CSV files
                amazon_df = pd.read_csv("data/Amazon Sale Report.csv")
                sales_df = pd.read_csv("data/Sale Report.csv")
                international_df = pd.read_csv("data/International sale Report.csv")
                
                # Process and transform data to match the view structure
                combined_df = DataLoader._process_sales_data(
                    amazon_df, 
                    sales_df, 
                    international_df
                )
                return combined_df
            except Exception as e:
                st.error(f"Error loading CSV files: {str(e)}")
                return None

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