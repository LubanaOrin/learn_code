-- Weekly cohort retention analysis from Week 0 to Week 6
-- Analysis date: 2021-02-07
-- Replace `your_project.your_dataset.subscriptions` with the real table path.

WITH analysis_parameters AS (
  SELECT
    DATE '2021-02-07' AS analysis_date
),

user_cohort_weeks AS (
  SELECT
    subscriptions.user_pseudo_id AS user_pseudo_id,
    DATE_TRUNC(MIN(subscriptions.subscription_start), WEEK(MONDAY)) AS cohort_week
  FROM `your_project.your_dataset.subscriptions` AS subscriptions
  GROUP BY subscriptions.user_pseudo_id
),

cohort_sizes AS (
  SELECT
    user_cohort_weeks.cohort_week AS cohort_week,
    COUNT(DISTINCT user_cohort_weeks.user_pseudo_id) AS cohort_size
  FROM user_cohort_weeks
  GROUP BY user_cohort_weeks.cohort_week
),

candidate_active_weeks AS (
  SELECT
    subscriptions.user_pseudo_id AS user_pseudo_id,
    generated_week_start AS active_week
  FROM `your_project.your_dataset.subscriptions` AS subscriptions
  CROSS JOIN analysis_parameters
  CROSS JOIN UNNEST(
    GENERATE_DATE_ARRAY(
      DATE_TRUNC(subscriptions.subscription_start, WEEK(MONDAY)),
      DATE_TRUNC(
        LEAST(
          COALESCE(subscriptions.subscription_end, analysis_parameters.analysis_date),
          analysis_parameters.analysis_date
        ),
        WEEK(MONDAY)
      ),
      INTERVAL 7 DAY
    )
  ) AS generated_week_start
),

user_active_weeks AS (
  SELECT DISTINCT
    subscriptions.user_pseudo_id AS user_pseudo_id,
    candidate_active_weeks.active_week AS active_week
  FROM `your_project.your_dataset.subscriptions` AS subscriptions
  CROSS JOIN analysis_parameters
  INNER JOIN candidate_active_weeks
    ON subscriptions.user_pseudo_id = candidate_active_weeks.user_pseudo_id
  WHERE subscriptions.subscription_start < DATE_ADD(candidate_active_weeks.active_week, INTERVAL 7 DAY)
    AND COALESCE(subscriptions.subscription_end, analysis_parameters.analysis_date) >= candidate_active_weeks.active_week
    AND candidate_active_weeks.active_week <= DATE_TRUNC(analysis_parameters.analysis_date, WEEK(MONDAY))
),

cohort_weekly_activity AS (
  SELECT
    user_cohort_weeks.user_pseudo_id AS user_pseudo_id,
    user_cohort_weeks.cohort_week AS cohort_week,
    user_active_weeks.active_week AS active_week,
    DATE_DIFF(user_active_weeks.active_week, user_cohort_weeks.cohort_week, WEEK(MONDAY)) AS week_index
  FROM user_cohort_weeks
  INNER JOIN user_active_weeks
    ON user_cohort_weeks.user_pseudo_id = user_active_weeks.user_pseudo_id
),

observed_cohort_retention AS (
  SELECT
    cohort_weekly_activity.cohort_week AS cohort_week,
    cohort_weekly_activity.week_index AS week_index,
    COUNT(DISTINCT cohort_weekly_activity.user_pseudo_id) AS active_users
  FROM cohort_weekly_activity
  WHERE cohort_weekly_activity.week_index BETWEEN 0 AND 6
  GROUP BY cohort_week, week_index
),

cohort_week_grid AS (
  SELECT
    cohort_sizes.cohort_week AS cohort_week,
    week_index_value AS week_index
  FROM cohort_sizes
  CROSS JOIN UNNEST([0, 1, 2, 3, 4, 5, 6]) AS week_index_value
),

cohort_observability AS (
  SELECT
    cohort_sizes.cohort_week AS cohort_week,
    DATE_DIFF(
      DATE_TRUNC(analysis_parameters.analysis_date, WEEK(MONDAY)),
      cohort_sizes.cohort_week,
      WEEK(MONDAY)
    ) AS max_observable_week_index
  FROM cohort_sizes
  CROSS JOIN analysis_parameters
)

SELECT
  cohort_week_grid.cohort_week AS cohort_week,
  cohort_week_grid.week_index AS week_index,
  CASE
    WHEN cohort_week_grid.week_index <= cohort_observability.max_observable_week_index
      THEN observed_cohort_retention.active_users
    ELSE NULL
  END AS active_users,
  cohort_sizes.cohort_size AS cohort_size,
  CASE
    WHEN cohort_week_grid.week_index <= cohort_observability.max_observable_week_index
      THEN SAFE_DIVIDE(observed_cohort_retention.active_users, cohort_sizes.cohort_size)
    ELSE NULL
  END AS retention_rate
FROM cohort_week_grid
INNER JOIN cohort_sizes
  ON cohort_week_grid.cohort_week = cohort_sizes.cohort_week
INNER JOIN cohort_observability
  ON cohort_week_grid.cohort_week = cohort_observability.cohort_week
LEFT JOIN observed_cohort_retention
  ON cohort_week_grid.cohort_week = observed_cohort_retention.cohort_week
  AND cohort_week_grid.week_index = observed_cohort_retention.week_index
ORDER BY
  cohort_week,
  week_index;
