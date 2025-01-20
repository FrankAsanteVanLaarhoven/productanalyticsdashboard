# pages/home.py
import streamlit as st
from services.product_service import ProductService

def show_home():
    st.title("Product Analysis & Insights")
    st.subheader("Make informed decisions with real-time data")
    
    try:
        # Get data using static method
        df = ProductService.get_recommendations()
        
        if not df.empty:
            # Summary metrics with hover effects
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(
                    label="Total Products", 
                    value=len(df),
                    help="Click to see product details"
                )
            with col2:
                st.metric(
                    label="Avg Price", 
                    value=f"${df['avg_price'].mean():.2f}",
                    help="Click for price analysis"
                )
            with col3:
                st.metric(
                    label="Total Units", 
                    value=f"{df['total_units'].sum():,}",
                    help="Click for inventory details"
                )
            
            # Interactive charts
            st.subheader("Quick Insights")
            tabs = st.tabs(["Price Ratings", "Volume Ratings", "Strategies"])
            
            with tabs[0]:
                price_dist = df['price_rating'].value_counts()
                st.bar_chart(price_dist)
                
            with tabs[1]:
                volume_dist = df['volume_rating'].value_counts()
                st.bar_chart(volume_dist)
                
            with tabs[2]:
                st.dataframe(
                    df[['category', 'price_strategy', 'volume_strategy']],
                    use_container_width=True
                )
        else:
            st.warning("No data available. Please check database connection.")
            
    except Exception as e:
        st.error(f"Error loading dashboard: {str(e)}")
        st.info("Please refresh the page or contact support.")

if __name__ == "__main__":
    show_home()