# Activate virtual environment
source .venv/bin/activate

# Load environment variables
export $(cat airflow_project.env | xargs)
export $(cat .env | xargs)

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL..."
until docker-compose exec postgres pg_isready -U airflow; do
    sleep 1
done

# Create schema and views
echo "Creating schema and views..."
docker-compose exec postgres psql -U airflow -d airflow -c "
CREATE SCHEMA IF NOT EXISTS meap;

-- Create product ratings view
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
GROUP BY category;

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

echo "Setup complete!"