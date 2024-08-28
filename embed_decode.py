# This python code decodes discord sd_embeds and returns them as a payload for the stable diffusion api.

from random import randint
from prompt_parser import parse_ez_negative


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

async def extract_footer(input_dict):
    footer = input_dict["footer"]["text"]
    footer_values = {}
    for item in footer.split(" • "):
        key, value = item.split(":")
        footer_values[key.strip()] = float(value.strip())
    return footer_values

async def extract_prompt(input_dict):
    prompt_start = input_dict['description'].find("prompt:") + len("prompt:")
    prompt_end = input_dict['description'].find("negative:")
    prompt = input_dict['description'][prompt_start:prompt_end].strip()

    neg_prompt_start = input_dict['description'].find(
        "negative:") + len("negative:")
    negative_prompt = input_dict['description'][neg_prompt_start:].strip()
    return prompt,negative_prompt
