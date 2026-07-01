import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
import random
from datetime import datetime

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

        user_id = str(interaction.user.id)

        # Kiểm tra đã đăng ký chưa
        cursor.execute(
            "SELECT account_id FROM accounts WHERE user_id=?",
            (user_id,)
        )

        if cursor.fetchone():
            await interaction.response.send_message(
                "❌ Bạn đã đăng ký tài khoản rồi!",
                ephemeral=True
            )
            db.close()
            return

        # Tạo thông tin tài khoản
        account_id = str(random.randint(100000, 999999))
        account_number = str(random.randint(1000000000, 9999999999))
        cccd = str(random.randint(100000000000, 999999999999))
        created_at = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        cursor.execute("""
        INSERT INTO accounts(
            user_id,
            account_id,
            account_number,
            cccd,
            balance,
            created_at,
            status
        )
        VALUES(?,?,?,?,?,?,?)
        """, (
            user_id,
            account_id,
            account_number,
            cccd,
            0,
            created_at,
            "active"
        ))

        db.commit()
        db.close()

        embed = discord.Embed(
            title="🏦 Đăng ký thành công",
            color=discord.Color.green()
        )

        embed.add_field(name="🆔 Mã tài khoản", value=f"`{account_id}`", inline=False)
        embed.add_field(name="💳 Số tài khoản", value=f"`{account_number}`", inline=False)
        embed.add_field(name="🪪 CCCD", value=f"`{cccd}`", inline=False)
        embed.add_field(name="💰 Số dư", value="`0 VNĐ`", inline=False)
        embed.set_footer(text="AnhBiu Bank")

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(DangKy(bot))
