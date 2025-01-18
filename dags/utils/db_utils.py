from sqlalchemy import create_engine
import pandas as pd

def get_postgres_conn():
    """Get PostgreSQL connection"""
    return create_engine('postgresql://airflow:airflow@postgres/airflow')

def execute_sql(sql, conn=None):
    """Execute SQL query"""
    if conn is None:
        conn = get_postgres_conn()
    return pd.read_sql(sql, conn)
