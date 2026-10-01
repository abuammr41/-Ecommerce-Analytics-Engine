"""
Ecommerce Analytics Engine — settings. Client ki zaroorat ke hisaab se yahan badlo.
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------- Dates ----------
DATE_DAYFIRST = False   # True for PK/UK-style exports (05/09/2026 = 5 Sep), False for US clients

# ---------- Column detection (header ke alfaaz se, flexible hai) ----------
ORDER_ID_KEYS = ["orderid", "order", "invoiceno", "invoice", "ordernumber", "ordername"]
DATE_KEYS = ["orderdate", "date", "createdat", "purchasedate", "transactiondate"]
CUSTOMER_KEYS = ["customeremail", "email", "customer", "customername", "buyer", "billingname"]
PRODUCT_KEYS = ["product", "item", "productname", "sku", "title", "lineitem"]
CATEGORY_KEYS = ["category", "producttype", "collection", "department"]
QUANTITY_KEYS = ["quantity", "qty", "units", "linequantity"]
PRICE_KEYS = ["unitprice", "price", "rate"]
TOTAL_KEYS = ["total", "ordertotal", "amount", "revenue", "linetotal", "grandtotal", "subtotal"]

# ---------- Cleaning ----------
OUTLIER_METHOD = "iqr"       # "iqr" or "zscore"
IQR_MULTIPLIER = 1.5
ZSCORE_THRESHOLD = 3

# ---------- Reports ----------
TOP_N_CUSTOMERS = 10
TOP_N_PRODUCTS = 10
