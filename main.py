import os
import sqlite3
import discord
from discord.ext import commands

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# ===== Database =====

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

db.commit()

# ===== Load Commands =====

@bot.event
async def setup_hook():
    print("📦 Đang tải commands...")

    for file in os.listdir("commands"):
        if file.endswith(".py") and file != "__init__.py":
            try:
                await bot.load_extension(f"commands.{file[:-3]}")
                print(f"✅ Đã tải {file}")
            except Exception as e:
                print(f"❌ Lỗi {file}: {e}")

# ===== Ready =====

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"✅ Đã đồng bộ {len(synced)} slash commands")
    except Exception as e:
        print(e)

    print(f"🤖 {bot.user} đã online!")

bot.run(TOKEN)
