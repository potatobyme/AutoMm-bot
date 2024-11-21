import json
import discord
from discord import app_commands
from discord.ext import commands
from function import *

class setCategory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setup-category", description="Set the category where ticket need to be opened")
    async def setcategory(self, interaction: discord.Interaction, category: discord.CategoryChannel):
        config = load_json()
        if interaction.user.id != config['buyer'] and interaction.user.id not in config['whitelist']:
            return await unauthorized(interaction)
        
        config['config']['tickets']['category'] = category.id
        json.dump(config, open("config.json", 'w'), indent=4)
        embed = discord.Embed(
            title="`✅`・Ticket Category",
            description=f"*The category **{category.name}** was set as category where ticket middleMan are opened*",
            color=embed_color()
        )
        embed.set_footer(text=config['footer'])
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(setCategory(bot))