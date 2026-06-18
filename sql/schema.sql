-- ============================================================================
-- Retail Sales Analytics - Schema + Load Script (PostgreSQL)
-- ============================================================================
-- Run order:
--   1. Run schema.sql to create the table
--   2. Run load_data.sql to import the cleaned CSV
--   3. Run analysis_queries.sql to perform analysis
-- ============================================================================

-- 1. Drop table if it exists (for re-runs)
DROP TABLE IF EXISTS superstore;

-- 2. Create the table
CREATE TABLE superstore (
    row_id          INTEGER PRIMARY KEY,
    order_id        VARCHAR(20) NOT NULL,
    order_date      DATE NOT NULL,
    ship_date       DATE NOT NULL,
    ship_mode       VARCHAR(50),
    customer_id     VARCHAR(20),
    customer_name   VARCHAR(100),
    segment         VARCHAR(50),
    country         VARCHAR(50),
    city            VARCHAR(100),
    state           VARCHAR(50),
    postal_code     INTEGER,
    region          VARCHAR(20),
    product_id      VARCHAR(20),
    category        VARCHAR(50),
    sub_category    VARCHAR(50),
    product_name    VARCHAR(255),
    sales           NUMERIC(10,2),
    quantity        INTEGER,
    discount        NUMERIC(4,2),
    profit          NUMERIC(10,2),
    -- Derived columns (populated in step 3 for performance)
    order_year      INTEGER,
    order_month     INTEGER,
    order_quarter   INTEGER,
    order_year_month VARCHAR(10),
    ship_days       INTEGER,
    profit_margin   NUMERIC(6,2)
);

-- 3. Create indexes on commonly filtered columns
CREATE INDEX idx_order_date ON superstore(order_date);
CREATE INDEX idx_region ON superstore(region);
CREATE INDEX idx_category ON superstore(category);
CREATE INDEX idx_segment ON superstore(segment);
CREATE INDEX idx_customer ON superstore(customer_name);
CREATE INDEX idx_year_month ON superstore(order_year_month);

-- 4. Load data using COPY (fastest method)
--    Make sure superstore_clean.csv is in the same directory you're running psql from.
COPY superstore(
    row_id, order_id, order_date, ship_date, ship_mode,
    customer_id, customer_name, segment, country, city, state,
    postal_code, region, product_id, category, sub_category, product_name,
    sales, quantity, discount, profit
)
FROM 'superstore_clean.csv'
DELIMITER ','
CSV HEADER
ENCODING 'UTF8';

-- 5. Populate derived columns
UPDATE superstore
SET order_year      = EXTRACT(YEAR FROM order_date),
    order_month     = EXTRACT(MONTH FROM order_date),
    order_quarter   = EXTRACT(QUARTER FROM order_date),
    order_year_month = TO_CHAR(order_date, 'YYYY-MM'),
    ship_days       = (ship_date - order_date),
    profit_margin   = ROUND((profit / NULLIF(sales, 0) * 100)::numeric, 2);

-- 6. Verify load
SELECT
    COUNT(*) AS total_rows,
    MIN(order_date) AS earliest_order,
    MAX(order_date) AS latest_order,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit
FROM superstore;