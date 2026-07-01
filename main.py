import os
import sqlite3
import discord
from discord.ext import commands

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

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
    for file in os.listdir("commands"):
        if file.endswith(".py") and file != "__init__.py":
            try:
                await bot.load_extension(f"commands.{file[:-3]}")
                print(f"Đã tải {file}")
            except Exception as e:
                print(f"Lỗi {file}: {e}")

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"{bot.user} đã online!")

bot.run(TOKEN)
