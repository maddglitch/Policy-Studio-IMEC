# IMEC LPI Analysis

A small R project for a tidyverse data-manipulation assignment.
Author: Mohammad Eisa AlDarmaki.

## The data

World Bank **Logistics Performance Index (LPI)** for 15 economies along the
India–Middle East–Europe Economic Corridor (IMEC) plus an ASEAN benchmark
group, across every survey round from 2007 to 2022. This is one of the
datasets from my IMEC single-window policy project, and was not used in class.

The raw file is `data/raw/lpi_corridor_raw.csv` (long format: one row per
country, indicator and year).

## What the script does

`analysis.R` runs top to bottom and uses the core tidyverse functions:

1. `read_csv()` — import the raw data.
2. `select()` — keep the columns needed.
3. `filter()` — keep only the customs-efficiency score (the LPI pillar closest
   to a "single window").
4. `mutate()` — add a `region` column grouping each economy (India, Gulf,
   Levant, Europe, ASEAN).
5. `group_by()` + `summarize()` — average customs score by region and year.
6. `write_csv()` — export that table to `output/lpi_corridor_summary.csv`.

It then does a second aggregation: `group_by()` + `summarize()` on the 2022
round to rank economies by their customs score, exported to
`output/lpi_latest_ranking_2022.csv`.

## How to run

1. Open `IMEC_LPI_Rproject.Rproj` in RStudio.
2. Run `install.packages("tidyverse")` once if needed.
3. Open `analysis.R` and run it. The two CSVs in `output/` are regenerated.

## Files

```
analysis.R                         the script
data/raw/lpi_corridor_raw.csv      raw input
output/lpi_corridor_summary.csv    avg customs score by region and year
output/lpi_latest_ranking_2022.csv 2022 customs ranking by economy
```

## Data source

World Bank Indicators API (LPI, source 51). Pillar codes:
`LP.LPI.OVRL.XQ` Overall, `LP.LPI.CUST.XQ` Customs,
`LP.LPI.INFR.XQ` Infrastructure, `LP.LPI.TIME.XQ` Timeliness (1 = low, 5 = high).
Browse: https://data360.worldbank.org/
