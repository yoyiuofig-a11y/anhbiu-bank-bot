import discord
from discord.ext import commands
from discord import app_commands

class ShopView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🛍️ Cửa hàng", style=discord.ButtonStyle.green)
    async def shop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🛒 Đang mở cửa hàng...", ephemeral=True)

    @discord.ui.button(label="📦 Kho đồ", style=discord.ButtonStyle.blurple)
    async def inventory_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("📦 Đang mở kho đồ...", ephemeral=True)

    @discord.ui.button(label="📜 Lịch sử", style=discord.ButtonStyle.gray)
    async def history_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("📜 Đang mở lịch sử mua...", ephemeral=True)

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
            description="Chào mừng đến với **AnhBiu Shop**!\n\nHãy chọn một chức năng bên dưới.",
            color=0x2ECC71
        )

        embed.add_field(
            name="✨ Chức năng",
            value=(
                "🛍️ Cửa hàng\n"
                "📦 Kho đồ\n"
                "📜 Lịch sử mua\n"
                "🎁 Khuyến mãi\n"
                "⭐ Sản phẩm nổi bật"
            ),
            inline=False
        )

        embed.set_footer(text="AnhBiu Shop")

        await interaction.response.send_message(
            embed=embed,
            view=ShopView()
        )

async def setup(bot):
    await bot.add_cog(AnhBiuShop(bot))
