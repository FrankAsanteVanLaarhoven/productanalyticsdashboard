docker-compose exec postgres psql -U airflow -d airflow -c "
CREATE OR REPLACE VIEW meap.vw_product_ratings AS
SELECT 
    category,
    ROUND(AVG(amount)::numeric, 2) as avg_price,
    SUM(qty) as total_units,
    CASE 
        WHEN AVG(amount) > 60 THEN 'AAA'
        WHEN AVG(amount) > 50 THEN 'AA'
        WHEN AVG(amount) > 40 THEN 'A'
        ELSE 'B'
    END as price_rating,
    CASE 
        WHEN SUM(qty) > 25 THEN 'High Volume'
        WHEN SUM(qty) > 20 THEN 'Medium Volume'
        ELSE 'Standard Volume'
    END as volume_rating
FROM meap.sales_data
GROUP BY category;"