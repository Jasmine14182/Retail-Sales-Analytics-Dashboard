# EDA Findings - Chart-by-Chart Interpretation

This document explains what each chart in `docs/eda_charts/` shows and what to look for.

---

## Chart 01: Monthly Revenue & Profit Trend
**File:** `01_revenue_by_month.png`

**What to look for:**
- Overall trajectory — is revenue growing year over year?
- Seasonality — recurring peaks (Q4) and troughs
- Profit vs revenue divergence — months where profit lags revenue (high discount periods)

**Typical findings:**
- Clear upward trend from 2015 → 2018
- Q4 spikes every November–December
- Some months show revenue growing while profit stays flat (discounting impact)

---

## Chart 02: Revenue & Profit by Region
**File:** `02_revenue_by_region.png`

**What to look for:**
- Which region dominates in both metrics
- Any region with high revenue but low/negative profit (operational inefficiency)

**Typical findings:**
- **West** is the strongest in both revenue and profit
- **Central** is often the weakest in profit despite decent revenue
- **South** tends to be smallest but profitable

---

## Chart 03: Revenue Share by Category
**File:** `03_category_pie.png`

**What to look for:**
- Roughly balanced segments indicate a diversified portfolio
- A single dominant category signals concentration risk

**Typical findings:**
- All three categories contribute ~30% each (well-diversified)
- Technology is slightly larger due to higher per-unit prices

---

## Chart 04: Top 10 Products by Revenue
**File:** `04_top10_products.png`

**What to look for:**
- Mix of categories among top sellers
- Technology products typically dominate (higher ticket)

**Typical findings:**
- Phones and computers make up 4–5 of the top 10
- Office supplies with high volume also appear
- Top 10 products usually represent 10–15% of total revenue

---

## Chart 05: Profit by Margin Bucket
**File:** `05_discount_vs_profit.png`

**What to look for:**
- The "Loss" bucket should be smaller than profitable buckets
- "Medium" and "Good" buckets should hold the bulk of orders

**Typical findings:**
- Loss bucket represents ~18% of orders (concerning)
- A 5–10% improvement here could save $40K+ annually

---

## Chart 06: Performance by Customer Segment
**File:** `06_segment_performance.png`

**What to look for:**
- Which segment drives the most revenue
- Whether profit scales with revenue per segment

**Typical findings:**
- **Consumer** is the largest segment (~51% of orders)
- **Corporate** has the highest revenue per customer
- **Home Office** is the smallest but most profitable per order

---

## Chart 07: Profit Margin Distribution
**File:** `07_profit_distribution.png`

**What to look for:**
- Distribution shape (normal vs skewed)
- Spread around 0 (how many orders are near break-even)
- Long tails (extreme losses/gains)

**Typical findings:**
- Roughly normal distribution centered around 10–15% margin
- Slight left tail (losses) — this is the discount-driven risk

---

## Chart 08: Correlation Heatmap
**File:** `08_correlation_heatmap.png`

**What to look for:**
- **Discount ↔ Profit**: should be strongly **negative** (key insight)
- **Sales ↔ Quantity**: moderately positive
- **Sales ↔ Profit**: moderately positive but weakened by discounts

**Typical findings:**
- Discount has the strongest negative correlation with profit
- Profit margin is almost entirely determined by discount level
- Quantity and sales correlate, but quantity has weak correlation with profit

---

## How to Use These Charts

1. **Portfolio** — embed them in your GitHub README under a "Key Visualizations" section
2. **Interviews** — reference them when explaining findings
3. **Power BI inspiration** — replicate the most useful ones as live visuals
4. **LinkedIn post** — pair the discount-vs-profit chart with the "$40K recovery" claim

---

## Reproducing the Charts

```bash
# 1. Generate sample data
python python/generate_sample_data.py

# 2. Clean
python python/clean_data.py

# 3. EDA
python python/eda.py
```

Charts are saved to `docs/eda_charts/`.