import os

APP_CONFIG = {
    "page_title": "Product Analysis Dashboard",
    "page_icon": "📊",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

DB_CONFIG = {
    'user': os.getenv('POSTGRES_USER', 'airflow_3prf_user'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.getenv('POSTGRES_HOST', 'dpg-cu63up5ds78s73agthn0-a.oregon-postgres.render.com'),
    'port': os.getenv('POSTGRES_PORT', '5432'),
    'database': os.getenv('POSTGRES_DB', 'airflow_3prf')
}