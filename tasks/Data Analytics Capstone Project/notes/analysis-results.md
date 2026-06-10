# Analysis Results Notes

## Current Analysis Outputs

Created by:

- `scripts/analyze_osmi_dataset.py`

Main output files:

- `outputs/executive_summary_metrics.csv`
- `outputs/hypothesis_test_results.csv`
- `outputs/treatment_model_performance.csv`
- `outputs/treatment_model_coefficients.csv`
- `outputs/treatment_by_benefits.csv`
- `outputs/treatment_by_care_options.csv`
- `outputs/treatment_by_family_history.csv`
- `outputs/treatment_by_work_interfere.csv`
- `outputs/charts/`

## Executive Summary Metrics

- Total survey responses: 1,259
- Respondents who sought mental health treatment: 637, or 50.6%
- Respondents who know their employer provides mental health benefits: 477, or 37.9%
- Respondents reporting any work interference: 782, or 62.1%
- Respondents comfortable discussing mental health with a supervisor: 516, or 41.0%
- Respondents comfortable discussing mental health with coworkers: 225, or 17.9%

## Hypothesis Test Results

All main chi-square tests showed statistically significant associations at the 0.05 level:

- Employer mental health benefits and treatment-seeking:
  - chi-square = 64.8386
  - p-value < 0.001
- Care options and treatment-seeking:
  - chi-square = 94.7587
  - p-value < 0.001
- Family history and treatment-seeking:
  - chi-square = 178.2668
  - p-value < 0.001
- Work interference and treatment-seeking:
  - chi-square = 594.9243
  - p-value < 0.001
- Expected mental health consequences and supervisor discussion comfort:
  - chi-square = 461.6603
  - p-value < 0.001
- Expected mental health consequences and coworker discussion comfort:
  - chi-square = 285.5339
  - p-value < 0.001

Company-size tests:

- Discussion comfort differs across company size groups:
  - Kruskal-Wallis statistic = 23.7876
  - p-value = 0.000238
- Leave difficulty did not show a statistically significant difference across company size groups at the 0.05 level:
  - Kruskal-Wallis statistic = 10.3592
  - p-value = 0.065674

## Logistic Regression Model

Target:

- `treatment_yes`

Model:

- Logistic regression

Performance:

- Train rows: 944
- Test rows: 315
- Accuracy: 0.819
- ROC AUC: 0.891
- Precision for treatment-seeking class: 0.797
- Recall for treatment-seeking class: 0.862
- F1 score for treatment-seeking class: 0.828

Strongest positive model signals:

- Work interference often
- Work interference sometimes
- Work interference rarely
- Family history of mental illness
- Comfort discussing mental health with coworkers
- Knowing employer provides care options
- Knowing employer provides mental health benefits

Important interpretation note:

The logistic regression shows association, not causation. For example, work interference is strongly related to treatment-seeking, but the model does not prove that work interference causes treatment.

## Current Story For Dashboard And Report

The data suggests a gap between treatment-seeking and workplace disclosure comfort:

- 50.6% of respondents sought treatment.
- 41.0% would discuss mental health with a supervisor.
- Only 17.9% would discuss mental health with coworkers.

This supports a capstone story about workplace mental health support, stigma, and disclosure risk:

1. Treatment-seeking is common in the survey sample.
2. Workplace support and care-option awareness are associated with treatment-seeking.
3. Perceived negative workplace consequences are strongly associated with lower comfort discussing mental health.
4. Work interference is strongly associated with treatment-seeking.
5. Recommendations should focus on benefit clarity, care access, anonymity, manager training, and reducing perceived disclosure risk.

## Cautions For Final Report

- The dataset is observational and cannot prove cause and effect.
- The respondents are not a random sample of all technology workers.
- The survey is self-reported.
- Some variables, such as `work_interfere`, may be closely connected to mental health status and treatment-seeking, so they should be interpreted as severity/context indicators rather than simple workplace policy variables.
- `Gender` required grouping from many raw self-reported values, which simplifies identity categories for analysis.
