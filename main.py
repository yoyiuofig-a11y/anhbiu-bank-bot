import discord
from discord.ext import commands
import sqlite3
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# Database
db = sqlite3.connect("bank.db")
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts(
    user_id TEXT PRIMARY KEY,
    account_id TEXT,
    account_number TEXT,
    cccd TEXT,
    balance INTEGER DEFAULT 0,
    created_at TEXT,
    status TEXT DEFAULT 'active'
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS logs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender TEXT,
    receiver TEXT,
    amount INTEGER,
    time TEXT
)
""")

db.commit()

@bot.event
async def setup_hook():
    for file in os.listdir("./commands"):
        if file.endswith(".py") and file != "__init__.py":
            await bot.load_extension(f"commands.{file[:-3]}")
            print(f"Đã tải {file}")

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"{bot.user} đã online!")

bot.run(TOKEN)            await bot.load_extension(
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
