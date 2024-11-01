# bot.py
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load the .env file containing the bot token and other variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

# Set up intents and bot instance
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)

# Load the 'ask' cog
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    # Load the cog for asking questions
    await bot.load_extension("cogs.ask")

bot.run(TOKEN)
