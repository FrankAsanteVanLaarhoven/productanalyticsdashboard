#!/bin/bash

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL..."
while ! pg_isready -h postgres -p 5432 -U airflow; do
    sleep 1
done

# Create schema and views in order matching our view dependencies
echo "Creating schema and views..."
psql -h postgres -U airflow -d airflow -c "
    -- Create schema if not exists
    CREATE SCHEMA IF NOT EXISTS meap;

    -- Create product ratings view
    CREATE OR REPLACE VIEW meap.vw_product_ratings AS
    SELECT 
        category,
        avg_price,
        total_units,
        price_rating,
        volume_rating
    FROM meap.product_metrics;

    -- Create product recommendations view
    CREATE OR REPLACE VIEW meap.vw_product_recommendations AS
    SELECT 
        p.*,
        CASE price_rating
            WHEN 'AAA' THEN 'Maintain premium pricing'
            WHEN 'AA' THEN 'Consider price optimization'
            WHEN 'A' THEN 'Review pricing strategy'
            ELSE 'Evaluate market position'
        END as price_strategy,
        CASE volume_rating
            WHEN 'High Volume' THEN 'Maintain inventory levels'
            WHEN 'Medium Volume' THEN 'Monitor stock levels'
            ELSE 'Review stock strategy'
        END as volume_strategy
    FROM meap.vw_product_ratings p;"

# Start Streamlit
echo "Starting Streamlit..."
streamlit run app.py --server.port=8501 --server.address=0.0.0.0