# AdventureWorks Relational Data Exploration

## Project Overview

This project uses SQL to explore the AdventureWorks database and answer business-style data questions across related tables.

The work focuses on joining product, category, work order, location, special offer, vendor, contact, and address tables. The goal was to practice relational data exploration, query validation, and clean SQL formatting.

## Main Deliverables

- `AdventureWorks SQL Tasks Results and Queries.xlsx`: workbook containing query results and corresponding SQL query sheets.
- `adventureworks_relational_data_exploration.sql`: cleaned SQL script with all task queries.

The SQL file contains multiple separate queries in one script. Each query is clearly marked with a task number, such as `Task 1.1`, `Task 2.2`, or `Task 3.1`. This keeps the project easy to download and review while still showing every SQL solution.

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

| Task | Output | Main Outcome |
|---|---:|---|
| 1.1 | 295 rows | Retrieved products that have a product subcategory. |
| 1.2 | 295 rows | Added product category names so products can be reviewed by category and subcategory. |
| 1.3 | 19 rows | Found actively sold bikes with a list price greater than 2000. The highest listed products were Road-250 bike variants at 2443.35. |
| 2.1 | 7 rows | Summarized January 2004 work orders by location. Location 10 had the highest actual cost in this output, at 37730.25. |
| 2.2 | 7 rows | Added location names and average work duration. Subassembly had the highest work order count and the longest average duration, 11.59 days. |
| 2.3 | 999 rows | Identified January 2004 work orders with total actual cost greater than 300. |
| 3.1 | 8607 rows | Fixed the special-offer order query by joining on both `ProductID` and `SpecialOfferID`, preventing incorrect matches. |
| 3.2 | 156 rows | Fixed the vendor query by correcting aliases and joining vendor addresses to addresses through `AddressId`. |
 
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

The Excel workbook is organized with paired sheets for each task:

- `1.1 Result` and `1.1 Query`
- `1.2 Result` and `1.2 Query`
- `1.3 Result` and `1.3 Query`
- `2.1 Result` and `2.1 Query`
- `2.2 Result` and `2.2 Query`
- `2.3 Result` and `2.3 Query`
- `3.1 Result` and `3.1 Query`
- `3.2 Result` and `3.2 Query`

This makes it easy to compare each SQL query with its output.

## How to Review

Open the Excel workbook to review the query results:

```text
AdventureWorks SQL Tasks Results and Queries.xlsx
```

Open the SQL file to review the cleaned query script:

```text
adventureworks_relational_data_exploration.sql
```

If viewing the Excel workbook on GitHub, click the file and use **View raw** or **Download** to open it locally in Excel.
