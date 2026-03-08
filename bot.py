import requests
import time

TOKEN = "8704324795:AAFEwg5zU-jCRDbTtHkozpR6vjyuMqaLWrc"
CHAT_ID = "-1003205569356"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

last_seen_mint = None

def send_message(text):
    url = f"{BASE_URL}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        print("Sent OK:", response.json().get("ok"))
    except Exception as e:
        print("Send failed:", str(e))

def check_for_new_tokens():
    global last_seen_mint
    try:
        print("Checking Birdeye new pairs...")
        r = requests.get(
            "https://public-api.birdeye.so/defi/v3/token/new_pairs?sort_by=created_timestamp&sort_type=desc&limit=5&network=solana",
            timeout=15
        )
        r.raise_for_status()

        data = r.json()
        pairs = data.get("data", {}).get("items", [])

        print(f"Got {len(pairs)} pairs")

        for pair in reversed(pairs):
            mint = pair.get("base", {}).get("address")
            if not mint or (last_seen_mint and mint == last_seen_mint):
                continue

            name = pair.get("base", {}).get("symbol", "Unknown")
            text = (
                f"New token detected! 🚀\n"
                f"Name: {name}\n"
                f"CA: {mint[:6]}...{mint[-6:]}\n"
                f"https://pump.fun/{mint}"
            )
            send_message(text)
            print(f"Alert: {name} - {mint}")
            last_seen_mint = mint

    except Exception as e:
        print("Check failed:", str(e))

if __name__ == "__main__":
    print("Bot started...")
    while True:
        try:
            check_for_new_tokens()
        except Exception as e:
            print("Loop error (continuing):", str(e))
        print("Alive, next in 60s...", time.strftime("%Y-%m-%d %H:%M:%S"))
        time.sleep(60)
