-- Funnel aggregation for the top 3 countries by unique event volume.
-- Replace `your_project.your_dataset.raw_events` with the real table path.

WITH unique_events AS (
  SELECT
    *
  FROM `your_project.your_dataset.raw_events`
  QUALIFY
    ROW_NUMBER() OVER (
      PARTITION BY user_pseudo_id, event_name
      ORDER BY event_timestamp, event_date, page_location, transaction_id
    ) = 1
),

funnel_events AS (
  SELECT 1 AS event_order, 'session_start' AS event_name UNION ALL
  SELECT 2 AS event_order, 'view_item' AS event_name UNION ALL
  SELECT 3 AS event_order, 'add_to_cart' AS event_name UNION ALL
  SELECT 4 AS event_order, 'begin_checkout' AS event_name UNION ALL
  SELECT 5 AS event_order, 'purchase' AS event_name
),

top_countries AS (
  SELECT
    country,
    COUNT(*) AS total_events
  FROM unique_events
  WHERE country IS NOT NULL
  GROUP BY country
  ORDER BY total_events DESC
  LIMIT 3
)

SELECT
  funnel_events.event_order,
  unique_events.event_name,
  unique_events.country,
  COUNT(*) AS event_count
FROM unique_events
JOIN top_countries
  ON unique_events.country = top_countries.country
JOIN funnel_events
  ON unique_events.event_name = funnel_events.event_name
GROUP BY
  funnel_events.event_order,
  unique_events.event_name,
  unique_events.country
ORDER BY
  funnel_events.event_order,
  event_count DESC;
