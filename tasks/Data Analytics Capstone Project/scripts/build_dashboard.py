"""Build a static HTML dashboard for the OSMI capstone project."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px


TASK_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = TASK_DIR / "outputs"
DASHBOARD_DIR = OUTPUT_DIR / "dashboard"
DASHBOARD_PATH = DASHBOARD_DIR / "osmi_mental_health_dashboard.html"


def figure_html(fig, include_plotlyjs: bool = False) -> str:
    return fig.to_html(
        full_html=False,
        include_plotlyjs=True if include_plotlyjs else False,
        config={"displayModeBar": False, "responsive": True},
    )


def make_table_html(df: pd.DataFrame, columns: list[str], max_rows: int = 8) -> str:
    table = df[columns].head(max_rows).copy()
    return table.to_html(index=False, classes="data-table", border=0)


def main() -> None:
    DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)

    clean_df = pd.read_csv(OUTPUT_DIR / "osmi_mental_health_cleaned.csv")
    executive_df = pd.read_csv(OUTPUT_DIR / "executive_summary_metrics.csv")
    tests_df = pd.read_csv(OUTPUT_DIR / "hypothesis_test_results.csv")
    model_perf_df = pd.read_csv(OUTPUT_DIR / "treatment_model_performance.csv")
    model_coef_df = pd.read_csv(OUTPUT_DIR / "treatment_model_coefficients.csv")

    by_benefits = pd.read_csv(OUTPUT_DIR / "treatment_by_benefits.csv")
    by_care = pd.read_csv(OUTPUT_DIR / "treatment_by_care_options.csv")
    by_work = pd.read_csv(OUTPUT_DIR / "treatment_by_work_interfere.csv")
    by_company = pd.read_csv(OUTPUT_DIR / "treatment_by_company_size.csv")
    company_order = ["1 to 5", "6 to 25", "26 to 100", "100 to 500", "500 to 1000", "More than 1000"]
    by_company["company_size"] = pd.Categorical(
        by_company["company_size"], categories=company_order, ordered=True
    )
    by_company = by_company.sort_values("company_size")

    treatment_counts = (
        clean_df["treatment"]
        .value_counts()
        .rename_axis("Treatment")
        .reset_index(name="Respondents")
    )
    fig_treatment = px.bar(
        treatment_counts,
        x="Treatment",
        y="Respondents",
        text="Respondents",
        color="Treatment",
        color_discrete_map={"Yes": "#2f6f73", "No": "#c25746"},
        title="Treatment-Seeking Overview",
    )
    fig_treatment.update_layout(showlegend=False, margin=dict(l=40, r=20, t=60, b=40))

    fig_benefits = px.bar(
        by_benefits,
        x="benefits",
        y="treatment_rate_percent",
        text="treatment_rate_percent",
        color="benefits",
        color_discrete_map={"Yes": "#2f6f73", "No": "#c25746", "Don't know": "#6b7280"},
        title="Treatment Rate By Mental Health Benefits",
        labels={"benefits": "Benefits", "treatment_rate_percent": "Treatment rate (%)"},
    )
    fig_benefits.update_layout(showlegend=False, margin=dict(l=40, r=20, t=60, b=40))

    work_order = ["Often", "Sometimes", "Rarely", "Never", "Missing"]
    by_work["work_interfere"] = pd.Categorical(
        by_work["work_interfere"], categories=work_order, ordered=True
    )
    by_work = by_work.sort_values("work_interfere")
    fig_work = px.bar(
        by_work,
        x="work_interfere",
        y="treatment_rate_percent",
        text="treatment_rate_percent",
        color="work_interfere",
        color_discrete_sequence=["#6d4c7d", "#9b6f93", "#d39b5f", "#52796f", "#9ca3af"],
        title="Treatment Rate By Work Interference",
        labels={
            "work_interfere": "Work interference",
            "treatment_rate_percent": "Treatment rate (%)",
        },
    )
    fig_work.update_layout(showlegend=False, margin=dict(l=40, r=20, t=60, b=40))

    consequence_supervisor = (
        clean_df.groupby(["mental_health_consequence", "supervisor"], dropna=False)
        .size()
        .reset_index(name="respondents")
    )
    fig_consequence = px.bar(
        consequence_supervisor,
        x="mental_health_consequence",
        y="respondents",
        color="supervisor",
        barmode="group",
        color_discrete_map={"Yes": "#2f6f73", "Some of them": "#d39b5f", "No": "#c25746"},
        title="Supervisor Discussion Comfort By Expected Consequences",
        labels={
            "mental_health_consequence": "Expected consequence",
            "respondents": "Respondents",
            "supervisor": "Discuss with supervisor",
        },
    )
    fig_consequence.update_layout(margin=dict(l=40, r=20, t=60, b=40))

    fig_company = px.bar(
        by_company,
        x="company_size",
        y="treatment_rate_percent",
        text="treatment_rate_percent",
        color="respondents",
        color_continuous_scale=["#8fb9aa", "#2f6f73"],
        title="Treatment Rate By Company Size",
        labels={"company_size": "Company size", "treatment_rate_percent": "Treatment rate (%)"},
    )
    fig_company.update_layout(margin=dict(l=40, r=20, t=60, b=80), coloraxis_showscale=False)

    roc_auc = model_perf_df.loc[0, "roc_auc"]
    accuracy = model_perf_df.loc[0, "accuracy"]
    recall = model_perf_df.loc[0, "recall_treatment_yes"]

    kpi_lookup = dict(zip(executive_df["metric"], executive_df["value"]))
    kpis = [
        ("Survey responses", kpi_lookup["Total survey responses"]),
        ("Sought treatment", kpi_lookup["Sought mental health treatment"]),
        ("Know benefits", kpi_lookup["Know employer provides mental health benefits"]),
        ("Any work interference", kpi_lookup["Report any work interference"]),
        ("Supervisor comfort", kpi_lookup["Comfortable discussing mental health with supervisor"]),
        ("Coworker comfort", kpi_lookup["Comfortable discussing mental health with coworkers"]),
    ]
    kpi_html = "\n".join(
        f'<article class="kpi"><span>{label}</span><strong>{value}</strong></article>'
        for label, value in kpis
    )

    tests_display = tests_df[
        ["test", "question", "p_value", "significant_at_0_05"]
    ].copy()
    tests_display["p_value"] = tests_display["p_value"].map(lambda x: f"{x:.6f}")

    model_display = model_coef_df.head(10).copy()

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>OSMI Mental Health In Tech Dashboard</title>
  <style>
    :root {{
      --ink: #1f2933;
      --muted: #5f6b7a;
      --line: #d8dee6;
      --bg: #f6f7f9;
      --surface: #ffffff;
      --teal: #2f6f73;
      --red: #c25746;
      --gold: #d39b5f;
      --violet: #6d4c7d;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--ink);
      background: var(--bg);
      line-height: 1.5;
    }}
    header {{
      background: var(--surface);
      border-bottom: 1px solid var(--line);
    }}
    .wrap {{
      max-width: 1180px;
      margin: 0 auto;
      padding: 24px;
    }}
    h1 {{
      margin: 0 0 8px;
      font-size: 30px;
      line-height: 1.15;
      letter-spacing: 0;
    }}
    h2 {{
      margin: 0 0 16px;
      font-size: 20px;
      letter-spacing: 0;
    }}
    p {{
      margin: 0;
      color: var(--muted);
      max-width: 920px;
    }}
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
      margin-top: 20px;
    }}
    .kpi {{
      background: var(--surface);
      border: 1px solid var(--line);
      border-left: 5px solid var(--teal);
      border-radius: 8px;
      padding: 14px 16px;
      min-height: 98px;
    }}
    .kpi span {{
      display: block;
      color: var(--muted);
      font-size: 13px;
      margin-bottom: 8px;
    }}
    .kpi strong {{
      display: block;
      font-size: 22px;
      line-height: 1.25;
      letter-spacing: 0;
    }}
    section {{
      margin-top: 20px;
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 18px;
    }}
    .chart-grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 16px;
    }}
    .chart-panel {{
      min-height: 420px;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 6px;
      overflow: hidden;
    }}
    .model-strip {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
      margin-bottom: 16px;
    }}
    .metric {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 12px;
      background: #fbfcfd;
    }}
    .metric span {{
      display: block;
      color: var(--muted);
      font-size: 13px;
    }}
    .metric strong {{
      font-size: 24px;
    }}
    .data-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 14px;
    }}
    .data-table th, .data-table td {{
      border-bottom: 1px solid var(--line);
      padding: 9px 8px;
      text-align: left;
      vertical-align: top;
    }}
    .data-table th {{
      background: #eef3f2;
      font-weight: 700;
    }}
    .table-scroll {{
      overflow-x: auto;
    }}
    footer {{
      color: var(--muted);
      font-size: 13px;
      padding-bottom: 32px;
    }}
    @media (max-width: 820px) {{
      .kpi-grid, .chart-grid, .model-strip {{
        grid-template-columns: 1fr;
      }}
      .wrap {{
        padding: 16px;
      }}
      h1 {{
        font-size: 24px;
      }}
      .kpi strong {{
        font-size: 19px;
      }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="wrap">
      <h1>Workplace Mental Health In Tech</h1>
      <p>Quantitative survey dashboard based on the OSMI Mental Health in Tech Survey. The focus is treatment-seeking, workplace support, disclosure comfort, and perceived consequences.</p>
      <div class="kpi-grid">
        {kpi_html}
      </div>
    </div>
  </header>

  <main class="wrap">
    <section>
      <h2>Treatment And Workplace Support</h2>
      <div class="chart-grid">
        <div class="chart-panel">{figure_html(fig_treatment, include_plotlyjs=True)}</div>
        <div class="chart-panel">{figure_html(fig_benefits)}</div>
        <div class="chart-panel">{figure_html(fig_work)}</div>
        <div class="chart-panel">{figure_html(fig_company)}</div>
      </div>
    </section>

    <section>
      <h2>Disclosure Comfort And Consequences</h2>
      <div class="chart-panel">{figure_html(fig_consequence)}</div>
    </section>

    <section>
      <h2>Hypothesis Tests</h2>
      <div class="table-scroll">
        {make_table_html(tests_display, ["test", "question", "p_value", "significant_at_0_05"], 10)}
      </div>
    </section>

    <section>
      <h2>Treatment-Seeking Model</h2>
      <div class="model-strip">
        <div class="metric"><span>ROC AUC</span><strong>{roc_auc:.3f}</strong></div>
        <div class="metric"><span>Accuracy</span><strong>{accuracy:.3f}</strong></div>
        <div class="metric"><span>Recall for treatment</span><strong>{recall:.3f}</strong></div>
      </div>
      <div class="table-scroll">
        {make_table_html(model_display, ["feature", "coefficient", "odds_ratio"], 10)}
      </div>
    </section>
  </main>

  <footer class="wrap">
    Source: OSMI Mental Health in Tech Survey via Kaggle. Analysis is observational and shows associations, not causation.
  </footer>
</body>
</html>
"""

    DASHBOARD_PATH.write_text(html, encoding="utf-8")
    print(f"Saved dashboard: {DASHBOARD_PATH}")


if __name__ == "__main__":
    main()
