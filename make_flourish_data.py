# make_flourish_data.py - Builds the CSV behind the post's interactive map
# (Flourish projection map: https://public.flourish.studio/visualisation/29808313/).
#
# HOW TO RERUN:  python make_flourish_data.py   (from the repo root)
#   -> writes data/processed/flourish_map_data.csv
#
# One row per country; one column per year of goods-export growth (% vs the
# year before), computed from the same World Bank dataset as Figure 6
# (data/raw/merch_exports_asw_window.csv). All years 2014-2023 are included;
# the interactive flags 2020-21 as the COVID crash and rebound.
# In Flourish: bind ISO3 to region IDs, the year columns to "Color by"
# (which creates the year slider), and Status to the popup metadata.

import csv, os
from collections import defaultdict

NAMES = {"IDN":"Indonesia","IND":"India","KHM":"Cambodia","LAO":"Laos","LKA":"Sri Lanka",
         "MMR":"Myanmar","MYS":"Malaysia","PHL":"Philippines","SGP":"Singapore",
         "THA":"Thailand","VNM":"Vietnam","CHN":"China","AUS":"Australia",
         "BGD":"Bangladesh","BRN":"Brunei"}

d = defaultdict(dict); grp = {}
for r in csv.DictReader(open("data/raw/merch_exports_asw_window.csv")):
    d[r["iso"]][int(r["year"])] = float(r["merch_exports_usd_mn"])
    grp[r["iso"]] = r["group"]

years = list(range(2014, 2024))
os.makedirs("data/processed", exist_ok=True)
with open("data/processed/flourish_map_data.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Name", "ISO3", "Status"] + [str(y) for y in years])
    for iso in sorted(d):
        row = [NAMES.get(iso, iso), iso,
               "ASEAN Single Window member" if grp[iso] == "ASEAN" else "Neighbor (non-member)"]
        for y in years:
            ok = y in d[iso] and (y - 1) in d[iso] and d[iso][y - 1] > 0
            row.append(round((d[iso][y] / d[iso][y - 1] - 1) * 100, 1) if ok else "")
        w.writerow(row)
print("written data/processed/flourish_map_data.csv")
