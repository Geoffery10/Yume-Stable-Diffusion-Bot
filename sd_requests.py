# This python file takes in a payload and sends it to the stable diffusion api on a new thread. The thread will then send an embed back to the interaction channel and close.
import txt2img
from models.ImageRequest import ImageRequest
from models.RequestTypes import RequestTypes

async def sd_request(interaction, img_request: ImageRequest, defer=True):
    # Start a new thread to send the request
    if img_request.request_type == RequestTypes.TXT2IMG:
        await txt2img.process_request(interaction=interaction, img_request=img_request, defer=defer)
    elif img_request.request_type == RequestTypes.IMG2IMG:
        await interaction.followup.send('img2img is not yet implemented')
    elif img_request.request_type == RequestTypes.PIX2PIX:
        await interaction.followup.send('pix2pix is not yet implemented')
    elif img_request.request_type == RequestTypes.UPSCALE:
        await interaction.followup.send('upscale is not yet implemented')
    else:
        await interaction.followup.send('Invalid type')
