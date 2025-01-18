# components/metrics.py
import streamlit as st

class MetricsComponent:
    def display_metrics(self, product_data):
        """Display both price and volume metrics"""
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
                <div class='metric-card'>
                    <h3>Price Analysis</h3>
                    <div class='metric-header'>
                        <h2>${product_data['avg_price']:,.2f}</h2>
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
                    <h3>Volume Analysis</h3>
                    <div class='metric-header'>
                        <h2>{int(product_data['total_units']):,}</h2>
                        <span class="rating-badge rating-{product_data['volume_rating'].lower().replace(' ', '-')}">
                            {product_data['volume_rating']}
                        </span>
                    </div>
                    <p class="strategy-text">📦 {product_data['volume_strategy']}</p>
                </div>
            """, unsafe_allow_html=True)