import json
import discord
from function import *
from discord.ui import Button
from .confirmRoles import confirmRoles

class senderButton(Button):
    def __init__(self, filename):
        self.filename = filename
        super().__init__(
            style=discord.ButtonStyle.blurple,
            label="sender",
            emoji="✨"
        )
        
    
    async def callback(self, interaction: discord.Interaction):
        from .resetRoles import resetRoles

        file = json.load(open(f"process/{self.filename}.json", 'r'))
        if interaction.user.id == file['sender']:
            return await interaction.response.send_message("You already take your role.", ephemeral=True)
        self.disabled = True
        file['sender'] = interaction.user.id
        file['confirmation'] = file['confirmation'] + 1
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
        await interaction.response.edit_message(view=self.view, embed=embed)
        if file['confirmation'] == 2:
            file = json.load(open(f"process/{self.filename}.json", 'r'))
            senderConfirmation = "✅" if file['senderConfirm'] == True else "❌"
            receverConfirmation = "✅" if file['receverConfirm'] == True else "❌"
            embed = discord.Embed(
                title="Roles Confirmations...",
                description=f"Are you sure you take rights roles \n\n> **Sender Confirmation: {senderConfirmation}**\n> **Recever Confirmation: {receverConfirmation}**",
                color=embed_color()
            )
            embed.add_field(name="Sender", value=f"<@{file['sender']}>", inline=True)
            embed.add_field(name="Recever", value=f"<@{file['recever']}>", inline=True)
            embed.set_footer(text=f"[{file['rolesConfirm']}/2] Confirmed")
            view = discord.ui.View(timeout=None)
            view.add_item(confirmRoles(self.filename))
            view.add_item(resetRoles(self.filename))

            await interaction.followup.edit_message(message_id=interaction.message.id, view=view, embed=embed)