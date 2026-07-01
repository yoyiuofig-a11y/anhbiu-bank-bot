import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
from datetime import datetime

class ChuyenTien(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="chuyen",
        description="Chuyển tiền cho tài khoản khác"
    )
    async def chuyen(
        self,
        interaction: discord.Interaction,
        ma_tai_khoan: str,
        so_tien: app_commands.Range[int, 1, None]
    ):

        db = sqlite3.connect("bank.db")
        cursor = db.cursor()

        # Kiểm tra người gửi
        cursor.execute(
            "SELECT account_id, balance, status FROM accounts WHERE user_id=?",
            (str(interaction.user.id),)
        )

        sender = cursor.fetchone()

        if sender is None:
            await interaction.response.send_message(
                "❌ Bạn chưa đăng ký tài khoản.",
                ephemeral=True
            )
            db.close()
            return

        sender_id, sender_balance, sender_status = sender

        if sender_status == "locked":
            await interaction.response.send_message(
                "❌ Tài khoản của bạn đang bị khóa.",
                ephemeral=True
            )
            db.close()
            return

        if sender_id == ma_tai_khoan:
            await interaction.response.send_message(
                "❌ Không thể chuyển tiền cho chính mình.",
                ephemeral=True
            )
            db.close()
            return

        # Kiểm tra người nhận
        cursor.execute(
            "SELECT balance, status FROM accounts WHERE account_id=?",
            (ma_tai_khoan,)
        )

        receiver = cursor.fetchone()

        if receiver is None:
            await interaction.response.send_message(
                "❌ Không tìm thấy tài khoản nhận.",
                ephemeral=True
            )
            db.close()
            return

        receiver_balance, receiver_status = receiver

        if receiver_status == "locked":
            await interaction.response.send_message(
                "❌ Tài khoản nhận đang bị khóa.",
                ephemeral=True
            )
            db.close()
            return

        if sender_balance < so_tien:
            await interaction.response.send_message(
                "❌ Số dư không đủ.",
                ephemeral=True
            )
            db.close()
            return

        # Trừ tiền người gửi
        cursor.execute(
            "UPDATE accounts SET balance = balance - ? WHERE account_id=?",
            (so_tien, sender_id)
        )

        # Cộng tiền người nhận
        cursor.execute(
            "UPDATE accounts SET balance = balance + ? WHERE account_id=?",
            (so_tien, ma_tai_khoan)
        )

        # Lưu lịch sử
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        cursor.execute(
            "INSERT INTO logs(sender, receiver, amount, time) VALUES(?,?,?,?)",
            (sender_id, ma_tai_khoan, so_tien, now)
        )

        db.commit()
        db.close()

        await interaction.response.send_message(
            f"✅ Chuyển thành công **{so_tien:,} VNĐ** đến tài khoản **{ma_tai_khoan}**."
        )

async def setup(bot):
    await bot.add_cog(ChuyenTien(bot))
