import discord
from os import listdir
from function import load_json
from discord.ext import commands

async def load_commands(bot) -> None:
    commands_files = [f'commands.{file[:-3]}' for file in listdir('./commands/') if file.endswith(".py")]
    events_files = [f'events.{file[:-3]}' for file in listdir('./events/') if file.endswith(".py")]
    
    for file in commands_files:
        try:
            await bot.load_extension(file)
        except Exception as e:
            print(e)
            
    for file in events_files:
        try:
            await bot.load_extension(file)
        except Exception as e:
            print(e)
            
class MyBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix="discord.gg/purity-dev",
            intents=discord.Intents.all(),
            help_command=None
        )
        
    async def on_ready(self) -> None:
        await load_commands(self)
        await self.tree.sync()
        
        print(f"Logged as {self.user.name}")
        
if __name__ == "__main__":
    config = load_json()
    PurityMm = MyBot()
    PurityMm.run(config['token'])