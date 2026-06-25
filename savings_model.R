# IMEC single-window benefit model (Monte Carlo, two independent methods)
# Author: Mohammad Eisa AlDarmaki
#
# Estimates two benefits of a corridor single window, as RANGES:
#   (1) COST SAVINGS  - lower trade-transaction costs
#   (2) TRADE CREATION - additional trade the lower costs generate
#
# Trade base is a 5-YEAR AVERAGE (2019-2023), not a single year, to smooth
# volatility (COVID 2020 trough, 2022 energy-price spike, soft 2023). See
# data/raw/corridor_trade_multiyear.csv.
#
# COST SAVINGS is estimated TWO independent ways so it is not single-anchored:
#   Method 1 (ASEAN-calibrated): the ASEAN Single Window saved ~$6.4bn over
#     2018-2022 (~$1.28bn/yr) on intra-ASEAN trade averaging ~$677bn -> a
#     realised rate of ~0.19% of trade value/yr. ASW is a PARTIAL single window
#     (mainly the e-Form D certificate of origin), so we scale 0.19% by a
#     "scope" multiplier of 1x (ASW-equivalent) to 4x (full multi-document SW).
#   Method 2 (ESCAP/OECD top-down): documentary/procedural trade costs are
#     ~1-3% of trade value; a single window cuts them ~10-31% (ESCAP).
# Energy/commodities are discounted (bulk shipments are far less
# document-intensive per dollar than manufactured goods).
#
# TRADE CREATION is benchmarked on ESCAP's estimate that full regional digital
# trade facilitation could lift exports ~3.4% (up to $257bn/yr in Asia-Pacific);
# we use a conservative 1.0-3.4% band. It is gross trade, not net welfare, and
# attribution to a single window specifically is illustrative.
#
# See data/raw/asean_calibration.csv and SOURCES.md for every input.

library(tidyverse)

my  <- read_csv("data/raw/corridor_trade_multiyear.csv")
flows <- my |>
  mutate(value = avg_2019_2023) |>
  select(flow, corridor_step, value, energy_share_est)

asw_rate <- 0.00189   # Method 1 anchor: ASW realised savings rate (share of trade/yr)

set.seed(7)
N <- 50000
draws <- tibble(
  scope = runif(N, 1.0, 4.0),    # M1: 1 = ASW-equivalent (e-CoO); 4 = full multi-document SW
  efac  = runif(N, 0.15, 0.35),  # energy/commodity documentary intensity vs manufactured
  dcs   = runif(N, 0.010, 0.030),# M2: documentary/procedural cost as share of trade value
  red   = runif(N, 0.10, 0.31),  # M2: single-window reduction of those costs (ESCAP)
  boost = runif(N, 0.010, 0.034) # trade-creation %: 1.0% (conservative) to 3.4% (ESCAP)
)

per_draw <- function(scope, efac, dcs, red, boost) {
  eff <- flows$value * (1 - flows$energy_share_est) +
         flows$value * flows$energy_share_est * efac        # energy-discounted base
  tibble(
    cost_m1 = sum(eff * asw_rate * scope),                  # Method 1
    cost_m2 = sum(eff * dcs * red),                         # Method 2
    trade   = sum(eff * boost)
  )
}

res <- draws |>
  mutate(out = pmap(list(scope, efac, dcs, red, boost), per_draw)) |>
  unnest(out) |>
  mutate(cost_combined = (cost_m1 + cost_m2) / 2)

q <- function(x, p) as.numeric(quantile(x, p))
summary_tbl <- tibble(
  metric = c("cost_m1_asean", "cost_m2_escap", "cost_combined", "trade_creation"),
  median = c(median(res$cost_m1), median(res$cost_m2), median(res$cost_combined), median(res$trade)),
  p10    = c(q(res$cost_m1,.10), q(res$cost_m2,.10), q(res$cost_combined,.10), q(res$trade,.10)),
  p90    = c(q(res$cost_m1,.90), q(res$cost_m2,.90), q(res$cost_combined,.90), q(res$trade,.90))
) |> mutate(across(median:p90, ~round(.x, 2)))
print(summary_tbl)
write_csv(summary_tbl, "output/savings_results_summary.csv")

# Per-step cost savings (Method 1), -> output/savings_results_by_step.csv
step_draws <- flows |>
  crossing(draws |> mutate(.draw = row_number())) |>
  mutate(eff  = value*(1-energy_share_est) + value*energy_share_est*efac,
         cost = eff * asw_rate * scope)
by_step <- step_draws |>
  group_by(corridor_step, .draw) |>
  summarize(step_cost = sum(cost), .groups = "drop") |>
  group_by(corridor_step) |>
  summarize(median_usd_bn = round(median(step_cost), 2),
            p10_usd_bn = round(q(step_cost,.10), 2),
            p90_usd_bn = round(q(step_cost,.90), 2), .groups = "drop") |>
  mutate(benefit = "cost_savings", .before = 1)
totals <- tibble(
  benefit = c("cost_savings_combined", "trade_creation"),
  corridor_step = c("Total corridor", "Total corridor (additional trade/yr)"),
  median_usd_bn = c(round(median(res$cost_combined),2), round(median(res$trade),2)),
  p10_usd_bn = c(round(q(res$cost_combined,.10),2), round(q(res$trade,.10),2)),
  p90_usd_bn = c(round(q(res$cost_combined,.90),2), round(q(res$trade,.90),2))
)
bind_rows(by_step, totals) |> write_csv("output/savings_results_by_step.csv")
