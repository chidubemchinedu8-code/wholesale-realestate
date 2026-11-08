# Cleveland sweep — protocol derived from the Dayton failures

Written 2026-11-08 **before** the first Cleveland listing is read. Every rule below exists
because it was broken during the Dayton sweep and cost real numbers. Each cites the defect
that produced it. This file is the checklist a Cleveland ZIP must satisfy before it may be
called `scanned`.

---

## 0. The seven rules that would have prevented most of Dayton

| # | Rule | Born from |
|---|---|---|
| 1 | Recount the live total from the source on the day you report it. Never carry a stored denominator forward. | **D-36** — all seven Dayton ZIP denominators were 17–44% of live; "18% swept" was computed on counts missing two thirds of the market |
| 2 | `comp.py` exit **3** = genuine UNPRICED. Exit **1** = file/check failure and must abort the batch loudly. A harness may never map any non-zero exit to UNPRICED. | **D-39** — an invalid exclusion label made the whole comp file fail, and 46 leads were filed as honest refusals |
| 3 | ARV present + MAO absent = **parse bug**, never a refusal. MAO regex must accept `-?`. | **D-40** — 624 N Broadway St had ARV $177,360 and MAO −$948; the harness read a blank and filed it UNPRICED |
| 4 | A subject needs a **sourced** coordinate before any radius claim. No geocoder, no radius. | **D-37** — 34 leads shared one comp's coordinate and were priced off three Beechwood comps |
| 5 | `radius = None` must print as *no radius applied*. Never print `0.00 mi` for a measurement not taken. | **D-42** — a ZIP-wide run boasted a 1.5 mi radius check it never executed |
| 6 | Close every file before spawning a subprocess; reconcile at least one lead by hand per batch. | **D-38** — an unclosed CSV truncated, and 12% of leads returned UNPRICED with all checks PASS |
| 7 | "Bimodal" needs ≥3 sales on **both** sides of the gap. | **D-41** — one 4,798 sf junk parcel was declared a second market |

## The same class of error in the sheet layer

| # | Rule | Born from |
|---|---|---|
| 8 | `updated_rows: N` is not a receipt. Recount from the sheet. | **D-43** — a 48-row write silently dropped 20 |
| 9 | A row is cleared across **all 18 columns**, not column A only. | **D-44** |
| 10 | Never batch `delete_dimension` from a precomputed index list. One row per call, re-read the ID first. A falling `row_count` proves *a* row went, never *which*. | **D-45** — four live pipeline rows destroyed |

---

## 1. Discovery (before any number exists)

- **Zillow is primary.** Redfin and Realtor.com are cross-checks and must also be read.
  A figure is not "confirmed" because Redfin repeated Zillow — one portal echoing another
  is not a second source. (`references/on-market.md`)
- **Scan by ZIP**, all types, unfiltered. No asking-price cap, no bedroom floor. Those are
  NOT in this repo and inventing them is what made the Dayton coverage numbers meaningless
  (**D-34**, `AUDIT.md` A-7). The buy box caps the **ARV** ($125K–$900K) and the 70%
  ceiling — never the asking price.
- **Read the photos before scoring.** Photos classify condition; listing copy does not.
  If photos cannot be rendered, the lead is `CONDITION UNVERIFIED` — do not quietly
  substitute a Redfin gallery.
- **Record every listing including rejects**, with a reject reason. Count rejects by reason.
- **Coverage is `examined / live_total`.** A ZIP is `scanned` only when they are equal.
  Otherwise it is `partial` and says so.

## 2. Neighbourhood gate (protects the ARV)

- A ZIP is not a hood. Cleveland ZIPs split hard — 44102 alone spans Ohio City, Detroit
  Shoreway, Stockyards, Clark-Fulton, Cudell, Edgewater and more, with medians that are
  not the same product.
- Hood must come from a **named source**: Zillow `## Neighborhood:` block, then
  `Subdivision:` in Facts & features, then OSM `hamlet` (weak, geocodes to street), then
  listing copy (hint only, never proof).
- `UNKNOWN` and `CONFLICT` are terminal for pricing. Record the blank and the reason.
- **Never pool two hoods silently.** If pooling to reach n=3 is the only way to a number,
  say so out loud, justify adjacency and buyer pool, and show what the number would be
  without the pool. (**D-31**; worked example: 9453 McKinney St.)

## 3. Comps

- ARV needs **≥3** comps (`comping/COMPING.md` §0). **Five** is the separate *submission*
  standard (`SKILL.md` rule 2, `comps.py`). Do not confuse them.
- Renovated condition only in the ARV pool. A dated sale sets an as-is floor, never an ARV.
- ±30% sqft band, subject bed count as a floor, ±45% consistency gate that never
  reinstates an outlier.
- Every comp needs **sourced** coordinates. Coordinates estimated by eye void the number.
- A "similar homes" carousel is a **lead** source, never a comp source.
- Hood **sold** feeds are not hood-coherent — mine row-by-row through each comp's own
  breadcrumb, never import a feed as a pool.

## 4. Arithmetic

```
ARV      = subject_sqft x MEDIAN $/sf of the comp set      (one method, no haircut)
CEILING  = ARV x 0.70 - repairs                            (buyer max)
SELLER MAO = CEILING - $10,000                             (the fee, subtracted once)
OFFER LOW  = 0.55 x ARV - repairs
OFFER HIGH = 0.60 x ARV - repairs
```
- Repair tiers **$20 / $35 / $50 per sf** (LIGHT / MODERATE / HEAVY). A repair number with
  no grade is a defect.
- **Never deduct the fee twice.** Never lower the fee to make a deal work — lower the offer.
- A **negative MAO** is a hard walk and is reported as a number, not as a blank.
- **No error band outside a measured market.** The ±40% was measured on Cuyahoga 44102 —
  so Cleveland 44102 is the one place a band may be printed, and even then only if the
  backtest file supports the claim. Everywhere else: `ARV BAND NONE`. (**D-29**)

## 5. Cleveland-specific reality

- Cuyahoga County GIS is live (521,078 parcels, 142 fields) — unlike Wayne County (D-33),
  a real backtest is possible here. `state/backtest/cuyahoga_44102_walkforward.py` exists
  and produces `walkforward_result.json`. **Run it before quoting a Cleveland band.**
- Wayne County lesson does not apply: do not import a Detroit conclusion into Cuyahoga.
- 44102 and 44128 are flagged "strong ZIP" in the ranking weights; 44110 likewise.
  Priority is a *research order*, not a valuation.

## 6. Reporting

Every ZIP report states, in this order:

1. `examined / live_total` and the date the live total was counted
2. rejections counted **by reason**
3. `UNPRICED` rows listed with the failing gate named — a refusal is a deliverable
4. `NEGATIVE MAO` rows listed separately
5. leads by verdict (PRIORITY / MARGINAL / ABOVE-MAO / NO / UNPRICED)
6. what was NOT read (detail pages, photos, cross-checks) and why

**Never claim more listings reviewed than were actually read.**
