# utils/database.py
class DatabaseService:
    @staticmethod
    @st.cache_data(ttl=300)
    def get_product_recommendations() -> pd.DataFrame:
        """Fetch data from the product recommendations view"""
        try:
            conn = get_database_connection()
            query = """
            SELECT *
            FROM meap.vw_product_recommendations
            ORDER BY 
                CASE price_rating
                    WHEN 'AAA' THEN 1
                    WHEN 'AA' THEN 2
                    WHEN 'A' THEN 3
                    ELSE 4
                END,
                category;
            """
            return pd.read_sql_query(query, conn)
        except Exception as e:
            st.error(f"Failed to fetch recommendations: {e}")
            return None
