import base64
import json
from PIL import Image
from io import BytesIO


async def store_image(response):
    # Get image from response
    image_data = response.json()["images"][0]
    image_bytes = base64.b64decode(image_data)
    # Save image
    path = r'\\Hal-server\nas\ai\stable diffusion bot\output\\'
    # name = seed-random_number-prompt-negative-prompt.png
    # File name must be unique and not contain any special characters or be longer than 255 characters
    info = json.loads(response.json()['info'])
    # generate a random number
    import random
    info['random_number'] = random.randint(0, 1000000)
    name = f"{info['seed']}-{info['random_number']}-{info['prompt']}-{info['negative_prompt']}.png"
    # Replace special characters
    chars_to_replace = [":", "/", "\\", "?", "*", "<", ">", "|", "\"", "'", "!", ";", "=", "+", "_", "&"]

    for char in chars_to_replace:
        name = name.replace(char, "-")

    print("Saving image as: " + name)

    # Check if file name is too long then trim it down and add png extension
    if len(name) > 255:
        name = name[:250] + ".png"
    image = Image.open(BytesIO(image_bytes))
    image.save(path + name)

async def parseImage(response):
    # Get image from response
    image_data = response.json()["images"][0]
    image_bytes = base64.b64decode(image_data)
    return image_bytes
