-- Task 2.1: Monthly sales figures by country and region
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
ORDER BY order_month, country_region_code, region;
