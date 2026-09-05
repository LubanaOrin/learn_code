-- Task 2.4: Monthly sales with cumulative total, rank, and country-level tax details
WITH monthly_sales AS (
  SELECT
    LAST_DAY(DATE(soh.OrderDate), MONTH) AS order_month,
    st.CountryRegionCode AS country_region_code,
    st.Name AS region,
    COUNT(DISTINCT soh.SalesOrderID) AS number_orders,
    COUNT(DISTINCT soh.CustomerID) AS number_customers,
    COUNT(DISTINCT soh.SalesPersonID) AS number_salespersons,
    CAST(ROUND(SUM(soh.TotalDue), 0) AS INT64) AS total_with_tax
  FROM `tc-da-1.adwentureworks_db.salesorderheader` AS soh
  LEFT JOIN `tc-da-1.adwentureworks_db.salesterritory` AS st
    ON soh.TerritoryID = st.TerritoryID
  GROUP BY order_month, country_region_code, region
),
province_tax AS (
  SELECT
    sp.CountryRegionCode AS country_region_code,
    sp.StateProvinceID AS state_province_id,
    MAX(CASE WHEN str.TaxType = 1 THEN str.TaxRate END) AS province_max_tax,
    MAX(CASE WHEN str.TaxType = 1 THEN 1 END) AS has_tax
  FROM `tc-da-1.adwentureworks_db.stateprovince` AS sp
  LEFT JOIN `tc-da-1.adwentureworks_db.salestaxrate` AS str
    ON str.StateProvinceID = sp.StateProvinceID
  GROUP BY country_region_code, state_province_id
),
country_tax AS (
  SELECT
    country_region_code,
    ROUND(AVG(CASE WHEN has_tax = 1 THEN province_max_tax END), 1) AS mean_tax_rate,
    ROUND(SAFE_DIVIDE(SUM(CASE WHEN has_tax = 1 THEN 1 ELSE 0 END), COUNT(*)), 2) AS perc_provinces_w_tax
  FROM province_tax
  GROUP BY country_region_code
)
SELECT
  ms.order_month,
  ms.country_region_code,
  ms.region,
  ms.number_orders,
  ms.number_customers,
  ms.number_salespersons,
  ms.total_with_tax,
  SUM(ms.total_with_tax) OVER (
    PARTITION BY ms.country_region_code, ms.region
    ORDER BY ms.order_month
  ) AS cumulative_sum,
  DENSE_RANK() OVER (
    PARTITION BY ms.country_region_code, ms.order_month
    ORDER BY ms.total_with_tax DESC
  ) AS country_sales_rank,
  ct.mean_tax_rate,
  ct.perc_provinces_w_tax
FROM monthly_sales AS ms
LEFT JOIN country_tax AS ct
  ON ct.country_region_code = ms.country_region_code
ORDER BY ms.order_month DESC, ms.country_region_code, ms.region;
