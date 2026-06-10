"""Build the full OSMI capstone analysis notebook."""

from __future__ import annotations

import json
import textwrap
from pathlib import Path


TASK_DIR = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = TASK_DIR / "notebooks" / "osmi_mental_health_analysis.ipynb"


def markdown(source: str) -> dict:
    clean_source = textwrap.dedent(source).strip()
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": clean_source.splitlines(keepends=True),
    }


def code(source: str) -> dict:
    clean_source = textwrap.dedent(source).strip()
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": clean_source.splitlines(keepends=True),
    }


def build_notebook() -> dict:
    cells = [
        markdown(
            """
            # Workplace Mental Health Disclosure And Support In The Technology Sector

            ## A Quantitative Survey Analysis

            This capstone analyzes the OSMI Mental Health in Tech Survey from Kaggle. The project uses a public survey dataset to show a reproducible quantitative research workflow: data cleaning, segmentation, hypothesis testing, and logistic regression modeling.
            """
        ),
        markdown(
            """
            ## Executive Summary

            The dataset contains **1,259 survey responses** about mental health and workplace support in the technology sector.

            Main early findings:

            - **637 respondents (50.6%)** reported seeking mental health treatment.
            - **477 respondents (37.9%)** knew their employer provides mental health benefits.
            - **782 respondents (62.1%)** reported at least some mental-health-related work interference.
            - **516 respondents (41.0%)** were comfortable discussing mental health with a supervisor.
            - Only **225 respondents (17.9%)** were comfortable discussing mental health with coworkers.
            - The treatment-seeking logistic regression model achieved **ROC AUC = 0.891** on the test set.

            The results suggest that treatment-seeking is common in this survey sample, but workplace disclosure comfort is much lower, especially with coworkers. Workplace benefits, care options, family history, and work interference are all statistically associated with treatment-seeking.
            """
        ),
        markdown(
            """
            ## Dataset Description

            - **Source:** OSMI Mental Health in Tech Survey on Kaggle.
            - **Raw file:** `data/osmi-mental-health-in-tech-survey/survey.csv`.
            - **Rows:** 1,259.
            - **Raw columns:** 27.
            - **One row means:** one survey response.
            - **Main topic:** mental health treatment, workplace support, stigma, disclosure comfort, and work interference in technology workplaces.

            The dataset is observational and self-reported. This means the analysis can show associations, but it cannot prove cause and effect.
            """
        ),
        markdown(
            """
            ## Research Question And Hypotheses

            **Research question:** What workplace and personal factors are associated with mental health treatment-seeking and disclosure comfort among technology workers?

            Hypotheses:

            1. Respondents who know their employer provides mental health benefits are more likely to seek treatment.
            2. Respondents who expect negative workplace consequences are less comfortable discussing mental health with supervisors or coworkers.
            3. Respondents whose mental health interferes with work are more likely to have sought treatment.
            4. Workplace support indicators differ by company size, remote work status, and whether the employer is primarily a tech company.
            """
        ),
        markdown(
            """
            ## Techniques Used

            This capstone uses three main techniques from the course:

            - **Segmentation:** comparing treatment-seeking and disclosure comfort across workplace and personal groups.
            - **Hypothesis testing:** using chi-square tests and Kruskal-Wallis tests to check whether group differences are statistically meaningful.
            - **Regression/classification modeling:** using logistic regression to model whether a respondent sought mental health treatment.

            A fourth supporting technique is dashboard-style visualization using chart outputs.
            """
        ),
        code(
            """
            from pathlib import Path

            import pandas as pd
            from IPython.display import display

            TASK_DIR = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
            OUTPUT_DIR = TASK_DIR / "outputs"
            CHART_DIR = OUTPUT_DIR / "charts"

            clean_df = pd.read_csv(OUTPUT_DIR / "osmi_mental_health_cleaned.csv")
            quality_df = pd.read_csv(OUTPUT_DIR / "osmi_data_quality_summary.csv")
            executive_df = pd.read_csv(OUTPUT_DIR / "executive_summary_metrics.csv")
            tests_df = pd.read_csv(OUTPUT_DIR / "hypothesis_test_results.csv")
            model_perf_df = pd.read_csv(OUTPUT_DIR / "treatment_model_performance.csv")
            model_coef_df = pd.read_csv(OUTPUT_DIR / "treatment_model_coefficients.csv")

            treatment_by_benefits = pd.read_csv(OUTPUT_DIR / "treatment_by_benefits.csv")
            treatment_by_care_options = pd.read_csv(OUTPUT_DIR / "treatment_by_care_options.csv")
            treatment_by_family_history = pd.read_csv(OUTPUT_DIR / "treatment_by_family_history.csv")
            treatment_by_work_interfere = pd.read_csv(OUTPUT_DIR / "treatment_by_work_interfere.csv")
            treatment_by_company_size = pd.read_csv(OUTPUT_DIR / "treatment_by_company_size.csv")

            clean_df.shape
            """
        ),
        markdown(
            """
            ## Data Quality And Cleaning

            Survey data often contains messy values because respondents can enter information in different ways. The cleaning script made the analysis reproducible by:

            - converting column names to `snake_case`;
            - treating ages outside **18-75** as missing;
            - grouping **49 raw gender values** into 4 broader analysis categories;
            - creating binary variables such as `treatment_yes`, `benefits_yes`, and `family_history_yes`;
            - creating ordered scores for work interference, leave difficulty, discussion comfort, and perceived consequences.
            """
        ),
        code(
            """
            display(quality_df)
            """
        ),
        markdown(
            """
            ## Key Survey Metrics

            These values provide the first overview of the sample before deeper analysis.
            """
        ),
        code(
            """
            display(executive_df)
            """
        ),
        markdown(
            """
            ## Segmentation: Treatment-Seeking By Workplace Support

            Segmentation means dividing respondents into groups and comparing outcomes between those groups. Here, the outcome is whether a respondent reported seeking mental health treatment.
            """
        ),
        code(
            """
            display(treatment_by_benefits)
            display(treatment_by_care_options)
            """
        ),
        markdown(
            """
            ## Segmentation: Treatment-Seeking By Personal And Work Context

            Family history and work interference are important context variables. They should not be interpreted as workplace policies, but they help explain why treatment-seeking may differ between respondents.
            """
        ),
        code(
            """
            display(treatment_by_family_history)
            display(treatment_by_work_interfere)
            """
        ),
        markdown(
            """
            ## Hypothesis Testing

            A hypothesis test checks whether an observed difference is large enough that it is unlikely to be only random noise.

            For categorical variables, this notebook uses the **chi-square test**. Example: it tests whether treatment-seeking differs across benefit-awareness groups.

            For ordered scores across multiple company-size groups, this notebook uses the **Kruskal-Wallis test**. This is useful when we compare ordinal or non-normal values across more than two groups.
            """
        ),
        code(
            """
            display(tests_df)
            """
        ),
        markdown(
            """
            ## Hypothesis Test Interpretation

            The main tests found statistically significant associations at the 0.05 level:

            - Employer mental health benefits and treatment-seeking: **p < 0.001**.
            - Care options and treatment-seeking: **p < 0.001**.
            - Family history and treatment-seeking: **p < 0.001**.
            - Work interference and treatment-seeking: **p < 0.001**.
            - Expected mental health consequences and supervisor discussion comfort: **p < 0.001**.
            - Expected mental health consequences and coworker discussion comfort: **p < 0.001**.

            Company size was significantly associated with discussion comfort (**p = 0.000238**), but not with leave difficulty at the 0.05 level (**p = 0.065674**).
            """
        ),
        markdown(
            """
            ## Logistic Regression Model

            Logistic regression is used when the target variable has two outcomes. In this project, the target is:

            - `1`: respondent sought mental health treatment;
            - `0`: respondent did not seek mental health treatment.

            The model uses workplace support, work context, family history, age, and gender variables to estimate which factors are associated with treatment-seeking.
            """
        ),
        code(
            """
            display(model_perf_df)
            display(model_coef_df.head(15))
            """
        ),
        markdown(
            """
            ## Model Interpretation

            The model achieved **ROC AUC = 0.891**, which means it separated treatment-seeking and non-treatment-seeking respondents well on the test data.

            The strongest positive model signals included:

            - frequent work interference;
            - family history of mental illness;
            - comfort discussing mental health with coworkers;
            - knowing that employer care options are available;
            - knowing that employer mental health benefits are available.

            Important caution: this is still association, not causation. For example, the model does not prove that work interference causes treatment. It shows that work interference is strongly related to treatment-seeking in this survey sample.
            """
        ),
        markdown(
            """
            ## Dashboard-Ready Chart Outputs

            The analysis script created interactive HTML charts in `outputs/charts/`.

            Current chart files:

            - `treatment_overview.html`
            - `treatment_by_benefits.html`
            - `treatment_by_work_interference.html`
            - `supervisor_comfort_by_consequence.html`

            These charts can support the dashboard, presentation, and written report.
            """
        ),
        code(
            """
            chart_files = sorted(path.name for path in CHART_DIR.glob("*.html"))
            chart_files
            """
        ),
        markdown(
            """
            ## Recommendations

            Based on the current analysis, technology employers should:

            1. Make mental health benefits and care options easier to understand, because benefit awareness is associated with treatment-seeking.
            2. Strengthen anonymity and confidentiality communication, because disclosure risk appears central to supervisor and coworker comfort.
            3. Train managers to discuss mental health safely, because only 41.0% of respondents were comfortable discussing mental health with supervisors.
            4. Reduce stigma in team culture, because only 17.9% of respondents were comfortable discussing mental health with coworkers.
            5. Monitor work interference as an early warning signal, because work interference is strongly associated with treatment-seeking.
            """
        ),
        markdown(
            """
            ## Limitations

            - The dataset is observational, so the analysis cannot prove cause and effect.
            - Respondents are not a perfectly random sample of all technology workers.
            - The data is self-reported, so it may include recall bias or social desirability bias.
            - Some variables have missing values, especially `work_interfere`.
            - Gender was grouped from many raw self-described values, which simplifies identity categories for analysis.
            - The survey is from one dataset and should not be generalized without caution.
            """
        ),
        markdown(
            """
            ## Final Conclusion

            The analysis shows that mental health treatment-seeking is common in this technology-sector survey sample, but workplace disclosure comfort is much lower. Workplace benefits, care options, family history, work interference, and perceived consequences are all meaningfully associated with treatment-seeking or disclosure comfort.

            For the capstone story, the most important insight is the gap between private action and workplace openness: **50.6%** of respondents sought treatment, but only **41.0%** were comfortable discussing mental health with a supervisor and only **17.9%** were comfortable discussing it with coworkers.
            """
        ),
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
    notebook = build_notebook()
    NOTEBOOK_PATH.write_text(json.dumps(notebook, indent=2), encoding="utf-8")
    print(f"Saved full analysis notebook: {NOTEBOOK_PATH}")


if __name__ == "__main__":
    main()
