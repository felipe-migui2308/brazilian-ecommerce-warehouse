-- ==========================================
-- BRAZILIAN E-COMMERCE DATA WAREHOUSE
-- CONSULTAS ANALÍTICAS
-- ==========================================


-- 1. VALOR TOTAL DOS PRODUTOS VENDIDOS

SELECT
    ROUND(SUM(price), 2) AS total_sales_value,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(*) AS total_items
FROM fact_sales;


-- 2. EVOLUÇÃO MENSAL DAS VENDAS

SELECT
    d.year,
    d.month,
    COUNT(DISTINCT f.order_id) AS total_orders,
    ROUND(SUM(f.price), 2) AS sales_value
FROM fact_sales f
JOIN dim_dates d
    ON f.purchase_date = d.date
GROUP BY
    d.year,
    d.month
ORDER BY
    d.year,
    d.month;


-- 3. TOP 10 CATEGORIAS POR VALOR VENDIDO

SELECT
    p.category,
    COUNT(*) AS items_sold,
    ROUND(SUM(f.price), 2) AS sales_value
FROM fact_sales f
JOIN dim_products p
    ON f.product_id = p.product_id
GROUP BY
    p.category
ORDER BY
    sales_value DESC
LIMIT 10;


-- 4. TOP 10 ESTADOS POR VALOR VENDIDO

SELECT
    c.customer_state,
    COUNT(DISTINCT f.order_id) AS total_orders,
    ROUND(SUM(f.price), 2) AS sales_value
FROM fact_sales f
JOIN dim_customers c
    ON f.customer_id = c.customer_id
GROUP BY
    c.customer_state
ORDER BY
    sales_value DESC
LIMIT 10;


-- 5. TICKET MÉDIO POR PEDIDO

WITH order_totals AS (
    SELECT
        order_id,
        SUM(price) AS order_value
    FROM fact_sales
    GROUP BY order_id
)

SELECT
    ROUND(AVG(order_value), 2) AS average_order_value
FROM order_totals;