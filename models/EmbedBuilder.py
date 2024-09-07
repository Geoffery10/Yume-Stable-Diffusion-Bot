from datetime import datetime
import math
import discord
from models.ImageRequest import ImageRequest


class EmbedBuilder:
    def __init__(self, img_request: ImageRequest, interaction: discord.interactions):
        self.img_request = img_request
        self.interaction = interaction
        self.description = self.build_description()
        self.footer = self.build_footer()
        self.now = datetime.now()
        self.embed_color = 6301830
        self.attachment_url = "attachment://temp.png"

    def get_embed(self):
        embed = discord.Embed(color=self.embed_color,
                                description=self.description)
        embed.set_author(name=self.interaction.user.nick, icon_url=self.interaction.user.avatar, url="")
        embed.set_footer(text=self.footer)
        embed.set_image(url=self.attachment_url)
        return embed
    
    def build_description(self):
        prompt = f"**prompt**: {self.img_request.prompt}"
        negative_prompt = ""
        if self.img_request.negative_prompt != "":
            negative_prompt = f"\n**negative**: {self.img_request.negative_prompt}"
        return prompt + negative_prompt
    
    def build_footer(self):
        footer = f"seed:{self.img_request.seed} • width:{self.img_request.width} • height:{self.img_request.height} • steps:{self.img_request.steps} • cfg_scale:{self.img_request.cfg_scale}"
        if not self.img_request.generation_time == None:
            footer += f" • {math.floor(self.img_request.generation_time)}s"
        return footer