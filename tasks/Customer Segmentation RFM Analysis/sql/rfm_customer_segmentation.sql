-- RFM customer segmentation analysis
-- Replace `your_project.your_dataset.rfm` with the real table path.
-- Expected fields: CustomerID, InvoiceNo, InvoiceDate, Quantity, UnitPrice.

WITH cleaned_transactions AS (
  SELECT
    CustomerID AS customer_id,
    InvoiceNo AS invoice_no,
    DATE(InvoiceDate) AS invoice_date,
    Quantity AS quantity,
    UnitPrice AS unit_price,
    Quantity * UnitPrice AS revenue
  FROM `your_project.your_dataset.rfm`
  WHERE CustomerID IS NOT NULL
    AND DATE(InvoiceDate) >= DATE '2010-12-01'
    AND DATE(InvoiceDate) < DATE '2011-12-01'
    AND Quantity > 0
    AND UnitPrice > 0
),

rfm_values AS (
  SELECT
    customer_id,
    DATE_DIFF(DATE '2011-12-01', MAX(invoice_date), DAY) AS recency_days,
    COUNT(DISTINCT invoice_no) AS frequency,
    ROUND(SUM(revenue), 2) AS monetary_value
  FROM cleaned_transactions
  GROUP BY customer_id
),

rfm_quantiles AS (
  SELECT
    APPROX_QUANTILES(recency_days, 4) AS recency_quantiles,
    APPROX_QUANTILES(frequency, 4) AS frequency_quantiles,
    APPROX_QUANTILES(monetary_value, 4) AS monetary_quantiles
  FROM rfm_values
),

rfm_scores AS (
  SELECT
    rfm_values.customer_id,
    rfm_values.recency_days,
    rfm_values.frequency,
    rfm_values.monetary_value,
    CASE
      WHEN rfm_values.recency_days <= rfm_quantiles.recency_quantiles[OFFSET(1)] THEN 4
      WHEN rfm_values.recency_days <= rfm_quantiles.recency_quantiles[OFFSET(2)] THEN 3
      WHEN rfm_values.recency_days <= rfm_quantiles.recency_quantiles[OFFSET(3)] THEN 2
      ELSE 1
    END AS r_score,
    CASE
      WHEN rfm_values.frequency <= rfm_quantiles.frequency_quantiles[OFFSET(1)] THEN 1
      WHEN rfm_values.frequency <= rfm_quantiles.frequency_quantiles[OFFSET(2)] THEN 2
      WHEN rfm_values.frequency <= rfm_quantiles.frequency_quantiles[OFFSET(3)] THEN 3
      ELSE 4
    END AS f_score,
    CASE
      WHEN rfm_values.monetary_value <= rfm_quantiles.monetary_quantiles[OFFSET(1)] THEN 1
      WHEN rfm_values.monetary_value <= rfm_quantiles.monetary_quantiles[OFFSET(2)] THEN 2
      WHEN rfm_values.monetary_value <= rfm_quantiles.monetary_quantiles[OFFSET(3)] THEN 3
      ELSE 4
    END AS m_score
  FROM rfm_values
  CROSS JOIN rfm_quantiles
),

segmented_customers AS (
  SELECT
    customer_id,
    recency_days,
    frequency,
    monetary_value,
    r_score,
    f_score,
    m_score,
    ROUND((r_score + f_score + m_score) / 3, 2) AS average_rfm_score,
    CONCAT(CAST(r_score AS STRING), CAST(f_score AS STRING), CAST(m_score AS STRING)) AS rfm_score,
    CASE
      WHEN r_score = 4 AND f_score >= 3 AND m_score >= 3 THEN 'Best Customers'
      WHEN r_score >= 3 AND f_score >= 3 THEN 'Loyal Customers'
      WHEN m_score = 4 THEN 'Big Spenders'
      WHEN r_score = 1 THEN 'Lost Customers'
      ELSE 'Other'
    END AS customer_segment
  FROM rfm_scores
)

SELECT
  customer_segment,
  COUNT(*) AS customers,
  ROUND(SUM(monetary_value), 2) AS total_revenue,
  ROUND(AVG(average_rfm_score), 2) AS avg_rfm_score,
  ROUND(SAFE_DIVIDE(SUM(monetary_value), COUNT(*)), 2) AS revenue_per_customer
FROM segmented_customers
GROUP BY customer_segment
ORDER BY total_revenue DESC;
