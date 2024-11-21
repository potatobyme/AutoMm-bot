import discord
from discord.ui import Button
from function import unauthorized
from .addUserModal import addUserModal

class addUserButton(Button):
    def __init__(self, userId, filename):
        self.userId = userId
        self.filename = filename
        super().__init__(
            style=discord.ButtonStyle.green,
            label="Add User",
            emoji="🔎"
        )
        
    async def callback(self, interaction):
        if interaction.user.id != self.userId:
            return await unauthorized(interaction)
        
        await interaction.response.send_modal(addUserModal(self.userId, self.filename))