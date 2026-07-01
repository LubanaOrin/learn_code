# Specialisation: Marketing Analyst

## Project Objective

This project answers the Marketing Campaign Comparison task.

The marketing manager wants to understand whether users spend more time on the e-commerce website on certain weekdays and whether that behavior differs across marketing campaigns.

## Main Dataset

The expected BigQuery table path is:

```sql
`tc-da-1.turing_data_analytics.raw_events`
```

The assignment wording may show `turing_college.raw_events`. If your BigQuery workspace uses that name, keep the same SQL logic and only replace the table path.

## Current Files

- `phases/marketing-campaign-comparison.md`: phase plan and progress notes.
- `notes/marketing-campaign-comparison-brief.md`: metric definition, visualization plan, limitations, and next steps.
- `sql/marketing_campaign_comparison_session_duration.sql`: BigQuery SQL for modeled weekday session duration by campaign.
- `data/marketing_campaign_weekday_duration.csv`: exported BigQuery result.
- `outputs/charts/`: chart images created from the export.
- `outputs/FINAL_SUBMISSION_FILES/`: final files for review/upload.

## Current Status

The first final version is complete.

Final submission files:

- `marketing_campaign_comparison_presentation.pptx`
- `marketing_campaign_comparison_findings.md`
- `marketing_campaign_comparison_session_duration.sql`
- `marketing_campaign_weekday_duration.csv`

Main result:

- Referral traffic has longer sessions than organic traffic across the week.
- Data Share Promo has the longest reliable weighted average duration, but a smaller sample than organic and referral traffic.
- Black Friday and holiday campaign averages should not be overclaimed because several have very small sample sizes.
