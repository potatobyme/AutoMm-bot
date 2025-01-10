import discord
from discord.ui import TextInput, Modal
from function import *

class walletModal(Modal):
    def __init__(self, prvKey, amount):
        self.prvKey = prvKey
        self.amount = amount
        super().__init__(
            title="Litecoin Address"
        )

        wallet = TextInput(
            label="Your Wallet",
            placeholder="Exemple: LVeJaGL2evHhgFCVa6GQWamL18oCdwLb2c",
            required=True,
            style=discord.TextStyle.short,
            min_length=1
        )
    
        self.add_item(wallet)

    async def on_submit(self, interaction: discord.Interaction):
        toAddress = self.children[0].value
        txId = send_to_address(self.prvKey, toAddress)
        embed = discord.Embed(
            title="MiddleMan Confirmed",
            description=f"""
# The deal processed successfuly, And Payment was Released 

> **Transaction Id:** `{txId}`
> **Wallet:** `{toAddress}`
> **Amount:** `{self.amount} €`

**MiddleMan Deal completed.**
            """,
            color=embed_color()
        )
        await interaction.response.edit_message(embed=embed, view=None, content=None)
        
