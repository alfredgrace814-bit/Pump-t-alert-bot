import requests
import time

# ────────────────────────────────────────────────
#   Your Telegram bot credentials – KEEP SECRET!
# ────────────────────────────────────────────────
TOKEN = "8704324795:AAFEwg5zU-jCRDbTtHkozpR6vjyuMqaLWrc"
CHAT_ID = "-1003205569356"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

# Global variable to avoid sending duplicate alerts for the same mint
last_seen_mint = None

def send_message(text):
    """Send message to your Telegram channel/group"""
    url = f"{BASE_URL}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        # Removed parse_mode so we avoid MarkdownV2 escaping issues
        # If you want formatting later, add back with proper escaping
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        print("Message sent successfully:", response.json())
    except Exception as e:
        print("Failed to send message:", str(e))


def check_for_new_tokens():
    """Check recent Pump.fun trades for new/recent token activity"""
    global last_seen_mint
    try:
        # PumpPortal public endpoint for recent trades (2026 working alternative)
        # Returns list of recent trades including mint addresses
        r = requests.get("https://pumpportal.fun/api/trade-recent?limit=10", timeout=15)
        r.raise_for_status()

        trades = r.json()  # should be list of dicts

        print(f"Received {len(trades)} recent trades from API")

        # Process from oldest to newest (catch everything new)
        for trade in reversed(trades):
            mint = trade.get("mint")
            if not mint:
                continue

            # Skip if we already sent alert for this mint
            if last_seen_mint and mint == last_seen_mint:
                continue

            # Get token info (adapt keys based on actual response)
            name = trade.get("name", trade.get("symbol", "Unknown Token"))
            symbol = trade.get("symbol", "")

            # Simple alert format – no MarkdownV2 to avoid escaping problems
            text = (
                f"New Pump.fun Activity! 🚀\n"
                f"Token: {name} ({symbol})\n"
                f"CA: {mint[:6]}...{mint[-6:]}\n"
                f"Link: https://pump.fun/{mint}\n"
                f"Recent trade detected – check it out!"
            )

            send_message(text)
            print(f"Alert sent for: {name} – {mint}")

            last_seen_mint = mint  # remember this mint

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {str(e)}")
        if 'r' in locals():
            print("Response preview:", r.text[:300])
    except Exception as e:
        print(f"Unexpected error in check_for_new_tokens: {str(e)}")


if __name__ == "__main__":
    print("Bot started - monitoring Pump.fun recent activity...")
    while True:
        try:
            check_for_new_tokens()
        except Exception as e:
            print(f"Main loop caught error (will continue): {str(e)}")

        print(f"Waiting 60 seconds until next check... ({time.strftime('%Y-%m-%d %H:%M:%S')})")
        time.sleep(60)  # Check every 60 seconds
