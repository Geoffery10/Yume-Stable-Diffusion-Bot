# This python file takes in user values and sends them to the stable diffusion api. Then returns the resulting base64. 
import os
import requests
import base64
import discord
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
from datetime import datetime
import json
from file_management import store_image, parseImage
from models.ImageRequest import ImageRequest


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
    response = requests.post(URL, headers=headers, data=img_request.get_payload())

    return response


async def process_request(interaction, img_request: ImageRequest, type, defer=True):
    if 'txt2img' in type:
        response = await txt2img(img_request)
        if response.status_code != 200:
            await img_request.discord_interaction.followup.send(f"Error! AI Artist Failed to Respond!")
            return
        # Send Image
        image = await parseImage(response)
        file = discord.File(BytesIO(image), filename="temp.png")

    elif 'img2img' in type:
        # file = await img2img(payload=payload)
        # await interaction.followup.send(file=file)
        await interaction.followup.send('img2img is not yet implemented')
        return None

    # Create embed
    # Get current time
    now = datetime.now()
    info = json.loads(response.json()['info'])
    print(info)

    description = f"prompt: {info['prompt']}"
    if info['negative_prompt'] != "":
        description += f"\nnegative: {info['negative_prompt']}"
    embed = discord.Embed(color=6301830,
                            description=description, timestamp=now)
    embed.set_author(
        name=interaction.user.nick, icon_url=interaction.user.avatar, url="")
    embed.set_footer(
        text=f"seed:{info['seed']} • width:{info['width']} • height:{info['height']} • steps:{info['steps']} • cfg_scale:{info['cfg_scale']}")
    # Attach file to embed
    embed.set_image(url="attachment://temp.png")

    # Send embed
    if defer:
        await interaction.followup.send(embed=embed, file=file, view=txt2img_Buttons())
    else:
        await interaction.channel.send(embed=embed, file=file, view=txt2img_Buttons())

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
