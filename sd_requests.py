# This python file takes in a payload and sends it to the stable diffusion api on a new thread. The thread will then send an embed back to the interaction channel and close.
from prompt_parser import parse_ez_negative
from models.ImageRequest import ImageRequest
import txt2img

async def sd_request(interaction, img_request, type="txt2img", defer=True):
    # Start a new thread to send the request
    if type == "txt2img":
        await txt2img.process_request(interaction=interaction, img_request=img_request, type=type, defer=defer)
    elif type == "img2img":
        await interaction.followup.send('img2img is not yet implemented')
    elif type == "pix2pix":
        await interaction.followup.send('pix2pix is not yet implemented')
    elif type == "upscale":
        await interaction.followup.send('upscale is not yet implemented')
    else:
        await interaction.followup.send('Invalid type')
