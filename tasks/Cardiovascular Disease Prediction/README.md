# Cardiovascular Disease Prediction

This project analyzes the Cardiovascular Study Dataset and fits a logistic regression model to predict 10-year coronary heart disease risk.

## Workflow

The final notebook is self-contained. Open and run:

```text
notebooks/cardiovascular_disease_prediction.ipynb
```

It loads the raw `data/train.csv`, performs cleaning and feature engineering, saves `outputs/cardiovascular_train_cleaned.csv`, and then continues into EDA, logistic regression, metric selection, threshold tuning, and coefficient interpretation.

## Review Upgrades Applied

- The notebook is self-contained for grading.
- Column names and categorical values are standardized.
- Feature engineering adds interpretable clinical signals such as pulse pressure, blood pressure stage, smoking intensity, high glucose, and high cholesterol flags.
- Model preprocessing uses a scikit-learn pipeline to avoid leakage.
- Evaluation focuses on recall/precision tradeoffs and an optimized threshold, which is more appropriate than default accuracy for imbalanced disease-risk screening.
