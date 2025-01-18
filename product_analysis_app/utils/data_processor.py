import pandas as pd

class DataProcessor:
    @staticmethod
    def process_recommendations(df: pd.DataFrame) -> pd.DataFrame:
        """Process raw recommendations data"""
        df = df.copy()
        df['price_rating_order'] = df['price_rating'].map({
            'AAA': 1, 'AA': 2, 'A': 3, 'B': 4
        })
        df['volume_rating_order'] = df['volume_rating'].map({
            'High Volume': 1, 'Medium Volume': 2, 'Standard Volume': 3
        })
        return df.sort_values(['price_rating_order', 'volume_rating_order'])