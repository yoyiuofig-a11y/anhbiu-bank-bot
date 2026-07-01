import discord
from discord.ext import commands
from discord import app_commands
import sqlite3

class HoSo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="hoso", description="Xem hồ sơ ngân hàng")
    async def hoso(self, interaction: discord.Interaction):

        db = sqlite3.connect("bank.db")
        cursor = db.cursor()

        user = str(interaction.user.id)

        cursor.execute(
            "SELECT * FROM accounts WHERE user_id=?",
            (user,)
        )

        data = cursor.fetchone()

        if not data:
            await interaction.response.send_message(
                "❌ Bạn chưa đăng ký tài khoản.",
                ephemeral=True
            )
            db.close()
            return

        user_id, account_id, account_number, cccd, balance, created_at, locked = data

        embed = discord.Embed(
            title="🏦 Hồ sơ ngân hàng",
            color=0x3498db
        )

        embed.add_field(
            name="👤 Chủ tài khoản",
            value=interaction.user.mention,
            inline=False
        )

        embed.add_field(
            name="🆔 Mã tài khoản",
            value=account_id,
            inline=True
        )

        embed.add_field(
            name="💳 Số tài khoản",
            value=account_number,
            inline=True
        )

        embed.add_field(
            name="🪪 CCCD",
            value=cccd,
            inline=False
        )

        embed.add_field(
            name="💰 Số dư",
            value=f"{balance:,} VNĐ",
            inline=True
        )

        embed.add_field(
            name="🔒 Trạng thái",
            value="Đã khóa 🔴" if locked else "Hoạt động 🟢",
            inline=True
        )

        embed.add_field(
            name="📅 Ngày mở",
            value=created_at,
            inline=False
        )

        embed.set_footer(text="AnhBiu Bank")

        await interaction.response.send_message(embed=embed)

        db.close()

async def setup(bot):
    await bot.add_cog(HoSo(bot))
