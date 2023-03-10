import discord
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


class RedButton(discord.ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.red, label="Red button")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("You pressed the red button!")


async def parse_embed(input_dict):
    # parse footer
    footer = input_dict["footer"]["text"]
    footer_values = {}
    for item in footer.split(" • "):
        key, value = item.split(":")
        footer_values[key.strip()] = float(value.strip())

    # parse description
    description = input_dict["description"]
    prompt = ""
    negative_prompt = ""
    for item in description.split("\n"):
        if "prompt:" in item:
            prompt = item.split(":")[1].strip()
        elif "negative:" in item:
            negative_prompt = item.split(":")[1].strip()

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
