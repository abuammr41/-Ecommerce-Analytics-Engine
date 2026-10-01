import argparse
import os
import sys
import time

from analyzer import customer_behavior, product_performance, sales_trends
from cleaner import clean_data
from connector import load_data
from exporter import export_report


def run_pipeline(file_path, output_name=None):
    start = time.time()
    df_raw = load_data(file_path)
    df_clean, report = clean_data(df_raw)

    daily, monthly = sales_trends(df_clean)
    customers, customer_summary = customer_behavior(df_clean)
    products, categories = product_performance(df_clean)

    if output_name is None:
        output_name = f"Analytics_{os.path.splitext(os.path.basename(file_path))[0]}.xlsx"
    output_path = export_report(
        daily, monthly, customers, customer_summary, products, categories, report, output_name
    )
    report["seconds"] = round(time.time() - start, 2)
    report["output"] = output_path
    return df_clean, report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ecommerce data analytics & reporting engine")
    parser.add_argument("input_file", nargs="?", default="orders_sample.csv", help="CSV / XLSX / JSON order export")
    parser.add_argument("-o", "--output", default=None, help="Output Excel file name (saved in output/)")
    args = parser.parse_args()

    try:
        _, rep = run_pipeline(args.input_file, args.output)
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)

    print("==================================================")
    print("   ECOMMERCE ANALYTICS PIPELINE COMPLETED")
    print("==================================================")
    print(f"Orders received        : {rep['rows_in']}")
    print(f"Removed (missing data) : {rep['missing_required_removed']}")
    print(f"Removed (bad dates)    : {rep['invalid_dates_removed']}")
    print(f"Removed (bad totals)   : {rep['invalid_totals_removed']}")
    print(f"Duplicate orders found : {rep['duplicate_orders_removed']}")
    print(f"Clean orders analyzed  : {rep['rows_out']}")
    print(f"Outliers flagged       : {rep['outliers_flagged']}")
    print(f"Time                   : {rep['seconds']} seconds")
    print(f"Report saved at        : {rep['output']}")
