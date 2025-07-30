# main.py

import os
from tools.agent_tool import find_anuschka_bag_for_style
import ast

# --- 1. Define the user's request ---
user_input = "A nature-loving person who enjoys garden walks and prefers lightweight crossbody bags with floral prints."


print(f"🚀 Starting tool with input: '{user_input}'")

# --- 2. Call the tool directly ---
# Instead of using a complex agent, we call our single, powerful tool directly.
# This is much more reliable, especially with local models.
products = find_anuschka_bag_for_style.invoke(user_input)

# --- 3. Parse and Print the Final Output ---
print("\n" + "="*50)
print("✅ Tool run complete. Final Answer:")
print("="*50 + "\n")

try:
    if isinstance(products, list) and products:
        print("🛍️ Here are the top recommendations for you:\n")
        for i, product in enumerate(products):
            if isinstance(product, dict) and 'error' not in product:
                print(f"--- Product {i+1} ---")
                print(f"✨ Title: {product.get('title', 'N/A')}")
                print(f"   Price: {product.get('price', 'N/A')}")
                print(f"   URL: {product.get('url', 'N/A')}")
                print(f"   Image: {product.get('image_url', 'N/A')}\n")
            else:
                print(
                    f"Found an issue in the results: {product.get('error', str(product))}")
    else:
        print("❌ Sorry, I couldn't find any specific products matching your request. The website may not have items matching your description at this time.")

except Exception as e:
    print(f"An error occurred while processing the output: {e}")
    print("\nRaw Output:")
    print(products)
