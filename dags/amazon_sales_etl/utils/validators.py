import pandas as pd
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class DataValidator:
    @staticmethod
    def validate_data(df: pd.DataFrame, required_columns: List[str]) -> bool:
        """Enhanced data validation with detailed checks"""
        # Basic validation
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        if df.empty:
            raise ValueError("Dataframe is empty")
        
        # Data quality checks
        null_counts = df[required_columns].isnull().sum()
        if null_counts.any():
            logger.warning(f"Null values found in columns: {null_counts[null_counts > 0]}")
        
        # Data type validation
        numeric_cols = ['selling_price', 'quantity']
        for col in numeric_cols:
            if col in df.columns and not pd.api.types.is_numeric_dtype(df[col]):
                logger.warning(f"Column {col} is not numeric type")
        
        return True

    @staticmethod
    def validate_transformations(df: pd.DataFrame) -> bool:
        """Validate transformed data"""
        required_metrics = ['amount', 'qty', 'price_volatility', 'volume_intensity']
        if df[required_metrics].isnull().any().any():
            raise ValueError("Transformed data contains null values")
        return True