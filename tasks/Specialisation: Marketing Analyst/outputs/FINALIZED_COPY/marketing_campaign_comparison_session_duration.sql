-- Marketing Campaign Comparison
-- Purpose:
--   Model website sessions from raw event data and compare average session
--   duration by campaign and weekday.
--
-- Main idea:
--   The table does not have a session ID, so this query creates one.
--   A new session starts when:
--     1. the user has no previous event,
--     2. the previous event was on a different date, or
--     3. the time gap from the previous event is more than 30 minutes.
--
-- BigQuery note:
--   If your course table uses a different full table path, replace the table
--   name in the base_events CTE.

WITH base_events AS (
  SELECT
    PARSE_DATE('%Y%m%d', event_date) AS event_day,
    TIMESTAMP_MICROS(event_timestamp) AS event_time,
    user_pseudo_id,
    NULLIF(TRIM(campaign), '') AS campaign,
    event_name
  FROM `tc-da-1.turing_data_analytics.raw_events`
  WHERE user_pseudo_id IS NOT NULL
    AND event_timestamp IS NOT NULL
    AND event_date IS NOT NULL
),

ordered_events AS (
  SELECT
    *,
    LAG(event_time) OVER (
      PARTITION BY user_pseudo_id
      ORDER BY event_time
    ) AS previous_event_time,
    LAG(event_day) OVER (
      PARTITION BY user_pseudo_id
      ORDER BY event_time
    ) AS previous_event_day
  FROM base_events
),

session_flags AS (
  SELECT
    *,
    CASE
      WHEN previous_event_time IS NULL THEN 1
      WHEN event_day != previous_event_day THEN 1
      WHEN TIMESTAMP_DIFF(event_time, previous_event_time, MINUTE) > 30 THEN 1
      ELSE 0
    END AS is_new_session
  FROM ordered_events
),

sessionized_events AS (
  SELECT
    *,
    SUM(is_new_session) OVER (
      PARTITION BY user_pseudo_id
      ORDER BY event_time
      ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS modeled_session_number
  FROM session_flags
),

sessions AS (
  SELECT
    user_pseudo_id,
    modeled_session_number,
    MIN(event_day) AS session_day,
    MIN(event_time) AS session_start_time,
    MAX(event_time) AS session_end_time,
    COUNT(*) AS events_in_session,
    ARRAY_AGG(
      campaign IGNORE NULLS
      ORDER BY event_time
      LIMIT 1
    )[SAFE_OFFSET(0)] AS session_campaign
  FROM sessionized_events
  GROUP BY
    user_pseudo_id,
    modeled_session_number
),

session_durations AS (
  SELECT
    session_day,
    FORMAT_DATE('%A', session_day) AS weekday_name,
    EXTRACT(DAYOFWEEK FROM session_day) AS weekday_number,
    MOD(EXTRACT(DAYOFWEEK FROM session_day) + 5, 7) + 1 AS weekday_sort_monday_start,
    session_campaign,
    events_in_session,
    TIMESTAMP_DIFF(session_end_time, session_start_time, SECOND) AS session_duration_seconds,
    ROUND(
      TIMESTAMP_DIFF(session_end_time, session_start_time, SECOND) / 60,
      2
    ) AS session_duration_minutes
  FROM sessions
  WHERE session_campaign IS NOT NULL
    AND session_campaign NOT IN ('(not set)', '(data deleted)', '(direct)')
),

campaign_weekday_summary AS (
  SELECT
    session_campaign AS campaign,
    weekday_name,
    weekday_number,
    weekday_sort_monday_start,
    COUNT(*) AS sessions,
    ROUND(AVG(session_duration_seconds) / 60, 2) AS avg_session_duration_minutes,
    FORMAT(
      '%02d:%02d:%02d',
      DIV(CAST(ROUND(AVG(session_duration_seconds), 0) AS INT64), 3600),
      DIV(MOD(CAST(ROUND(AVG(session_duration_seconds), 0) AS INT64), 3600), 60),
      MOD(CAST(ROUND(AVG(session_duration_seconds), 0) AS INT64), 60)
    ) AS avg_session_duration_hh_mm_ss,
    ROUND(APPROX_QUANTILES(session_duration_seconds, 100)[OFFSET(50)] / 60, 2)
      AS median_session_duration_minutes,
    ROUND(MAX(session_duration_seconds) / 60, 2) AS max_session_duration_minutes,
    ROUND(AVG(events_in_session), 2) AS avg_events_per_session
  FROM session_durations
  -- This removes extreme sessions that are probably tracking artifacts.
  -- Keep it in the query so the rule is transparent.
  WHERE session_duration_seconds BETWEEN 0 AND 14400
  GROUP BY
    campaign,
    weekday_name,
    weekday_number,
    weekday_sort_monday_start
)

SELECT
  campaign,
  weekday_name,
  weekday_number,
  weekday_sort_monday_start,
  sessions,
  avg_session_duration_minutes,
  avg_session_duration_hh_mm_ss,
  median_session_duration_minutes,
  max_session_duration_minutes,
  avg_events_per_session
FROM campaign_weekday_summary
ORDER BY
  campaign,
  weekday_sort_monday_start;
