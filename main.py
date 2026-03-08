import requests
import time

# ────────────────────────────────────────────────
#   Telegram bot credentials – KEEP SECRET!
# ────────────────────────────────────────────────
TOKEN = "8704324795:AAFEwg5zU-jCRDbTtHkozpR6vjyuMqaLWrc"
CHAT_ID = "-1003205569356"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

# ────────────────────────────────────────────────
#   Moralis API key (get free at moralis.com)
#   Paste your key here ↓
# ────────────────────────────────────────────────
MORALIS_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6IjU1NzExMjE0LTVkODMtNDA2Ny1iYTg2LWNhZmNlNTFhN2YzOCIsIm9yZ0lkIjoiNTA0NDg0IiwidXNlcklkIjoiNTE5MDkyIiwidHlwZUlkIjoiMDlhMTlmZTEtNTM0Ny00MjAzLTg2NDAtNDY0MTM1MjQxYmYxIiwidHlwZSI6IlBST0pFQ1QiLCJpYXQiOjE3NzMwMDc2MDUsImV4cCI6NDkyODc2NzYwNX0.akkGXsOQgdPfN3e_4WHw9sVUcpv8xgV4TC6hWU_E2eQ"

# Remember last alerted mint to avoid duplicates
last_seen_mint = None

def send_message(text):
    """Send alert to Telegram channel/group"""
    url = f"{BASE_URL}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        print("Message sent successfully")
    except Exception as e:
        print("Send failed:", str(e))


def check_for_new_tokens():
    """Fetch new Pump.fun tokens using Moralis API"""
    global last_seen_mint
    try:
        print("Fetching new Pump.fun tokens from Moralis...")
        headers = {"X-API-Key": MORALIS_API_KEY}
        r = requests.get(
            "https://solana-gateway.moralis.io/token/mainnet/pump-fun/new?limit=5",
            headers=headers,
            timeout=15
        )
        r.raise_for_status()

        data = r.json()
        tokens = data.get("result", [])  # Moralis returns {"result": [...]}

        print(f"Received {len(tokens)} new tokens")

        for token in reversed(tokens):
            mint = token.get("mint")
            if not mint or (last_seen_mint and mint == last_seen_mint):
                continue

            name = token.get("name", "Unknown")
            symbol = token.get("symbol", "")

            text = (
                f"New Pump.fun Token Launched! 🚀\n"
                f"Token: {name} ({symbol})\n"
                f"CA: {mint[:6]}...{mint[-6:]}\n"
                f"Link: https://pump.fun/{mint}"
            )

            send_message(text)
            print(f"Alert sent → {name} ({mint})")
            last_seen_mint = mint

    except requests.exceptions.RequestException as e:
        print(f"Moralis API error: {str(e)}")
        if 'r' in locals():
            print("Response preview:", r.text[:300])
    except Exception as e:
        print(f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    print("Bot started - monitoring new Pump.fun tokens via Moralis...")
    
    while True:
        try:
            check_for_new_tokens()
        except Exception as e:
            print(f"Main loop caught error (bot keeps running): {str(e)}")
        
        print(f"Alive - next check in 60 seconds → {time.strftime('%Y-%m-%d %H:%M:%S')}")
        time.sleep(60)
