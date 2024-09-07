from enum import Enum

class RequestTypes(Enum):
    TXT2IMG = 'txt2img'
    IMG2IMG = 'img2img'
    PIX2PIX = 'pix2pix'
    UPSCALE = 'upscale'