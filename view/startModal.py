import json
import discord
from discord.ui import Modal, TextInput, View
from discord import TextStyle
from .addUserButton import addUserButton
from .cancelButton import cancelButton
from function import *

class startModal(Modal):
    def __init__(self, userId, bot) -> None:
        self.userId = userId
        self.bot = bot
        super().__init__(
            title="Registration"
        )
        
        item = TextInput(
            label="Which item are you dealing",
            placeholder="Exemple: 5 Nitro Boost",
            style=TextStyle.short,
            required=True
        )
        
        price = TextInput(
            label="How much buyer need to pay for all",
            placeholder="Exemple: 10€/10$",
            style=TextStyle.short,
            required=True
        )
        
        description = TextInput(
            placeholder="like terms and conditions",
            label="Describe the deal",
            style=TextStyle.long,
            required=True
        )
        
        self.add_item(item)
        self.add_item(price)
        self.add_item(description)
            
    async def on_submit(self, interaction: discord.Interaction):
        config = load_json()
        itemValue = self.children[0].value
        priceValue = self.children[1].value
        descValue = self.children[2].value
        
        category = discord.utils.get(interaction.guild.categories, id=config['config']['tickets']['category'])
        if category == None:
            return await interaction.response.send_message("Sorry, the category where ticket need to be opened not found. Please contact a staff member", ephemeral=True)
        filename = gen_uid()
        
        embed = discord.Embed(
            title=f"`👑`・{interaction.guild.name} MiddleMan Service",
            description=f"***Informations about the deal***\n\n> **Deal Item:** *{itemValue}*\n> **Money will be given:** *{priceValue}*\n**> Description:** *```{descValue}```*",
            color=embed_color()
        )
        embed.set_footer(text=footer(self.bot, uid=filename))
        view = View(timeout=None)
        view.add_item(addUserButton(self.userId, filename))
        view.add_item(cancelButton(self.userId, filename))
        channel = await category.create_text_channel(name=f"{interaction.user.name}-mm")
        await channel.set_permissions(interaction.guild.default_role, read_messages=False)
        await channel.send(embed=embed, view=view)
        await interaction.response.send_message(f"Your ticket is opened in {channel.mention}", ephemeral=True)
        payload = {
            "confirmation": 0,
            "sender": None,
            "recever": None,
            "senderConfirm": False,
            "receverConfirm": False,
            "rolesConfirm": 0
        }
        json.dump(payload, open(f"process/{filename}.json", 'w', encoding='utf-8'), indent=4)
        config = load_json()
        logsConfig = config['config']['logs']
        if logsConfig['status'] == "on":
            if logsConfig['channel'] != None:
                logsChannel = discord.utils.get(interaction.guild.channels, id=logsConfig['channel'])
                if logsChannel:
                    embed = discord.Embed(
                        title="`👑`・Middleman Ticket Opened",
                        description=f"***Informations about the deal ({channel.mention})***\n\n> **Opened by:** {interaction.user.mention}`{interaction.user.id}`\n> **Item:** {itemValue}\n> **Price:** {priceValue}",
                        color=embed_color()
                    )
                    embed.set_footer(text=footer(self.bot, uid=filename))
                    await logsChannel.send(embed=embed)