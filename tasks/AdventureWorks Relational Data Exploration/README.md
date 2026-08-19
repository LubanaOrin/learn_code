# AdventureWorks Relational Data Exploration

## Project Overview

This project uses SQL to explore the AdventureWorks database and answer business-style data questions across related tables.

The work focuses on joining product, category, work order, location, special offer, vendor, contact, and address tables. The goal was to practice relational data exploration, query validation, and clean SQL formatting.

## Main Deliverables

- `AdventureWorks SQL Query Results.xlsx`: workbook containing only the query result sheets.
- `sql/`: folder containing one SQL file for each query.

The Excel workbook is kept for outputs only. The SQL queries are stored separately so each task can be reviewed directly on GitHub.

## Business And Technical Questions

The project answers three groups of tasks:

1. Product overview:
   - List products with product subcategories.
   - Add product category names.
   - Identify the most expensive actively sold bikes.

2. Work order review:
   - Summarize January 2004 work orders by location.
   - Add location names and average work duration.
   - Find work orders with actual cost greater than 300.

3. Query validation:
   - Fix a special-offer order query where join logic created incorrect results.
   - Fix a vendor information query with alias and join errors.

## Results Summary

| Task | SQL File | Excel Result Sheet | Output | Main Outcome |
|---|---|---|---:|---|
| 1.1 | `sql/01_products_with_subcategories.sql` | `1.1 Result` | 295 rows | Retrieved products that have a product subcategory. |
| 1.2 | `sql/02_products_with_categories.sql` | `1.2 Result` | 295 rows | Added product category names so products can be reviewed by category and subcategory. |
| 1.3 | `sql/03_expensive_active_bikes.sql` | `1.3 Result` | 19 rows | Found actively sold bikes with a list price greater than 2000. The highest listed products were Road-250 bike variants at 2443.35. |
| 2.1 | `sql/04_work_orders_by_location.sql` | `2.1 Result` | 7 rows | Summarized January 2004 work orders by location. Location 10 had the highest actual cost in this output, at 37730.25. |
| 2.2 | `sql/05_work_orders_with_location_names.sql` | `2.2 Result` | 7 rows | Added location names and average work duration. Subassembly had the highest work order count and the longest average duration, 11.59 days. |
| 2.3 | `sql/06_high_cost_work_orders.sql` | `2.3 Result` | 999 rows | Identified January 2004 work orders with total actual cost greater than 300. |
| 3.1 | `sql/07_correct_special_offer_orders.sql` | `3.1 Result` | 8607 rows | Fixed the special-offer order query by joining on both `ProductID` and `SpecialOfferID`, preventing incorrect matches. |
| 3.2 | `sql/08_correct_vendor_information.sql` | `3.2 Result` | 156 rows | Fixed the vendor query by correcting aliases and joining vendor addresses to addresses through `AddressId`. |

## Main Learning Outcome

This project shows how relational databases require careful join logic. The query validation tasks were especially important because the original queries could run or nearly run while still giving incorrect or incomplete results. Correct joins and readable aliases made the outputs easier to trust and review.

## Skills Demonstrated

- SQL joins across relational tables
- Primary-key and foreign-key reasoning
- Aggregation with `COUNT`, `SUM`, and `AVG`
- Filtering with date logic
- Query validation and debugging
- Clean SQL formatting and aliases
- Documenting query results in a spreadsheet

## Workbook Structure

The Excel workbook is organized with one result sheet for each task:

- `1.1 Result`
- `1.2 Result`
- `1.3 Result`
- `2.1 Result`
- `2.2 Result`
- `2.3 Result`
- `3.1 Result`
- `3.2 Result`

The matching SQL files are stored in the `sql/` folder.

## How to Review

Open the Excel workbook to review the query results:

```text
AdventureWorks SQL Query Results.xlsx
```

Open the `sql/` folder to review the query files:

```text
sql/
```

If viewing the Excel workbook on GitHub, click the file and use **View raw** or **Download** to open it locally in Excel.
