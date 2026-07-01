import os
import sqlite3
from threading import Thread

from flask import Flask
import discord
from discord.ext import commands

# ================= WEB SERVER =================

app = Flask(__name__)

@app.route("/")
def home():
    return "AnhBiu Bank Bot đang chạy!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

Thread(target=run_web).start()

# ================= DISCORD =================

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise Exception("Thiếu biến môi trường TOKEN")

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

@bot.event
async def setup_hook():
    print("📦 Đang tải commands...")

    if os.path.exists("commands"):
        for file in os.listdir("commands"):
            if file.endswith(".py") and file != "__init__.py":
                try:
                    await bot.load_extension(f"commands.{file[:-3]}")
                    print(f"✅ {file}")
                except Exception as e:
                    print(f"❌ {file}: {e}")

# ================= READY =================

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"✅ Đồng bộ {len(synced)} slash commands")
    except Exception as e:
        print(e)

    print("=" * 40)
    print(f"🤖 {bot.user}")
    print(f"🌍 {len(bot.guilds)} server")
    print("=" * 40)

bot.run(TOKEN)
