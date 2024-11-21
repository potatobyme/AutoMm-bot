import json
import discord
from discord.ui import Button
from function import *
from .walletModal import walletModal

class confirmDeal(Button):
    def __init__(self, filename, prvKey, amount):
        self.filename = filename
        self.prvKey = prvKey
        self.amount = amount
        super().__init__(
            style=discord.ButtonStyle.green,
            label="Confirm",
            emoji="✅"
        )
        
    async def callback(self, interaction: discord.Interaction):
        file = json.load(open(f"process/{self.filename}.json", 'r'))
        if interaction.user.id != file['sender']:
            return await interaction.response.send_message("You cannot confirm this deal because you are not the sender.", ephemeral=True)
            
        await interaction.response.send_modal(walletModal(self.prvKey, self.amount))