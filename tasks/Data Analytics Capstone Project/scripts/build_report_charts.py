"""Build static chart images for the capstone report and notebook.

The project keeps the interactive HTML dashboard as a supplementary artifact,
but the written report and notebook need static chart snippets that travel well
to Google Docs, DOCX, PDF, and GitHub previews.
"""

from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib-capstone")

import matplotlib.pyplot as plt
import pandas as pd


TASK_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = TASK_DIR / "outputs"
ASSET_DIR = OUTPUT_DIR / "report_chart_assets"

INK = "#1f2933"
MUTED = "#5f6b7a"
TEAL = "#2f6f73"
RED = "#c25746"
GOLD = "#d39b5f"
VIOLET = "#6d4c7d"
LINE = "#d8dee6"
PAPER = "#ffffff"


def save_fig(fig: plt.Figure, filename: str) -> None:
    path = ASSET_DIR / filename
    fig.savefig(path, dpi=180, bbox_inches="tight", facecolor=PAPER)
    plt.close(fig)


def style_axis(ax: plt.Axes, title: str, ylabel: str | None = None) -> None:
    ax.set_title(title, loc="left", fontsize=15, fontweight="bold", color=INK, pad=14)
    ax.set_ylabel(ylabel or "", color=MUTED)
    ax.tick_params(axis="x", colors=INK, labelsize=10)
    ax.tick_params(axis="y", colors=MUTED, labelsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(LINE)
    ax.spines["bottom"].set_color(LINE)
    ax.grid(axis="y", color=LINE, linewidth=0.8, alpha=0.65)
    ax.set_axisbelow(True)


def add_bar_labels(ax: plt.Axes, suffix: str = "") -> None:
    for patch in ax.patches:
        height = patch.get_height()
        ax.annotate(
            f"{height:.1f}{suffix}" if isinstance(height, float) else f"{height}{suffix}",
            (patch.get_x() + patch.get_width() / 2, height),
            ha="center",
            va="bottom",
            fontsize=9,
            color=INK,
            fontweight="bold",
            xytext=(0, 4),
            textcoords="offset points",
        )


def treatment_overview(clean_df: pd.DataFrame) -> None:
    counts = clean_df["treatment"].value_counts().reindex(["Yes", "No"])
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.bar(counts.index, counts.values, color=[TEAL, RED], width=0.55)
    style_axis(ax, "Mental Health Treatment-Seeking Among Respondents", "Respondents")
    for patch in ax.patches:
        height = patch.get_height()
        pct = height / counts.sum() * 100
        ax.annotate(
            f"{int(height):,}\n({pct:.1f}%)",
            (patch.get_x() + patch.get_width() / 2, height),
            ha="center",
            va="bottom",
            fontsize=10,
            color=INK,
            fontweight="bold",
            xytext=(0, 5),
            textcoords="offset points",
        )
    ax.set_ylim(0, max(counts.values) * 1.22)
    save_fig(fig, "figure_01_treatment_overview.png")


def treatment_rate_chart(
    df: pd.DataFrame,
    category_col: str,
    title: str,
    filename: str,
    color: str,
    order: list[str] | None = None,
    rotation: int = 0,
) -> None:
    plot_df = df.copy()
    if order:
        plot_df[category_col] = pd.Categorical(plot_df[category_col], order, ordered=True)
        plot_df = plot_df.sort_values(category_col)
    fig, ax = plt.subplots(figsize=(8.2, 4.4))
    ax.bar(plot_df[category_col].astype(str), plot_df["treatment_rate_percent"], color=color, width=0.62)
    style_axis(ax, title, "Treatment rate (%)")
    add_bar_labels(ax, "%")
    ax.set_ylim(0, max(plot_df["treatment_rate_percent"]) * 1.22)
    ax.set_xlabel("")
    plt.xticks(rotation=rotation, ha="right" if rotation else "center")
    save_fig(fig, filename)


def care_and_benefits_chart(benefits_df: pd.DataFrame, care_df: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2), sharey=True)
    for ax, plot_df, col, title, color in [
        (axes[0], benefits_df, "benefits", "By Benefits Awareness", TEAL),
        (axes[1], care_df, "care_options", "By Care Options Awareness", GOLD),
    ]:
        ax.bar(plot_df[col].astype(str), plot_df["treatment_rate_percent"], color=color, width=0.62)
        style_axis(ax, title, "Treatment rate (%)")
        add_bar_labels(ax, "%")
        ax.set_xlabel("")
        ax.set_ylim(0, 82)
    fig.suptitle(
        "Treatment-Seeking Is Higher When Mental Health Support Is Known",
        x=0.03,
        y=1.04,
        ha="left",
        fontsize=16,
        fontweight="bold",
        color=INK,
    )
    save_fig(fig, "figure_02_benefits_and_care_options.png")


def supervisor_consequence_chart(clean_df: pd.DataFrame) -> None:
    order = ["No", "Maybe", "Yes"]
    supervisor = (
        clean_df.groupby(["mental_health_consequence", "supervisor"], dropna=False)
        .size()
        .reset_index(name="respondents")
    )
    pivot = supervisor.pivot_table(
        index="mental_health_consequence",
        columns="supervisor",
        values="respondents",
        aggfunc="sum",
        fill_value=0,
    )
    pivot = pivot.reindex(order)
    cols = [col for col in ["Yes", "Some of them", "No"] if col in pivot.columns]
    fig, ax = plt.subplots(figsize=(9.2, 4.8))
    bottom = None
    colors = {"Yes": TEAL, "Some of them": GOLD, "No": RED}
    for col in cols:
        ax.bar(pivot.index, pivot[col], bottom=bottom, label=col, color=colors.get(col, MUTED), width=0.6)
        bottom = pivot[col] if bottom is None else bottom + pivot[col]
    style_axis(ax, "Supervisor Discussion Comfort By Expected Mental Health Consequences", "Respondents")
    ax.set_xlabel("Expected negative consequences")
    ax.legend(title="Comfort discussing with supervisor", frameon=False, loc="upper right")
    save_fig(fig, "figure_04_supervisor_comfort_by_consequence.png")


def company_size_chart(company_df: pd.DataFrame) -> None:
    order = ["1 to 5", "6 to 25", "26 to 100", "100 to 500", "500 to 1000", "More than 1000"]
    treatment_rate_chart(
        company_df,
        "company_size",
        "Treatment-Seeking Rate By Company Size",
        "figure_05_treatment_by_company_size.png",
        TEAL,
        order,
        18,
    )


def model_metrics_chart(model_df: pd.DataFrame) -> None:
    row = model_df.iloc[0]
    metrics = pd.Series(
        {
            "ROC AUC": row["roc_auc"],
            "Accuracy": row["accuracy"],
            "Precision": row["precision_treatment_yes"],
            "Recall": row["recall_treatment_yes"],
            "F1 score": row["f1_treatment_yes"],
        }
    )
    fig, ax = plt.subplots(figsize=(8.2, 4.4))
    ax.bar(metrics.index, metrics.values, color=[TEAL, GOLD, VIOLET, TEAL, GOLD], width=0.62)
    style_axis(ax, "Logistic Regression Model Performance", "Score")
    for patch in ax.patches:
        height = patch.get_height()
        ax.annotate(
            f"{height:.3f}",
            (patch.get_x() + patch.get_width() / 2, height),
            ha="center",
            va="bottom",
            fontsize=9,
            color=INK,
            fontweight="bold",
            xytext=(0, 4),
            textcoords="offset points",
        )
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("")
    save_fig(fig, "figure_06_model_performance.png")


def main() -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)

    clean_df = pd.read_csv(OUTPUT_DIR / "osmi_mental_health_cleaned.csv")
    benefits_df = pd.read_csv(OUTPUT_DIR / "treatment_by_benefits.csv")
    care_df = pd.read_csv(OUTPUT_DIR / "treatment_by_care_options.csv")
    work_df = pd.read_csv(OUTPUT_DIR / "treatment_by_work_interfere.csv")
    company_df = pd.read_csv(OUTPUT_DIR / "treatment_by_company_size.csv")
    model_df = pd.read_csv(OUTPUT_DIR / "treatment_model_performance.csv")

    treatment_overview(clean_df)
    care_and_benefits_chart(benefits_df, care_df)
    treatment_rate_chart(
        work_df,
        "work_interfere",
        "Treatment-Seeking Rate By Work Interference",
        "figure_03_treatment_by_work_interference.png",
        VIOLET,
        ["Often", "Sometimes", "Rarely", "Never", "Missing"],
    )
    supervisor_consequence_chart(clean_df)
    company_size_chart(company_df)
    model_metrics_chart(model_df)

    print(f"Saved report chart assets to: {ASSET_DIR}")


if __name__ == "__main__":
    main()
