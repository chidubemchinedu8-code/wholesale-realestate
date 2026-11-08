# 45417 — full unfiltered sweep, 2026-11-08

111 of 111 active listings examined against live Redfin. No price cap, no bed
filter: both were agent-invented (`AUDIT.md:347` — the buy box sets no asking
cap). Every listing is recorded, including every reject and why.

## Coverage

| | count |
|---|---|
| Redfin active total | 111 |
| recorded in roster | 111 |
| houses | 84 (83 SFR + 5 new build, 3 duplex) |
| land | 19 |

Roster: `state/sweeps/roster/45417.csv`.

## The denominator was wrong

`state/sweeps/dayton_coverage.csv` said 49 active listings. Redfin says 111.
It was not one bad row — all seven ZIPs were understated:

| ZIP | recorded | LIVE 2026-11-08 | examined | true coverage |
|---|---|---|---|---|
| 45402 | 24 | 73 | 6 | 8% |
| 45403 | 13 | 69 | 4 | 6% |
| 45404 | 8 | 48 | 2 | 4% |
| 45405 | 39 | 114 | 9 | 8% |
| 45406 | 16 | 86 | 5 | 6% |
| 45410 | 24 | 78 | 2 | 3% |
| 45417 | 49 | 111 | 111 | **100%** |
| **total** | **173** | **579** | 139 | **24%** |

The previous 18% "Dayton coverage" was itself computed against wrong
denominators. City-wide truth today is 24%.

## Rejects — 86 of 111

| reason | n |
|---|---|
| land, no structure to ARV | 19 |
| above market ARV band (no spread) | 11 |
| turnkey / retail-ready (no spread to capture) | 8 |
| new construction (different product) | 5 |
| nominal $1 ask, not arm's-length | 3 |
| duplex (needs 2–4 unit comps, engine is SFR) | 3 |
| 1-bed (ARV floor unreachable) | 2 |
| tenant-occupied, lease through Nov 2026 | 1 |

Three listings carried a **$1** ask (273 Brooklyn, 608 N Kilmer, 657 Randolph).
Recorded, not treated as asks — they are land-bank / auction placeholders.

## Comp pool — the honest state of 45417

92 sold homes in the last 3 months. **Only 6 are renovated.**

| comp | sold | price | sf | $/sf |
|---|---|---|---|---|
| 117 Riegel St | 2026-10-13 | $115,000 | 1,462 | 78.66 |
| 4614 Oakridge Dr | 2026-10-09 | $123,000 | 1,322 | 93.04 |
| 1305 S Edwin C Moses | 2026-08-14 | $176,000 | 1,584 | 111.11 |
| 3920 Cain Ct | 2026-09-11 | $107,000 | 912 | 117.32 |
| 501 Conley St | 2026-08-19 | $172,000 | 1,415 | 121.55 |
| 512 Campbell St | 2026-10-07 | $149,000 | 1,132 | 131.63 |

**Renovated median $111.11/sf. ZIP-wide median (all 54 usable sales) $79.06/sf.**
That 41% gap is the condition split: 45417 splits by condition, not geography.
The engine's ±30% sqft band is what keeps a 2-bed from borrowing a 1,415 sf comp.

`anchor.py`: single distribution, no bimodality — so the ZIP median is a valid
sanity band.

## Results — 26 sub-market houses run through `comp.py`

| address | ask | tier | repairs | ARV | MAO | verdict |
|---|---|---|---|---|---|---|
| 2520 Germantown St | $17,500 | heavy | $58,150 | $136,448 | $27,364 | PRIORITY |
| 361 Adelite Ave | $19,900 | heavy | $57,400 | $134,689 | $26,882 | PRIORITY |
| 58 Anna St | $29,900 | heavy | $67,200 | $149,333 | $27,333 | NO (above MAO) |
| 252 Brooklyn Ave | $65,000 | heavy | $51,400 | $120,610 | $23,027 | NO |
| 625 Fleetfoot Ave | $78,000 | heavy | $65,250 | $145,000 | $26,250 | NO |
| 321 Alicia Rd | $78,500 | heavy | $56,500 | $132,577 | $26,304 | NO |
| 330 Bolander Ave | $79,000 | moderate | $56,980 | $166,180 | $49,346 | NO |
| 162 Lorenz Ave | $80,000 | moderate | $47,040 | $149,333 | $47,493 | NO |

17 UNPRICED — all 2-bed. The ZIP has **zero renovated 2-bed sales** in the
180-day window, so `comp.py` refuses: `only 1 renovated comp within 1.5 mi
(needs 3)`. Correct refusal, not a gap to paper over.

**The 33 remaining houses: every single one fails.** All priced, none clears.
Full table: `state/comps/dayton_45417_sweep_results.csv`.

## 361 Adelite — the block problem, stated plainly

The two PRIORITY hits depend entirely on which block they are in, and I do not
know that. The 6 renovated comps span **$79–$132/sf**, and neither Adelite nor
Germantown St is any of those streets.

| basis | ARV | 70% ceiling | MAO | spread vs $77,300 basis |
|---|---|---|---|---|
| low comp $78.66/sf | $90,302 | $63,211 | $5,811 | **−$14,089** |
| 4614 Oakridge $93.04/sf | $106,810 | $74,767 | $17,367 | **−$2,533** |
| median $114.22/sf | $131,119 | $91,783 | $34,383 | +$14,483 |
| 501 Conley $121.55/sf | $139,539 | $97,678 | $40,278 | +$20,378 |
| high $131.63/sf | $151,111 | $105,778 | $48,378 | +$28,478 |

**At the two lowest renovated comps the deal loses money.** The neighbour
signal is worse: **365 Adelite sold $26,000 on 2026-09-14** — $21/sf, not
$117/sf. That is a distressed sale and correctly excluded from ARV, but it is
what traded on that block one month ago. 361 Adelite at $19,900 is priced
close to its own block's last sale, not close to a renovated comp.

Verdict: **PRIORITY on arithmetic, UNPROVEN on condition.** Not actionable
without a walkthrough and a parcel-level condition read.

## What is NOT done

- **County validation failed.** `mcrealestate.org` returns "The System is
  currently unavailable due to maintenance" on every endpoint, including the
  address-search postback; `gis.mcohio.org` 404s. The user asked for ARVs
  checked against appraised values and that did not happen. **No ARV here is
  county-confirmed.**
- No 45417 backtest exists, so `comp.py` reports `ARV BAND NONE — error
  UNMEASURED`. The Cuyahoga ±40% band is not transferable (D-29).
- The 6 other ZIPs have live totals but are **not swept**. 24% city-wide.
