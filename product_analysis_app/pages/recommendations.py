# /Users/frankvanlaarhoven/airflow_project/product_analysis_app/pages/recommendations.py
import streamlit as st
from services.product_service import ProductService
from components.metrics import MetricsComponent

def show():
    st.title("Product Recommendations")
    
    # Get data from view
    df = ProductService.get_recommendations()
    
    if df is not None:
        selected_category = st.selectbox(
            "Select Category",
            options=df['category'].unique()
        )
        
        if selected_category:
            product_data = df[df['category'] == selected_category].iloc[0]
            
            # Display recommendations
            st.markdown(f"""
                <div class='metric-card'>
                    <h3>Price Strategy</h3>
                    <div class='metric-header'>
                        <div class='metric-value'>${product_data['avg_price']:,.2f}</div>
                        <span class="rating-badge rating-{product_data['price_rating'].lower()}">
                            {product_data['price_rating']}
                        </span>
                    </div>
                    <p class="strategy-text">💡 {product_data['price_strategy']}</p>
                </div>
                
                <div class='metric-card'>
                    <h3>Volume Strategy</h3>
                    <div class='metric-header'>
                        <div class='metric-value'>{int(product_data['total_units']):,}</div>
                        <span class="rating-badge rating-{product_data['volume_rating'].lower().replace(' ', '-')}">
                            {product_data['volume_rating']}
                        </span>
                    </div>
                    <p class="strategy-text">📦 {product_data['volume_strategy']}</p>
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    show()