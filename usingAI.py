import json

from openai import OpenAI

client = OpenAI()

# Making bought items usable for search
def enhance_bought_items(input_content):
    response = client.responses.create(
        model="gpt-4o",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Extract all products and their prices from this receipt file. "
                                "If there are two of the same product, return price per item."
                                "If the item has a specific brand name, remove it from the name and add it to details."
                                "For example XTRA MAISKORN can be just MAISKORN or COOP CHEDDAR REVET can be just CHEDDAR REVET."
                                "Also items such as FIRKLØVER M/APPELSIN can be just FIRKLØVER with rest added to details."
                                "If the item has weight or unit, remove it from the name and add to details."
                                "Skip items such as PANT, PLASTPOSE"
                    },
                    input_content,
                ],
            }
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "receipt_items",
                "schema": {
                    "type": "object",
                    "properties": {
                        "items": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "details": {"type": "string"},
                                    "price": {"type": "string"}
                                },
                                "required": ["name", "price", "details"],
                                "additionalProperties": False
                            }
                        }
                    },
                    "required": ["items"],
                    "additionalProperties": False
                },
                "strict": True
            }
        }
    )
    return response.output_text

# Finding best match for each item from Oda
def find_best_match(receipt_item, oda_products):
    if not oda_products:
        return {
            "searched": f"{receipt_item['name']} {receipt_item.get('details', '')}".strip(),
            "oda_name": "Not Found",
            "oda_price": "N/A",
            "oda_url": "N/A"
        }

    product_list = "\n".join([
        f"- {p['name']}" +
        (f" — {p['description']}" if p.get("description") else "") +
        f" — {p['price']}"
        for p in oda_products
    ])

    prompt = (
        f"The customer bought '{receipt_item['name']} {receipt_item.get('details', '')}'.\n\n"
        f"Below is a list of product results from a grocery store:\n\n"
        f"{product_list}\n\n"
        "Please choose the closest possible match and return its name and price. "
        "Try to match quantities and units as much as possible. "
    )
    response = client.responses.create(
        model="gpt-4o",
        input=[{
            "role": "user",
            "content": [
                {"type": "input_text", "text": prompt}
            ]
        }],
        text={
            "format": {
                "type": "json_schema",
                "name": "selected_oda_match",
                "schema": {
                    "type": "object",
                    "properties": {
                        "oda_name": {"type": "string"},
                        "oda_price": {"type": "string"}
                    },
                    "required": ["oda_name", "oda_price"],
                    "additionalProperties": False
                },
                "strict": True,

            }
        }
    )
    print(response.output_text)
    best = json.loads(response.output_text)
    return {
        "searched": f"{receipt_item['name']} {receipt_item.get('details', '')}".strip(),
        "oda_name": best["oda_name"],
        "oda_price": best["oda_price"]
    }


#Compare prices of what user bought to Oda prices
def compare_price(receipt_items, oda_items):
    response = client.responses.create(
        model="gpt-4o",
        input="You are an assistant which helps to compare grocery prices in different stores."
              "Please compare the prices of the items in the list and tell user"
              "how much they would save or overpaid if they would shopped from Oda. "
              "BE SURE TO DO MATH CORRECT!"
              "Try to keep answers short"
              "Here is the list of items user bought at different store:\n\n"
              f"{receipt_items}\n\n"
              f"And here is the list of items from Oda:\n\n"
              f"{oda_items}\n\n"
    )
    return response.output_text