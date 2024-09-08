import discord
import buttons


class EmbedButtons(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(buttons.TryAgain())
        self.add_item(buttons.EditButton())
        self.add_item(buttons.DeleteButton())
        self.add_item(buttons.UpscaleButton())
