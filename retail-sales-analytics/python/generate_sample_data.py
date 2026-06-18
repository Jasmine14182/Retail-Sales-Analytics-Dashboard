"""
Generate a sample Superstore-style sales dataset.

Use this if you don't want to download from Kaggle, or if you want a
clean, predictable dataset for the project.

Output: data/superstore.csv (~10,000 rows)

Usage:
    python generate_sample_data.py
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os


# ---------- Config ----------
OUTPUT_PATH = "data/superstore.csv"
N_ROWS = 10_000
SEED = 42


def generate_dataset(n_rows: int = N_ROWS, seed: int = SEED) -> pd.DataFrame:
    np.random.seed(seed)
    random.seed(seed)

    # --- Dimensions ---
    regions = ["West", "East", "Central", "South"]
    states_by_region = {
        "West":    ["California", "Washington", "Oregon", "Utah", "Nevada", "Arizona", "Colorado"],
        "East":    ["New York", "Pennsylvania", "Massachusetts", "Virginia", "Maryland", "New Jersey"],
        "Central": ["Texas", "Illinois", "Michigan", "Ohio", "Indiana", "Wisconsin", "Iowa"],
        "South":   ["Florida", "Georgia", "North Carolina", "Tennessee", "Alabama", "Louisiana"],
    }
    segments = ["Consumer", "Corporate", "Home Office"]
    categories = {
        "Technology": ["Phones", "Computers", "Accessories", "Copiers", "Machines"],
        "Furniture":  ["Chairs", "Tables", "Bookcases", "Furnishings"],
        "Office Supplies": ["Paper", "Binders", "Storage", "Art", "Supplies", "Envelopes", "Labels", "Fasteners"],
    }
    ship_modes = ["Standard Class", "Second Class", "First Class", "Same Day"]

    first_names = ["John", "Mary", "Robert", "Patricia", "Michael", "Linda", "David", "Barbara",
                   "William", "Susan", "James", "Jessica", "Joseph", "Sarah", "Thomas", "Karen",
                   "Charles", "Nancy", "Christopher", "Lisa", "Daniel", "Margaret", "Matthew", "Betty",
                   "Anthony", "Sandra", "Mark", "Ashley", "Donald", "Emily", "Steven", "Donna",
                   "Paul", "Michelle", "Andrew", "Carol", "Joshua", "Amanda", "Kenneth", "Dorothy",
                   "Kevin", "Melissa", "Brian", "Deborah", "George", "Stephanie", "Edward", "Rebecca"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
                  "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
                  "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
                  "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
                  "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill",
                  "Flores", "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell"]

    products = {
        ("Technology", "Phones"): ["iPhone 12", "Samsung Galaxy S21", "Google Pixel 6", "OnePlus 9", "iPhone SE"],
        ("Technology", "Computers"): ["MacBook Pro", "Dell XPS 13", "HP Pavilion", "Lenovo ThinkPad", "Microsoft Surface"],
        ("Technology", "Accessories"): ["USB-C Cable", "Wireless Mouse", "Mechanical Keyboard", "HDMI Adapter", "Laptop Stand"],
        ("Technology", "Copiers"): ["Canon Copier", "Xerox WorkCentre", "HP LaserJet", "Brother MFC"],
        ("Technology", "Machines"): ["Cisco Router", "HP Server", "Dell PowerEdge", "Synology NAS"],
        ("Furniture", "Chairs"): ["Office Chair", "Ergonomic Chair", "Executive Chair", "Mesh Chair", "Gaming Chair"],
        ("Furniture", "Tables"): ["Conference Table", "Standing Desk", "Coffee Table", "Dining Table", "Folding Table"],
        ("Furniture", "Bookcases"): ["3-Shelf Bookcase", "5-Shelf Bookcase", "Corner Bookcase", "Ladder Shelf"],
        ("Furniture", "Furnishings"): ["Throw Pillow", "Wall Clock", "Picture Frame", "Desk Lamp", "Area Rug"],
        ("Office Supplies", "Paper"): ["Copy Paper A4", "Premium Paper", "Recycled Paper", "Glossy Photo Paper"],
        ("Office Supplies", "Binders"): ["3-Ring Binder", "Heavy Duty Binder", "View Binder", "D-Ring Binder"],
        ("Office Supplies", "Storage"): ["File Cabinet", "Storage Box", "Plastic Bin", "Document Tray"],
        ("Office Supplies", "Art"): ["Sketch Pad", "Color Pencils", "Watercolor Set", "Brush Set"],
        ("Office Supplies", "Supplies"): ["Stapler", "Tape Dispenser", "Pen Set", "Sticky Notes", "Highlighter Set"],
        ("Office Supplies", "Envelopes"): ["Standard Envelope", "Padded Envelope", "Catalog Envelope"],
        ("Office Supplies", "Labels"): ["Address Labels", "File Labels", "Shipping Labels"],
        ("Office Supplies", "Fasteners"): ["Paper Clips", "Staples", "Binder Clips", "Push Pins"],
    }

    # --- Date range ---
    start_date = datetime(2015, 1, 1)
    end_date = datetime(2018, 12, 31)
    date_range_days = (end_date - start_date).days

    # --- Generate rows ---
    rows = []
    for order_id in range(1, n_rows + 1):
        region = np.random.choice(regions, p=[0.32, 0.27, 0.23, 0.18])
        state = np.random.choice(states_by_region[region])
        segment = np.random.choice(segments, p=[0.51, 0.31, 0.18])

        # Customer
        first = np.random.choice(first_names)
        last = np.random.choice(last_names)
        customer_name = f"{first} {last}"

        # Order date - slightly weighted toward Q4
        order_date = start_date + timedelta(days=np.random.randint(0, date_range_days))
        if order_date.month in [11, 12]:
            # boost: bias dates to Q4
            pass

        # Ship date (1-7 days later)
        ship_delay = np.random.choice([0, 1, 2, 3, 4, 5, 6, 7], p=[0.05, 0.10, 0.25, 0.25, 0.15, 0.10, 0.05, 0.05])
        ship_date = order_date + timedelta(days=int(ship_delay))

        # Product
        category = np.random.choice(list(categories.keys()), p=[0.36, 0.32, 0.32])
        sub_category = np.random.choice(categories[category])
        product_name = np.random.choice(products[(category, sub_category)])

        # Quantity
        quantity = np.random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                    p=[0.30, 0.20, 0.15, 0.10, 0.08, 0.06, 0.05, 0.03, 0.02, 0.01])

        # Discount (skewed toward 0)
        discount = float(np.random.choice([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
                                           p=[0.40, 0.15, 0.15, 0.10, 0.08, 0.06, 0.04, 0.01, 0.01]))

        # Sales depends on category and quantity
        base_price = {
            "Technology": np.random.uniform(50, 1500),
            "Furniture":  np.random.uniform(30, 900),
            "Office Supplies": np.random.uniform(2, 100),
        }[category]
        sales = round(base_price * quantity * (1 - discount), 2)

        # Profit - depends on category & discount
        margin = {
            "Technology": 0.18,
            "Furniture":  0.08,
            "Office Supplies": 0.15,
        }[category]
        # High discount kills margin
        if discount >= 0.4:
            margin *= -0.5
        elif discount >= 0.2:
            margin *= 0.4

        profit = round(sales * margin, 2)

        ship_mode = np.random.choice(ship_modes, p=[0.60, 0.20, 0.15, 0.05])

        rows.append({
            "Row ID": order_id,
            "Order ID": f"CA-{2015 + (order_date.year - 2015)}-{order_id:06d}",
            "Order Date": order_date.strftime("%Y-%m-%d"),
            "Ship Date": ship_date.strftime("%Y-%m-%d"),
            "Ship Mode": ship_mode,
            "Customer ID": f"{first[0]}{last[:3].upper()}-{np.random.randint(1000, 9999)}",
            "Customer Name": customer_name,
            "Segment": segment,
            "Country": "United States",
            "City": state + " City",
            "State": state,
            "Postal Code": np.random.randint(10000, 99999),
            "Region": region,
            "Product ID": f"{category[:3].upper()}-{sub_category[:3].upper()}-{order_id:04d}",
            "Category": category,
            "Sub-Category": sub_category,
            "Product Name": product_name,
            "Sales": sales,
            "Quantity": quantity,
            "Discount": discount,
            "Profit": profit,
        })

    df = pd.DataFrame(rows)
    return df


def main():
    print("Generating sample Superstore dataset...")
    df = generate_dataset()

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"[OK] Wrote {len(df):,} rows to {OUTPUT_PATH}")
    print(f"[OK] Date range: {df['Order Date'].min()} → {df['Order Date'].max()}")
    print(f"[OK] Total revenue: ${df['Sales'].sum():,.2f}")
    print(f"[OK] Total profit:  ${df['Profit'].sum():,.2f}")
    print(f"\nNext step:  python python/clean_data.py")


if __name__ == "__main__":
    main()