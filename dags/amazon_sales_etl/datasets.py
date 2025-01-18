from airflow.datasets import Dataset

# Define datasets for each stage
SALES_RAW_DATA = Dataset("s3://meap/sales/raw/amazon_sales.csv")
SALES_TRANSFORMED_DATA = Dataset("s3://meap/sales/transformed/amazon_sales.parquet")
PRODUCT_RECOMMENDATIONS = Dataset("postgresql://meap/views/product_recommendations")