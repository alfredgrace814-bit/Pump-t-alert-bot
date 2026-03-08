import requests
import time

# ────────────────────────────────────────────────
#   Telegram bot credentials – KEEP THESE SECRET!
# ────────────────────────────────────────────────
TOKEN = "8704324795:AAFEwg5zU-jCRDbTtHkozpR6vjyuMqaLWrc"
CHAT_ID = "-1003205569356"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

# Remember the last alerted mint to avoid duplicate messages
last_seen_mint = None

def send_message(text):
    """Send a message to your Telegram channel/group"""
    url = f"{BASE_URL}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        # No parse_mode → plain text = no escaping problems
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        print("Message sent OK:", response.json().get("ok"))
    except Exception as e:
        print("Failed to send message:", str(e))


def check_for_new_tokens():
    """Check for recent new token pairs on Solana (many from Pump.fun)"""
    global last_seen_mint
    try:
        print("Checking Birdeye for new token pairs...")
        # Birdeye public API – new token pairs on Solana, sorted by creation time
        r = requests.get(
            "https://public-api.birdeye.so/defi/v3/token/new_pairs?sort_by=created_timestamp&sort_type=desc&limit=5&network=solana",
            timeout=15
        )
        r.raise_for_status()

        data = r.json()
        pairs = data.get("data", {}).get("items", [])

        print(f"Received {len(pairs)} recent new token pairs")

        # Process from oldest to newest (catch new ones in order)
        for pair in reversed(pairs):
            mint = pair.get("base", {}).get("address")
            if not mint:
                continue

            if last_seen_mint and mint == last_seen_mint:
                continue  # already alerted

            name = pair.get("base", {}).get("symbol", "Unknown")
            symbol = pair​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​
