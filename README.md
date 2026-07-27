# Can the IMEC Corridor Go Paperless? — Data & Code

Final project for **MSPP-GP.3101 Policy and Data Studio** (NYU Wagner, July 2026).
Author: Mohammad Eisa AlDarmaki.

This repository contains all data, code, and documentation behind the post
**"IMEC's Missing Digital Pillar: What Connecting the Corridor's Customs
Systems Is Worth"** (published on Medium, July 2026). Every figure and number in the post can be reproduced
from here.

## What's in the box

| Piece | Files |
|---|---|
| Raw data | `data/raw/*.csv` — each dataset documented in `SOURCES.md`; per-dataset caveats in `data/raw/*_NOTES.md` and `METHODS.md` |
| Analysis (R) | `readiness_index.R` (readiness scorecard + cross-checks), `savings_model.R` (savings scenarios with sensitivity ranges), `analysis.R` (earlier LPI exercise) |
| Data pulls (Python) | `pull_worldbank_exports.py` — reproducible World Bank pull for the map dataset |
| Figures (Python) | `make_figures.py` (Figures 1–5), `make_map.py` (static six-panel map), `make_map_gif.py` (animated GIF version), `make_flourish_data.py` (data for the interactive map) |
| Processed data | `data/processed/flourish_map_data.csv` — feeds the interactive map |
| Results | `output/*.csv` |
| Figures as shipped | `figures/*.png` (post), `figures/*.svg` (editable vectors), `figures/chartB_asw_map_animated.gif` |

## The interactive map (Figure 6)

The post's Figure 6 is an interactive choropleth with a year slider and hover
values, published on Flourish:
https://public.flourish.studio/visualisation/29808313/

It renders `data/processed/flourish_map_data.csv` (built by
`make_flourish_data.py` from the same World Bank dataset as the static map).
In Flourish's Projection map template: bind `ISO3` to the region IDs, the ten
year columns to "Color by" (this creates the slider), and `Status` to the
popup metadata; diverging scale fixed at −20 / 0 / +30 to match the static
palette. The static six-panel version (`make_map.py`) and an animated GIF
(`make_map_gif.py`) are in `figures/` for contexts without embeds.

## How to rerun everything

**R analysis** — open `IMEC_LPI_Rproject.Rproj` in RStudio, then:
```r
install.packages("tidyverse")
source("readiness_index.R")   # -> output/readiness_scorecard.csv
source("savings_model.R")     # -> output/savings_results_*.csv
```

**Figures** — from the repo root:
```
pip install matplotlib "geopandas==0.13.2" "fiona==1.9.6" Pillow requests
python make_figures.py            # Figures 1-5 -> figures/
python make_map.py                # static map -> figures/
python make_map_gif.py            # animated map -> figures/
python make_flourish_data.py      # interactive-map data -> data/processed/
python pull_worldbank_exports.py  # optional: refresh the map dataset
```
(geopandas 0.13.x is pinned because it bundles the Natural Earth country
shapes, so the maps render offline.)

## Figure-to-data map

- **Fig 1** (reported digitization trend) ← `data/raw/untfs_corridor_raw.csv`
- **Fig 2** (automation at home vs cross-border co-operation) ← `data/raw/oecd_tfi_corridor.csv`
- **Fig 3** (implementation scores vs rated efficiency) ← `output/readiness_scorecard.csv` + `data/raw/lpi_corridor_raw.csv` + the OECD file
- **Fig 4** (savings scenarios by corridor step) ← `output/savings_results_by_step.csv` (built by `savings_model.R` from the trade CSVs)
- **Fig 5** (three-step path) — schematic
- **Fig 6** (interactive year-by-year export map) ← `data/processed/flourish_map_data.csv` ← `data/raw/merch_exports_asw_window.csv` (built by `pull_worldbank_exports.py`)

## Honesty file

`METHODS.md` records how each dataset was obtained, what was reconstructed
versus read directly, and every known limitation the post summarizes —
including why all savings figures are presented as scenarios rather than
predictions (published ASEAN benchmark figures diverge; see the
reconciliation note in `SOURCES.md`) and why the map is exploratory rather
than causal.
