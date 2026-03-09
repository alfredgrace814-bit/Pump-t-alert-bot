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

# Track the latest mint we've already alerted about
last_seen_mint = None

def send_message(text):
    try:
        bot.send_message(
            chat_id=CHANNEL_ID,
            text=text,
            parse_mode='HTML',
            disable_web_page_preview=True
        )
        print(f"[SENT] {text[:80]}...")
    except ApiTelegramException as e:
        print(f"[TELEGRAM ERROR] {e}")
    except Exception as e:
        print(f"[SEND ERROR] {type(e).__name__}: {e}")

# Startup message
print("Pump.fun new token alert bot started")
print(f"Channel ID: {CHANNEL_ID}")
print("Polling every 30 seconds...")

# One-time test message on startup (remove this line after you see it in channel)
send_message("Test message from Railway bot – I'm alive! 🚀\n(remove this line from code after testing)")

while True:
    try:
        print("Fetching recent Pump.fun tokens from Moralis...")
        headers = {
            "X-API-Key": MORALIS_API_KEY,
            "accept": "application/json"
        }

        r = requests.get(
            "https://solana-gateway.moral.io/token/mainnet/exchange/pumpfun/new",
            headers=headers,
            timeout=15
        )

        r.raise_for_status()
        data = r.json()
        tokens = data.get("result", [])

        print(f"Received {len(tokens)} tokens")

        # Process newest first
        for token in reversed(tokens):
            mint = token.get("mint")
            if not mint:
