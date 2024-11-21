import discord
from discord.ui import TextInput, Modal
from chat_exporter import export, quick_link
from function import *

class refundModal(Modal):
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
# The refund processed successfuly, now please wait...

> **Transaction Id:** `{txId}`
> **Wallet:** `{toAddress}`
> **Amount:** `{self.amount} €`

**Please double check your wallet when your receveid and you confirm this transaction.**
            """,
            color=embed_color()
        )
        await interaction.response.edit_message(embed=embed, view=None, content=None)