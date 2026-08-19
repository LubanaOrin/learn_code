-- Task 2.3: January 2004 work orders with actual cost greater than 300
SELECT
  WorkOrderID AS work_order_id,
  SUM(ActualCost) AS actual_cost
FROM `tc-da-1.adwentureworks_db.workorderrouting`
WHERE EXTRACT(YEAR FROM ActualStartDate) = 2004
  AND EXTRACT(MONTH FROM ActualStartDate) = 1
GROUP BY WorkOrderID
HAVING SUM(ActualCost) > 300;
