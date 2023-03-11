# This python file takes in a payload and sends it to the stable diffusion api on a new thread. The thread will then send an embed back to the interaction channel and close.
from prompt_parser import parse_ez_negative
import txt2img

async def sd_request(interaction, payload, type="txt2img", defer=True):
    # Parse the payload
    payload = await keyword_decode(payload, interaction)
    # Validate the payload
    payload, valid = await validate_payload(payload)

    if valid:
        # Start a new thread to send the request
        if type == "txt2img":
            await txt2img.process_request(interaction=interaction, payload=payload, type=type, defer=defer)
        elif type == "img2img":
            await interaction.followup.send('img2img is not yet implemented')
        elif type == "pix2pix":
            await interaction.followup.send('pix2pix is not yet implemented')
        elif type == "upscale":
            await interaction.followup.send('upscale is not yet implemented')
        else:
            await interaction.followup.send('Invalid type')
    else:
        await interaction.followup.send('Invalid payload')
    return


async def parse_payload(enable_hr=False, denoising_strength=0, firstphase_width=0,
                    firstphase_height=0, hr_scale=2, hr_upscaler="",
                    hr_second_pass_steps=0, hr_resize_x=0, hr_resize_y=0, prompt="warning sign",
                    styles=[], seed=-1, subseed=-1, subseed_strength=0,
                    seed_resize_from_h=-1, seed_resize_from_w=-1, sampler_name="",
                    batch_size=1, n_iter=1, steps=20, cfg_scale=7, width=512, height=512,
                    restore_faces=False, tiling=False, negative_prompt="", eta=0,
                    s_churn=0, s_tmax=0, s_tmin=0, s_noise=1, override_settings={},
                    override_settings_restore_afterwards=True, script_args=[], sampler_index="Euler"):
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

    return payload

async def keyword_decode(payload, interaction):
    if "easy_negative" in payload['negative_prompt']:
        payload['negative_prompt'] = parse_ez_negative(payload['negative_prompt'])

    # Check if channel is not nsfw
    if interaction.channel.is_nsfw() == False:
        # NSFW to the beginning of negative_prompt if it is not already
        if "nsfw" not in payload['negative_prompt']:
            payload['negative_prompt'] = "nsfw, " + payload['negative_prompt']

    return payload

async def validate_payload(payload):
    # Check for empty payload 
    if payload == {}:
        return payload, False
    
    print(payload)
    
    # Check bad values
    if payload['width'] < 1:
        payload['width'] = 512
    if payload['width'] > 1024:
        payload['width'] = 512
    if payload['height'] < 1:
        payload['height'] = 512
    if payload['height'] > 1024:
        payload['height'] = 512
    if payload['steps'] < 1:
        payload['steps'] = 20
    if payload['steps'] > 80:
        payload['steps'] = 80
    if payload['cfg_scale'] < 1:
        payload['cfg_scale'] = 7
    if payload['prompt'] == "":
        payload['prompt'] = "warning sign"

    return payload, True
    