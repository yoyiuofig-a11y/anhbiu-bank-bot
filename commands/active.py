import discord
from discord.ext import commands
from discord import app_commands
import sqlite3

class Active(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="active",
        description="Xem số tài khoản đang hoạt động"
    )
    async def active(self, interaction: discord.Interaction):

        db = sqlite3.connect("bank.db")
        cursor = db.cursor()

        cursor.execute("SELECT COUNT(*) FROM accounts")
        tong = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM accounts WHERE status='active'"
        )
        hoatdong = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM accounts WHERE status='locked'"
        )
        khoa = cursor.fetchone()[0]

        db.close()

        embed = discord.Embed(
            title="📊 Thống kê ngân hàng",
            color=0x3498db
        )

        embed.add_field(
            name="👥 Tổng tài khoản",
            value=str(tong),
            inline=False
        )

        embed.add_field(
            name="🟢 Đang hoạt động",
            value=str(hoatdong),
            inline=True
        )

        embed.add_field(
            name="🔴 Đã khóa",
            value=str(khoa),
            inline=True
        )

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Active(bot))
