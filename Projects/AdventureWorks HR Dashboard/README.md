# AdventureWorks HR Dashboard

## Project Overview

This project builds an interactive Power BI dashboard for AdventureWorks HR workforce analysis.

The dashboard is designed for HR managers and leadership who need a quick view of employee headcount, hiring activity, department distribution, gender ratio, tenure, transfers, attrition, and employee location patterns.

## Main Deliverables

- `AdventureWorks HR Dashboard.pbix`: Power BI dashboard file.
- `analysis_report.md`: dashboard planning notes, measures, insights, limitations, and future analysis ideas.
- `dax/`: reusable DAX code for the date table and HR measures.

## Business Questions

The dashboard focuses on these questions:

1. Has employee count increased or decreased over time?
2. Which years had the highest hiring activity?
3. How does employee distribution vary across departments?
4. What is the current active headcount?
5. What are the gender ratio and average tenure?
6. Are there signs of employee transfers or attrition?
7. Where are employees located geographically?

## Data Model

The dashboard uses AdventureWorks HR-related tables, including:

- `Employee`
- `EmployeeDepartmentHistory`
- `Department`
- `EmployeePayHistory`
- `BusinessEntity`
- `BusinessEntityAddress`
- `Address`
- `StateProvince`
- `CountryRegion`

The model connects employee, department, address, and location tables to support workforce and geographic reporting.

## Dashboard Features

- KPI cards for active headcount, new hires, year-over-year hiring change, and department count.
- Hiring trend by year.
- Employee distribution by department.
- Gender ratio and average tenure cards.
- Employee location map.
- Transfer and attrition measures.
- Year slicer for interactive filtering.

The Power BI report file contains 2 pages and 15 visual containers, including cards, slicer, line chart, bar chart, table, combo chart, and map visuals.

## Key Findings

- The dataset contains **290 employees**.
- Hiring activity is shown across **2006 to 2013**.
- Because all employees are marked as active in the dataset, the active headcount remains constant.
- Production is the largest department, followed by Sales and Engineering.
- Transfer activity appears limited and evenly distributed across departments.
- Attrition is recorded as **0%**, which may reflect either strong retention or missing termination data.

## Skills Demonstrated

- Power BI dashboard design
- Data modeling and table relationships
- DAX measures
- KPI design
- Workforce trend analysis
- Department-level segmentation
- Map-based visualization
- Communicating dashboard limitations

## How to Review

Open the Power BI file in Power BI Desktop:

```text
AdventureWorks HR Dashboard.pbix
```

Then read:

```text
analysis_report.md
```

The DAX code is also available separately:

```text
dax/
```

If viewing this project on GitHub, click the `.pbix` file and use **View raw** or **Download** to open it locally.
