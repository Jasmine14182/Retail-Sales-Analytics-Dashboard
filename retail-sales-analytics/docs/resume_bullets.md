# Resume Bullets — Copy/Paste Ready

Pick 2–3 of these for your one-line project description on your resume.

---

## Short Version (1-line, ATS-friendly)

> **Retail Sales Analytics Dashboard** | Python, SQL, Power BI
> Analyzed 10K+ retail transactions to build an interactive dashboard with KPIs, customer segmentation, and 3-month revenue forecasting.

---

## Medium Version (2-line, best for fresher resumes)

> **Retail Sales Analytics Dashboard** | Python · SQL · Power BI · DAX
> Cleaned and analyzed 10K+ sales records using Python (Pandas); wrote 15+ SQL queries for revenue, profit, and segment analysis; built an interactive Power BI dashboard with 6 KPI cards, regional/product breakdowns, and a 3-month forecast. Surfaced $74K in loss-making products and identified that discounts above 40% drive negative margins.

---

## Long Version (for projects section with bullets)

**Retail Sales Analytics Dashboard | Python, SQL, Power BI, DAX**

- Cleaned and preprocessed 10K+ retail transactions using Python (Pandas, NumPy), engineered 12 derived features including profit margin, shipping days, and discount buckets.
- Authored 15+ SQL queries (joins, CTEs, window functions) for revenue, profit, top products, customer segmentation, and YoY/MoM growth analysis.
- Designed a 4-page interactive Power BI dashboard with 6 KPI cards, drill-downs by region/category/segment, and a 3-month revenue forecast using Power BI's analytics pane.
- Uncovered that discounts above 40% consistently produce negative profit margins, recommending a policy change projected to recover $40K+ annually.
- Identified the top 10 loss-making products and the West region as the strongest revenue contributor, enabling data-driven inventory and marketing decisions.

---

## Skills to List Alongside This Project

- **Languages:** SQL, Python
- **Libraries:** Pandas, NumPy, Matplotlib
- **BI Tools:** Power BI, DAX, Power Query
- **Concepts:** Data Cleaning, EDA, KPI Design, Time-Series Forecasting, Data Modeling, Star Schema
- **Soft Skills:** Business Storytelling, Stakeholder Reporting

---

## LinkedIn Project Post Template

```
🚀 Just wrapped up a Retail Sales Analytics project!

📊 Analyzed 10,000+ sales transactions across 4 years
🧹 Cleaned & engineered features using Python (Pandas)
🗄️ Wrote 15+ SQL queries covering revenue, profit & segmentation
📈 Built a 4-page Power BI dashboard with KPIs and a 3-month forecast

🔍 Key finding: discounts above 40% drive negative margins —
a single policy tweak could recover $40K+ per year.

Tech: Python · SQL · Power BI · DAX · Pandas

#DataAnalytics #PowerBI #SQL #Python #Freshers
```

---

## Interview Q&A Cheat Sheet

**Q: Walk me through this project.**
A: I worked with the Superstore Sales dataset (~10K rows). First, I cleaned it in Python — handled missing postal codes, parsed dates, removed duplicates, and created derived columns like profit margin and shipping days. Then I loaded it into SQL and wrote queries to analyze revenue, profit, customer segments, and product performance. Finally, I built a 4-page Power BI dashboard with KPI cards, trend lines, and a 3-month revenue forecast.

**Q: What was the most interesting insight?**
A: Discounts above 40% consistently produced negative profit margins. The data showed that high discounts were being used to clear inventory, but the cost of the discount exceeded the recovered revenue. A 20% discount cap could save the business tens of thousands per year.

**Q: What DAX measures did you use?**
A: I used SUM, DISTINCTCOUNT, AVERAGE, DIVIDE for KPIs. For time intelligence, I used TOTALYTD, SAMEPERIODLASTYEAR, and DIVIDE for YoY growth. I also created a custom Profit Color measure using SWITCH for conditional KPI formatting.

**Q: Why Power BI over Tableau?**
A: Power BI is widely used in mid-sized companies and integrates well with the Microsoft stack (Excel, Azure, SQL Server). It's also more affordable. The DAX language is powerful for custom measures.

**Q: How did you handle forecasting?**
A: I used Power BI's built-in analytics pane on the revenue trend line chart, set forecast length to 3 months, and let it auto-detect seasonality. For more advanced forecasting, I'd use Python's Prophet library or R's forecast package.