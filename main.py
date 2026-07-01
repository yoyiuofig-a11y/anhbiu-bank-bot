import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    print("=" * 40)
    print(f"🤖 {bot.user} đã sẵn sàng!")
    print("=" * 40)

    try:
        synced = await bot.tree.sync()
        print(f"✅ Đã đồng bộ {len(synced)} Slash Commands")
    except Exception as e:
        print(e)

async def load_cogs():

    for file in os.listdir("./commands"):

        if file.endswith(".py"):

            await bot.load_extension(
                f"commands.{file[:-3]}"
            )

async def main():

    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

import asyncio
asyncio.run(main()))
async def ping(interaction: discord.Interaction):

    await interaction.response.send_message(
        f"🏓 Pong!\n{round(bot.latency*1000)}ms"
    )

# Các lệnh ngân hàng sẽ được thêm ở đây

bot.run(TOKEN)async def dangky(interaction: discord.Interaction):

    user = str(interaction.user.id)

    cursor.execute("SELECT * FROM accounts WHERE user_id=?", (user,))
    if cursor.fetchone
