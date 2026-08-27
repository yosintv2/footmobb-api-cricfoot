import requests
from datetime import datetime, timezone

URL = "https://www.football.com/api/ng/factsCenter/event/firstSearch"
PARAMS = {"keyword": "BestOdds", "offset": 0, "pageSize": 20}
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.football.com/",
    "Origin": "https://www.football.com",
}

resp = requests.get(URL, params=PARAMS, headers=HEADERS)
resp.raise_for_status()
body = resp.json()

if body.get("bizCode") != 10000:
    raise RuntimeError(f"API error: {body.get('message')}")

matches = []
for m in body["data"].get("live", []) + body["data"].get("pre", []):
    ts = m.get("estimateStartTime", 0) / 1000
    matches.append({
        "eventId": m.get("eventId"),
        "estimateStartTime": m.get("estimateStartTime"),
        "time": datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "homeTeamName": m.get("homeTeamName"),
        "awayTeamName": m.get("awayTeamName"),
    })

import json
with open("today.json", "w", encoding="utf-8") as f:
    json.dump(matches, f, indent=2, ensure_ascii=False)

print(f"Saved {len(matches)} matches to today.json")
