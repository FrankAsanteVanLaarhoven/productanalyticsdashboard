# /Users/frankvanlaarhoven/airflow_project/product_analysis_app/pages/dashboard.py
import streamlit as st
from services.product_service import ProductService
from components.charts import ChartComponent
from components.metrics import MetricsComponent

# pages/dashboard.py
def show():
    st.title("Dashboard")
    
    try:
        df = ProductService.get_recommendations()
        
        if not df.empty:
            charts = ChartComponent(df)
            price_chart = charts.create_price_chart()
            
            if price_chart:
                st.plotly_chart(price_chart, use_container_width=True)
            else:
                st.warning("No data available for price chart")
        else:
            st.warning("No data available")
            
    except Exception as e:
        st.error(f"Error loading dashboard: {str(e)}")
        
        # Charts
        charts = ChartComponent(df)
        st.plotly_chart(charts.create_price_chart(), use_container_width=True)

if __name__ == "__main__":
    show()