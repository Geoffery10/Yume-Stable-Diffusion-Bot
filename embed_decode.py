# This python code decodes discord sd_embeds and returns them as a payload for the stable diffusion api.

from random import randint
from prompt_parser import parse_ez_negative
from models.ImageRequest import ImageRequest


async def decode(input_dict):
    footer_values = await extract_footer(input_dict)

    # parse description
    prompt, negative_prompt = await extract_prompt(input_dict)

    # parse ez negative
    if "easy_negative" in prompt:
        prompt = parse_ez_negative(prompt)

    # generate new seed
    footer_values["seed"] = randint(0, 2 ** 32 - 1)

    # create payload
    img_request = ImageRequest()
    
    img_request.set_prompt(prompt)
    img_request.set_negative_prompt(negative_prompt)
    img_request.set_steps(footer_values.get("steps", 20))
    img_request.set_seed(footer_values.get("seed", -1))
    img_request.set_cfg(footer_values.get("cfg_scale", 7))
    img_request.set_width(footer_values.get("width", 512))
    img_request.set_height(footer_values.get("height", 512))

    return img_request

async def extract_footer(input_dict):
    footer = input_dict["footer"]["text"]
    footer_values = {}
    for item in footer.split(" • "):
        key, value = item.split(":")
        footer_values[key.strip()] = float(value.strip())
    return footer_values

async def extract_prompt(input_dict):
    prompt_start = input_dict['description'].find("**prompt**:") + len("**prompt**:")
    prompt_end = input_dict['description'].find("**negative**:")
    prompt = input_dict['description'][prompt_start:prompt_end].strip()

    neg_prompt_start = input_dict['description'].find(
        "**negative**:") + len("**negative**:")
    negative_prompt = input_dict['description'][neg_prompt_start:].strip()
    return prompt,negative_prompt
