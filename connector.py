import os
import re

import pandas as pd

import config


def _key(header):
    return re.sub(r"[^a-z0-9]", "", str(header).lower())


def _match(header, keys):
    t = _key(header)
    return any(k in t for k in keys)


def detect_columns(df):
    """Map real-world headers (any export format) -> standard field names."""
    mapping = {}
    checks = [
        ("order_id", config.ORDER_ID_KEYS),
        ("date", config.DATE_KEYS),
        ("customer", config.CUSTOMER_KEYS),
        ("product", config.PRODUCT_KEYS),
        ("category", config.CATEGORY_KEYS),
        ("quantity", config.QUANTITY_KEYS),
        ("total", config.TOTAL_KEYS),
        ("unit_price", config.PRICE_KEYS),
    ]
    used = set()
    for col in df.columns:
        for field, keys in checks:
            if field in used:
                continue
            if _match(col, keys):
                mapping[col] = field
                used.add(field)
                break
    return mapping


def load_data(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext in (".xlsx", ".xls"):
        df = pd.read_excel(file_path)
    elif ext == ".json":
        df = pd.read_json(file_path)
    else:
        df = pd.read_csv(file_path)

    mapping = detect_columns(df)
    missing = [f for f in ("date", "total") if f not in mapping.values()]
    if missing:
        raise ValueError(
            f"Required column(s) not found: {missing}. "
            f"Detected headers in file: {list(df.columns)}"
        )
    return df.rename(columns=mapping)
