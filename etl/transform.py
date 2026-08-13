import pandas as pd
import os


if __name__ == "__main__":

    # ==========================================
    # READ RAW DATA
    # ==========================================

    customers = pd.read_csv(
        "data/raw/customers.csv"
    )

    products = pd.read_csv(
        "data/raw/products.csv"
    )

    orders = pd.read_csv(
        "data/raw/orders.csv"
    )

    order_items = pd.read_csv(
        "data/raw/order_items.csv"
    )

    # ==========================================
    # DATA VALIDATION
    # ==========================================

    print("=" * 50)
    print("DATA VALIDATION")
    print("=" * 50)

    print("\n--- Missing Values ---")

    print(
        "Customers:",
        customers.isnull().sum().sum()
    )

    print(
        "Products:",
        products.isnull().sum().sum()
    )

    print(
        "Orders:",
        orders.isnull().sum().sum()
    )

    print(
        "Order Items:",
        order_items.isnull().sum().sum()
    )

    print("\n--- Duplicate Records ---")

    print(
        "Customers:",
        customers.duplicated().sum()
    )

    print(
        "Products:",
        products.duplicated().sum()
    )

    print(
        "Orders:",
        orders.duplicated().sum()
    )

    print(
        "Order Items:",
        order_items.duplicated().sum()
    )

    print("\n--- Quantity Validation ---")

    invalid_quantity = order_items[
        order_items["quantity"] <= 0
    ]

    print(
        "Invalid Quantity Records:",
        len(invalid_quantity)
    )

    print("\n--- Product Price Validation ---")

    invalid_product_price = products[
        products["unit_price"] <= 0
    ]

    print(
        "Invalid Product Prices:",
        len(invalid_product_price)
    )

    print("\n--- Order Item Price Validation ---")

    invalid_item_price = order_items[
        order_items["unit_price"] <= 0
    ]

    print(
        "Invalid Order Item Prices:",
        len(invalid_item_price)
    )

    print("\n" + "=" * 50)
    print("VALIDATION COMPLETED")
    print("=" * 50)

    # ==========================================
    # DATA TRANSFORMATION
    # ==========================================

    print("\n" + "=" * 50)
    print("DATA TRANSFORMATION")
    print("=" * 50)

    # Remove duplicates
    customers = customers.drop_duplicates()
    products = products.drop_duplicates()
    orders = orders.drop_duplicates()
    order_items = order_items.drop_duplicates()

    # ------------------------------------------
    # Customer text cleaning
    # ------------------------------------------

    customers["customer_name"] = (
        customers["customer_name"]
        .str.strip()
        .str.title()
    )

    customers["city"] = (
        customers["city"]
        .str.strip()
        .str.title()
    )

    # ------------------------------------------
    # Product cleaning
    # ------------------------------------------

    products["product_name"] = (
        products["product_name"]
        .str.strip()
    )

    # category_id and supplier_id are already
    # database-compatible IDs.
    products["category_id"] = pd.to_numeric(
        products["category_id"],
        errors="coerce"
    )

    products["supplier_id"] = pd.to_numeric(
        products["supplier_id"],
        errors="coerce"
    )

    products["unit_price"] = pd.to_numeric(
        products["unit_price"],
        errors="coerce"
    )

    # ------------------------------------------
    # Order cleaning
    # ------------------------------------------

    orders["order_date"] = pd.to_datetime(
        orders["order_date"],
        errors="coerce"
    )

    orders["customer_id"] = pd.to_numeric(
        orders["customer_id"],
        errors="coerce"
    )

    # ------------------------------------------
    # Order Item cleaning
    # ------------------------------------------

    order_items["order_id"] = pd.to_numeric(
        order_items["order_id"],
        errors="coerce"
    )

    order_items["product_id"] = pd.to_numeric(
        order_items["product_id"],
        errors="coerce"
    )

    order_items["quantity"] = pd.to_numeric(
        order_items["quantity"],
        errors="coerce"
    )

    order_items["unit_price"] = pd.to_numeric(
        order_items["unit_price"],
        errors="coerce"
    )

    # Recalculate total amount
    order_items["total_amount"] = (
        order_items["quantity"]
        * order_items["unit_price"]
    ).round(2)

    print("✅ Transformation completed")

    # ==========================================
    # CREATE CLEANED DIRECTORY
    # ==========================================

    os.makedirs(
        "data/cleaned",
        exist_ok=True
    )

    # ==========================================
    # SAVE CLEAN DATA
    # ==========================================

    customers.to_csv(
        "data/cleaned/customers_clean.csv",
        index=False
    )

    products.to_csv(
        "data/cleaned/products_clean.csv",
        index=False
    )

    orders.to_csv(
        "data/cleaned/orders_clean.csv",
        index=False
    )

    order_items.to_csv(
        "data/cleaned/order_items_clean.csv",
        index=False
    )

    print(
        "✅ Cleaned datasets saved successfully"
    )

    print("\n" + "=" * 50)
    print("FINAL CLEAN DATASET")
    print("=" * 50)

    print(
        "Customers   :",
        len(customers)
    )

    print(
        "Products    :",
        len(products)
    )

    print(
        "Orders      :",
        len(orders)
    )

    print(
        "Order Items :",
        len(order_items)
    )