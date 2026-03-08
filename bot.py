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
        "parse_mode": "MarkdownV2"
    }
    response = requests.post(url, json=payload)
    print(response.json())  # For debugging

# Example alert function (later replace with real Pump.fun monitoring)
def check_for_new_tokens():
    # Placeholder: in real version, query Solana RPC or Pump.fun API
    # For testing: send dummy alert every 60 seconds
    message = (
        "*New Pump\\.fun Launch\\!* 🚀\n"
        "Token: *TESTCOIN*\n"
        "CA: `FakePump123abc...`\n"
        "Market Cap: \\~$8k\n"
        "[Buy on Pump\\.fun](https://pump.fun/FakePump123abc...)\n"
        "Don't miss it!"
    )
    send_message(message)

if __name__ == "__main__":
    print("Bot started (polling simulation)...")
    while True:
        check_for_new_tokens()
        time.sleep(60)  # Check every minute
