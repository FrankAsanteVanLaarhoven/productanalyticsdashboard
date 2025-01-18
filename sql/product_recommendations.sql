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
