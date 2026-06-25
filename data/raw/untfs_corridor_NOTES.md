# UNTFS corridor dataset — provenance & caveats

**File:** `untfs_corridor_raw.csv` (primary dataset for the IMEC project).

**Source:** UN Global Survey on Digital and Sustainable Trade Facilitation (UNTFS),
joint initiative of the UN Regional Commissions and UNCTAD, coordinated by ESCAP.
Pulled from the public dashboard at https://untfsurvey.org (Global Data + Economy
Briefs), waves 2015, 2017, 2019, 2021, 2023, 2025.

**Citation:** United Nations (2025). *Digital and Sustainable Trade Facilitation:
Global Report 2025*, United Nations, ESCAP, Bangkok. Available at https://untfsurvey.org

**Coverage:** 20 economies along the corridor plus an ASEAN benchmark —
Gulf (ARE, SAU, QAT, KWT, BHR, OMN), India (IND), Levant (JOR; Israel had no
machine-readable series), Europe (DEU, FRA, ITA, NLD, ESP, GRC), ASEAN (SGP, MYS,
THA, VNM, IDN, PHL). 103 economy-year rows.

**Columns:** `overall` and the five core group implementation rates
(`transparency`, `formalities`, `institutional`, `paperless`, `crossborder`),
each a 0–100% rate; `single_window_stage` (the "Electronic Single Window System"
measure) and its numeric `single_window_score` (Fully=3, Partially=2,
Planning/Not implemented=0; blank = not reported that wave).

**Method note:** group rates were read from the dashboard's per-economy data;
`overall` is the mean of the five core groups (verified to reconcile within 0.006).
The single-window stage was read from each economy's measure-by-year brief.

**Caveats (important for analysis):**
- **UAE reported only in 2015 and 2017.** The anchor economy of the whole thesis
  has no UNTFS data after 2017 — its recent single-window/paperless status is not
  tracked by this survey and must be sourced separately (e.g., MAITRI, FASAH docs).
- **Carry-forward:** 16 rows repeat the previous wave's values exactly. The survey
  carries the last reported value forward when an economy does not resubmit, so some
  "2025" figures reflect the prior wave. Treat consecutive identical rows as
  "last known," not fresh observations.
- Some economies enter the panel late (Kuwait, Oman: 2023 onward; Saudi: 2019 onward;
  Bahrain missing 2019; Qatar missing 2019/2021).
- Europe is represented by member states here; for bloc-level trade figures the
  project treats the EU as one partner (separate trade dataset).
