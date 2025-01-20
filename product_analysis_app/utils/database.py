# utils/database.py
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import psycopg2
import pandas as pd
import os

def get_db_params():
    """Get database parameters based on environment"""
    if os.getenv('RENDER'):  # If running on Render
        return {
            "host": "dpg-cu63up5ds78s73agthn0-a.oregon-postgres.render.com",
            "database": "airflow_3prf",
            "user": "airflow_3prf_user",
            "password": os.getenv('POSTGRES_PASSWORD'),
            "sslmode": "require"
        }
    else:  # Local Docker environment - matches the quote
        return {
            "host": "postgres",
            "database": "airflow",
            "user": "airflow",
            "password": "airflow",
            "port": "5432"
        }

def get_postgres_connection():
    """Get direct psycopg2 connection"""
    try:
        conn = psycopg2.connect(**get_db_params())
        with conn.cursor() as cursor:
            cursor.execute("SET search_path TO meap, public;")
        return conn
    except Exception as e:
        print(f"Connection error: {str(e)}")
        raise e