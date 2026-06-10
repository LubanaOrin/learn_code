"""Build a Google Sheets-ready dashboard workbook for the capstone.

The college requires a dashboard in a tool such as Tableau, Google Sheets, or
Power BI. This script creates an XLSX workbook with dashboard sheets, summary
tables, and native charts that can be uploaded to Google Drive and opened as a
Google Sheets dashboard.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter


TASK_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = TASK_DIR / "outputs"
DASHBOARD_DIR = OUTPUT_DIR / "google_sheets_dashboard"
WORKBOOK_PATH = DASHBOARD_DIR / "osmi_mental_health_google_sheets_dashboard.xlsx"

INK = "1F2933"
MUTED = "5F6B7A"
TEAL = "2F6F73"
RED = "C25746"
GOLD = "D39B5F"
VIOLET = "6D4C7D"
LIGHT = "F6F7F9"
LINE = "D8DEE6"
WHITE = "FFFFFF"


def pct(value: float) -> float:
    return round(float(value), 1)


def style_title(cell, size: int = 20, color: str = INK) -> None:
    cell.font = Font(name="Aptos Display", bold=True, size=size, color=color)
    cell.alignment = Alignment(vertical="center", wrap_text=True)


def style_header_row(ws, row: int, start_col: int, end_col: int) -> None:
    fill = PatternFill("solid", fgColor=INK)
    font = Font(name="Aptos", bold=True, color=WHITE)
    for col in range(start_col, end_col + 1):
        cell = ws.cell(row=row, column=col)
        cell.fill = fill
        cell.font = font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = Border(bottom=Side(style="thin", color=LINE))


def write_df(ws, df: pd.DataFrame, start_row: int, start_col: int) -> tuple[int, int]:
    for j, col_name in enumerate(df.columns, start=start_col):
        ws.cell(row=start_row, column=j, value=col_name)
    style_header_row(ws, start_row, start_col, start_col + len(df.columns) - 1)

    for i, row in enumerate(df.itertuples(index=False), start=start_row + 1):
        for j, value in enumerate(row, start=start_col):
            if pd.isna(value):
                value = None
            ws.cell(row=i, column=j, value=value)

    end_row = start_row + len(df)
    end_col = start_col + len(df.columns) - 1
    for col in range(start_col, end_col + 1):
        ws.column_dimensions[get_column_letter(col)].width = min(
            28, max(12, max(len(str(ws.cell(row=r, column=col).value or "")) for r in range(start_row, end_row + 1)) + 2)
        )
    return end_row, end_col


def make_bar_chart(
    ws,
    title: str,
    data_min_col: int,
    data_min_row: int,
    data_max_row: int,
    cat_col: int,
    anchor: str,
    y_axis_title: str = "Treatment rate (%)",
    height: float = 7.0,
    width: float = 11.0,
) -> BarChart:
    chart = BarChart()
    chart.type = "col"
    chart.style = 10
    chart.title = title
    chart.y_axis.title = y_axis_title
    chart.x_axis.title = ""
    chart.height = height
    chart.width = width
    data = Reference(ws, min_col=data_min_col, min_row=data_min_row, max_row=data_max_row)
    cats = Reference(ws, min_col=cat_col, min_row=data_min_row + 1, max_row=data_max_row)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.legend = None
    if anchor:
        ws.add_chart(chart, anchor)
    return chart


def setup_sheet(ws, title: str) -> None:
    ws.sheet_view.showGridLines = False
    ws.freeze_panes = "A4"
    ws["A1"] = title
    style_title(ws["A1"], 18)
    ws["A2"] = "OSMI Mental Health in Tech Survey | Data Analytics Capstone Project"
    ws["A2"].font = Font(name="Aptos", size=11, color=MUTED)
    ws.row_dimensions[1].height = 28


def build_workbook() -> None:
    DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)

    executive = pd.read_csv(OUTPUT_DIR / "executive_summary_metrics.csv")
    benefits = pd.read_csv(OUTPUT_DIR / "treatment_by_benefits.csv")
    care = pd.read_csv(OUTPUT_DIR / "treatment_by_care_options.csv")
    work = pd.read_csv(OUTPUT_DIR / "treatment_by_work_interfere.csv")
    company = pd.read_csv(OUTPUT_DIR / "treatment_by_company_size.csv")
    family = pd.read_csv(OUTPUT_DIR / "treatment_by_family_history.csv")
    tests = pd.read_csv(OUTPUT_DIR / "hypothesis_test_results.csv")
    model = pd.read_csv(OUTPUT_DIR / "treatment_model_performance.csv")
    coefficients = pd.read_csv(OUTPUT_DIR / "treatment_model_coefficients.csv")

    wb = Workbook()
    dashboard = wb.active
    dashboard.title = "Dashboard"
    data_ws = wb.create_sheet("Dashboard_Data")
    tests_ws = wb.create_sheet("Hypothesis_Tests")
    model_ws = wb.create_sheet("Model")
    readme_ws = wb.create_sheet("README")

    for ws in [dashboard, data_ws, tests_ws, model_ws, readme_ws]:
        ws.sheet_view.showGridLines = False

    setup_sheet(dashboard, "Workplace Mental Health Dashboard")

    dashboard["A4"] = "Main finding"
    dashboard["A4"].font = Font(name="Aptos", bold=True, size=13, color=TEAL)
    dashboard["A5"] = (
        "Treatment-seeking is common in the sample, but workplace disclosure comfort is much lower. "
        "Support visibility, perceived consequences, and work interference are strongly associated with the outcomes."
    )
    dashboard["A5"].alignment = Alignment(wrap_text=True, vertical="top")
    dashboard.merge_cells("A5:H6")

    kpi_values = {
        row["metric"]: row["value"] for _, row in executive.iterrows()
    }
    kpis = [
        ("Survey responses", kpi_values["Total survey responses"]),
        ("Sought treatment", kpi_values["Sought mental health treatment"]),
        ("Know benefits", kpi_values["Know employer provides mental health benefits"]),
        ("Any work interference", kpi_values["Report any work interference"]),
        ("Supervisor comfort", kpi_values["Comfortable discussing mental health with supervisor"]),
        ("Coworker comfort", kpi_values["Comfortable discussing mental health with coworkers"]),
    ]
    start_cells = ["A8", "D8", "G8", "A12", "D12", "G12"]
    for (label, value), cell_ref in zip(kpis, start_cells):
        cell = dashboard[cell_ref]
        row = cell.row
        col = cell.column
        dashboard.merge_cells(start_row=row, start_column=col, end_row=row + 2, end_column=col + 1)
        merged = dashboard.cell(row=row, column=col)
        merged.value = f"{label}\n{value}"
        merged.font = Font(name="Aptos", bold=True, size=13, color=INK)
        merged.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        merged.fill = PatternFill("solid", fgColor=WHITE)
        merged.border = Border(
            left=Side(style="thin", color=LINE),
            right=Side(style="thin", color=LINE),
            top=Side(style="thin", color=LINE),
            bottom=Side(style="thin", color=LINE),
        )

    for col in range(1, 10):
        dashboard.column_dimensions[get_column_letter(col)].width = 16
    for row in range(1, 32):
        dashboard.row_dimensions[row].height = 22

    setup_sheet(data_ws, "Dashboard Source Tables")
    row = 4
    data_ws["A4"] = "Treatment rate by benefits"
    style_title(data_ws["A4"], 13, TEAL)
    row += 1
    end_row_benefits, _ = write_df(data_ws, benefits[["benefits", "respondents", "treatment_rate_percent"]], row, 1)

    row = end_row_benefits + 3
    data_ws.cell(row=row, column=1, value="Treatment rate by care options")
    style_title(data_ws.cell(row=row, column=1), 13, TEAL)
    row += 1
    end_row_care, _ = write_df(data_ws, care[["care_options", "respondents", "treatment_rate_percent"]], row, 1)

    row = end_row_care + 3
    data_ws.cell(row=row, column=1, value="Treatment rate by work interference")
    style_title(data_ws.cell(row=row, column=1), 13, TEAL)
    row += 1
    end_row_work, _ = write_df(data_ws, work[["work_interfere", "respondents", "treatment_rate_percent"]], row, 1)

    row = end_row_work + 3
    data_ws.cell(row=row, column=1, value="Treatment rate by company size")
    style_title(data_ws.cell(row=row, column=1), 13, TEAL)
    row += 1
    end_row_company, _ = write_df(data_ws, company[["no_employees", "respondents", "treatment_rate_percent"]], row, 1)

    row = end_row_company + 3
    data_ws.cell(row=row, column=1, value="Treatment rate by family history")
    style_title(data_ws.cell(row=row, column=1), 13, TEAL)
    row += 1
    write_df(data_ws, family[["family_history", "respondents", "treatment_rate_percent"]], row, 1)

    setup_sheet(tests_ws, "Hypothesis Test Results")
    tests_display = tests.copy()
    tests_display["p_value"] = tests_display["p_value"].round(6)
    write_df(tests_ws, tests_display, 4, 1)

    setup_sheet(model_ws, "Model Results")
    write_df(model_ws, model, 4, 1)
    model_metrics = pd.DataFrame(
        {
            "metric": ["ROC AUC", "Accuracy", "Precision", "Recall", "F1 score"],
            "score": [
                model.loc[0, "roc_auc"],
                model.loc[0, "accuracy"],
                model.loc[0, "precision_treatment_yes"],
                model.loc[0, "recall_treatment_yes"],
                model.loc[0, "f1_treatment_yes"],
            ],
        }
    )
    write_df(model_ws, model_metrics, 8, 1)
    model_ws["A16"] = "Top model coefficients"
    style_title(model_ws["A16"], 13, TEAL)
    write_df(model_ws, coefficients.head(15), 17, 1)

    make_bar_chart(data_ws, "Treatment Rate By Benefits", 3, 6, end_row_benefits, 1, "E5")
    make_bar_chart(data_ws, "Treatment Rate By Care Options", 3, end_row_benefits + 5, end_row_care, 1, "E21")
    make_bar_chart(data_ws, "Treatment Rate By Work Interference", 3, end_row_care + 5, end_row_work, 1, "E37")
    make_bar_chart(data_ws, "Treatment Rate By Company Size", 3, end_row_work + 5, end_row_company, 1, "E53")
    make_bar_chart(model_ws, "Model Performance", 2, 8, 13, 1, "E4", "Score")

    # Dashboard charts read from the source sheets.
    chart = make_bar_chart(data_ws, "Treatment Rate By Benefits", 3, 6, end_row_benefits, 1, None)
    chart.height = 7.5
    chart.width = 12
    dashboard.add_chart(chart, "A17")

    chart = make_bar_chart(data_ws, "Treatment Rate By Work Interference", 3, end_row_care + 5, end_row_work, 1, None)
    chart.height = 7.5
    chart.width = 12
    dashboard.add_chart(chart, "J17")

    chart = make_bar_chart(model_ws, "Logistic Regression Model Performance", 2, 8, 13, 1, None, "Score")
    chart.height = 7.5
    chart.width = 12
    dashboard.add_chart(chart, "A35")

    readme_ws["A1"] = "Dashboard Submission Notes"
    style_title(readme_ws["A1"], 18)
    notes = [
        "This workbook is designed to be uploaded to Google Drive and opened as Google Sheets.",
        "Use the Dashboard sheet as the submitted dashboard.",
        "Dashboard_Data contains the chart source tables.",
        "Hypothesis_Tests contains statistical test results.",
        "Model contains logistic regression model performance and coefficients.",
        "The supplementary notebook and report contain the same chart story and reproducible analysis.",
    ]
    for i, note in enumerate(notes, start=3):
        readme_ws.cell(row=i, column=1, value=note)
        readme_ws.cell(row=i, column=1).alignment = Alignment(wrap_text=True)
    readme_ws.column_dimensions["A"].width = 110

    for ws in wb.worksheets:
        for row_cells in ws.iter_rows():
            for cell in row_cells:
                cell.font = cell.font.copy(name="Aptos")
                cell.alignment = cell.alignment.copy(vertical="center")

    wb.save(WORKBOOK_PATH)
    print(f"Saved Google Sheets-ready dashboard workbook: {WORKBOOK_PATH}")


if __name__ == "__main__":
    build_workbook()
