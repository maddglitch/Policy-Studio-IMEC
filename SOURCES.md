# Sources and citations

Every dataset and key figure used in this project, with its source and what it
backs. Access dates June-July 2026 unless noted. Data pulls are 2023 reference year
unless noted.

## Primary datasets

**UN Global Survey on Digital and Sustainable Trade Facilitation (UNTFS)**
United Nations (2025), *Digital and Sustainable Trade Facilitation: Global
Report 2025*, UN ESCAP, Bangkok. Dashboard: https://www.untfsurvey.org/ (Global
Data and Economy Briefs). Waves 2015–2025. Backs: `untfs_corridor_raw.csv`,
readiness scorecard, the "built" layer of the staircase. NB the implementation
percentages were reconstructed from the dashboard's raw scores — see
`data/raw/untfs_corridor_NOTES.md` and METHODS 2.2.

**World Bank Logistics Performance Index (LPI)**
World Bank, *Logistics Performance Index*, Indicators API source 51;
https://lpi.worldbank.org/ and https://data360.worldbank.org/. Rounds 2007–2023
(latest data point 2022). Backs: `lpi_corridor_raw.csv`, the "performing" layer.
Coverage extended to 21 economies (NLD, ITA, ESP, IDN, VNM, PHL added) and
India's stitched rows re-verified against the API, July 2026.

**EU Single Window Environment for Customs (EU SWE-C)**
Regulation (EU) 2022/2399 of 23 Nov 2022, EUR-Lex (consolidated version
CELEX 02022R2399-20241017); DG TAXUD, "The EU Single Window Environment for
Customs," https://taxation-customs.ec.europa.eu/customs/customs-controls/eu-single-window-environment-customs_en;
EUR-Lex summary: https://eur-lex.europa.eu/EN/legal-content/summary/european-union-single-window-environment-for-customs.html.
In force 12 Dec 2022; G2G (EU CSW-CERTEX) mandatory from 2025, domain expansion
2026–2028; B2G from 13 Dec 2031. Backs: the "EU mature system" step and
`data/raw/eu_swec_NOTES.md`. Accessed July 2026.

**OECD Trade Facilitation Indicators (TFI)**
OECD (March 2025), *OECD Trade Facilitation Indicators: Monitoring Policies up
to 2025*, https://www.oecd.org/en/publications/oecd-trade-facilitation-indicators_fd6f27dc-en.html;
data pulled from the Policy Simulator (https://sim.oecd.org/default.ashx?ds=TFI)
data endpoints, accessed 1 July 2026 — 21 corridor economies × 11 dimensions,
0–2 scale. Backs: `oecd_tfi_corridor.csv`, the objective layer, and the
automation-vs-external-cooperation gap finding. Vintage: 2025 publication (March 2025
update), reflecting policies through 2024 — see `data/raw/oecd_tfi_NOTES.md`.

**WTO Trade Facilitation Agreement Database (TFAD)**
World Trade Organization, *TFA Database*, https://tfadatabase.org/ (Matrix of
current rate of implementation commitments; Member profiles; Art. 10.4 single
window). Backs: `wto_tfa_corridor.csv`, the "legal commitment" layer. Developing
members read directly from the matrix; EU members inferred at 100% from the
developed-member entry-into-force rule (22 Feb 2017) — flagged in the CSV.

**UN Comtrade (trade volumes)**
UN Comtrade, https://comtradeapi.un.org/ (public preview API), **2019–2023 goods**
(5-year panel), HS classification; EU as reporter (code 97, extra-EU). Backs:
`corridor_trade_multiyear.csv` (per-year) and `corridor_trade_flows.csv` (5-yr
avg). HS27 (mineral fuels) used for energy shares: India imports from UAE 45%;
EU 2023 HS27 imports from Saudi $33.8bn, UAE $9.6bn, Qatar $11.3bn, India $9.15bn.

**OECD / trade-facilitation cost literature (savings Method 2)**
OECD Trade Facilitation Indicators and ESCAP estimates that cross-border
paperless trade reduces trade costs by ~10–30% of transaction costs, with
documentary/procedural costs a low single-digit share of trade value. Used for
the independent second savings estimate (`savings_model.R`, Method 2).

**Digital Trade Integration (DTI) database**
Ferracane, M.F., Lee-Makiyama, H., & van der Marel, E. (lead authors), DTI
Project, European University Institute; and "Global Trends in Digital Trade
Policies and Practices: Evidence from the Digital Trade Integration Database,"
*World Trade Review* (2026), 25, 127–151, doi:10.1017/S1474745625100955.
Database (network-blocked on UAE side): https://dti.eui.eu/. Backs:
`dti_region_summary.csv`, `dti_corridor_NOTES.md`. Figures are 2023 policy counts
from the paper; UAE and Qatar are not in the paper's country sample.

## Cross-border legal layer

**CPTA — Framework Agreement on Cross-border Paperless Trade in Asia and the
Pacific**
UN ESCAP, https://www.unescap.org/projects/cpta and ESCAP Cross-Border Paperless
Trade Database https://www.digitalizetrade.org/. In force 20 Feb 2021. Parties
incl. Philippines (2019), Thailand (2025).

**UAE CEPA network** — UAE Ministry of Economy & Tourism,
https://www.moet.gov.ae/en/cepa. Per-agreement digital-chapter verification
(`uae_cepa_digital_verification.csv`):
- India — Digital Policy Alert; ELP Law analysis.
- Indonesia — ESCAP Cross-Border Paperless Trade Database (e-CoO exchange + AEO).
- Israel — PwC Middle East (Ch 9, Arts 9.6/9.7/9.8); pwc.com/m1.
- Vietnam — VCCI/WTO Center Vietnam; Vietnam Briefing (Ch 9 Digital Trade).
- Malaysia — ATB Legal; Dagang Net.
- Jordan — PwC Middle East (Ch 4 Art 4.5 paperless + AEO mutual admin assistance).
- Türkiye — ATB Legal.

**UAE–India Virtual Trade Corridor (operating)** — launched 10 Sept 2024 (ANI;
Times of Oman); operationalized via the MAITRI interface, welcomed in India–UAE
joint statements May 2026 (DD News, "India advances IMEEC trade corridor with
key UAE discussions"). Bilateral trade $101.25bn FY25-26, $200bn target by 2032.
Backs: the operating-channel claim and Step 1 of the working paper's roadmap. Accessed
July 2026.

**UAE–Mercosur CEPA (negotiating, advanced)** — ANBA, "UAE and Mercosur advance
trade agreement"; AGBI (Jan 2026); reaffirmed at the Mercosur Summit 30 June
2026. Accessed July 2026.

**UAE–EU CEPA (negotiating)** — European Commission, "EU and UAE agree to launch
free trade talks" (10 Apr 2025), https://ec.europa.eu/commission/presscorner/
detail/en/read_25_1043 and https://policy.trade.ec.europa.eu/ (EU–UAE agreement).
Talks launched 28 May 2025; first round June 2025; 4th round Dec 2025; digital
trade an explicit focus. Reported progress: Semafor (12 Dec 2025); AGBI.

**UAE cross-border data policy** — Clifford Chance, "Doing Business in the Middle
East: Data Transfers in the UAE and KSA" (2025); Addleshaw Goddard, "A new era
for cross-border data flows across QFC, DIFC and ADGM" (2026). DIFC Data
Protection Law No. 5/2020 and ADGM Data Protection Regulations 2021 are
GDPR-aligned with adequacy mechanisms; mandatory localisation only in narrow
sectors (health, banking). Backs the UAE-data-openness claim in METHODS 2.5.

## ASEAN benchmark (savings-model calibration)

**ASW reported savings** (see reconciliation note below) — USAID, via Vietnam Ministry of Industry & Trade and
Jakarta Globe ("ASEAN Companies Save $6.5b by Exchanging Trade Documents
Online," Feb 2024): ~$6.4–6.5bn cumulative 2018–2022, ~$2,300/transaction;
ASEAN.org ASW page (https://asean.org/.../asean-single-window/).

**ASW operational timeline** — ASEAN Single Window portal,
https://asw.asean.org/. e-Form D live among 5 states 1 Jan 2018; all 10 by 30
Dec 2019; ACDD from Dec 2020.

**Intra-ASEAN trade** — ASEANstats, "Exploring Intra-ASEAN Merchandise Trade
Dynamics" (Vol. VIII, May 2024), https://www.aseanstats.org/. Intra-ASEAN trade
$769.9bn (2023, −10.1% y/y); CAGR 7.4% (2003–2023). 2018–2019 values (~$620–630bn)
approximate, to firm.

**ESCAP trade-creation benchmark** — UN ESCAP: full regional digital trade
facilitation could cut export time up to 44%, cost up to 31%, and boost exports
by up to ~$257bn/year in Asia-Pacific; cross-border paperless trade reduces
trade costs 10–30% of transaction costs. (ESCAP digital trade facilitation
studies / AWP174.) Backs the 1.0–3.4% trade-creation band.

**Single-window cost-reduction range (20–50%)** — ESCAP/UNNExT and the project
proposal's cited literature; used only as the upper-scope reference, not the
operative parameter (the model is anchored to ASW's realized 0.19% rate).

**World Bank merchandise exports (Figure 6 map)**
World Bank, merchandise exports (current US$), indicator TX.VAL.MRCH.CD.WT,
api.worldbank.org, pulled July 2026: ASEAN-10 plus China, India, Bangladesh,
Australia, Sri Lanka, 2013–2023. Backs: `data/raw/merch_exports_asw_window.csv`
and the exploratory before/after-ASW growth map (`make_map.py`). Presented as
exploratory (current dollars; COVID inside the post window; totals, not
intra-bloc trade).

## Trade creation and spillover literature (added July 2026)

**WTO (2015). World Trade Report 2015: Speeding up trade — benefits and
challenges of implementing the WTO Trade Facilitation Agreement.**
https://www.wto.org/english/res_e/publications_e/wtr15_e.htm. Full TFA
implementation estimated to raise global merchandise exports by **$750bn–$1tn
per year** (gravity-model estimates higher), with developing economies
capturing over half the gains, LDC exports up 13–36%, plus diversification and
SME-participation effects. Backs: the trade-creation direction in the working paper §4,
the Medium post spillover section, and Brief B.

**Djankov, S., Freund, C., & Pham, C.S. (2010). Trading on Time.** Review of
Economics and Statistics 92(1), 166–173.
https://direct.mit.edu/rest/article/92/1/166/57797/Trading-on-Time. Each
additional day of pre-shipment delay reduces bilateral trade by **more than
1%** (≈ 70 km of added distance); worst for time-sensitive goods.

**Hummels, D.L., & Schaur, G. (2013). Time as a Trade Barrier.** American
Economic Review 103(7). NBER WP 17758:
https://www.nber.org/system/files/working_papers/w17758/w17758.pdf. Each day
in transit equivalent to a **0.6–2.1% ad valorem tariff**.

**Corridor spillovers.** "Wider economic benefits of transport corridors:
evidence from international development organizations" (ScienceDirect,
2022) — spatial spillovers from corridor investment to surrounding areas,
evidence from ~40 ADB/JICA/World Bank projects; CAREC corridor study
(Springer, 2025) — trade-facilitation improvements along corridors raise
trade flows. Backs: the spillover framing (mechanism-level, not
corridor-specific estimates).

## GCC

**Intra-GCC trade** — GCC Statistical Centre (GCC-Stat), https://gccstat.org/,
2023: intra-GCC merchandise ~$133bn. Also: Gulf customs union; December 2025 GCC Supreme Council approval
of a Customs Data Exchange Platform (gradual operation from H2 2026).


## ASEAN savings benchmark: reconciliation note (July 2026)
Published ASW savings figures diverge: ~$6.4bn cumulative 2018-2022 (US government material, OECD-cited, ultimately linked to Vietnam NTR figures) vs ASEAN's own ~$150m and 6m business days for 2022. Period, scope (e-Form D vs full ASW), and definition of savings likely differ; unresolved. The model's 0.19%/yr rate is the higher-end published reading; all corridor savings scale linearly with it (ASEAN's own figure implies roughly $0.2-0.3bn/yr corridor savings). All headline figures are therefore presented as scenarios.
