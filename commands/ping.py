import discord
from discord import app_commands 
from discord.ext import commands
from function import *

class ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Show bot latency")
    async def ping(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("pong !", ephemeral=True)            
    
async def setup(bot):
    await bot.add_cog(ping(bot))