import json
from typing import Any
import discord
from discord.ui import Button
from function import *
from .refundModal import refundModal

class refundButton(Button):
    def __init__(self, filename, amount, prvKey):
        self.filename = filename
        self.amount = amount
        self.prvKey = prvKey
        super().__init__(
            style=discord.ButtonStyle.red,
            label="Refund",
            emoji="⛔"
        )

    async def callback(self, interaction: discord.Interaction) -> Any:
        file = json.load(open(f"process/{self.filename}.json", 'r'))
        if interaction.user.id != file['sender']:
            return await interaction.response.send_message("You cannot refund your money yourself", ephemeral=True)
        
        await interaction.response.send_modal(refundModal(self.prvKey, self.amount))