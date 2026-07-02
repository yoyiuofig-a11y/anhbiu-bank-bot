import discord
import json

from .buttons import BuyView


class ShopSelect(discord.ui.Select):
    def __init__(self):

        with open("data/items.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        options = []

        for item in data["items"]:

            options.append(
                discord.SelectOption(
                    label=item["name"],
                    description=f"{item['price']}$",
                    value=str(item["id"])
                )
            )

        super().__init__(
            placeholder="🛒 Chọn vật phẩm...",
            min_values=1,
            max_values=1,
            options=options[:25]  # Discord chỉ cho tối đa 25 lựa chọn mỗi menu
        )

    async def callback(self, interaction: discord.Interaction):

        with open("data/items.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        item = next(
            i for i in data["items"]
            if str(i["id"]) == self.values[0]
        )

        embed = discord.Embed(
            title=item["name"],
            description=item["description"],
            color=0x2ECC71
        )

        embed.add_field(
            name="💰 Giá",
            value=f"{item['price']}$"
        )

        await interaction.response.send_message(
            embed=embed,
            view=BuyView(item),
            ephemeral=True
        )


class ShopView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ShopSelect())
