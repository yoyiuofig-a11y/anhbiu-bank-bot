import discord
from discord.ext import commands
from discord import app_commands
import sqlite3

class LichSu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="lichsu",
        description="Xem lịch sử giao dịch"
    )
    async def lichsu(
        self,
        interaction: discord.Interaction
    ):

        db = sqlite3.connect("bank.db")
        cursor = db.cursor()

        # Lấy mã tài khoản của người dùng
        cursor.execute(
            "SELECT account_id FROM accounts WHERE user_id=?",
            (str(interaction.user.id),)
        )

        account = cursor.fetchone()

        if account is None:
            await interaction.response.send_message(
                "❌ Bạn chưa đăng ký tài khoản.",
                ephemeral=True
            )
            db.close()
            return

        ma_tai_khoan = account[0]

        # Lấy 20 giao dịch gần nhất
        cursor.execute("""
            SELECT sender, receiver, amount, time
            FROM logs
            WHERE sender=? OR receiver=?
            ORDER BY id DESC
            LIMIT 20
        """, (ma_tai_khoan, ma_tai_khoan))

        logs = cursor.fetchall()
        db.close()

        if not logs:
            await interaction.response.send_message(
                "📄 Bạn chưa có giao dịch nào."
            )
            return

        embed = discord.Embed(
            title="📜 Lịch sử giao dịch",
            description=f"👤 {interaction.user.mention}",
            color=discord.Color.blue()
        )

        for sender, receiver, amount, time in logs:

            if amount >= 0:
                icon = "📥"
            else:
                icon = "📤"

            embed.add_field(
                name=f"{icon} {abs(amount):,} VNĐ",
                value=(
                    f"**Người gửi:** `{sender}`\n"
                    f"**Người nhận:** `{receiver}`\n"
                    f"**Thời gian:** `{time}`"
                ),
                inline=False
            )

        embed.set_footer(
            text=f"{len(logs)} giao dịch gần nhất"
        )

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(LichSu(bot))
