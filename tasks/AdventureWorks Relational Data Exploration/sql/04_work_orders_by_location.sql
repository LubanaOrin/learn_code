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
