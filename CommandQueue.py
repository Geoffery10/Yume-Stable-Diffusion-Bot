import base64
import io
import json
import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
from datetime import datetime
from PIL import Image
from io import BytesIO

class CommandQueue:
    def __init__(self):
        self.queue = []

    def put(self, interaction, payload, type="txt2img"):
        print('Putting command in queue')
        if interaction.user.id not in self.queue:
            self.queue.append((interaction.user.id, interaction, payload, type))
            # Return the result of process_command
            return self.process_command(interaction, payload, type)
        else:
            print('User already in queue')
            interaction.followup.send('You already have a command in the queue!')

    def get_next_command(self):
        if len(self.queue) > 0:
            return self.queue.pop(0)
        else:
            return None

    async def process_command(self, interaction, payload, type):
        if 'txt2img' in type:
            from txt2img import txt2img
            response = await txt2img(payload=payload)
            # Send Image
            image = await parseImage(response)
            file = discord.File(io.BytesIO(image), filename="temp.png")

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
        # Check if sus otherwise continue
        if info['prompt'] == "(masterpiece), best quality, highres, absurdres, 1other, amongus <lora:amongUsLORAV1_v10:0.8>" and info['negative_prompt'] == "":
            # Send sus
            await sus_embed(interaction, payload, response, file, info)
        else:
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
            await interaction.followup.send(embed=embed, file=file)

        await store_image(response)



async def parseImage(response):
    # Get image from response
    image_data = response.json()["images"][0]
    image_bytes = base64.b64decode(image_data)
    return image_bytes

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


async def sus_embed(interaction, payload, response, file, info):
    # IF SUS THEN SEND ONLY IMAGE AND SEED
    # Send image on its own
    await interaction.followup.send(file=file)
    # Send seed as censored message
    await interaction.channel.send(f"||{info['seed']}||")
