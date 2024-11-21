import discord
from discord.ext import commands
from discord import app_commands
from function import *

class changeBlockcypherKey(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="change-api-key", description="Change the blockcypher api key")
    async def changeapikey(self, interaction: discord.Interaction, key: str):
        config = load_json()
        if interaction.user.id != config['buyer']:
            return await unauthorized(interaction)
        
        config['blockcypher'] = key
        json.dump(config, open("config.json", 'w'), indent=4)
        embed = discord.Embed(
            title="`✅`・BlockCypher Api Key",
            description=f"*Your new BlockCypher api key is `{key}`.*",
            color=embed_color()            
        )
        embed.set_footer(text=config['footer'])
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(changeBlockcypherKey(bot))