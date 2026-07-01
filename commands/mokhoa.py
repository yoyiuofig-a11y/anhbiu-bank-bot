import discord
from discord.ext import commands
from discord import app_commands
import sqlite3

class MoKhoa(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="mokhoa",
        description="Mở khóa tài khoản"
    )
    async def mokhoa(
        self,
        interaction: discord.Interaction,
        ma_tai_khoan: str
    ):

        allowed_roles = {
            "Owner",
            "Co-Owner",
            "HeadAdmin",
            "Admin",
            "Developer"
        }

        # Kiểm tra quyền người dùng
        user_roles = {role.name for role in interaction.user.roles}

        if not user_roles.intersection(allowed_roles):
            await interaction.response.send_message(
                "❌ Bạn không có quyền sử dụng lệnh này.",
                ephemeral=True
            )
            return

        db = sqlite3.connect("bank.db")
        cursor = db.cursor()

        # Lấy user_id của tài khoản
        cursor.execute(
            "SELECT user_id FROM accounts WHERE account_id=?",
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

        # Không mở khóa tài khoản của staff
        if member:
            target_roles = {role.name for role in member.roles}

            if target_roles.intersection(allowed_roles):
                await interaction.response.send_message(
                    "❌ Không thể mở khóa tài khoản của Owner, Co-Owner, HeadAdmin, Admin hoặc Developer.",
                    ephemeral=True
                )
                db.close()
                return

        cursor.execute(
            "UPDATE accounts SET status='active' WHERE account_id=?",
            (ma_tai_khoan,)
        )

        db.commit()
        db.close()

        await interaction.response.send_message(
            f"✅ Đã mở khóa tài khoản **{ma_tai_khoan}**."
        )

async def setup(bot):
    await bot.add_cog(MoKhoa(bot))
