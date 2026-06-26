#!/usr/bin/env python3
"""Fetch the latest value of each FRED series we need and write fred_latest.json.

Runs in GitHub Actions (a normal egress FRED does not block). The FRED API key is
read from the FRED_API_KEY env var (an encrypted Actions secret) — never committed.
"""
import json
import os
import datetime
import urllib.request

KEY = os.environ["FRED_API_KEY"]

# daily series, raw level (OAS values are in %, x100 for bps; 5y5y is a rate in %)
RAW = ["BAMLH0A0HYM2", "BAMLC0A0CM", "T5YIFR"]
# monthly series, returned as year-over-year % via FRED units=pc1
YOY = ["CPIAUCSL", "CPILFESL", "PCEPI", "PCEPILFE", "PPIFIS"]


def fetch(series_id, pc1=False):
    url = (
        "https://api.stlouisfed.org/fred/series/observations"
        f"?series_id={series_id}&api_key={KEY}&file_type=json"
        "&sort_order=desc&limit=1" + ("&units=pc1" if pc1 else "")
    )
    with urllib.request.urlopen(url, timeout=30) as r:
        d = json.load(r)
    o = d["observations"][0]
    return {"date": o["date"], "value": o["value"]}


out = {
    "asof_utc": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    "series": {},
}
for s in RAW:
    out["series"][s] = {**fetch(s), "kind": "level"}
for s in YOY:
    out["series"][s] = {**fetch(s, pc1=True), "kind": "yoy_pct"}

with open("fred_latest.json", "w") as f:
    json.dump(out, f, indent=2)
print(json.dumps(out, indent=2))
