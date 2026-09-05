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
