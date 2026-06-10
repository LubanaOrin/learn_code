"""Run the first capstone analysis outputs for the OSMI survey."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
from scipy.stats import chi2_contingency, kruskal
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


TASK_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = TASK_DIR / "outputs" / "osmi_mental_health_cleaned.csv"
OUTPUT_DIR = TASK_DIR / "outputs"
CHART_DIR = OUTPUT_DIR / "charts"


def pct(value: float) -> float:
    return round(value * 100, 1)


def treatment_summary(df: pd.DataFrame, group_col: str) -> pd.DataFrame:
    summary = (
        df.groupby(group_col, dropna=False)
        .agg(
            respondents=("response_id", "count"),
            treatment_count=("treatment_yes", "sum"),
            treatment_rate=("treatment_yes", "mean"),
        )
        .reset_index()
    )
    summary["treatment_rate_percent"] = (summary["treatment_rate"] * 100).round(1)
    return summary.sort_values(
        ["treatment_rate_percent", "respondents"], ascending=[False, False]
    )


def chi_square_test(df: pd.DataFrame, row_col: str, target_col: str) -> dict:
    table = pd.crosstab(df[row_col], df[target_col])
    chi2, p_value, dof, expected = chi2_contingency(table)
    return {
        "test": "chi-square",
        "question": f"Association between {row_col} and {target_col}",
        "variable_1": row_col,
        "variable_2": target_col,
        "chi2": round(float(chi2), 4),
        "degrees_of_freedom": int(dof),
        "p_value": round(float(p_value), 6),
        "significant_at_0_05": bool(p_value < 0.05),
        "table_rows": int(table.shape[0]),
        "table_columns": int(table.shape[1]),
    }


def kruskal_test(df: pd.DataFrame, group_col: str, score_col: str) -> dict:
    usable = df[[group_col, score_col]].dropna()
    groups = [group[score_col].values for _, group in usable.groupby(group_col)]
    statistic, p_value = kruskal(*groups)
    return {
        "test": "kruskal-wallis",
        "question": f"Difference in {score_col} across {group_col}",
        "variable_1": group_col,
        "variable_2": score_col,
        "statistic": round(float(statistic), 4),
        "p_value": round(float(p_value), 6),
        "significant_at_0_05": bool(p_value < 0.05),
        "groups": int(usable[group_col].nunique()),
        "usable_rows": int(len(usable)),
    }


def build_model(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    model_df = df[
        [
            "treatment_yes",
            "age_clean",
            "gender_clean",
            "family_history",
            "work_interfere",
            "no_employees",
            "remote_work",
            "tech_company",
            "benefits",
            "care_options",
            "wellness_program",
            "seek_help",
            "anonymity",
            "leave",
            "mental_health_consequence",
            "coworkers",
            "supervisor",
            "obs_consequence",
        ]
    ].copy()

    x = model_df.drop(columns=["treatment_yes"])
    y = model_df["treatment_yes"]

    numeric_features = ["age_clean"]
    categorical_features = [col for col in x.columns if col not in numeric_features]

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "numeric",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scaler", StandardScaler()),
                    ]
                ),
                numeric_features,
            ),
            (
                "categorical",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        (
                            "onehot",
                            OneHotEncoder(handle_unknown="ignore", drop="first"),
                        ),
                    ]
                ),
                categorical_features,
            ),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "classifier",
                LogisticRegression(max_iter=1000, class_weight="balanced"),
            ),
        ]
    )

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=42, stratify=y
    )
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)
    y_prob = model.predict_proba(x_test)[:, 1]

    report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
    performance = pd.DataFrame(
        [
            {
                "model": "Logistic regression",
                "target": "treatment_yes",
                "train_rows": len(x_train),
                "test_rows": len(x_test),
                "accuracy": round(float(accuracy_score(y_test, y_pred)), 3),
                "roc_auc": round(float(roc_auc_score(y_test, y_prob)), 3),
                "precision_treatment_yes": round(report["1"]["precision"], 3),
                "recall_treatment_yes": round(report["1"]["recall"], 3),
                "f1_treatment_yes": round(report["1"]["f1-score"], 3),
            }
        ]
    )

    feature_names = model.named_steps["preprocessor"].get_feature_names_out()
    coefficients = model.named_steps["classifier"].coef_[0]
    coefficients_df = pd.DataFrame(
        {
            "feature": feature_names,
            "coefficient": coefficients,
            "odds_ratio": np.exp(coefficients),
        }
    )
    coefficients_df["abs_coefficient"] = coefficients_df["coefficient"].abs()
    coefficients_df = coefficients_df.sort_values(
        "abs_coefficient", ascending=False
    ).drop(columns="abs_coefficient")
    coefficients_df["coefficient"] = coefficients_df["coefficient"].round(4)
    coefficients_df["odds_ratio"] = coefficients_df["odds_ratio"].round(3)

    return performance, coefficients_df


def save_charts(df: pd.DataFrame, summaries: dict[str, pd.DataFrame]) -> None:
    CHART_DIR.mkdir(parents=True, exist_ok=True)

    treatment_counts = (
        df["treatment"]
        .value_counts()
        .rename_axis("treatment")
        .reset_index(name="respondents")
    )
    fig = px.bar(
        treatment_counts,
        x="treatment",
        y="respondents",
        title="Mental Health Treatment-Seeking Among Respondents",
        text="respondents",
    )
    fig.write_html(CHART_DIR / "treatment_overview.html", include_plotlyjs="cdn")

    benefits = summaries["treatment_by_benefits"].copy()
    fig = px.bar(
        benefits,
        x="benefits",
        y="treatment_rate_percent",
        text="treatment_rate_percent",
        title="Treatment-Seeking Rate By Employer Mental Health Benefits",
        labels={"treatment_rate_percent": "Treatment rate (%)"},
    )
    fig.write_html(CHART_DIR / "treatment_by_benefits.html", include_plotlyjs="cdn")

    work = summaries["treatment_by_work_interfere"].copy()
    fig = px.bar(
        work,
        x="work_interfere",
        y="treatment_rate_percent",
        text="treatment_rate_percent",
        title="Treatment-Seeking Rate By Work Interference",
        labels={"treatment_rate_percent": "Treatment rate (%)"},
    )
    fig.write_html(
        CHART_DIR / "treatment_by_work_interference.html", include_plotlyjs="cdn"
    )

    supervisor = (
        df.groupby(["mental_health_consequence", "supervisor"], dropna=False)
        .size()
        .reset_index(name="respondents")
    )
    fig = px.bar(
        supervisor,
        x="mental_health_consequence",
        y="respondents",
        color="supervisor",
        barmode="group",
        title="Supervisor Discussion Comfort By Expected Mental Health Consequences",
    )
    fig.write_html(
        CHART_DIR / "supervisor_comfort_by_consequence.html", include_plotlyjs="cdn"
    )


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(INPUT_PATH)

    summaries = {
        "treatment_by_benefits": treatment_summary(df, "benefits"),
        "treatment_by_care_options": treatment_summary(df, "care_options"),
        "treatment_by_family_history": treatment_summary(df, "family_history"),
        "treatment_by_work_interfere": treatment_summary(df, "work_interfere"),
        "treatment_by_company_size": treatment_summary(df, "no_employees"),
        "treatment_by_remote_work": treatment_summary(df, "remote_work"),
        "treatment_by_tech_company": treatment_summary(df, "tech_company"),
        "treatment_by_gender_clean": treatment_summary(df, "gender_clean"),
    }

    for name, table in summaries.items():
        table.to_csv(OUTPUT_DIR / f"{name}.csv", index=False)

    tests = pd.DataFrame(
        [
            chi_square_test(df, "benefits", "treatment"),
            chi_square_test(df, "care_options", "treatment"),
            chi_square_test(df, "family_history", "treatment"),
            chi_square_test(df, "work_interfere", "treatment"),
            chi_square_test(df, "mental_health_consequence", "supervisor"),
            chi_square_test(df, "mental_health_consequence", "coworkers"),
            chi_square_test(df, "remote_work", "benefits"),
            chi_square_test(df, "tech_company", "benefits"),
            kruskal_test(df, "no_employees", "discussion_comfort_score"),
            kruskal_test(df, "no_employees", "leave_difficulty_score"),
        ]
    )
    tests.to_csv(OUTPUT_DIR / "hypothesis_test_results.csv", index=False)

    model_performance, model_coefficients = build_model(df)
    model_performance.to_csv(OUTPUT_DIR / "treatment_model_performance.csv", index=False)
    model_coefficients.to_csv(OUTPUT_DIR / "treatment_model_coefficients.csv", index=False)

    executive_summary = pd.DataFrame(
        [
            {"metric": "Total survey responses", "value": len(df)},
            {
                "metric": "Sought mental health treatment",
                "value": f"{int(df['treatment_yes'].sum())} respondents ({pct(df['treatment_yes'].mean())}%)",
            },
            {
                "metric": "Know employer provides mental health benefits",
                "value": f"{int(df['benefits_yes'].sum())} respondents ({pct(df['benefits_yes'].mean())}%)",
            },
            {
                "metric": "Report any work interference",
                "value": f"{int(df['work_interfere_any'].sum())} respondents ({pct(df['work_interfere_any'].mean())}%)",
            },
            {
                "metric": "Comfortable discussing mental health with supervisor",
                "value": f"{int(df['comfortable_with_supervisor'].sum())} respondents ({pct(df['comfortable_with_supervisor'].mean())}%)",
            },
            {
                "metric": "Comfortable discussing mental health with coworkers",
                "value": f"{int(df['comfortable_with_coworkers'].sum())} respondents ({pct(df['comfortable_with_coworkers'].mean())}%)",
            },
            {
                "metric": "Logistic model ROC AUC",
                "value": float(model_performance.loc[0, "roc_auc"]),
            },
        ]
    )
    executive_summary.to_csv(OUTPUT_DIR / "executive_summary_metrics.csv", index=False)

    save_charts(df, summaries)

    print("Saved analysis tables, hypothesis tests, model outputs, and charts.")


if __name__ == "__main__":
    main()
