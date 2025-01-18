# product_analysis_app/services/database.py
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_postgres_connection():
    """Create a connection to the PostgreSQL database"""
    try:
        connection = psycopg2.connect(
            host="postgres",
            database="airflow",
            user="airflow",
            password="airflow"
        )
        return connection
    except Exception as e:
        raise Exception(f"Error connecting to database: {str(e)}")