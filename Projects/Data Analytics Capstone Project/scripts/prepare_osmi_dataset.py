"""Prepare the OSMI Mental Health in Tech survey dataset.

This script keeps the cleaning step reproducible:
- reads the raw Kaggle CSV
- standardizes column names
- fixes obvious data quality issues
- creates analysis-ready variables
- saves cleaned outputs
- writes a starter notebook that documents the workflow
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np
import pandas as pd


TASK_DIR = Path(__file__).resolve().parents[1]
RAW_PATH = TASK_DIR / "data" / "osmi-mental-health-in-tech-survey" / "survey.csv"
OUTPUT_DIR = TASK_DIR / "outputs"
NOTEBOOK_DIR = TASK_DIR / "notebooks"

CLEANED_PATH = OUTPUT_DIR / "osmi_mental_health_cleaned.csv"
QUALITY_PATH = OUTPUT_DIR / "osmi_data_quality_summary.csv"
VARIABLE_DICT_PATH = OUTPUT_DIR / "osmi_variable_dictionary.csv"
NOTEBOOK_PATH = NOTEBOOK_DIR / "osmi_mental_health_analysis.ipynb"


def to_snake_case(name: str) -> str:
    """Convert a column name into a simple snake_case name."""
    name = name.strip()
    name = re.sub(r"[^0-9a-zA-Z]+", "_", name)
    name = re.sub(r"_+", "_", name)
    return name.strip("_").lower()


def clean_gender(value: object) -> str:
    """Group many raw gender responses into broader analysis categories."""
    if pd.isna(value):
        return "Missing"

    text = str(value).strip().lower()
    text = re.sub(r"[^a-z\s-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    if not text:
        return "Missing"

    female_terms = {
        "female",
        "f",
        "woman",
        "woman",
        "cis female",
        "cis-female",
        "cis woman",
        "female cis",
        "female woman",
    }
    male_terms = {
        "male",
        "m",
        "man",
        "cis male",
        "cis-male",
        "male cis",
        "male-ish",
        "maile",
        "mal",
        "msle",
        "mail",
        "make",
        "malr",
        "guy",
    }

    gender_diverse_keywords = [
        "trans",
        "non-binary",
        "non binary",
        "genderqueer",
        "agender",
        "androgyne",
        "fluid",
        "queer",
        "neuter",
        "enby",
    ]

    if text in female_terms or text.startswith("female"):
        return "Female"
    if text in male_terms or text.startswith("male"):
        return "Male"
    if any(keyword in text for keyword in gender_diverse_keywords):
        return "Non-binary / gender diverse"
    if text in {"nah", "all", "something kinda male", "ostensibly male unsure what that really means"}:
        return "Other / unclear"

    return "Other / unclear"


def yes_no_flag(series: pd.Series, yes_value: str = "Yes") -> pd.Series:
    """Create a 1/0 flag where the selected yes_value is 1."""
    return series.eq(yes_value).astype(int)


def prepare_dataset() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    raw = pd.read_csv(RAW_PATH)
    df = raw.copy()
    df.columns = [to_snake_case(col) for col in df.columns]

    df["response_id"] = np.arange(1, len(df) + 1)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    df["age_raw"] = df["age"]
    df["age"] = pd.to_numeric(df["age"], errors="coerce")
    df["age_clean"] = df["age"].where(df["age"].between(18, 75))
    df["age_group"] = pd.cut(
        df["age_clean"],
        bins=[17, 24, 34, 44, 54, 64, 75],
        labels=["18-24", "25-34", "35-44", "45-54", "55-64", "65-75"],
        include_lowest=True,
    )

    df["gender_raw"] = df["gender"]
    df["gender_clean"] = df["gender"].apply(clean_gender)

    for col in [
        "self_employed",
        "family_history",
        "treatment",
        "remote_work",
        "tech_company",
        "benefits",
        "care_options",
        "wellness_program",
        "seek_help",
        "anonymity",
        "mental_health_consequence",
        "phys_health_consequence",
        "mental_vs_physical",
        "obs_consequence",
    ]:
        df[col] = df[col].fillna("Missing")

    df["work_interfere"] = df["work_interfere"].fillna("Missing")
    df["state"] = df["state"].fillna("Not applicable / missing")
    df["comments"] = df["comments"].fillna("")

    df["treatment_yes"] = yes_no_flag(df["treatment"])
    df["self_employed_yes"] = yes_no_flag(df["self_employed"])
    df["family_history_yes"] = yes_no_flag(df["family_history"])
    df["remote_work_yes"] = yes_no_flag(df["remote_work"])
    df["tech_company_yes"] = yes_no_flag(df["tech_company"])
    df["benefits_yes"] = yes_no_flag(df["benefits"])
    df["care_options_yes"] = yes_no_flag(df["care_options"])
    df["wellness_program_yes"] = yes_no_flag(df["wellness_program"])
    df["seek_help_yes"] = yes_no_flag(df["seek_help"])
    df["anonymity_yes"] = yes_no_flag(df["anonymity"])
    df["observed_consequence_yes"] = yes_no_flag(df["obs_consequence"])

    consequence_map = {"No": 0, "Maybe": 1, "Yes": 2, "Missing": np.nan}
    df["mental_health_consequence_score"] = df["mental_health_consequence"].map(
        consequence_map
    )
    df["physical_health_consequence_score"] = df["phys_health_consequence"].map(
        consequence_map
    )

    discussion_map = {"No": 0, "Some of them": 1, "Yes": 2, "Missing": np.nan}
    df["coworker_discussion_score"] = df["coworkers"].map(discussion_map)
    df["supervisor_discussion_score"] = df["supervisor"].map(discussion_map)
    df["discussion_comfort_score"] = df[
        ["coworker_discussion_score", "supervisor_discussion_score"]
    ].mean(axis=1)
    df["comfortable_with_supervisor"] = df["supervisor"].eq("Yes").astype(int)
    df["comfortable_with_coworkers"] = df["coworkers"].eq("Yes").astype(int)

    work_interfere_map = {
        "Never": 0,
        "Rarely": 1,
        "Sometimes": 2,
        "Often": 3,
        "Missing": np.nan,
    }
    df["work_interfere_score"] = df["work_interfere"].map(work_interfere_map)
    df["work_interfere_any"] = df["work_interfere"].isin(
        ["Rarely", "Sometimes", "Often"]
    ).astype(int)

    leave_map = {
        "Very easy": 1,
        "Somewhat easy": 2,
        "Don't know": 3,
        "Somewhat difficult": 4,
        "Very difficult": 5,
    }
    df["leave_difficulty_score"] = df["leave"].map(leave_map)
    df["leave_difficult"] = df["leave"].isin(
        ["Somewhat difficult", "Very difficult"]
    ).astype(int)

    company_size_map = {
        "1-5": 1,
        "6-25": 2,
        "26-100": 3,
        "100-500": 4,
        "500-1000": 5,
        "More than 1000": 6,
    }
    company_size_label_map = {
        "1-5": "1 to 5",
        "6-25": "6 to 25",
        "26-100": "26 to 100",
        "100-500": "101 to 500",
        "500-1000": "501 to 1000",
        "More than 1000": "More than 1000",
    }
    df["company_size_order"] = df["no_employees"].map(company_size_map)
    df["company_size_label"] = df["no_employees"].map(company_size_label_map)

    raw_missing = raw.isna().sum().sum()
    raw_age = pd.to_numeric(raw["Age"], errors="coerce")
    invalid_age_count = int((~raw_age.between(18, 75)).sum())

    quality = pd.DataFrame(
        [
            {"metric": "raw_rows", "value": len(raw)},
            {"metric": "raw_columns", "value": raw.shape[1]},
            {"metric": "cleaned_rows", "value": len(df)},
            {"metric": "cleaned_columns", "value": df.shape[1]},
            {"metric": "raw_missing_values", "value": int(raw_missing)},
            {
                "metric": "invalid_or_out_of_range_age_values",
                "value": invalid_age_count,
            },
            {"metric": "raw_gender_unique_values", "value": raw["Gender"].nunique()},
            {
                "metric": "cleaned_gender_categories",
                "value": df["gender_clean"].nunique(),
            },
            {
                "metric": "treatment_yes_count",
                "value": int(df["treatment_yes"].sum()),
            },
            {
                "metric": "treatment_yes_percent",
                "value": round(df["treatment_yes"].mean() * 100, 1),
            },
        ]
    )

    variable_dict = pd.DataFrame(
        [
            {
                "variable": "treatment_yes",
                "type": "outcome",
                "description": "1 if respondent has sought mental health treatment, else 0.",
            },
            {
                "variable": "comfortable_with_supervisor",
                "type": "outcome",
                "description": "1 if respondent would discuss mental health with a supervisor, else 0.",
            },
            {
                "variable": "comfortable_with_coworkers",
                "type": "outcome",
                "description": "1 if respondent would discuss mental health with coworkers, else 0.",
            },
            {
                "variable": "work_interfere_score",
                "type": "predictor",
                "description": "Ordered score for whether mental health interferes with work.",
            },
            {
                "variable": "benefits_yes",
                "type": "predictor",
                "description": "1 if respondent knows employer provides mental health benefits.",
            },
            {
                "variable": "care_options_yes",
                "type": "predictor",
                "description": "1 if respondent knows employer provides mental health care options.",
            },
            {
                "variable": "family_history_yes",
                "type": "predictor",
                "description": "1 if respondent has family history of mental illness.",
            },
            {
                "variable": "mental_health_consequence_score",
                "type": "predictor",
                "description": "Perceived negative consequence score: No=0, Maybe=1, Yes=2.",
            },
            {
                "variable": "leave_difficulty_score",
                "type": "predictor",
                "description": "Ordered score for difficulty taking mental health leave.",
            },
            {
                "variable": "gender_clean",
                "type": "control",
                "description": "Grouped gender category based on raw self-reported gender.",
            },
            {
                "variable": "age_clean",
                "type": "control",
                "description": "Age after treating values outside 18-75 as missing.",
            },
            {
                "variable": "company_size_order",
                "type": "control",
                "description": "Ordered company size category.",
            },
            {
                "variable": "company_size_label",
                "type": "display",
                "description": "Spreadsheet-safe company size label used in report, dashboard, and presentation outputs.",
            },
        ]
    )

    return df, quality, variable_dict


def make_notebook() -> dict:
    """Create a starter notebook as JSON."""
    cells = [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Workplace Mental Health Disclosure And Support In The Technology Sector\n",
                "\n",
                "## A Quantitative Survey Analysis\n",
                "\n",
                "This notebook prepares the OSMI Mental Health in Tech Survey for the capstone analysis. The goal is to show a reproducible quantitative research workflow: data loading, cleaning, variable creation, quality checks, and preparation for hypothesis testing and modeling.",
            ],
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Dataset Description\n",
                "\n",
                "- Source: OSMI Mental Health in Tech Survey on Kaggle.\n",
                "- Raw file: `data/osmi-mental-health-in-tech-survey/survey.csv`.\n",
                "- One row represents one survey response.\n",
                "- The dataset includes workplace support, mental health treatment, disclosure comfort, work interference, and demographic/work context variables.",
            ],
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Research Question\n",
                "\n",
                "**What workplace and personal factors are associated with mental health treatment-seeking and disclosure comfort among technology workers?**",
            ],
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Hypotheses\n",
                "\n",
                "1. Respondents who know their employer provides mental health benefits are more likely to seek treatment.\n",
                "2. Respondents who expect negative workplace consequences are less comfortable discussing mental health with supervisors or coworkers.\n",
                "3. Respondents whose mental health interferes with work are more likely to have sought treatment.\n",
                "4. Workplace support indicators differ by company size, remote work status, and whether the employer is primarily a tech company.",
            ],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "from pathlib import Path\n",
                "\n",
                "import numpy as np\n",
                "import pandas as pd\n",
                "\n",
                "TASK_DIR = Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()\n",
                "RAW_PATH = TASK_DIR / 'data' / 'osmi-mental-health-in-tech-survey' / 'survey.csv'\n",
                "CLEANED_PATH = TASK_DIR / 'outputs' / 'osmi_mental_health_cleaned.csv'\n",
                "QUALITY_PATH = TASK_DIR / 'outputs' / 'osmi_data_quality_summary.csv'\n",
                "\n",
                "raw_df = pd.read_csv(RAW_PATH)\n",
                "clean_df = pd.read_csv(CLEANED_PATH)\n",
                "quality_df = pd.read_csv(QUALITY_PATH)\n",
                "\n",
                "raw_df.shape, clean_df.shape",
            ],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "quality_df",
            ],
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Why Cleaning Was Needed\n",
                "\n",
                "Survey datasets often contain inconsistent self-reported values. In this dataset, age includes impossible values and gender has many raw text variations. Cleaning makes the dataset easier to analyze and helps avoid misleading results.",
            ],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "clean_df[['age_clean', 'gender_clean', 'treatment', 'benefits', 'work_interfere']].head()",
            ],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "summary = pd.Series({\n",
                "    'responses': clean_df['response_id'].count(),\n",
                "    'treatment_rate_percent': clean_df['treatment_yes'].mean() * 100,\n",
                "    'benefits_known_rate_percent': clean_df['benefits_yes'].mean() * 100,\n",
                "    'family_history_rate_percent': clean_df['family_history_yes'].mean() * 100,\n",
                "    'remote_work_rate_percent': clean_df['remote_work_yes'].mean() * 100,\n",
                "})\n",
                "summary.round(1)",
            ],
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Next Analysis Steps\n",
                "\n",
                "- Segment treatment-seeking by workplace benefits, family history, work interference, remote work, and company size.\n",
                "- Run chi-square tests for the main categorical hypotheses.\n",
                "- Build a logistic regression model for treatment-seeking.\n",
                "- Create dashboard-ready summary tables and charts.",
            ],
        },
    ]

    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "pygments_lexer": "ipython3",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    NOTEBOOK_DIR.mkdir(parents=True, exist_ok=True)

    cleaned, quality, variable_dict = prepare_dataset()
    cleaned.to_csv(CLEANED_PATH, index=False)
    quality.to_csv(QUALITY_PATH, index=False)
    variable_dict.to_csv(VARIABLE_DICT_PATH, index=False)

    notebook = make_notebook()
    NOTEBOOK_PATH.write_text(json.dumps(notebook, indent=2), encoding="utf-8")

    print(f"Saved cleaned dataset: {CLEANED_PATH}")
    print(f"Saved quality summary: {QUALITY_PATH}")
    print(f"Saved variable dictionary: {VARIABLE_DICT_PATH}")
    print(f"Saved starter notebook: {NOTEBOOK_PATH}")


if __name__ == "__main__":
    main()
