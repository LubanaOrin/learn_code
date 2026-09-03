-- Optional export query for deeper analysis in Python, Google Sheets, or Tableau.
-- This returns one row per purchasing user per day.
-- Dates are derived in UTC, and first arrival means the first recorded event
-- for the user-date rather than a confirmed session_start event.

WITH user_day_events AS (
  SELECT
    DATE(TIMESTAMP_MICROS(event_timestamp)) AS event_date,
    user_pseudo_id,
    MIN(TIMESTAMP_MICROS(event_timestamp)) AS first_arrival_time,
    MIN(
      CASE
        WHEN event_name = 'purchase' THEN TIMESTAMP_MICROS(event_timestamp)
      END
    ) AS first_purchase_time,
    ANY_VALUE(country) AS country,
    ANY_VALUE(category) AS device_category
  FROM `project.dataset.raw_events`
  WHERE DATE(TIMESTAMP_MICROS(event_timestamp)) BETWEEN '2020-11-01' AND '2021-01-31'
  GROUP BY
    event_date,
    user_pseudo_id
)

SELECT
  event_date,
  user_pseudo_id,
  country,
  device_category,
  first_arrival_time,
  first_purchase_time,
  ROUND(
    TIMESTAMP_DIFF(first_purchase_time, first_arrival_time, SECOND) / 60.0,
    2
  ) AS duration_to_purchase_minutes
FROM user_day_events
WHERE first_purchase_time IS NOT NULL
  AND first_purchase_time >= first_arrival_time
ORDER BY
  event_date,
  duration_to_purchase_minutes DESC;
