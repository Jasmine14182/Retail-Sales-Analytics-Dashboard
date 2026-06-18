"""
Exploratory Data Analysis (EDA) with visualizations.

Generates 8 charts in /docs/eda_charts/:
  01_revenue_by_month.png       - Monthly revenue trend
  02_revenue_by_region.png      - Region breakdown
  03_category_pie.png           - Category contribution
  04_top10_products.png         - Top 10 products
  05_discount_vs_profit.png     - Discount impact on profit
  06_segment_performance.png    - Segment performance
  07_profit_distribution.png    - Profit margin distribution
  08_correlation_heatmap.png    - Numeric correlation heatmap

Usage:
    python python/eda.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import os
import sys


# ---------- Config ----------
INPUT_PATH = "data/superstore_clean.csv"
OUT_DIR = "docs/eda_charts"
DPI = 150


def load_data(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        sys.exit(f"[ERROR] Run python/clean_data.py first.\nMissing: {path}")
    return pd.read_csv(path, parse_dates=["order_date", "ship_date"])


def setup_style():
    sns.set_theme(style="whitegrid", palette="muted")
    plt.rcParams.update({
        "figure.figsize": (12, 6),
        "axes.titlesize": 14,
        "axes.labelsize": 11,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 10,
        "figure.dpi": DPI,
    })


def chart_01_monthly_trend(df: pd.DataFrame):
    monthly = df.groupby("order_year_month").agg(
        revenue=("sales", "sum"),
        profit=("profit", "sum"),
    ).reset_index()

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(monthly["order_year_month"], monthly["revenue"],
            marker="o", linewidth=2, color="#2E86AB", label="Revenue")
    ax.plot(monthly["order_year_month"], monthly["profit"],
            marker="s", linewidth=2, color="#A23B72", label="Profit")

    # Show every 3rd x-tick to avoid crowding
    ax.set_xticks(monthly["order_year_month"][::3])
    ax.set_xticklabels(monthly["order_year_month"][::3], rotation=45)

    ax.set_title("Monthly Revenue & Profit Trend (2015–2018)")
    ax.set_xlabel("Month")
    ax.set_ylabel("USD")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/01_revenue_by_month.png")
    plt.close()


def chart_02_region(df: pd.DataFrame):
    region = df.groupby("region").agg(
        revenue=("sales", "sum"),
        profit=("profit", "sum"),
    ).reset_index().sort_values("revenue", ascending=False)

    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(region))
    width = 0.35
    ax.bar(x - width/2, region["revenue"], width, label="Revenue", color="#2E86AB")
    ax.bar(x + width/2, region["profit"],  width, label="Profit",  color="#A23B72")
    ax.set_xticks(x)
    ax.set_xticklabels(region["region"])
    ax.set_title("Revenue & Profit by Region")
    ax.set_ylabel("USD")
    ax.legend()
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/02_revenue_by_region.png")
    plt.close()


def chart_03_category_pie(df: pd.DataFrame):
    cat = df.groupby("category")["sales"].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(8, 8))
    colors = ["#2E86AB", "#A23B72", "#F18F01"]
    ax.pie(cat, labels=cat.index, autopct="%1.1f%%", colors=colors,
           startangle=90, wedgeprops={"edgecolor": "white", "linewidth": 2})
    ax.set_title("Revenue Share by Category")
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/03_category_pie.png")
    plt.close()


def chart_04_top_products(df: pd.DataFrame):
    top = df.groupby("product_name")["sales"].sum().nlargest(10).sort_values()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top.index, top.values, color="#2E86AB")
    ax.set_title("Top 10 Products by Revenue")
    ax.set_xlabel("Revenue (USD)")
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/04_top10_products.png")
    plt.close()


def chart_05_discount_vs_profit(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(10, 6))
    # Aggregate profit margin by discount bucket
    bucket = df.groupby("margin_band").agg(
        profit=("profit", "mean"),
        sales=("sales", "mean"),
    ).reset_index()

    order = ["Loss", "Low (0-10%)", "Medium (10-20%)", "Good (20-30%)", "High (>30%)"]
    bucket["margin_band"] = pd.Categorical(bucket["margin_band"], categories=order, ordered=True)
    bucket = bucket.sort_values("margin_band")

    colors = ["#D62828", "#F77F00", "#FCBF49", "#06A77D", "#2E86AB"]
    ax.bar(bucket["margin_band"].astype(str), bucket["profit"], color=colors)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_title("Average Profit by Profit-Margin Bucket")
    ax.set_ylabel("Avg Profit (USD)")
    ax.set_xlabel("Profit Margin Bucket")
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/05_discount_vs_profit.png")
    plt.close()


def chart_06_segment(df: pd.DataFrame):
    seg = df.groupby("segment").agg(
        revenue=("sales", "sum"),
        profit=("profit", "sum"),
        orders=("row_id", "count"),
    ).reset_index().sort_values("revenue", ascending=False)

    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(seg))
    ax.bar(x, seg["revenue"], color="#2E86AB", label="Revenue")
    ax.bar(x, seg["profit"],  color="#A23B72", label="Profit", alpha=0.7)
    for i, (rev, prof) in enumerate(zip(seg["revenue"], seg["profit"])):
        ax.text(i, rev + 5000, f"${rev/1000:.0f}K", ha="center", fontsize=9)
    ax.set_xticks(x)
    ax.set_xticklabels(seg["segment"])
    ax.set_title("Performance by Customer Segment")
    ax.set_ylabel("USD")
    ax.legend()
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/06_segment_performance.png")
    plt.close()


def chart_07_profit_dist(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(df["profit_margin"], bins=50, color="#2E86AB", edgecolor="white")
    ax.axvline(0, color="red", linestyle="--", label="Break-even")
    ax.set_title("Profit Margin Distribution")
    ax.set_xlabel("Profit Margin (%)")
    ax.set_ylabel("Frequency")
    ax.legend()
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/07_profit_distribution.png")
    plt.close()


def chart_08_correlation(df: pd.DataFrame):
    cols = ["sales", "profit", "discount", "quantity", "ship_days", "profit_margin"]
    corr = df[cols].corr()

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap="RdBu_r", center=0, fmt=".2f",
                square=True, ax=ax, cbar_kws={"shrink": 0.8})
    ax.set_title("Correlation Heatmap (Numeric Features)")
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/08_correlation_heatmap.png")
    plt.close()


def main():
    print("=" * 60)
    print("Retail Sales Analytics - EDA")
    print("=" * 60)

    df = load_data(INPUT_PATH)
    setup_style()
    os.makedirs(OUT_DIR, exist_ok=True)

    print(f"[INFO] Loaded {len(df):,} rows")

    charts = [
        ("Monthly trend",        chart_01_monthly_trend),
        ("Region breakdown",     chart_02_region),
        ("Category pie",         chart_03_category_pie),
        ("Top 10 products",      chart_04_top_products),
        ("Discount vs profit",   chart_05_discount_vs_profit),
        ("Segment performance",  chart_06_segment),
        ("Profit distribution",  chart_07_profit_dist),
        ("Correlation heatmap",  chart_08_correlation),
    ]

    for name, fn in charts:
        print(f"[PLOT] {name}...")
        fn(df)

    print(f"\n[SUCCESS] {len(charts)} charts saved to {OUT_DIR}/")
    print("Open the PNGs and reference them in your Power BI dashboard.")


if __name__ == "__main__":
    main()