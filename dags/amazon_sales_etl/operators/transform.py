from amazon_sales_etl.utils.validators import DataValidator
from amazon_sales_etl.utils.logger import ETLLogger
import pandas as pd
logger = ETLLogger()

def transform_sales_data(**context) -> str:
    """Enhanced transformation with advanced analytics"""
    logger.logger.info("Starting transformation process...")
    try:
        raw_data = context['task_instance'].xcom_pull(task_ids='extract_sales_data', key='raw_data')
        df = pd.DataFrame(raw_data)
        
        # Clean and transform
        df['selling_price'] = pd.to_numeric(df['selling_price'], errors='coerce')
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
        
        # Remove outliers using IQR
        for col in ['selling_price', 'quantity']:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            df = df[~((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR)))]
        
        # Advanced metrics
        transformed_df = df.groupby('category').agg({
            'selling_price': ['mean', 'median', 'std'],
            'quantity': ['sum', 'mean', 'count']
        }).reset_index()
        
        transformed_df.columns = ['category', 'amount', 'median_price', 'price_std', 
                                'qty', 'avg_qty', 'transaction_count']
        
        # Additional metrics
        transformed_df['price_volatility'] = transformed_df['price_std'] / transformed_df['amount']
        transformed_df['volume_intensity'] = transformed_df['qty'] / transformed_df['transaction_count']
        
        DataValidator.validate_transformations(transformed_df)
        context['task_instance'].xcom_push(key='transformed_data', value=transformed_df.to_dict('records'))
        
        return f"Transformed {len(transformed_df)} categories"
        
    except Exception as e:
        logger.log_error(e, "Transform")
        raise