last_seen_mint = None

def check_for_new_tokens():
    global last_seen_mint
    try:
        # Working public endpoint for recent Pump.fun trades (includes new tokens)
        r = requests.get("https://pumpportal.fun/api/trade-recent?limit=10")
        r.raise_for_status()  # raise if not 200

        trades = r.json()

        for trade in reversed(trades):
            mint = trade.get("mint")
            if not mint or (last_seen_mint and mint == last_seen_mint):
                continue

            name = trade.get("name", "Unknown")
            symbol = trade.get("symbol", "")
            text = (
                f"*New Pump.fun Activity!* 🚀\n"
                f"Token: *{name}* ({symbol})\n"
                f"CA: `{mint[:6]}...{mint[-6:]}`\n"
                f"[View on Pump.fun](https://pump.fun/{mint})\n"
                f"Recent trade detected!"
            )
            send_message(text)
            print(f"Alert sent: {name} - {mint}")
            last_seen_mint = mint

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
