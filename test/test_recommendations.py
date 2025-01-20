# tests/test_recommendations.py
conn = psycopg2.connect(
    host="host.docker.internal",  # Special Docker DNS name
    database="airflow",
    user="airflow",
    password="airflow",
    port="5432"
)

