# Weekly Subscription Cohort Retention Analysis

## Project Overview

This project analyzes subscription retention by weekly cohort.

The goal is to understand how many users remain active after starting a subscription, from Week 0 through Week 6. Weekly retention is useful because it shows drop-off patterns faster than monthly reporting.

## Main Deliverables

- `Weekly Cohort Retention Results.xlsx`: workbook with query results, pivot output, and cohort retention visualization.
- `weekly_cohort_retention_results.csv`: previewable CSV export of the final query results.
- `sql/weekly_cohort_retention.sql`: SQL query used to calculate weekly cohort retention.

The workbook is kept for outputs and visualization. The SQL query is stored separately so the logic is easy to review on GitHub.

## Business Question

How well do subscription users retain after their starting week, and where does the largest drop-off happen?

## Method

1. Assign each user to a cohort based on their first subscription start week.
2. Treat that starting week as `Week 0`.
3. Track whether each user is still active in weeks `0` through `6`.
4. Count active users per cohort and week.
5. Divide active users by the starting cohort size to calculate retention rate.
6. Leave future weeks blank when the full observation window is not available.

The analysis assumes the reporting date is **2021-02-07**.

## Workbook Structure

The Excel workbook contains:

- `SQL Result`: exported query output with readable cohort dates and retention percentages.
- `Retention Pivot`: pivot-table support for summarizing retention.
- `Cohort Results`: cohort retention percentage table from Week 0 to Week 6.

## Key Findings

- `Week 0` is the baseline, so each cohort starts at **100.0%** retention.
- The first cohort, starting **2020-10-26**, had **87.9%** retention by Week 6.
- The cohort starting **2020-11-02** had **85.3%** retention by Week 6.
- The cohort starting **2020-11-09** had **85.6%** retention by Week 6.
- The strongest drop-off happens early, especially between Week 1 and Week 2.
- After the early drop-off, retention declines more slowly and becomes more stable.
- Cohorts show broadly similar retention patterns, suggesting consistent subscription behavior.
- Newer cohorts appear slightly stronger in some weeks, but the difference is not large enough to overclaim without more context.
- Users who remain active beyond the first few weeks are more likely to continue longer term.

## Recommendation

Focus product and lifecycle work on the early subscription period. Improving onboarding, activation, reminder flows, or first-week product value could have the biggest impact on retention.

## Skills Demonstrated

- SQL cohort analysis
- Subscription retention logic
- Date truncation and weekly windows
- Active-user calculation
- Cohort-size normalization
- Pivot tables
- Retention heatmap visualization
- Turning retention results into product recommendations

## How to Review

Open the Excel workbook:

```text
Weekly Cohort Retention Results.xlsx
```

Review the SQL query:

```text
sql/weekly_cohort_retention.sql
```

If viewing the workbook on GitHub, click the `.xlsx` file and use **View raw** or **Download** to open it locally in Excel.
