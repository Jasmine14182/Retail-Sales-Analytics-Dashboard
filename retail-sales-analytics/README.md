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
├── data/                  # Raw + cleaned dataset
├── python/
│   └── clean_data.py      # Data cleaning script
├── sql/
│   └── analysis_queries.sql # 10+ business queries
├── powerbi/
│   └── dashboard_build_guide.md # Step-by-step Power BI build
├── docs/
│   ├── insights.md        # Findings + business insights
│   └── resume_bullets.md  # Ready-to-paste resume bullets
├── requirements.txt
└── README.md
```

---

## How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Download dataset from Kaggle and place in data/superstore.csv

# 3. Run cleaning script
python python/clean_data.py

# 4. Import cleaned data into PostgreSQL/MySQL/SQLite and run sql/analysis_queries.sql

# 5. Open Power BI Desktop, import data/superstore_clean.csv, follow powerbi/dashboard_build_guide.md
```

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