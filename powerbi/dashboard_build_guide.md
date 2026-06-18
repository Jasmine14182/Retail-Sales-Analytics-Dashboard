# Power BI Dashboard Build Guide

A step-by-step guide to building the Retail Sales Analytics Dashboard in Power BI Desktop.

---

## 1. Get Data

1. Open **Power BI Desktop**.
2. Click **Home → Get Data → Text/CSV**.
3. Select `data/superstore_clean.csv`.
4. Click **Transform Data** to open Power Query.
5. Verify column data types:
   - `order_date` → Date
   - `ship_date` → Date
   - `sales`, `profit`, `discount` → Decimal Number
   - `quantity`, `postal_code` → Whole Number
6. Click **Close & Apply**.

---

## 2. Create a Date Table (Required for Time Intelligence)

In Power Query, click **New Source → Blank Query**, then paste:

```m
= List.Dates(#date(2014,1,1), 1461, #duration(1,0,0,0))
```

Then convert to table → rename column to `Date` → change type to Date.

Add columns: `Year`, `Month Number`, `Month Name`, `Quarter`.

Mark this table as the **Date Table**:

```
Modeling → Mark as Date Table → choose "Date"
```

Create a relationship: `Date[Date]` → `superstore[order_date]` (Many-to-One, single direction).

---

## 3. DAX Measures

Create a new table called `_Measures` (or just put measures in the superstore table).

### Core KPIs

```dax
Total Revenue = SUM(superstore[sales])

Total Profit = SUM(superstore[profit])

Total Orders = DISTINCTCOUNT(superstore[row_id])

Total Customers = DISTINCTCOUNT(superstore[customer_name])

Total Quantity = SUM(superstore[quantity])
```

### Derived KPIs

```dax
Profit Margin % =
DIVIDE([Total Profit], [Total Revenue], 0)

Avg Order Value =
DIVIDE([Total Revenue], [Total Orders], 0)

Avg Discount =
AVERAGE(superstore[discount])

Revenue Per Customer =
DIVIDE([Total Revenue], [Total Customers], 0)
```

### Time Intelligence

```dax
Revenue YTD =
TOTALYTD([Total Revenue], 'Date'[Date])

Revenue Last Year =
SAMEPERIODLASTYEAR('Date'[Date])

Revenue YoY Growth % =
DIVIDE(
    [Total Revenue] - [Revenue Last Year],
    [Revenue Last Year],
    0
)

Revenue MTD =
TOTALMTD([Total Revenue], 'Date'[Date])
```

### Forecast Helper (for line chart)

```dax
Revenue Forecast (3 months) =
VAR hist_avg =
    AVERAGEX(
        SUMMARIZE('Date', 'Date'[Year Month Number], "Rev", [Total Revenue]),
        [Rev]
    )
VAR last_actual =
    CALCULATE([Total Revenue], LASTDATE('Date'[Date]))
RETURN
    hist_avg
```

(For a proper forecast, use the built-in **Analytics → Forecast** pane on a line chart — see step 5.)

---

## 4. Dashboard Layout (Page 1: Executive Summary)

### KPI Cards (top row, 6 cards)

| Card | Measure | Format |
|------|---------|--------|
| Total Revenue | `Total Revenue` | $ #,##0 |
| Total Profit | `Total Profit` | $ #,##0 |
| Profit Margin | `Profit Margin %` | 0.00% |
| Total Orders | `Total Orders` | #,##0 |
| Total Customers | `Total Customers` | #,##0 |
| Avg Order Value | `Avg Order Value` | $ #,##0.00 |

**How:** Modeling pane → New Card visual → drag measure into Fields → format.

### Visual 1 — Revenue & Profit Trend (Line Chart)

- Axis: `Date[Year Month Number]` (sorted by Year Month Number)
- Values: `Total Revenue`, `Total Profit`
- Add forecast:
  1. Click the chart → **Analytics** pane (magnifying glass icon)
  2. Expand **Forecast**
  3. Set Forecast length = **3 months** (or 90 days)
  4. Ignore last = 0
  5. Seasonality = **Auto** (or set to 12 for monthly seasonality)
  6. Confidence interval = 95%
- A dashed line will extend 3 months into the future.

### Visual 2 — Revenue by Region (Bar/Column Chart)

- Axis: `region`
- Value: `Total Revenue`
- Data labels: On

### Visual 3 — Top 10 Products (Table or Bar)

- Drag `product_name` to Axis, `Total Revenue` to Value
- Filter Top N = 10 (in Filters pane)

### Visual 4 — Category Contribution (Donut Chart)

- Legend: `category`
- Values: `Total Revenue`
- Show legend: On

### Visual 5 — Segment Performance (Clustered Bar)

- Axis: `segment`
- Values: `Total Revenue`, `Total Profit`

### Slicers (right side panel)

- Region (slicer)
- Category (slicer)
- Order Year (slicer)
- Segment (slicer)

---

## 5. Page 2: Customer & Segment Analysis

- Card: Revenue Per Customer
- Bar chart: Top 10 Customers by revenue
- Pie: Segment share
- Line: Orders by segment over time
- Table: Customer Name, Segment, Total Spend, Orders

---

## 6. Page 3: Product Analysis

- Treemap: Category → Sub-Category (size = revenue)
- Bar: Top 10 products by revenue
- Bar: Bottom 10 loss-making products
- Scatter: Sales vs Profit (X = Sales, Y = Profit, Size = Quantity, Detail = Product)

---

## 7. Page 4: Forecasting & Trends

- Line chart: Monthly revenue with 3-month forecast (built-in Analytics pane)
- Line chart: Monthly profit trend
- Card: Predicted Next Quarter Revenue (use `Revenue Forecast (3 months)` measure)

---

## 8. Formatting Tips

- **Theme:** Use a dark theme (View → Themes → Dark) for portfolio screenshots.
- **Background:** Insert → Shape → Rectangle behind visuals → fill `#1F2A44`.
- **Font:** Segoe UI Bold for KPI values, Segoe UI Semibold for labels.
- **Title:** Add text box "Retail Sales Analytics Dashboard | 2015–2018" at the top.

---

## 9. Publish & Export

1. **Save** the .pbix file.
2. **File → Publish to Power BI Service** (free account works).
3. Take screenshots of all 4 pages → add to `docs/screenshots/` for your portfolio/LinkedIn post.

---

## 10. Troubleshooting

| Issue | Fix |
|-------|-----|
| Forecast option grayed out | Make sure the X-axis is a Date/Continuous field |
| Profit Margin shows weird % | Wrap in `FORMAT()` or set format to Percentage |
| Top N filter not working | Apply filter on visual-level filters, not page-level |
| Geo map not showing states | Use a Filled Map visual; ensure `state` column has full names |

---

**That's it. Your dashboard is ready.** Take screenshots, add to your resume and LinkedIn.