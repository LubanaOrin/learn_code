-- AdventureWorks Relational Data Exploration
-- SQL queries for product, work order, and query validation tasks.

-- Task 1.1: Products with subcategory names
SELECT
  product.ProductID AS product_id,
  product.Name AS product_name,
  product.ProductNumber AS product_number,
  product.Size AS size,
  product.Color AS color,
  product.ProductSubcategoryID AS product_subcategory_id,
  product_subcategory.Name AS subcategory_name
FROM `tc-da-1.adwentureworks_db.product` AS product
JOIN `tc-da-1.adwentureworks_db.productsubcategory` AS product_subcategory
  ON product.ProductSubcategoryID = product_subcategory.ProductSubcategoryID
ORDER BY subcategory_name;

-- Task 1.2: Products with category and subcategory names
SELECT
  product.ProductID AS product_id,
  product.Name AS product_name,
  product.ProductNumber AS product_number,
  product.Size AS size,
  product.Color AS color,
  product.ProductSubcategoryID AS product_subcategory_id,
  product_subcategory.Name AS subcategory_name,
  product_category.Name AS category_name
FROM `tc-da-1.adwentureworks_db.product` AS product
JOIN `tc-da-1.adwentureworks_db.productsubcategory` AS product_subcategory
  ON product.ProductSubcategoryID = product_subcategory.ProductSubcategoryID
JOIN `tc-da-1.adwentureworks_db.productcategory` AS product_category
  ON product_subcategory.ProductCategoryID = product_category.ProductCategoryID
ORDER BY category_name;

-- Task 1.3: Most expensive actively sold bikes
SELECT
  product.ProductID AS product_id,
  product.Name AS product_name,
  product.ProductNumber AS product_number,
  product.Size AS size,
  product.Color AS color,
  product.ProductSubcategoryID AS product_subcategory_id,
  product_subcategory.Name AS subcategory_name,
  product_category.Name AS category_name,
  product.ListPrice AS list_price
FROM `tc-da-1.adwentureworks_db.product` AS product
JOIN `tc-da-1.adwentureworks_db.productsubcategory` AS product_subcategory
  ON product.ProductSubcategoryID = product_subcategory.ProductSubcategoryID
JOIN `tc-da-1.adwentureworks_db.productcategory` AS product_category
  ON product_subcategory.ProductCategoryID = product_category.ProductCategoryID
WHERE product.ListPrice > 2000
  AND product.SellEndDate IS NULL
  AND product_category.Name = 'Bikes'
ORDER BY list_price DESC;

-- Task 2.1: January 2004 work order summary by location
SELECT
  LocationID AS location_id,
  COUNT(DISTINCT WorkOrderID) AS work_order_count,
  COUNT(DISTINCT ProductID) AS unique_product_count,
  SUM(ActualCost) AS actual_cost
FROM `tc-da-1.adwentureworks_db.workorderrouting`
WHERE EXTRACT(YEAR FROM ActualStartDate) = 2004
  AND EXTRACT(MONTH FROM ActualStartDate) = 1
GROUP BY LocationID
ORDER BY actual_cost DESC;

-- Task 2.2: January 2004 work order summary with location names
SELECT
  routing.LocationID AS location_id,
  location.Name AS location_name,
  COUNT(DISTINCT routing.WorkOrderID) AS work_order_count,
  COUNT(DISTINCT routing.ProductID) AS unique_product_count,
  SUM(routing.ActualCost) AS actual_cost,
  ROUND(AVG(DATE_DIFF(routing.ActualEndDate, routing.ActualStartDate, DAY)), 2) AS avg_days_diff
FROM `tc-da-1.adwentureworks_db.workorderrouting` AS routing
JOIN `tc-da-1.adwentureworks_db.location` AS location
  ON routing.LocationID = location.LocationID
WHERE EXTRACT(YEAR FROM routing.ActualStartDate) = 2004
  AND EXTRACT(MONTH FROM routing.ActualStartDate) = 1
GROUP BY routing.LocationID, location.Name
ORDER BY avg_days_diff DESC;

-- Task 2.3: January 2004 work orders with actual cost greater than 300
SELECT
  WorkOrderID AS work_order_id,
  SUM(ActualCost) AS actual_cost
FROM `tc-da-1.adwentureworks_db.workorderrouting`
WHERE EXTRACT(YEAR FROM ActualStartDate) = 2004
  AND EXTRACT(MONTH FROM ActualStartDate) = 1
GROUP BY WorkOrderID
HAVING SUM(ActualCost) > 300;

-- Task 3.1: Corrected query for orders linked to special offers
SELECT
  sales_detail.SalesOrderId AS sales_order_id,
  sales_detail.OrderQty AS order_quantity,
  sales_detail.UnitPrice AS unit_price,
  sales_detail.LineTotal AS line_total,
  sales_detail.ProductId AS product_id,
  sales_detail.SpecialOfferID AS special_offer_id,
  spec_offer_product.ModifiedDate AS special_offer_product_modified_date,
  spec_offer.Category AS special_offer_category,
  spec_offer.Description AS special_offer_description
FROM `tc-da-1.adwentureworks_db.salesorderdetail` AS sales_detail
JOIN `tc-da-1.adwentureworks_db.specialofferproduct` AS spec_offer_product
  ON sales_detail.ProductID = spec_offer_product.ProductID
 AND sales_detail.SpecialOfferID = spec_offer_product.SpecialOfferID
JOIN `tc-da-1.adwentureworks_db.specialoffer` AS spec_offer
  ON spec_offer_product.SpecialOfferID = spec_offer.SpecialOfferID
ORDER BY sales_detail.LineTotal DESC;

-- Task 3.2: Corrected vendor information query
SELECT
  vendor.VendorId AS vendor_id,
  vendor_contact.ContactId AS contact_id,
  vendor_contact.ContactTypeID AS contact_type_id,
  vendor.Name AS vendor_name,
  vendor.CreditRating AS credit_rating,
  vendor.ActiveFlag AS active_flag,
  vendor_address.AddressId AS address_id,
  address.City AS city
FROM `tc-da-1.adwentureworks_db.vendor` AS vendor
LEFT JOIN `tc-da-1.adwentureworks_db.vendorcontact` AS vendor_contact
  ON vendor.VendorId = vendor_contact.VendorId
LEFT JOIN `tc-da-1.adwentureworks_db.vendoraddress` AS vendor_address
  ON vendor.VendorId = vendor_address.VendorId
LEFT JOIN `tc-da-1.adwentureworks_db.address` AS address
  ON vendor_address.AddressId = address.AddressId;
