import discord
from discord import app_commands
from discord.ext import commands

class DangKy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="dangky", description="Đăng ký tài khoản ngân hàng")
    async def dangky(self, interaction: discord.Interaction):
        await interaction.response.send_message("✅ Đăng ký thành công!")

async def setup(bot):
    await bot.add_cog(DangKy(bot))        if cursor.fetchone():
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
            async def setup(bot):
    await bot.add_cog(DangKy(bot))
