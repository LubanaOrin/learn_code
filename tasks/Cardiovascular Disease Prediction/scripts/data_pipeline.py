"""Clean and enrich the cardiovascular disease training dataset.

The script keeps target-independent cleaning and feature engineering outside the
analysis notebook. Model-specific imputation, scaling, and encoding are handled
inside the notebook pipeline to avoid train/test leakage.
"""

from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parents[1]
RAW_PATH = PROJECT_DIR / "data" / "train.csv"
CLEANED_PATH = PROJECT_DIR / "outputs" / "cardiovascular_train_cleaned.csv"


COLUMN_RENAMES = {
    "cigsPerDay": "cigs_per_day",
    "BPMeds": "bp_meds",
    "prevalentStroke": "prevalent_stroke",
    "prevalentHyp": "prevalent_hyp",
    "totChol": "total_cholesterol",
    "sysBP": "systolic_bp",
    "diaBP": "diastolic_bp",
    "BMI": "bmi",
    "heartRate": "heart_rate",
    "TenYearCHD": "ten_year_chd",
}


def load_raw_data(path: Path = RAW_PATH) -> pd.DataFrame:
    """Load the raw Kaggle training file."""
    return pd.read_csv(path)


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Apply stable snake_case names and remove the exported row identifier."""
    cleaned = df.rename(columns=COLUMN_RENAMES).copy()
    return cleaned.drop(columns=["id"])


def standardize_values(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize categorical values for display and modeling."""
    cleaned = df.copy()
    cleaned["sex"] = cleaned["sex"].astype(str).str.strip().str.upper()
    cleaned["is_smoking"] = cleaned["is_smoking"].astype(str).str.strip().str.title()
    return cleaned


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create clinically interpretable deterministic features."""
    enriched = df.copy()

    enriched["pulse_pressure"] = (
        enriched["systolic_bp"] - enriched["diastolic_bp"]
    )
    enriched["mean_arterial_pressure"] = (
        enriched["diastolic_bp"] + enriched["pulse_pressure"] / 3
    )

    enriched["age_group"] = pd.cut(
        enriched["age"],
        bins=[0, 39, 49, 59, 120],
        labels=["Under 40", "40-49", "50-59", "60+"],
        right=True,
    )

    enriched["bp_stage"] = pd.cut(
        enriched["systolic_bp"],
        bins=[0, 120, 130, 140, 1000],
        labels=["Normal", "Elevated", "Stage 1", "Stage 2"],
        right=False,
    )

    enriched["smoking_intensity"] = pd.cut(
        enriched["cigs_per_day"],
        bins=[-0.1, 0, 10, 20, 1000],
        labels=["Non-smoker", "Light", "Moderate", "Heavy"],
        right=True,
    )

    enriched["is_heavy_smoker"] = threshold_flag(enriched["cigs_per_day"], 20)
    enriched["has_high_glucose"] = threshold_flag(enriched["glucose"], 126)
    enriched["has_high_cholesterol"] = threshold_flag(
        enriched["total_cholesterol"], 240
    )
    enriched["log_cigs_per_day"] = np.log1p(enriched["cigs_per_day"])
    enriched["log_glucose"] = np.log1p(enriched["glucose"])

    return enriched


def threshold_flag(series: pd.Series, threshold: float) -> pd.Series:
    """Return 1/0 threshold flags while preserving missing source values."""
    return pd.Series(
        np.where(series.isna(), np.nan, series >= threshold),
        index=series.index,
        dtype="float",
    )


def validate_data(df: pd.DataFrame) -> None:
    """Fail fast if the cleaned dataset violates core assumptions."""
    assert set(df["ten_year_chd"].dropna().unique()).issubset({0, 1})
    assert set(df["sex"].dropna().unique()).issubset({"F", "M"})
    assert set(df["is_smoking"].dropna().unique()).issubset({"No", "Yes"})
    assert df["age"].between(18, 100).all()
    assert (df["pulse_pressure"] > 0).all()
    assert not df.duplicated().any()


def run_pipeline() -> pd.DataFrame:
    """Run the full cleaning pipeline and save the analysis-ready CSV."""
    cleaned = (
        load_raw_data()
        .pipe(standardize_columns)
        .pipe(standardize_values)
        .pipe(add_features)
    )
    validate_data(cleaned)
    CLEANED_PATH.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(CLEANED_PATH, index=False)
    return cleaned


if __name__ == "__main__":
    output = run_pipeline()
    print(f"Saved {len(output):,} rows and {output.shape[1]} columns to {CLEANED_PATH}")
