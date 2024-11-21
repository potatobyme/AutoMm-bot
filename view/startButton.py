import discord
from discord.ui import Button
from .startModal import startModal

class startButton(Button):
    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__(
            style=discord.ButtonStyle.blurple,
            label="Start MiddleMan",
            emoji="⭐"
        )
    
    async def callback(self, interaction) -> None:
        return await interaction.response.send_modal(startModal(interaction.user.id, self.bot))        