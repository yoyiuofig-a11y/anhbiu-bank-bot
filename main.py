import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def setup_hook():
    print("📦 Đang tải commands...")

    for file in os.listdir("./commands"):

        if not file.endswith(".py"):
            continue

        if file == "__init__.py":
            continue

        extension = f"commands.{file[:-3]}"

        try:
            await bot.load_extension(extension)
            print(f"✅ Đã tải: {extension}")

        except commands.ExtensionAlreadyLoaded:
            print(f"⚠️ Đã tải trước: {extension}")

        except commands.NoEntryPointError:
            print(f"❌ {extension} thiếu async def setup(bot)")

        except commands.ExtensionFailed as e:
            print(f"❌ Lỗi trong {extension}")
            print(e)

        except Exception as e:
            print(f"❌ Không thể tải {extension}")
            print(e)

@bot.event
async def on_ready():
    synced = await bot.tree.sync()

    print("=" * 40)
    print(f"🤖 {bot.user}")
    print(f"🌍 Đã vào {len(bot.guilds)} server")
    print(f"📜 Đồng bộ {len(synced)} slash commands")
    print("=" * 40)
