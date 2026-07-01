import os
import sqlite3
import discord
from discord.ext import commands

TOKEN = os.getenv("TOKEN")

if TOKEN is None:
    raise RuntimeError("Chưa tìm thấy biến môi trường TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# ================= DATABASE =================

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

# ================= LOAD COMMANDS =================

async def load_extensions():
    if not os.path.exists("commands"):
        print("❌ Không tìm thấy thư mục commands")
        return

    for file in os.listdir("commands"):
        if file.endswith(".py") and file != "__init__.py":
            extension = f"commands.{file[:-3]}"
            try:
                await bot.load_extension(extension)
                print(f"✅ Loaded {extension}")
            except Exception as e:
                print(f"❌ {extension}: {e}")

@bot.event
async def setup_hook():
    await load_extensions()

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"✅ Đồng bộ {len(synced)} slash commands")
    except Exception as e:
        print(e)

    print(f"🤖 {bot.user} đã online")

bot.run(TOKEN)
