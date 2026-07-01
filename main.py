import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from database import *

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
    await bot.tree.sync()

    print("=" * 40)
    print("🏦 AnhBiu Bank đã khởi động")
    print(f"🤖 Bot: {bot.user}")
    print(f"🌍 Servers: {len(bot.guilds)}")
    print("=" * 40)

# ==========================
# /ping
# ==========================

@bot.tree.command(
    name="ping",
    description="Kiểm tra bot"
)
async def ping(interaction: discord.Interaction):

    await interaction.response.send_message(
        f"🏓 Pong!\n{round(bot.latency*1000)}ms"
    )

# Các lệnh ngân hàng sẽ được thêm ở đây

bot.run(TOKEN)async def dangky(interaction: discord.Interaction):

    user = str(interaction.user.id)

    cursor.execute("SELECT * FROM accounts WHERE user_id=?", (user,))
    if cursor.fetchone
