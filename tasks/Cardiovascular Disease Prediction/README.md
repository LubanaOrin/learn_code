# Cardiovascular Disease Prediction

This project analyzes the Cardiovascular Study Dataset and fits a logistic regression model to predict 10-year coronary heart disease risk.

## Workflow

1. Run the cleaning pipeline:

   ```bash
   python3 scripts/data_pipeline.py
   ```

2. Open and run:

   ```text
   notebooks/cardiovascular_disease_prediction.ipynb
   ```

The pipeline saves `outputs/cardiovascular_train_cleaned.csv`. The notebook starts from that cleaned file and focuses on EDA, model creation, metric selection, threshold tuning, coefficient interpretation, and presentation-ready insights.

## Review Upgrades Applied

- Cleaning is modularized into a script instead of mixed into the notebook.
- Column names and categorical values are standardized.
- Feature engineering adds interpretable clinical signals such as pulse pressure, blood pressure stage, smoking intensity, high glucose, and high cholesterol flags.
- Model preprocessing uses a scikit-learn pipeline to avoid leakage.
- Evaluation focuses on recall/precision tradeoffs and an optimized threshold, which is more appropriate than default accuracy for imbalanced disease-risk screening.
