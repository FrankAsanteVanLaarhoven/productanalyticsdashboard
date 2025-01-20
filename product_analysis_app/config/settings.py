# product_analysis_app/config/settings.py
from sqlalchemy import create_engine
import os

DB_CONFIG = {
    'user': 'airflow_3prf_user',
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': 'dpg-cu63up5ds78s73agthn0-a.oregon-postgres.render.com',
    'port': '5432',
    'database': 'airflow_3prf',
    'schema': 'meap'
}

def get_database_engine():
    try:
        connection_string = (
            f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
            f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
        )
        
        engine = create_engine(
            connection_string,
            connect_args={
                'options': f"-c search_path={DB_CONFIG['schema']}",
                'sslmode': 'require'  # Required for Render
            }
        )
        
        # Verify connection and schema
        with engine.connect() as conn:
            conn.execute("SELECT 1 FROM meap.vw_product_recommendations LIMIT 1")
            
        return engine
    except Exception as e:
        print(f"Database connection error: {str(e)}")
        raise