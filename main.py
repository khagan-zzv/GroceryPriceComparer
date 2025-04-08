import recieptExtract
from odaPrices import get_oda_prices_for_items
from priceDiffCalculator import calculate_price_differences
from usingAI import compare_price


def main():
    image_path = "photo_2025-04-08 21.26.54.jpeg"

    receipt_items = recieptExtract.get_purchased_items(image_path)
    oda_items = get_oda_prices_for_items(receipt_items)

    price_notes = calculate_price_differences(receipt_items, oda_items)

    print("\n📊 Price Analysis:")
    for note in price_notes:
        print(note)
"""
   
    print(f"Receipt Items:{receipt_items}")
    print("Oda Search Results:")
    for item in oda_items:
        print(f"{item['oda_name']} — {item['oda_price']}")

    print(compare_price(receipt_items, oda_items))
"""

if __name__ == "__main__":
    main()
