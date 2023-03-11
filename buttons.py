import random
import discord
from discord import ui
from random import randint
from embed_decode import decode
from sd_requests import sd_request


class TryAgain(discord.ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.green, label="Try again")

    async def callback(self, interaction: discord.Interaction):
        # Get the embed from the original message
        embed = interaction.message.embeds[0]

        # Convert embed to dict
        embed = embed.to_dict()

        # Log embed
        print('Embed: ')
        print(embed)

        # Parse the embed
        payload = await decode(embed)
        print('Payload: ')
        print(payload)

        # Acknowledge the interaction
        await interaction.response.defer()

        
        # Send request to stable diffusion
        await sd_request(interaction, payload, 'txt2img')


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

class UpscaleButton(discord.ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.blurple, label="Upscale")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("Soon this will upscale the image.", ephemeral=True)


class EditButton(discord.ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.secondary, label="Edit")

    async def callback(self, interaction: discord.Interaction):
        # Acknowledge the interaction
        # await interaction.response.defer()

        # Get the embed from the original message
        embed = interaction.message.embeds[0]

        # Convert embed to dict
        embed = embed.to_dict()

        # Log embed
        print('Embed: ')
        print(embed)

        # Parse the embed
        payload = await decode(embed)
        print('Payload: ')
        print(payload)

        # Open a modal to edit the prompt
        # Pass the payload to the EditModal constructor
        edit_modal = EditModal(payload=payload)
        await interaction.response.send_modal(edit_modal)


class EditModal(ui.Modal, title='Edit Prompt'):
    def __init__(self, payload, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.payload = payload
        # Set the default value for the prompt TextInput
        self.prompt.default = payload.get('prompt', '')
        # Set the default value for the answer TextInput
        self.negative_prompt.default = payload.get('negative_prompt', '')
        # Set the default value for the steps TextInput parse to string to prevent errors
        print(int(payload.get('steps', 20)))
        self.steps.default = str(int(payload.get('steps', 20)))
        # Set the default value for the width TextInput
        print(int(payload.get('width', 512)))
        self.width.default = str(int(payload.get('width', 512)))
        # Set the default value for the height TextInput
        print(int(payload.get('height', 640)))
        self.height.default = str(int(payload.get('height', 640)))


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
        prompt = self.prompt.value
        negative_prompt = self.negative_prompt.value

        # Update the payload with the new values
        self.payload['prompt'] = prompt
        self.payload['negative_prompt'] = negative_prompt
        # Parse the steps value to an integer
        steps = int(self.steps.value)
        # Update the payload with the new value
        self.payload['steps'] = steps
        # Parse the width value to an integer
        width = int(self.width.value)
        # Update the payload with the new value
        self.payload['width'] = width
        # Parse the height value to an integer
        height = int(self.height.value)
        # Update the payload with the new value
        self.payload['height'] = height

        # TODO: ADD CFG SCALE and SEED
        

        # Acknowledge the interaction
        await interaction.response.defer()

        # Send the request to stable diffusion
        await sd_request(interaction, self.payload, 'txt2img', defer=True)

    async def on_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message(f'An error occurred: {error}', ephemeral=True)
