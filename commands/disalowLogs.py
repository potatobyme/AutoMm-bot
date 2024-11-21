import json
import discord
from discord import app_commands
from discord.ext import commands
from function import load_json, unauthorized, embed_color

class disableLogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="disable-logs", description="Disable logs off middleman tickets")
    async def disablelogs(self, interaction: discord.Interaction):
        config = load_json()
        if interaction.user.id != config['buyer'] and interaction.user.id not in config['whitelist']:
            return await unauthorized(interaction)
        
        config['config']['logs']['channel'] = None
        config['config']['logs']['status'] = "off"
        json.dump(config, open("config.json", 'w'), indent=4)
        embed = discord.Embed(
            title="`✅`・Logs Tickets",
            description=f"*Logs off ticket for middleman are disabled*",
            color=embed_color()
        )
        embed.set_footer(text=config['footer'])
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(disableLogs(bot))