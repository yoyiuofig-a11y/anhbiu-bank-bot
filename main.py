import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
import random
from datetime import datetime
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

db = sqlite3.connect("bank.db")
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts(
    user_id TEXT PRIMARY KEY,
    account_id TEXT,
    account_number TEXT,
    cccd TEXT,
    balance INTEGER,
    created_at TEXT
)
""")
db.commit()

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"{bot.user} đã hoạt động!")

@bot.tree.command(name="dangky", description="Đăng ký tài khoản ngân hàng")
async def dangky(interaction: discord.Interaction):

    user = str(interaction.user.id)

    cursor.execute("SELECT * FROM accounts WHERE user_id=?", (user,))
    if cursor.fetchone
