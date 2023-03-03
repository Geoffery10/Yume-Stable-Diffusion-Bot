import base64
import io
import json
import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
from datetime import datetime

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

async def parseImage(response):
    # Get image from response
    image_data = response.json()["images"][0]
    image_bytes = base64.b64decode(image_data)
    return image_bytes
