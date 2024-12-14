CREATE VIEW customer_summary AS
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    MAX(t.transaction_date) AS last_transaction_date,
    COUNT(t.transaction_id) AS total_transactions,
    SUM(t.amount) AS total_spent,
    AVG(t.amount) AS avg_transaction_amount,
    EXTRACT(DAY FROM '2021-12-31' - MAX(t.transaction_date)) AS recency,
    CASE 
        WHEN EXTRACT(DAY FROM '2021-12-31' - MAX(t.transaction_date)) > 180 THEN TRUE
        ELSE FALSE
    END AS churn_flag
FROM
    customers c
LEFT JOIN
    transactions t ON c.customer_id = t.customer_id
GROUP BY
    c.customer_id, c.first_name, c.last_name;
