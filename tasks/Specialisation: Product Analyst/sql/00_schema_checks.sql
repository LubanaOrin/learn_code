-- Specialisation: Product Analyst
-- Phase 1: BigQuery schema checks
--
-- Run these queries first in BigQuery.
-- They help us confirm the exact column names before finalizing the analysis SQL.

-- 1) Confirm available columns and nested field types.
SELECT
  column_name,
  data_type
FROM `tc-da-1.turing_data_analytics.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'raw_events'
ORDER BY ordinal_position;

-- 2) Confirm date range and main event names.
SELECT
  MIN(DATE(TIMESTAMP_MICROS(event_timestamp))) AS first_event_date,
  MAX(DATE(TIMESTAMP_MICROS(event_timestamp))) AS last_event_date,
  COUNT(*) AS events_count,
  COUNT(DISTINCT user_pseudo_id) AS users_count
FROM `tc-da-1.turing_data_analytics.raw_events`;

-- 3) Confirm which event names exist.
SELECT
  event_name,
  COUNT(*) AS events_count
FROM `tc-da-1.turing_data_analytics.raw_events`
GROUP BY event_name
ORDER BY events_count DESC;

-- 4) Preview the columns likely needed for this project.
SELECT
  DATE(TIMESTAMP_MICROS(event_timestamp)) AS event_date,
  TIMESTAMP_MICROS(event_timestamp) AS event_time,
  user_pseudo_id,
  event_name,
  country,
  category AS device_category,
  browser,
  browser_version
FROM `tc-da-1.turing_data_analytics.raw_events`
ORDER BY event_timestamp
LIMIT 50;
