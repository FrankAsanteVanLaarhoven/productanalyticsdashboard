-- Create schema if it doesn't exist
CREATE SCHEMA IF NOT EXISTS meap;

-- Create sales_data table if needed
CREATE TABLE IF NOT EXISTS meap.sales_data (
    id SERIAL PRIMARY KEY,
    category VARCHAR(50),
    amount NUMERIC(10,2),
    qty INTEGER,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);