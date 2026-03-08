import requests
import time

# Your details — keep secret!
TOKEN = "8704324795:AAFEwg5zU-jCRDbTtHkozpR6vjyuMqaLWrc"
CHAT_ID = "-1003205569356"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

def send_message(text):
    url = f"{BASE_URL}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
    }
    response = requests.post(url, json=payload)
    print(response.json())  # For debugging

# ────────────────────────────────────────────────
#   ← Replace the whole function body with this →
# ────────────────────────────────────────────────

last_seen_mint = None   # We remember the last alerted token to avoid duplicates

def check_for_new_tokens():
    global last_seen_mint
    try:
        # Get the 5 most recent projects/launches from Pump.fun
        r = requests.get("https://pump.fun/api/projects?sort=recent&limit=5")
        if not r.ok:
            print(f"Pump.fun API error: {r.status_code} - {r.text}")
            return

        projects = r.json()

        # Process from oldest to newest so we catch everything new
        for project in reversed(projects):
            mint = project.get('mint')
            if not mint:
                continue

            # Only alert if we haven't seen this mint before
            if last_seen_mint is None or mint != last_seen_mint:
                name = project.get('name', 'Unknown')
                symbol = project.get('symbol', '')
                # market cap is usually in lamports → very rough USD estimate
                mc_sol = project.get('marketCap', 0) / 1_000_000_000
                mc_usd_approx = mc_sol * 150  # assuming ~$150 per SOL

                text = (
                    f"*New Pump.fun Launch!* 🚀\n"
                    f"Token: *{name}* ({symbol})\n"
                    f"CA: `{mint[:6]}...{mint[-4:]}`\n"
                    f"Market Cap: ~${mc_usd_approx:,.0f}\n"
                    f"[Buy on Pump.fun](https://pump.fun/{mint})\n"
                    f"Don't miss it!"
                )

                send_message(text)
                print(f"Real alert sent → {name} ({mint})")

                last_seen_mint = mint  # remember this one

    except Exception as e:
        print(f"Error while checking new tokens: {str(e)}")

# ────────────────────────────────────────────────

if __name__ == "__main__":
    print("Bot started (polling simulation)...")
    while True:
        check_for_new_tokens()
        time.sleep(60)  # Check every minute
