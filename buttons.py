import discord
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


class EditButton(discord.ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.secondary, label="Edit")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("Soon this will open a menu to let you edit your prompt.", ephemeral=True)

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
