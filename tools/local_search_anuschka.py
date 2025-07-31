import requests
from bs4 import BeautifulSoup
import json
from duckduckgo_search import DDGS
from urllib.parse import urljoin

def search_products(query: str, max_results=5):
    """
    Searches for products on the Anuschka Leather website using DuckDuckGo and scrapes product details.

    Args:
        query: The search query.
        max_results: The maximum number of products to return.

    Returns:
        A list of dictionaries, where each dictionary represents a product.
    """
    base_url = "https://anuschkaleather.com"
    site_query = f"site:{base_url} {query}"
    products = []
    seen_urls = set()

    print(f"[🦆] Searching DuckDuckGo for: {site_query}")
    try:
        with DDGS() as ddgs:
            # Get more results to increase chances of finding valid products
            results = list(ddgs.text(site_query, max_results=15))
            print(f"[📊] DDGS returned {len(results)} results.")
    except Exception as e:
        print(f"[❌] DuckDuckGo search failed: {e}")
        results = []

    if not results:
        print("[⚠️] No results from DuckDuckGo search. Aborting.")
        return []

    for r in results:
        if len(products) >= max_results:
            break

        url = r.get('href') or r.get('url')
        # Ensure we are only processing valid product pages
        if not url or 'anuschkaleather.com/products/' not in url:
            continue

        url = url.split('?')[0]  # Clean up URL parameters
        if url in seen_urls:
            continue
        seen_urls.add(url)

        print(f"[🔗] Processing product page: {url}")
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            resp = requests.get(url, timeout=20, headers=headers)
            print(f"[📈] HTTP Status for {url}: {resp.status_code}")
            resp.raise_for_status()
            soup = BeautifulSoup(resp.content, 'html.parser')

            title_el = soup.select_one(
                'h1.product__title, h1.product-title, h1, title')
            title = title_el.get_text(strip=True) if title_el else 'N/A'
            print(f"[🏷️] Found title: {title != 'N/A'}")

            price_el = soup.select_one(
                '.price__regular .price-item, .product__price, .price, .product-price')
            price = price_el.get_text(
                strip=True) if price_el else 'Price not available'
            print(f"[💰] Found price: {price != 'Price not available'}")

            # --- NEW, MORE ROBUST IMAGE EXTRACTION STRATEGY ---
            image_url = ''

            # 1. Try to find JSON-LD structured data (most reliable method)
            json_ld_script = soup.find(
                'script', {'type': 'application/ld+json'})
            if json_ld_script:
                try:
                    data = json.loads(json_ld_script.string)
                    if isinstance(data, list):
                        data = data[0]
                    if data.get('@type') == 'Product':
                        image_data = data.get('image')
                        if isinstance(image_data, list) and image_data:
                            image_url = image_data[0]
                        elif isinstance(image_data, str):
                            image_url = image_data
                        if image_url:
                            print(
                                f"[✅] Found image URL in JSON-LD data: {image_url}")
                except (json.JSONDecodeError, KeyError, IndexError) as e:
                    print(f"[⚠️] Could not parse JSON-LD data: {e}")

            # 2. If JSON-LD fails, try Open Graph meta tags (very reliable)
            if not image_url:
                og_image = soup.find('meta', {'property': 'og:image'})
                if og_image and og_image.get('content'):
                    image_url = og_image['content']
                    print(
                        f"[✅] Found image URL in Open Graph meta tag: {image_url}")

            # 3. If that fails, try a broad set of CSS selectors
            if not image_url:
                selectors = [
                    'figure.product__media img',
                    '.product-gallery__image img',
                    '.product-image-main img',
                    'img.product-gallery__image',
                    'img.product__image'
                ]
                image_element = soup.select_one(', '.join(selectors))
                if image_element:
                    src = image_element.get(
                        'src') or image_element.get('data-src')
                    if src:
                        if src.startswith('//'):
                            image_url = f"https:{src}"
                        else:
                            image_url = urljoin(base_url, src)
                        print(
                            f"[🖼️] Successfully extracted image URL with CSS selector: {image_url}")

            if not image_url:
                print(
                    f"[❌] Could not find an image URL for this product: {url}")

            desc = soup.select_one(
                '.product__description, .product-description, .product__info-content')
            description = desc.get_text(strip=True) if desc else ''

            # Only add product if we have the essential details
            if title != 'N/A' and image_url:
                products.append({
                    'id': str(hash(url)),  # Generate unique ID from URL
                    'name': title,  # Map title to name for frontend
                    'title': title,  # Keep original for backwards compatibility
                    'price': price,
                    'link': url,  # Map url to link for frontend
                    'url': url,  # Keep original for backwards compatibility
                    'image': image_url,  # Map image_url to image for frontend
                    'image_url': image_url,  # Keep original for backwards compatibility
                    'description': description,
                })
                print(f"[✅] Successfully scraped product: {title}")
            else:
                print(f"[❌] Discarding product due to missing title or image: {url}")

        except requests.exceptions.RequestException as e:
            print(f"[⚠️] Request failed for {url}: {e}")
            continue
        except Exception as e:
            print(f"[⚠️] Error scraping {url}: {e}")
            continue

    print(f"[🎉] Finished scraping. Found {len(products)} valid products.")
    return products