import discord
from discord import app_commands
from discord.ext import commands
import sqlite3
import random
from datetime import datetime

class DangKy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="dangky", description="Đăng ký tài khoản ngân hàng")
    async def dangky(self, interaction: discord.Interaction):

        db = sqlite3.connect("bank.db")
        cursor = db.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts(
            user_id TEXT PRIMARY KEY,
            account_id TEXT,
            account_number TEXT,
            cccd TEXT,
            balance INTEGER,
            created_at TEXT,
            locked INTEGER DEFAULT 0
        )
        """)

        user = str(interaction.user.id)

        cursor.execute(
            "SELECT * FROM accounts WHERE user_id=?",
            (user,)
        )

        if cursor.fetchone():
            await interaction.response.send_message(
                "❌ Bạn đã có tài khoản ngân hàng.",
                ephemeral=True
            )
            db.close()
            return

        cursor.execute("SELECT COUNT(*) FROM accounts")
        count = cursor.fetchone()[0] + 1

        account_id = f"AB{count:06d}"

        account_number = "".join(
            random.choice("0123456789")
            for _ in range(random.randint(10,12))
        )

        cccd = "".join(
            random.choice("0123456789")
            for _ in range(12)
        )

        created = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        cursor.execute("""
        INSERT INTO accounts
        VALUES(?,?,?,?,?,?,0)
        """,(
            user,
            account_id,
            account_number,
            cccd,
            1000,
            created
        ))

        db.commit()
        db.close()

        embed = discord.Embed(
            title="🏦 Đăng ký thành công",
            color=0x2
