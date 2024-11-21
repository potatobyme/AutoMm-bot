import json
import discord
from discord import app_commands
from discord.ext import commands
from function import load_json, embed_color, unauthorized

class wl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="whitelist-add", description="Add an user into the whitelist")
    async def whitelistAdd(self, interaction: discord.Interaction, member: discord.Member):
        config = load_json()
        if interaction.user.id != config['buyer']:
            return await unauthorized(interaction)

        whitelist = config['whitelist']

        if member.id in whitelist:
            embed = discord.Embed(
                title="`🔎`・Whitelist",
                description=f"*Member {member.mention}`{member.id}` is already into the whitelist.*",
                color=embed_color()
            )
            embed.set_footer(text=config['footer'])
            return await interaction.response.send_message(embed=embed)
        
        whitelist.append(member.id)
        json.dump(config, open("config.json", 'w'), indent=4)
        embed = discord.Embed(
            title="`✅`・Whitelist",
            description=f"*Member {member.mention}`{member.id}` successfuly added into the whitelist.*",
            color=embed_color()
        )
        embed.set_footer(text=config['footer'])
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(wl(bot))