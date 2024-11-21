import discord
from discord import app_commands
from discord.ext import commands
from function import *

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Show help command")
    async def helpcommand(self, interaction: discord.Interaction):
        config = load_json()
        embed = discord.Embed(
            title="Help command",
            color=embed_color()
        )
        embed.set_footer(text=config['footer'])
        embed.add_field(name="`/change-api-key`", value="*Change BlockCypher api token / key used for middleMan tickets*", inline=False)
        embed.add_field(name="`/disable-logs`", value="*Disable logs of middleMan Tickets*", inline=False)
        embed.add_field(name="`/help`", value="*Show this embed*", inline=False)
        embed.add_field(name="`/middleman-embed`", value="*Send embed to start middleMan Ticket*", inline=False)
        embed.add_field(name="`/ping`", value="*Reply with pong !*", inline=False)
        embed.add_field(name="`setup-category`", value="*Setup category where ticket are opened*", inline=False)
        embed.add_field(name="`/setup-logs`", value="*Setup logs channels of middleMan Tickets*", inline=False)
        embed.add_field(name="`/whitelist-remove`", value="*Remove a member from the whitelist*", inline=False)
        embed.add_field(name="`/whitelist-add`", value="*Add a member into the whitelist*", inline=False)
        embed.add_field(name="`/whitelist-list`", value="*Show all member in the whitelist*", inline=False)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpCommand(bot))