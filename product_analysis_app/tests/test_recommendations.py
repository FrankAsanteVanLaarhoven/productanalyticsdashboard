import psycopg2
import pandas as pd

def test_recommendations():
    try:
        # Use exact connection from the quote
        conn = psycopg2.connect(
            host="localhost",
            database="airflow",
            user="airflow",
            password="airflow",
            port="5432"
        )
        
        # First set the schema path
        with conn.cursor() as cursor:
            cursor.execute("SET search_path TO meap, public;")
        
        # Query the view we just created
        query = """
        SELECT * FROM meap.vw_product_recommendations;
        """
        
        df = pd.read_sql(query, conn)
        print(f"Records found: {len(df)}")
        print("\nSample data:")
        print(df[["category", "price_rating", "volume_rating", "price_strategy", "volume_strategy"]])
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_recommendations()
