#!/bin/bash

echo "Setting up product recommendation views..."

# Create product ratings view
docker-compose exec postgres psql -U airflow -d airflow -c "
CREATE OR REPLACE VIEW meap.vw_product_ratings AS
SELECT 
    category,
    avg_price,
    total_units,
    CASE 
        WHEN avg_price >= 75 THEN 'AAA'
        WHEN avg_price >= 55 THEN 'AA'
        WHEN avg_price >= 35 THEN 'A'
        ELSE 'B'
    END as price_rating,
    CASE 
        WHEN total_units >= 30 THEN 'High Volume'
        WHEN total_units >= 22 THEN 'Medium Volume'
        ELSE 'Standard Volume'
    END as volume_rating,
    created_at
FROM meap.product_metrics;"

# Create product recommendations view
docker-compose exec postgres psql -U airflow -d airflow -c "
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

echo "Views created successfully!"

# Verify views were created
docker-compose exec postgres psql -U airflow -d airflow -c "\dv meap.*"

# Show sample data
docker-compose exec postgres psql -U airflow -d airflow -c "
SELECT * FROM meap.vw_product_recommendations LIMIT 5;"
