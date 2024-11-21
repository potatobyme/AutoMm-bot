import json
import discord
from discord import app_commands
from discord.ext import commands
from function import load_json, embed_color, unauthorized

class wllist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="whitelist-list", description="Show all members into the whitelist")
    async def whitelistlist(self, interaction: discord.Interaction):
        config = load_json()
        if interaction.user.id != config['buyer']:
            return await unauthorized(interaction)
        
        whitelist = config['whitelist']
        joined = '\n'.join(f'<@{memberId}>`{memberId}`' for memberId in whitelist)
        embed = discord.Embed(
            title="`✨`・Whitelist",
            description=joined,
            color=embed_color()
        )
        embed.set_footer(text=config['footer'])
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(wllist(bot))