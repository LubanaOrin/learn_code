# Specialisation: Product Analyst

## Project Objective

This project answers a product manager's follow-up question:

> How much time does it take for a user to make a purchase on the website?

The analysis measures the time between a user's first recorded website event on a day and that user's first purchase on the same day.

## Stakeholder and Decision

The primary audience is the e-commerce product manager and product team.

The decision problem is whether the product team should track same-day time to purchase as a product KPI, and where follow-up analysis should focus if some journeys look slow.

Main research question:

> How much time does it take same-day purchasing users to make their first purchase after first arriving on the website?

Supporting questions:

- What is the daily progression of median time to purchase?
- Is the average misleading compared with the median?
- Does purchase volume affect how confidently we should read each day?
- Does device category explain differences in time to purchase?
- Which country segments may be useful leads for follow-up analysis?

## Main Dataset

The source table is:

```sql
`tc-da-1.turing_data_analytics.raw_events`
```

The table contains 4,295,584 frontend event rows from 2020-11-01 to 2021-01-31.

## Files

- `notes/project_brief.md`: stakeholder, decision problem, research questions, and analysis structure.
- `sql/01_daily_time_to_purchase.sql`: working copy of the main BigQuery query.
- `data/daily_time_to_purchase.csv`: exported result from BigQuery.
- `data/user_level_time_to_purchase.csv`: user-level export used for device and country splits.
- `outputs/charts/daily_median_time_to_purchase.png`: main trend chart.
- `outputs/charts/average_vs_median_time_to_purchase.png`: chart showing skew/outliers.
- `outputs/charts/daily_purchasing_users.png`: daily volume context.
- `outputs/charts/device_median_time_to_purchase.png`: device split chart.
- `outputs/charts/top_country_median_time_to_purchase.png`: country split chart.
- `outputs/monthly_time_to_purchase_summary.csv`: monthly summary table.
- `outputs/product_analyst_time_to_purchase.pptx`: final PowerPoint presentation.
- `outputs/time_to_purchase_dashboard.xlsx`: Excel/Google Sheets-ready visualization workbook.
- `scripts/build_presentation_charts.py`: reproducible script that builds presentation chart images.
- `scripts/build_excel_visualization.py`: reproducible script that builds the Excel workbook.

## SQL Logic

The query creates one row per user per day, then calculates:

- first arrival time: the user's first event timestamp on that date.
- first purchase time: the user's first `purchase` event timestamp on that same date.
- duration to purchase: minutes between first arrival and first purchase.

Because the task asks for first arrival on a given day, the first recorded event for each user-date is used as the arrival timestamp.

The final result summarizes those user-level durations by date.

## Key Findings

- The exported result contains 92 daily records from 2020-11-01 to 2021-01-31.
- Across the full period, the average daily median time to purchase was 18.72 minutes.
- The median daily duration ranged from 10.52 minutes to 38.98 minutes.
- The overall user-level average duration was 74.68 minutes, much higher than the 19.07-minute overall median.
- The average of the 92 daily average durations was 67.66 minutes. This is a daily-summary statistic, not the overall user-level average.
- The gap between average and median means the data is skewed by some users who took many hours before buying.
- December had the highest purchase activity, with 2,085 same-day purchasing users and 67.26 purchasing users per day on average.
- December also had the highest average median time to purchase, 19.99 minutes.
- January had lower purchasing activity, with 1,108 same-day purchasing users and 35.74 purchasing users per day on average.
- The user-level export contains 4,794 same-day purchasing user records.
- Desktop and mobile purchase duration is very similar: desktop median is 19.20 minutes and mobile median is 18.92 minutes.
- The United States has the largest sample, with 2,095 same-day purchasing users and an 18.60 minute median duration.
- Among countries with at least 50 purchasing users, Turkey has the slowest median duration at 25.40 minutes, followed by Brazil at 25.17 minutes and the Netherlands at 24.22 minutes.

## Recommended Main Metric

Use `median_duration_minutes` as the main presentation metric.

Reason: the average is strongly affected by unusually long sessions. The median better describes the typical same-day purchaser.

Decision:

- Track weekly median same-day time to purchase.
- Show purchaser count beside the median.
- Use p75 and p90 to monitor slower journeys.
- Investigate material changes by funnel step, traffic source, and country.

## Presentation Story

The presentation leads with the PM decision and moves technical detail to the appendix:

1. Product decision and headline answer.
2. Daily time-to-purchase trend.
3. Why median is the correct headline metric.
4. December purchase-volume signal.
5. Device check.
6. Country follow-up leads.
7. What the analysis supports and cannot diagnose.
8. Action plan.
9. Appendix: metric definition.
10. Appendix: SQL logic.

## Limitations

- The analysis only includes users who purchased on the same day they first arrived.
- It does not include users who arrived on one day and purchased on a later day.
- First arrival is defined as the first recorded event, not necessarily a true session start.
- `DATE(TIMESTAMP_MICROS(event_timestamp))` uses the timestamp date in UTC. Results may change if the business requires a specific local timezone.
- A session-based arrival definition may produce different results from the user-date definition used here.
- The analysis includes device and country splits, but does not yet split by traffic source, product type, or funnel step.
- Very long durations may represent users leaving the website open and returning later.

## Recommended Follow-Up Analysis

- Compare time to purchase by device category.
- Compare time to purchase by country or traffic source.
- Use session-level logic if a reliable session identifier is available.
- Check whether long durations are real shopping journeys or inactive browser tabs.
- Analyze conversion funnel steps before purchase to see where users spend the most time.
- Add a 7-day rolling median to smooth daily noise, especially on dates with lower purchase volume.
- Remove likely inactive time from long durations before using the metric operationally.
- Test whether longer time to purchase is associated with higher order value, using `purchase_revenue_in_usd` or a cleaned order-value field.

## Review Feedback Incorporated

The reviewer agreed that median is a stronger headline metric than average because the data contains many outliers. The reviewer also noted that p75 and p90 are useful supporting quantiles for investigating longer session durations.

Recommended future improvements are:

- use a rolling median, such as a 7-day rolling median, to reduce noisy daily movement;
- clean or exclude inactive time from long purchase durations;
- analyze whether longer time to purchase is connected to higher order value.

## Final Presentation

The final PowerPoint presentation is saved at:

```text
outputs/product_analyst_time_to_purchase.pptx
```

It contains 10 slides following the decision-led story listed above.

## Portfolio Outputs

The GitHub project presents the final deliverables directly in `outputs/`:

- `product_analyst_time_to_purchase.pptx`;
- `time_to_purchase_dashboard.xlsx`;
- presentation-ready charts and analytical summary CSV files.

The final Excel workbook contains:

- a dashboard with native Excel charts;
- daily summary data;
- device and country summaries;
- user-level source data;
- a README explaining metric definitions and limitations.
