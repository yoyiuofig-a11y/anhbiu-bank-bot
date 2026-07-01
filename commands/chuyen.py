import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
from datetime import datetime

class Chuyen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="chuyen", description="Chuyển tiền")
    @app_commands.describe(
        ma_tai_khoan="Mã tài khoản người nhận",
        so_tien="Số tiền muốn chuyển"
    )
    async def chuyen(
        self,
        interaction: discord.Interaction,
        ma_tai_khoan: str,
        so_tien: int
    ):

        if so_tien <= 0:
            await interaction.response.send_message(
                "❌ Số tiền phải lớn hơn 0.",
                ephemeral=True
            )
            return

        db = sqlite3.connect("bank.db")
        cursor = db.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            receiver TEXT,
            amount INTEGER,
            time TEXT
        )
        """)

        user = str(interaction.user.id)

        cursor.execute(
            "SELECT balance, locked, account_id FROM accounts WHERE user_id=?",
            (user,)
        )

        sender = cursor.fetchone()

        if not sender:
            await interaction.response.send_message(
                "❌ Bạn chưa đăng ký tài khoản.",
                ephemeral=True
            )
            db.close()
            return

        balance, locked, sender_id = sender

        if locked:
            await interaction.response.send_message(
                "🔒 Tài khoản của bạn đang bị khóa.",
                ephemeral=True
            )
            db.close()
            return

        if balance < so_tien:
            await interaction.response.send_message(
                "❌ Số dư không đủ.",
                ephemeral=True
            )
            db.close()
            return

        cursor.execute(
            "SELECT user_id, locked FROM accounts WHERE account_id=?",
            (ma_tai_khoan,)
        )

        target = cursor.fetchone()

        if not target:
            await interaction.response.send_message(
                "❌ Không tìm thấy tài khoản nhận.",
                ephemeral=True
            )
            db.close()
            return

        target_user, target_locked = target

        if target_locked:
            await interaction.response.send_message(
                "❌ Tài khoản nhận đang bị khóa.",
                ephemeral=True
            )
            db.close()
            return

        cursor.execute(
            "UPDATE accounts SET balance=balance-? WHERE user_id=?",
            (so_tien, user)
        )

        cursor.execute(
            "UPDATE accounts SET balance=balance+? WHERE user_id=?",
            (so_tien, target_user)
        )

        cursor.execute(
            "INSERT INTO history(sender,receiver,amount,time) VALUES(?,?,?,?)",
            (
                sender_id,
                ma_tai_khoan,
                so_tien,
                datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            )
        )

        db.commit()
        db.close()

        await interaction.response.send_message(
            f"✅ Đã chuyển **{so_tien:,} VNĐ** đến **{ma_tai_khoan}**."
        )

async def setup(bot):
    await bot.add_cog(Chuyen(bot))
