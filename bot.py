def check_for_new_tokens():
    global last_seen_mint
    try:
        print("Checking Birdeye recent token pairs...")
        # Birdeye public endpoint for new token pairs on Solana (sorted by created time desc)
        # limit=5 → most recent 5 new pairs (many are Pump.fun)
        r = requests.get(
            "https://public-api.birdeye.so/defi/v3/token/new_pairs?sort_by=created_timestamp&sort_type=desc&limit=5&network=solana",
            timeout=15
        )
        r.raise_for_status()

        data = r.json()
        pairs = data.get("data", {}).get("items", [])  # navigate to list of pairs

        print(f"Received {len(pairs)} recent token pairs")

        for pair in reversed(pairs):  # oldest first to catch new ones
            mint = pair.get("base", {}).get("address")
            if not mint:
                continue

            if last_seen_mint and mint == last_seen_mint:
                continue

            name = pair.get("base", {}).get("symbol", "Unknown")
            symbol = pair.get("base", {}).get("symbol", "")
            created = pair.get("created_timestamp", "")

            text = (
                f"New Solana Token Pair Detected! 🚀 (likely Pump.fun)\n"
                f"Token: {name} ({symbol})\n"
                f"CA/Mint: {mint[:6]}...{mint[-6:]}\n"
                f"Created: {created}\n"
                f"Check: https://pump.fun/{mint}\n"
                f"Birdeye: https://birdeye.so/token/{mint}?chain=solana"
            )

            send_message(text)
            print(f"Alert sent for mint: {mint} ({name})")
            last_seen_mint = mint

    except requests.exceptions.RequestException as e:
        print(f"Birdeye API failed: {str(e)}")
        if 'r' in locals():
            print("Response preview:", r.text[:300])
    except Exception as e:
        print(f"Unexpected error: {str(e)}")o
