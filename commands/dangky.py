import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
import random
from datetime import datetime
from zoneinfo import ZoneInfo

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

        cursor.execute("""
        SELECT account_id,
               account_number,
               cccd,
               balance,
               created_at,
               status
        FROM accounts
        WHERE user_id=?
        """, (user_id,))

        account = cursor.fetchone()

        if account:

            embed = discord.Embed(
                title="🏦 Bạn đã có tài khoản",
                color=discord.Color.orange()
            )

            embed.add_field(
                name="🆔 Mã tài khoản",
                value=f"`{account[0]}`",
                inline=False
            )

            embed.add_field(
                name="💳 Số tài khoản",
                value=f"`{account[1]}`",
                inline=False
            )

            embed.add_field(
                name="🪪 CCCD",
                value=f"`{account[2]}`",
                inline=False
            )

            embed.add_field(
                name="💰 Số dư",
                value=f"`{account[3]:,} VNĐ`",
                inline=False
            )

            embed.add_field(
                name="📅 Ngày & Giờ mở",
                value=f"`{account[4]}`",
                inline=False
            )

            embed.add_field(
                name="📌 Trạng thái",
                value=f"`{account[5]}`",
                inline=False
            )

            embed.set_footer(text="AnhBiu Bank")

            await interaction.response.send_message(
                embed=embed,
                ephemeral=True
            )

            db.close()
            return

        while True:
            account_id = str(random.randint(100000, 999999))
            cursor.execute(
                "SELECT 1 FROM accounts WHERE account_id=?",
                (account_id,)
            )
            if cursor.fetchone() is None:
                break

        while True:
            account_number = str(random.randint(1000000000, 9999999999))
            cursor.execute(
                "SELECT 1 FROM accounts WHERE account_number=?",
                (account_number,)
            )
            if cursor.fetchone() is None:
                break

        while True:
            cccd = str(random.randint(100000000000, 999999999999))
            cursor.execute(
                "SELECT 1 FROM accounts WHERE cccd=?",
                (cccd,)
            )
            if cursor.fetchone() is None:
                break

        created_at = datetime.now(
            ZoneInfo("Asia/Ho_Chi_Minh")
        ).strftime("%d/%m/%Y %H:%M:%S")

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
        VALUES (?, ?, ?, ?, ?, ?, ?)
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
            description="Chào mừng bạn đến với AnhBiu Bank!",
            color=discord.Color.green()
        )

        embed.add_field(
            name="🆔 Mã tài khoản",
            value=f"`{account_id}`",
            inline=False
        )

        embed.add_field(
            name="💳 Số tài khoản",
            value=f"`{account_number}`",
            inline=False
        )

        embed.add_field(
            name="🪪 CCCD",
            value=f"`{cccd}`",
            inline=False
        )

        embed.add_field(
            name="💰 Số dư",
            value="`0 VNĐ`",
            inline=False
        )

        embed.add_field(
            name="📅 Ngày & Giờ mở",
            value=f"`{created_at}`",
            inline=False
        )

        embed.add_field(
            name="📌 Trạng thái",
            value="`active`",
            inline=False
        )

        embed.set_footer(text="AnhBiu Bank")

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(DangKy(bot))
