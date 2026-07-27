# make_map.py - Figure 6 of the Medium post: year-by-year maps of export
# growth for Southeast Asia's shared-system members and their neighbors.
#
# HOW TO RERUN:
#   pip install matplotlib "geopandas==0.13.2" "fiona==1.9.6"
#   python make_map.py          (from the repo root)
#   -> writes figures/chartB_asw_map.png and .svg
#   (geopandas 0.13.x is pinned because it bundles the country shapes, so
#    the map renders offline with no external downloads.)
#
# WHAT THE MAPS SHOW, IN PLAIN WORDS:
# Six small maps, one per year. In each, a country's color shows how much
# its goods exports grew THAT year compared with the year before - teal for
# growth, brown for decline. The COVID years (2020 and 2021) are left out,
# because the crash and the rebound swamp everything else.
#
# COLOR NOTE: teal is Southeast Asia's color throughout the post; the brown
# used for declines appears in no other figure, so nothing clashes.
#
# HONESTY NOTE (also in the post): exploratory, not causal. Current
# dollars, total (not intra-bloc) exports, and many forces moved these
# numbers - supply-chain relocation out of China above all.
#
# Data: data/raw/merch_exports_asw_window.csv - produced by
# pull_worldbank_exports.py (World Bank, goods exports, current US$).
# Spot-verified against a fresh API pull and the indicator page, July 2026.

import csv
import warnings
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
from matplotlib.cm import ScalarMappable
warnings.filterwarnings("ignore", category=FutureWarning)
import geopandas as gpd

TITLE = "#1A2B45"; TEAL_DARK = "#0E4B47"; BROWN = "#7A4E2D"

# ---- Step 1: read the data and compute each year's growth vs the year before
d = defaultdict(dict); group = {}
for r in csv.DictReader(open("data/raw/merch_exports_asw_window.csv")):
    d[r["iso"]][int(r["year"])] = float(r["merch_exports_usd_mn"])
    group[r["iso"]] = r["group"]

years = [2015, 2017, 2018, 2019, 2022, 2023]   # 2020-21 omitted (COVID crash + rebound)
yoy = {yr: {iso: 100 * (d[iso][yr] / d[iso][yr - 1] - 1) for iso in d} for yr in years}

# ---- Step 2: draw one small map per year -------------------------------------
try:
    world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
except AttributeError:
    raise SystemExit("geopandas >= 1.0 removed the bundled Natural Earth dataset. "
                     "Install the pinned versions from the README: "
                     "pip install 'geopandas==0.13.2' 'fiona==1.9.6'")
world["iso"] = world["iso_a3"]
world.loc[world["name"] == "France", "iso"] = "FRA"

centroid = {"BRN": (4.9, 114.7), "KHM": (12.0, 105.0), "IDN": (-2.2, 113.0),
            "LAO": (19.9, 102.5), "MMR": (21.0, 96.0), "MYS": (3.8, 102.0),
            "PHL": (12.9, 122.5), "SGP": (1.35, 103.8), "THA": (15.8, 101.0),
            "VNM": (16.4, 106.6)}

cmap = LinearSegmentedColormap.from_list("brownteal", [BROWN, "#F3EFE8", "#5FA8A2", TEAL_DARK])
norm = TwoSlopeNorm(vmin=-20, vcenter=0, vmax=30)   # values beyond the ends saturate

fig, axes = plt.subplots(2, 3, figsize=(13.2, 7.0), dpi=200)
fig.subplots_adjust(left=0.01, right=0.90, top=0.80, bottom=0.13, wspace=0.02, hspace=0.18)
for ax, yr in zip(axes.flat, years):
    world.plot(ax=ax, color="#F4F3F0", edgecolor="#E2E2E2", linewidth=0.4)
    w = world.copy()
    w["v"] = w["iso"].map(lambda i: yoy[yr].get(i))
    w[w["v"].notna()].plot(ax=ax, column="v", cmap=cmap, norm=norm,
                           edgecolor="#FFFFFF", linewidth=0.6)
    for iso, (lat, lon) in centroid.items():
        ax.scatter([lon], [lat], s=12, color="#1A1A1A", zorder=5)
    ax.set_xlim(62, 155); ax.set_ylim(-13, 36); ax.axis("off")
    label = f"{yr}"
    if yr == 2018: label = "2018 — shared window goes live"
    ax.set_title(label, fontsize=12.5, color=TITLE,
                 fontweight="bold" if yr == 2018 else "normal", pad=4)

fig.suptitle("After the shared window's 2018 go-live, its smallest members grew exports 10-14% a year, against about 3% for neighbors\n"
             "Each country's color shows how much its goods exports grew that year. ● = member of the shared system. 2020–21 omitted (COVID crash and rebound).",
             fontsize=14.5, fontweight="bold", color=TITLE, x=0.02, ha="left", y=0.97)
cax = fig.add_axes([0.92, 0.15, 0.016, 0.60])
sm = ScalarMappable(norm=norm, cmap=cmap)
cbar = fig.colorbar(sm, cax=cax, extend="both")
cbar.set_label("Export growth vs. the year before (%)", fontsize=10.5)
fig.text(0.02, 0.045, "After the window opens, the deepest teal sits over the system's smallest members — Cambodia, Laos, Vietnam grew fastest\n"
                      "(averaging 10–14% a year across 2013–2023, COVID excluded) while neighbors like India and China averaged about 3%.",
         fontsize=10.5, color="#333333", ha="left")
fig.text(0.02, 0.005, "Data: World Bank, goods exports (current US$), 2013–2023, pulled via pull_worldbank_exports.py and spot-verified against the World Bank site  ·  "
                      "Exploratory, not causal — see post End Notes  ·  Map: Mohammad AlDarmaki (Python/geopandas); code in repo",
         fontsize=8, color="#888888", ha="left")
plt.savefig("figures/chartB_asw_map.png", bbox_inches="tight")
plt.savefig("figures/chartB_asw_map.svg", bbox_inches="tight")
print("map written")
