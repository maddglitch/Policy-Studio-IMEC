# make_figures.py — regenerates every figure in the Medium post
# "The Middle East Built the World's Newest Trade Corridor on Paper. Literally."
# Author: Mohammad Eisa AlDarmaki
#
# HOW TO RERUN:
#   1. Install Python 3.10+ and matplotlib:  pip install matplotlib
#   2. From this folder (the repo root), run:  python make_figures.py
#   3. Figures are written to ./figures/ as PNG (for the post) and SVG
#      (editable vectors — open directly in Figma or Illustrator to restyle)
#
# These are the PLAIN-LANGUAGE versions used in the published post (labels
# written for a general audience, data source credited on each chart).
# The technical companion paper (Stream A) uses versions of the same charts
# with statistical labels; both derive from the same repository files:
#   data/raw/untfs_corridor_raw.csv      (UN survey, waves 2015-2025)
#   data/raw/oecd_tfi_corridor.csv       (OECD TFI, pulled 1 Jul 2026)
#   data/raw/lpi_corridor_raw.csv        (World Bank LPI, API pull)
#   output/readiness_scorecard.csv       (built by readiness_index.R)
#   output/savings_results_by_step.csv   (built by savings_model.R)
# See METHODS_AND_AUDIT.md for provenance and SOURCES.md for citations.

import csv
import os
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

NAVY = "#1F3864"; BLUE = "#2E5395"; RED = "#B23A48"
GREY = "#9A9A9A"; GOLD = "#C88719"; GREEN = "#5B8C5A"; LIGHT = "#D5DEEE"
os.makedirs("figures", exist_ok=True)

ASEAN = {"IDN", "MYS", "PHL", "SGP", "THA", "VNM"}
GULF = {"ARE", "BHR", "KWT", "OMN", "QAT", "SAU"}
EU = {"DEU", "ESP", "FRA", "GRC", "ITA", "NLD"}

def source_note(fig, text):
    """Credit line at the bottom of every chart (visuals best practice)."""
    fig.text(0.01, -0.02, text + "  ·  Chart: Mohammad AlDarmaki (Python/matplotlib); code in repo",
             fontsize=8, color="#888888", ha="left")

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
    """OECD Trade Facilitation Indicator values (0-2) for one dimension code."""
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
    fig, ax = plt.subplots(figsize=(9.6, 4.4), dpi=200)
    for lab, isos, c, ls in [("Southeast Asia average", ASEAN, GREY, "--"),
                             ("Gulf average", GULF, RED, "-"),
                             ("EU members average", EU, NAVY, "-"),
                             ("India", {"IND"}, GOLD, "-"),
                             ("UAE", {"ARE"}, BLUE, "-"),
                             ("Jordan", {"JOR"}, GREEN, ":")]:
        ax.plot(waves, [group_mean(isos, w) for w in waves], color=c, ls=ls,
                lw=2.6 if "Southeast" not in lab else 2.2, marker="o", ms=5, label=lab)
    ax.set_ylim(30, 105); ax.set_xticks(waves)
    ax.set_ylabel("How much trade paperwork has gone digital\n(governments' reports to the UN, score out of 100)", fontsize=10)
    ax.set_title("On paper, the corridor caught up to Southeast Asia — 2015–2025",
                 fontsize=13.5, fontweight="bold", color=NAVY, loc="left", pad=10)
    ax.legend(loc="lower right", frameon=False, fontsize=9.5, ncol=2)
    for s in ["top", "right"]: ax.spines[s].set_visible(False)
    ax.grid(color="#F0F0F0", lw=0.7)
    source_note(fig, "Data: UN Global Survey on Digital and Sustainable Trade Facilitation, 2015–2025 (untfsurvey.org)")
    plt.tight_layout(); plt.savefig("figures/chartB_untfs_trend.png", bbox_inches="tight")
    plt.savefig("figures/chartB_untfs_trend.svg", bbox_inches="tight")  # editable vector for Figma/Illustrator
    plt.close()

# --------------------------------------- Figure 2: home systems vs connections
def fig_tfi_gap():
    g, j = load_tfi("g"), load_tfi("j")
    def mean(isos, d): return sum(d[i] for i in isos) / len(isos)
    rows = [("EU members", mean(EU, g), mean(EU, j), "−0.01", False),
            ("Southeast Asia\n(runs a shared system)", mean(ASEAN, g), mean(ASEAN, j), "+0.13", False),
            ("Israel & Jordan", mean({"ISR", "JOR"}, g), mean({"ISR", "JOR"}, j), "+0.33", False),
            ("India", g["IND"], j["IND"], "+0.51", False),
            ("Gulf states", mean(GULF, g), mean(GULF, j), "+0.58", False),
            ("UAE", g["ARE"], j["ARE"], "+0.95", True)]
    fig, ax = plt.subplots(figsize=(9.6, 4.6), dpi=200)
    for i, (lab, gv, jv, gap, hl) in enumerate(rows):
        ax.plot([jv, gv], [i, i], color=RED if hl else LIGHT, lw=7 if hl else 5,
                solid_capstyle="round", zorder=1)
        ax.scatter([gv], [i], s=150 if hl else 110, color=NAVY, zorder=3)
        ax.scatter([jv], [i], s=150 if hl else 110, color=RED if hl else GREY, zorder=3)
        ax.text(max(gv, jv) + 0.05, i, gap, va="center", fontsize=12,
                fontweight="bold" if hl else "normal", color=RED if hl else "#444444")
    ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows], fontsize=11.5)
    for tick, r in zip(ax.get_yticklabels(), rows):
        if r[4]: tick.set_fontweight("bold"); tick.set_color(RED)
    ax.set_xlim(0.35, 2.3); ax.set_ylim(-0.6, len(rows) - 0.1)
    ax.scatter([], [], s=110, color=NAVY, label="Digital customs systems at home")
    ax.scatter([], [], s=110, color=GREY, label="Cooperation with other countries' border agencies")
    ax.legend(loc="lower left", frameon=False, fontsize=10.5)
    ax.set_xlabel("OECD trade facilitation score (0 = weakest, 2 = best), 2025", fontsize=11, color="#333333")
    ax.set_title("Built at home, unconnected abroad: the gap behind the corridor's delays",
                 fontsize=14, fontweight="bold", color=NAVY, loc="left", pad=12)
    for s in ["top", "right", "left"]: ax.spines[s].set_visible(False)
    ax.grid(axis="x", color="#EEEEEE", lw=0.8, zorder=0)
    source_note(fig, "Data: OECD Trade Facilitation Indicators, 2025 edition (oecd.org)")
    plt.tight_layout(); plt.savefig("figures/chart_tfi_gap.png", bbox_inches="tight")
    plt.savefig("figures/chart_tfi_gap.svg", bbox_inches="tight")  # editable vector for Figma/Illustrator
    plt.close()

# ------------------------------- Figure 3: self-reports vs assessed, two-panel
def fig_contrast_scatter():
    lpin = load_lpi_customs_norm()
    tfi_j = load_tfi("j")
    ready = {r["iso"]: (float(r["sw_readiness"]),
                        float(r["lpi_cust_norm"]) if r["lpi_cust_norm"] else None,
                        r["region"]) for r in scorecard}
    region = {r["iso"]: r["region"] for r in scorecard}; region.setdefault("ISR", "Levant")
    regcol = {"Gulf": RED, "Europe": NAVY, "ASEAN": GREY, "India": GOLD, "Levant": GREEN}
    leglab = {"Gulf": "Gulf", "Europe": "EU members", "ASEAN": "Southeast Asia", "India": "India", "Levant": "Israel & Jordan"}
    fig, axes = plt.subplots(1, 2, figsize=(11.4, 4.9), dpi=200)
    ax = axes[0]
    for iso, (x, y, reg) in ready.items():
        if y is None: continue
        ax.scatter(x, y, s=70, color=regcol.get(reg, GREY), zorder=3, alpha=0.9)
        if iso in {"QAT", "SAU", "JOR", "IND", "ARE", "DEU", "FRA", "SGP"}:
            ax.annotate(iso, (x, y), textcoords="offset points", xytext=(5, 4), fontsize=9, color="#333333")
    ax.plot([30, 105], [30, 105], ls="--", lw=1, color="#CCCCCC", zorder=1)
    ax.text(97, 91, "reports match reality", fontsize=8.5, color="#999999", rotation=38, ha="right")
    ax.set_xlabel("What governments report to the UN (score out of 100)", fontsize=10.5)
    ax.set_ylabel("How customs actually performs\n(World Bank score out of 100)", fontsize=10.5)
    ax.set_title("(a) What governments say about themselves\ndoesn't match how they perform", fontsize=11.5, color=NAVY, loc="left")
    ax.set_xlim(58, 106); ax.set_ylim(25, 95)
    ax = axes[1]
    for iso, jv in tfi_j.items():
        if iso not in lpin: continue
        ax.scatter(jv, lpin[iso], s=70, color=regcol.get(region.get(iso, "?"), GREY), zorder=3, alpha=0.9)
        if iso in {"QAT", "SAU", "KWT", "IND", "ARE", "DEU", "FRA", "NLD", "SGP"}:
            ax.annotate(iso, (jv, lpin[iso]), textcoords="offset points", xytext=(5, 4), fontsize=9, color="#333333")
    ax.set_xlabel("Cross-border cooperation, scored by OECD assessors (0–2)", fontsize=10.5)
    ax.set_ylabel("How customs actually performs\n(World Bank score out of 100)", fontsize=10.5)
    ax.set_title("(b) What independent assessors measure\ntracks performance closely", fontsize=11.5, color=NAVY, loc="left")
    ax.set_xlim(0.3, 2.05); ax.set_ylim(25, 95)
    handles = [plt.Line2D([], [], marker="o", ls="", color=c, label=leglab[r]) for r, c in regcol.items()]
    fig.legend(handles=handles, loc="lower center", ncol=5, frameon=False, fontsize=9.5, bbox_to_anchor=(0.5, -0.02))
    for ax in axes:
        for s in ["top", "right"]: ax.spines[s].set_visible(False)
        ax.grid(color="#F0F0F0", lw=0.7, zorder=0)
    source_note(fig, "Data: UN Global Survey (2025); OECD Trade Facilitation Indicators (2025); World Bank Logistics Performance Index (2022)")
    plt.tight_layout(rect=[0, 0.05, 1, 1])
    plt.savefig("figures/chart_contrast_scatter.png", bbox_inches="tight")
    plt.savefig("figures/chart_contrast_scatter.svg", bbox_inches="tight")  # editable vector for Figma/Illustrator
    plt.close()

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
    fig, ax = plt.subplots(figsize=(9.6, 4.4), dpi=200)
    cols = [BLUE, BLUE, BLUE, NAVY]
    for i, (lab, med, p10, p90) in enumerate(steps):
        ax.bar(i, med, width=0.56, color=cols[i], zorder=2)
        ax.errorbar(i, med, yerr=[[med - p10], [p90 - med]], fmt="none", ecolor="#666666",
                    elinewidth=1.6, capsize=6, capthick=1.6, zorder=3)
        ax.text(i, p90 + 0.08, f"${med:.2f}bn", ha="center", fontsize=12.5, fontweight="bold", color=NAVY)
    ax.axhline(0.64, color=RED, lw=1.4, ls="--", zorder=1)  # most conservative version of the estimate
    ax.text(-0.42, 0.70, "most conservative estimate: $0.64bn per year",
            fontsize=9.5, color=RED, ha="left", va="bottom")
    ax.set_xticks(range(len(steps))); ax.set_xticklabels([s[0] for s in steps], fontsize=11.5)
    ax.set_ylabel("Estimated savings, $ billions per year", fontsize=11, color="#333333")
    ax.set_ylim(0, 2.75); ax.set_xlim(-0.55, 3.55)
    ax.set_title("What connecting the corridor's paperwork is worth, each year",
                 fontsize=13.5, fontweight="bold", color=NAVY, loc="left", pad=12)
    ax.text(0.005, 1.005, "Bars show the typical estimate; thin lines show the range across thousands of runs with different assumptions.",
            transform=ax.transAxes, fontsize=9, color="#666666", va="bottom")
    for s in ["top", "right"]: ax.spines[s].set_visible(False)
    ax.grid(axis="y", color="#EEEEEE", lw=0.8, zorder=0)
    source_note(fig, "Data: UN Comtrade & GCC-Stat trade values (2019–2023); savings rate calibrated to the ASEAN Single Window's realized savings")
    plt.tight_layout(); plt.savefig("figures/chart_savings_steps.png", bbox_inches="tight")
    plt.savefig("figures/chart_savings_steps.svg", bbox_inches="tight")  # editable vector for Figma/Illustrator
    plt.close()

# --------------------------------------------- Figure 5: three-step diagram
def fig_threestep():
    fig, ax = plt.subplots(figsize=(9.6, 3.3), dpi=200)
    ax.axis("off")
    boxes = [(0.02, "STEP 1 - now", "UAE-India link",
              "Digital channel already running\n(since May 2026)\nExpand it to full document exchange", "$0.23bn/yr", BLUE),
             (0.36, "STEP 2 - 2026-28", "Gulf integration",
              "Turn the Gulf states' January 2026\ncustoms-data agreement\ninto a working system", "$0.45bn/yr", RED),
             (0.70, "STEP 3 - to ~2031", "EU connection",
              "Connect to the EU's own customs\nsingle window, through the\nUAE-EU trade deal being negotiated", "$0.92bn/yr", NAVY)]
    for x, step, title, body, val, c in boxes:
        ax.add_patch(plt.Rectangle((x, 0.08), 0.28, 0.84, facecolor="#F4F6FA", edgecolor=c, lw=2))
        ax.text(x + 0.14, 0.86, step, ha="center", fontsize=10.5, fontweight="bold", color=c)
        ax.text(x + 0.14, 0.72, title, ha="center", fontsize=12, fontweight="bold", color="#222222")
        ax.text(x + 0.14, 0.44, body, ha="center", fontsize=9, color="#444444")
        ax.text(x + 0.14, 0.15, val, ha="center", fontsize=11.5, fontweight="bold", color=c)
    for x in (0.315, 0.655):
        ax.annotate("", xy=(x + 0.04, 0.5), xytext=(x, 0.5),
                    arrowprops=dict(arrowstyle="-|>", color="#888888", lw=2))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    source_note(fig, "Savings estimates from this analysis; each step's anchor is a signed commitment (see post)")
    plt.tight_layout(); plt.savefig("figures/chartB_threestep.png", bbox_inches="tight")
    plt.savefig("figures/chartB_threestep.svg", bbox_inches="tight")  # editable vector for Figma/Illustrator
    plt.close()

if __name__ == "__main__":
    fig_untfs_trend()
    fig_tfi_gap()
    fig_contrast_scatter()
    fig_savings_steps()
    fig_threestep()
    print("All figures written to ./figures/")
