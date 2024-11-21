import discord
from discord.ui import Modal, TextInput
from function import *
from discord import PermissionOverwrite
from .senderButton import senderButton
from .receverButton import receverButton

class addUserModal(Modal):
    def __init__(self, userId, filename):
        self.userId = userId
        self.filename = filename
        super().__init__(
            title="Add the second user"
        )
        
        secondUserId = TextInput(
            label="User Id:",
            placeholder="Exemple: 940965110443302974",
            required=True
        )
        
        self.add_item(secondUserId)
        
    
    async def on_submit(self, interaction: discord.Interaction):
        newUserId = self.children[0].value
        try:
            newUserId = int(newUserId)
        except ValueError:
            return await interaction.response.send_message('The item you give don\'t looks like a Discord user Id', ephemeral=True)
        
        newUser = discord.utils.get(interaction.guild.members, id=newUserId)
        if newUser == None:
            return await interaction.response.send_message("The user you give me are not in the server.", ephemeral=True)
        
        overwrite = PermissionOverwrite()
        overwrite.read_messages = True  
        overwrite.send_messages = True 
        overwrite.attach_files = True
        overwrite.embed_links = True
        overwrite.add_reactions = True
        overwrite.use_external_emojis = True
        
        await interaction.channel.set_permissions(newUser, overwrite=overwrite)
        embed = discord.Embed(
            title="`✅`・Successfuly added",
            description=f"*{newUser.mention} successfuly added into the ticket.*",
            color=embed_color()
        )
        await interaction.response.send_message(embed=embed)
        file = json.load(open(f"process/{self.filename}.json", 'r'))
        embed = discord.Embed(
            title="Taking dealing roles...",
            description="Who is who ?\n\n",
            color=embed_color()
        )
        embed.set_footer(text="[0/2] Confirmed")
        sender = f"<@{file['sender']}>" if file['sender'] != None else "nobody"
        recever = f"<@{file['recever']}>" if file['recever'] != None else "nobody"
        embed.add_field(name="Sender", value=sender, inline=True)
        embed.add_field(name="Recever", value=recever, inline=True)
        view = discord.ui.View(timeout=None)
        view.add_item(senderButton(self.filename))
        view.add_item(receverButton(self.filename))
        await interaction.channel.send(embed=embed, content=f"{interaction.user.mention}{newUser.mention}", view=view)

