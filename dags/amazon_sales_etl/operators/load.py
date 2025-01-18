from sqlalchemy import create_engine, text
import pandas as pd
import os
from amazon_sales_etl.utils.logger import ETLLogger
from amazon_sales_etl.utils.validators import DataValidator

logger = ETLLogger()

def load_sales_data(**context) -> str:
    """Load data and create views for product recommendations"""
    engine = None
    try:
        # Get transformed data from previous task
        transformed_data = context['task_instance'].xcom_pull(task_ids='transform_sales_data', key='transformed_data')
        if not transformed_data:
            raise ValueError("No transformed data available for loading")
        
        df = pd.DataFrame(transformed_data)
        logger.logger.info(f"Preparing to load {len(df)} records")
        
        # Create database connection
        engine = create_engine('postgresql://airflow:airflow@postgres/airflow')
        
        with engine.begin() as connection:
            # Create schema and tables using SQL files
            with open('/opt/airflow/sql/create_schema.sql', 'r') as file:
                connection.execute(text(file.read()))
            
            with open('/opt/airflow/sql/create_tables.sql', 'r') as file:
                connection.execute(text(file.read()))
            
            # Load new data
            df.to_sql(
                'sales_data',
                connection,
                schema='meap',
                if_exists='replace',
                index=False,
                method='multi',
                chunksize=1000
            )
            
            # Create views using SQL files
            with open('/opt/airflow/sql/product_ratings.sql', 'r') as file:
                connection.execute(text(file.read()))
            
            with open('/opt/airflow/sql/product_recommendations.sql', 'r') as file:
                connection.execute(text(file.read()))
            
            # Verify data load
            result = connection.execute(text("""
                SELECT 
                    COUNT(*) as record_count,
                    COUNT(DISTINCT category) as category_count,
                    AVG(amount) as avg_price,
                    SUM(qty) as total_quantity
                FROM meap.sales_data
            """))
            stats = result.fetchone()
            
            # Log load statistics
            load_stats = {
                'records_loaded': stats[0],
                'categories': stats[1],
                'average_price': round(stats[2], 2),
                'total_quantity': stats[3]
            }
            logger.log_stats(load_stats, "Data Load")
            
        return f"Successfully loaded {stats[0]} records across {stats[1]} categories"
    
    except Exception as e:
        logger.log_error(e, "Load")
        raise
    finally:
        if engine:
            engine.dispose()