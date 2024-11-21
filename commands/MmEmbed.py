import discord
from function import *
from discord import app_commands
from discord.ext import commands
from view.startButton import startButton
from function import unauthorized

class MiddleManEmbed(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        
    @app_commands.command(name="middleman-embed", description="Send MiddleMan Panel")
    async def mmembed(self, interaction: discord.Interaction) -> None:
        config = load_json()
        if interaction.user.id not in config['whitelist'] and interaction.user.id != config['buyer']:
            return await unauthorized(interaction)
        embed = discord.Embed(
            title="`🏆`・MiddleMan Bot",
            description=f"Je sais pas sah laisse moi dev",
            color=embed_color()
        )
        view = discord.ui.View(timeout=None)
        view.add_item(startButton(self.bot))
        await interaction.response.send_message(embed=embed, view=view)
        
async def setup(bot) -> None:
    await bot.add_cog(MiddleManEmbed(bot))