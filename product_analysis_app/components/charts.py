# /app/product_analysis_app/components/charts.py
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class ChartComponent:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        # Colors matching the view's rating system
        self.price_colors = {
            'AAA': '#28a745',  # Maintain premium pricing
            'AA': '#17a2b8',   # Consider price optimization
            'A': '#ffc107',    # Review pricing strategy
            'B': '#dc3545'     # Evaluate market position
        }
        self.volume_colors = {
            'High Volume': '#28a745',      # Maintain inventory levels
            'Medium Volume': '#ffc107',    # Monitor stock levels
            'Standard Volume': '#17a2b8'   # Review stock strategy
        }

    def create_price_chart(self):
        """Price analysis chart showing ratings and strategies"""
        fig = px.bar(
            self.df,
            x='category',
            y='avg_price',
            color='price_rating',
            color_discrete_map=self.price_colors,
            title='Price Analysis by Category',
            labels={
                'category': 'Category',
                'avg_price': 'Average Price ($)',
                'price_rating': 'Price Rating'
            },
            custom_data=['price_strategy']
        )
        fig.update_traces(
            hovertemplate="<br>".join([
                "Category: %{x}",
                "Price: $%{y:.2f}",
                "Strategy: %{customdata[0]}"
            ])
        )
        return fig

    def create_category_chart(self):  # Added this method
        """Category performance overview"""
        df_category = self.df.groupby('category').agg({
            'avg_price': 'mean',
            'total_units': 'sum',
            'price_strategy': 'first',
            'volume_strategy': 'first'
        }).reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Average Price',
            x=df_category['category'],
            y=df_category['avg_price'],
            customdata=df_category[['price_strategy']],
            hovertemplate="<br>".join([
                "Category: %{x}",
                "Avg Price: $%{y:.2f}",
                "Strategy: %{customdata[0]}"
            ])
        ))
        return fig

    def create_volume_chart(self):
        """Volume analysis chart"""
        fig = px.bar(
            self.df,
            x='category',
            y='total_units',
            color='volume_rating',
            color_discrete_map=self.volume_colors,
            title='Volume Analysis by Category',
            custom_data=['volume_strategy']
        )
        fig.update_traces(
            hovertemplate="<br>".join([
                "Category: %{x}",
                "Units: %{y:,}",
                "Strategy: %{customdata[0]}"
            ])
        )
        return fig

    def create_performance_matrix(self):
        """Performance matrix combining price and volume ratings"""
        fig = px.scatter(
            self.df,
            x='avg_price',
            y='total_units',
            color='price_rating',
            color_discrete_map=self.price_colors,
            hover_data=['category', 'price_strategy', 'volume_strategy'],
            title='Price-Volume Performance Matrix'
        )
        return fig