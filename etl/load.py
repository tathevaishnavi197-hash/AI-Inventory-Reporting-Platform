import pandas as pd
import psycopg2


# ==========================================
# DATABASE CONNECTION
# ==========================================

connection = psycopg2.connect(
    host="localhost",
    database="inventory_sales_db",
    user="postgres",
    password="root",
    port="5432"
)

cursor = connection.cursor()

print("✅ PostgreSQL connection successful!")


# ==========================================
# LOAD CUSTOMERS
# ==========================================

customers = pd.read_csv(
    "data/cleaned/customers_clean.csv"
)

print("\nCustomers to load:", len(customers))


for _, row in customers.iterrows():

    cursor.execute(
        """
        INSERT INTO customers
        (
            customer_id,
            first_name,
            last_name,
            email,
            phone,
            city
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (customer_id) DO NOTHING
        """,
        (
            int(row["customer_id"]),
            row["customer_name"].split(" ", 1)[0],
            row["customer_name"].split(" ", 1)[1],
            row["email"],
            str(row["phone"]),
            row["city"]
        )
    )

# ==========================================
# LOAD PRODUCTS
# ==========================================

products = pd.read_csv(
    "data/cleaned/products_clean.csv"
)

print("\nProducts to load:", len(products))

for _, row in products.iterrows():

    cursor.execute(
        """
        INSERT INTO products
        (
            product_id,
            product_name,
            category_id,
            supplier_id,
            sku,
            unit_price,
            stock_quantity
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (product_id) DO NOTHING
        """,
        (
            int(row["product_id"]),
            row["product_name"],
            int(row["category_id"]),
            int(row["supplier_id"]),
            f"SKU-{int(row['product_id']):05d}",
            float(row["unit_price"]),
            0
        )
    )
    # ==========================================
# LOAD ORDERS
# ==========================================

orders = pd.read_csv(
    "data/cleaned/orders_clean.csv"
)

print("\nOrders to load:", len(orders))

for _, row in orders.iterrows():

    cursor.execute(
        """
        INSERT INTO orders
        (
            order_id,
            customer_id,
            order_date,
            total_amount,
            order_status
        )
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (order_id) DO NOTHING
        """,
        (
            int(row["order_id"]),
            int(row["customer_id"]),
            row["order_date"],
            0,
            row["order_status"]
        )
    )
# ==========================================
# LOAD ORDER ITEMS
# ==========================================

order_items = pd.read_csv(
    "data/cleaned/order_items_clean.csv"
)

print("\nOrder Items to load:", len(order_items))

for _, row in order_items.iterrows():

    cursor.execute(
        """
        INSERT INTO order_items
        (
            order_item_id,
            order_id,
            product_id,
            quantity,
            unit_price
        )
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (order_item_id) DO NOTHING
        """,
        (
            int(row["order_item_id"]),
            int(row["order_id"]),
            int(row["product_id"]),
            int(row["quantity"]),
            float(row["unit_price"])
        )
    )
# ==========================================
# LOAD PAYMENTS
# ==========================================

print("\nLoading payments...")

payment_id = 1

for _, row in orders.iterrows():
    cursor.execute(
        """
        SELECT total_amount
        FROM orders
        WHERE order_id = %s
        """,
        (int(row["order_id"]),)
    )

    result = cursor.fetchone()

    amount = result[0]

    cursor.execute(
        """
        INSERT INTO payments
        (
            payment_id,
            order_id,
            payment_date,
            payment_method,
            payment_status,
            amount
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (payment_id) DO NOTHING
        """,
        (
            payment_id,
            int(row["order_id"]),
            row["order_date"],
            row["payment_method"],
            row["payment_status"],
            0
        )
    )

    payment_id += 1

    # ==========================================
# LOAD INVENTORY
# ==========================================

print("\nLoading inventory...")

import random

inventory_id = 1

for _, row in products.iterrows():

    stock_available = random.randint(10, 200)
    reorder_level = random.randint(10, 50)

    cursor.execute(
        """
        INSERT INTO inventory
        (
            inventory_id,
            product_id,
            stock_available,
            reorder_level
        )
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (inventory_id) DO NOTHING
        """,
        (
            inventory_id,
            int(row["product_id"]),
            stock_available,
            reorder_level
        )
    )

    inventory_id += 1

connection.commit()

print("✅ Inventory loaded successfully!")

connection.commit()

print("✅ Payments loaded successfully!")
connection.commit()

print("✅ Order Items loaded successfully!")
connection.commit()

print("✅ Orders loaded successfully!")

connection.commit()

print("✅ Products loaded successfully!")
connection.commit()

print("✅ Customers loaded successfully!")


# ==========================================
# CLOSE CONNECTION
# ==========================================

cursor.close()
connection.close()

print("✅ Database connection closed!")