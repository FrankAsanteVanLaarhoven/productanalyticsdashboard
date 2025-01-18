# components/recommendations.py
import streamlit as st

class RecommendationComponent:
    """Component for displaying product recommendations"""
    
    def __init__(self, product_data):
        self.data = product_data
    
    def display_price_strategy(self):
        return f"""
            <div class='metric-card'>
                <h3>Price Strategy</h3>
                <div class='metric-header'>
                    <h2>${self.data['avg_price']:,.2f}</h2>
                    <span class="rating-badge rating-{self.data['price_rating'].lower()}">
                        {self.data['price_rating']}
                    </span>
                </div>
                <div class='strategy-box'>
                    <p class="strategy-text">💡 {self.data['price_strategy']}</p>
                </div>
            </div>
        """
    
    def display_volume_strategy(self):
        return f"""
            <div class='metric-card'>
                <h3>Volume Strategy</h3>
                <div class='metric-header'>
                    <h2>{int(self.data['total_units']):,}</h2>
                    <span class="rating-badge rating-{self.data['volume_rating'].lower().replace(' ', '-')}">
                        {self.data['volume_rating']}
                    </span>
                </div>
                <div class='strategy-box'>
                    <p class="strategy-text">📦 {self.data['volume_strategy']}</p>
                </div>
            </div>
        """