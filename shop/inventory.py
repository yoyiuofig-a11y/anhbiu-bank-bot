import discord
from discord.ext import commands
from discord import app_commands

from .database import get_inventory

class Inventory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="inventory",
        description="Xem kho đồ của bạn"
    )
    async def inventory(self, interaction: discord.Interaction):

        inventory = get_inventory(interaction.user.id)

        if not inventory:
            await interaction.response.send_message(
                "📦 Kho đồ của bạn đang trống.",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title=f"📦 Kho đồ của {interaction.user.display_name}",
            color=0x3498DB
        )

        items = {}

        for item in inventory:
            items[item] = items.get(item, 0) + 1

        text = ""

        for name, amount in items.items():
            text += f"• {name} ×{amount}\n"

        embed.description = text

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Inventory(bot))
