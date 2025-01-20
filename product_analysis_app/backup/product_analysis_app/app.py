# app.py
import streamlit as st
import os
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime

# Custom styles
CUSTOM_STYLES = """
<style>
    .gradient-text {
        background: linear-gradient(45deg, #1E88E5, #00ACC1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .header-container {
        text-align: center;
        padding: 2rem 0;
    }
    .subtitle {
        color: #666;
        font-size: 1.2rem;
    }
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    .rating-badge {
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: bold;
    }
</style>
"""

def init_page_config():
    """Initialize page configuration"""
    st.set_page_config(
        page_title="Product Analysis Dashboard",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    # Apply custom styling
    st.markdown(CUSTOM_STYLES, unsafe_allow_html=True)

def apply_custom_style():
    """Apply custom styling"""
    st.markdown(CUSTOM_STYLES, unsafe_allow_html=True)

def add_theme_toggle():
    """Add dark/light mode toggle"""
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'
    
    with st.sidebar:
        theme = st.selectbox(
            "Choose Theme",
            ["Light", "Dark"],
            index=0 if st.session_state.theme == 'light' else 1,
            key='theme_selector'
        )
        st.session_state.theme = theme.lower()
# Database configuration matching view environment
DB_CONFIG = {
    'host': os.getenv('POSTGRES_HOST', 'postgres'),
    'port': os.getenv('POSTGRES_PORT', '5432'),
    'database': os.getenv('POSTGRES_DB', 'airflow'),
    'user': os.getenv('POSTGRES_USER', 'airflow'),
    'password': os.getenv('POSTGRES_PASSWORD', 'airflow'),
    'schema': 'meap'
}

# Constants matching view's CASE statements exactly
PRICE_RATINGS = {
    'AAA': {'color': '#007AFF', 'strategy': 'Maintain premium pricing'},
    'AA': {'color': '#5856D6', 'strategy': 'Consider price optimization'},
    'A': {'color': '#FF9500', 'strategy': 'Review pricing strategy'},
    'B': {'color': '#FF3B30', 'strategy': 'Evaluate market position'}
}

VOLUME_RATINGS = {
    'High Volume': {'color': '#34C759', 'strategy': 'Maintain inventory levels'},
    'Medium Volume': {'color': '#FF9F0A', 'strategy': 'Monitor stock levels'},
    'Standard Volume': {'color': '#64D2FF', 'strategy': 'Review stock strategy'}
}

class ProductService:
    @staticmethod
    def get_db_connection():
        """Create database connection"""
        try:
            engine = create_engine(
                f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
                f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
            )
            return engine
        except Exception as e:
            st.error(f"Database connection error: {e}")
            return None

    @staticmethod
    @st.cache_data(ttl=300)
    def get_recommendations():
        """Fetch recommendations matching view exactly"""
        engine = ProductService.get_db_connection()
        if engine:
            try:
                with engine.connect() as conn:
                    # Set schema path
                    conn.execute(text("SET search_path TO meap, public;"))
                    
                    # Query matching view exactly
                    query = """
                    SELECT DISTINCT
                        p.category,
                        p.avg_price,
                        p.total_units,
                        p.price_rating,
                        p.volume_rating,
                        CASE p.price_rating
                            WHEN 'AAA' THEN 'Maintain premium pricing'
                            WHEN 'AA' THEN 'Consider price optimization'
                            WHEN 'A' THEN 'Review pricing strategy'
                            ELSE 'Evaluate market position'
                        END as price_strategy,
                        CASE p.volume_rating
                            WHEN 'High Volume' THEN 'Maintain inventory levels'
                            WHEN 'Medium Volume' THEN 'Monitor stock levels'
                            ELSE 'Review stock strategy'
                        END as volume_strategy,
                        p.created_at
                    FROM meap.vw_product_recommendations p;
                    """
                    
                    df = pd.read_sql(text(query), conn)
                    return df if not df.empty else pd.DataFrame()
                    
            except Exception as e:
                st.error(f"Data fetch error: {e}")
                return pd.DataFrame()
            finally:
                engine.dispose()
        return pd.DataFrame()

# Rest of your existing code remains the same...

class ChartComponent:
    def __init__(self, df):
        self.df = df

    def create_price_chart(self):
        """Create price distribution chart"""
        fig = px.box(
            self.df,
            x='price_rating',
            y='avg_price',
            color='price_rating',
            color_discrete_map={k: v['color'] for k, v in PRICE_RATINGS.items()},
            title='Price Distribution by Rating'
        )
        return fig

    def create_volume_chart(self):
        """Create volume distribution chart"""
        fig = px.box(
            self.df,
            x='volume_rating',
            y='total_units',
            color='volume_rating',
            color_discrete_map={k: v['color'] for k, v in VOLUME_RATINGS.items()},
            title='Volume Distribution by Rating'
        )
        return fig


def main():
    try:
        # Initialize configuration
        init_page_config()
        
        # Modern header with animation
        st.markdown("""
            <div class="header-container">
                <h1 class="gradient-text">Product Analysis & Insights</h1>
                <p class="subtitle">Make informed decisions with real-time data</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Data source selector and filters
        with st.sidebar:
            source_type = st.selectbox(
                "Select Data Source",
                options=["Database View"],  # Simplified to match view
                key="source_selector"
            )
            
            st.header("Filters")
            price_filter = st.multiselect(
                "Price Rating",
                options=list(PRICE_RATINGS.keys()),
                default=list(PRICE_RATINGS.keys())
            )
            volume_filter = st.multiselect(
                "Volume Rating",
                options=list(VOLUME_RATINGS.keys()),
                default=list(VOLUME_RATINGS.keys())
            )

        # Load and filter data
        if st.button("Analyze Products", key="load_btn", help="Click to fetch data"):
            with st.spinner("Loading insights..."):
                df = ProductService.get_recommendations()  # Static method call
                
                if not df.empty:
                    # Apply filters
                    filtered_df = df[
                        (df['price_rating'].isin(price_filter)) &
                        (df['volume_rating'].isin(volume_filter))
                    ]

                    if filtered_df.empty:
                        st.warning("No data matches the selected filters.")
                        return

                    # Dashboard tabs with modern UI
                    tabs = st.tabs(["📊 Overview", "🎯 Price Analysis", "📦 Volume Analysis", "💡 Recommendations"])

                    with tabs[0]:  # Overview
                        # Key metrics
                        metrics_cols = st.columns(4)
                        with metrics_cols[0]:
                            st.metric("Total Categories", len(filtered_df['category'].unique()))
                        with metrics_cols[1]:
                            st.metric("Average Price", f"${filtered_df['avg_price'].mean():.2f}")
                        with metrics_cols[2]:
                            st.metric("Total Units", f"{filtered_df['total_units'].sum():,}")
                        with metrics_cols[3]:
                            st.metric("Last Updated", filtered_df['created_at'].max().strftime('%Y-%m-%d %H:%M'))

                        # Charts
                        charts = ChartComponent(filtered_df)
                        col1, col2 = st.columns(2)
                        with col1:
                            st.plotly_chart(charts.create_price_chart(), use_container_width=True)
                        with col2:
                            st.plotly_chart(charts.create_volume_chart(), use_container_width=True)

                    with tabs[1]:  # Price Analysis
                        st.header("Category Insights")
                        categories = filtered_df['category'].unique()
                        if len(categories) > 0:
                            selected_category = st.selectbox(
                                "Select Category",
                                options=categories
                            )

                            if selected_category:
                                product_data = filtered_df[filtered_df['category'] == selected_category].iloc[0]
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

                    with tabs[2]:  # Volume Analysis
                        for rating, info in VOLUME_RATINGS.items():
                            products = filtered_df[filtered_df['volume_rating'] == rating]
                            if not products.empty:
                                st.markdown(f"""
                                    <div class="metric-card volume-{rating.lower().replace(' ', '-')}">
                                        <h3>{info['strategy']}</h3>
                                        <p>Products: {len(products)}</p>
                                    </div>
                                """, unsafe_allow_html=True)

                    with tabs[3]:  # Recommendations
                        st.dataframe(
                            filtered_df[[
                                'category', 
                                'price_rating', 
                                'volume_rating', 
                                'price_strategy', 
                                'volume_strategy'
                            ]],
                            use_container_width=True,
                            height=400
                        )

                else:
                    st.error("Unable to load data. Please check database connection.")

    except Exception as e:
        st.error(f"Application error: {str(e)}")
        st.info("Please refresh the page or contact support if the issue persists")

if __name__ == "__main__":
    main()