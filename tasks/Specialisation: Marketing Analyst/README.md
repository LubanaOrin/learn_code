# Marketing Campaign Duration Analysis

## Project Objective

This project compares modeled website session duration across weekdays and marketing campaigns.

## Main Dataset

The analysis uses an event-level e-commerce dataset queried in BigQuery. The public SQL keeps the source table as a placeholder so the logic can be reused with another compatible raw events table.

## Current Files

- `phases/marketing-campaign-comparison.md`: phase plan and progress notes.
- `notes/marketing-campaign-comparison-brief.md`: metric definition, visualization plan, limitations, and next steps.
- `sql/marketing_campaign_comparison_session_duration.sql`: SQL for modeled weekday session duration by campaign.
- `data/marketing_campaign_weekday_duration.csv`: exported query result.
- `outputs/charts/`: chart images created from the export.
- `outputs/marketing_campaign_comparison_presentation.pptx`: final portfolio presentation.
- `outputs/marketing_campaign_duration_dashboard.xlsx`: final Excel dashboard.
- `outputs/marketing_campaign_comparison_findings.md`: written findings.
- `outputs/marketing_campaign_comparison_speaker_notes.md`: presentation notes.

## Current Status

The portfolio version is complete.

Final portfolio files:

- `marketing_campaign_comparison_presentation.pptx`
- `marketing_campaign_duration_dashboard.xlsx`
- `marketing_campaign_comparison_findings.md`

Main result:

- Referral traffic has longer sessions than organic traffic across the week.
- Data Share Promo has the longest reliable weighted average duration, but a smaller sample than organic and referral traffic.
- Black Friday and holiday campaign averages should not be overclaimed because several have very small sample sizes.
