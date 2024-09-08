import json
from random import randint
import time
from models.RequestTypes import RequestTypes

class ImageRequest:
    def __init__(self):
        self.prompt = "warning sign"
        self.negative_prompt = "fewer digits, extra digits"
        self.seed = -1
        self.enable_hr = False
        self.hr_scale = 2
        self.hr_upscaler = ""
        self.hr_second_pass_steps = 0
        self.hr_resize_x = 0
        self.hr_resize_y = 0
        self.styles = []
        self.batch_size = 1
        self.steps = 20
        self.cfg_scale = 7
        self.width = 816
        self.height = 1024
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
        if not "rating_safe" in self.prompt:
            self.prompt = "rating_safe, " + self.prompt
        if not "rating_explicit" in self.negative_prompt:
            self.negative_prompt = "rating_explicit, " + self.negative_prompt
            
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
        if not "score_9, score_8_up, score_7_up" in prompt:
            return "score_9, score_8_up, score_7_up, " + prompt
        else:
            return prompt
        
    def easy_negative(self, negative_prompt):
        if not "fewer digits, extra digits" in negative_prompt:
            return "fewer digits, extra digits, " + negative_prompt
        return negative_prompt