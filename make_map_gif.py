# make_map_gif.py - Animated version of Figure 6 for platforms without
# iframe embeds (e.g. Substack): one frame per year, cycling automatically.
#
# HOW TO RERUN:
#   pip install matplotlib "geopandas==0.13.2" "fiona==1.9.6" Pillow
#   python make_map_gif.py       (from the repo root)
#   -> writes figures/chartB_asw_map_animated.gif
#
# Same data, palette and fixed color scale as make_map.py. Includes 2020-21
# (flagged as COVID years on the frame) so the animation is continuous.

import csv, io, warnings
from collections import defaultdict
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
from matplotlib.cm import ScalarMappable
warnings.filterwarnings("ignore", category=FutureWarning)
import geopandas as gpd
from PIL import Image

TITLE = "#1A2B45"; TEAL_DARK = "#0E4B47"; BROWN = "#7A4E2D"

d = defaultdict(dict); group = {}
for r in csv.DictReader(open("data/raw/merch_exports_asw_window.csv")):
    d[r["iso"]][int(r["year"])] = float(r["merch_exports_usd_mn"])
    group[r["iso"]] = r["group"]

years = list(range(2014, 2024))
yoy = {yr: {iso: 100 * (d[iso][yr] / d[iso][yr - 1] - 1)
            for iso in d if yr in d[iso] and (yr - 1) in d[iso]} for yr in years}

try:
    world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
except AttributeError:
    raise SystemExit("geopandas >= 1.0 removed the bundled Natural Earth dataset. "
                     "Install the pinned versions from the README: "
                     "pip install 'geopandas==0.13.2' 'fiona==1.9.6'")
world["iso"] = world["iso_a3"]

centroid = {"BRN": (4.9, 114.7), "KHM": (12.0, 105.0), "IDN": (-2.2, 113.0),
            "LAO": (19.9, 102.5), "MMR": (21.0, 96.0), "MYS": (3.8, 102.0),
            "PHL": (12.9, 122.5), "SGP": (1.35, 103.8), "THA": (15.8, 101.0),
            "VNM": (16.4, 106.6)}

cmap = LinearSegmentedColormap.from_list("brownteal", [BROWN, "#F3EFE8", "#5FA8A2", TEAL_DARK])
norm = TwoSlopeNorm(vmin=-20, vcenter=0, vmax=30)

frames = []
for yr in years:
    fig, ax = plt.subplots(figsize=(8.6, 6.4), dpi=110)
    fig.subplots_adjust(left=0.01, right=0.86, top=0.76, bottom=0.10)
    world.plot(ax=ax, color="#F4F3F0", edgecolor="#E2E2E2", linewidth=0.4)
    w = world.copy()
    w["v"] = w["iso"].map(lambda i: yoy[yr].get(i))
    w[w["v"].notna()].plot(ax=ax, column="v", cmap=cmap, norm=norm,
                           edgecolor="#FFFFFF", linewidth=0.6)
    for iso, (lat, lon) in centroid.items():
        ax.scatter([lon], [lat], s=16, color="#1A1A1A", zorder=5)
    ax.set_xlim(62, 155); ax.set_ylim(-13, 36); ax.axis("off")

    label = str(yr)
    note = ""
    if yr == 2018: note = "shared window goes live"
    if yr in (2020, 2021): note = "COVID crash and rebound"
    ax.text(0.02, 0.97, label, transform=ax.transAxes, fontsize=30,
            fontweight="bold", color=TITLE, va="top")
    if note:
        ax.text(0.02, 0.86, note, transform=ax.transAxes, fontsize=13,
                color="#B23A48" if yr in (2020, 2021) else TEAL_DARK,
                fontweight="bold", va="top")

    fig.suptitle("Export growth around the ASEAN Single Window's 2018 go-live\n"
                 "Color: goods export growth vs the year before.\n"
                 "\u25cf = member of the shared system. Exploratory, not causal.",
                 fontsize=11.5, fontweight="bold", color=TITLE, x=0.02, ha="left", y=0.99)
    cax = fig.add_axes([0.88, 0.15, 0.02, 0.6])
    cbar = fig.colorbar(ScalarMappable(norm=norm, cmap=cmap), cax=cax, extend="both")
    cbar.set_label("Growth vs. year before (%)", fontsize=9.5)
    fig.text(0.02, 0.02, "Data: World Bank goods exports (2013-2023)  ·  Map: Mohammad AlDarmaki; code in repo",
             fontsize=8.5, color="#888888")

    buf = io.BytesIO()
    fig.savefig(buf, format="png", facecolor="white")
    plt.close(fig)
    buf.seek(0)
    frames.append(Image.open(buf).convert("P", palette=Image.ADAPTIVE))

durations = []
for yr in years:
    durations.append(2600 if yr in (2018,) else 1500)
frames[0].save("figures/chartB_asw_map_animated.gif", save_all=True,
               append_images=frames[1:], duration=durations, loop=0, optimize=False)
print("gif written:", len(frames), "frames")
