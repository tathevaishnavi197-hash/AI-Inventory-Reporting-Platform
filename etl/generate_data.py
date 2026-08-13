import pandas as pd
import random
from datetime import datetime, timedelta

# ==========================================
# SETTINGS
# ==========================================

NUM_CUSTOMERS = 1000
NUM_PRODUCTS = 500
NUM_ORDERS = 5000

random.seed(42)

# Existing PostgreSQL master-data IDs
CATEGORY_IDS = [1, 2, 3, 4, 5]
SUPPLIER_IDS = [1, 2, 3, 4, 5]

# ==========================================
# MASTER DATA
# ==========================================

first_names = [
    "Aarav", "Vivaan", "Aditya", "Arjun", "Rohan",
    "Rahul", "Amit", "Karan", "Ankit", "Raj",
    "Priya", "Sneha", "Pooja", "Neha", "Meera",
    "Ananya", "Isha", "Kavya", "Riya", "Simran"
]

last_names = [
    "Patil", "Sharma", "Kulkarni", "Joshi", "Deshmukh",
    "Pawar", "Jadhav", "More", "Tathe", "Kale"
]

cities = [
    "Pune", "Mumbai", "Nashik", "Nagpur",
    "Bangalore", "Hyderabad", "Delhi", "Chennai"
]

payment_methods = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Cash",
    "Net Banking"
]

payment_statuses = [
    "Paid",
    "Pending",
    "Failed"
]

order_statuses = [
    "Completed",
    "Pending",
    "Cancelled",
    "Shipped"
]

# ==========================================
# 1. CUSTOMERS
# ==========================================

customers = []

for i in range(1, NUM_CUSTOMERS + 1):

    first_name = random.choice(first_names)
    last_name = random.choice(last_names)

    customers.append({
        "customer_id": i,
        "customer_name": f"{first_name} {last_name}",
        "email": f"customer{i}@example.com",
        "phone": f"9{random.randint(100000000, 999999999)}",
        "city": random.choice(cities)
    })

customers_df = pd.DataFrame(customers)

# ==========================================
# 2. PRODUCTS
# ==========================================

product_names = [
    "Laptop",
    "Desktop",
    "Monitor",
    "Keyboard",
    "Mouse",
    "Printer",
    "Office Chair",
    "Desk",
    "Router",
    "USB Hub",
    "Headphones",
    "Webcam",
    "SSD",
    "Hard Disk",
    "Tablet"
]

products = []

for i in range(1, NUM_PRODUCTS + 1):

    products.append({
        "product_id": i,
        "product_name": f"{random.choice(product_names)} {i}",

        # Existing PostgreSQL category IDs
        "category_id": random.choice(CATEGORY_IDS),

        # Existing PostgreSQL supplier IDs
        "supplier_id": random.choice(SUPPLIER_IDS),

        "unit_price": round(
            random.uniform(500, 100000),
            2
        )
    })

products_df = pd.DataFrame(products)

# ==========================================
# 3. ORDERS
# ==========================================

orders = []

start_date = datetime(2025, 1, 1)

for i in range(1, NUM_ORDERS + 1):

    order_date = start_date + timedelta(
        days=random.randint(0, 500)
    )

    orders.append({
        "order_id": i,
        "customer_id": random.randint(
            1,
            NUM_CUSTOMERS
        ),
        "order_date": order_date.strftime(
            "%Y-%m-%d"
        ),
        "order_status": random.choice(
            order_statuses
        ),
        "payment_method": random.choice(
            payment_methods
        ),
        "payment_status": random.choice(
            payment_statuses
        )
    })

orders_df = pd.DataFrame(orders)

# ==========================================
# 4. ORDER ITEMS
# ==========================================

order_items = []

item_id = 1

for order_id in range(1, NUM_ORDERS + 1):

    number_of_items = random.randint(1, 4)

    selected_products = random.sample(
        range(1, NUM_PRODUCTS + 1),
        number_of_items
    )

    for product_id in selected_products:

        quantity = random.randint(1, 10)

        product_price = products_df.loc[
            products_df["product_id"] == product_id,
            "unit_price"
        ].iloc[0]

        order_items.append({
            "order_item_id": item_id,
            "order_id": order_id,
            "product_id": product_id,
            "quantity": quantity,
            "unit_price": product_price,
            "total_amount": round(
                quantity * product_price,
                2
            )
        })

        item_id += 1

order_items_df = pd.DataFrame(order_items)

# ==========================================
# 5. SAVE RAW DATA
# ==========================================

customers_df.to_csv(
    "data/raw/customers.csv",
    index=False
)

products_df.to_csv(
    "data/raw/products.csv",
    index=False
)

orders_df.to_csv(
    "data/raw/orders.csv",
    index=False
)

order_items_df.to_csv(
    "data/raw/order_items.csv",
    index=False
)

# ==========================================
# SUCCESS
# ==========================================

print("=" * 50)
print("✅ FINAL PROJECT DATA GENERATED")
print("=" * 50)

print(f"Customers    : {len(customers_df)}")
print(f"Products     : {len(products_df)}")
print(f"Orders       : {len(orders_df)}")
print(f"Order Items  : {len(order_items_df)}")

print("=" * 50)
print("Existing PostgreSQL master data:")
print("Categories   : IDs 1-5")
print("Suppliers    : IDs 1-5")
print("=" * 50)