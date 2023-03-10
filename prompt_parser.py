
def parse_ez_negative(prompt):
    # This function parses too and from the ez negative format if it is used
    if "easy_negative" in prompt:
        # Parse from ez negative
        prompt = prompt.replace(
            "easy_negative", "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name")
    else:
        # Parse to ez negative
        prompt = prompt.replace(
            "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name", "easy_negative")
        
    return prompt

def ez_negative_long(prompt):
    if "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name" in prompt:
        return True
    else:
        return False
