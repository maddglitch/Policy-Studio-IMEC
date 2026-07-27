# make_figures.py - regenerates Figures 1-5 of the Medium post
# "The Middle East Built the World's Newest Trade Corridor on Paper. Literally."
# Author: Mohammad Eisa AlDarmaki
#
# HOW TO RERUN:
#   1. Install Python 3.10+ and matplotlib:  pip install matplotlib
#   2. From this folder (the repo root), run:  python make_figures.py
#   3. Figures are written to ./figures/ as PNG (for the post) and SVG
#      (editable vectors - open directly in Figma or Illustrator to restyle)
#
# DESIGN RULES (so every chart stands on its own):
#   1. Every figure gets a HEADLINE that states the story in plain words,
#      and a SUBTITLE that explains what the reader is looking at.
#   2. Each REGION owns one color everywhere it appears:
#      Gulf = red, EU members = navy, Southeast Asia = teal,
#      India = gold, Israel & Jordan = green.
#   3. Things that are NOT regions (the two measure types in Figure 2) use
#      colors no region uses: purple and orange. Neutral greys/slates are
#      reserved for context.
#   4. Every figure carries its data source and author credit at the bottom.
#
# Inputs (all in this repository):
#   data/raw/untfs_corridor_raw.csv      (UN survey, waves 2015-2025)
#   data/raw/oecd_tfi_corridor.csv       (OECD indicators, pulled 1 Jul 2026)
#   data/raw/lpi_corridor_raw.csv        (World Bank LPI, API pull)
#   output/readiness_scorecard.csv       (built by readiness_index.R)
#   output/savings_results_by_step.csv   (built by savings_model.R)

import csv
import os
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---- the palette (see design rules above) ----
GULF = "#B23A48"; GULF_DARK = "#7A1E2B"   # Gulf family (UAE = darker Gulf red)
EUN  = "#1F3864"                           # EU members
TEAL = "#1F7A74"                           # Southeast Asia
GOLD = "#C88719"                           # India
GREEN = "#5B8C5A"                          # Israel & Jordan
PURPLE = "#6B4FA1"; ORANGE = "#E07B39"     # measure types (Fig 2) - not regions
SLATE = "#5E718D"; SLATE_DARK = "#2F3E53"  # neutral bars (Fig 4) - not regions
TITLE = "#1A2B45"                          # titles/annotations only
os.makedirs("figures", exist_ok=True)

ASEAN = {"IDN", "MYS", "PHL", "SGP", "THA", "VNM"}
GULF6 = {"ARE", "BHR", "KWT", "OMN", "QAT", "SAU"}
EU6 = {"DEU", "ESP", "FRA", "GRC", "ITA", "NLD"}

def headline(fig, title, subtitle, top=0.97):
    """Story-first header: bold claim on top, plain explanation under it."""
    fig.text(0.01, top, title, fontsize=15, fontweight="bold", color=TITLE, ha="left", va="top")
    fig.text(0.01, top - 0.065, subtitle, fontsize=10.3, color="#484848", ha="left", va="top")

def source_note(fig, text):
    """Credit line at the bottom of every chart (visuals best practice)."""
    fig.text(0.01, -0.02, text + "  ·  Chart: Mohammad AlDarmaki (Python/matplotlib); code in repo",
             fontsize=8, color="#888888", ha="left")

def save(name):
    plt.savefig(f"figures/{name}.png", bbox_inches="tight")
    plt.savefig(f"figures/{name}.svg", bbox_inches="tight")
    plt.close()

# ---------------------------------------------------------------- shared data
def load_lpi_customs_norm():
    """Latest World Bank LPI customs score per economy, rescaled 1-5 -> 0-100."""
    lpi = {}
    for r in csv.DictReader(open("data/raw/lpi_corridor_raw.csv")):
        if r["indicator_code"] == "LP.LPI.CUST.XQ":
            y, v = int(r["year"]), float(r["value"])
            if r["iso"] not in lpi or y > lpi[r["iso"]][0]:
                lpi[r["iso"]] = (y, v)
    return {k: (v[1] - 1) / 4 * 100 for k, v in lpi.items()}

def load_tfi(code):
    """OECD indicator values (0-2) for one dimension code (g = automation at
    home, j = cooperation with other countries' border agencies)."""
    out = {}
    for r in csv.DictReader(open("data/raw/oecd_tfi_corridor.csv")):
        if r["dimension_code"] == code:
            out[r["iso"]] = float(r["tfi_index_0_2"])
    return out

scorecard = list(csv.DictReader(open("output/readiness_scorecard.csv")))

# ------------------------------------------------- Figure 1: UN survey trend
def fig_untfs_trend():
    waves = [2015, 2017, 2019, 2021, 2023, 2025]
    series = defaultdict(dict)
    for r in csv.DictReader(open("data/raw/untfs_corridor_raw.csv")):
        if r["paperless"]:
            series[r["iso"]][int(r["year"])] = float(r["paperless"])
    def group_mean(isos, w):
        vals = []
        for iso in isos:
            yrs = [y for y in series.get(iso, {}) if y <= w]
            if yrs:
                vals.append(series[iso][max(yrs)])  # carry latest report forward
        return sum(vals) / len(vals) if vals else None
    fig, ax = plt.subplots(figsize=(9.6, 5.2), dpi=200)
    for lab, isos, c, ls in [("Southeast Asia average", ASEAN, TEAL, "--"),
                             ("Gulf average", GULF6, GULF, "-"),
                             ("EU members average", EU6, EUN, "-"),
                             ("India", {"IND"}, GOLD, "-"),
                             ("UAE", {"ARE"}, GULF_DARK, ":"),
                             ("Jordan", {"JOR"}, GREEN, "-")]:
        ax.plot(waves, [group_mean(isos, w) for w in waves], color=c, ls=ls,
                lw=2.6 if "Southeast" not in lab else 2.2, marker="o", ms=5, label=lab)
    ax.set_ylim(30, 105); ax.set_xticks(waves)
    ax.set_ylabel("Digital paperwork score (out of 100)", fontsize=10)
    ax.legend(loc="lower right", frameon=False, fontsize=9.5, ncol=2)
    for s in ["top", "right"]: ax.spines[s].set_visible(False)
    ax.grid(color="#F0F0F0", lw=0.7)
    headline(fig,
        "On paper, India, Gulf and EU governments report trade digitization on par with Southeast Asia's",
        "Every two years the UN asks governments how much of their trade paperwork has gone digital. By 2025, the Middle East\n"
        "corridor's scores match or beat Southeast Asia's — the region that already runs a shared customs system.")
    plt.tight_layout(rect=[0, 0, 1, 0.85])
    source_note(fig, "Data: UN Global Survey on Digital and Sustainable Trade Facilitation, 2015–2025 (untfsurvey.org). UAE line carries its last report (2017) forward.")
    save("chartB_untfs_trend")

# --------------------------------------- Figure 2: home systems vs connections
def fig_tfi_gap():
    g, j = load_tfi("g"), load_tfi("j")
    def mean(isos, d): return sum(d[i] for i in isos) / len(isos)
    rows = [("EU members", mean(EU6, g), mean(EU6, j), "−0.01", False),
            ("Southeast Asia\n(runs a shared system)", mean(ASEAN, g), mean(ASEAN, j), "+0.13", False),
            ("Israel & Jordan", mean({"ISR", "JOR"}, g), mean({"ISR", "JOR"}, j), "+0.33", False),
            ("India", g["IND"], j["IND"], "+0.51", False),
            ("Gulf states", mean(GULF6, g), mean(GULF6, j), "+0.58", False),
            ("UAE", g["ARE"], j["ARE"], "+0.95", True)]
    fig, ax = plt.subplots(figsize=(9.6, 5.4), dpi=200)
    for i, (lab, gv, jv, gap, hl) in enumerate(rows):
        ax.plot([jv, gv], [i, i], color="#D9D9D9", lw=7 if hl else 5,
                solid_capstyle="round", zorder=1)
        ax.scatter([gv], [i], s=160 if hl else 110, color=PURPLE, zorder=3)
        ax.scatter([jv], [i], s=160 if hl else 110, color=ORANGE, zorder=3)
        ax.text(max(gv, jv) + 0.05, i, "gap " + gap, va="center", fontsize=11.5,
                fontweight="bold" if hl else "normal", color=TITLE if hl else "#444444")
    ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows], fontsize=11.5)
    for tick, r in zip(ax.get_yticklabels(), rows):
        if r[4]: tick.set_fontweight("bold")
    ax.set_xlim(0.35, 2.35); ax.set_ylim(-0.6, len(rows) - 0.1)
    ax.scatter([], [], s=110, color=PURPLE, label="Digital customs systems at home")
    ax.scatter([], [], s=110, color=ORANGE, label="Cooperation with other countries' border agencies")
    ax.legend(loc="lower left", frameon=False, fontsize=10.5)
    ax.set_xlabel("OECD trade facilitation score (0 = weakest, 2 = best), 2025", fontsize=11, color="#333333")
    for s in ["top", "right", "left"]: ax.spines[s].set_visible(False)
    ax.grid(axis="x", color="#EEEEEE", lw=0.8, zorder=0)
    headline(fig,
        "The Gulf and the UAE show the biggest gaps between automation at home and cross-border co-operation",
        "Independent OECD assessments of each place, on two questions: how digital its customs systems are at home (purple), and\n"
        "how well its border agencies work with other countries' (orange). The wider the gap, the more it has built but not connected.")
    plt.tight_layout(rect=[0, 0, 1, 0.86])
    source_note(fig, "Data: OECD Trade Facilitation Indicators, 2025 edition (oecd.org)")
    save("chart_tfi_gap")

# ------------------------------- Figure 3: self-reports vs assessed, two-panel
def fig_contrast_scatter():
    disp = {"ARE": "UAE", "SAU": "KSA", "DEU": "GER", "NLD": "NED", "KWT": "KUW",
            "QAT": "QAT", "JOR": "JOR", "IND": "IND", "SGP": "SGP", "FRA": "FRA"}
    lpin = load_lpi_customs_norm()
    tfi_j = load_tfi("j")
    ready = {r["iso"]: (float(r["sw_readiness"]),
                        float(r["lpi_cust_norm"]) if r["lpi_cust_norm"] else None,
                        r["region"]) for r in scorecard}
    region = {r["iso"]: r["region"] for r in scorecard}; region.setdefault("ISR", "Levant")
    regcol = {"Gulf": GULF, "Europe": EUN, "ASEAN": TEAL, "India": GOLD, "Levant": GREEN}
    leglab = {"Gulf": "Gulf", "Europe": "EU members", "ASEAN": "Southeast Asia", "India": "India", "Levant": "Israel & Jordan"}
    fig, axes = plt.subplots(1, 2, figsize=(11.4, 5.6), dpi=200)
    ax = axes[0]
    for iso, (x, y, reg) in ready.items():
        if y is None: continue
        ax.scatter(x, y, s=70, color=regcol.get(reg, "#999999"), zorder=3, alpha=0.9)
        if iso in {"QAT", "SAU", "JOR", "IND", "ARE", "DEU", "FRA", "SGP"}:
            ax.annotate(disp.get(iso, iso), (x, y), textcoords="offset points", xytext=(5, 4), fontsize=9, color="#333333")
    ax.plot([30, 105], [30, 105], ls="--", lw=1, color="#CCCCCC", zorder=1)
    ax.text(97, 91, "scores match ratings", fontsize=8.5, color="#999999", rotation=38, ha="right")
    import numpy as _np
    _xs = [x for iso, (x, y, reg) in ready.items() if y is not None]
    _ys = [y for iso, (x, y, reg) in ready.items() if y is not None]
    _m, _b = _np.polyfit(_xs, _ys, 1)
    _xr = _np.array([min(_xs) - 2, max(_xs) + 2])
    ax.plot(_xr, _m * _xr + _b, lw=2.2, color="#444444", zorder=2)
    ax.text(0.03, 0.05, "average relationship: flat\nrank correlation \u2248 0.00", transform=ax.transAxes,
            fontsize=10, color="#444444", fontweight="bold")
    ax.set_xlabel("UN survey single-window implementation score (out of 100)", fontsize=10.5)
    ax.set_ylabel("Customs efficiency, as rated by freight\nprofessionals (World Bank LPI, 0-100)", fontsize=10.5)
    ax.set_title("UN survey implementation score:\nno relationship with rated efficiency", fontsize=11, color=TITLE, loc="left")
    ax.set_xlim(58, 106); ax.set_ylim(25, 95)
    ax = axes[1]
    for iso, jv in tfi_j.items():
        if iso not in lpin: continue
        ax.scatter(jv, lpin[iso], s=70, color=regcol.get(region.get(iso, "?"), "#999999"), zorder=3, alpha=0.9)
        if iso in {"QAT", "SAU", "KWT", "IND", "ARE", "DEU", "FRA", "NLD", "SGP"}:
            ax.annotate(disp.get(iso, iso), (jv, lpin[iso]), textcoords="offset points", xytext=(5, 4), fontsize=9, color="#333333")
    _xs2 = [jv for iso, jv in tfi_j.items() if iso in lpin]
    _ys2 = [lpin[iso] for iso, jv in tfi_j.items() if iso in lpin]
    _m2, _b2 = _np.polyfit(_xs2, _ys2, 1)
    _xr2 = _np.array([min(_xs2) - 0.05, max(_xs2) + 0.05])
    ax.plot(_xr2, _m2 * _xr2 + _b2, lw=2.2, color="#444444", zorder=2)
    ax.text(0.03, 0.9, "average relationship: rising\nrank correlation \u2248 0.62", transform=ax.transAxes,
            fontsize=10, color="#444444", fontweight="bold")
    ax.set_xlabel("Cooperation with other countries' border agencies,\nscored by OECD assessors (0–2)", fontsize=10.5)
    ax.set_ylabel("Customs efficiency, as rated by freight\nprofessionals (World Bank LPI, 0-100)", fontsize=10.5)
    ax.set_title("OECD external co-operation score:\ntracks rated efficiency closely", fontsize=11, color=TITLE, loc="left")
    ax.set_xlim(0.3, 2.05); ax.set_ylim(25, 95)
    handles = [plt.Line2D([], [], marker="o", ls="", color=c, label=leglab[r]) for r, c in regcol.items()]
    fig.legend(handles=handles, loc="lower center", ncol=5, frameon=False, fontsize=9.5, bbox_to_anchor=(0.5, -0.02))
    for ax in axes:
        for s in ["top", "right"]: ax.spines[s].set_visible(False)
        ax.grid(color="#F0F0F0", lw=0.7, zorder=0)
    headline(fig,
        "What governments report implementing doesn't predict their customs efficiency; their cross-border co-operation does",
        "Each dot is a country, colored by region; the dark line is the average relationship. Left: the UN survey's implementation score shows no\n"
        "relationship with customs efficiency as rated by the freight professionals who use it. Right: the OECD's co-operation score tracks it closely.",
        top=0.99)
    plt.tight_layout(rect=[0, 0.05, 1, 0.86])
    source_note(fig, "Data: UN Global Survey (2025); OECD Trade Facilitation Indicators (2025); World Bank Logistics Performance Index 2023 (survey fielded 2022)")
    save("chart_contrast_scatter")

# --------------------------------------------- Figure 4: savings by step
def fig_savings_steps():
    rows = list(csv.DictReader(open("output/savings_results_by_step.csv")))
    labels = {"Step 1 (anchor link: UAE-India)": "Step 1\nUAE–India link",
              "Step 2 (Gulf integration: intra-Gulf)": "Step 2\nGulf integration",
              "Step 3 (connect EU: Gulf-EU + India-EU)": "Step 3\nEU connection",
              "Total corridor": "Whole corridor"}
    steps = [(labels[r["corridor_step"]], float(r["median_usd_bn"]),
              float(r["p10_usd_bn"]), float(r["p90_usd_bn"]))
             for r in rows if r["corridor_step"] in labels]
    fig, ax = plt.subplots(figsize=(9.6, 5.2), dpi=200)
    cols = [SLATE, SLATE, SLATE, SLATE_DARK]
    for i, (lab, med, p10, p90) in enumerate(steps):
        ax.bar(i, med, width=0.56, color=cols[i], zorder=2)
        ax.errorbar(i, med, yerr=[[med - p10], [p90 - med]], fmt="none", ecolor="#666666",
                    elinewidth=1.6, capsize=6, capthick=1.6, zorder=3)
        ax.text(i, p90 + 0.08, f"${med:.2f}bn", ha="center", fontsize=12.5, fontweight="bold", color=TITLE)
    ax.axhline(0.64, color="#555555", lw=1.4, ls="--", zorder=1)  # most conservative estimate
    ax.text(-0.45, 2.30, "dashed line: higher benchmark at current ASEAN scope (~$0.6bn/yr)\nmost conservative benchmark: ~$0.2-0.3bn/yr", fontsize=9.5, color="#555555", va="top")
    ax.set_xticks(range(len(steps))); ax.set_xticklabels([s[0] for s in steps], fontsize=11.5)
    ax.set_ylabel("Estimated savings, $ billions per year", fontsize=11, color="#333333")
    ax.set_ylim(0, 2.75); ax.set_xlim(-0.55, 3.55)
    for s in ["top", "right"]: ax.spines[s].set_visible(False)
    ax.grid(axis="y", color="#EEEEEE", lw=0.8, zorder=0)
    headline(fig,
        "Connecting the corridor's paperwork could save \\$0.2bn to \\$1.4bn a year, most of it on the EU leg",
        "A scenario estimate, not a forecast: yearly savings if the corridor's customs systems talked to each other, anchored to reported\n"
        "savings from Southeast Asia's shared system. Bars show the central scenario; thin lines the range across thousands of runs.")
    plt.tight_layout(rect=[0, 0, 1, 0.86])
    source_note(fig, "Data: UN Comtrade & GCC-Stat trade values (2019–2023); savings rate anchored to reported ASEAN Single Window savings figures (see End Notes)")
    save("chart_savings_steps")

# --------------------------------------------- Figure 5: three-step diagram
# Step boxes use the region colors of the economies each step connects:
# Step 1 = India gold (the UAE-India link), Step 2 = Gulf red, Step 3 = EU navy.
def fig_threestep():
    fig, ax = plt.subplots(figsize=(9.6, 4.0), dpi=200)
    ax.axis("off")
    boxes = [(0.02, "STEP 1 - now", "UAE-India link",
              "Digital channel already running\n(since May 2026)\nExpand it to full document exchange", "$0.23bn/yr", GOLD),
             (0.36, "STEP 2 - 2026-28", "Gulf integration",
              "Turn the Gulf leaders' December 2025\ncustoms-platform decision\ninto a working system", "$0.45bn/yr", GULF),
             (0.70, "STEP 3 - to ~2031", "EU connection",
              "Connect to the EU's own customs\nsingle window, through the\nUAE-EU trade deal being negotiated", "$0.92bn/yr", EUN)]
    for x, step, title, body, val, c in boxes:
        ax.add_patch(plt.Rectangle((x, 0.06), 0.28, 0.76, facecolor="#F6F5F2", edgecolor=c, lw=2))
        ax.text(x + 0.14, 0.76, step, ha="center", fontsize=10.5, fontweight="bold", color=c)
        ax.text(x + 0.14, 0.63, title, ha="center", fontsize=12, fontweight="bold", color="#222222")
        ax.text(x + 0.14, 0.38, body, ha="center", fontsize=9, color="#444444")
        ax.text(x + 0.14, 0.12, val, ha="center", fontsize=11.5, fontweight="bold", color=c)
    for x in (0.315, 0.655):
        ax.annotate("", xy=(x + 0.04, 0.44), xytext=(x, 0.44),
                    arrowprops=dict(arrowstyle="-|>", color="#888888", lw=2))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    headline(fig,
        "The three-step path to a connected corridor",
        "")
    plt.tight_layout(rect=[0, 0, 1, 0.90])
    source_note(fig, "Illustrative savings scenarios from this analysis; step anchors are existing commitments or legal processes (see post)")
    save("chartB_threestep")

if __name__ == "__main__":
    fig_untfs_trend()
    fig_tfi_gap()
    fig_contrast_scatter()
    fig_savings_steps()
    fig_threestep()
    print("All figures written to ./figures/")
