import discord
from discord.ext import commands
from discord import app_commands
import sqlite3

class CongTien(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="congtien",
        description="Cộng tiền cho tài khoản (Admin)"
    )
    @app_commands.default_permissions(administrator=True)
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

            data = cursor.fetchone()

            if data is None:
                await interaction.response.send_message(
                    "❌ Không tìm thấy số tài khoản.",
                    ephemeral=True
                )
                db.close()
                return

            cursor.execute(
                "UPDATE accounts SET balance = balance + ? WHERE account_number=?",
                (so_tien, stk)
            )

            db.commit()
            db.close()

            await interaction.response.send_message(
                f"✅ Đã cộng **{so_tien:,} VNĐ** vào STK **{stk}**."
            )

        except Exception as e:
            print(f"[CONGTIEN] {e}")

            if not interaction.response.is_done():
                await interaction.response.send_message(
                    "❌ Có lỗi xảy ra khi cộng tiền.",
                    ephemeral=True
                )

async def setup(bot):
    await bot.add_cog(CongTien(bot))
