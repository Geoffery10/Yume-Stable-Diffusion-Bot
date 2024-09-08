# This python file takes in user values and sends them to the stable diffusion api. Then returns the resulting base64. 
import os
import time
import requests
import base64
import discord
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import json
from file_management import store_image, parseImage
from models.EmbedBuilder import EmbedBuilder
from models.ImageRequest import ImageRequest
from models.RequestTypes import RequestTypes


async def txt2img(img_request=None):
    load_dotenv()
    URL = os.getenv('URL')

    # Define the request headers and body
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    
    if img_request == None:
        img_request = ImageRequest()
        
    # Send the API request
    print("Sending API Request")
    start_time = time.time()
    response = requests.post(URL, headers=headers, data=img_request.get_payload())
    end_time = time.time()
    img_request.set_generation_time((end_time - start_time))

    return response, img_request


async def process_request(interaction, img_request: ImageRequest, defer=True):
    if img_request.request_type == RequestTypes.TXT2IMG:
        response, img_request = await txt2img(img_request)
        if response.status_code != 200:
            await interaction.followup.send(f"Error! AI Artist Failed to Respond!")
            return
        # Send Image
        image = await parseImage(response)
        file = discord.File(BytesIO(image), filename="temp.png")

    elif img_request.request_type == RequestTypes.IMG2IMG:
        # file = await img2img(payload=payload)
        # await interaction.followup.send(file=file)
        await interaction.followup.send('img2img is not yet implemented')
        return None

    # Create embed
    info = json.loads(response.json()['info'])
    print(info)

    embed = EmbedBuilder(img_request, interaction)

    # Send embed
    if defer:
        await interaction.followup.send(embed=embed.get_embed(), file=file, view=txt2img_Buttons())
    else:
        await interaction.channel.send(embed=embed.get_embed(), file=file, view=txt2img_Buttons())

    await store_image(response)


class txt2img_Buttons(discord.ui.View):
    def __init__(self):
        super().__init__()
        import buttons
        self.add_item(buttons.TryAgain())
        self.add_item(buttons.EditButton())
        self.add_item(buttons.DeleteButton())
        self.add_item(buttons.UpscaleButton())
        


if __name__ == "__main__":
    print("Starting txt2img.py")
    import asyncio
    async def main():
        response = await txt2img()

        if response.status_code == 200:
            print("Decoding response")
            # Decode the base64-encoded image and save it to a file
            image_data = response.json()["images"][0]
            image_bytes = base64.b64decode(image_data)
            image = Image.open(BytesIO(image_bytes))
            image.save("temp.png")

            # Open the saved image using the default image viewer
            image.show()
        else:
            print(f'Error: response code {response.status_code}')
        
    asyncio.run(main())
