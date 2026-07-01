# Product Analyst Time-to-Purchase Submission

## Main Files

1. `daily_time_to_purchase.sql`
   Main BigQuery SQL used to calculate daily time from first arrival to first same-day purchase.

2. `user_level_time_to_purchase_export.sql`
   Supporting BigQuery SQL used to export user-level records for device and country split analysis.

3. `product_analyst_time_to_purchase.pptx`
   Final PowerPoint presentation.

4. `daily_time_to_purchase.csv`
   Exported daily result used for the main time-series charts.

5. `user_level_time_to_purchase.csv`
   Exported user-level result used for device and country split analysis.

6. `time_to_purchase_dashboard.xlsx`
   Excel visualization workbook designed for Excel or Google Sheets upload.

7. `project_brief.md`
   Stakeholder, decision problem, analytical approach, and expected action.

8. `README.md`
   Full project explanation, key findings, limitations, and recommendations.

## Main Finding

The typical same-day purchaser buys in about 19 minutes. The average daily median time to purchase is 18.72 minutes.

The overall user-level average is 74.68 minutes, while the overall user-level median is 19.07 minutes. A smaller number of very long journeys pulls the average upward. For that reason, the presentation recommends using median time to purchase as the main KPI, supported by purchase volume and p75/p90 duration.

## Stakeholder and Decision

The audience is the e-commerce product manager and product team.

The decision is whether same-day time to purchase should be tracked as a product KPI and where the team should investigate slower journeys.

## Recommended Action

Track weekly median same-day time to purchase as the headline KPI. Show purchaser count beside it and use p75/p90 to monitor the long tail. When the median or p90 changes materially, investigate funnel-step timing, traffic source, and country. Validate session logic before using the metric operationally.

## Future Improvements From Review

- Add a 7-day rolling median to smooth daily noise from low-volume dates.
- Remove likely inactive time before interpreting very long durations.
- Test whether longer time to purchase is associated with higher order value.
