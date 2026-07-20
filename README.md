# IMEC single-window — evidence base

## Start here (NYU Wagner Policy & Data Studio — final project)

This repository contains all data, code, and documentation behind the Medium
post **"The Middle East Built the World's Newest Trade Corridor on Paper.
Literally."** Everything in the post can be reproduced from here:

1. **Data** — `data/raw/` (every dataset documented in `SOURCES.md`, with
   provenance and confidence tiers in `METHODS_AND_AUDIT.md`).
2. **Analysis** — `readiness_index.R` (readiness scorecard + cross-checks) and
   `savings_model.R` (the savings estimate; sensitivity ranges), both written
   to `output/`. Open `IMEC_LPI_Rproject.Rproj` in RStudio and
   `install.packages("tidyverse")` to rerun.
3. **Figures** — `make_figures.py` (Figures 1–5) and `make_map.py` (Figure 6);
   `pip install matplotlib "geopandas==0.13.2"` and run each from the repo
   root. PNGs and editable SVGs are written to `figures/`.
4. **Every caveat** the post summarizes (reconstructed survey scores, stale
   UAE data, sensitivity-not-confidence ranges, exploratory map) is recorded
   in `METHODS_AND_AUDIT.md` §4.

The sections below describe the wider evidence base this project is drawn
from.

Data and analysis for a policy paper on building a shared digital customs system
(a "single window") along the India–Middle East–Europe Economic Corridor (IMEC).
Author: Mohammad Eisa AlDarmaki.

**Thesis / anchor framing:** replicate the ASEAN Single Window model → integrate
the GCC / Middle East as the first step (starting from the existing UAE–India
link) → connect to the EU's mature system.

## The finding, in one line

Every corridor economy has legally committed to a national single window (WTO TFA
100%) and mostly built one (UNTFS), but the cross-border layer that connects them
is weak — because the anchors are among the world's most data-restrictive
economies with no open-data commitments (DTI) — so real performance lags the
paper status (LPI). The gap is being closed bilaterally, outward from the UAE,
through its CEPA network (India, Jordan, Israel, Indonesia… and now the EU).

## Datasets (see `SOURCES.md` and `METHODS_AND_AUDIT.md`)

| Layer | Dataset | File |
|---|---|---|
| Legal commitment | WTO TFA | `data/raw/wto_tfa_corridor.csv` |
| Implementation (built) | UN Trade Facilitation Survey | `data/raw/untfs_corridor_raw.csv` |
| Cross-border legal layer | CPTA + UAE CEPAs | `data/raw/cross_border_legal_layer.csv`, `uae_cepa_digital_verification.csv` |
| Why cross-border lags | Digital Trade Integration | `data/raw/dti_region_summary.csv` |
| Performance | World Bank LPI | `data/raw/lpi_corridor_raw.csv` |
| Trade base / savings | UN Comtrade + ASEAN | `data/raw/corridor_trade_flows.csv`, `asean_calibration.csv` |

## Analysis outputs

- `output/readiness_scorecard.csv` — triangulated readiness index (UNTFS + LPI).
- `output/savings_results_by_step.csv` — benefit model results (cost savings +
  trade creation), by corridor step.
- `output/lpi_corridor_summary.csv`, `lpi_latest_ranking_2022.csv` — LPI summaries.

## Headline numbers (5-yr 2019–2023 avg base; ranges = Monte Carlo sensitivity)

- Corridor goods trade in scope: ~$415bn (5-yr average; $482bn in 2023 alone).
- Cost savings from a single window: **median ~$1.4bn/yr (P10–P90 $0.8–2.4bn)**,
  estimated two independent ways that converge — ASEAN-calibrated (~$1.6bn) and
  ESCAP/OECD top-down (~$1.3bn).
- Trade creation: median ~$7.5bn/yr additional trade (ESCAP-benchmarked).
- Largest prize: the EU connection — the exact leg the UAE–EU CEPA is now
  negotiating (talks launched 28 May 2025).

## Reproduce

Open `IMEC_LPI_Rproject.Rproj` in RStudio; `install.packages("tidyverse")`.

## Figures for the Medium post (Stream B)

`make_figures.py` regenerates every figure in the published post ("The Middle
East Built the World's Newest Trade Corridor on Paper. Literally.") from the
CSVs in this repository — no external downloads needed.

```
pip install matplotlib
python make_figures.py        # writes PNGs to ./figures/
```

Figure-to-data map: Fig 1 ← `data/raw/untfs_corridor_raw.csv`; Fig 2 ←
`data/raw/oecd_tfi_corridor.csv`; Fig 3 ← `output/readiness_scorecard.csv` +
`data/raw/lpi_corridor_raw.csv` + the TFI file; Fig 4 ←
`output/savings_results_by_step.csv` (built by `savings_model.R`); Fig 5 is a
schematic of the build plan. Methods and caveats: `METHODS_AND_AUDIT.md`.


- `savings_model.R` — reads `corridor_trade_flows.csv` + `asean_calibration.csv`,
  runs the Monte Carlo, writes the savings outputs.
- `readiness_index.R` — builds `output/readiness_scorecard.csv` from UNTFS + LPI.
- `analysis.R` — the original LPI tidyverse exercise (Assignment 1) producing the
  two LPI summary CSVs.

## Provenance and honesty

`METHODS_AND_AUDIT.md` records every dataset's confidence tier (direct pull /
derived / estimated / inferred), all transformations, and the open limitations.
`SOURCES.md` is the full citation list. Key disclosed caveats: UNTFS percentages
are reconstructed (validated, not read); EU WTO TFA values are inferred from the
entry-into-force rule; DTI figures are policy counts, not a normalized index; and
the savings rate is anchored to ASW's partial (e-CoO) scope, scaled 1–4× for a
fuller single window.
