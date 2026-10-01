# Ecommerce Analytics Engine

Turns a store's raw order export (CSV / Excel / JSON — Shopify, WooCommerce, or any
platform's order list) into a cleaned dataset plus a multi-sheet Excel report covering
sales trends, customer behavior, and product performance.
510 orders processed in under 1 second.

## Quick Start (Windows)

```
py -m pip install -r requirements.txt
py main.py orders_sample.csv
py main.py client_orders.xlsx -o Client_Report.xlsx
```
Output is saved in the `output/` folder.

## What it does

1. **Connects** — reads orders from CSV/Excel/JSON; auto-detects columns regardless of
   naming (`Order Date`, `Created At`, `Purchase Date` all map to the same field), so it
   works with real-world exports, not just one fixed template.
2. **Cleans** — removes rows missing required fields, fixes/validates dates and totals,
   drops duplicate orders (by Order ID), and flags statistical outliers (IQR method) on
   order value so unusually large/small orders get reviewed, not silently averaged in.
3. **Analyzes**
   - **Sales trends** — daily and monthly order count & revenue
   - **Customer behavior** — repeat vs. one-time customers, average order value, top
     customers by spend and recency
   - **Product performance** — top products and categories by revenue/units sold
4. **Reports** — a formatted Excel workbook with a Summary sheet, trend charts
   (line chart for monthly revenue, bar chart for top products), and filterable data
   sheets — easy to hand to a non-technical client or plug into Google Sheets/Looker
   Studio for a live dashboard.

## Output Excel

- **Summary** — orders in/out, rows cleaned/removed, outliers flagged, customer overview
- **Sales_Trends_Daily / Sales_Trends_Monthly** — orders & revenue over time, with chart
- **Customer_Behavior** — top customers: orders, total spent, avg order value, recency
- **Product_Performance** — top products by revenue/units, with chart
- **Category_Breakdown** — revenue by product category

## Settings (`config.py`)

`DATE_DAYFIRST`, outlier method (`OUTLIER_METHOD`: `iqr` or `zscore`), top-N customers/
products shown, and the header keyword lists used for column auto-detection.

## Portfolio sample

`portfolio_sample/` contains a generated demo order file (`Orders_Sample.csv`, fake data
— not a real client's) and the resulting `Ecommerce_Analytics_Report_SAMPLE.xlsx`,
showing the full pipeline end to end.

## License

All Rights Reserved — shared publicly for portfolio/demonstration purposes only.
See [LICENSE](LICENSE). No reuse, copying, or redistribution without permission.
