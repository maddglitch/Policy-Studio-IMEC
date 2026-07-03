# OECD Trade Facilitation Indicators (TFI) — objective layer

Added July 2026. **PULLED 1 Jul 2026** → `data/raw/oecd_tfi_corridor.csv`
(21 economies × 11 dimensions, values 0–2). Method: the OECD Policy Simulator's
data endpoints (`sim.oecd.org/Graph.ashx?lang=En&ds=TFI&d1c=<group>&d2c=<ISO3>`,
where group ∈ oecd / hinoecd / umic / lmic — the country's income group;
dimension labels identical across all 21, verified). Vintage: 2025 per OECD
*TFI: Monitoring Policies up to 2025* (March 2025) — **to verify**: the
simulator does not display the vintage year explicitly; cross-check a few
values against the Compare-your-country 2025 edition before publication.

## Headline finding from the pull (the thesis, in OECD's own assessment)
Gap = (g) Formalities–automation minus (j) External border agency co-operation:

| Region | Mean gap |
|---|---|
| Gulf | **+0.58** |
| India | **+0.51** |
| Levant | +0.33 |
| ASEAN (has ASW) | +0.13 |
| Europe (EU) | −0.01 |

The **UAE has the largest gap in the corridor (+0.95: automation 1.85/2,
external cooperation 0.90/2)**. Objectively measured: the corridor's anchors
have world-class national systems and the weakest cross-border layer —
independent, non-self-reported confirmation of the staircase. ASEAN's small
gap is consistent with the ASW having closed it (supports the calibration).

## Why
Closes limitation §4.3/§4.8 (METHODS): WTO TFA and UNTFS are self-reports and
saturate; LPI is perception-based. The TFIs are **OECD-assessed policy
indicators** (163 economies, 2025 vintage, "Monitoring Policies up to 2025",
March 2025) — an independent, non-self-reported read on the same construct.

## What to take (per corridor economy)
The TFI dimensions closest to the paper's constructs:
- **(g) Formalities – automation** (electronic exchange, automated processing,
  digital signatures) → maps to the UNTFS "paperless" layer.
- **(h) Formalities – documents** (simplification, acceptance of copies).
- **(i/j) Border agency cooperation, internal & external** → maps directly to
  the weak cross-border layer; *external* cooperation is the paper's core gap.
- **(c) Involvement of the trade community** and **(a) Information
  availability** as secondary checks.

Expected pattern if the thesis holds: corridor economies score well on
automation (g) but weaker on external border-agency cooperation (j) — the
objective mirror of the UNTFS-vs-LPI divergence.

## How to pull
- Compare-your-country tool / Trade Facilitation Policy Simulator:
  https://sim.oecd.org/default.ashx?ds=TFI (per-country values, all 11 dims).
- OECD Data Explorer (SDMX): search "Trade Facilitation Indicators"
  (OECD.TAD.TPD); export CSV for the 21 corridor/comparator economies.
  NB: the public SDMX endpoint returned structure XML only when scripted
  July 2026 — pulling via the Data Explorer UI export is the reliable route.
- Publication (regional aggregates, method): OECD, *OECD Trade Facilitation
  Indicators: Monitoring Policies up to 2025*, March 2025.

Target file: `data/raw/oecd_tfi_corridor.csv`
(iso, dimension_code, dimension, value_0_2, vintage).

## Optional companion (hard time-based measure)
World Bank **Container Port Performance Index** (CPPI) for corridor ports —
Jebel Ali, Mundra/Nhava Sheva, Jeddah, Piraeus, Rotterdam, Haifa — actual
vessel-time performance; would be the only non-survey, non-perception measure
in the set.

Confidence when pulled: **Direct** (OECD-assessed, not self-reported).
