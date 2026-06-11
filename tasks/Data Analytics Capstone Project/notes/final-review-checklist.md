# Final Review Checklist

## Project Identity

- Project title: **Workplace Mental Health Disclosure And Support In The Technology Sector: A Quantitative Survey Analysis**
- Dataset: OSMI Mental Health in Tech Survey
- Source: https://www.kaggle.com/datasets/osmi/mental-health-in-tech-survey
- Target audience: PhD admissions or research reviewers, workplace wellbeing researchers, HR analytics teams, and technology employers.
- Main research question: What workplace and personal factors are associated with mental health treatment-seeking and disclosure comfort among technology workers?

## College Requirement Check

| Requirement | Status | Evidence |
|---|---:|---|
| Choose a unique dataset not used in course graded or hands-on tasks | Ready | Public Kaggle OSMI survey dataset saved in `data/` |
| Provide quick introduction to the data source | Ready | Written report, dashboard, notebook, and `notes/osmi-dataset-inventory.md` |
| Explain data context and business/research context | Ready | Written report sections: Introduction, Data Source And Context |
| Explain targeted audience | Ready | Written report and `notes/research-design.md` |
| State problem and hypothesis | Ready | Written report and notebook |
| Use at least three learned techniques | Ready | Segmentation, hypothesis testing, logistic regression/classification |
| Dashboard is accessible | Ready | Google Sheets-ready XLSX dashboard is saved in `outputs/google_sheets_dashboard/` |
| Presentation is 10-15 minutes with speaker notes | Ready | 11-slide PPTX and separate speaker-notes Markdown file |
| Written report exists | Draft ready | Markdown report draft saved; still needs transfer to Google Docs if required for submission |
| Results are consistent across deliverables | Ready | Same figures used in notebook, dashboard, report, and presentation |
| Include limitations and recommendations | Ready | Written report, presentation, and analysis notes |

## Required Techniques

### 1. Segmentation

Used to compare treatment-seeking, disclosure comfort, and workplace-support indicators across groups including benefits, care options, family history, work interference, company size, remote work, and tech-company status.

Main evidence files:

- `outputs/treatment_by_benefits.csv`
- `outputs/treatment_by_care_options.csv`
- `outputs/treatment_by_family_history.csv`
- `outputs/treatment_by_work_interfere.csv`
- `outputs/treatment_by_company_size.csv`

### 2. Hypothesis Testing

Used chi-square tests for categorical relationships and Kruskal-Wallis tests for ordered scores across company-size groups.

Main evidence file:

- `outputs/hypothesis_test_results.csv`

Key results:

- Benefits and treatment-seeking: chi-square = 64.8386, p-value < 0.001
- Care options and treatment-seeking: chi-square = 94.7587, p-value < 0.001
- Family history and treatment-seeking: chi-square = 178.2668, p-value < 0.001
- Work interference and treatment-seeking: chi-square = 594.9243, p-value < 0.001
- Mental-health consequences and supervisor comfort: chi-square = 461.6603, p-value < 0.001
- Mental-health consequences and coworker comfort: chi-square = 285.5339, p-value < 0.001
- Company size and discussion comfort: Kruskal-Wallis p-value = 0.000238

### 3. Logistic Regression / Classification Modeling

Used logistic regression to predict whether respondents sought mental health treatment.

Main evidence files:

- `outputs/treatment_model_performance.csv`
- `outputs/treatment_model_coefficients.csv`

Key performance:

- ROC AUC: 0.891
- Accuracy: 0.819
- Recall for treatment-seeking class: 0.862
- Precision for treatment-seeking class: 0.797
- F1 score for treatment-seeking class: 0.828

## Deliverable Locations

- Raw dataset ZIP: `data/osmi-mental-health-in-tech-survey.zip`
- Extracted raw CSV: `data/osmi-mental-health-in-tech-survey/survey.csv`
- SQL notes: `sql/README.md`
- Cleaned dataset: `outputs/osmi_mental_health_cleaned.csv`
- Notebook: `notebooks/osmi_mental_health_analysis.ipynb`
- Report chart assets: `outputs/report_chart_assets/`
- Google Sheets-ready dashboard workbook: `outputs/google_sheets_dashboard/osmi_mental_health_google_sheets_dashboard.xlsx`
- Supplementary HTML dashboard: `outputs/dashboard/osmi_mental_health_dashboard.html`
- Written report draft: `outputs/osmi_mental_health_written_report_draft.md`
- Upload-ready report DOCX: `outputs/osmi_mental_health_written_report.docx`
- Report PDF preview: `outputs/osmi_mental_health_written_report.pdf`
- Presentation: `outputs/presentation/osmi_mental_health_capstone_presentation.pptx`
- Presentation PDF preview: `outputs/presentation/osmi_mental_health_capstone_presentation.pdf`
- Rendered presentation QA images: `outputs/presentation/rendered_slides/`
- Speaker notes: `outputs/presentation/osmi_mental_health_speaker_notes.md`
- Analysis notes: `notes/analysis-results.md`
- Research design: `notes/research-design.md`
- Submission package ZIP: `outputs/data_analytics_capstone_submission_package.zip`

## Verification Completed

- Cleaned dataset has 1,259 rows and 57 columns.
- Notebook has 25 cells, including 17 markdown cells and 8 code cells.
- Notebook contains six static chart references for dashboard-style visual review.
- All notebook code cells were tested successfully.
- Report includes six embedded chart snippets from `outputs/report_chart_assets/`.
- Google Sheets-ready dashboard workbook contains 6 sheets, a focused Dashboard sheet with 4 embedded chart images, and an Additional_Charts sheet with 2 supporting chart images.
- Supplementary HTML dashboard was rebuilt with embedded Plotly JavaScript for standalone access.
- Written report DOCX was exported from Markdown and visually checked through a 7-page PDF render.
- PPTX archive integrity check passed with no compressed-data errors.
- Presentation package contains 11 slides and 11 matching notes sections.
- Presentation was exported to an 11-page PDF and rendered into 11 slide preview images for visual QA.
- BigQuery SQL is documented as optional because the selected dataset is a single survey CSV and the project is reproducible locally.
- Submission package ZIP was created and passed archive integrity verification.

## Remaining Submission Actions

- Transfer the written report draft into Google Docs if the platform requires a Google Docs link.
- Upload or convert the PPTX to Google Slides if the platform requires a Google Slides link.
- Upload or host the dashboard somewhere accessible if local HTML upload is not accepted.

## Final Interpretation To Keep Consistent

The analysis shows that mental health treatment-seeking is common in this survey sample, but workplace disclosure comfort is much lower. Workplace benefit awareness, care options, work interference, family history, and expected consequences are strongly associated with treatment-seeking or disclosure comfort. Because the data is observational and self-reported, the findings should be interpreted as associations rather than causal effects.
