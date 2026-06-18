# Retail Sales Analytics Dashboard

End-to-end data analytics project built with **SQL, Python, and Power BI** using the Superstore Sales Dataset (~10,000 records). Designed as a resume-ready project for fresher Data Analyst roles.

---

## Tech Stack

| Tool       | Purpose                                                  |
| ---------- | -------------------------------------------------------- |
| Python     | Data cleaning, EDA, feature engineering                   |
| Pandas     | Data wrangling                                           |
| Matplotlib | Quick visual checks during EDA                           |
| SQL        | Business analysis (revenue, profit, segments, trends)    |
| Power BI   | Interactive dashboard with KPIs and forecasting          |
| GitHub     | Version control & portfolio hosting                      |

---

## Dataset

- **Source:** [Superstore Sales Dataset on Kaggle](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final)
- **Rows:** ~9,994 transactions
- **Columns:** Order Date, Ship Date, Customer, Product, Category, Sub-Category, Sales, Profit, Quantity, Discount, Region, Segment

> Note: The dataset is not included in this repo due to Kaggle licensing. Download it and place it in `/data/superstore.csv` before running the scripts.

---

## Project Structure

```
retail-sales-analytics/
├── data/                      # Raw + cleaned dataset (created on first run)
├── python/
│   ├── generate_sample_data.py  # Sample Superstore-style data (10K rows)
│   ├── clean_data.py            # Data cleaning + feature engineering
│   └── eda.py                   # 8 EDA charts → docs/eda_charts/
├── sql/
│   ├── schema.sql               # CREATE TABLE + COPY load
│   └── analysis_queries.sql     # 17 business queries (CTEs, windows)
├── powerbi/
│   ├── dashboard_build_guide.md # Step-by-step build guide
│   ├── dax_measures.dax         # 15+ DAX measures (copy-paste)
│   └── retail_theme.json        # Custom Power BI theme
├── docs/
│   ├── insights.md              # Key business findings
│   ├── eda_findings.md          # Chart-by-chart interpretation
│   ├── resume_bullets.md        # Resume + LinkedIn + interview Q&A
│   └── eda_charts/              # Generated PNG visualizations
├── requirements.txt
├── .gitignore
└── README.md
```

---

## How to Run

### Option A — Use the bundled sample data (no download needed)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate 10K rows of Superstore-style sample data
python python/generate_sample_data.py

# 3. Clean + engineer features
python python/clean_data.py

# 4. Generate 8 EDA charts
python python/eda.py

# 5. Load into PostgreSQL
psql -U postgres -d retail -f sql/schema.sql
psql -U postgres -d retail -f sql/analysis_queries.sql

# 6. Open Power BI Desktop → import data/superstore_clean.csv
#    → View → Themes → Browse for theme → powerbi/retail_theme.json
#    → follow powerbi/dashboard_build_guide.md
```

### Option B — Use the real Kaggle dataset

1. Download from [Kaggle](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final)
2. Save to `data/superstore.csv` (skipping step 2 above)
3. Continue from step 3

---

## Key KPIs Tracked

- **Total Revenue** (Sales)
- **Total Profit**
- **Profit Margin %**
- **Total Orders**
- **Total Customers**
- **Average Order Value (AOV)**
- **Revenue by Region / Category / Segment**
- **Top 10 Products**
- **Monthly Trend (with 3-month forecast)**

---

## Dashboard Preview

The dashboard contains 4 pages:
1. **Executive Summary** — KPI cards + revenue/profit trend
2. **Customer & Segment Analysis** — Segment-level performance
3. **Product Analysis** — Top products, category contribution
4. **Forecasting** — 3-month forward-looking revenue prediction

---

## Resume Bullets

See `docs/resume_bullets.md` for copy-paste ready lines for your resume.

---

## License

Dataset © original Kaggle contributor. Code in this repo is MIT licensed.