# Marketing Campaign Comparison Brief

## Assignment Focus

The final task asks us to identify trends in website time spent across weekdays and marketing campaigns.

The key metric is:

`average modeled session duration`

This means the average amount of time users spend on the website during one modeled visit.

## Why We Need Session Modeling

The table has website events, but it does not have a session identifier.

Because of that, we create sessions ourselves using a simple rule:

- same user;
- events sorted by time;
- a new session starts after a new day or a gap longer than 30 minutes.

This matters because one user can visit the website more than once. If we grouped only by user and date, we might accidentally combine separate visits into one long fake visit.

## SQL Output

The SQL query creates one row per campaign and weekday.

Columns:

- `campaign`: marketing campaign name.
- `weekday_name`: weekday label.
- `weekday_number`: weekday order from BigQuery, where Sunday is 1 and Saturday is 7.
- `weekday_sort_monday_start`: weekday order for charts, where Monday is 1 and Sunday is 7.
- `sessions`: number of modeled sessions.
- `avg_session_duration_minutes`: average session duration.
- `avg_session_duration_hh_mm_ss`: average session duration in hours, minutes, and seconds.
- `median_session_duration_minutes`: middle session duration, useful because averages can be affected by unusually long sessions.
- `max_session_duration_minutes`: longest session duration after filtering extreme values.
- `avg_events_per_session`: average number of events in each session.

## Recommended Visualization

Use a line chart or grouped bar chart:

- X-axis: weekday.
- Y-axis: average session duration in minutes.
- Color: campaign.

A line chart is useful for showing weekday trends.

A grouped bar chart is useful if there are only a few campaigns and we want easier campaign-by-campaign comparison.

## Techniques Applied

This task can use two course techniques:

1. **Feature engineering**: creating a modeled session number from raw event rows.
2. **Segmentation**: comparing the metric by weekday and campaign.

## Drawbacks To Mention

- Session IDs are not available, so session duration is estimated.
- Single-event sessions have zero duration because there is no second event to measure against.
- A 30-minute timeout is a common rule, but it is still an assumption.
- Campaign attribution may be imperfect if the campaign value is missing on some events.
- Long session durations can mean strong engagement, but they can also mean the user left the tab open.

## Further Analysis Ideas

- Compare average duration with median duration to check whether outliers affect the story.
- Compare session duration with conversion events or purchases.
- Analyze engagement by device, country, or traffic source.
- Check whether campaigns with longer sessions also have higher revenue or conversion rate.
- Review single-event sessions separately because they may indicate weak engagement or tracking limitations.

## Next Step

Run this SQL file in BigQuery:

`tasks/Specialisation: Marketing Analyst/sql/marketing_campaign_comparison_session_duration.sql`

Then export the result as CSV to:

`tasks/Specialisation: Marketing Analyst/data/marketing_campaign_weekday_duration.csv`
