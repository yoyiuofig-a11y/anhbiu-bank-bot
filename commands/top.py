import discord
from discord.ext import commands
from discord import app_commands
import sqlite3

class Top(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="top",
        description="Top tài khoản giàu nhất"
    )
    async def top(self, interaction: discord.Interaction):

        db = sqlite3.connect("bank.db")
        cursor = db.cursor()

        cursor.execute("""
        SELECT account_id, balance
        FROM accounts
        ORDER BY balance DESC
        LIMIT 10
        """)

        rows = cursor.fetchall()

        if not rows:
            await interaction.response.send_message(
                "❌ Chưa có dữ liệu."
            )
            db.close()
            return

        embed = discord.Embed(
            title="🏆 Top 10 tài khoản giàu nhất",
            color=0xf1c40f
        )

        medals = ["🥇","🥈","🥉"]

        for index, row in enumerate(rows):

            account_id = row[0]
            balance = row[1]

            if index < 3:
                icon = medals[index]
            else:
                icon = f"#{index+1}"

            embed.add_field(
                name=f"{icon} {account_id}",
                value=f"💰 {balance:,} VNĐ",
                inline=False
            )

        embed.set_footer(text="AnhBiu Bank")

        await interaction.response.send_message(embed=embed)

        db.close()


async def setup(bot):
    await bot.add_cog(Top(bot))
