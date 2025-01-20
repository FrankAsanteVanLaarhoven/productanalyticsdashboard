# test_service.py
import streamlit as st
from services.product_service import ProductService

def test_recommendations():
    try:
        # Test recommendations fetch
        service = ProductService()
        df = service.get_recommendations()
        
        # Print results
        if df is not None and not df.empty:
            print("Data fetched successfully!")
            print("\nSample data:")
            print(df[['category', 'price_rating', 'volume_rating', 'price_strategy', 'volume_strategy']].head())
        else:
            print("No data fetched")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_recommendations()