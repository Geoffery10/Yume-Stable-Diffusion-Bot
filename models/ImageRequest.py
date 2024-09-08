import json
from random import randint
import time
from models.RequestTypes import RequestTypes


class ImageRequest:
    def __init__(self, prompt: str = "warning sign",
                 negative_prompt: str = "fewer digits, extra digits, score_6, score_5, score_4",
                 width: int = 816,
                 height: int = 1024,
                 seed: int = -1,
                 steps: int = 20,
                 cfg_scale: float = 7):
        self.good_qualities = "score_9, score_8_up, score_7_up"
        self.bad_qualities = "fewer digits, extra digits, score_6, score_5, score_4"
        self.sfw_prompt = "rating_safe"
        self.sfw_negative = "rating_explicit"

        self.set_prompt(prompt)
        self.set_negative_prompt(negative_prompt)
        self.set_width(width)
        self.set_height(height)
        self.set_seed(seed)
        self.set_steps(steps)
        self.set_cfg_scale(cfg_scale)
        self.enable_hr = False
        self.hr_scale = 2
        self.hr_upscaler = ""
        self.hr_second_pass_steps = 0
        self.hr_resize_x = 0
        self.hr_resize_y = 0
        self.styles = []
        self.batch_size = 1
        self.restore_faces = False
        self.tiling = False
        self.eta = 0
        self.sampler_index = "DPM++ 2M"
        self.comments = {}
        self.send_images = True
        self.save_images = True
        self.disable_extra_networks = False
        self.request_type = RequestTypes.TXT2IMG
        self.generation_time = None

    def set_prompt(self, prompt: str):
        prompt = self.easy_positive(prompt)
        if prompt == "":
            self.prompt = "warning sign"
        else:
            self.prompt = prompt

    def set_negative_prompt(self, negative_prompt: str):
        negative_prompt = self.easy_negative(negative_prompt)
        self.negative_prompt = negative_prompt

    def set_width(self, width: int):
        self.width = self.dimension_clamp(width)

    def set_height(self, height: int):
        self.height = self.dimension_clamp(height)

    def set_steps(self, steps: int):
        if steps < 1:
            self.steps = 20
        elif steps > 40:
            self.steps = 40
        else:
            self.steps = steps

    def set_cfg_scale(self, cfg_scale: float):
        if cfg_scale < 1:
            self.cfg_scale = 7
        else:
            self.cfg_scale = cfg_scale

    def set_seed(self, seed: int):
        if seed < 1 or seed == -1:
            self.seed = randint(1, 10000000000)
        else:
            self.seed = seed

    def set_not_nsfw(self):
        if not self.sfw_prompt in self.prompt:
            self.prompt = f"{self.sfw_prompt}, " + self.prompt
        if not self.sfw_negative in self.negative_prompt:
            self.negative_prompt = f"{self.sfw_negative}, " + \
                self.negative_prompt

    def set_request_type(self, type: RequestTypes):
        self.request_type = type

    def set_generation_time(self, time: time):
        self.generation_time = time

    def get_payload(self) -> str:
        data = {
            'prompt': self.prompt,
            'negative_prompt': self.negative_prompt,
            'seed': self.seed,
            'batch_size': self.batch_size,
            'steps': self.steps,
            'cfg_scale': self.cfg_scale,
            'width': self.width,
            'height': self.height,
            'restore_faces': self.restore_faces,
            'tiling': self.tiling,
            'eta': self.eta,
            'comments': self.comments,
            'enable_hr': self.enable_hr,
            'sampler_index': self.sampler_index,
            'send_images': self.send_images,
            'save_images': self.save_images,
            'disable_extra_networks': self.disable_extra_networks
        }
        return json.dumps(data)

    def dimension_clamp(self, dimension):
        if dimension < 1:
            return 512
        elif dimension > 1024:
            return 1024
        else:
            return dimension

    def easy_positive(self, prompt):
        if not self.good_qualities in prompt:
            return f"{self.good_qualities}, " + prompt
        else:
            return prompt

    def easy_negative(self, negative_prompt):
        if not self.bad_qualities in negative_prompt:
            return f"{self.bad_qualities}, " + negative_prompt
        return negative_prompt

    def get_prompt_without_qualities(self):
        cleaned_prompt = self.prompt
        if self.good_qualities in self.prompt:
            cleaned_prompt = cleaned_prompt.replace(
                f"{self.good_qualities}, ", "")

        return cleaned_prompt

    def get_negative_without_qualities(self):
        cleaned_prompt = self.negative_prompt
        if self.bad_qualities in self.negative_prompt:
            cleaned_prompt = cleaned_prompt.replace(
                f"{self.bad_qualities}, ", "")

        return cleaned_prompt
