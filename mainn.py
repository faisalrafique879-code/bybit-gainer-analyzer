import requests
from datetime import datetime, timezone

URL = "https://api.bybit.com/v5/market/tickers"

params = {
    "category": "linear"
}

response = requests.get(URL, params=params, timeout=20)
data = response.json()

if data["retCode"] != 0:
    print("Error getting Bybit data")
    print(data)
    exit()

coins = []

for item in data["result"]["list"]:
    symbol = item["symbol"]

    if not symbol.endswith("USDT"):
        continue

    try:
        change = float(item["price24hPcnt"]) * 100
    except:
        continue

    coins.append({
        "symbol": symbol,
        "change": change
    })

coins.sort(key=lambda x: x["change"], reverse=True)

print("=" * 50)
print("BYBIT TOP GAINERS")
print("=" * 50)

for coin in coins[:10]:
    print(f'{coin["symbol"]:15} {coin["change"]:>8.2f}%')

print()
print("=" * 50)
print("BYBIT TOP LOSERS")
print("=" * 50)

for coin in coins[-10:]:
    print(f'{coin["symbol"]:15} {coin["change"]:>8.2f}%')

print()
print("Collected:", datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"))
