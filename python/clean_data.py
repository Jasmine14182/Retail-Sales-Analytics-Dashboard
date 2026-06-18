"""
Retail Sales Analytics - Data Cleaning Script
==============================================

Cleans the Superstore Sales Dataset:
- Fixes column naming (lowercase, snake_case)
- Parses dates to datetime
- Handles missing values
- Removes duplicates
- Creates derived columns (profit_margin, order_month, ship_days, etc.)
- Validates data types
- Outputs cleaned CSV for SQL + Power BI

Usage:
    python clean_data.py
"""

import pandas as pd
import numpy as np
import os
import sys


# ---------- Configuration ----------
RAW_PATH = "data/superstore.csv"
CLEAN_PATH = "data/superstore_clean.csv"
SUMMARY_PATH = "docs/cleaning_summary.txt"


def load_data(path: str) -> pd.DataFrame:
    """Load CSV and normalize column names."""
    if not os.path.exists(path):
        sys.exit(f"[ERROR] File not found: {path}\n"
                 f"Download the Superstore dataset from Kaggle and place it here.")

    # The raw file is sometimes encoded as cp1252
    df = pd.read_csv(path, encoding="cp1252")
    print(f"[INFO] Loaded {len(df):,} rows × {df.shape[1]} columns")
    return df


def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names to snake_case."""
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    return df


def parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Parse order_date and ship_date to datetime."""
    for col in ["order_date", "ship_date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


def handle_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Report and impute/drop missing values based on column rules."""
    print("\n[MISSING VALUES BEFORE]")
    print(df.isna().sum()[df.isna().sum() > 0])

    # Postal codes may have nulls — fill with placeholder
    if "postal_code" in df.columns:
        df["postal_code"] = df["postal_code"].fillna(0).astype(int)

    # Drop rows where critical fields are missing
    critical = ["order_date", "sales", "profit", "customer_name"]
    before = len(df)
    df = df.dropna(subset=[c for c in critical if c in df.columns])
    dropped = before - len(df)
    if dropped:
        print(f"[INFO] Dropped {dropped} rows with missing critical fields")

    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate rows."""
    before = len(df)
    df = df.drop_duplicates()
    print(f"[INFO] Removed {before - len(df)} duplicate rows")
    return df


def fix_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure numeric columns are correctly typed."""
    for col in ["sales", "profit", "discount", "quantity"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create derived columns useful for analysis and BI."""
    if "order_date" in df.columns:
        df["order_year"] = df["order_date"].dt.year
        df["order_month"] = df["order_date"].dt.month
        df["order_month_name"] = df["order_date"].dt.strftime("%b")
        df["order_quarter"] = df["order_date"].dt.quarter
        df["order_year_month"] = df["order_date"].dt.strftime("%Y-%m")

    if {"order_date", "ship_date"}.issubset(df.columns):
        df["ship_days"] = (df["ship_date"] - df["order_date"]).dt.days

    if {"profit", "sales"}.issubset(df.columns):
        df["profit_margin"] = np.where(
            df["sales"] != 0,
            (df["profit"] / df["sales"]) * 100,
            0
        ).round(2)

    # Bucket profit margin for easier analysis
    if "profit_margin" in df.columns:
        df["margin_band"] = pd.cut(
            df["profit_margin"],
            bins=[-100, 0, 10, 20, 30, 100],
            labels=["Loss", "Low (0-10%)", "Medium (10-20%)",
                    "Good (20-30%)", "High (>30%)"]
        )

    return df


def validate_data(df: pd.DataFrame) -> dict:
    """Run final checks and return summary stats."""
    summary = {
        "rows": len(df),
        "columns": df.shape[1],
        "date_range": (
            df["order_date"].min().strftime("%Y-%m-%d")
            + " to "
            + df["order_date"].max().strftime("%Y-%m-%d")
        ),
        "total_revenue": round(df["sales"].sum(), 2),
        "total_profit": round(df["profit"].sum(), 2),
        "profit_margin_pct": round(
            (df["profit"].sum() / df["sales"].sum()) * 100, 2
        ),
        "unique_customers": df["customer_name"].nunique(),
        "unique_products": df["product_name"].nunique(),
        "categories": df["category"].nunique(),
        "regions": df["region"].nunique(),
    }
    return summary


def write_summary(summary: dict, path: str) -> None:
    """Write a human-readable summary file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write("DATA CLEANING SUMMARY\n")
        f.write("=" * 50 + "\n\n")
        for k, v in summary.items():
            f.write(f"{k:>20}: {v}\n")
    print(f"[INFO] Summary written to {path}")


def main():
    print("=" * 60)
    print("Retail Sales Analytics - Data Cleaning")
    print("=" * 60)

    df = load_data(RAW_PATH)
    df = clean_columns(df)
    df = parse_dates(df)
    df = handle_missing(df)
    df = remove_duplicates(df)
    df = fix_data_types(df)
    df = engineer_features(df)

    summary = validate_data(df)

    print("\n" + "=" * 60)
    print("FINAL DATASET SUMMARY")
    print("=" * 60)
    for k, v in summary.items():
        print(f"  {k:>20}: {v}")

    # Save cleaned data
    df.to_csv(CLEAN_PATH, index=False)
    print(f"\n[SUCCESS] Cleaned data saved to {CLEAN_PATH}")
    print(f"[SUCCESS] Cleaned rows: {len(df):,}")

    write_summary(summary, SUMMARY_PATH)

    print("\n[NEXT STEPS]")
    print("  1. Load data/superstore_clean.csv into your SQL database")
    print("  2. Run sql/analysis_queries.sql")
    print("  3. Import data/superstore_clean.csv into Power BI")


if __name__ == "__main__":
    main()