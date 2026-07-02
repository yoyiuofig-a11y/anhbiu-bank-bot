import discord
from discord.ext import commands
from discord import app_commands

from .database import get_money, get_bank, deposit, withdraw


class Bank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="balance",
        description="Xem số dư"
    )
    async def balance(self, interaction: discord.Interaction):

        wallet = get_money(interaction.user.id)
        bank = get_bank(interaction.user.id)

        embed = discord.Embed(
            title="💰 Tài khoản của bạn",
            color=0xF1C40F
        )

        embed.add_field(
            name="💵 Ví",
            value=f"{wallet:,}$",
            inline=True
        )

        embed.add_field(
            name="🏦 Ngân hàng",
            value=f"{bank:,}$",
            inline=True
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="deposit",
        description="Gửi tiền vào ngân hàng"
    )
    async def deposit_cmd(
        self,
        interaction: discord.Interaction,
        amount: int
    ):

        if amount <= 0:
            await interaction.response.send_message(
                "❌ Số tiền không hợp lệ.",
                ephemeral=True
            )
            return

        if deposit(interaction.user.id, amount):
            await interaction.response.send_message(
                f"🏦 Đã gửi **{amount:,}$** vào ngân hàng."
            )
        else:
            await interaction.response.send_message(
                "❌ Bạn không đủ tiền.",
                ephemeral=True
            )

    @app_commands.command(
        name="withdraw",
        description="Rút tiền từ ngân hàng"
    )
    async def withdraw_cmd(
        self,
        interaction: discord.Interaction,
        amount: int
    ):

        if amount <= 0:
            await interaction.response.send_message(
                "❌ Số tiền không hợp lệ.",
                ephemeral=True
            )
            return

        if withdraw(interaction.user.id, amount):
            await interaction.response.send_message(
                f"💵 Đã rút **{amount:,}$**."
            )
        else:
            await interaction.response.send_message(
                "❌ Ngân hàng không đủ tiền.",
                ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(Bank(bot))
