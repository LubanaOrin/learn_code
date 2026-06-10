# Data Analytics Capstone Project

## Workplace Mental Health Disclosure And Support In The Technology Sector

This capstone analyzes the public OSMI Mental Health in Tech Survey from Kaggle to study workplace mental health treatment-seeking, support awareness, work interference, perceived consequences, and disclosure comfort among technology-sector respondents.

The project is designed as a quantitative research portfolio item. It demonstrates survey-data cleaning, segmentation, hypothesis testing, logistic regression/classification modeling, dashboard storytelling, written reporting, and presentation development.

## Research Question

What workplace and personal factors are associated with mental health treatment-seeking and disclosure comfort among technology workers?

## Dataset

- Source: https://www.kaggle.com/datasets/osmi/mental-health-in-tech-survey
- Raw rows: 1,259
- Raw columns: 27
- Cleaned columns: 56
- Unit of analysis: one survey response

## Techniques Used

1. Segmentation
2. Hypothesis testing
3. Logistic regression / classification modeling

## Key Results

- 637 respondents, or 50.6%, reported seeking mental health treatment.
- 477 respondents, or 37.9%, knew their employer provided mental health benefits.
- 782 respondents, or 62.1%, reported at least some work interference.
- 516 respondents, or 41.0%, were comfortable discussing mental health with a supervisor.
- 225 respondents, or 17.9%, were comfortable discussing mental health with coworkers.
- Logistic regression ROC AUC: 0.891.

## Main Deliverables

- Analysis notebook: `notebooks/osmi_mental_health_analysis.ipynb`
- Report chart assets: `outputs/report_chart_assets/`
- Google Sheets-ready dashboard workbook: `outputs/google_sheets_dashboard/osmi_mental_health_google_sheets_dashboard.xlsx`
- Supplementary HTML dashboard: `outputs/dashboard/osmi_mental_health_dashboard.html`
- Written report draft: `outputs/osmi_mental_health_written_report_draft.md`
- Upload-ready report DOCX: `outputs/osmi_mental_health_written_report_upload_ready.docx`
- Report PDF preview: `outputs/osmi_mental_health_written_report_upload_ready.pdf`
- Presentation: `outputs/presentation/osmi_mental_health_capstone_presentation.pptx`
- Presentation PDF preview: `outputs/presentation/osmi_mental_health_capstone_presentation.pdf`
- Speaker notes: `outputs/presentation/osmi_mental_health_speaker_notes.md`
- Final review checklist: `notes/final-review-checklist.md`
- Submission package ZIP: `outputs/data_analytics_capstone_submission_package.zip`

## Reproducibility

Run the scripts in this order from the project folder:

```bash
python3 scripts/prepare_osmi_dataset.py
python3 scripts/analyze_osmi_dataset.py
python3 scripts/build_report_charts.py
python3 scripts/build_analysis_notebook.py
python3 scripts/build_google_sheets_dashboard.py
python3 scripts/build_dashboard.py
python3 scripts/build_presentation.py
```

## Interpretation Note

The dataset is observational and self-reported. The findings show associations between workplace support, perceived consequences, work interference, and treatment-seeking, but they should not be interpreted as causal effects.
