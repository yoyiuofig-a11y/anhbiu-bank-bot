import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
from datetime import datetime

class TruTien(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="trutien",
        description="Trừ tiền khỏi tài khoản"
    )
    async def trutien(
        self,
        interaction: discord.Interaction,
        ma_tai_khoan: str,
        so_tien: app_commands.Range[int, 1, None]
    ):

        allowed_roles = {
            "Owner",
            "Co-Owner",
            "HeadAdmin",
            "Admin",
            "Developer"
        }

        # Kiểm tra quyền người thực hiện
        user_roles = {role.name for role in interaction.user.roles}

        if not user_roles.intersection(allowed_roles):
            await interaction.response.send_message(
                "❌ Bạn không có quyền sử dụng lệnh này.",
                ephemeral=True
            )
            return

        db = sqlite3.connect("bank.db")
        cursor = db.cursor()

        # Lấy user_id và số dư
        cursor.execute(
            "SELECT user_id, balance FROM accounts WHERE account_id=?",
            (ma_tai_khoan,)
        )

        data = cursor.fetchone()

        if data is None:
            await interaction.response.send_message(
                "❌ Không tìm thấy tài khoản.",
                ephemeral=True
            )
            db.close()
            return

        member = interaction.guild.get_member(int(data[0]))

        # Không cho trừ tiền Staff
        if member:
            target_roles = {role.name for role in member.roles}

            if target_roles.intersection(allowed_roles):
                await interaction.response.send_message(
                    "❌ Không thể trừ tiền của Owner, Co-Owner, HeadAdmin, Admin hoặc Developer.",
                    ephemeral=True
                )
                db.close()
                return

        balance = data[1]

        if balance < so_tien:
            await interaction.response.send_message(
                "❌ Số dư không đủ.",
                ephemeral=True
            )
            db.close()
            return

        cursor.execute(
            "UPDATE accounts SET balance = balance - ? WHERE account_id=?",
            (so_tien, ma_tai_khoan)
        )

        cursor.execute(
            "INSERT INTO logs(sender, receiver, amount, time) VALUES(?,?,?,?)",
            (
                "ADMIN",
                ma_tai_khoan,
                -so_tien,
                datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            )
        )

        db.commit()
        db.close()

        await interaction.response.send_message(
            f"✅ Đã trừ **{so_tien:,} VNĐ** khỏi tài khoản **{ma_tai_khoan}**."
        )

async def setup(bot):
    await bot.add_cog(TruTien(bot))
