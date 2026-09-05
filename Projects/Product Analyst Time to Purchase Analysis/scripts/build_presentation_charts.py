"""Build clean, presentation-sized chart images for the Product Analyst deck."""

from __future__ import annotations

from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd


TASK_DIR = Path(__file__).resolve().parents[1]
CHART_DIR = TASK_DIR / "outputs" / "charts"

BLUE = "#2878B5"
ORANGE = "#E76F51"
GREEN = "#3A9D5D"
PURPLE = "#8561A8"
INK = "#24313D"
MUTED = "#5F6B7A"
GRID = "#E6EAF0"


def style_axis(ax, *, y_grid: bool = True) -> None:
    ax.set_facecolor("white")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#B9C2CC")
    ax.spines["bottom"].set_color("#B9C2CC")
    ax.tick_params(axis="both", labelsize=16, colors=INK, length=0, pad=8)
    ax.grid(False)
    if y_grid:
        ax.grid(axis="y", color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)


def save(fig, name: str) -> None:
    fig.savefig(CHART_DIR / name, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main() -> None:
    CHART_DIR.mkdir(parents=True, exist_ok=True)
    daily = pd.read_csv(TASK_DIR / "data" / "daily_time_to_purchase.csv", parse_dates=["event_date"])
    user = pd.read_csv(TASK_DIR / "data" / "user_level_time_to_purchase.csv", parse_dates=["event_date"])

    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "axes.labelcolor": INK,
        "axes.titlecolor": INK,
        "text.color": INK,
        "axes.titleweight": "bold",
    })

    # Daily median and middle 50%.
    fig, ax = plt.subplots(figsize=(12.8, 6.4))
    ax.fill_between(
        daily["event_date"],
        daily["p25_duration_minutes"],
        daily["p75_duration_minutes"],
        color=BLUE,
        alpha=0.14,
        linewidth=0,
        label="Middle 50%",
    )
    ax.plot(
        daily["event_date"],
        daily["median_duration_minutes"],
        color=BLUE,
        linewidth=3.2,
        label="Median",
    )
    ax.axhline(18.72, color=ORANGE, linewidth=1.8, linestyle="--", label="Period benchmark: 18.72 min")
    ax.set_ylabel("Minutes to first purchase", fontsize=18, labelpad=12)
    ax.set_xlabel("")
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.set_ylim(bottom=0)
    style_axis(ax)
    ax.legend(frameon=False, fontsize=15, ncol=3, loc="upper left")
    fig.tight_layout()
    save(fig, "daily_median_time_to_purchase.png")

    # Average versus median.
    fig, ax = plt.subplots(figsize=(12.8, 6.4))
    ax.plot(daily["event_date"], daily["avg_duration_minutes"], color=ORANGE, linewidth=2.7, label="Daily average")
    ax.plot(daily["event_date"], daily["median_duration_minutes"], color=BLUE, linewidth=3.2, label="Daily median")
    ax.set_ylabel("Minutes to first purchase", fontsize=18, labelpad=12)
    ax.set_xlabel("")
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.set_ylim(bottom=0)
    style_axis(ax)
    ax.legend(frameon=False, fontsize=16, ncol=2, loc="upper left")
    fig.tight_layout()
    save(fig, "average_vs_median_time_to_purchase.png")

    # Daily purchasing users.
    fig, ax = plt.subplots(figsize=(12.8, 6.0))
    ax.bar(daily["event_date"], daily["purchasing_users_count"], color=GREEN, width=0.85)
    ax.set_ylabel("Same-day purchasers", fontsize=18, labelpad=12)
    ax.set_xlabel("")
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.set_ylim(bottom=0)
    style_axis(ax)
    fig.tight_layout()
    save(fig, "daily_purchasing_users.png")

    # Device median.
    device = (
        user.groupby("device_category")
        .agg(
            purchasing_users=("user_pseudo_id", "count"),
            median_minutes=("duration_to_purchase_minutes", "median"),
        )
        .round(2)
        .reindex(["desktop", "mobile", "tablet"])
    )
    fig, ax = plt.subplots(figsize=(10.6, 6.2))
    bars = ax.bar(
        ["Desktop", "Mobile", "Tablet"],
        device["median_minutes"],
        color=[BLUE, ORANGE, GREEN],
        width=0.62,
    )
    for bar, (_, row) in zip(bars, device.iterrows()):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.55,
            f"{row['median_minutes']:.1f} min\nn={int(row['purchasing_users']):,}",
            ha="center",
            va="bottom",
            fontsize=16,
            color=INK,
            fontweight="bold",
        )
    ax.set_ylabel("Median minutes", fontsize=18, labelpad=12)
    ax.set_ylim(0, 24)
    style_axis(ax)
    fig.tight_layout()
    save(fig, "device_median_time_to_purchase.png")

    # Top countries by volume.
    country = (
        user.groupby("country")
        .agg(
            purchasing_users=("user_pseudo_id", "count"),
            median_minutes=("duration_to_purchase_minutes", "median"),
        )
        .round(2)
        .sort_values("purchasing_users", ascending=False)
        .head(10)
        .sort_values("median_minutes")
    )
    fig, ax = plt.subplots(figsize=(11.5, 7.0))
    bars = ax.barh(country.index, country["median_minutes"], color=PURPLE, height=0.68)
    for bar, (_, row) in zip(bars, country.iterrows()):
        ax.text(
            bar.get_width() + 0.25,
            bar.get_y() + bar.get_height() / 2,
            f"{row['median_minutes']:.1f} min",
            va="center",
            fontsize=14,
            color=INK,
            fontweight="bold",
        )
    ax.set_xlabel("Median minutes to first purchase", fontsize=18, labelpad=12)
    ax.set_ylabel("")
    ax.set_xlim(0, max(country["median_minutes"]) + 4)
    style_axis(ax, y_grid=False)
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    fig.tight_layout()
    save(fig, "top_country_median_time_to_purchase.png")

    print(f"Saved presentation charts to {CHART_DIR}")


if __name__ == "__main__":
    main()
