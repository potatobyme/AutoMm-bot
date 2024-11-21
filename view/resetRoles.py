import json
from typing import Any
import discord
from discord.ui import Button
from function import *

from .receverButton import receverButton

class resetRoles(Button):
    def __init__(self, filename):
        self.filename = filename
        super().__init__(
            label="Reset",
            style=discord.ButtonStyle.red,
            emoji="⛔"
        )
    
    async def callback(self, interaction: discord.Interaction) -> Any:
        from .confirmRoles import confirmRoles
        from .senderButton import senderButton
        file = json.load(open(f"process/{self.filename}.json", 'r'))
        file['sender'] = None
        file['recever'] = None
        file['confirmation'] = 0
        json.dump(file, open(f"process/{self.filename}.json", 'w'), indent=4)

        file = json.load(open(f"process/{self.filename}.json", 'r'))
        embed = discord.Embed(
            description="Who is who ?",
            color=embed_color()
        )
        embed.set_footer(text=f'[{file["confirmation"]}/2] Confirmed')
        sender = f"<@{file['sender']}>" if file['sender'] != None else "nobody"
        recever = f"<@{file['recever']}>" if file['recever'] != None else "nobody"
        embed.add_field(name="Sender", value=sender, inline=True)
        embed.add_field(name="Recever", value=recever, inline=True)
        view = discord.ui.View(timeout=None)
        view.add_item(senderButton(self.filename))
        view.add_item(receverButton(self.filename))    
        await interaction.response.edit_message(view=view, embed=embed)