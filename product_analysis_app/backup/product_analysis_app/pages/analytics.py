# pages/analytics.py
import streamlit as st
from components.charts import ChartComponent
import pandas as pd
from utils.database import get_postgres_connection  # Single import path
import logging
from services.product_service import ProductService

# Configure logging and page settings
logger = logging.getLogger(__name__)
st.set_page_config(
    page_title="Product Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_product_data():
    """Load product data from recommendations view"""
    try:
        query = """
        SELECT 
            category,
            avg_price,
            total_units,
            price_rating,
            volume_rating,
            created_at,
            price_strategy,
            volume_strategy
        FROM meap.vw_product_recommendations
        """
        return pd.read_sql(query, con=get_postgres_connection())
    except Exception as e:
        logger.error(f"Data loading error: {str(e)}")
        return None

# pages/analytics.py
def show_analytics():
    st.title("Product Analysis")
    
    # Data source selector
    service = ProductService()
    source_type = st.selectbox(
        "Select Data Source Type",
        service.get_data_source_types()
    )
    
    # Dataset selector based on source type
    if source_type == "Local CSV Files":
        dataset = st.selectbox(
            "Select Local Dataset",
            service.get_local_datasets()
        )
    elif source_type == "Kaggle Dataset":
        dataset = st.text_input(
            "Enter Kaggle Dataset Name (e.g., 'username/dataset')"
        )
    else:
        dataset = None
    
    # Load and display data
    if st.button("Load Data"):
        df = service.get_recommendations(source_type, dataset)
        if not df.empty:
            st.dataframe(df)
            
            # Visualizations
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Price Ratings")
                st.bar_chart(df['price_rating'].value_counts())
            with col2:
                st.subheader("Volume Ratings")
                st.bar_chart(df['volume_rating'].value_counts())

def show():
    # Custom CSS for better UI
    st.markdown("""
        <style>
        .main {
            padding: 0rem 1rem;
        }
        .stMetric {
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 0.5rem;
            box-shadow: 0 0.125rem 0.25rem rgba(0,0,0,0.075);
        }
        .stAlert {
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 1rem 0;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header with company branding
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("📊 Product Analytics Dashboard")
        st.markdown("*Real-time insights for data-driven decisions*")
    
    df = load_product_data()
    
    if df is not None:
        try:
            # Sidebar Configuration
            with st.sidebar:
                st.image("https://via.placeholder.com/150?text=Logo", width=150)
                st.markdown("### Dashboard Controls")
                
                # Time Range Filter
                st.markdown("#### 📅 Time Range")
                date_range = st.date_input(
                    "Select Date Range",
                    value=(df['created_at'].min().date(), df['created_at'].max().date()),
                    key="date_range"
                )
                
                # Category Filter with Select All option
                st.markdown("#### 🏷️ Categories")
                all_categories = st.checkbox("Select All Categories", value=True)
                if all_categories:
                    categories = df['category'].unique().tolist()
                else:
                    categories = st.multiselect(
                        "Choose Categories",
                        options=sorted(df['category'].unique()),
                        default=sorted(df['category'].unique())[:3]
                    )
                
                # Advanced Filters
                with st.expander("🔍 Advanced Filters"):
                    price_ratings = st.multiselect(
                        "Price Ratings",
                        options=['AAA', 'AA', 'A', 'B'],
                        default=['AAA', 'AA', 'A', 'B']
                    )
                    volume_ratings = st.multiselect(
                        "Volume Ratings",
                        options=['High Volume', 'Medium Volume', 'Standard Volume'],
                        default=['High Volume', 'Medium Volume', 'Standard Volume']
                    )

            # Apply filters
            filtered_df = df[
                (df['category'].isin(categories)) &
                (df['price_rating'].isin(price_ratings)) &
                (df['volume_rating'].isin(volume_ratings)) &
                (df['created_at'].dt.date.between(date_range[0], date_range[1]))
            ]

            # Initialize charts
            charts = ChartComponent(filtered_df)

            # Main Dashboard Area
            tab1, tab2, tab3, tab4 = st.tabs([
                "📈 Overview", "💰 Sales Analysis", 
                "📊 Category Insights", "📦 Stock Management"
            ])

            with tab1:
                # KPI Metrics Row
                st.markdown("### Key Performance Indicators")
                m1, m2, m3, m4 = st.columns(4)
                
                with m1:
                    revenue = (filtered_df['avg_price'] * filtered_df['total_units']).sum()
                    st.metric("Total Revenue", f"${revenue:,.2f}")
                
                with m2:
                    avg_price = filtered_df['avg_price'].mean()
                    st.metric("Average Price", f"${avg_price:.2f}")
                
                with m3:
                    total_units = filtered_df['total_units'].sum()
                    st.metric("Total Units", f"{total_units:,}")
                
                with m4:
                    categories_count = len(filtered_df['category'].unique())
                    st.metric("Active Categories", categories_count)

                # Performance Matrix
                st.plotly_chart(charts.create_performance_matrix(), use_container_width=True)

            with tab2:
                st.markdown("### Sales Performance Analysis")
                
                # Price Distribution
                c1, c2 = st.columns(2)
                with c1:
                    st.plotly_chart(charts.create_price_chart(), use_container_width=True)
                with c2:
                    # Price Strategy Distribution
                    strategy_dist = filtered_df.groupby('price_strategy').size().reset_index(name='count')
                    st.dataframe(strategy_dist, use_container_width=True)

            with tab3:
                st.markdown("### Category Performance Insights")
                
                # Category Metrics Table
                category_metrics = filtered_df.groupby('category').agg({
                    'avg_price': 'mean',
                    'total_units': 'sum',
                    'price_rating': lambda x: x.mode()[0],
                    'volume_rating': lambda x: x.mode()[0],
                    'price_strategy': 'first',
                    'volume_strategy': 'first'
                }).reset_index()
                
                category_metrics['revenue'] = category_metrics['avg_price'] * category_metrics['total_units']
                st.dataframe(
                    category_metrics.sort_values('revenue', ascending=False),
                    use_container_width=True
                )
                
                st.plotly_chart(charts.create_category_chart(), use_container_width=True)

            with tab4:
                st.markdown("### Stock Management Dashboard")
                
                # Volume Analysis
                v1, v2 = st.columns([2, 1])
                with v1:
                    st.plotly_chart(charts.create_volume_chart(), use_container_width=True)
                with v2:
                    st.markdown("#### Stock Recommendations")
                    for _, row in filtered_df.drop_duplicates(['category', 'volume_rating']).iterrows():
                        if row['volume_rating'] == 'High Volume':
                            st.success(f"✅ {row['category']}: {row['volume_strategy']}")
                        elif row['volume_rating'] == 'Medium Volume':
                            st.info(f"ℹ️ {row['category']}: {row['volume_strategy']}")
                        else:
                            st.warning(f"⚠️ {row['category']}: {row['volume_strategy']}")

        except Exception as e:
            logger.error(f"Dashboard error: {str(e)}")
            st.error("🚨 An error occurred while rendering the dashboard")
            st.info("Please refresh the page or contact support if the issue persists")
    else:
        st.error("🚨 Unable to load data")
        st.info("Please check the database connection and try again")

if __name__ == "__main__":
    show()