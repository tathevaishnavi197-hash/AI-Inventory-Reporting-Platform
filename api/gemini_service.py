import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_inventory_report(report_data):

    prompt = f"""
You are an AI inventory reporting assistant.

Analyze the validated inventory data provided below and generate a professional
inventory report for a business manager.

IMPORTANT RULE:
The backend has already validated which products require reordering.

A product requires reordering ONLY when:
stock_available < reorder_level

Do NOT independently add products to the reorder list.
Use ONLY the products provided in "reorder_products" as products requiring reorder.

Inventory Summary:
- Total Products: {report_data["total_products"]}
- Products Requiring Reorder: {len(report_data["reorder_products"])}

Validated Reorder Products:
{report_data["reorder_products"]}

Generate the report with these sections:

1. Overall Inventory Situation
2. Products That Need Reordering
3. Critically Low Stock Products
4. Inventory Risk Analysis
5. Recommended Inventory Actions

For each reorder product, clearly show:
- Product name
- Current stock
- Reorder level

Critically low stock means stock_available <= 13.

Do not invent products, stock values, reorder levels, or numerical facts.
Base the report only on the provided data.

Keep the report professional, clear and useful for inventory management.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text