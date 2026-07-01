import discord
from discord.ext import commands
from discord import app_commands
import sqlite3

class TimKiem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="timkiem",
        description="Tìm tài khoản bằng mã tài khoản"
    )
    @app_commands.describe(
        ma_tai_khoan="Ví dụ: AB000001"
    )
    async def timkiem(
        self,
        interaction: discord.Interaction,
        ma_tai_khoan: str
    ):

        db = sqlite3.connect("bank.db")
        cursor = db.cursor()

        cursor.execute("""
        SELECT account_id,
               account_number,
               balance,
               status,
               created_at
        FROM accounts
        WHERE account_id=?
        """, (ma_tai_khoan,))

        data = cursor.fetchone()

        if not data:
            await interaction.response.send_message(
                "❌ Không tìm thấy tài khoản.",
                ephemeral=True
            )
            db.close()
            return

        account_id, stk, balance, status, created = data

        embed = discord.Embed(
            title="🔍 Thông tin tài khoản",
            color=0x00b894
        )

        embed.add_field(
            name="🏦 Mã tài khoản",
            value=account_id,
            inline=False
        )

        embed.add_field(
            name="💳 Số tài khoản",
            value=stk,
            inline=False
        )

        embed.add_field(
            name="💰 Số dư",
            value=f"{balance:,} VNĐ",
            inline=False
        )

        embed.add_field(
            name="🔒 Trạng thái",
            value=status,
            inline=False
        )

        embed.add_field(
            name="📅 Ngày mở",
            value=created,
            inline=False
        )

        embed.set_footer(text="AnhBiu Bank")

        await interaction.response.send_message(embed=embed)

        db.close()


async def setup(bot):
    await bot.add_cog(TimKiem(bot))
