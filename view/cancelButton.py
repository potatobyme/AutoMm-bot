import os
import asyncio
import discord
from discord.ui import Button
from function import unauthorized
from function import *

class cancelButton(Button):
    def __init__(self, userId, filename):
        self.userId = userId
        self.filename = filename
        super().__init__(
            style=discord.ButtonStyle.red,
            label="Cancel",
            emoji="❌"
        )
        
    async def callback(self, interaction):
        if interaction.user.id != self.userId:
            return await unauthorized(interaction)
        os.remove(f"process/{self.filename}.json")
        await interaction.response.send_message("Ticket will be delete in 5 seconds", ephemeral=True)
        await asyncio.sleep(5)
        await interaction.channel.delete()
        config = load_json()
        logsConfig = config['config']['logs']
        if logsConfig['status'] == "on":
            if logsConfig['channel'] != None:
                logsChannel = discord.utils.get(interaction.guild.channels, id=logsConfig['channel'])
                if logsChannel:
                    embed = discord.Embed(
                        title="`👑`・Middleman Ticket Deleted",
                        description=f"***Ticket Deleted by user ({interaction.user.mention})***",
                        color=embed_color()
                    )
                    await logsChannel.send(embed=embed)