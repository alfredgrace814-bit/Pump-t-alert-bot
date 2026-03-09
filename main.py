import os
import time
import requests
from telebot import TeleBot
from telebot.apihelper import ApiTelegramException

# Load config from Railway environment variables
MORALIS_API_KEY = os.getenv("MORALIS_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Safety checks - exit early if anything is missing
if not MORALIS_API_KEY:
    print("ERROR: MORALIS_API_KEY is not set in Railway Variables")
    exit(1)

if not BOT_TOKEN:
    print("ERROR: BOT_TOKEN is not set in Railway Variables")
    exit(1)

if not CHANNEL_ID:
    print("ERROR: CHANNEL_ID is not set in Railway Variables")
    exit(1)

# Convert CHANNEL_ID to integer (Telegram requires int for channels)
try:
    CHANNEL_ID = int(CHANNEL_ID)
except ValueError:
    print("ERROR: CHANNEL_ID must be a number like -1001234567890")
    exit(1)

# Initialize Telegram bot
bot = TeleBot(BOT_TOKEN)

# Track the latest processed mint to avoid duplicates
last_seen_mint = None

def send_message(text):
    try:
        bot.send_message(
            chat_id=CHANNEL_ID,
            text
