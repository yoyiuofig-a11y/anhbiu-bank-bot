import os
import sqlite3
from threading import Thread

from flask import Flask
import discord
from discord.ext import commands

# ==========================
# WEB SERVER
# ==========================

app = Flask(__name__)

@app.route("/")
def home():
    return "🤖 AnhBiu Bot đang hoạt động!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

Thread(target=run_web, daemon=True).start()

# ==========================
# DISCORD BOT
# ==========================

TOKEN = os.getenv("TOKEN")

if TOKEN is None:
    raise Exception("❌ Không tìm thấy TOKEN!")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

# ==========================
# DATABASE
# ==========================

db = sqlite3.connect(
    "bank.db",
    check_same_thread=False
)

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

# ==========================
# LOAD COMMANDS
# ==========================

@bot.event
async def setup_hook():

    print("=" * 40)
    print("📦 Đang tải Commands...")
    print("=" * 40)

    if not os.path.exists("commands"):
        os.mkdir("commands")

    for file in os.listdir("commands"):

        if file.endswith(".py") and file != "__init__.py":

            try:
                await bot.load_extension(
                    f"commands.{file[:-3]}"
                )

                print(f"✅ Đã tải {file}")

            except Exception as e:

                print(f"❌ Lỗi {file}")
                print(e)

    try:
        synced = await bot.tree.sync()
        print(f"\n✅ Đồng bộ {len(synced)} Slash Commands")

    except Exception as e:
        print(f"❌ Sync lỗi: {e}")

# ==========================
# EVENTS
# ==========================

@bot.event
async def on_ready():

    print("=" * 40)
    print(f"🤖 Bot: {bot.user}")
    print(f"🆔 ID: {bot.user.id}")
    print(f"🌍 Servers: {len(bot.guilds)}")
    print("=" * 40)

# ==========================
# START BOT
# ==========================

bot.run(TOKEN)
