import time
import requests
# Likely one of these for Telegram (adjust based on your imports)
# from telebot import TeleBot  # if using pyTelegramBotAPI
# or
# from telethon import TelegramClient, events, sync  # if using Telethon

# =====================================
# CONFIG - SET THESE AS ENVIRONMENT VARIABLES ON RAILWAY!
# =====================================
MORALIS_API_KEY = "your_moralis_api_key_here"  # From moralis.io dashboard
BOT_TOKEN = "your_telegram_bot_token_here"     # From @BotFather
CHANNEL_ID = -100103205569356                  # Your alert channel

# If using pyTelegramBotAPI (simpler):
bot = TeleBot(BOT_TOKEN)

# If using Telethon (async/MTProto - more powerful but needs API_ID/API_HASH):
# client = TelegramClient('session', API_ID, API_HASH)
# client.start(bot_token=BOT_TOKEN)

POLL_INTERVAL = 30  # seconds between checks

last_seen_mint = None  # Global to track the latest processed mint

def send_alert(text):
    """Send message to your Telegram channel."""
    try:
        bot.send_message(CHANNEL_ID, text, parse_mode='HTML')  # or 'Markdown'
        print(f"Alert sent: {text[:50]}...")
    except Exception as e:
        print(f"Telegram send failed: {e}")

print("Pump.fun Alert Bot starting...")

while True:
    """Fetch new Pump.fun tokens using Moralis API"""
    global last_seen_mint
    try:
        print("Fetching new Pump.fun tokens...")
        headers = {"X-API-Key": MORALIS_API_KEY}
        r = requests.get(
            "https://solana-gateway.moralis.io/token/mainnet/exchange/pumpfun/new",
            headers=headers,
            timeout=15,
        )
        r.raise_for_status()
        data = r.json()
        tokens = data.get("result", [])
        print(f"Received {len(tokens)} new tokens")

        for token in reversed(tokens):  # Process newest first
            mint = token.get("mint")
            if not mint or (last_seen_mint and mint == last_seen_mint):
                continue  # Skip if no mint or already processed

            name = token.get("name", "Unknown")
            symbol = token.get("symbol", "???")
            # Add more fields if available in response, e.g. description, image_uri, etc.

            text = (
                f"<b>New Pump.fun Token Launch!</b>\n"
                f"Token: {name} ({symbol})\n"
                f"CA: <code>{mint[:6]}...{mint[-4:]}</code>\n"
                # Optional extras:
                # f"Description: {token.get('description', 'N/A')}\n"
                # f"Buy: https://pump.fun/{mint}\n"
            )

            send_alert(text)

            # Update to the newest one after processing
            last_seen_mint = mint

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    time.sleep(POLL_INTERVAL)
