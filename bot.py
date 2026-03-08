def check_for_new_tokens():
    global last_seen_mint
    try:
        # Working public endpoint for recent Pump.fun activity (trades/tokens)
        # From PumpPortal (2026) - returns recent trades with mints
        r = requests.get("https://pumpportal.fun/api/trade-recent?limit=10")
        if not r.ok:
            print(f"API call failed: {r.status_code} - {r.text[:300]}...")  # show error snippet
            return

        trades = r.json()  # assume array of recent trades

        for trade in reversed(trades[:5]):  # last 5, oldest first to catch new
            mint = trade.get("mint")
            if not mint:
                continue

            # Skip if we already alerted this mint
            if last_seen_mint and mint == last_seen_mint:
                continue

            # Extract data (adapt based on actual response format - check logs)
            name = trade.get("name", trade.get("symbol", "Unknown"))
            text = (
                f"*New Pump.fun Activity!* 🚀\n"
                f"Token: *{name}*\n"
                f"CA: `{mint[:6]}...{mint[-4:]}`\n"
                f"[View on Pump.fun](https://pump.fun/{mint})\n"
                f"Recent trade detected - check it out!"
            )

            send_message(text)
            print(f"Alert sent for mint: {mint} (name: {name})")

            last_seen_mint = mint  # update to avoid repeats

    except Exception as e:
        print(f"Error in check_for_new_tokens: {str(e)}")
