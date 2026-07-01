import discord
from discord.ext import commands
from discord import app_commands
import sqlite3

class Khoa(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="khoa",
        description="Khóa tài khoản"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def khoa(
        self,
        interaction: discord.Interaction,
        ma_tai_khoan: str
    ):
        db = sqlite3.connect("bank.db")
        cursor = db.cursor()

        cursor.execute(
            "UPDATE accounts SET status='locked' WHERE account_id=?",
            (ma_tai_khoan,)
        )

        if cursor.rowcount == 0:
            await interaction.response.send_message(
                "❌ Không tìm thấy tài khoản.",
                ephemeral=True
            )
        else:
            db.commit()
            await interaction.response.send_message(
                f"🔒 Đã khóa tài khoản **{ma_tai_khoan}**."
            )

        db.close()

    @khoa.error
    async def khoa_error(self, interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                "❌ Chỉ Admin mới được sử dụng lệnh này.",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(Khoa(bot))
