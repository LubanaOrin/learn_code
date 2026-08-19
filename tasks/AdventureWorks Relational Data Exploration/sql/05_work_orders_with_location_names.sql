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
