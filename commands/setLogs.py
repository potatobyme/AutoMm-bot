import json
import discord
from discord import app_commands
from discord.ext import commands
from function import load_json, unauthorized, embed_color

class setLogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="setup-logs", description="Set the logs channels for middleman ticket")
    async def setuplogs(self, interaction: discord.Interaction, channel: discord.TextChannel):
        config = load_json()
        if interaction.user.id != config['buyer'] and interaction.user.id not in config['whitelist']:
            return await unauthorized(interaction)
        
        config['config']['logs']['channel'] = channel.id
        config['config']['logs']['status'] = "on"
        json.dump(config, open("config.json", 'w'), indent=4)
        embed = discord.Embed(
            title="`✅`・Logs Tickets",
            description=f"*The channel {channel.mention}`{channel.id}` are successfuly setup as **logs channel**.*",
            color=embed_color()
        )
        embed.set_footer(text=config['footer'])
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(setLogs(bot))