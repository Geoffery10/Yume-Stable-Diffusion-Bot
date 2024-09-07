import json
import discord
from discord import app_commands
from dotenv import load_dotenv
from loggingChannel import sendLog
import os
from models.ImageRequest import ImageRequest
from models.RequestTypes import RequestTypes
from styles import styles
from sd_requests import sd_request

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


intents = discord.Intents(messages=True, guilds=True, guild_messages=True,
                          guild_reactions=True, members=True, reactions=True, presences=True)
intents.message_content = True
intents.reactions = True


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        # Get the guild object
        guild_ids = [786690956514426910,
                     254779349352448001, 885595844999532624]

        for guild_id in guild_ids:
            print(f"Syncing trees for guild {guild_id}")
            await tree.sync(guild=client.get_guild(guild_id))
        print("Synced trees")

        # Loaded
        print(await sendLog(log=(f'{client.user} has connected to Discord!'), client=client))
        await updateStatus()

    async def on_message(self, message):
        if message.author == client.user:
            return

        # Update Status
        await updateStatus()

        # Log message
        print(
            f'{message.author.name} [{message.author.id}] sent: {message.content} on Channel: {message.channel.id}')


async def updateStatus():
    global streamers
    with open('status.json') as fs:
        data = json.load(fs)
    await client.change_presence(
        activity=await activityType(data))


async def activityType(data):
    if data["activity"]["type"] == "PLAYING":
        return discord.Activity(type=discord.Game(data["activity"]["name"]))
    elif data["activity"]["type"] == "STREAMING":
        return discord.Activity(activity=discord.Streaming(name=data["activity"]["name"], url=data["activity"]["url"]))
    elif data["activity"]["type"] == "WATCHING":
        return discord.Activity(type=discord.ActivityType.watching, name=data["activity"]["name"])
    elif data["activity"]["type"] == "LISTENING":
        return discord.Activity(type=discord.ActivityType.listening, name=data["activity"]["name"])


client = MyClient(intents=intents)
tree = app_commands.CommandTree(client)
myid = '<@1043957906921492562>'


# ================================== #
#           Slash Commands           #
# ================================== #
# Command: /dream
# Description: Dream of an Image
# This should have most of the payload options
# ================================== #
@tree.command(description="Dream of an Image")
async def dream(interaction: discord.Interaction, prompt: str, negative: str = "", steps: int = 20, 
                seed: int = -1, cfg_scale: int = 7, width: int = 816, height: int = 1024):
    # Dream
    print(await sendLog(log=f'{interaction.user.name} dreaming of {prompt}', client=client))
    img_request = ImageRequest()

    # Acknowledge the interaction
    try:
        await interaction.response.defer()
    except Exception as e:
        print(await sendLog(log=e))        

    img_request.set_prompt(prompt)
    img_request.set_negative_prompt(negative)
    img_request.set_steps(steps)
    img_request.set_seed(seed)
    img_request.set_cfg_scale(cfg_scale)
    img_request.set_width(width)
    img_request.set_height(height)
    img_request.set_request_type(RequestTypes.TXT2IMG)
    
    if not interaction.channel.is_nsfw():
        img_request.set_not_nsfw()

    
    # Add the command to the queue
    await sd_request(interaction, img_request, defer=True)



# Get the TOKEN variable from the environment
client.run(TOKEN)
