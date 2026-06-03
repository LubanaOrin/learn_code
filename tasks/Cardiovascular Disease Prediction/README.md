# Cardiovascular Disease Prediction

## Project Objective

This project analyzes the Cardiovascular Study Dataset and builds a logistic regression model to predict whether a patient has a 10-year risk of coronary heart disease (CHD).

The main focus is not only model fitting, but also explaining the full analytical workflow: data cleaning, feature engineering, variable selection, model evaluation, threshold optimization, and coefficient interpretation.

## Files for Submission

Recommended college Git upload structure:

```text
.
├── README.md
├── data/
│   └── train.csv
└── notebooks/
    └── cardiovascular_disease_prediction.ipynb
```

The notebook is self-contained and should be the main file reviewed.

## How to Run

1. Open the notebook:

```text
notebooks/cardiovascular_disease_prediction.ipynb
```

2. Make sure the dataset is available at:

```text
data/train.csv
```

3. Run the notebook from top to bottom.

The notebook loads the raw dataset, performs cleaning and feature engineering, saves a cleaned CSV in `outputs/`, performs exploratory analysis, fits logistic regression, selects an optimal threshold, and interprets the model.

## Methods Used

- Pandas and NumPy for data preparation
- Plotly, Matplotlib, and Seaborn for visualization
- Scikit-learn for preprocessing, logistic regression, cross-validation, and evaluation
- Median imputation for numeric missing values
- Most-frequent imputation for categorical missing values
- Standard scaling for numeric variables
- One-hot encoding for categorical variables
- Logistic regression with cross-validation

## Metric and Threshold Decision

The target variable is imbalanced: only about **15.1%** of patients are CHD-positive.

Because this is a screening-style healthcare problem, recall is more important than plain accuracy. Missing a high-risk patient is more harmful than sending an extra patient for follow-up.

For that reason, the notebook uses **F2 score** to select the decision threshold.

Key result:

- Default threshold `0.50`: recall `64.7%`, missed CHD cases `36`
- Optimized threshold `0.41`: recall `81.4%`, missed CHD cases `19`

The optimized threshold improves detection of CHD-risk patients, while accepting more false positives as a reasonable screening tradeoff.

## Main Findings

- Age, systolic blood pressure, male sex, smoking exposure, high glucose, hypertension history, and cholesterol are the strongest positive model signals.
- Accuracy alone is not appropriate because the majority class dominates the dataset.
- The model should be interpreted as a follow-up prioritization tool, not as a medical diagnosis.

## Limitations

- The dataset is observational, so coefficients describe association rather than causation.
- The positive class contains only 511 CHD cases, so the threshold should be validated on external data before real-world use.
- Important predictors such as family history, diet, exercise, and detailed medication history are unavailable.
