import discord
import json

from .database import remove_money, add_item, add_history


class BuyButton(discord.ui.Button):
    def __init__(self, item):
        self.item = item

        super().__init__(
            label=f"Mua ({item['price']}$)",
            style=discord.ButtonStyle.green,
            emoji="🛒"
        )

    async def callback(self, interaction: discord.Interaction):

        success = remove_money(
            interaction.user.id,
            self.item["price"]
        )

        if not success:
            await interaction.response.send_message(
                "❌ Bạn không đủ tiền!",
                ephemeral=True
            )
            return

        add_item(
            interaction.user.id,
            self.item["name"]
        )

        add_history(
            interaction.user.id,
            f"Đã mua {self.item['name']} ({self.item['price']}$)"
        )

        await interaction.response.send_message(
            f"✅ Bạn đã mua **{self.item['name']}** với giá **{self.item['price']}$**",
            ephemeral=True
        )


class BuyView(discord.ui.View):
    def __init__(self, item):
        super().__init__(timeout=120)

        self.add_item(BuyButton(item))
