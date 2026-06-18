-- ============================================================================
-- Retail Sales Analytics - SQL Analysis Queries
-- ============================================================================
-- Compatible with: PostgreSQL, MySQL (minor syntax tweaks), SQLite
-- Assumes table name: superstore
-- All currency columns: numeric(10,2)
-- ============================================================================

-- 1. EXECUTIVE KPI SUMMARY -----------------------------------------------
-- Total Revenue, Profit, Orders, Customers, AOV, Profit Margin
SELECT
    ROUND(SUM(sales), 2)                              AS total_revenue,
    ROUND(SUM(profit), 2)                             AS total_profit,
    ROUND(SUM(profit) / NULLIF(SUM(sales), 0) * 100, 2)
                                                      AS profit_margin_pct,
    COUNT(DISTINCT row_id)                            AS total_orders,
    COUNT(DISTINCT customer_name)                     AS total_customers,
    COUNT(DISTINCT product_name)                      AS total_products,
    ROUND(SUM(sales) / NULLIF(COUNT(DISTINCT row_id), 0), 2)
                                                      AS avg_order_value
FROM superstore;


-- 2. MONTHLY REVENUE & PROFIT TREND -------------------------------------
-- Used for time-series chart and forecasting
SELECT
    order_year_month,
    ROUND(SUM(sales), 2)  AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    COUNT(*)              AS orders
FROM superstore
GROUP BY order_year_month
ORDER BY order_year_month;


-- 3. YEARLY PERFORMANCE -------------------------------------------------
SELECT
    order_year,
    ROUND(SUM(sales), 2)                             AS revenue,
    ROUND(SUM(profit), 2)                            AS profit,
    ROUND(SUM(profit) / NULLIF(SUM(sales), 0) * 100, 2)
                                                     AS profit_margin_pct,
    COUNT(DISTINCT customer_name)                    AS customers
FROM superstore
GROUP BY order_year
ORDER BY order_year;


-- 4. REVENUE BY REGION ---------------------------------------------------
SELECT
    region,
    ROUND(SUM(sales), 2)                             AS revenue,
    ROUND(SUM(profit), 2)                            AS profit,
    ROUND(SUM(profit) / NULLIF(SUM(sales), 0) * 100, 2)
                                                     AS profit_margin_pct,
    COUNT(*)                                         AS orders,
    RANK() OVER (ORDER BY SUM(sales) DESC)           AS revenue_rank
FROM superstore
GROUP BY region
ORDER BY revenue DESC;


-- 5. CATEGORY-WISE PERFORMANCE -------------------------------------------
SELECT
    category,
    ROUND(SUM(sales), 2)                             AS revenue,
    ROUND(SUM(profit), 2)                            AS profit,
    ROUND(SUM(profit) / NULLIF(SUM(sales), 0) * 100, 2)
                                                     AS profit_margin_pct,
    COUNT(DISTINCT product_name)                     AS product_count
FROM superstore
GROUP BY category
ORDER BY revenue DESC;


-- 6. SUB-CATEGORY PERFORMANCE -------------------------------------------
-- Drill-down for category
SELECT
    category,
    sub_category,
    ROUND(SUM(sales), 2)                             AS revenue,
    ROUND(SUM(profit), 2)                            AS profit,
    ROUND(SUM(profit) / NULLIF(SUM(sales), 0) * 100, 2)
                                                     AS profit_margin_pct
FROM superstore
GROUP BY category, sub_category
ORDER BY category, revenue DESC;


-- 7. CUSTOMER SEGMENT ANALYSIS ------------------------------------------
SELECT
    segment,
    COUNT(DISTINCT customer_name)                     AS customers,
    ROUND(SUM(sales), 2)                             AS revenue,
    ROUND(SUM(profit), 2)                            AS profit,
    ROUND(SUM(sales) / NULLIF(COUNT(DISTINCT customer_name), 0), 2)
                                                      AS revenue_per_customer
FROM superstore
GROUP BY segment
ORDER BY revenue DESC;


-- 8. TOP 10 PRODUCTS BY REVENUE -----------------------------------------
SELECT
    product_name,
    category,
    sub_category,
    ROUND(SUM(sales), 2)                             AS revenue,
    ROUND(SUM(profit), 2)                            AS profit,
    SUM(quantity)                                    AS units_sold
FROM superstore
GROUP BY product_name, category, sub_category
ORDER BY revenue DESC
LIMIT 10;


-- 9. TOP 10 PRODUCTS BY PROFIT ------------------------------------------
SELECT
    product_name,
    category,
    ROUND(SUM(profit), 2)                            AS profit,
    SUM(quantity)                                    AS units_sold
FROM superstore
GROUP BY product_name, category
ORDER BY profit DESC
LIMIT 10;


-- 10. BOTTOM 10 PRODUCTS (LOSS-MAKING) ---------------------------------
SELECT
    product_name,
    category,
    ROUND(SUM(profit), 2)                            AS total_loss,
    SUM(quantity)                                    AS units_sold
FROM superstore
GROUP BY product_name, category
HAVING SUM(profit) < 0
ORDER BY total_loss ASC
LIMIT 10;


-- 11. DISCOUNT IMPACT ON PROFIT -----------------------------------------
-- Higher discount tiers often correlate with lower/negative profit
SELECT
    CASE
        WHEN discount = 0     THEN 'No Discount'
        WHEN discount <= 0.2   THEN '1-20%'
        WHEN discount <= 0.4   THEN '21-40%'
        WHEN discount <= 0.6   THEN '41-60%'
        ELSE                       '60%+'
    END                                            AS discount_bucket,
    COUNT(*)                                       AS orders,
    ROUND(SUM(sales), 2)                           AS revenue,
    ROUND(SUM(profit), 2)                          AS profit,
    ROUND(SUM(profit) / NULLIF(SUM(sales), 0) * 100, 2)
                                                    AS profit_margin_pct
FROM superstore
GROUP BY discount_bucket
ORDER BY discount_bucket;


-- 12. TOP 10 CUSTOMERS BY REVENUE ---------------------------------------
SELECT
    customer_name,
    segment,
    region,
    ROUND(SUM(sales), 2)                             AS total_spend,
    ROUND(SUM(profit), 2)                            AS total_profit,
    COUNT(DISTINCT row_id)                          AS orders
FROM superstore
GROUP BY customer_name, segment, region
ORDER BY total_spend DESC
LIMIT 10;


-- 13. SHIPPING MODE PERFORMANCE ----------------------------------------
SELECT
    ship_mode,
    COUNT(*)                                        AS orders,
    ROUND(SUM(sales), 2)                            AS revenue,
    ROUND(AVG(ship_days), 1)                        AS avg_ship_days
FROM superstore
GROUP BY ship_mode
ORDER BY orders DESC;


-- 14. SEASONALITY - QUARTERLY SALES ------------------------------------
SELECT
    order_year,
    order_quarter,
    ROUND(SUM(sales), 2)                             AS revenue,
    ROUND(SUM(profit), 2)                            AS profit
FROM superstore
GROUP BY order_year, order_quarter
ORDER BY order_year, order_quarter;


-- 15. STATE-WISE REVENUE (Geo map data) --------------------------------
SELECT
    state,
    region,
    ROUND(SUM(sales), 2)                             AS revenue,
    ROUND(SUM(profit), 2)                            AS profit,
    COUNT(DISTINCT customer_name)                    AS customers
FROM superstore
GROUP BY state, region
ORDER BY revenue DESC
LIMIT 20;


-- 16. WINDOW FUNCTION - MONTHLY GROWTH % -------------------------------
WITH monthly AS (
    SELECT
        order_year_month,
        ROUND(SUM(sales), 2) AS revenue
    FROM superstore
    GROUP BY order_year_month
)
SELECT
    order_year_month,
    revenue,
    LAG(revenue) OVER (ORDER BY order_year_month) AS prev_revenue,
    ROUND(
        (revenue - LAG(revenue) OVER (ORDER BY order_year_month))
        / NULLIF(LAG(revenue) OVER (ORDER BY order_year_month), 0) * 100,
    2) AS mom_growth_pct
FROM monthly
ORDER BY order_year_month;


-- 17. CTE - CATEGORY CONTRIBUTION % ------------------------------------
WITH cat_rev AS (
    SELECT
        category,
        SUM(sales) AS revenue
    FROM superstore
    GROUP BY category
)
SELECT
    category,
    ROUND(revenue, 2)                                AS revenue,
    ROUND(revenue / SUM(revenue) OVER () * 100, 2)   AS pct_of_total
FROM cat_rev
ORDER BY revenue DESC;


-- ============================================================================
-- END OF QUERIES
-- ============================================================================