import discord
from exceptiongroup import catch
from txt2img import process_request
from random import randint

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
        payload = await parse_embed(embed)
        print('Payload: ')
        print(payload)

        # Acknowledge the interaction
        await interaction.response.defer()

        
        # Send request to stable diffusion
        await process_request(interaction, payload, 'txt2img')


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


async def parse_embed(input_dict):
    # parse footer
    footer = input_dict["footer"]["text"]
    footer_values = {}
    for item in footer.split(" • "):
        key, value = item.split(":")
        footer_values[key.strip()] = float(value.strip())

    # parse description
    prompt_start = input_dict['description'].find("prompt:") + len("prompt:")
    prompt_end = input_dict['description'].find("negative:")
    prompt = input_dict['description'][prompt_start:prompt_end].strip()

    neg_prompt_start = input_dict['description'].find(
        "negative:") + len("negative:")
    negative_prompt = input_dict['description'][neg_prompt_start:].strip()

    # generate new seed
    footer_values["seed"] = randint(0, 2 ** 32 - 1)

    # create payload
    payload = {
        "enable_hr": False,
        "denoising_strength": 0,
        "firstphase_width": 0,
        "firstphase_height": 0,
        "hr_scale": 2,
        "hr_upscaler": "",
        "hr_second_pass_steps": 0,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "prompt": prompt,
        "styles": [],
        "seed": footer_values.get("seed", -1),
        "subseed": -1,
        "subseed_strength": 0,
        "seed_resize_from_h": -1,
        "seed_resize_from_w": -1,
        "sampler_name": "",
        "batch_size": 1,
        "n_iter": 1,
        "steps": footer_values.get("steps", 20),
        "cfg_scale": footer_values.get("cfg_scale", 7),
        "width": footer_values.get("width", 512),
        "height": footer_values.get("height", 512),
        "restore_faces": False,
        "tiling": False,
        "negative_prompt": negative_prompt,
        "eta": 0,
        "s_churn": 0,
        "s_tmax": 0,
        "s_tmin": 0,
        "s_noise": 1,
        "override_settings": {},
        "override_settings_restore_afterwards": True,
        "script_args": [],
        "sampler_index": "Euler"
    }

    return payload
