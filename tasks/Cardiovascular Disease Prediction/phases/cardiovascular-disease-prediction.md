# Cardiovascular Disease Prediction - Phase Plan

## Objective

Analyze the cardiovascular study training dataset and build an interpretable logistic regression model for 10-year coronary heart disease risk.

## Evaluation Focus

- Follow the expected modeling workflow.
- Explain variable selection and transformations.
- Interpret performance metrics and coefficients.
- Choose a classification metric and calculate an optimal threshold.
- Present clear, useful, and actionable insights.
- Follow Python best practices.

## Upgrade Standard

This task intentionally applies reviewer feedback from the Spotify and Coursera projects:

- Keep ETL in `scripts/data_pipeline.py`.
- Keep the notebook focused on analysis and presentation.
- Use vectorized Pandas operations.
- Standardize dataframe values, not only column names.
- Despine charts globally for stronger data-ink ratio.
- Add deeper engineered features rather than stopping at surface-level EDA.
- Use a healthcare-aware metric and threshold instead of relying on default accuracy.

## Planned Deliverables

- `data/train.csv`: raw graded dataset.
- `outputs/cardiovascular_train_cleaned.csv`: cleaned and feature-enriched data.
- `notebooks/cardiovascular_disease_prediction.ipynb`: final analysis notebook.
- `outputs/charts/`: reusable chart exports.
- `outputs/model_performance_summary.csv`: model comparison and threshold summary.
