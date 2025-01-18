-- Create schema if not exists
CREATE SCHEMA IF NOT EXISTS meap;

-- Create sales table
CREATE TABLE IF NOT EXISTS meap.amazon_sales (
    id SERIAL PRIMARY KEY,
    category VARCHAR(100),
    size VARCHAR(20),
    sale_date DATE,
    status VARCHAR(50),
    fulfillment VARCHAR(100),
    style VARCHAR(100),
    sku VARCHAR(100),
    asin VARCHAR(50),
    courier_status VARCHAR(50),
    quantity INTEGER,
    amount DECIMAL(10,2),
    is_b2b BOOLEAN,
    currency VARCHAR(3),
    amount_usd DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_sales_date ON meap.amazon_sales(sale_date);
CREATE INDEX IF NOT EXISTS idx_sales_category ON meap.amazon_sales(category);
CREATE INDEX IF NOT EXISTS idx_sales_sku ON meap.amazon_sales(sku);

-- Create analytics views
CREATE OR REPLACE VIEW meap.daily_sales AS
SELECT 
    sale_date,
    category,
    COUNT(*) as order_count,
    SUM(quantity) as total_quantity,
    SUM(amount_usd) as total_revenue_usd,
    AVG(amount_usd) as avg_order_value_usd
FROM meap.amazon_sales
GROUP BY sale_date, category;
