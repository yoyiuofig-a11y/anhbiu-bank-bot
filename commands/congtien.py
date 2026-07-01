import discord
from discord.ext import commands
from discord import app_commands
import sqlite3

class CongTien(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="congtien",
        description="Cộng tiền cho tài khoản"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def congtien(
        self,
        interaction: discord.Interaction,
        ma_tai_khoan: str,
        so_tien: int
    ):

        db = sqlite3.connect("bank.db")
        cursor = db.cursor()

        cursor.execute(
            "SELECT balance FROM accounts WHERE account_id=?",
            (ma_tai_khoan,)
        )

        data = cursor.fetchone()

        if not data:
            await interaction.response.send_message(
                "❌ Không tìm thấy tài khoản.",
                ephemeral=True
            )
            db.close()
            return

        cursor.execute(
            "UPDATE accounts SET balance = balance + ? WHERE account_id=?",
            (so_tien, ma_tai_khoan)
        )

        db.commit()
        db.close()

        await interaction.response.send_message(
            f"✅ Đã cộng **{so_tien:,} VNĐ** cho **{ma_tai_khoan}**."
        )

async def setup(bot):
    await bot.add_cog(CongTien(bot))
