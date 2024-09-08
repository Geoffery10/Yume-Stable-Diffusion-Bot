import base64


async def parseImage(response):
    # Get image from response
    image_data = response.json()["images"][0]
    image_bytes = base64.b64decode(image_data)
    return image_bytes


async def decode_response(response):
    image_data = response.json()["images"][0]
    return base64.b64decode(image_data)
