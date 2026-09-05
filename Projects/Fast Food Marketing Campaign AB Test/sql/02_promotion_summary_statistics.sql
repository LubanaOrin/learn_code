-- Promotion-level summary statistics for A/B test comparison.
-- Replace `your_project.your_dataset.wa_marketing_campaign` with the real table path.

WITH store_promotion_sales AS (
  SELECT
    LocationID AS location_id,
    PromotionID AS promotion_id,
    SUM(SalesInThousands) AS total_sales_thousands
  FROM `your_project.your_dataset.wa_marketing_campaign`
  GROUP BY
    location_id,
    promotion_id
)

SELECT
  promotion_id,
  COUNT(*) AS store_count,
  ROUND(AVG(total_sales_thousands), 2) AS mean_sales_thousands,
  ROUND(STDDEV_SAMP(total_sales_thousands), 2) AS stddev_sales_thousands
FROM store_promotion_sales
GROUP BY promotion_id
ORDER BY promotion_id;
