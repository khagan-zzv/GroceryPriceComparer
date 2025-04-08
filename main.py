import recieptExtract
from odaPrices import get_oda_prices_for_items
from usingAI import compare_price


def main():
    image_path = "photo_2025-04-08 15.10.53.jpeg"

    receipt_items = recieptExtract.get_purchased_items(image_path)
    oda_items = get_oda_prices_for_items(receipt_items)
    print(f"Receipt Items:{receipt_items}")
    print("Oda Search Results:")
    for item in oda_items:
        print(f"{item['oda_name']} — {item['oda_price']}")

    print(compare_price(receipt_items, oda_items))


if __name__ == "__main__":
    main()
