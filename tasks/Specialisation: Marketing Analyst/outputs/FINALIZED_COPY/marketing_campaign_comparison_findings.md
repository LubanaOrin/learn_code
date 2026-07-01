# Marketing Campaign Comparison Findings

## Dataset Check

- The BigQuery export contains 57 campaign-weekday rows.
- The analysis covers 10 campaign/source groups.
- Total modeled sessions in the exported result: 219,170.

## Main Findings

- Among campaign/source groups with at least 100 sessions, **Data Share Promo** has the longest weighted average session duration at **6.40 minutes**.
- Referral traffic has **82,353 sessions** and a weighted average duration of **5.54 minutes**.
- Organic traffic has **102,309 sessions** and a weighted average duration of **4.06 minutes**.
- Data Share Promo has **1,294 sessions** and a weighted average duration of **6.40 minutes**.
- The highest raw campaign-weekday average is **BlackFriday_V2 on Sunday** at **26.73 minutes**, but it is based on only **4 sessions**.
- BlackFriday_V1 Friday average session duration was 12.44 minutes (00:12:27), based on 2 sessions. It did not take longer than 1 hour.

## Interpretation

Referral sessions are consistently longer than organic sessions across the week. This can be a positive sign because referred users may be more engaged, but longer time on site can also mean users are struggling to find information or leaving tabs open.

The small named campaigns should be treated carefully. Several have fewer than 100 modeled sessions in total, so one or two unusually long visits can strongly affect the average.

## Drawbacks

- The dataset does not include a real session ID, so sessions are modeled with a 30-minute inactivity rule.
- Single-event sessions have a duration of 0 minutes because there is no second event to measure against.
- Campaign attribution may be incomplete when campaign values are missing from events.
- Long duration can mean engagement, confusion, or inactive browser tabs.
- Several campaigns have very small samples.

## Recommended Further Analysis

- Compare average and median session duration for each campaign.
- Connect session duration to purchases or conversion events.
- Repeat the analysis by device, country, and traffic source.
- Separate single-event sessions from multi-event sessions.
- Test whether longer sessions have higher revenue or only more browsing.

## Chart Outputs

- `outputs/charts/reliable_campaign_weekday_duration.png`
- `outputs/charts/campaign_sample_size_context.png`
- `outputs/charts/top_weekday_campaign_duration_combinations.png`
