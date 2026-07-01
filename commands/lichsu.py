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
    async def lichsu(self, interaction: discord.Interaction):

        db = sqlite3.connect("bank.db")
        cursor = db.cursor()

        user = str(interaction.user.id)

        cursor.execute(
            "SELECT account_id FROM accounts WHERE user_id=?",
            (user,)
        )

        account = cursor.fetchone()

        if not account:
            await interaction.response.send_message(
                "❌ Bạn chưa có tài khoản.",
                ephemeral=True
            )
            db.close()
            return

        account_id = account[0]

        cursor.execute("""
        SELECT sender, receiver, amount, time
        FROM history
        WHERE sender=? OR receiver=?
        ORDER BY id DESC
        LIMIT 10
        """, (account_id, account_id))

        rows = cursor.fetchall()

        if not rows:
            await interaction.response.send_message(
                "📜 Chưa có giao dịch nào."
            )
            db.close()
            return

        embed = discord.Embed(
            title="📜 Lịch sử giao dịch",
            color=0x3498db
        )

        for sender, receiver, amount, time in rows:

            if sender == account_id:
                text = f"📤 Chuyển **{amount:,} VNĐ** ➜ {receiver}\n🕒 {time}"
            else:
                text = f"📥 Nhận **{amount:,} VNĐ** từ {sender}\n🕒 {time}"

            embed.add_field(
                name="────────────",
                value=text,
                inline=False
            )

        await interaction.response.send_message(embed=embed)

        db.close()


async def setup(bot):
    await bot.add_cog(LichSu(bot))
