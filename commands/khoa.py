import discord
from discord.ext import commands
from discord import app_commands
import sqlite3

class Khoa(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="khoa",
        description="Khóa tài khoản"
    )
    async def khoa(
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

        # Không cho khóa tài khoản của staff
        if member:
            target_roles = {role.name for role in member.roles}

            if target_roles.intersection(allowed_roles):
                await interaction.response.send_message(
                    "❌ Không thể khóa tài khoản của Owner, Co-Owner, HeadAdmin, Admin hoặc Developer.",
                    ephemeral=True
                )
                db.close()
                return

        # Khóa tài khoản
        cursor.execute(
            "UPDATE accounts SET status='locked' WHERE account_id=?",
            (ma_tai_khoan,)
        )

        db.commit()
        db.close()

        await interaction.response.send_message(
            f"🔒 Đã khóa tài khoản **{ma_tai_khoan}** thành công."
        )

async def setup(bot):
    await bot.add_cog(Khoa(bot))
