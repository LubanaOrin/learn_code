# Data Analytics Capstone Project - Phase Plan

## Objective

Complete a portfolio-ready capstone analysis with a dashboard, 10-15 minute presentation with speaker notes, and written report.

The project must use a dataset that was not used in course Hands-On or Graded Tasks. The final work should tell one consistent story across all deliverables.

## Assignment Requirements

- Choose and document a unique data source.
- Explain the data context, including time period and business context.
- Define the target audience.
- State the problem being solved.
- State the hypothesis or hypotheses being tested.
- Use at least three course analysis techniques.
- Create an accessible dashboard.
- Create a presentation for 10-15 minutes with extensive speaker notes.
- Create a written report in Google Docs.
- Include final results, limitations, and future recommendations.
- Follow a structured analytical story, even if the six analysis steps are not listed directly.

## Lessons From Previous Work And Feedback

- Keep the final work self-contained so reviewers can understand it without extra explanation.
- Use exact numbers in summaries and conclusions.
- Avoid vague claims unless the data supports them.
- Use visualizations for important findings.
- Go deeper than surface-level exploratory analysis.
- Explain why each technique was used and what decision it supports.
- Include limitations clearly.
- Keep SQL, notebooks, outputs, reports, and presentation files organized for Git.
- Save SQL code in the repo so it is not lost if BigQuery access changes.
- Avoid relying only on BigQuery Sandbox storage because sandbox tables expire after 60 days.

## Supporting Documents Saved

- `notes/supporting-documents/Apple Company Analysis Report.pdf`
- `notes/supporting-documents/Simulation Analysis Report.pdf`
- `notes/supporting-documents/Fixing Data Set Configuration Error.pdf`

## Report Structure Guide From Examples

The example reports suggest this simple structure:

1. Executive summary
2. Introduction or project background
3. Data and business context
4. Approach or methodology
5. Analysis
6. Results
7. Conclusion
8. Recommendations
9. References

## Proposed Folder Structure

- `data/`: raw or exported datasets
- `sql/`: BigQuery SQL queries and saved analysis queries
- `notebooks/`: Python notebooks if used for cleaning, EDA, or modeling
- `outputs/`: charts, cleaned datasets, dashboard exports, report assets
- `notes/`: planning notes, feedback, supporting documents
- `phases/`: task plan and progress notes

## Phase 1 - Understand The Brief And Constraints

Status: Completed

What this phase covers:

- Read the capstone instructions.
- Save the supporting PDFs inside the task folder.
- Identify required deliverables and grading expectations.
- Capture previous feedback lessons that should guide the capstone.

Why this matters:

This project is broad. Before choosing a dataset or writing SQL, we need a clear checklist so the final dashboard, presentation, and report all answer the same business question.

## Phase 2 - Choose Dataset And Business Problem

Status: In progress

What this phase will cover:

- Choose an industry or role direction.
- Find candidate datasets.
- Check that the dataset was not used in course tasks.
- Confirm the dataset has enough columns, rows, and time/business context for at least three analysis techniques.
- Choose a clear target audience.

Progress:

- Created `notes/dataset-selection.md`.
- Shortlisted three dataset directions:
  - TheLook E-commerce
  - Olist Brazilian E-commerce
  - Citi Bike Trip Data
- Current recommendation is TheLook E-commerce because it supports funnel analysis, cohort analysis, RFM analysis, segmentation, and time-series analysis in one connected business story.
- Checked local terminal setup: `bq` and `gcloud` are not installed yet, so BigQuery command-line work will need setup later if we use it.
- Updated direction after user clarified the profile goal: the capstone should demonstrate quantitative research experience that can support future PhD applications.
- New recommendation is the Stack Overflow Annual Developer Survey, framed as a survey-based quantitative study about AI tool adoption, trust, and developer outcomes.

## Phase 3 - Define Techniques And Analysis Plan

Status: Completed

What this phase will cover:

- Select at least three course techniques.
- Define what question each technique answers.
- Decide which work should happen in SQL, Python, dashboard tool, and report.
- Create a first hypothesis list.

Progress:

- Created `notes/research-design.md`.
- Selected working title: **AI Tool Adoption, Trust, And Developer Outcomes: A Quantitative Survey Analysis**.
- Selected recommended dataset: Stack Overflow Developer Survey 2025.
- Kept Stack Overflow Developer Survey 2024 as fallback.
- Defined the main research question: **What factors are associated with AI tool adoption and trust among software developers?**
- Defined four hypotheses.
- Selected three required techniques:
  - Segmentation
  - Hypothesis testing
  - Regression or classification modeling
- Defined the dashboard, report, and presentation story.

Possible techniques, depending on the dataset:

- Cohort analysis
- Retention analysis
- Funnel analysis
- RFM analysis
- Segmentation
- A/B testing
- Time-series analysis
- Regression or classification modeling

## Phase 4 - Data Preparation

Status: In progress

What this phase will cover:

- Load or connect the dataset.
- Save raw data or source notes.
- Clean column names and values.
- Check missing values, duplicates, data types, and date ranges.
- Save SQL queries and cleaned outputs.

Progress:

- Tried to download the Stack Overflow 2025 and 2024 survey ZIP files from likely official dataset URL patterns.
- Both attempts returned small HTML 404 pages instead of valid ZIP files.
- Checked the local files and removed the invalid placeholder ZIPs.
- Added `data/README.md` to document the planned dataset, source pages, expected files, and current download status.
- User checked the Stack Overflow survey page and did not see a download option.
- Current decision: treat Stack Overflow as blocked unless a reliable raw-data link is found.
- Found local files that may support a quantitative survey-style capstone, but they may contain thesis-related respondent data and need user permission before inspection.
- User clarified that Suhkonen files are private university capstone work and must not be used.
- Checked Kaggle direction and selected OSMI Mental Health in Tech Survey as the current recommended public dataset.
- Checked local Kaggle setup: Kaggle CLI is not installed and no Kaggle API token was found.
- User provided the Kaggle archive as `/Users/lubana/Downloads/archive.zip`.
- Copied it into the project as `data/osmi-mental-health-in-tech-survey.zip`.
- Extracted `survey.csv` into `data/osmi-mental-health-in-tech-survey/`.
- Inspected the dataset:
  - 1,259 rows
  - 27 columns
  - one row per survey response
- Created `notes/osmi-dataset-inventory.md`.

Next action:

- Clean the dataset in a reproducible notebook.
- Standardize age and gender values.
- Create modeling variables for treatment-seeking and workplace support.
- Save a cleaned CSV in `outputs/`.

Completed cleaning outputs:

- Created `scripts/prepare_osmi_dataset.py`.
- Created `outputs/osmi_mental_health_cleaned.csv`.
- Created `outputs/osmi_data_quality_summary.csv`.
- Created `outputs/osmi_variable_dictionary.csv`.
- Created `notebooks/osmi_mental_health_analysis.ipynb`.

Cleaning decisions:

- Converted column names to snake_case.
- Treated ages outside 18-75 as missing.
- Grouped 49 raw gender values into 4 analysis categories.
- Created binary variables such as `treatment_yes`, `benefits_yes`, `care_options_yes`, `family_history_yes`, and `remote_work_yes`.
- Created ordered scores for work interference, leave difficulty, perceived consequences, and discussion comfort.

Verification:

- Cleaned dataset has 1,259 rows and 56 columns.
- 8 age values were invalid or outside the chosen 18-75 analysis range.
- 637 respondents, or 50.6%, reported seeking treatment.
- Notebook code cells were tested successfully.

## Phase 5 - Analysis And Dashboard

Status: In progress

What this phase will cover:

- Run the three selected techniques.
- Create charts and summary tables.
- Build the dashboard.
- Make sure the dashboard tells the same story as the report and presentation.

Progress:

- Created `scripts/analyze_osmi_dataset.py`.
- Created dashboard/report-ready summary tables in `outputs/`.
- Created hypothesis-test results in `outputs/hypothesis_test_results.csv`.
- Created logistic regression outputs:
  - `outputs/treatment_model_performance.csv`
  - `outputs/treatment_model_coefficients.csv`
- Created interactive chart files in `outputs/charts/`.
- Created `notes/analysis-results.md`.
- Created `scripts/build_analysis_notebook.py`.
- Rebuilt `notebooks/osmi_mental_health_analysis.ipynb` as the full analysis notebook.
- Verified the notebook JSON is valid.
- Verified all 8 notebook code cells run successfully.
- Created `scripts/build_dashboard.py`.
- Created static HTML dashboard:
  - `outputs/dashboard/osmi_mental_health_dashboard.html`
- Dashboard includes:
  - 6 KPI blocks
  - 5 Plotly chart panels
  - hypothesis-test table
  - treatment-seeking model summary
- Rebuilt dashboard with embedded Plotly JavaScript so it can be opened directly from the file.

Key early results:

- 637 respondents, or 50.6%, reported seeking mental health treatment.
- 477 respondents, or 37.9%, knew their employer provided mental health benefits.
- 782 respondents, or 62.1%, reported at least some work interference.
- 516 respondents, or 41.0%, were comfortable discussing mental health with a supervisor.
- 225 respondents, or 17.9%, were comfortable discussing mental health with coworkers.
- Logistic regression model ROC AUC: 0.891.
- Main hypothesis tests showed statistically significant associations at the 0.05 level.

Notebook structure:

- 25 total cells
- 17 markdown explanation cells
- 8 code cells
- Includes executive summary, dataset description, research question, hypotheses, techniques, data cleaning, segmentation, hypothesis testing, logistic regression, recommendations, limitations, and conclusion.

## Phase 6 - Written Report

Status: In progress

What this phase will cover:

- Draft the Google Docs report.
- Include executive summary, data source, methodology, analysis, limitations, recommendations, and references.
- Use exact numbers and clear business language.

Progress:

- Created written report draft:
  - `outputs/osmi_mental_health_written_report_draft.md`
- The draft includes:
  - executive summary
  - introduction
  - data source and context
  - target audience
  - research question
  - hypotheses
  - methodology
  - data preparation
  - analysis and results
  - logistic regression model
  - dashboard summary
  - recommendations
  - limitations
  - conclusion
  - references

## Phase 7 - Presentation

Status: Completed

What this phase will cover:

- Build a 10-15 minute presentation.
- Add extensive speaker notes.
- Keep the story aligned with the dashboard and report.
- Prepare a confident explanation of the problem, hypothesis, methods, findings, limitations, and recommendations.

Progress:

- Created `scripts/build_presentation.py`.
- Created editable PPTX presentation:
  - `outputs/presentation/osmi_mental_health_capstone_presentation.pptx`
- Created presentation PDF preview:
  - `outputs/presentation/osmi_mental_health_capstone_presentation.pdf`
- Created separate speaker-notes file:
  - `outputs/presentation/osmi_mental_health_speaker_notes.md`
- Presentation includes 11 slides:
  - title and project frame
  - research design and hypotheses
  - dataset and cleaning
  - treatment versus disclosure comfort
  - workplace support and treatment-seeking
  - work interference
  - disclosure risk
  - logistic regression model
  - recommendations
  - limitations
  - final takeaway

Verification:

- PPTX archive integrity check passed with no compressed-data errors.
- Presentation package contains 11 slide XML files and 11 matching notes XML files.
- Presentation was exported to an 11-page PDF and rendered into 11 slide preview images for visual QA.
- Separate speaker-notes file contains 444 words.

## Phase 8 - Final Review

Status: Completed

What this phase will cover:

- Check every assignment requirement.
- Confirm all files are saved in Git-friendly folders.
- Save SQL queries and dashboard recovery notes.
- Prepare final submission instructions.

Progress:

- Created final requirement checklist:
  - `notes/final-review-checklist.md`
- Created portfolio-facing project README:
  - `README.md`
- Created SQL/BigQuery note:
  - `sql/README.md`
- Created upload-ready report files:
  - `outputs/osmi_mental_health_written_report_upload_ready.docx`
  - `outputs/osmi_mental_health_written_report_upload_ready.pdf`
- Created static chart snippets for notebook and report:
  - `outputs/report_chart_assets/`
- Embedded six chart snippets in the written report.
- Added the six chart snippets to the analysis notebook as dashboard-style visuals.
- Created a Google Sheets-ready dashboard workbook for the required dashboard deliverable:
  - `outputs/google_sheets_dashboard/osmi_mental_health_google_sheets_dashboard.xlsx`
- Verified the workbook archive and confirmed it contains 6 sheets and 6 embedded chart images.
- Exported the dashboard workbook to PDF and visually checked the main Dashboard page after redesign.
- Rendered the updated report PDF into 10 PNG pages and visually checked the chart-embedded report layout.
- Created submission guide:
  - `notes/submission-guide.md`
- Rebuilt verified submission package with chart assets and preserved folder paths:
  - `outputs/data_analytics_capstone_submission_package.zip`
- Checked the capstone against the assignment requirements.
- Confirmed the current project is reproducible with Python scripts and saved CSV files.
- Confirmed BigQuery is optional for this capstone because all required analysis outputs are already reproducible locally.
- Identified remaining submission actions:
  - move the written report draft into Google Docs if a Google Docs link is required
  - upload or convert the PPTX to Google Slides if a Google Slides link is required
  - host or upload the dashboard HTML if a public dashboard link is required

## Open Decisions

- Final report location in Google Docs
- Dashboard hosting or upload method for final submission
