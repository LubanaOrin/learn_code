-- Task 2.3: Monthly sales with cumulative total and sales rank
WITH monthly_sales AS (
  SELECT
    LAST_DAY(DATE(salesorderheader.OrderDate), MONTH) AS order_month,
    salesterritory.CountryRegionCode AS country_region_code,
    salesterritory.Name AS region,
    COUNT(DISTINCT salesorderheader.SalesOrderID) AS number_orders,
    COUNT(DISTINCT salesorderheader.CustomerID) AS number_customers,
    COUNT(DISTINCT salesorderheader.SalesPersonID) AS number_salespersons,
    CAST(ROUND(SUM(salesorderheader.TotalDue), 0) AS INT64) AS total_with_tax
  FROM `tc-da-1.adwentureworks_db.salesorderheader` AS salesorderheader
  LEFT JOIN `tc-da-1.adwentureworks_db.salesterritory` AS salesterritory
    ON salesorderheader.TerritoryID = salesterritory.TerritoryID
  GROUP BY order_month, country_region_code, region
)
SELECT
  order_month,
  country_region_code,
  region,
  number_orders,
  number_customers,
  number_salespersons,
  total_with_tax,
  SUM(total_with_tax) OVER (
    PARTITION BY country_region_code, region
    ORDER BY order_month
  ) AS cumulative_sum,
  DENSE_RANK() OVER (
    PARTITION BY country_region_code, region
    ORDER BY total_with_tax DESC
  ) AS sales_rank
FROM monthly_sales
ORDER BY country_region_code, region, sales_rank, order_month DESC;
