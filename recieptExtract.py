import json
from prepareFile import prepare_input_for_openai
from usingAI import enhance_bought_items

def get_purchased_items(image_path):
    input_content = prepare_input_for_openai(image_path)
    purchased_items=enhance_bought_items(input_content)
    print(json.loads(purchased_items))
    receipt_data = json.loads(purchased_items)
    return receipt_data["items"]
