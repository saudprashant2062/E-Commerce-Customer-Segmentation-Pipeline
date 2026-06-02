WITH cleaned_transactions AS (
    SELECT
        customer_id,
        invoice_no,
        CAST(invoice_date AS DATE) AS invoice_date,
        quantity,
        unit_price,
        quantity * unit_price AS total_price
    FROM transactions
    WHERE customer_id IS NOT NULL
      AND invoice_no IS NOT NULL
      AND invoice_date IS NOT NULL
      AND quantity > 0
      AND unit_price > 0
      AND invoice_no NOT LIKE 'C%'
),
reference_date AS (
    SELECT DATEADD(DAY, 1, MAX(invoice_date)) AS ref_date
    FROM cleaned_transactions
),
rfm AS (
    SELECT
        ct.customer_id,
        DATEDIFF(DAY, MAX(ct.invoice_date), rd.ref_date) AS recency,
        COUNT(DISTINCT ct.invoice_no) AS frequency,
        SUM(ct.total_price) AS monetary
    FROM cleaned_transactions ct
    CROSS JOIN reference_date rd
    GROUP BY ct.customer_id, rd.ref_date
)
SELECT *
FROM rfm
ORDER BY monetary DESC;
