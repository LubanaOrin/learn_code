# Fast Food Marketing Campaign A/B Test

## Project Overview

This project analyzes a fast-food marketing experiment comparing three promotional campaigns.

The goal is to identify which promotion generated the strongest sales performance across store locations and recommend which campaign should be rolled out more broadly.

## Main Deliverables

- `Fast Food Marketing Campaign AB Test.pdf`: final written analysis report.
- `promotion_summary_statistics.csv`: promotion-level summary metrics.
- `pairwise_test_results.csv`: statistical test results.
- `sql/01_store_promotion_sales.sql`: SQL for aggregating weekly sales by store and promotion.
- `sql/02_promotion_summary_statistics.sql`: SQL for promotion-level summary statistics.

## Business Question

Which of the three marketing promotions should the business choose based on average sales performance?

## Method

1. Aggregate weekly sales into total sales per store and promotion.
2. Calculate average sales for each promotion.
3. Compare promotions using pairwise two-sample t-tests.
4. Use a **99% confidence level** because three pairwise comparisons increase the risk of false positives.
5. Interpret p-values and confidence intervals to make a business recommendation.

## Target Metric

Average total sales, in thousands, per location across the four-week test period.

## Results Summary

| Comparison | Mean Difference | p-value | 99% Confidence Interval | Result |
|---|---:|---:|---|---|
| Promotion 1 vs Promotion 2 | 43.08 | 0.00128 | [9.05, 77.11] | Significant |
| Promotion 1 vs Promotion 3 | 10.94 | 0.43 | [-25.05, 46.93] | Not significant |
| Promotion 2 vs Promotion 3 | -32.14 | 0.0136 | [-65.70, 1.42] | Not significant at 99% |

## Key Findings

- Promotion 1 had the highest average sales at **232.40** thousand.
- Promotion 3 followed with **221.46** thousand.
- Promotion 2 had the lowest average sales at **189.32** thousand.
- Promotion 1 significantly outperformed Promotion 2 at the 99% confidence level.
- Promotion 1 did not significantly outperform Promotion 3 at the 99% confidence level.
- Promotion 2 and Promotion 3 were not significantly different at the 99% confidence level.

## Recommendation

Roll out **Promotion 1** as the preferred campaign because it has the highest average sales and significantly outperforms Promotion 2.

Promotion 3 should remain a reasonable alternative if cost, execution difficulty, or market fit makes it more attractive than Promotion 1.

## Limitations

- The dataset does not include campaign cost, so ROI cannot be calculated.
- Store size, customer traffic, local demographics, and baseline sales are not included.
- The test covers a limited period, so results may change over a longer campaign window.
- Promotion 1 and Promotion 3 were not statistically different, so the business should compare implementation cost before making a final rollout decision.

## Skills Demonstrated

- A/B test analysis
- Pairwise statistical testing
- Two-sample t-test interpretation
- Confidence intervals
- Multiple-comparison awareness
- SQL aggregation
- Business recommendation writing

## How to Review

Open the final report:

```text
Fast Food Marketing Campaign AB Test.pdf
```

Review the SQL logic:

```text
sql/
```

Preview the results:

```text
promotion_summary_statistics.csv
pairwise_test_results.csv
```
