import pandas as pd

import config


def sales_trends(df):
    daily = (
        df.groupby(df["date"].dt.date)
        .agg(Orders=("total", "count"), Revenue=("total", "sum"))
        .reset_index()
        .rename(columns={"date": "Date"})
    )
    daily["Revenue"] = daily["Revenue"].round(2)

    monthly = (
        df.groupby(df["date"].dt.to_period("M"))
        .agg(Orders=("total", "count"), Revenue=("total", "sum"))
        .reset_index()
    )
    monthly["date"] = monthly["date"].astype(str)
    monthly = monthly.rename(columns={"date": "Month"})
    monthly["Revenue"] = monthly["Revenue"].round(2)
    return daily, monthly


def customer_behavior(df):
    if "customer" not in df.columns:
        return pd.DataFrame(), {}

    snapshot = df["date"].max()
    agg = (
        df.groupby("customer")
        .agg(Orders=("total", "count"), Total_Spent=("total", "sum"), Last_Order=("date", "max"))
        .reset_index()
        .rename(columns={"customer": "Customer"})
    )
    agg["Avg_Order_Value"] = (agg["Total_Spent"] / agg["Orders"]).round(2)
    agg["Days_Since_Last_Order"] = (snapshot - agg["Last_Order"]).dt.days
    agg["Total_Spent"] = agg["Total_Spent"].round(2)
    agg = agg.sort_values("Total_Spent", ascending=False)

    summary = {
        "total_customers": len(agg),
        "repeat_customers": int((agg["Orders"] > 1).sum()),
        "one_time_customers": int((agg["Orders"] == 1).sum()),
        "avg_order_value_overall": round(df["total"].mean(), 2),
    }
    return agg.head(config.TOP_N_CUSTOMERS).reset_index(drop=True), summary


def product_performance(df):
    if "product" not in df.columns:
        return pd.DataFrame(), pd.DataFrame()

    agg_kwargs = {"Revenue": ("total", "sum"), "Orders": ("total", "count")}
    if "quantity" in df.columns:
        agg_kwargs["Units_Sold"] = ("quantity", "sum")

    by_product = (
        df.groupby("product").agg(**agg_kwargs).reset_index().rename(columns={"product": "Product"})
    )
    by_product["Revenue"] = by_product["Revenue"].round(2)
    by_product = by_product.sort_values("Revenue", ascending=False)

    by_category = pd.DataFrame()
    if "category" in df.columns:
        by_category = (
            df.groupby("category")
            .agg(Revenue=("total", "sum"), Orders=("total", "count"))
            .reset_index()
            .rename(columns={"category": "Category"})
            .sort_values("Revenue", ascending=False)
        )
        by_category["Revenue"] = by_category["Revenue"].round(2)

    return (
        by_product.head(config.TOP_N_PRODUCTS).reset_index(drop=True),
        by_category.reset_index(drop=True),
    )
