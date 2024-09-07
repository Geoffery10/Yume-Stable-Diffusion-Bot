import random
import discord
from discord import ui
from random import randint
from embed_decode import decode
from sd_requests import sd_request
from models.ImageRequest import ImageRequest
from models.RequestTypes import RequestTypes

class TryAgain(discord.ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.green, label="Try again")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        # Get the embed from the original message
        embed = interaction.message.embeds[0]

        # Convert embed to dict
        embed = embed.to_dict()

        # Log embed
        print('Embed: ')
        print(embed)

        # Parse the embed
        img_request = await decode(embed)
        img_request.set_request_type(RequestTypes.TXT2IMG)
        print('Payload: ')
        print(img_request.get_payload())

        
        # Send request to stable diffusion
        await sd_request(interaction, img_request)
        # Respond to the interaction with nothing incase it fails
        try:
            await interaction.response.send_message("")
        except:
            pass


class DeleteButton(discord.ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.danger, label="Delete")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        try:
            # Get the embed from the original message
            embed = interaction.message.embeds[0]

            # Delete the original message
            await interaction.message.delete()

            # remove the image from the embed
            embed.set_image(url="")

            # add a new field to the embed saying that the image has been deleted
            embed.add_field(name="Image deleted", value="This image has been deleted. Restoring is not yet possible.")

            # Send the embed
            await interaction.followup.send(embed=embed)
        except Exception as e:
            print(e)
            await interaction.followup.send("Something went wrong while deleting the image. Please try again later.", ephemeral=True)
        
        try:
            await interaction.response.send_message("")
        except:
            pass


class UpscaleButton(discord.ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.blurple, label="Upscale")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("Soon this will upscale the image.", ephemeral=True)
        try:
            await interaction.response.send_message("")
        except:
            pass


class EditButton(discord.ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.secondary, label="Edit")

    async def callback(self, interaction: discord.Interaction):
        # Get the embed from the original message
        embed = interaction.message.embeds[0]

        # Convert embed to dict
        embed = embed.to_dict()

        # Log embed
        print('Embed: ')
        print(embed)

        # Parse the embed
        img_request = await decode(embed)
        print('Payload: ')
        print(img_request.get_payload())

        # Open a modal to edit the prompt
        # Pass the payload to the EditModal constructor
        edit_modal = EditModal(img_request)
        await interaction.response.send_modal(edit_modal)

        try:
            await interaction.response.send_message("")
        except:
            pass


class EditModal(ui.Modal, title='Edit Prompt'):
    def __init__(self, img_request: ImageRequest, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.img_request = img_request
        self.prompt.default = img_request.prompt
        self.negative_prompt.default = img_request.negative_prompt
        self.steps.default = str(int(img_request.steps))
        self.width.default = str(int(img_request.width))
        self.height.default = str(int(img_request.height))


    prompt = ui.TextInput(label='Prompt',
                          style=discord.TextStyle.paragraph,
                          placeholder='Enter your prompt here',
                          min_length=1,
                          max_length=2000,
                          required=True)
    negative_prompt = ui.TextInput(label='Negative Prompt',
                                    style=discord.TextStyle.paragraph,
                                    placeholder='Enter your negative prompt here',
                                    min_length=0,
                                    max_length=2000,
                                    required=False)
    # Steps integer input 
    steps = ui.TextInput(label='Steps',
                         style=discord.TextStyle.short,
                            placeholder='Enter the number of steps',
                            min_length=1,
                            max_length=2,
                            required=True)
    # width integer input
    width = ui.TextInput(label='Width',
                            style=discord.TextStyle.short,
                            placeholder='Enter the width of the image',
                            min_length=1,
                            max_length=4,
                            required=True)
    # height integer input
    height = ui.TextInput(label='Height',
                            style=discord.TextStyle.short,
                            placeholder='Enter the height of the image',
                            min_length=1,
                            max_length=4,
                            required=True)
    


    async def on_submit(self, interaction: discord.Interaction):
        # Get the values from the text inputs
        
        img_request = ImageRequest()
        img_request.set_prompt(str(self.prompt.value))
        img_request.set_negative_prompt(str(self.negative_prompt.value))
        img_request.set_steps(int(self.steps.value))
        img_request.set_width(int(self.width.value))
        img_request.set_height(int(self.height.value))
        img_request.set_request_type(RequestTypes.TXT2IMG)
        img_request.set_seed(-1)
        
        # Acknowledge the interaction
        try:
            await interaction.response.defer()
        except:
            pass

        # Send the request to stable diffusion
        await sd_request(interaction, img_request, defer=True)

    async def on_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message(f'An error occurred: {error}', ephemeral=True)
