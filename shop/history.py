import discord
from discord.ext import commands
from discord import app_commands

from .database import get_history


class History(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="history",
        description="Xem lịch sử giao dịch"
    )
    async def history(self, interaction: discord.Interaction):

        history = get_history(interaction.user.id)

        if not history:
            await interaction.response.send_message(
                "📜 Bạn chưa có giao dịch nào.",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title="📜 Lịch sử giao dịch",
            color=0x3498DB
        )

        embed.description = "\n".join(
            f"• {item}" for item in history[-20:]
        )

        embed.set_footer(
            text=f"Tổng cộng: {len(history)} giao dịch"
        )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(History(bot))
