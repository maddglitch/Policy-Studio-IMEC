# IMEC triangulated readiness index
# Author: Mohammad Eisa AlDarmaki
#
# Builds output/readiness_scorecard.csv from two independent sources:
#   - UNTFS (self-reported digital trade-facilitation implementation)
#   - World Bank LPI customs efficiency (perceived performance)
# The point of the index is the TRIANGULATION: where the two sources diverge
# (notably the Gulf, which self-reports far above its measured performance).
#
# sw_readiness = mean of the three single-window-specific digital dimensions
# (paperless trade, cross-border paperless, single-window measure). It deliberately
# EXCLUDES the survey "overall" to avoid double-counting (overall already embeds
# paperless and cross-border). Indicative, not a weighted index.

library(tidyverse)

untfs <- read_csv("data/raw/untfs_corridor_raw.csv")
lpi   <- read_csv("data/raw/lpi_corridor_raw.csv")

# latest UNTFS wave per economy
untfs_latest <- untfs |>
  group_by(iso) |>
  slice_max(year, n = 1) |>
  ungroup() |>
  mutate(stale = year < 2025)

# latest LPI customs efficiency (LP.LPI.CUST.XQ)
cust <- lpi |>
  filter(indicator_code == "LP.LPI.CUST.XQ") |>
  group_by(iso) |>
  slice_max(year, n = 1) |>
  ungroup() |>
  select(iso, lpi_customs = value)

scorecard <- untfs_latest |>
  left_join(cust, by = "iso") |>
  mutate(
    sw_norm       = round(single_window_score / 3 * 100, 1),  # 0-3 -> 0-100
    lpi_cust_norm = round((lpi_customs - 1) / 4 * 100, 1),     # 1-5 -> 0-100
    sw_readiness  = round((paperless + crossborder + sw_norm) / 3, 1),  # no double-count
    divergence    = round(sw_readiness - lpi_cust_norm, 1)
  ) |>
  arrange(desc(sw_readiness)) |>
  mutate(rank = row_number()) |>
  select(rank, iso, region, untfs_year = year, overall, single_window_score,
         paperless, crossborder, sw_norm, sw_readiness, lpi_customs,
         lpi_cust_norm, divergence, stale)

print(scorecard, n = Inf)
write_csv(scorecard, "output/readiness_scorecard.csv")

# Rank-correlation check (UNTFS readiness vs LPI customs, overlapping economies)
ov <- scorecard |> filter(!is.na(lpi_cust_norm))
message("Spearman rank corr (sw_readiness vs LPI customs, n=",
        nrow(ov), "): ",
        round(cor(rank(ov$sw_readiness), rank(ov$lpi_cust_norm)), 2))
