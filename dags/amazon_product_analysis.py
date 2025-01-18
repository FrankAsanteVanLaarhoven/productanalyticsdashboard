# /Users/frankvanlaarhoven/airflow_project/dags/amazon_product_analysis.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.datasets import Dataset
from datetime import datetime
import pandas as pd

# Define dataset dependency
PRODUCT_RECOMMENDATIONS = Dataset("meap/product_recommendations")

def analyze_recommendations(**context):
    """Analyze product recommendations and generate insights"""
    try:
        # Connect to database
        pg_hook = PostgresHook(postgres_conn_id='postgres_default')
        
        # Get recommendations data
        recommendations_df = pg_hook.get_pandas_df("""
            SELECT 
                category,
                avg_price,
                total_units,
                price_rating,
                price_strategy,
                volume_rating, 
                volume_strategy
            FROM meap.vw_product_recommendations
            ORDER BY avg_price DESC
        """)
        
        # Generate price rating analysis
        price_analysis = recommendations_df.groupby(['price_rating', 'price_strategy']).agg({
            'category': 'count',
            'avg_price': 'mean',
            'total_units': 'sum'
        }).round(2)
        
        # Generate volume rating analysis
        volume_analysis = recommendations_df.groupby(['volume_rating', 'volume_strategy']).agg({
            'category': 'count',
            'avg_price': 'mean',
            'total_units': 'sum'
        }).round(2)
        
        # Generate category insights
        category_insights = recommendations_df.groupby('category').agg({
            'avg_price': ['mean', 'min', 'max'],
            'total_units': 'sum',
            'price_strategy': lambda x: x.mode()[0],
            'volume_strategy': lambda x: x.mode()[0]
        }).round(2)
        
        # Store analysis results
        analysis_results = {
            'price_analysis': price_analysis.to_dict(),
            'volume_analysis': volume_analysis.to_dict(),
            'category_insights': category_insights.to_dict(),
            'total_products': len(recommendations_df),
            'total_categories': recommendations_df['category'].nunique(),
            'avg_price_overall': recommendations_df['avg_price'].mean(),
            'total_units_overall': recommendations_df['total_units'].sum()
        }
        
        # Push results to XCom
        context['task_instance'].xcom_push(
            key='recommendations_analysis',
            value=analysis_results
        )
        
        return "Analysis completed successfully"
        
    except Exception as e:
        print(f"Error analyzing recommendations: {str(e)}")
        raise

# DAG definition
with DAG(
    'amazon_product_analysis',
    schedule=[PRODUCT_RECOMMENDATIONS],  # This DAG runs when recommendations are updated
    start_date=datetime(2024, 1, 1),
    catchup=False,
    description='Analyze product recommendations and generate insights',
    tags=['amazon', 'analysis', 'recommendations']
) as dag:

    analyze_task = PythonOperator(
        task_id='analyze_recommendations',
        python_callable=analyze_recommendations,
        provide_context=True
    )

    # Task dependencies (single task for now)
    analyze_task