# pull_worldbank_exports.py — reproducible data pull for the Figure 6 map.
#
# Downloads merchandise exports (current US$), World Bank indicator
# TX.VAL.MRCH.CD.WT, for the ten ASEAN members and five neighboring
# economies, 2013-2023, and writes data/raw/merch_exports_asw_window.csv.
#
# HOW TO RERUN:
#   pip install requests
#   python pull_worldbank_exports.py     (from the repo root)
#
# The checked-in CSV was produced by this pull in July 2026; rerunning may
# differ slightly if the World Bank revises historical series.
# API docs: https://datahelpdesk.worldbank.org/knowledgebase/topics/125589

import csv
import requests

ASEAN = ["BRN", "KHM", "IDN", "LAO", "MMR", "MYS", "PHL", "SGP", "THA", "VNM"]
NEIGHBORS = ["CHN", "IND", "BGD", "AUS", "LKA"]
INDICATOR = "TX.VAL.MRCH.CD.WT"
YEARS = "2013:2023"

rows = []
for iso in ASEAN + NEIGHBORS:
    url = (f"https://api.worldbank.org/v2/country/{iso}/indicator/{INDICATOR}"
           f"?format=json&date={YEARS}&per_page=100")
    data = requests.get(url, timeout=60).json()
    for obs in data[1]:
        if obs["value"] is not None:
            rows.append({
                "iso": iso,
                "year": int(obs["date"]),
                "merch_exports_usd_mn": round(obs["value"] / 1e6),
                "group": "ASEAN" if iso in ASEAN else "neighbor",
            })

rows.sort(key=lambda r: (r["iso"], r["year"]))
with open("data/raw/merch_exports_asw_window.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["iso", "year", "merch_exports_usd_mn", "group"])
    w.writeheader()
    w.writerows(rows)
print(f"wrote {len(rows)} rows for {len(ASEAN + NEIGHBORS)} economies")
