CREATE OR REPLACE VIEW meap.vw_product_ratings AS
SELECT 
    category,
    amount as avg_price,
    qty as total_units,
    CASE 
        WHEN amount >= 70 THEN 'AAA'
        WHEN amount >= 60 THEN 'AA'
        WHEN amount >= 50 THEN 'A'
        ELSE 'B'
    END as price_rating,
    CASE 
        WHEN qty >= 30 THEN 'High Volume'
        WHEN qty >= 25 THEN 'Medium Volume'
        ELSE 'Standard Volume'
    END as volume_rating
FROM meap.sales_data;
