import pandas as pd


def extract_data():
    customers = pd.read_csv("data/raw/customers.csv")
    products = pd.read_csv("data/raw/products.csv")
    orders = pd.read_csv("data/raw/orders.csv")
    order_items = pd.read_csv("data/raw/order_items.csv")

    return customers, products, orders, order_items

if __name__ == "__main__":

    customers, products, orders, order_items = extract_data()

    print("=" * 50)
    print("RAW DATA EXTRACTION")
    print("=" * 50)

    print(f"Customers   : {len(customers)}")
    print(f"Products    : {len(products)}")
    print(f"Orders      : {len(orders)}")
    print(f"Order Items : {len(order_items)}")

    print("\n" + "=" * 50)
    print("CUSTOMERS")
    print("=" * 50)
    print(customers.head())

    print("\n" + "=" * 50)
    print("PRODUCTS")
    print("=" * 50)
    print(products.head())

    print("\n" + "=" * 50)
    print("ORDERS")
    print("=" * 50)
    print(orders.head())

    print("\n" + "=" * 50)
    print("ORDER ITEMS")
    print("=" * 50)
    print(order_items.head())