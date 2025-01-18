# /Users/frankvanlaarhoven/airflow_project/product_analysis_app/pages/dashboard.py
import streamlit as st
from services.product_service import ProductService
from components.charts import ChartComponent
from components.metrics import MetricsComponent

def show():
    st.title("Executive Dashboard")
    
    # Get data from view
    df = ProductService.get_recommendations()
    
    if df is not None:
        # Summary KPIs
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Categories", len(df['category'].unique()))
        with col2:
            st.metric("Avg Price", f"${df['avg_price'].mean():.2f}")
        with col3:
            st.metric("Total Units", f"{df['total_units'].sum():,}")
        with col4:
            st.metric("AAA Products", len(df[df['price_rating'] == 'AAA']))
        
        # Charts
        charts = ChartComponent(df)
        st.plotly_chart(charts.create_price_chart(), use_container_width=True)

if __name__ == "__main__":
    show()