import discord
from os import listdir
from function import load_json
from discord.ext import commands
import requests
import hashlib
import os

# Configuration for license verification
SERVER_URL = "http://204.10.194.198:8000/verify"

def get_hwid():
    """
    Generates a unique HWID based on system information.
    """
    unique_id = os.getenv("COMPUTERNAME") or os.getenv("HOSTNAME") or "unknown"
    hardware_info = f"{unique_id}-{os.name}"
    hwid = hashlib.sha256(hardware_info.encode()).hexdigest()
    return hwid

def verify_license(key):
    """
    Sends the license key and HWID to the server for verification.
    """
    hwid = get_hwid()
    payload = {
        "key": key,
        "hwid": hwid
    }
    try:
        response = requests.post(SERVER_URL, json=payload)
        data = response.json()
        if data.get("success"):
            print(f"License Verified: {data.get('message')}")
            return True
        else:
            print(f"License Verification Failed: {data.get('message')}")
            return False
    except Exception as e:
        print(f"Error communicating with the license server: {e}")
        return False

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
            command_prefix="yoyo",
            intents=discord.Intents.all(),
            help_command=None
        )
        
    async def on_ready(self) -> None:
        await load_commands(self)
        await self.tree.sync()
        
        print(f"Logged in as {self.user.name}")
        
if __name__ == "__main__":
    # Load configuration
    config = load_json()
    license_key = config.get('license_key')

    # Verify the license key
    if not verify_license(license_key):
        print("Invalid license key. Shutting down...")
        exit(1)  # Exit the program if the license is invalid

    # Start the bot if the license is valid
    PurityMm = MyBot()
    PurityMm.run(config['token'])
        
