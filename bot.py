def check_for_new_tokens():
    global last_seen_mint
    try:
        print("Fetching recent new token pairs from Birdeye...")
        r = requests.get(
            "https://public-api.birdeye.so/defi/v3/token/new_pairs?sort_by=created_timestamp&sort_type=desc&limit=5&network=solana",
            timeout=15
        )
        r.raise_for_status()

        data = r.json()
        pairs = data.get("data", {}).get("items", [])

        print(f"Got {len(pairs)} recent new token pairs")

        for pair in reversed(pairs):  # oldest to newest
            mint = pair.get("base", {}).get("address")
            if not mint:
                continue

            if last_seen_mint and mint == last_seen_mint:
                continue

            name = pair.get("base", {}).get("symbol", "Unknown")
            symbol = pair.get("base", {}).get("symbol", "")
            created = pair.get("created_timestamp", "recent")

            text = (
                f"New Solana Token Launched! 🚀 (likely Pump.fun)\n"
                f"Token: {name} ({symbol})\n"
                f"Mint/CA: {mint[:6]}...{mint[-6:]}\n"
                f"Created: {created}\n"
                f"Pump.fun: https://pump.fun/{mint}\n"
                f"Birdeye: https://birdeye.so/token/{mint}?chain=solana"
            )

            send_message(text)
            print(f"Sent alert for mint: {mint} ({name})")
            last_seen_mint = mint

    except requests.exceptions.RequestException as e:
        print(f"Birdeye API error: {str(e)}")
        if 'r' in locals():
            print("Response preview:", r.text[:300])
    except Exception as e:
        print(f"Unexpected error in check: {str(e)}")
    
