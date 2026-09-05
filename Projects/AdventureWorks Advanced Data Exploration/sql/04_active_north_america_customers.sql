-- Task 1.4: Active North America customers meeting value or order thresholds
WITH latest_address AS (
  SELECT
    customeraddress.CustomerID,
    MAX(customeraddress.AddressID) AS address_id
  FROM `tc-da-1.adwentureworks_db.customeraddress` AS customeraddress
  GROUP BY customeraddress.CustomerID
),
orders_agg AS (
  SELECT
    salesorderheader.CustomerID,
    COUNT(*) AS number_orders,
    SUM(salesorderheader.TotalDue) AS total_amount,
    MAX(salesorderheader.OrderDate) AS date_last_order
  FROM `tc-da-1.adwentureworks_db.salesorderheader` AS salesorderheader
  GROUP BY salesorderheader.CustomerID
),
max_order_date AS (
  SELECT MAX(DATE(OrderDate)) AS max_order_date
  FROM `tc-da-1.adwentureworks_db.salesorderheader`
)
SELECT
  customer.CustomerID AS customer_id,
  contact.FirstName AS first_name,
  contact.LastName AS last_name,
  CONCAT(contact.FirstName, ' ', contact.LastName) AS full_name,
  CASE
    WHEN contact.Title IS NOT NULL THEN CONCAT(contact.Title, ' ', contact.LastName)
    ELSE CONCAT('Dear ', contact.LastName)
  END AS addressing_title,
  contact.EmailAddress AS email_address,
  contact.Phone AS phone,
  customer.AccountNumber AS account_number,
  customer.CustomerType AS customer_type,
  address.City AS city,
  stateprovince.Name AS state,
  countryregion.Name AS country,
  address.AddressLine1 AS address_line_1,
  COALESCE(orders_agg.number_orders, 0) AS number_orders,
  ROUND(COALESCE(orders_agg.total_amount, 0), 3) AS total_amount_with_tax,
  orders_agg.date_last_order,
  LEFT(address.AddressLine1, STRPOS(address.AddressLine1, ' ') - 1) AS address_no,
  SUBSTR(address.AddressLine1, STRPOS(address.AddressLine1, ' ') + 1) AS address_st
FROM `tc-da-1.adwentureworks_db.customer` AS customer
LEFT JOIN `tc-da-1.adwentureworks_db.individual` AS individual
  ON customer.CustomerID = individual.CustomerID
LEFT JOIN `tc-da-1.adwentureworks_db.contact` AS contact
  ON individual.ContactID = contact.ContactID
LEFT JOIN latest_address
  ON customer.CustomerID = latest_address.CustomerID
LEFT JOIN `tc-da-1.adwentureworks_db.address` AS address
  ON latest_address.address_id = address.AddressID
LEFT JOIN `tc-da-1.adwentureworks_db.stateprovince` AS stateprovince
  ON address.StateProvinceID = stateprovince.StateProvinceID
LEFT JOIN `tc-da-1.adwentureworks_db.countryregion` AS countryregion
  ON stateprovince.CountryRegionCode = countryregion.CountryRegionCode
LEFT JOIN `tc-da-1.adwentureworks_db.salesterritory` AS salesterritory
  ON stateprovince.CountryRegionCode = salesterritory.CountryRegionCode
LEFT JOIN orders_agg
  ON customer.CustomerID = orders_agg.CustomerID
CROSS JOIN max_order_date
WHERE (customer.CustomerType = 'I' OR individual.CustomerID IS NOT NULL)
  AND salesterritory.Group = 'North America'
  AND DATE(orders_agg.date_last_order) >= DATE_SUB(max_order_date.max_order_date, INTERVAL 365 DAY)
  AND (COALESCE(orders_agg.total_amount, 0) >= 2500 OR COALESCE(orders_agg.number_orders, 0) >= 5)
ORDER BY country, state, date_last_order;
