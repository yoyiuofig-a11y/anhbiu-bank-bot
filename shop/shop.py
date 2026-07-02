import discord
from discord.ext import commands
from discord import app_commands

class AnhBiuShop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="shop",
        description="Mở AnhBiu Shop"
    )
    async def shop(self, interaction: discord.Interaction):

        embed = discord.Embed(
            title="🛒 AnhBiu Shop",
            description=(
                "Chào mừng đến với AnhBiu Shop!\n\n"
                "Sắp có các danh mục:\n"
                "🍜 Mì ăn liền\n"
                "🥤 Đồ uống\n"
                "🍪 Bánh kẹo\n"
                "🧴 Gia dụng\n"
                "🎁 Quà tặng\n"
                "🎮 Thẻ game\n"
                "💎 Discord Nitro"
            ),
            color=discord.Color.green()
        )

        embed.set_footer(text="AnhBiu Shop")

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(AnhBiuShop(bot))
