# This python file takes in user values and sends them to the stable diffusion api. Then returns the resulting base64. 
import os
import requests
import base64
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv


async def txt2img(payload=None, enable_hr=False, denoising_strength=0, firstphase_width=0,
            firstphase_height=0, hr_scale=2, hr_upscaler="",
            hr_second_pass_steps=0, hr_resize_x=0, hr_resize_y=0, prompt="warning sign",
            styles=[], seed=-1, subseed=-1, subseed_strength=0,
            seed_resize_from_h=-1, seed_resize_from_w=-1, sampler_name="",
            batch_size=1, n_iter=1, steps=20, cfg_scale=7, width=512, height=512,
            restore_faces=False, tiling=False, negative_prompt="", eta=0,
            s_churn=0, s_tmax=0, s_tmin=0, s_noise=1, override_settings={},
            override_settings_restore_afterwards=True, script_args=[], sampler_index="Euler"):
    load_dotenv()
    URL = os.getenv('URL')

    # Define the request headers and body
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    # Body will include every valid parameter (Prompt is required!)
    if payload is None:
        payload = {
            "enable_hr": enable_hr,
            "denoising_strength": denoising_strength,
            "firstphase_width": firstphase_width,
            "firstphase_height": firstphase_height,
            "hr_scale": hr_scale,
            "hr_upscaler": hr_upscaler,
            "hr_second_pass_steps": hr_second_pass_steps,
            "hr_resize_x": hr_resize_x,
            "hr_resize_y": hr_resize_y,
            "prompt": prompt,
            "styles": styles,
            "seed": seed,
            "subseed": subseed,
            "subseed_strength": subseed_strength,
            "seed_resize_from_h": seed_resize_from_h,
            "seed_resize_from_w": seed_resize_from_w,
            "sampler_name": sampler_name,
            "batch_size": batch_size,
            "n_iter": n_iter,
            "steps": steps,
            "cfg_scale": cfg_scale,
            "width": width,
            "height": height,
            "restore_faces": restore_faces,
            "tiling": tiling,
            "negative_prompt": negative_prompt,
            "eta": eta,
            "s_churn": s_churn,
            "s_tmax": s_tmax,
            "s_tmin": s_tmin,
            "s_noise": s_noise,
            "override_settings": override_settings,
            "override_settings_restore_afterwards": override_settings_restore_afterwards,
            "script_args": script_args,
            "sampler_index": sampler_index
        }

    # Send the API request
    response = requests.post(URL, headers=headers, json=payload)

    return response


if __name__ == "__main__":
    print("Starting txt2img.py")
    response = txt2img()

    print("Decoding response")
    # Decode the base64-encoded image and save it to a file
    image_data = response.json()["images"][0]
    image_bytes = base64.b64decode(image_data)
    image = Image.open(BytesIO(image_bytes))
    image.save("temp.png")

    # Open the saved image using the default image viewer
    image.show()
