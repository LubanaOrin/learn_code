-- Task 2.2: Monthly sales with cumulative total by country and region
WITH monthly_sales AS (
  SELECT
    LAST_DAY(DATE(salesorderheader.OrderDate), MONTH) AS order_month,
    salesterritory.CountryRegionCode AS country_region_code,
    salesterritory.Name AS region,
    COUNT(salesorderheader.SalesOrderID) AS number_orders,
    COUNT(DISTINCT salesorderheader.CustomerID) AS number_customers,
    COUNT(DISTINCT salesorderheader.SalesPersonID) AS number_salespersons,
    CAST(ROUND(SUM(salesorderheader.TotalDue), 0) AS INT64) AS total_with_tax
  FROM `tc-da-1.adwentureworks_db.salesorderheader` AS salesorderheader
  LEFT JOIN `tc-da-1.adwentureworks_db.salesterritory` AS salesterritory
    ON salesorderheader.TerritoryID = salesterritory.TerritoryID
  GROUP BY order_month, country_region_code, region
)
SELECT
  monthly_sales.order_month,
  monthly_sales.country_region_code,
  monthly_sales.region,
  monthly_sales.number_orders,
  monthly_sales.number_customers,
  monthly_sales.number_salespersons,
  monthly_sales.total_with_tax,
  CAST(
    SUM(monthly_sales.total_with_tax) OVER (
      PARTITION BY monthly_sales.country_region_code, monthly_sales.region
      ORDER BY monthly_sales.order_month
    ) AS INT64
  ) AS cumulative_sum
FROM monthly_sales
ORDER BY order_month, country_region_code, region;
