-- Specialisation: Product Analyst
-- Main task: daily time from first same-day arrival to first same-day purchase
--
-- Definition used here:
-- first_arrival_time = user's first recorded event on that date
-- first_purchase_time = user's first purchase event on that same date
-- duration_to_purchase_minutes = minutes between those two timestamps
-- The date is derived in UTC. A business-local timezone or session-based
-- definition could produce different user-day boundaries.

WITH user_day_events AS (
  SELECT
    DATE(TIMESTAMP_MICROS(event_timestamp)) AS event_date,
    user_pseudo_id,
    MIN(TIMESTAMP_MICROS(event_timestamp)) AS first_arrival_time,
    MIN(
      CASE
        WHEN event_name = 'purchase' THEN TIMESTAMP_MICROS(event_timestamp)
      END
    ) AS first_purchase_time
  FROM `project.dataset.raw_events`
  WHERE DATE(TIMESTAMP_MICROS(event_timestamp)) BETWEEN '2020-11-01' AND '2021-01-31'
  GROUP BY
    event_date,
    user_pseudo_id
),

user_day_purchase_durations AS (
  SELECT
    event_date,
    user_pseudo_id,
    first_arrival_time,
    first_purchase_time,
    TIMESTAMP_DIFF(first_purchase_time, first_arrival_time, SECOND) / 60.0
      AS duration_to_purchase_minutes
  FROM user_day_events
  WHERE first_purchase_time IS NOT NULL
    AND first_purchase_time >= first_arrival_time
),

daily_duration_summary AS (
  SELECT
    event_date,
    COUNT(*) AS purchasing_users_count,
    ROUND(AVG(duration_to_purchase_minutes), 2) AS avg_duration_minutes,
    ROUND(
      APPROX_QUANTILES(duration_to_purchase_minutes, 100)[OFFSET(50)],
      2
    ) AS median_duration_minutes,
    ROUND(
      APPROX_QUANTILES(duration_to_purchase_minutes, 100)[OFFSET(25)],
      2
    ) AS p25_duration_minutes,
    ROUND(
      APPROX_QUANTILES(duration_to_purchase_minutes, 100)[OFFSET(75)],
      2
    ) AS p75_duration_minutes,
    ROUND(
      APPROX_QUANTILES(duration_to_purchase_minutes, 100)[OFFSET(90)],
      2
    ) AS p90_duration_minutes,
    ROUND(MIN(duration_to_purchase_minutes), 2) AS min_duration_minutes,
    ROUND(MAX(duration_to_purchase_minutes), 2) AS max_duration_minutes
  FROM user_day_purchase_durations
  GROUP BY event_date
)

SELECT
  event_date,
  purchasing_users_count,
  avg_duration_minutes,
  median_duration_minutes,
  p25_duration_minutes,
  p75_duration_minutes,
  p90_duration_minutes,
  min_duration_minutes,
  max_duration_minutes
FROM daily_duration_summary
ORDER BY event_date;
