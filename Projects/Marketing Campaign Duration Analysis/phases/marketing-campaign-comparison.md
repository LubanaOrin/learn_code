# Marketing Campaign Comparison

## Goal

Complete the marketing campaign comparison analysis.

The task compares marketing campaigns by how long users spend on the e-commerce website on different weekdays.

The analysis uses an event-level e-commerce raw events table in BigQuery. In the public SQL, the source table is represented as a placeholder so the logic can be reused with any compatible dataset.

The important columns are:

- `event_date`: date of the event, stored as text in `YYYYMMDD` format.
- `event_timestamp`: event time, stored as microseconds.
- `user_pseudo_id`: anonymous user identifier.
- `campaign`: marketing campaign name.
- `event_name`: action taken on the website.

## What We Need To Submit

The final submission should include:

1. SQL query used to extract the data.
2. Visualization comparing weekday session duration across campaigns.
3. Short written comments explaining the findings.
4. Drawbacks of the analysis.
5. Further analysis recommendations.

## Important Modeling Decision

The dataset does not include a ready-made session ID.

That means we must create our own session logic. A **session** means one visit to the website. Since we do not have official session IDs, we will define a new session when:

- the user has no previous event;
- the previous event was on a different day; or
- the gap between events is more than 30 minutes.

This is a common web analytics rule. It is not perfect, but it is reasonable and easy to explain.

## Phases

### Phase 1: Understand the Task

Status: Done

What we did:

- Read the project instructions.
- Focused on the final task: **Marketing Campaign Comparison**.
- Checked the Excel workbook only as a learning reference.
- Confirmed the workbook should not be copied into the repository.

### Phase 2: Build the SQL Query

Status: Done

What we did:

- Created a BigQuery SQL query in `sql/marketing_campaign_comparison_session_duration.sql`.
- Converted event timestamps into readable timestamps.
- Sorted events by user and time.
- Created a new session whenever there is a new day or a gap longer than 30 minutes.
- Calculated session duration from first event to last event.
- Grouped average and median session duration by campaign and weekday.
- Added a human-readable `HH:MM:SS` average duration field for presentation discussion.

### Phase 3: Export Query Results

Status: Done

What we did:

- Imported the query export.
- Saved the CSV in:

`Projects/Marketing Campaign Duration Analysis/data/marketing_campaign_weekday_duration.csv`

Result:

- 57 campaign-weekday rows.
- 10 campaign/source groups.
- 219,170 modeled sessions.

### Phase 4: Visualize Results

Status: Done

What we created:

- `outputs/charts/reliable_campaign_weekday_duration.png`
- `outputs/charts/campaign_sample_size_context.png`
- `outputs/charts/top_weekday_campaign_duration_combinations.png`
- `outputs/marketing_campaign_comparison_findings.md`
- `outputs/marketing_campaign_comparison_presentation.pptx`

### Phase 5: Final QA

Status: Done

Checklist:

- [x] SQL is readable and formatted.
- [x] Session duration logic is explained.
- [x] Visualization answers the marketing manager's question.
- [x] Findings are written clearly.
- [x] Limitations are included.
- [x] Recommendations are included.
- [x] PPTX package validates with `unzip -t`.
- [x] PPTX rendered to PDF with LibreOffice for visual QA.

## Beginner-Friendly Explanation

The key challenge is that the table has many website events, but it does not directly tell us which events belong to the same website visit.

So we make a practical rule:

If the same user keeps doing things close together in time, we treat those events as one session. If they disappear for more than 30 minutes, we treat the next event as a new session.

Then we calculate:

`session duration = last event time - first event time`

After that, we compare the average duration by:

- weekday, such as Monday or Friday;
- marketing campaign, such as Black Friday or Holiday campaign.

This helps answer whether some campaigns bring users who spend more time on the website on specific weekdays.
