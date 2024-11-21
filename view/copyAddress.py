import json
import discord
from discord.ui import Button
from function import *

class copyAddress(Button):
    def __init__(self, address, filename):
        self.address = address
        self.filename = filename
        super().__init__(
            style=discord.ButtonStyle.blurple,
            label="Copy Address",
            emoji="🧾"
        )
        
    async def callback(self, interaction: discord.Interaction):
        config = load_json()
        file = json.load(open(f'process/{self.filename}.json', 'r'))
        if interaction.user.id != file['sender']:
            return await interaction.response.send_message("Only the sender can copy this litecoin address", ephemeral=True)
        
        await interaction.response.send_message(content=self.address, ephemeral=True)
        