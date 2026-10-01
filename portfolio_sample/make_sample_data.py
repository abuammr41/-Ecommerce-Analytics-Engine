"""Generates a fake 'Apoc Store'-style order export for portfolio/demo purposes. Not real client data."""
import random
from datetime import datetime, timedelta

import pandas as pd

random.seed(7)

products = [
    ("Wireless Earbuds", "Electronics", 24.99),
    ("Phone Case", "Electronics", 9.99),
    ("Yoga Mat", "Fitness", 19.99),
    ("Resistance Bands", "Fitness", 14.99),
    ("Ceramic Mug", "Home", 8.99),
    ("Throw Blanket", "Home", 29.99),
    ("Desk Lamp", "Home", 22.5),
    ("Running Shoes", "Fitness", 49.99),
    ("Bluetooth Speaker", "Electronics", 34.99),
    ("Scented Candle", "Home", 11.99),
]
customers = [f"customer{i}@example.com" for i in range(1, 36)]

rows = []
start = datetime(2026, 7, 1)
order_id = 1000
for day in range(90):
    date = start + timedelta(days=day)
    n_orders = random.randint(2, 9)
    for _ in range(n_orders):
        name, category, price = random.choice(products)
        qty = random.choice([1, 1, 1, 2, 2, 3])
        total = round(price * qty, 2)
        rows.append({
            "Order ID": f"#{order_id}",
            "Order Date": date.strftime("%Y-%m-%d"),
            "Customer Email": random.choice(customers),
            "Product": name,
            "Category": category,
            "Quantity": qty,
            "Unit Price": price,
            "Order Total": total,
        })
        order_id += 1

# a few data-quality issues on purpose, so the report demonstrates the cleaning step
rows.append(dict(rows[5]))                       # exact duplicate order
rows[10]["Order Total"] = ""                      # missing total
rows[20]["Order Date"] = ""                       # missing date
rows.append({                                      # genuine outlier (bulk/wholesale order)
    "Order ID": "#9999", "Order Date": "2026-08-15", "Customer Email": "customer5@example.com",
    "Product": "Bluetooth Speaker", "Category": "Electronics", "Quantity": 40,
    "Unit Price": 34.99, "Order Total": 1399.60,
})

df = pd.DataFrame(rows)
df.to_csv("portfolio_sample/Orders_Sample.csv", index=False)
print(f"Sample written: {len(df)} rows")
