import pandas as pd

import config


def clean_data(df):
    """Return (clean_df, report dict). Handles missing values, bad dates/totals,
    duplicate orders, and flags statistical outliers on order total."""
    report = {"rows_in": len(df)}
    df = df.copy()

    required = [c for c in ("date", "total") if c in df.columns]
    before = len(df)
    df = df.dropna(subset=required)
    report["missing_required_removed"] = before - len(df)

    df["date"] = pd.to_datetime(df["date"], dayfirst=config.DATE_DAYFIRST, errors="coerce")
    before = len(df)
    df = df.dropna(subset=["date"])
    report["invalid_dates_removed"] = before - len(df)

    df["total"] = pd.to_numeric(
        df["total"].astype(str).str.replace(r"[^\d.\-]", "", regex=True), errors="coerce"
    )
    before = len(df)
    df = df.dropna(subset=["total"])
    report["invalid_totals_removed"] = before - len(df)

    if "quantity" in df.columns:
        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(1)
    if "product" in df.columns:
        df["product"] = df["product"].fillna("Unknown Product").astype(str).str.strip()
    if "category" in df.columns:
        df["category"] = df["category"].fillna("Uncategorized").astype(str).str.strip()
    if "customer" in df.columns:
        df["customer"] = df["customer"].fillna("Guest").astype(str).str.strip().str.lower()

    if "order_id" in df.columns:
        before = len(df)
        df = df.drop_duplicates(subset=["order_id"], keep="first")
        report["duplicate_orders_removed"] = before - len(df)
    else:
        report["duplicate_orders_removed"] = 0

    df = flag_outliers(df)
    report["outliers_flagged"] = int(df["is_outlier"].sum())
    report["rows_out"] = len(df)
    return df.reset_index(drop=True), report


def flag_outliers(df):
    values = df["total"]
    if config.OUTLIER_METHOD == "zscore":
        std = values.std(ddof=0) or 1
        z = (values - values.mean()) / std
        mask = z.abs() > config.ZSCORE_THRESHOLD
    else:
        q1, q3 = values.quantile(0.25), values.quantile(0.75)
        iqr = q3 - q1
        lower, upper = q1 - config.IQR_MULTIPLIER * iqr, q3 + config.IQR_MULTIPLIER * iqr
        mask = (values < lower) | (values > upper)
    df = df.copy()
    df["is_outlier"] = mask.values
    return df
