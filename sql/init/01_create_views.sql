CREATE SCHEMA IF NOT EXISTS meap;

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
FROM meap.vw_product_ratings p;