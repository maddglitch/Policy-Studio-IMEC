# Project brief — IMEC single-window policy paper (session handoff)

## What this is
A policy paper (NYU Wagner Applied Policy Analysis; goal is a publishable/
circulatable paper) arguing that a shared digital customs "single window" can be
built along the India–Middle East–Europe Economic Corridor (IMEC) by **replicating
the ASEAN Single Window model → integrating the GCC/Middle East as the first step
(starting from the existing UAE–India link) → connecting to the EU's mature
system.** Falsifiable hypothesis: the real obstacles are legal/political, not
technical.

Two streams, shared evidence: **Stream A** = technical analysis (the rigorous
backbone, all data/numbers). **Stream B** = narrative paper for a general policy
audience, built from A's findings. Don't let B invent claims A hasn't established.

## Where it stands
The **evidence base is complete and audited.** Six datasets pulled, verified,
documented, and cited; a two-part benefit model calibrated and stress-tested; full
provenance written up. **The next step is drafting** (Stream A first — its methods
section is essentially pre-written by `METHODS_AND_AUDIT.md`).

## The core finding (a "staircase")
Every corridor economy has legally committed to a national single window (WTO TFA
100%) and mostly built one (UNTFS), **but the cross-border layer that connects
them is weak** — because the anchors (India, the Gulf) are among the world's most
data-restrictive economies with no open-data commitments (DTI) — so real
performance lags the paper status (LPI). The gap is being closed bilaterally,
**outward from the UAE** via its CEPA network (India, Jordan, Israel, Indonesia,
Vietnam, Malaysia… and now the **UAE–EU CEPA**, in negotiation since May 2025 with
digital trade an explicit focus). The UAE–Indonesia CEPA already does the actual
ASW mechanism (electronic Certificate-of-Origin exchange + AEO mutual recognition).

## Headline numbers (5-yr 2019–2023 avg base; ranges = MC sensitivity)
- Corridor goods trade in scope: ~$415bn (5-yr avg).
- **Cost savings from a single window: median ~$1.4bn/yr ($0.8–2.4bn)** — two
  independent methods converge (ASEAN-calibrated ~$1.6bn; ESCAP/OECD top-down ~$1.3bn).
- **Trade creation: ~$7.5bn/yr additional trade** (ESCAP-benchmarked; illustrative).
- Largest prize on both counts: the EU connection — the leg the UAE–EU CEPA covers.

## Datasets (all in `data/raw/`; sources in `SOURCES.md`)
WTO TFA (legal), UNTFS (implementation), CPTA + UAE CEPAs (cross-border legal
layer), DTI (why cross-border lags), World Bank LPI (performance), UN Comtrade
2019–2023 + ASEAN/GCC-Stat (trade base & calibration).

## Files (repo: IMEC_LPI_Rproject/Policy-Studio-IMEC/, GitHub: maddglitch/Policy-Studio-IMEC)
- `README.md` — orientation. `METHODS_AND_AUDIT.md` — provenance + confidence tiers
  + limitations. `SOURCES.md` — full citations.
- Scripts: `savings_model.R`, `readiness_index.R`, `analysis.R` (LPI/Assignment 1).
- Outputs: `output/readiness_scorecard.csv`, `output/savings_results_*.csv`.

## Caveats to preserve in the writing (don't overclaim)
1. UNTFS implementation percentages are **reconstructed** from the dashboard, not
   read directly (validated on spot checks).
2. Monte Carlo ranges are **prior-driven sensitivity bands**, not confidence intervals.
3. Trade creation attribution to a single window is **not causally identified** — illustrative.
4. **A CEPA digital chapter ≠ working cross-border interoperability** (only UAE–Indonesia
   goes that far). Keep "signed a chapter" distinct from "operating a system."
5. Self-reported sources (TFA, UNTFS) saturate; the ASEAN analogy has limits (one bloc
   vs three regimes). Triangulation (UNTFS-vs-LPI, corr ~0.00 on n=20 after the July
   2026 LPI extension; was −0.06 on n=14) is indicative, not proof.
6. Open data gaps: UAE's own UNTFS is stale (2017) and it's absent from the DTI sample.

## Suggested first ask for the new session
"Draft Stream A (the technical analysis) from the evidence base in
`METHODS_AND_AUDIT.md` and the data files, following the Assignment 1 section
outline. Keep the caveats above intact."
