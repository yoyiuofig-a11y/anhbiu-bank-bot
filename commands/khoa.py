import discord
from discord.ext import commands
from discord import app_commands
import sqlite3

class Khoa(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="khoa",
        description="Khóa tài khoản ngân hàng"
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
            "SELECT * FROM accounts WHERE account_id=?",
            (ma_tai_khoan,)
        )

        if not cursor.fetchone():
            await interaction.response.send_message(
                "❌ Không tìm thấy tài khoản.",
                ephemeral=True
            )
            db.close()
            return

        cursor.execute(
            "UPDATE accounts SET status='locked' WHERE account_id=?",
            (ma_tai_khoan,)
        )

        db.commit()
        db.close()

        embed = discord.Embed(
            title="🔒 Khóa tài khoản",
            description=f"Tài khoản **{ma_tai_khoan}** đã bị khóa.",
            color=0xe74c3c
        )

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Khoa(bot))
