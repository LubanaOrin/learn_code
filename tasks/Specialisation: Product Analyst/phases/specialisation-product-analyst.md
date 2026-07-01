# Specialisation: Product Analyst - Phase Plan

## Project Status

Task brief received and copied into the project.

## Working Standard

This project will apply the lessons from the previous reviewed projects:

- Follow the assignment requirements in the same order as the reviewer expects.
- Start with a clear dataset or task description near the top of the final notebook/report.
- Include an executive summary when useful.
- Use exact numbers in findings, not vague wording.
- Add visualizations for important results.
- Use clean Pandas code and avoid unnecessary manual loops.
- Explain each phase in beginner-friendly language.
- Keep final files organized and easy to review.

## Planned Folder Structure

- `data/` for raw or provided datasets.
- `notebooks/` for Jupyter notebooks.
- `outputs/` for cleaned files, charts, exports, or reports.
- `notes/` for assignment briefs and reference material.
- `phases/` for phase plans and progress notes.
- `sql/` for BigQuery SQL files.

## Source Files

- `notes/Product Analyst Intro.docx`: full weekly context and graded task brief.
- `data/Monday. 1st view.xlsx`: daily purchases count example.
- `data/Monday. 2nd view.xlsx`: purchases split by country example.
- `data/Tuesday. 1st view.xlsx`: desktop/mobile purchase ratio example.
- `data/Wednesday. 1st view.xlsx`: browser-version purchase funnel example.
- `data/Friday. 1st view.xlsx`: returning-user purchase split example.

## Main Graded Task

The main task begins with:

> You have a follow-up task from your product manager to identify how much time it takes for a user to make a purchase on your website.

The PM wants to see how long it takes users to make their first purchase after first arriving on the website on the same day.

Final result should show the daily progression of that duration.

## Evaluation Criteria

- SQL uses the correct columns.
- SQL logic correctly calculates the analysis.
- SQL is formatted and readable.
- Visualizations clearly communicate the answer.
- Findings and main points are clearly structured.
- Analytical approach is strong, including drawbacks and recommended follow-up analysis.

## Phase 1 - Task Understanding and Access Plan

Status: In progress

Tasks:

- [x] Copy the task files into the project folder.
- [x] Read the assignment document.
- [x] Identify the actual graded task.
- [x] Create a BigQuery collaboration plan for the private table.
- [x] Confirm the exact column names in `tc-da-1.turing_data_analytics.raw_events`.
- [x] Run the first analysis SQL in BigQuery.
- [x] Save or paste/export the query result for analysis.

BigQuery access plan:

- Codex will not need direct access to the private college BigQuery link.
- Codex will write SQL files in `sql/`.
- The user will run the SQL in BigQuery.
- The user can paste result previews here or export results as CSV/XLSX.
- Codex will use those results to build the notebook, charts, and presentation.

## Planned Phases

1. Confirm schema and produce the first correct BigQuery query.
2. Calculate daily same-day time-to-purchase results.
3. Explore useful splits or outliers, such as device, country, weekday, or high-duration days.
4. Build a clear visualization of daily duration.
5. Write analytical insights, drawbacks, and recommended next analysis.
6. Create final deliverables: SQL file, notebook or analysis report, presentation, README, and outputs.

## Important Analysis Definitions

- First arrival on a day: the first recorded event for a user on that date.
- First purchase on the same day: the user's earliest `purchase` event on that same date.
- Duration to purchase: time between first arrival and first same-day purchase.
- Daily progression: daily summary of those user-level durations.

These definitions may be adjusted if BigQuery confirms the table has a more precise event such as `session_start`.

## Phase 1 Notes

The schema is a flattened event table, not a nested GA4 export. This means SQL should use:

- `country`, not `geo.country`.
- `category`, not `device.category`.
- `browser`, not `device.web_info.browser`.
- `browser_version`, not `device.web_info.browser_version`.

The full BigQuery table path is:

```sql
`tc-da-1.turing_data_analytics.raw_events`
```

## Phase 2 - Daily Time-to-Purchase Analysis

Status: Complete

Tasks:

- [x] Import the BigQuery result into `data/daily_time_to_purchase.csv`.
- [x] Check the date range and number of rows.
- [x] Calculate summary statistics.
- [x] Create presentation-ready charts.
- [x] Save monthly and top-day summary tables.

Results:

- The result contains 92 daily records.
- Date range: 2020-11-01 to 2021-01-31.
- The average daily median time to purchase is 18.72 minutes.
- The median duration ranges from 10.52 minutes to 38.98 minutes.
- The average daily duration is 67.66 minutes, much higher than the median.
- This difference means the data is right-skewed: a smaller number of very long purchase journeys pull the average upward.
- December has the highest same-day purchasing-user volume: 2,085 users.
- December also has the highest average median duration: 19.99 minutes.

Charts created:

- `outputs/charts/daily_median_time_to_purchase.png`
- `outputs/charts/average_vs_median_time_to_purchase.png`
- `outputs/charts/daily_purchasing_users.png`

What this phase teaches:

- Median is often better than average when a metric has extreme values.
- A product analyst should show both behavior and context: duration tells us how long users take, while purchase count tells us how much evidence each day has.

## Phase 3 - Device and Country Split Analysis

Status: Complete

Tasks:

- [x] Import the user-level BigQuery export.
- [x] Save a CSV copy for reproducibility.
- [x] Compare same-day time to purchase by device category.
- [x] Compare same-day time to purchase by country.
- [x] Create split charts for presentation use.

Results:

- The user-level export contains 4,794 same-day purchasing user records.
- Desktop median time to purchase: 19.20 minutes across 2,722 purchasing users.
- Mobile median time to purchase: 18.92 minutes across 1,969 purchasing users.
- Tablet median time to purchase: 17.10 minutes across 103 purchasing users.
- Device category does not explain the main duration pattern because desktop and mobile are very close.
- United States is the largest country group, with 2,095 purchasing users and an 18.60 minute median duration.
- Among countries with at least 50 purchasing users, the slowest median durations are Turkey at 25.40 minutes, Brazil at 25.17 minutes, and the Netherlands at 24.22 minutes.

Charts created:

- `outputs/charts/device_median_time_to_purchase.png`
- `outputs/charts/top_country_median_time_to_purchase.png`

What this phase teaches:

- Segment analysis helps test possible explanations.
- Similar device medians mean we should avoid blaming device experience without more evidence.
- Country differences are useful leads, but smaller sample sizes should be interpreted carefully.

## Phase 4 - PowerPoint Presentation

Status: Complete

Tasks:

- [x] Build a real `.pptx` presentation.
- [x] Add embedded chart images.
- [x] Add editable text boxes and KPI shapes.
- [x] Add speaker notes.
- [x] Render the presentation to PDF for verification.
- [x] Create preview images and a contact sheet for visual QA.

Files created:

- `outputs/presentation/FINAL_product_analyst_time_to_purchase.pptx`
- `outputs/presentation/FINAL_speaker_notes.md`
- `outputs/presentation/rendered/product_analyst_time_to_purchase.pdf`
- `outputs/archive/presentation_qa/contact_sheet.png`
- `scripts/build_presentation.py`

Verification:

- The PPTX package is recognized as `Microsoft PowerPoint 2007+`.
- LibreOffice successfully rendered the deck to PDF.
- The PDF was converted into slide preview images.
- The contact sheet shows all 10 slides render with visible text and charts.

What this phase teaches:

- A presentation should tell a clear analytical story, not only show charts.
- The best order is question -> method -> main answer -> supporting evidence -> limitations -> recommendation.

## Phase 5 - Project Direction Review

Status: Complete

Tasks:

- [x] Read the capstone future-project-direction note.
- [x] Add a sharper stakeholder and decision problem to the current project.
- [x] Add a one-page project brief.
- [x] Fix README wording that became outdated after device and country split analysis.
- [x] Update the upload README with the stakeholder decision and recommended action.

Result:

- Added `notes/project_brief.md`.
- Updated `README.md`.
- Updated `outputs/FINAL_SUBMISSION_FILES/README_UPLOAD.md`.

What this phase teaches:

- Before building charts, a product analyst should define the stakeholder, decision problem, and main research question.
- A strong presentation keeps one message per slide and ends with a clear recommended action.

## Phase 6 - Decision-Led Presentation Revision

Status: Complete

Reason for revision:

- The original deck presented methodology before the PM answer.
- Several slides behaved like a compressed report.
- The recommendation was delayed until the final slide.
- Technical content and stakeholder content had equal visual priority.

Changes:

- Put the PM decision and headline answer on slide 1.
- Moved metric definition and SQL logic to appendix slides.
- Rewrote slide titles as conclusions.
- Reframed device analysis as a ruled-out explanation.
- Reframed country analysis as a follow-up lead.
- Replaced the general limitations slide with a decision-boundary slide.
- Added a specific KPI monitoring and investigation plan.
- Preserved the user's PowerPoint layout edits and enlarged charts.

Revised file:

- `outputs/presentation/FINAL_product_analyst_time_to_purchase.pptx`

Verification:

- Rendered successfully to PDF.
- Reviewed all 10 slides in a contact sheet.
- Confirmed the main story follows decision -> evidence -> boundary -> action -> appendix.

## Phase 7 - Accuracy Fixes and Excel Visualization

Status: Complete

Accuracy fixes:

- Replaced the ambiguous 67.66-minute wording.
- Overall user-level average: 74.68 minutes.
- Overall user-level median: 19.07 minutes.
- Clarified that 67.66 minutes is the average of daily averages.
- Clarified that first recorded event per user-date is used as arrival.
- Added UTC date-boundary and session-definition limitations.

Excel deliverable:

- Created `outputs/FINAL_time_to_purchase_visualization.xlsx`.
- Added native Excel charts for daily duration, average versus median, purchase volume, device, and country.
- Included daily and user-level source data.
- Included a workbook README with metric definitions and limitations.

## Phase 8 - Review Feedback Notes

Status: Complete

Reviewer feedback:

- Median is a better headline metric than average because the data contains many outliers.
- p75 and p90 are relevant supporting quantiles for investigating longer same-day purchase durations.

Future improvements:

- Add a 7-day rolling median to smooth noisy daily movement from low-observation dates.
- Remove likely inactive time from duration calculations before operational use.
- Test whether longer time to purchase is associated with higher order value.
