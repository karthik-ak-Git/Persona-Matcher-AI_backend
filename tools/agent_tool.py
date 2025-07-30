# tools/agent_tool.py

from langchain_core.tools import tool
from .bag_recommender import get_style_recommendation
from .local_search_anuschka import search_anuschka_products
import re


@tool
def find_anuschka_bag_for_style(style_description: str) -> list[dict]:
    """
    Finds and returns a list of Anuschka bags based on a style description.
    This tool intelligently searches for bags using style keywords and performs
    fallback searches if no exact matches are found.
    """
    print(f"[🔎] Using combined tool for style: '{style_description}'")

    # Step 1: Get style recommendation and keywords from our helper function
    recommendation_output = get_style_recommendation(style_description)
    print(f"[📝] Generated recommendation: {recommendation_output}")

    # Step 2: Extract the keywords from the recommendation string
    match = re.search(r"Search Keywords: (.*)", recommendation_output)
    if not match:
        print("[⚠️] Could not extract keywords from recommendation.")
        return [{'error': 'Could not determine search keywords from the style description.'}]

    keywords = match.group(1).strip().split(', ')

    # --- Primary Search Attempt ---
    primary_search_query = ' '.join(keywords[:3])
    print(
        f"[🔑] Attempting primary search with keywords: '{primary_search_query}'")
    products = search_anuschka_products(primary_search_query)

    # --- Secondary Search ---
    if not products:
        print("[⚠️] Primary search failed. Attempting secondary search.")
        secondary_search_query = ' '.join(keywords[:2])
        print(
            f"[🔑] Attempting secondary search with keywords: '{secondary_search_query}'")
        products = search_anuschka_products(secondary_search_query)

    # --- Tertiary Search ---
    if not products:
        print("[⚠️] Secondary search failed. Attempting tertiary search.")
        tertiary_search_query = keywords[0]
        print(
            f"[🔑] Attempting tertiary search with keyword: '{tertiary_search_query}'")
        products = search_anuschka_products(tertiary_search_query)

    # --- Final Broad Search with Filtering ---
    if not products:
        print(
            "[🛠️] All strict keyword searches failed. Trying broad site search + keyword filtering.")
        # Empty query to trigger broad search
        all_results = search_anuschka_products("")

        if all_results:
            print(
                f"[📦] Found {len(all_results)} products in broad search. Filtering by keyword match...")
            filtered = []
            for product in all_results:
                combined_text = f"{product.get('title', '')} {product.get('description', '')}".lower(
                )
                if any(keyword.lower() in combined_text for keyword in keywords):
                    filtered.append(product)
            products = filtered
            print(
                f"[✅] Found {len(products)} filtered matches using fallback strategy.")
        else:
            print("[❌] Broad fallback search returned no products.")

    if not products:
        print("[❌] Final fallback search also failed. No matching products found.")

    return products
