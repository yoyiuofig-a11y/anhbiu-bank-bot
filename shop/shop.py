import discord
from discord.ext import commands
from discord import app_commands

from .views import ShopView


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
                "Chào mừng đến **AnhBiu Shop**!\n\n"
                "📦 Chọn vật phẩm trong menu bên dưới để xem chi tiết và mua.\n\n"
                "💰 Mua vật phẩm\n"
                "📦 Lưu vào kho đồ\n"
                "📝 Lưu lịch sử giao dịch"
            ),
            color=0x2ECC71
        )

        embed.add_field(
            name="🛍️ Danh mục",
            value=(
                "🍎 Đồ ăn\n"
                "🛠️ Công cụ\n"
                "💻 Thiết bị\n"
                "🎁 Quà tặng\n"
                "💎 Vật phẩm hiếm\n"
                "🚗 Phương tiện\n"
                "🏠 Nhà cửa"
            ),
            inline=False
        )

        embed.set_thumbnail(url=interaction.guild.icon.url if interaction.guild and interaction.guild.icon else discord.Embed.Empty)

        embed.set_footer(
            text=f"Người dùng: {interaction.user.display_name}"
        )

        await interaction.response.send_message(
            embed=embed,
            view=ShopView()
        )


async def setup(bot):
    await bot.add_cog(AnhBiuShop(bot))
