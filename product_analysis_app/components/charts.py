# components/charts.py
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class ChartComponent:
    def __init__(self, df: pd.DataFrame):
        """Initialize with view-matching colors and data validation"""
        if df is None or df.empty:
            raise ValueError("DataFrame cannot be empty")
            
        required_cols = [
            'category', 'avg_price', 'total_units', 
            'price_rating', 'volume_rating',
            'price_strategy', 'volume_strategy'
        ]
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
            
        self.df = df
        
        # Colors matching view's rating system exactly
        self.price_colors = {
            'AAA': '#007AFF',  # Maintain premium pricing
            'AA': '#5856D6',   # Consider price optimization
            'A': '#FF9500',    # Review pricing strategy
            'B': '#FF3B30'     # Evaluate market position
        }
        
        self.volume_colors = {
            'High Volume': '#34C759',      # Maintain inventory levels
            'Medium Volume': '#FF9F0A',    # Monitor stock levels
            'Standard Volume': '#64D2FF'    # Review stock strategy
        }

    def create_price_chart(self):
        """Price analysis chart matching view's CASE statements"""
        try:
            price_dist = self.df.groupby(['price_rating', 'price_strategy']).size().reset_index(name='count')
            
            fig = px.bar(
                price_dist,
                x='price_rating',
                y='count',
                color='price_rating',
                color_discrete_map=self.price_colors,
                title='Price Rating Distribution',
                labels={
                    'price_rating': 'Price Rating',
                    'count': 'Number of Products'
                },
                custom_data=['price_strategy']
            )
            
            fig.update_traces(
                hovertemplate="<br>".join([
                    "Rating: %{x}",
                    "Products: %{y}",
                    "Strategy: %{customdata[0]}"
                ])
            )
            
            return fig
        except Exception as e:
            print(f"Error creating price chart: {str(e)}")
            return None

    def create_volume_chart(self):
        """Volume analysis chart matching view's CASE statements"""
        try:
            volume_dist = self.df.groupby(['volume_rating', 'volume_strategy']).size().reset_index(name='count')
            
            fig = px.bar(
                volume_dist,
                x='volume_rating',
                y='count',
                color='volume_rating',
                color_discrete_map=self.volume_colors,
                title='Volume Rating Distribution',
                labels={
                    'volume_rating': 'Volume Rating',
                    'count': 'Number of Products'
                },
                custom_data=['volume_strategy']
            )
            
            fig.update_traces(
                hovertemplate="<br>".join([
                    "Rating: %{x}",
                    "Products: %{y}",
                    "Strategy: %{customdata[0]}"
                ])
            )
            
            return fig
        except Exception as e:
            print(f"Error creating volume chart: {str(e)}")
            return None

    def create_performance_matrix(self):
        """Performance matrix combining price and volume strategies"""
        try:
            fig = px.scatter(
                self.df,
                x='avg_price',
                y='total_units',
                color='price_rating',
                symbol='volume_rating',
                color_discrete_map=self.price_colors,
                title='Price-Volume Performance Matrix',
                labels={
                    'avg_price': 'Average Price ($)',
                    'total_units': 'Total Units',
                    'price_rating': 'Price Rating',
                    'volume_rating': 'Volume Rating'
                },
                custom_data=[
                    'category',
                    'price_strategy',
                    'volume_strategy'
                ]
            )
            
            fig.update_traces(
                hovertemplate="<br>".join([
                    "Category: %{customdata[0]}",
                    "Price: $%{x:.2f}",
                    "Units: %{y:,}",
                    "Price Strategy: %{customdata[1]}",
                    "Volume Strategy: %{customdata[2]}"
                ])
            )
            
            return fig
        except Exception as e:
            print(f"Error creating performance matrix: {str(e)}")
            return None

    def create_category_chart(self):
        """Category performance overview matching view structure"""
        try:
            category_stats = self.df.groupby('category').agg({
                'avg_price': 'mean',
                'total_units': 'sum',
                'price_strategy': 'first',
                'volume_strategy': 'first',
                'price_rating': 'first',
                'volume_rating': 'first'
            }).reset_index()
            
            fig = go.Figure()
            
            # Price bars
            fig.add_trace(go.Bar(
                name='Average Price',
                x=category_stats['category'],
                y=category_stats['avg_price'],
                yaxis='y',
                marker_color=[self.price_colors[rating] for rating in category_stats['price_rating']],
                customdata=category_stats[['price_strategy', 'price_rating']],
                hovertemplate="<br>".join([
                    "Category: %{x}",
                    "Avg Price: $%{y:.2f}",
                    "Rating: %{customdata[1]}",
                    "Strategy: %{customdata[0]}"
                ])
            ))
            
            # Volume bars
            fig.add_trace(go.Bar(
                name='Total Units',
                x=category_stats['category'],
                y=category_stats['total_units'],
                yaxis='y2',
                marker_color=[self.volume_colors[rating] for rating in category_stats['volume_rating']],
                customdata=category_stats[['volume_strategy', 'volume_rating']],
                hovertemplate="<br>".join([
                    "Category: %{x}",
                    "Total Units: %{y:,}",
                    "Rating: %{customdata[1]}",
                    "Strategy: %{customdata[0]}"
                ])
            ))
            
            fig.update_layout(
                title='Category Performance Overview',
                yaxis=dict(title='Average Price ($)', side='left'),
                yaxis2=dict(title='Total Units', side='right', overlaying='y'),
                barmode='group'
            )
            
            return fig
        except Exception as e:
            print(f"Error creating category chart: {str(e)}")
            return None