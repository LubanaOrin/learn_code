# Customer Segmentation Using RFM Analysis

## Project Overview

This project uses RFM analysis to segment customers based on purchasing behavior.

RFM stands for:

- Recency: how recently a customer purchased.
- Frequency: how often a customer purchased.
- Monetary value: how much revenue a customer generated.

The goal is to identify high-value customer groups, customers at risk of churn, and marketing actions for retention, reactivation, and cross-sell campaigns.

## Main Deliverables

- `RFM Customer Segmentation Dashboard.pbix`: Power BI dashboard file.
- `RFM Customer Segmentation Dashboard.pdf`: dashboard PDF preview.
- `rfm_segment_summary.csv`: previewable summary of customer segments and revenue contribution.
- `sql/rfm_customer_segmentation.sql`: SQL workflow for RFM calculation and segmentation.

## Business Question

Which customer groups should the marketing team prioritize based on recency, frequency, and monetary value?

## Method

1. Filter transactions to one year of data: **2010-12-01 to 2011-12-01**.
2. Clean transaction records by removing missing customers and invalid transaction values.
3. Calculate each customer's recency, frequency, and monetary value.
4. Use quartiles to assign R, F, and M scores.
5. Combine scores into a customer segment.
6. Build a Power BI dashboard to compare customer count, revenue, and average RFM score by segment.

## Customer Segments

- Best Customers: recent, frequent, high-value customers.
- Loyal Customers: frequent and engaged customers.
- Big Spenders: high monetary value customers.
- Lost Customers: customers who have not purchased recently.
- Other: customers who do not fit the main strategic groups.

## Key Metrics

- Total customers: **4,297**
- Total revenue: **$8.39M**
- Average RFM score: **2.45**
- Best Customers: about **10%** of customers and **48%** of revenue.

## Key Findings

- Best Customers generate **$4.02M** out of **$8.39M** total revenue.
- Loyal Customers generate **$2.20M**, around 5 times more than Lost Customers.
- Lost Customers are similar in size to Loyal Customers, but generate much less revenue.
- The largest group is Other customers, with **1,740** customers and **$1.08M** revenue.
- Revenue is highly concentrated among high-value customer segments.

## Recommendations

- Protect Best and Loyal Customers with retention campaigns, loyalty rewards, and cross-sell offers.
- Re-activate Lost and stale customers with time-bound win-back offers.
- Convert recent low-engagement customers into repeat buyers through onboarding, reminders, and small incentives.
- Track segment movement over time to see whether marketing actions improve retention and customer value.

## Skills Demonstrated

- RFM analysis
- Customer segmentation
- SQL data cleaning and scoring
- Quartile-based scoring with `APPROX_QUANTILES`
- Power BI dashboard design
- Revenue concentration analysis
- Marketing recommendation development

## How to Review

Open the dashboard preview:

```text
RFM Customer Segmentation Dashboard.pdf
```

Open the Power BI file:

```text
RFM Customer Segmentation Dashboard.pbix
```

Review the SQL workflow:

```text
sql/rfm_customer_segmentation.sql
```

Preview the segment summary:

```text
rfm_segment_summary.csv
```

If viewing the `.pbix` file on GitHub, use **View raw** or **Download** to open it locally in Power BI Desktop.
