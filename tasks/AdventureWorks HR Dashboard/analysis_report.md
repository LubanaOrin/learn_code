# AdventureWorks HR Dashboard Analysis Report

## Project Choice

Project type: HR dashboard

Target audience: HR managers and leadership

## Questions

- Has total employee count increased or decreased over time?
- Which years saw the highest hiring activity?
- How does hiring vary across departments?
- What is the current active headcount?
- What is the employee gender ratio?
- What is the average employee tenure?
- Are there visible transfer or attrition patterns?

## Key KPIs

- Total active employees
- New hires per year
- Employees by department
- New hires year-over-year percentage
- Total departments
- Gender ratio
- Average tenure
- Transfer rate
- Attrition rate

## Data Preparation

Selected tables:

- `Employee`
- `EmployeeDepartmentHistory`
- `Department`
- `Shift`
- `EmployeePayHistory`
- `BusinessEntity`
- `BusinessEntityAddress`
- `Address`
- `StateProvince`
- `CountryRegion`

Main relationships used:

- `Employee[BusinessEntityID]` to `BusinessEntity[BusinessEntityID]`
- `BusinessEntity[BusinessEntityID]` to `BusinessEntityAddress[BusinessEntityID]`
- `BusinessEntityAddress[AddressID]` to `Address[AddressID]`
- `Address[StateProvinceID]` to `StateProvince[StateProvinceID]`
- `StateProvince[CountryRegionCode]` to `CountryRegion[CountryRegionCode]`
- `Employee[BusinessEntityID]` to `EmployeeDepartmentHistory[BusinessEntityID]`
- `EmployeeDepartmentHistory[DepartmentID]` to `Department[DepartmentID]`

## Important Measures

```DAX
Active Headcount =
VAR TotalActives =
    COUNTROWS ( FILTER ( Employee, Employee[CurrentFlag] = TRUE() ) )
RETURN
    COALESCE ( TotalActives, 0 )
```

```DAX
New Hires =
VAR SelectedYear = SELECTEDVALUE ( DimDate[Year] )
RETURN
IF (
    ISBLANK ( SelectedYear ),
    COUNTROWS ( Employee ),
    CALCULATE (
        COUNTROWS ( Employee ),
        FILTER ( Employee, YEAR ( Employee[HireDate] ) = SelectedYear )
    )
)
```

```DAX
Employees by Department =
CALCULATE (
    DISTINCTCOUNT ( EmployeeDepartmentHistory[BusinessEntityID] ),
    FILTER (
        EmployeeDepartmentHistory,
        ISBLANK ( EmployeeDepartmentHistory[EndDate] )
    ),
    Employee[CurrentFlag] = TRUE()
)
```

```DAX
Total Departments =
DISTINCTCOUNT ( Department[DepartmentID] )
```

```DAX
Transferred Employees =
VAR Transfers =
    CALCULATETABLE (
        VALUES ( EmployeeDepartmentHistory[BusinessEntityID] ),
        NOT ( ISBLANK ( EmployeeDepartmentHistory[EndDate] ) )
    )
RETURN
    COUNTROWS ( Transfers )
```

```DAX
Terminated Employees =
VAR TerminatedCount =
    CALCULATE (
        DISTINCTCOUNT ( Employee[BusinessEntityID] ),
        FILTER ( Employee, Employee[CurrentFlag] = FALSE() )
    )
RETURN
    COALESCE ( TerminatedCount, 0 )
```

```DAX
Attrition Rate % =
VAR Terminated = [Terminated Employees]
VAR Total = [Total Employees]
RETURN
    IF ( Total > 0, DIVIDE ( Terminated, Total ), 0 )
```

## Dashboard Layout

- Year slicer using `DimDate[Year]`
- KPI cards for active employees, new hires, year-over-year hiring change, and total departments
- Line chart for hiring trend over time
- Bar chart for employees by department
- Cards for gender ratio and average tenure
- Map view for employee distribution by country

## Insights

- The workforce contains **290 employees**.
- Hiring activity appears across **2006 to 2013**.
- The dashboard shows hiring fluctuations by year, highlighting stronger and weaker recruitment periods.
- Since every employee in the dataset is marked as active, the total active headcount remains constant.
- Production is the largest department, followed by Sales and Engineering.
- Transfer activity is limited, with only small movement across departments.
- Attrition is shown as **0%**, which may indicate either strong retention or missing termination records.

## Limitations

- The dataset does not include a clear resignation or termination date field.
- Because all employees are marked as active, true historical attrition cannot be measured confidently.
- Some date-model relationships required manual checking.
- Date-format differences made time-based modeling more difficult.
- The dashboard should be interpreted as a workforce snapshot rather than a complete employee lifecycle model.

## Future Analysis

- Add termination or exit-date data to measure attrition accurately.
- Connect performance and compensation data for deeper workforce analysis.
- Compare tenure, pay, department, and transfer behavior.
- Add hiring source or recruitment channel data if available.
- Track department-level growth and movement over time.
