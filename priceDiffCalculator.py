def clean_price(raw):
    """
    Cleans up price string like 'kr 27,40' or '29.90 kr' to a float.
    """
    raw = raw.replace("kr", "").replace("NOK", "").replace(",", ".").strip()
    return float(raw)


def calculate_price_differences(receipt_items, oda_items):
    """
    Compares receipt items with Oda prices.
    Returns a list of human-readable comparison notes.
    """
    comparisons = []
    total_diff = 0

    for receipt, oda in zip(receipt_items, oda_items):
        try:
            receipt_price = clean_price(receipt["price"])
            oda_price = clean_price(oda["oda_price"])
            diff = round(receipt_price - oda_price, 2)
            total_diff += diff

            product_name = receipt["name"]

            if diff > 0:
                comparisons.append(f"You overpaid {diff} NOK for {product_name}.")
            elif diff < 0:
                comparisons.append(f"You saved {abs(diff)} NOK on {product_name}!")
            else:
                comparisons.append(f"The price for {product_name} was the same.")
        except Exception as e:
            comparisons.append(f"Could not compare {receipt.get('name', 'Unknown')} due to error: {e}")

    summary = f"\nOverall you have {'overpaid' if total_diff > 0 else 'saved'} {abs(round(total_diff, 2))} NOK."

    comparisons.append(summary)
    return comparisons