import base64
import json
from PIL import Image
from io import BytesIO
import random


async def store_image(response):
    image_bytes = await decode_response(response)
    
    # Save image
    path = r'\\Hal-server\nas\ai\stable diffusion bot\output\\'
    info = json.loads(response.json()['info'])

    name = await generate_file_name(info)
    print("Saving image as: " + name)

    image = Image.open(BytesIO(image_bytes))
    image.save(path + name)

async def parseImage(response):
    # Get image from response
    image_data = response.json()["images"][0]
    image_bytes = base64.b64decode(image_data)
    return image_bytes

async def decode_response(response):
    image_data = response.json()["images"][0]
    return base64.b64decode(image_data)

async def generate_file_name(info):
    info['random_number'] = random.randint(0, 1000000)
    name = f"{info['seed']}-{info['random_number']}-{info['prompt']}-{info['negative_prompt']}.png"
    # Replace special characters
    chars_to_replace = [":", "/", "\\", "?", "*", "<", ">", "|", "\"", "'", "!", ";", "=", "+", "_", "&"]

    for char in chars_to_replace:
        name = name.replace(char, "-")
        
    # Check if file name is too long then trim it down and add png extension
    if len(name) > 255:
        name = name[:250] + ".png"
    return name

