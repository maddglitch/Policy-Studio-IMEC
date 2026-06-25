# IMEC single-window project — methods, sources, and audit

This document records every dataset used, how it was obtained, what was read
directly versus derived or assumed, and the known limitations. It is the
provenance backbone for Stream A. Last updated June 2026.
**Full citations (publishers, URLs, access dates) are in `SOURCES.md`.**

Anchor framing (fixed): replicate the **ASEAN Single Window** model →
**GCC / Middle East** as the first step → connect to the **EU**'s mature system.

---

## 1. Data inventory and confidence

| Dataset | File | Source | Confidence |
|---|---|---|---|
| Logistics Performance Index | `data/raw/lpi_corridor_raw.csv` | World Bank Indicators API (source 51) | Direct pull |
| UN Trade Facilitation Survey | `data/raw/untfs_corridor_raw.csv` | untfsurvey.org dashboard | Derived (see 2.2) |
| WTO TFA commitments | `data/raw/wto_tfa_corridor.csv` | tfadatabase.org | Direct (developing) / inferred (EU) |
| CPTA + UAE CEPAs | `data/raw/cross_border_legal_layer.csv`, `uae_cepa_digital_verification.csv` | ESCAP, govt texts, ESCAP CBPT DB, EU Commission | Direct |
| Digital Trade Integration | `data/raw/dti_region_summary.csv` | DTI database via published paper | Evidence, policy counts |
| Trade volumes | `data/raw/corridor_trade_flows.csv` | UN Comtrade API (2023) | Direct (energy shares grounded) |
| ASEAN calibration | `data/raw/asean_calibration.csv` | ASEANstats, USAID/MOIT, ESCAP | Direct |

Tiers: **Direct** (read from source), **Derived** (computed from direct data —
valid only if the method is), **Estimated** (judgement), **Inferred** (from one
source / a rule, not independently pulled).

---

## 2. Per-dataset notes

### 2.1 LPI (Direct)
World Bank API, 15 economies, 4 sub-indices, 2007–2022. India was re-fetched
separately after a truncated bulk pull and stitched in — re-verify. Used as the
performance check (perceived customs efficiency).

### 2.2 UNTFS (Derived — important)
Read from the dashboard's in-page data. **The implementation percentages are
reconstructed, not read**: each indicator's maximum was back-computed from the
regional aggregate scores, then converted to a percent. Validated against the
UAE spider (100% = 27/27; 77.8% = 14/18) and India 2023 (~93.5 vs computed
93.33). "Overall" = our mean of the five core groups. Single-window stage read
directly. Caveats: UAE reported only 2015 & 2017; 16 carry-forward rows.

### 2.3 WTO TFA (Direct for developing; Inferred for EU)
Single-window column (Art 10.4) and 36-measure matrix read directly for 14
developing corridor members + Saudi — all 100%. **EU members set to 100% by the
entry-into-force rule** — not pulled.

### 2.4 CPTA + UAE CEPAs (Direct)
CPTA: Philippines and Thailand are parties; the Gulf, Levant and EU are not
ESCAP-eligible. UAE CEPA digital chapters verified per agreement — India,
Indonesia (ESCAP-catalogued; e-CoO exchange + AEO), Israel (Ch 9 Arts
9.6/9.7/9.8), Vietnam, Malaysia, Türkiye, and now **Jordan (confirmed: Ch 4 Art
4.5 paperless communications + AEO mutual administrative assistance + digital
chapter)**. **NEW: the UAE–EU CEPA — talks launched 28 May 2025, first round
June 2025, 4th round Dec 2025, with digital trade an explicit focus.** This puts
the corridor's one empty leg (EU–Gulf) into active negotiation, via a UAE CEPA,
exactly as the thesis predicts.

### 2.5 DTI (Evidence — policy counts, not an index)
Figures are **policy counts (2023)** from the published paper (Ferracane et al.,
*World Trade Review* 2026); the live database is blocked on the UAE network. Not
a normalised index. The UAE and Qatar are not in the paper's country sample.
**UAE's own data stance (qualitative, sourced — Clifford Chance 2025;
Addleshaw Goddard 2026; DIFC DP Law 5/2020; ADGM DP Regs 2021):** relatively
open — DIFC and ADGM run GDPR-aligned regimes with adequacy mechanisms / SCCs /
BCRs; mandatory localisation only in narrow sectors (health, banking). This is
*why* the UAE, uniquely in MENA, can carry cross-border data-flow commitments in
its CEPAs. (Full refs in `SOURCES.md`.)

### 2.6 Trade volumes (Direct — multi-year, energy shares grounded)
UN Comtrade API, **2019–2023 goods panel** (`corridor_trade_multiyear.csv`),
all-modes aggregate; EU as reporter (97). 5-year averages used as the model base:
UAE–India $65.2bn (33% energy), India–EU $103.3bn (8% energy — grounded: EU HS27
imports from India $9.15bn), Gulf–EU $134.0bn (35% energy — grounded: EU HS27
imports Saudi/UAE/Qatar = $54.7bn in 2023; Gulf–EU = Saudi+UAE+Qatar, excludes
Kuwait/Oman/Bahrain), intra-Gulf $112.2bn (GCC-Stat; 2023 = $133bn). Only the
intra-Gulf energy share (~20%) and its 2019/21/22 levels remain estimates.

---

## 3. The benefit model (`savings_model.R`)

Two benefits, both ranges from a 50,000-draw Monte Carlo. **Trade base is a
5-year average (2019–2023), not a single year** (`corridor_trade_multiyear.csv`),
to smooth the COVID 2020 trough, the 2022 energy spike and soft 2023. 5-yr-avg
base ≈ **$415bn** (vs $482bn in 2023 alone).

**Cost savings is estimated two independent ways, so it is not single-anchored:**
- *Method 1 (ASEAN-calibrated):* ASW saved ~$6.4bn over 2018–2022 (~$1.28bn/yr)
  on intra-ASEAN trade averaging ~$677bn → realised rate **~0.19% of trade/yr**.
  ASW is a *partial* single window (e-Form D), so 0.19% is scaled by a `scope`
  multiplier ∈ [1,4] (1 = ASW-equivalent; 4 = full multi-document SW). → **median
  ~$1.61bn/yr (P10–P90 $0.8–2.4bn)**.
- *Method 2 (ESCAP/OECD top-down):* documentary/procedural costs ~1–3% of trade
  value, cut ~10–31% by a single window (ESCAP). → **median ~$1.29bn/yr (P10–P90
  $0.7–2.3bn)**.
- The two methods bracket each other; **combined median ~$1.44bn/yr (P10–P90
  $0.8–2.4bn)**. By step (Method 1): anchor (UAE–India) $0.23bn, Gulf integration
  $0.45bn, connect-EU $0.92bn. Energy weighted 0.15–0.35× manufactured intensity.

**Trade creation** = energy-discounted base × boost, boost ∈ [1.0%, 3.4%] (3.4% =
ESCAP "up to $257bn/yr" Asia-Pacific export gain). Result: **median ~$7.5bn/yr
additional corridor trade (P10–P90 $4.2–10.8bn)** — gross trade, not net welfare,
attribution to a single window illustrative.

**Back-test:** 0.19% × ASEAN's 2018 base (~$620bn) ≈ $1.17bn/yr, in line with
ASW's realised ~$1.28bn (consistent by construction).

---

## 4. Remaining limitations / to-fix

1. **Monte Carlo ranges reflect chosen priors**, not empirical confidence
   intervals — describe as sensitivity bands.
2. **Trade creation** uses ESCAP's upper-bound elasticity; attribution to a single
   window specifically is not identified — present as illustrative.
3. **Self-reporting saturation:** WTO TFA and UNTFS are government self-reports and
   both saturate (TFA 100%; UNTFS single window mostly "full"); LPI is the one
   independent counterweight but is itself perception-based. No hard objective
   measure (actual e-document volumes / clearance times) is in the set.
4. **Triangulation is indicative, not proof.** The UNTFS-vs-LPI divergence
   (rank corr −0.06) rests on n=14, a year mismatch (LPI 2022 vs UNTFS 2025) and
   two different constructs (self-reported implementation vs perceived
   performance). State it as suggestive.
5. **Scope:** trade is **goods only** (services excluded); the Gulf–EU base is the
   three largest GCC states (excludes Kuwait/Oman/Bahrain ~$6–15bn); intra-Gulf
   energy share (~20%) and 2018–19/intra-Gulf early-year values remain estimates.
6. **Conceptual:** a CEPA digital *chapter* ≠ working cross-border *interoperability*
   (only the UAE–Indonesia CEPA goes to e-CoO exchange + AEO MRA); and ASEAN is one
   bloc under one agreement whereas the corridor spans three regimes — the analogy
   has limits. Keep "signed a chapter" distinct from "operating a system."
7. Still to obtain: **UAE's own UNTFS** (stale after 2017) and **DTI index score**
   (UAE not in the paper sample); re-verify the **India LPI** stitched rows and the
   **EU TFA** inference.

CLOSED since first audits: Jordan CEPA text confirmed; energy shares grounded in
HS27; intra-Gulf value pulled (GCC-Stat); UAE–EU CEPA added; UAE data-policy stance
sourced; **trade base extended to a 5-year (2019–2023) average**; **savings
de-single-anchored with a second independent (ESCAP/OECD) method**; **readiness
double-count fixed** (now mean of paperless + cross-border + single-window only).
