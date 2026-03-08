def check_for_new_tokens():
    global last_seen_mint
    try:
        # Use a working public/third-party endpoint for recent/new Pump.fun tokens
        # This one is from community sources (2026 era) – may need adjustment if it changes
        # Alternative: sign up for free Moralis key and use their /pump-fun/new endpoint
        r = requests.get("https://api.pumpportal.fun/api/trade-recent")  # example recent trades endpoint – returns list with mints
        # Or try this for new tokens if the above 404s: "https://pumpportal.fun/data-api/recent"
        
        if not r.ok:
            print(f"API call failed: {r.status_code} - {r.text[:200]}...")  # print first 200 chars of error
            return

        data = r.json()
        # The response format varies – adapt based on what you see in logs
        # Assuming it returns array of objects with 'mint', 'name', etc.
        recent_tokens = data.get("tokens", data)  # adjust key if needed

        for token in reversed(recent_tokens[:5]):  # last 5, oldest first
            mint = token.get("mint")
            if not mint or (last_seen_mint and mint == last_seen_mint):
                continue

            name = token.get("name", token.get("symbol", "Unknown"))
            text = (
                f"*New Pump.fun Launch!* 🚀\n"
                f"Token: *{name}*\n"
                f"CA: `{mint[:6]}...{mint[-4:]}`\n"
                f"[Buy on Pump.fun](https://pump.fun/{mint})\n"
                f"Don't miss it!"
            )
            send_message(text)
            print(f"Sent real alert for {name} - {mint}")
            last_seen_mint = mint  # update to skip duplicates next time

    except Exception as e:
        print(f"Check failed: {str(e)}")
