# pages/recommendations.py
import streamlit as st
from services.product_service import ProductService
import os

def show():
    st.title("Product Recommendations")
    
    # Sidebar - Data Controls
    with st.sidebar:
        st.header("Data Controls")
        
        # Data Source Selection
        st.subheader("Select Data Source")
        source_type = st.selectbox(
            "Source Type",
            options=["Database View", "Local File", "Sample Data", "Kaggle Dataset"],
            key="source_type"
        )
        
        df = None
        
        # In recommendations.py
        if source_type == "Database View":
            df = ProductService.get_recommendations(source_type)
            
        elif source_type == "Local File":
            selected_file = st.selectbox(
                "Select Dataset",
                options=list(ProductService.DATA_FILES.keys()),
                key="file_selector"
            )
            
            if selected_file:
                file_path = os.path.join(
                    ProductService.DATA_PATH,
                    ProductService.DATA_FILES[selected_file]
                )
                df = ProductService.load_data(file_path)
                
        elif source_type == "Kaggle Dataset":
            dataset_name = st.text_input(
                "Dataset Name",
                placeholder="username/dataset-name",
                help="Example: singhnavjot2062001/11000-men",
                key="kaggle_input"
            )
            if st.button("Load Dataset", key="kaggle_button"):
                st.info("Kaggle integration coming soon")
                
        elif source_type == "Sample Data":
            df = ProductService.get_sample_data()

    # Display recommendations if data is loaded
    if df is not None and not df.empty:
        selected_category = st.selectbox(
            "Select Category",
            options=df['category'].unique(),
            key="category_selector"
        )
        
        if selected_category:
            product_data = df[df['category'] == selected_category].iloc[0]
            
            # Display recommendations matching view structure
            col1, col2 = st.columns(2)
            
            with col1:
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
                """, unsafe_allow_html=True)
                
            with col2:
                st.markdown(f"""
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
                
            # Add additional metrics
            st.markdown("### Additional Metrics")
            metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
            
            with metrics_col1:
                st.metric("Revenue", f"${product_data['avg_price'] * product_data['total_units']:,.2f}")
            with metrics_col2:
                st.metric("Average Price", f"${product_data['avg_price']:,.2f}")
            with metrics_col3:
                st.metric("Total Units", f"{int(product_data['total_units']):,}")
                
    else:
        st.info("Please select a data source to view recommendations")

if __name__ == "__main__":
    show()