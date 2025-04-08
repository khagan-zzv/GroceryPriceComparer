import os
import base64
from openai import OpenAI

client = OpenAI()

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def upload_file(file_path):
    file = client.files.create(
        file=open(file_path, "rb"),
        purpose="user_data"
    )
    return file


def prepare_input_for_openai(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext in [".jpg", ".jpeg", ".png"]:
        image_data = encode_image(file_path)
        return {
            "type": "input_image",
            "image_url": f"data:image/{ext[1:]};base64,{image_data}"
        }
    elif ext == ".pdf":
        file = upload_file(file_path)
        return {
            "type": "input_file",
            "file_id": file.id
        }
    else:
        raise ValueError("Unsupported file type. Only image and PDF files are supported.")
