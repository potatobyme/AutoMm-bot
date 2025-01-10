import json
import discord
from discord.ui import Button, View
from function import *
from .walletModal import walletModal

class confirmDeal(Button):
    def __init__(self, filename, prvKey, amount):
        self.filename = filename
        self.prvKey = prvKey
        self.amount = amount
        super().__init__(
            style=discord.ButtonStyle.green,
            label="Confirm",
            emoji="✅"
        )
        
    async def callback(self, interaction: discord.Interaction):
        # Load deal details from file
        file = json.load(open(f"process/{self.filename}.json", 'r'))

        # Ensure only the sender can confirm
        if interaction.user.id != file['sender']:
            return await interaction.response.send_message(
                "You cannot confirm this deal because you are not the sender.", ephemeral=True
            )

        # Define a button for the recever to enter the LTC address
        class EnterLTCAddress(Button):
            def __init__(self, prvKey, amount):
                self.prvKey = prvKey
                self.amount = amount
                super().__init__(
                    style=discord.ButtonStyle.primary,
                    label="Enter LTC Address",
                    emoji="💰"
                )
            
            async def callback(self, interaction: discord.Interaction):
                # Ensure only the recever can use this button
                if interaction.user.id != file['recever']:
                    return await interaction.response.send_message(
                        "You cannot enter the LTC address because you are not the recever.", ephemeral=True
                    )
                
                # Show the wallet modal to the recever
                await interaction.response.send_modal(walletModal(self.prvKey, self.amount))

        # Create a view for the button
        view = View()
        view.add_item(EnterLTCAddress(self.prvKey, self.amount))

        # Create an embed
        embed = discord.Embed(
            title="Deal Confirmed!",
            description="Please use the button below to enter the LTC address.",
            color=discord.Color.blue()
        )
        embed.set_footer(text="Make sure to complete the transaction promptly.")

        # Send a plain text mention followed by the embed with the button
        await interaction.channel.send(
            content=f"<@{file['recever']}>, the sender has confirmed the deal.",
            embed=embed,
            view=view
        )

        # Acknowledge the sender
        await interaction.response.send_message(
            "You have confirmed the deal. Waiting for the recever to enter the LTC address.", ephemeral=True
        )
        
