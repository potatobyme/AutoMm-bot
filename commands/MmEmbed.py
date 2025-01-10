import discord
from discord import app_commands
from discord.ext import commands
from view.startButton import startButton
from function import load_json, unauthorized, embed_color

class MiddleManEmbed(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command(name="middleman-embed", description="Send the MiddleMan Panel to a selected channel.")
    @app_commands.describe(channel="The channel where the MiddleMan embed should be sent.")
    async def mmembed(self, interaction: discord.Interaction, channel: discord.TextChannel) -> None:
        # Load configuration
        config = load_json()

        # Authorization check
        if interaction.user.id not in config['whitelist'] and interaction.user.id != config['buyer']:
            return await unauthorized(interaction)

        # Create the enhanced embed
        embed = discord.Embed(
            title="`🏆`・MiddleMan Service Panel",
            description=(
                "**Welcome to the MiddleMan Service!**\n\n"
                "This panel ensures secure and transparent transactions between parties.\n\n"
                "Press the `Start` button below to initiate the process."
            ),
            color=embed_color()
        )
        embed.add_field(
            name="`🔒`・Secure Transactions",
            value="Your deals will be handled with the utmost security and reliability.",
            inline=False
        )
        embed.add_field(
            name="`⚡`・Fast and Efficient",
            value="Complete your deals quickly and without hassle.",
            inline=False
        )
        embed.add_field(
            name="`📍`・Instructions",
            value="1. Click the `Start` button to begin.\n"
                  "2. Follow the steps as instructed in the bot.\n"
                  "3. Enjoy seamless transactions!",
            inline=False
        )
        embed.set_footer(
            text=f"Requested by {interaction.user.name} • MiddleMan Bot",
            icon_url=interaction.user.avatar.url if interaction.user.avatar else None
        )
        embed.set_thumbnail(
            url="https://example.com/your-thumbnail.png"  # Replace with a relevant image URL
        )

        # Create a persistent button view
        view = discord.ui.View(timeout=None)
        view.add_item(startButton(self.bot))

        # Send embed to the selected channel
        await channel.send(embed=embed, view=view)

        # Acknowledge the interaction
        await interaction.response.send_message(
            f"The MiddleMan embed has been sent to {channel.mention}.",
            ephemeral=True
        )

# Cog setup function
async def setup(bot) -> None:
    await bot.add_cog(MiddleManEmbed(bot))
    
