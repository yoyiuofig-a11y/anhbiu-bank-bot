import discord
import discord
from discord.ext import commands
from discord import app_commands
import sqlite3

class MoKhoa(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="mokhoa",
        description="Mở khóa tài khoản"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def mokhoa(
        self,
        interaction: discord.Interaction,
        ma_tai_khoan: str
    ):
        db = sqlite3.connect("bank.db")
        cursor = db.cursor()

        cursor.execute(
            "UPDATE accounts SET status='active' WHERE account_id=?",
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
                f"🔓 Đã mở khóa tài khoản **{ma_tai_khoan}**."
            )

        db.close()

    @mokhoa.error
    async def mokhoa_error(self, interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                "❌ Chỉ Admin mới được sử dụng lệnh này.",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(MoKhoa(bot))
