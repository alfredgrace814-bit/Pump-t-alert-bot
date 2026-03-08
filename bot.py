def check_for_new_tokens():
    global last_seen_mint
    try:
        print("Checking Birdeye new token pairs...")
        r = requests.get(
            "https://public-api.birdeye.so/defi/v3/token/new_pairs?sort_by=created_timestamp&sort_type=desc&limit=5&network=solana",
            timeout=15
        )
        r.raise_for_status()

        data = r.json()
        pairs = data.get("data", {}).get("items", [])

        print(f"Received {len(pairs)} new token pairs")

        for pair in reversed(pairs):
            mint = pair.get("base", {}).get("address")
            if not mint or (last_seen_mint and mint == last_seen_mint):
                continue

            name = pair.get("base", {}).get("symbol", "Unknown")
            text = (
                f"New Solana Token Detected! 🚀 (likely Pump.fun)\n"
                f"Token: {name}\n"
                f"Mint/CA: {mint[:6]}...{mint[-6:]}\n"
                f"Link: https://pump.fun/{mint}\n"
                f"Birdeye: https://birdeye.so/token/{mint}?chain=solana"
            )

            send_message(text)
            print(f"Alert sent: {name} - {mint}")
            last_seen_mint = mint

    except Exception as e:
        print(f"Birdeye check failed: {str(e)}")
