# run_image_batch.py

import os
from tools.agent_tool import find_anuschka_bag_for_style
from dotenv import load_dotenv


def display_results(image_path, products):
    """Helper function to print product results for a given image."""
    print("\n" + "="*60)
    print(f"🌟 Recommendations For: {os.path.basename(image_path)}")
    print("="*60)

    try:
        if isinstance(products, list) and products:
            # The tool is designed to return the single best product in a list
            product = products[0]
            if isinstance(product, dict) and 'error' not in product:
                print(f"✨ Title: {product.get('title', 'N/A')}")
                print(f"   Price: {product.get('price', 'N/A')}")
                print(f"   URL: {product.get('url', 'N/A')}")
                print(f"   Image: {product.get('image_url', 'N/A')}\n")
            else:
                print(
                    f"❌ An issue occurred: {product.get('error', str(product))}")
        else:
            print("❌ Sorry, no specific products were found for this image.")

    except Exception as e:
        print(f"An error occurred while processing the output: {e}")
        print("\nRaw Output:")
        print(products)


def process_image_recommendations(image_paths: list[str]):
    """
    Processes a list of image file paths and gets a bag recommendation for each.
    """
    if not image_paths:
        print("No image paths provided.")
        return

    for image_path in image_paths:
        if os.path.exists(image_path):
            print(f"\n🚀 Starting tool with image input: '{image_path}'")
            # Here we invoke our powerful image-based tool for each image
            recommended_products = find_anuschka_bag_for_style.invoke(
                image_path)
            display_results(image_path, recommended_products)
        else:
            print(f"\n⚠️  Could not find image at '{image_path}'. Skipping.")


if __name__ == "__main__":
    # Load API keys from .env file
    load_dotenv()

    # --- List of Images to Process ---
    # **IMPORTANT**: Create a folder named 'test_images' in your project
    # and add the images you want to test. Then, update the list below.
    # For example:
    # image_files_to_test = [
    #     "test_images/professional_outfit.jpg",
    #     "test_images/casual_style.png",
    #     "test_images/person_with_bold_colors.jpg",
    # ]

    image_files_to_test = [
        "pexels-see2believe-2450308.jpg"
    ]

    if not image_files_to_test:
        print("="*60)
        print("‼️ Please edit 'run_image_batch.py' and add your image paths to the 'image_files_to_test' list.")
        print("="*60)
    else:
        process_image_recommendations(image_files_to_test)
