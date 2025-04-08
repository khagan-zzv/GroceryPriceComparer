import time
from urllib.parse import quote_plus
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from usingAI import find_best_match

ODA_SEARCH_URL = "https://oda.com/no/search/products/?q="


def get_oda_prices_for_items(receipt_items):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    results = []

    try:
        for item in receipt_items:
            name_only = item["name"]
            encoded = quote_plus(name_only)
            search_url = ODA_SEARCH_URL + encoded
            print(f"Searching Oda for: {name_only} → {search_url}")
            driver.get(search_url)
            time.sleep(5)
            product_cards = driver.find_elements(By.CSS_SELECTOR, "#main-content article")
            oda_candidates = []
            for card in product_cards:
                try:
                    name_el = card.find_element(By.CSS_SELECTOR, "h2")
                    try:
                        #if on sale
                        price_el = card.find_element(
                            By.CSS_SELECTOR,
                            "div.k-flex.k-align-items-flex-start.k-flex--gap-0.k-flex--direction-column > span"
                        )
                    except:
                        try:
                            #regular price
                            price_el = card.find_element(By.CSS_SELECTOR, "span")
                        except:
                            print(f"Skipping item (no price found)")
                            continue
                    try:
                        description_el = card.find_element(By.CSS_SELECTOR, "p")
                        description = description_el.text.strip()
                    except:
                        description = ""
                    oda_candidates.append({
                        "name": name_el.text.strip(),
                        "price": price_el.text.strip(),
                        "description": description,
                        "url": search_url
                    })
                except Exception:
                    continue
            best_match = find_best_match(item, oda_candidates)
            best_match["oda_url"] = search_url
            results.append(best_match)
        return results
    finally:
        driver.quit()
