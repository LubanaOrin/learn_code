# AdventureWorks Advanced Data Exploration

## Project Overview

This project uses advanced SQL to explore AdventureWorks customer and sales data.

The work focuses on customer segmentation, inactive-customer identification, active-customer flags, North America customer filtering, monthly sales reporting, cumulative sales totals, sales ranking, and country-level tax context.

## Main Deliverables

- `AdventureWorks Advanced SQL Query Results.xlsx`: workbook containing only the query result sheets.
- `sql/`: folder containing one SQL file for each query.

The Excel workbook is kept for outputs only. The SQL queries are stored separately so each task can be reviewed directly on GitHub.

## Business Questions

The project answers two groups of business questions:

1. Customer overview:
   - Who are the top individual customers by total amount with tax?
   - Which high-value customers have not ordered in the last 365 days?
   - Which customers are active or inactive?
   - Which active North America customers meet value or order-count thresholds?

2. Sales reporting:
   - What are monthly sales figures by country and region?
   - What are cumulative sales totals by country and region?
   - Which regions rank highest within each country/month?
   - What tax-rate context is available by country?

## Results Summary

| Task | SQL File | Excel Result Sheet | Output | Main Outcome |
|---|---|---|---:|---|
| 1.1 | `sql/01_top_individual_customers.sql` | `1.1 Result` | 200 rows | Returned the top individual customers by total amount with tax. |
| 1.2 | `sql/02_inactive_top_customers.sql` | `1.2 Result` | 200 rows | Identified high-value individual customers who had not ordered in the last 365 days. |
| 1.3 | `sql/03_customers_with_active_status.sql` | `1.3 Result` | 500 rows | Added an active/inactive customer status based on the latest order date in the database. |
| 1.4 | `sql/04_active_north_america_customers.sql` | `1.4 Result` | 3680 rows | Returned active North America customers meeting either the value threshold or order-count threshold, with address split into number and street columns. |
| 2.1 | `sql/05_monthly_sales_by_country_region.sql` | `2.1 Results` | 368 rows | Reported monthly orders, customers, salespeople, and total amount with tax by country and region. |
| 2.2 | `sql/06_monthly_sales_cumulative.sql` | `2.2 Result` | 368 rows | Added cumulative sales totals by country and region. |
| 2.3 | `sql/07_monthly_sales_rank.sql` | `2.3 Result` | 368 rows | Added a sales rank to compare regional performance within the reporting output. |
| 2.4 | `sql/08_monthly_sales_tax_details.sql` | `2.4 Result` | 368 rows | Added country-level mean tax rate and province tax-coverage percentage. |

## Skills Demonstrated

- SQL joins across customer, sales, address, territory, and tax tables
- Common table expressions
- Customer segmentation
- Date-based active/inactive logic
- String parsing for address fields
- Monthly sales aggregation
- Window functions for cumulative sums and ranking
- Tax-rate summarization and coverage calculation
- Clean SQL formatting and readable aliases

## Workbook Structure

The Excel workbook is organized with one result sheet for each task:

- `1.1 Result`
- `1.2 Result`
- `1.3 Result`
- `1.4 Result`
- `2.1 Results`
- `2.2 Result`
- `2.3 Result`
- `2.4 Result`

The matching SQL files are stored in the `sql/` folder.

## How to Review

Open the Excel workbook to review the query results:

```text
AdventureWorks Advanced SQL Query Results.xlsx
```

Open the `sql/` folder to review the query files:

```text
sql/
```

If viewing the Excel workbook on GitHub, click the file and use **View raw** or **Download** to open it locally in Excel.
