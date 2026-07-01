import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
import random
import datetime

class DangKy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="dangky",
        description="Đăng ký tài khoản ngân hàng"
    )
    async def dangky(self, interaction: discord.Interaction):

        db = sqlite3.connect("bank.db")
        cursor = db.cursor()

        user = str(interaction.user.id)

        cursor.execute(
            "SELECT * FROM accounts WHERE user_id=?",
            (user,)
        )

        if cursor.fetchone():
            await interaction.response.send_message(
                "❌ Bạn đã đăng ký rồi!",
                ephemeral=True
            )
            db.close()
            return

        account_id = str(random.randint(100000, 999999))
        account_number = str(random.randint(1000000000, 9999999999))
        cccd = str(random.randint(100000000000, 999999999999))

        cursor.execute("""
        INSERT INTO accounts
        (user_id, account_id, account_number, cccd, balance, created_at, status)
        VALUES (?,?,?,?,?,?,?)
        """, (
            user,
            account_id,
            account_number,
            cccd,
            0,
            datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "active"
        ))

        db.commit()
        db.close()

        embed = discord.Embed(
            title="🏦 Đăng ký thành công",
            color=discord.Color.green()
        )

        embed.add_field(name="🆔 ID", value=account_id, inline=False)
        embed.add_field(name="💳 STK", value=account_number, inline=False)
        embed.add_field(name="🪪 CCCD", value=cccd, inline=False)
        embed.add_field(name="💰 Số dư", value="0 VNĐ", inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(DangKy(bot))
