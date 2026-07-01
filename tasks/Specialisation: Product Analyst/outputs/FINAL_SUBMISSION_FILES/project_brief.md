# Product Analyst Project Brief

## Stakeholder Audience

The primary audience is the e-commerce product manager and product team.

## Decision Problem

The product manager must decide whether same-day time to purchase should become a recurring product KPI and which follow-up analysis should be prioritized to explain slow journeys.

## Main Research Question

How much time does it take same-day purchasing users to make their first purchase after first arriving on the website?

## Sub-Questions

1. What is the daily progression of median time to purchase?
2. Is average time to purchase misleading compared with median time to purchase?
3. Does purchase volume change the confidence we should have in each daily result?
4. Does device category explain differences in time to purchase?
5. Which country segments may be useful leads for follow-up analysis?

## Planned Techniques

- BigQuery SQL to transform raw event data into user-day purchase journeys.
- Daily aggregation using median, average, p25, p75, and p90 duration.
- Time-series visualization for daily progression.
- Segment analysis by device category and country.
- Limitation review to avoid overclaiming.

## Expected Final Action

Adopt weekly median same-day time to purchase as the headline KPI, supported by purchaser count, p75, and p90. Prioritize funnel-step timing as the next analysis because device category does not explain the long tail.

Reviewer feedback supports this metric choice because the data contains outliers and median better represents the typical user than average. Future analysis should add a 7-day rolling median to reduce daily noise, clean inactive time from long durations, and test whether longer time to purchase is associated with higher order value.

## Ask, Prepare, Process, Analyze, Share, Act

### Ask

The product manager wants to know how long users take to purchase after arriving on the website. The decision is whether the product team should treat time to purchase as a KPI and where to investigate possible journey friction.

### Prepare

The required data comes from the raw events table:

```sql
`tc-da-1.turing_data_analytics.raw_events`
```

Important fields include `event_timestamp`, `event_name`, `user_pseudo_id`, `country`, and `category`.

### Process

The SQL creates one row per user and date, then identifies the user's first event and first same-day purchase. The duration is calculated in minutes.

### Analyze

The analysis compares median and average time to purchase, checks purchase volume by day/month, and explores device and country splits.

### Share

The PowerPoint leads with the PM decision and keeps technical detail in an appendix:

- decision and headline answer;
- daily trend;
- metric choice;
- volume signal;
- device check;
- market leads;
- decision boundary;
- action plan;
- metric appendix;
- SQL appendix.

### Act

Track weekly median time to purchase with purchaser count, p75, and p90. Investigate material changes by funnel step, traffic source, and country. Validate session logic before using the metric operationally.

As a future improvement, smooth the daily metric with a rolling median, remove likely inactive time before interpreting long durations, and compare cleaned duration against order value.
