import os
import time
import requests
from telebot import TeleBot
from telebot.apihelper import ApiTelegramException

# ==============================================
# Load configuration from environment variables
# (set these in Railway Variables tab)
# ==============================================
MORALIS_API_KEY = os.getenv("MORALIS_API_KEY")
BOT_TOKEN       = os.getenv("BOT_TOKEN")
CHANNEL_ID      = os.getenv("CHANNEL_ID")

if not MORALIS_API_KEY:
    print("ERROR: MORALIS_API_KEY environment variable is not set")
    exit(1)
if not BOT_TOKEN:
    print("ERROR: BOT_TOKEN environment variable is not set")
    exit(1)
if not CHANNEL_ID:
    print("ERROR: CHANNEL_ID environment variable is not set")
    exit(1)

# Convert CHANNEL_ID to integer (Telegram expects int for channels)
try:
    CHANNEL_ID = int(CHANNEL_ID)
except ValueError:
    print("ERROR: CHANNEL_ID must be a valid integer (e.g. -1001234567890)")
    exit(1)

# Initialize Telegram bot
bot = TeleBot(BOT_TOKEN)

# Global variable to remember the last seen mint
last_seen_mint = None

def send_message(text):
    try:
        bot.send_message(
            chat_id=CHANNEL_ID,
            text=text,
            parse_mode='HTML',
            disable_web_page_preview=True
        )
        print(f"Message sent to channel: {text[:60]}...")
    except ApiTelegramException as e:
        print(f"Telegram error: {e}")
    except Exception as e:
        print(f"Failed to send message: {e}")

print("Pump.fun new token alert bot started")
print(f"Channel ID: {CHANNEL_ID}")
print(f"Polling every 30 seconds...")

while True:
    try:
        print("Fetching recent Pump.fun tokens from Moralis...")
        headers = {
            "X-API-Key": MORALIS_API_KEY,
            "accept": "application/json"
        }

        response = requests.get(
            "https://solana-gateway.moralis.io/token/mainnet/exchange/pumpfun/new",
            headers=headers,
            timeout=15
        )

        response.raise_for_status()
        data = response.json()
        tokens = data.get("result", [])

        print(f"Received {len(tokens)} tokens")

        # Process from newest to oldest
        for token in reversed(tokens):
            mint = token.get("mint")
            if not mint:
                continue

            # Skip if we've already seen this mint or older
            if last_seen_mint and mint == last_seen_mint:
                break  # since list is sorted, we can stop here

            name    = token.get("name",    "Unknown")
            symbol  = token.get("symbol",  "???")
            # uri     = token.get("uri",     None)     # if you want metadata later

            message = (
                f"<b>🚀 New Pump.fun Token Launched!</b>\n\n"
                f"• Name: <b>{name}</b>\n"
                f"• Symbol: <b>{symbol}</b>\n"
                f"• CA: <code>{mint[:6]}...{mint[-4:]}</code>\n"
                f"\n"
                f"https://pump.fun/{mint}"
            )

            send_message(message)

            # Update last seen (only after successful processing)
            last_seen_mint = mint

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
    except Exception as e:
        print(f"Unexpected error in main loop: {type(e).__name__}: {e}")

    # Wait before next poll
    time.sleep(30)
