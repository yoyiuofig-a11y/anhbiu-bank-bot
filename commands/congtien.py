import discord
from discord.ext import commands
from discord import app_commands
import sqlite3

class CongTien(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="congtien",
        description="Cộng tiền vào tài khoản (Chỉ Admin)"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def congtien(
        self,
        interaction: discord.Interaction,
        stk: str,
        so_tien: app_commands.Range[int, 1, None]
    ):
        try:
            db = sqlite3.connect("bank.db")
            cursor = db.cursor()

            cursor.execute(
                "SELECT balance FROM accounts WHERE account_number=?",
                (stk,)
            )
            account = cursor.fetchone()

            if account is None:
                await interaction.response.send_message(
                    "❌ Không tìm thấy số tài khoản.",
                    ephemeral=True
                )
                db.close()
                return

            balance = account[0] + so_tien

            cursor.execute(
                "UPDATE accounts SET balance=? WHERE account_number=?",
                (balance, stk)
            )

            db.commit()
            db.close()

            embed = discord.Embed(
                title="💰 Cộng tiền thành công",
                color=discord.Color.green()
            )

            embed.add_field(
                name="🏦 STK",
                value=stk,
                inline=False
            )

            embed.add_field(
                name="💵 Đã cộng",
                value=f"{so_tien:,} VNĐ",
                inline=False
            )

            embed.add_field(
                name="💳 Số dư mới",
                value=f"{balance:,} VNĐ",
                inline=False
            )

            await interaction.response.send_message(embed=embed)

        except Exception as e:
            print(e)

            if not interaction.response.is_done():
                await interaction.response.send_message(
                    f"❌ Lỗi: {e}",
                    ephemeral=True
                )

    @congtien.error
    async def congtien_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                "❌ Chỉ người có quyền **Administrator** mới được sử dụng lệnh này.",
                ephemeral=True
            )
        else:
            print(error)

async def setup(bot):
    await bot.add_cog(CongTien(bot))
