import requests
from datetime import datetime, timezone

URL = "https://api.bybit.com/v5/market/tickers"

params = {
    "category": "linear"
}

print("=" * 60)
print("BYBIT GAINER / LOSER ANALYZER")
print("=" * 60)

try:
    response = requests.get(
        URL,
        params=params,
        timeout=30,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    print("HTTP Status:", response.status_code)

    response.raise_for_status()

    try:
        data = response.json()
    except ValueError:
        print("ERROR: Bybit did not return valid JSON.")
        print("Response received:")
        print(response.text[:1000])
        raise SystemExit(1)

except requests.RequestException as e:
    print("ERROR: Could not connect to Bybit.")
    print(e)
    raise SystemExit(1)


if data.get("retCode") != 0:
    print("ERROR: Bybit API returned an error.")
    print(data)
    raise SystemExit(1)


coins = []

for item in data.get("result", {}).get("list", []):

    symbol = item.get("symbol", "")

    # Only USDT perpetual/futures contracts
    if not symbol.endswith("USDT"):
        continue

    try:
        change = float(item.get("price24hPcnt", "0")) * 100
    except (ValueError, TypeError):
        continue

    coins.append({
        "symbol": symbol,
        "change": change
    })


if not coins:
    print("ERROR: No USDT market data was found.")
    raise SystemExit(1)


# Highest gain first
coins.sort(
    key=lambda x: x["change"],
    reverse=True
)


print()
print("=" * 60)
print("TOP 10 GAINERS")
print("=" * 60)

for number, coin in enumerate(coins[:10], start=1):
    print(
        f"{number:2}. "
        f"{coin['symbol']:15} "
        f"{coin['change']:+8.2f}%"
    )


print()
print("=" * 60)
print("TOP 10 LOSERS")
print("=" * 60)

for number, coin in enumerate(coins[-10:][::-1], start=1):
    print(
        f"{number:2}. "
        f"{coin['symbol']:15} "
        f"{coin['change']:+8.2f}%"
    )


print()
print("=" * 60)
print(
    "Collected:",
    datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
)
print("=" * 60)
