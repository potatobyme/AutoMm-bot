import json
import discord
from discord.ui import Button
from function import *
import asyncio
from .copyAddress import copyAddress
from .confirmDeal import confirmDeal
from .refundButton import refundButton

class confirmRoles(Button):
    def __init__(self, filename):
        self.filename = filename
        super().__init__(
            style=discord.ButtonStyle.green,
            label="Confirm",
            emoji="✅"
        )
        
    async def callback(self, interaction: discord.Interaction):
        file = json.load(open(f"process/{self.filename}.json", 'r'))
        if interaction.user.id == file['sender']:
            if file['senderConfirm'] == True:
                return await interaction.response.send_message("You already confirmed this roles, please wait the second user confirmation.", ephemeral=True)
                
            file['senderConfirm'] = True
            file['rolesConfirm'] = file['rolesConfirm'] + 1
            json.dump(file, open(f"process/{self.filename}.json", 'w'), indent=4)
        elif interaction.user.id == file['recever']:
            if file['receverConfirm'] == True:
                return await interaction.response.send_message("You already confirmed this roles, please wait the second user confirmation.", ephemeral=True)
            file['receverConfirm'] = True
            file['rolesConfirm'] = file['rolesConfirm'] + 1
            json.dump(file, open(f"process/{self.filename}.json", 'w'), indent=4)
            
        file = json.load(open(f"process/{self.filename}.json", 'r'))
        senderConfirmation = "✅" if file['senderConfirm'] == True else "❌"
        receverConfirmation = "✅" if file['receverConfirm'] == True else "❌"
        embed = discord.Embed(
            title="Roles Confirmations...",
            description=f"Are you sure you take rights roles \n\n> **Sender Confirmation: {senderConfirmation}**\n> **Recever Confirmation: {receverConfirmation}**",
            color=embed_color()
        )
        embed.add_field(name="Sender Confirmation", value=f"<@{file['sender']}>", inline=True)
        embed.add_field(name="Recever", value=f"<@{file['recever']}>", inline=True)
        embed.set_footer(text=f"[{file['rolesConfirm']}/2] Confirmed")
        await interaction.response.edit_message(view=self.view, embed=embed)
        if file['rolesConfirm'] == 2:
            wallet, privateKey, publicKey, wif = create_wallet()
            embed = discord.Embed(
                title="Awaiting Payment",
                description=f"""
# <@{file['sender']}> Please send amount at this adress:

> **Address:** `{wallet}`
> **Please send only litecoin and any other cryptocurrency.**
                """,
                color=embed_color()
            )
            embed.set_footer(text="Awaiting Payment... [Anything]")
            view = discord.ui.View(timeout=None)
            view.add_item(copyAddress(wallet, self.filename))
            await interaction.followup.edit_message(message_id=interaction.message.id, embed=embed, view=view)
            time = 0
            while True:
                check, litoshi = check_transactions(wallet)
                if check == "detected but not confirmed":
                    embed = discord.Embed(
                        title="Payment Detected",
                        description=f"""
# Payment detected, please wait For confirmation:

> **Address:** `{wallet}`
> **Please send only litecoin .**
                        """, color=embed_color()
                    )
                    embed.set_footer(text="Detected paiement... [Detected]")
                    await interaction.followup.edit_message(message_id=interaction.message.id, embed=embed, view=None)
                elif check == "confirmed":
                    try:
                        ltcAmount = litoshi / 100000000
                        eurAmount = convertToLtc(ltcAmount)
                        embed = discord.Embed(
                            title="Payment Confirmed and Received",
                            description=f"""
# Payment are confirmed and Received.

> **Amount in litecoin:** `{ltcAmount} ltc`  
> **Amount in €: `{eurAmount} €`** 
> **Now you can process to DEAL**
> **Please confirm the deal after you get your products**
                            """, 
                            color=embed_color()
                        )
                        embed.set_footer(text="Receive Payment [Done]")
                        view = discord.ui.View(timeout=None)
                        view.add_item(confirmDeal(self.filename, privateKey, eurAmount))
                        view.add_item(refundButton(self.filename, eurAmount, privateKey))
                        await interaction.followup.edit_message(message_id=interaction.message.id, embed=embed, view=view)
                        config = load_json()
                        logsConfig = config['config']['logs']
                        if logsConfig['status'] == "on":
                            if logsConfig['channel'] != None:
                                file = json.load(open(f"process/{self.filename}.json", 'r'))
                                senderId = file['sender']
                                receverId = file['recever']
                                logsChannel = discord.utils.get(interaction.guild.channels, id=logsConfig['channel'])
                                if logsChannel:
                                    embed = discord.Embed(
                                        title="`✨`・Deal completed",
                                        description=f"*A middleman deal finished now.*",
                                        color=embed_color()
                                    )
                                    embed.add_field(name="Sender Infos", value=f"> **Id:** {senderId}\n> **Mention:** <@{senderId}>\n> **Role:** Sender")
                                    embed.add_field(name="Recever Infos", value=f"> **Id:** {receverId}\n> **Mention:** <@{receverId}>\n> **Role:** Sender")
                                    embed.set_footer(text=footer(self.bot, uid=self.filename))
                                    await logsChannel.send(embed=embed)
                        break
                    except Exception as e:
                        print(e)
                await asyncio.sleep(90)
                time += 0.5
