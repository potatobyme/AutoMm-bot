import discord
from discord.ext import commands

class MessageCreate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.user.mention in message.content:
            await message.reply("Hey, you can use me using slash commands, try /help !")

async def setup(bot):
    await bot.add_cog(MessageCreate(bot))