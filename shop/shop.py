import discord
from discord.ext import commands
from discord import app_commands

class AnhBiuShop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="shop",
        description="Mở cửa hàng AnhBiu Shop"
    )
    async def shop(self, interaction: discord.Interaction):

        embed = discord.Embed(
            title="🛒 AnhBiu Shop",
            description=(
                "**Chọn một chức năng:**\n\n"
                "🛍️ Cửa hàng\n"
                "📦 Kho đồ\n"
                "📜 Lịch sử mua\n"
                "🎁 Khuyến mãi\n"
                "⭐ Sản phẩm nổi bật"
            ),
            color=0x2ECC71
        )

        embed.set_footer(text="AnhBiu Shop")

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(AnhBiuShop(bot))
