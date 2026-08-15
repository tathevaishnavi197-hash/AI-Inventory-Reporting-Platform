from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from sqlalchemy import text
from database.connection import engine
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from google import genai
from api.gemini_service import generate_inventory_report

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

app = FastAPI(
    title="AI-Powered Inventory Reporting Platform",
    description="Backend API for inventory, sales and reporting analytics",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:3000",
    "https://ai-inventory-reporting-platform.vercel.app",
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "AI Inventory Reporting Platform API is running!"
    }

@app.get("/products")
def get_products():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT
                    product_id,
                    product_name,
                    category_id,
                    supplier_id,
                    unit_price,
                    stock_quantity
                FROM products
                ORDER BY product_id
            """)
        )

        products = result.mappings().all()

    return {
        "count": len(products),
        "products": products
    }

@app.get("/inventory")
def get_inventory():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT
                    i.inventory_id,
                    i.product_id,
                    p.product_name,
                    i.stock_available,
                    i.reorder_level,
                    i.last_updated
                FROM inventory i
                JOIN products p
                    ON i.product_id = p.product_id
                ORDER BY i.inventory_id
            """)
        )

        inventory = result.mappings().all()

    return {
        "count": len(inventory),
        "inventory": inventory
    }

@app.get("/orders")
def get_orders():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT
                    order_id,
                    customer_id,
                    order_date,
                    total_amount,
                    order_status
                FROM orders
                ORDER BY order_id
            """)
        )

        orders = result.mappings().all()

    return {
        "count": len(orders),
        "orders": orders
    }
@app.get("/customers")
def get_customers():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT
                    customer_id,
                    first_name,
                    last_name,
                    email,
                    phone,
                    city
                FROM customers
                ORDER BY customer_id
            """)
        )

        customers = result.mappings().all()

    return {
        "count": len(customers),
        "customers": customers
    }
@app.get("/dashboard/summary")
def dashboard_summary():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT
                    (SELECT COUNT(*) FROM customers) AS total_customers,
                    (SELECT COUNT(*) FROM products) AS total_products,
                    (SELECT COUNT(*) FROM orders) AS total_orders,
                    (SELECT COUNT(*) FROM inventory) AS total_products_in_inventory,
                    (SELECT COALESCE(SUM(total_amount), 0) FROM orders) AS total_sales
            """)
        )

        summary = result.mappings().one()

    return summary

@app.get("/payments")
def get_payments():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT
                    payment_id,
                    order_id,
                    payment_date,
                    payment_method,
                    payment_status,
                    amount
                FROM payments
                ORDER BY payment_id
            """)
        )

        payments = result.mappings().all()

    return {
        "count": len(payments),
        "payments": payments
    }
@app.get("/order-items")
def get_order_items():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT
                    order_item_id,
                    order_id,
                    product_id,
                    quantity,
                    unit_price
                FROM order_items
                ORDER BY order_item_id
            """)
        )

        order_items = result.mappings().all()

    return {
        "count": len(order_items),
        "order_items": order_items
    }
@app.get("/inventory/low-stock")
def get_low_stock():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT
                    i.inventory_id,
                    i.product_id,
                    p.product_name,
                    i.stock_available,
                    i.reorder_level
                FROM inventory i
                JOIN products p
                    ON i.product_id = p.product_id
                WHERE i.stock_available <= i.reorder_level
                ORDER BY i.stock_available ASC
            """)
        )

        low_stock = result.mappings().all()

    return {
        "count": len(low_stock),
        "low_stock_products": low_stock
    }
@app.get("/analytics/sales")
def sales_summary():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT
                    COUNT(order_id) AS total_orders,
                    ROUND(COALESCE(SUM(total_amount), 0), 2) AS total_sales,
                    ROUND(COALESCE(AVG(total_amount), 0), 2) AS average_order_value
                FROM orders
            """)
        )

        sales = result.mappings().one()

    return sales
@app.get("/analytics/payments")
def payment_summary():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT
                    payment_status,
                    COUNT(*) AS payment_count,
                    ROUND(SUM(amount), 2) AS total_amount
                FROM payments
                GROUP BY payment_status
                ORDER BY payment_status
            """)
        )

        payments = result.mappings().all()

    return {
        "payments": payments
    }
@app.get("/analytics/categories")
def category_summary():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT
                    c.category_name,
                    COUNT(p.product_id) AS product_count,
                    COALESCE(SUM(p.stock_quantity), 0) AS total_stock
                FROM categories c
                LEFT JOIN products p
                    ON c.category_id = p.category_id
                GROUP BY c.category_id, c.category_name
                ORDER BY product_count DESC
            """)
        )

        categories = result.mappings().all()

    return {
        "categories": categories
    }
@app.get("/analytics/suppliers")
def supplier_summary():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT
                    s.supplier_name,
                    COUNT(p.product_id) AS product_count,
                    COALESCE(SUM(p.stock_quantity), 0) AS total_stock
                FROM suppliers s
                LEFT JOIN products p
                    ON s.supplier_id = p.supplier_id
                GROUP BY s.supplier_id, s.supplier_name
                ORDER BY product_count DESC
            """)
        )

        suppliers = result.mappings().all()

    return {
        "suppliers": suppliers
    }
@app.get("/analytics/customers")
def customer_summary():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT
                    c.customer_id,
                    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
                    COUNT(o.order_id) AS order_count,
                    ROUND(COALESCE(SUM(o.total_amount), 0), 2) AS total_spent
                FROM customers c
                LEFT JOIN orders o
                    ON c.customer_id = o.customer_id
                GROUP BY c.customer_id, c.first_name, c.last_name
                ORDER BY total_spent DESC
            """)
        )

        customers = result.mappings().all()

    return {
        "customers": customers
    }
@app.get("/analytics/customers")
def customer_summary():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT
                    c.customer_id,
                    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
                    COUNT(o.order_id) AS order_count,
                    ROUND(COALESCE(SUM(o.total_amount), 0), 2) AS total_spent
                FROM customers c
                LEFT JOIN orders o
                    ON c.customer_id = o.customer_id
                GROUP BY c.customer_id, c.first_name, c.last_name
                ORDER BY total_spent DESC
            """)
        )

        customers = result.mappings().all()

    return {
        "customers": customers
    }
@app.get("/analytics/order-status")
def order_status_summary():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT
                    order_status,
                    COUNT(*) AS order_count,
                    ROUND(COALESCE(SUM(total_amount), 0), 2) AS total_amount
                FROM orders
                GROUP BY order_status
                ORDER BY order_count DESC
            """)
        )

        statuses = result.mappings().all()

    return {
        "order_status": statuses
    }
@app.get("/analytics/top-products")
def top_products():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT
                    p.product_id,
                    p.product_name,
                    SUM(oi.quantity) AS total_quantity_sold,
                    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_revenue
                FROM order_items oi
                JOIN products p
                    ON oi.product_id = p.product_id
                GROUP BY p.product_id, p.product_name
                ORDER BY total_revenue DESC
                LIMIT 10
            """)
        )

        products = result.mappings().all()

    return {
        "top_products": products
    }
@app.get("/analytics/inventory-value")
def inventory_value():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT
                    ROUND(
                        COALESCE(
                            SUM(i.stock_available * p.unit_price),
                            0
                        ),
                        2
                    ) AS total_inventory_value
                FROM inventory i
                JOIN products p
                    ON i.product_id = p.product_id
            """)
        )

        inventory = result.mappings().one()

    return inventory
@app.get("/analytics/monthly-sales")
def monthly_sales():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT
                    TO_CHAR(order_date, 'YYYY-MM') AS month,
                    COUNT(order_id) AS order_count,
                    ROUND(SUM(total_amount), 2) AS total_sales
                FROM orders
                GROUP BY TO_CHAR(order_date, 'YYYY-MM')
                ORDER BY month
            """)
        )

        monthly = result.mappings().all()

    return {
        "monthly_sales": monthly
    }
@app.get("/analytics/stock-summary")
def stock_summary():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT
                    COUNT(*) AS total_products,
                    COALESCE(SUM(stock_available), 0) AS total_stock,
                    COUNT(*) FILTER (
                        WHERE stock_available <= reorder_level
                    ) AS low_stock_products,
                    COUNT(*) FILTER (
                        WHERE stock_available = 0
                    ) AS out_of_stock_products
                FROM inventory
            """)
        )

        stock = result.mappings().one()

    return stock
@app.get("/ai-test")
def ai_test():
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Explain in one sentence what an inventory reporting system does."
    )

    return {
        "ai_response": response.text
    }
@app.get("/ai/inventory-report")
def ai_inventory_report():

    inventory_response = get_inventory()

    inventory_data = inventory_response["inventory"]

    reorder_items = [
        item
        for item in inventory_data
        if item["stock_available"] < item["reorder_level"]
    ]

    report_data = {
        "total_products": len(inventory_data),
        "reorder_products": reorder_items
    }

    report = generate_inventory_report(report_data)

    return {
        "report": report
    }

@app.get("/ai/analyze")
def ai_analyze(query: str = Query(..., min_length=1)):

    query_lower = query.lower()

    # --------------------------------------------------
    # FETCH BUSINESS DATA
    # --------------------------------------------------

    inventory_response = get_inventory()
    inventory_data = inventory_response["inventory"]

    sales_data = sales_summary()
    payments_data = payment_summary()
    order_status_data = order_status_summary()
    category_data = category_summary()
    top_products_data = top_products()
    monthly_sales_data = monthly_sales()

    # --------------------------------------------------
    # DETERMINE QUERY TYPE
    # --------------------------------------------------

    if any(word in query_lower for word in [
        "reorder",
        "low stock",
        "low-stock",
        "inventory"
    ]):
        query_type = "inventory"

    elif any(word in query_lower for word in [
        "monthly sales",
        "sales trend",
        "sales",
        "revenue"
    ]):
        query_type = "sales"

    elif any(word in query_lower for word in [
        "payment",
        "payments",
        "paid",
        "failed",
        "pending"
    ]):
        query_type = "payments"

    elif any(word in query_lower for word in [
        "order status",
        "orders"
    ]):
        query_type = "orders"

    elif any(word in query_lower for word in [
        "category",
        "categories"
    ]):
        query_type = "categories"

    elif any(word in query_lower for word in [
        "top product",
        "top products",
        "best selling",
        "best-selling",
        "selling products"
    ]):
        query_type = "top_products"

    else:
        query_type = "general"

    # --------------------------------------------------
    # DEFAULT
    # --------------------------------------------------

    metrics = []
    charts = []
    recommendations = []
    relevant_data = {}

    # ==================================================
    # INVENTORY
    # ==================================================

    if query_type == "inventory":

        reorder_items = [
            item
            for item in inventory_data
            if float(item["stock_available"])
            < float(item["reorder_level"])
        ]

        critical_items = [
            item
            for item in reorder_items
            if float(item["stock_available"]) <= 13
        ]

        metrics = [
            {
                "label": "Total Products",
                "value": len(inventory_data)
            },
            {
                "label": "Low Stock Products",
                "value": len(reorder_items)
            },
            {
                "label": "Critical Stock",
                "value": len(critical_items)
            }
        ]

        chart_items = reorder_items[:10]

        # CHART 1 — REORDER STOCK
        charts.append({
            "type": "bar",
            "title": "Products Requiring Reorder",
            "labels": [
                item["product_name"]
                for item in chart_items
            ],
            "values": [
                int(item["stock_available"])
                for item in chart_items
            ]
        })

        # CHART 2 — REORDER LEVEL
        charts.append({
            "type": "line",
            "title": "Stock Available vs Reorder Level",
            "labels": [
                item["product_name"]
                for item in chart_items
            ],
            "values": [
                int(item["reorder_level"])
                for item in chart_items
            ]
        })

        recommendations = [
            "Prioritize products that are below their reorder level.",
            "Review critically low-stock products immediately.",
            "Create purchase orders for products requiring replenishment."
        ]

        relevant_data = reorder_items

    # ==================================================
    # SALES
    # ==================================================

    elif query_type == "sales":

        monthly_rows = monthly_sales_data["monthly_sales"]

        metrics = [
            {
                "label": "Total Orders",
                "value": int(sales_data["total_orders"])
            },
            {
                "label": "Total Sales",
                "value": float(sales_data["total_sales"])
            },
            {
                "label": "Average Order Value",
                "value": float(sales_data["average_order_value"])
            }
        ]

        # CHART 1 — MONTHLY SALES
        charts.append({
            "type": "line",
            "title": "Monthly Sales Trend",
            "labels": [
                item["month"]
                for item in monthly_rows
            ],
            "values": [
                float(item["total_sales"])
                for item in monthly_rows
            ]
        })

        # CHART 2 — MONTHLY ORDERS
        charts.append({
            "type": "bar",
            "title": "Monthly Order Count",
            "labels": [
                item["month"]
                for item in monthly_rows
            ],
            "values": [
                int(item["order_count"])
                for item in monthly_rows
            ]
        })

        recommendations = [
            "Monitor monthly sales trends to identify strong and weak periods.",
            "Compare order volume with sales revenue before planning inventory purchases."
        ]

        relevant_data = {
            "sales": sales_data,
            "monthly_sales": monthly_rows
        }

    # ==================================================
    # PAYMENTS
    # ==================================================

    elif query_type == "payments":

        payment_rows = payments_data["payments"]

        metrics = [
            {
                "label": "Payment Records",
                "value": sum(
                    int(item["payment_count"])
                    for item in payment_rows
                )
            },
            {
                "label": "Paid Payments",
                "value": next(
                    (
                        int(item["payment_count"])
                        for item in payment_rows
                        if item["payment_status"] == "Paid"
                    ),
                    0
                )
            },
            {
                "label": "Failed Payments",
                "value": next(
                    (
                        int(item["payment_count"])
                        for item in payment_rows
                        if item["payment_status"] == "Failed"
                    ),
                    0
                )
            }
        ]

        # CHART 1 — PAYMENT COUNT
        charts.append({
            "type": "pie",
            "title": "Payment Status Distribution",
            "labels": [
                item["payment_status"]
                for item in payment_rows
            ],
            "values": [
                int(item["payment_count"])
                for item in payment_rows
            ]
        })

        # CHART 2 — PAYMENT AMOUNT
        charts.append({
            "type": "bar",
            "title": "Payment Amount by Status",
            "labels": [
                item["payment_status"]
                for item in payment_rows
            ],
            "values": [
                float(item["total_amount"] or 0)
                for item in payment_rows
            ]
        })

        recommendations = [
            "Monitor failed payments and investigate recurring payment issues.",
            "Review pending payments regularly to improve cash-flow visibility."
        ]

        relevant_data = payment_rows

    # ==================================================
    # ORDER STATUS
    # ==================================================

    elif query_type == "orders":

        status_rows = order_status_data["order_status"]

        metrics = [
            {
                "label": "Total Orders",
                "value": sum(
                    int(item["order_count"])
                    for item in status_rows
                )
            },
            {
                "label": "Order Statuses",
                "value": len(status_rows)
            }
        ]

        # CHART 1 — ORDER COUNT
        charts.append({
            "type": "bar",
            "title": "Order Status Distribution",
            "labels": [
                item["order_status"]
                for item in status_rows
            ],
            "values": [
                int(item["order_count"])
                for item in status_rows
            ]
        })

        # CHART 2 — ORDER VALUE
        charts.append({
            "type": "pie",
            "title": "Order Value by Status",
            "labels": [
                item["order_status"]
                for item in status_rows
            ],
            "values": [
                float(item["total_amount"] or 0)
                for item in status_rows
            ]
        })

        recommendations = [
            "Monitor order statuses to identify delays or operational bottlenecks.",
            "Investigate unusual increases in cancelled or pending orders."
        ]

        relevant_data = status_rows

    # ==================================================
    # CATEGORIES
    # ==================================================

    elif query_type == "categories":

        category_rows = category_data["categories"]

        metrics = [
            {
                "label": "Total Categories",
                "value": len(category_rows)
            },
            {
                "label": "Total Stock",
                "value": sum(
                    int(item["total_stock"])
                    for item in category_rows
                )
            }
        ]

        # CHART 1 — PRODUCT COUNT
        charts.append({
            "type": "bar",
            "title": "Products by Category",
            "labels": [
                item["category_name"]
                for item in category_rows
            ],
            "values": [
                int(item["product_count"])
                for item in category_rows
            ]
        })

        # CHART 2 — STOCK
        charts.append({
            "type": "line",
            "title": "Stock by Category",
            "labels": [
                item["category_name"]
                for item in category_rows
            ],
            "values": [
                int(item["total_stock"])
                for item in category_rows
            ]
        })

        recommendations = [
            "Compare category-level product counts to understand assortment distribution.",
            "Review categories with unusually low stock before replenishment planning."
        ]

        relevant_data = category_rows

    # ==================================================
    # TOP PRODUCTS
    # ==================================================

    elif query_type == "top_products":

        product_rows = top_products_data["top_products"]

        metrics = [
            {
                "label": "Top Products",
                "value": len(product_rows)
            },
            {
                "label": "Total Units Sold",
                "value": sum(
                    int(item["total_quantity_sold"])
                    for item in product_rows
                )
            },
            {
                "label": "Top Product Revenue",
                "value": (
                    float(product_rows[0]["total_revenue"])
                    if product_rows
                    else 0
                )
            }
        ]

        # CHART 1 — REVENUE
        charts.append({
            "type": "bar",
            "title": "Top Selling Products by Revenue",
            "labels": [
                item["product_name"]
                for item in product_rows
            ],
            "values": [
                float(item["total_revenue"])
                for item in product_rows
            ]
        })

        # CHART 2 — UNITS SOLD
        charts.append({
            "type": "line",
            "title": "Top Selling Products by Units Sold",
            "labels": [
                item["product_name"]
                for item in product_rows
            ],
            "values": [
                int(item["total_quantity_sold"])
                for item in product_rows
            ]
        })

        recommendations = [
            "Maintain sufficient inventory for high-performing products.",
            "Prioritize popular products during replenishment planning."
        ]

        relevant_data = product_rows

    # ==================================================
    # GENERAL
    # ==================================================

    else:

        metrics = [
            {
                "label": "Total Products",
                "value": len(inventory_data)
            },
            {
                "label": "Total Orders",
                "value": int(sales_data["total_orders"])
            },
            {
                "label": "Total Sales",
                "value": float(sales_data["total_sales"])
            }
        ]

        # General query gets NO irrelevant charts
        charts = []

        recommendations = [
            "Ask about inventory, sales, payments, orders, categories or top-selling products for a focused analysis."
        ]

        relevant_data = {
            "inventory": inventory_data[:20],
            "sales": sales_data,
            "payments": payments_data,
            "orders": order_status_data
        }

        # ==================================================
    # GEMINI ANALYSIS - FAST
    # ==================================================

    prompt = f"""
You are an AI business analyst for an Inventory Reporting Platform.

User query: "{query}"
Query type: "{query_type}"

Business data:
{relevant_data}

Give a SHORT professional analysis based ONLY on this data.

Return only:
1. Analysis - 2 short sentences.
2. Key Findings - maximum 3 points.
3. Business Recommendation - maximum 2 points.

Do not invent numbers or data.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        analysis = response.text.strip()

    except Exception as e:
        print("GEMINI ERROR:", e)

        analysis = (
            "The business data was analyzed successfully. "
            "AI-generated insights are temporarily unavailable."
        )

    # ==================================================
    # FINAL RESPONSE
    # ==================================================

    return {
        "query": query,
        "query_type": query_type,
        "analysis": analysis,
        "metrics": metrics,
        "charts": charts,
        "recommendations": recommendations
    }
# ==================================================
# INVENTORY PDF REPORT
# ==================================================

@app.get("/reports/inventory-pdf")
def inventory_pdf(query: str = Query(..., min_length=1)):

    sales = sales_summary()
    monthly = monthly_sales()["monthly_sales"]

    file_path = "inventory_report.pdf"

    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    story = []

    story.append(
        Paragraph(
            "AI-Powered Inventory Reporting Platform",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            f"<b>Query:</b> {query}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "Sales Summary",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            f"Total Orders: {sales['total_orders']}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Total Sales: {sales['total_sales']}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Average Order Value: {sales['average_order_value']}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "Monthly Sales Data",
            styles["Heading2"]
        )
    )

    for row in monthly:
        story.append(
            Paragraph(
                f"{row['month']} — "
                f"Orders: {row['order_count']} — "
                f"Sales: {row['total_sales']}",
                styles["Normal"]
            )
        )

    doc.build(story)

    return FileResponse(
        file_path,
        media_type="application/pdf",
        filename="inventory_report.pdf"
    )