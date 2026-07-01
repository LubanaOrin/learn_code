"""Build charts and written findings for the Marketing Analyst task."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


TASK_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = TASK_DIR / "data" / "marketing_campaign_weekday_duration.csv"
OUTPUT_DIR = TASK_DIR / "outputs"
CHART_DIR = OUTPUT_DIR / "charts"
FINAL_DIR = OUTPUT_DIR / "FINAL_SUBMISSION_FILES"

WEEKDAY_ORDER = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

CAMPAIGN_COLORS = {
    "(organic)": "#2F6B5F",
    "(referral)": "#4666A6",
    "<Other>": "#7A6478",
    "Data Share Promo": "#C77C2E",
    "BlackFriday_V1": "#A33E3E",
    "BlackFriday_V2": "#6A3D9A",
    "Holiday_V1": "#3B8EA5",
    "Holiday_V2": "#8A9A5B",
    "NewYear_V1": "#D39C2F",
    "NewYear_V2": "#5F6B7A",
}


def load_data() -> pd.DataFrame:
    """Load the BigQuery export and keep weekday order stable for charts."""
    df = pd.read_csv(DATA_PATH)
    df["weekday_name"] = pd.Categorical(
        df["weekday_name"], categories=WEEKDAY_ORDER, ordered=True
    )
    return df.sort_values(["campaign", "weekday_sort_monday_start"]).copy()


def save_summary_tables(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Create campaign-level and weekday-level summaries."""
    campaign_summary = (
        df.groupby("campaign", as_index=False)
        .agg(
            total_sessions=("sessions", "sum"),
            weighted_avg_duration_minutes=(
                "avg_session_duration_minutes",
                lambda s: round(
                    (s * df.loc[s.index, "sessions"]).sum()
                    / df.loc[s.index, "sessions"].sum(),
                    2,
                ),
            ),
            median_of_weekday_medians=("median_session_duration_minutes", "median"),
            avg_events_per_session=(
                "avg_events_per_session",
                lambda s: round(
                    (s * df.loc[s.index, "sessions"]).sum()
                    / df.loc[s.index, "sessions"].sum(),
                    2,
                ),
            ),
            observed_weekdays=("weekday_name", "count"),
        )
        .sort_values("total_sessions", ascending=False)
    )

    weekday_summary = (
        df.groupby("weekday_name", observed=False, as_index=False)
        .agg(
            total_sessions=("sessions", "sum"),
            weighted_avg_duration_minutes=(
                "avg_session_duration_minutes",
                lambda s: round(
                    (s * df.loc[s.index, "sessions"]).sum()
                    / df.loc[s.index, "sessions"].sum(),
                    2,
                ),
            ),
            median_of_campaign_medians=("median_session_duration_minutes", "median"),
        )
        .sort_values("weekday_name")
    )

    campaign_summary.to_csv(OUTPUT_DIR / "campaign_duration_summary.csv", index=False)
    weekday_summary.to_csv(OUTPUT_DIR / "weekday_duration_summary.csv", index=False)
    return campaign_summary, weekday_summary


def style_axis(ax, title: str, ylabel: str) -> None:
    ax.set_title(title, loc="left", fontsize=15, fontweight="bold", pad=14)
    ax.set_ylabel(ylabel)
    ax.set_xlabel("")
    ax.grid(axis="y", color="#E4E7EC", linewidth=0.8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#CBD5E1")
    ax.spines["bottom"].set_color("#CBD5E1")
    ax.tick_params(axis="x", rotation=25)


def build_reliable_campaign_chart(df: pd.DataFrame) -> Path:
    """Line chart for campaigns with enough sessions to support comparisons."""
    reliable_campaigns = ["(organic)", "(referral)", "<Other>", "Data Share Promo"]
    plot_df = df[df["campaign"].isin(reliable_campaigns)]

    fig, ax = plt.subplots(figsize=(11, 6.2))
    for campaign in reliable_campaigns:
        campaign_df = plot_df[plot_df["campaign"] == campaign]
        ax.plot(
            campaign_df["weekday_name"].astype(str),
            campaign_df["avg_session_duration_minutes"],
            marker="o",
            linewidth=2.7,
            label=campaign,
            color=CAMPAIGN_COLORS[campaign],
        )

    style_axis(
        ax,
        "Referral sessions are consistently longer than organic sessions",
        "Average modeled session duration, minutes",
    )
    ax.legend(frameon=False, ncol=2, loc="upper center", bbox_to_anchor=(0.5, -0.16))
    fig.text(
        0.01,
        0.01,
        "Source: BigQuery export from tc-da-1.turing_data_analytics.raw_events. Sessions modeled with a 30-minute inactivity timeout.",
        fontsize=9,
        color="#5F6B7A",
    )
    fig.tight_layout(rect=[0, 0.06, 1, 1])
    path = CHART_DIR / "reliable_campaign_weekday_duration.png"
    fig.savefig(path, dpi=180)
    plt.close(fig)
    return path


def build_sample_size_chart(campaign_summary: pd.DataFrame) -> Path:
    """Bar chart showing why some campaign findings need caution."""
    plot_df = campaign_summary.sort_values("total_sessions", ascending=True)

    fig, ax = plt.subplots(figsize=(10.8, 6.4))
    colors = [
        "#4666A6" if sessions >= 100 else "#C25746"
        for sessions in plot_df["total_sessions"]
    ]
    bars = ax.barh(plot_df["campaign"], plot_df["total_sessions"], color=colors)
    ax.set_xscale("log")
    ax.set_xlabel("Total modeled sessions, log scale")
    ax.set_ylabel("")
    ax.set_title(
        "Several named campaigns have very small sample sizes",
        loc="left",
        fontsize=15,
        fontweight="bold",
        pad=14,
    )
    ax.grid(axis="x", color="#E4E7EC", linewidth=0.8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#CBD5E1")
    ax.spines["bottom"].set_color("#CBD5E1")

    for bar, sessions in zip(bars, plot_df["total_sessions"]):
        ax.text(
            sessions * 1.08,
            bar.get_y() + bar.get_height() / 2,
            f"{sessions:,}",
            va="center",
            fontsize=9,
            color="#1F2933",
        )

    fig.text(
        0.01,
        0.01,
        "Red bars have fewer than 100 modeled sessions, so duration comparisons should be treated as directional only.",
        fontsize=9,
        color="#5F6B7A",
    )
    fig.tight_layout(rect=[0, 0.06, 1, 1])
    path = CHART_DIR / "campaign_sample_size_context.png"
    fig.savefig(path, dpi=180)
    plt.close(fig)
    return path


def build_top_duration_chart(df: pd.DataFrame) -> Path:
    """Show the highest observed weekday-campaign combinations."""
    plot_df = df.sort_values("avg_session_duration_minutes", ascending=False).head(12)
    labels = plot_df["campaign"] + " - " + plot_df["weekday_name"].astype(str)

    fig, ax = plt.subplots(figsize=(10.8, 6.4))
    ax.barh(labels[::-1], plot_df["avg_session_duration_minutes"][::-1], color="#6A3D9A")
    ax.set_xlabel("Average modeled session duration, minutes")
    ax.set_ylabel("")
    ax.set_title(
        "Longest averages are based on tiny samples",
        loc="left",
        fontsize=15,
        fontweight="bold",
        pad=14,
    )
    ax.grid(axis="x", color="#E4E7EC", linewidth=0.8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#CBD5E1")
    ax.spines["bottom"].set_color("#CBD5E1")

    for i, (_, row) in enumerate(plot_df.iloc[::-1].iterrows()):
        ax.text(
            row["avg_session_duration_minutes"] + 0.35,
            i,
            f"{row['avg_session_duration_minutes']:.1f} min | n={int(row['sessions'])}",
            va="center",
            fontsize=9,
            color="#1F2933",
        )

    fig.text(
        0.01,
        0.01,
        "Use this as exploration, not final proof: high averages with 2-9 sessions can change sharply with one unusual visit.",
        fontsize=9,
        color="#5F6B7A",
    )
    fig.tight_layout(rect=[0, 0.06, 1, 1])
    path = CHART_DIR / "top_weekday_campaign_duration_combinations.png"
    fig.savefig(path, dpi=180)
    plt.close(fig)
    return path


def write_findings(
    df: pd.DataFrame,
    campaign_summary: pd.DataFrame,
    weekday_summary: pd.DataFrame,
    chart_paths: list[Path],
) -> Path:
    """Write a concise findings note for submission and slide drafting."""
    reliable = campaign_summary[campaign_summary["total_sessions"] >= 100]
    top_reliable = reliable.sort_values(
        "weighted_avg_duration_minutes", ascending=False
    ).iloc[0]
    organic = campaign_summary[campaign_summary["campaign"] == "(organic)"].iloc[0]
    referral = campaign_summary[campaign_summary["campaign"] == "(referral)"].iloc[0]
    data_share = campaign_summary[
        campaign_summary["campaign"] == "Data Share Promo"
    ].iloc[0]
    highest = df.sort_values("avg_session_duration_minutes", ascending=False).iloc[0]
    friday_bfv1 = df[
        (df["campaign"] == "BlackFriday_V1") & (df["weekday_name"].astype(str) == "Friday")
    ]
    friday_bfv1_text = "No Friday row was available for BlackFriday_V1."
    if not friday_bfv1.empty:
        row = friday_bfv1.iloc[0]
        friday_bfv1_text = (
            "BlackFriday_V1 Friday average session duration was "
            f"{row['avg_session_duration_minutes']:.2f} minutes "
            f"({row['avg_session_duration_hh_mm_ss']}), based on "
            f"{int(row['sessions'])} sessions. It did not take longer than 1 hour."
        )

    text = f"""# Marketing Campaign Comparison Findings

## Dataset Check

- The BigQuery export contains {len(df)} campaign-weekday rows.
- The analysis covers {campaign_summary['campaign'].nunique()} campaign/source groups.
- Total modeled sessions in the exported result: {campaign_summary['total_sessions'].sum():,}.

## Main Findings

- Among campaign/source groups with at least 100 sessions, **{top_reliable['campaign']}** has the longest weighted average session duration at **{top_reliable['weighted_avg_duration_minutes']:.2f} minutes**.
- Referral traffic has **{referral['total_sessions']:,} sessions** and a weighted average duration of **{referral['weighted_avg_duration_minutes']:.2f} minutes**.
- Organic traffic has **{organic['total_sessions']:,} sessions** and a weighted average duration of **{organic['weighted_avg_duration_minutes']:.2f} minutes**.
- Data Share Promo has **{data_share['total_sessions']:,} sessions** and a weighted average duration of **{data_share['weighted_avg_duration_minutes']:.2f} minutes**.
- The highest raw campaign-weekday average is **{highest['campaign']} on {highest['weekday_name']}** at **{highest['avg_session_duration_minutes']:.2f} minutes**, but it is based on only **{int(highest['sessions'])} sessions**.
- {friday_bfv1_text}

## Interpretation

Referral sessions are consistently longer than organic sessions across the week. This can be a positive sign because referred users may be more engaged, but longer time on site can also mean users are struggling to find information or leaving tabs open.

The small named campaigns should be treated carefully. Several have fewer than 100 modeled sessions in total, so one or two unusually long visits can strongly affect the average.

## Drawbacks

- The dataset does not include a real session ID, so sessions are modeled with a 30-minute inactivity rule.
- Single-event sessions have a duration of 0 minutes because there is no second event to measure against.
- Campaign attribution may be incomplete when campaign values are missing from events.
- Long duration can mean engagement, confusion, or inactive browser tabs.
- Several campaigns have very small samples.

## Recommended Further Analysis

- Compare average and median session duration for each campaign.
- Connect session duration to purchases or conversion events.
- Repeat the analysis by device, country, and traffic source.
- Separate single-event sessions from multi-event sessions.
- Test whether longer sessions have higher revenue or only more browsing.

## Chart Outputs

{chr(10).join(f'- `{path.relative_to(TASK_DIR)}`' for path in chart_paths)}
"""
    path = OUTPUT_DIR / "marketing_campaign_comparison_findings.md"
    path.write_text(text, encoding="utf-8")
    (FINAL_DIR / "marketing_campaign_comparison_findings.md").write_text(
        text, encoding="utf-8"
    )
    return path


def main() -> None:
    CHART_DIR.mkdir(parents=True, exist_ok=True)
    FINAL_DIR.mkdir(parents=True, exist_ok=True)

    df = load_data()
    campaign_summary, weekday_summary = save_summary_tables(df)
    chart_paths = [
        build_reliable_campaign_chart(df),
        build_sample_size_chart(campaign_summary),
        build_top_duration_chart(df),
    ]
    findings_path = write_findings(df, campaign_summary, weekday_summary, chart_paths)

    print(f"Rows analyzed: {len(df)}")
    print(f"Campaign groups: {df['campaign'].nunique()}")
    print(f"Findings written to: {findings_path}")
    for path in chart_paths:
        print(f"Chart written to: {path}")


if __name__ == "__main__":
    main()
