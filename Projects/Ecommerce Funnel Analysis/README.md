# Ecommerce Funnel Analysis

## Project Overview

This project analyzes an ecommerce event funnel for the top 3 countries by event volume: United States, India, and Canada.

The funnel counts unique users at each step so repeated actions do not inflate the results. The goal is to understand where users drop off between session start, product view, add to cart, checkout, and purchase.

## Main Deliverables

- `Ecommerce Funnel Dashboard.xlsx`: Excel workbook with the funnel dashboard and visualization.
- `funnel_summary_top_countries.csv`: previewable summary of funnel counts and conversion rates.
- `sql/01_unique_events.sql`: SQL logic for deduplicating events by user and event type.
- `sql/02_top_country_funnel.sql`: SQL logic for the top-country funnel aggregation.

The workbook is kept for dashboard review. The SQL files are stored separately so the logic can be reviewed directly on GitHub.

## Funnel Steps

1. `session_start`
2. `view_item`
3. `add_to_cart`
4. `begin_checkout`
5. `purchase`

## Key Metrics

- Date range: **2020-11-01 to 2021-01-31**
- Top 3 countries: **United States, India, Canada**
- Total top-country sessions: **162,256**
- Total purchases across the top 3 countries: **2,703**

## Results Summary

| Funnel Step | Canada Users | India Users | United States Users |
|---|---:|---:|---:|
| Session start | 20,037 | 25,059 | 117,160 |
| View item | 4,653 | 5,795 | 26,953 |
| Add to cart | 993 | 1,162 | 5,603 |
| Begin checkout | 764 | 878 | 4,310 |
| Purchase | 355 | 406 | 1,942 |

## Key Findings

- Country-level funnel patterns are very similar across the United States, India, and Canada.
- The largest drop-off happens early: only about **23%** of session users reach `view_item`.
- The next major drop-off is from `view_item` to `add_to_cart`, where step conversion is about **20-21%**.
- Once users begin checkout, purchase completion is stronger: about **45-47%** of checkout users purchase.
- Canada has the highest final purchase conversion from session start at about **1.8%**, followed by the United States at about **1.7%** and India at about **1.6%**.

## Recommendations

- Improve the early funnel by optimizing landing pages, navigation, search, and product discovery.
- Improve add-to-cart conversion by testing clearer pricing, shipping information, product detail pages, and call-to-action placement.
- Segment the funnel further by device, traffic source, campaign, and product category to find where conversion differs most.
- Scale channels or product journeys that produce stronger product-view and add-to-cart rates.

## Skills Demonstrated

- Funnel analysis
- SQL event deduplication
- Window functions with `ROW_NUMBER`
- Top-country segmentation
- Conversion-rate and step drop-off analysis
- Excel dashboard design
- Turning funnel metrics into product recommendations

## How to Review

Open the Excel workbook:

```text
Ecommerce Funnel Dashboard.xlsx
```

Review the SQL logic:

```text
sql/
```

Preview the funnel numbers:

```text
funnel_summary_top_countries.csv
```

If viewing the workbook on GitHub, click the `.xlsx` file and use **View raw** or **Download** to open it locally in Excel.
