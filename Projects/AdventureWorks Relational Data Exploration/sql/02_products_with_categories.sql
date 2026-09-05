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
