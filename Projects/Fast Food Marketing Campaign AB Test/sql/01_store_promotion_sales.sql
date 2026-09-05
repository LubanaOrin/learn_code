-- Store-level sales by promotion for a fast-food marketing campaign A/B test.
-- Replace `your_project.your_dataset.wa_marketing_campaign` with the real table path.

SELECT
  LocationID AS location_id,
  PromotionID AS promotion_id,
  SUM(SalesInThousands) AS total_sales_thousands
FROM `your_project.your_dataset.wa_marketing_campaign`
GROUP BY
  location_id,
  promotion_id
ORDER BY
  promotion_id,
  total_sales_thousands DESC;
