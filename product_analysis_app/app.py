# /Users/frankvanlaarhoven/airflow_project/product_analysis_app/app.py
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import os
from datetime import datetime

# Configuration
DB_CONFIG = {
    'host': os.getenv('POSTGRES_HOST', 'postgres'),
    'port': os.getenv('POSTGRES_PORT', '5432'),
    'database': os.getenv('POSTGRES_DB', 'airflow'),
    'user': os.getenv('POSTGRES_USER', 'airflow'),
    'password': os.getenv('POSTGRES_PASSWORD', 'airflow'),
    'schema': os.getenv('POSTGRES_SCHEMA', 'meap')
}

PRICE_RATINGS = {
    'AAA': {'color': '#28a745', 'description': 'Premium pricing'},
    'AA': {'color': '#17a2b8', 'description': 'High-tier pricing'},
    'A': {'color': '#ffc107', 'description': 'Mid-tier pricing'},
    'B': {'color': '#dc3545', 'description': 'Entry-level pricing'}
}

VOLUME_RATINGS = {
    'High Volume': {'color': '#28a745', 'description': 'Strong demand'},
    'Medium Volume': {'color': '#ffc107', 'description': 'Moderate demand'},
    'Standard Volume': {'color': '#17a2b8', 'description': 'Regular demand'}
}

# Update DB_CONFIG with Render PostgreSQL details
DB_CONFIG = {
    'user': 'airflow_3prf_user',
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': 'dpg-cu63up5ds78s73agthn0-a.oregon-postgres.render.com',
    'port': '5432',
    'database': 'airflow_3prf'
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
    def get_recommendations():
        """Fetch product recommendations from view"""
        engine = ProductService.get_db_connection()
        if engine:
            try:
                query = f"""
                SELECT 
                    category,
                    avg_price,
                    total_units,
                    price_rating,
                    volume_rating,
                    price_strategy,
                    volume_strategy,
                    created_at
                FROM {DB_CONFIG['schema']}.vw_product_recommendations
                """
                return pd.read_sql(query, engine)
            except Exception as e:
                st.error(f"Data fetch error: {e}")
                return None
            finally:
                engine.dispose()
        return None

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
    """Main application"""
    st.set_page_config(
        page_title="Product Analysis Dashboard",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS
    st.markdown("""
        <style>
        .metric-card {
            padding: 1rem;
            border-radius: 0.5rem;
            background: #f8f9fa;
            margin: 1rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .metric-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 0.5rem 0;
        }
        .metric-value {
            font-size: 1.8rem;
            font-weight: bold;
        }
        .rating-badge {
            padding: 0.25rem 0.5rem;
            border-radius: 0.25rem;
            color: white;
            font-weight: bold;
        }
        .rating-aaa { background-color: #28a745; }
        .rating-aa { background-color: #17a2b8; }
        .rating-a { background-color: #ffc107; }
        .rating-b { background-color: #dc3545; }
        .rating-high-volume { background-color: #28a745; }
        .rating-medium-volume { background-color: #ffc107; }
        .rating-standard-volume { background-color: #17a2b8; }
        .strategy-text {
            margin-top: 0.5rem;
            font-size: 1.1rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header
    st.title("Product Analysis & Insights")
    st.markdown("Make informed decisions with real-time data")

    # Load data
    df = ProductService.get_recommendations()
    
    if df is not None:
        try:
            # Sidebar filters
            with st.sidebar:
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

            # Apply filters
            filtered_df = df[
                (df['price_rating'].isin(price_filter)) &
                (df['volume_rating'].isin(volume_filter))
            ]

            if filtered_df.empty:
                st.warning("No data matches the selected filters.")
                return

            # Dashboard tabs
            tab1, tab2, tab3 = st.tabs(["📊 Analytics", "🎯 Recommendations", "📈 Trends"])

            with tab1:
                metrics_cols = st.columns(4)
                with metrics_cols[0]:
                    st.metric("Total Categories", len(filtered_df['category'].unique()))
                with metrics_cols[1]:
                    st.metric("Average Price", f"${filtered_df['avg_price'].mean():.2f}")
                with metrics_cols[2]:
                    st.metric("Total Units", f"{filtered_df['total_units'].sum():,}")
                with metrics_cols[3]:
                    st.metric("Last Updated", filtered_df['created_at'].max().strftime('%Y-%m-%d %H:%M'))

                charts = ChartComponent(filtered_df)
                col1, col2 = st.columns(2)
                with col1:
                    st.plotly_chart(charts.create_price_chart(), use_container_width=True)
                with col2:
                    st.plotly_chart(charts.create_volume_chart(), use_container_width=True)

            with tab2:
                st.header("Category Insights")
                selected_category = st.selectbox(
                    "Select Category",
                    options=filtered_df['category'].unique()
                )

                if selected_category:
                    product_data = filtered_df[filtered_df['category'] == selected_category].iloc[0]
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

            with tab3:
                st.header("Rating Distribution")
                col1, col2 = st.columns(2)
                
                with col1:
                    price_dist = filtered_df['price_rating'].value_counts()
                    fig = px.pie(
                        values=price_dist.values,
                        names=price_dist.index,
                        title="Price Rating Distribution",
                        color=price_dist.index,
                        color_discrete_map={k: v['color'] for k, v in PRICE_RATINGS.items()}
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    volume_dist = filtered_df['volume_rating'].value_counts()
                    fig = px.pie(
                        values=volume_dist.values,
                        names=volume_dist.index,
                        title="Volume Rating Distribution",
                        color=volume_dist.index,
                        color_discrete_map={k: v['color'] for k, v in VOLUME_RATINGS.items()}
                    )
                    st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.info("Please refresh the page or contact support if the issue persists.")
    else:
        st.error("Unable to load data. Please check database connection.")

if __name__ == "__main__":
    main()