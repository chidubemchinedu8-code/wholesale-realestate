# Dayton 45404 — Full Sweep

**Date:** 2026-11-08 · **Coverage: 48 of 48 live listings examined (100%)** · **Filter: none**

- Roster: `state/sweeps/roster/45404.csv` (48 rows)
- Sold master: `state/comps/dayton_45404_sold_master.csv` (69 rows, 6-month window)
- Pricing: `state/sweeps/dayton_45404_sweep_results.csv` (25 leads)

---

## Headline: 45404 clears nothing, and over half of it cannot be priced at all

**Zero PRIORITY. Zero MARGINAL.** Of 25 underwritten leads: 12 NO, **13 UNPRICED**.

This ZIP holds the worst pricing coverage of the seven — **52% of leads refused**, against
29% for 45406, 28% for 45403 and 39% for 45402. That is not a thin-market excuse; it is a
specific structural fact about 45404, set out below.

---

## The 4-bedroom gap — this ZIP's defining defect

**In six months, exactly ONE 4-bedroom single-family sale closed in 45404** — 636 Hillrose
Ave at $224,900, and its condition is unknown so it cannot enter a renovated comp set.

Every other 4-bed SFR sold in this ZIP is multifamily. The full count of SFR sales by bed:

| Beds | SFR sales | Renovated |
|---|---|---|
| 1 | 4 | 1 |
| 2 | 24 | 3 |
| 3 | 32 | 5 |
| **4** | **1** | **0** |
| 5+ | 0 (all multifamily) | 0 |

So **seven of the 25 leads are 4-bedroom and cannot be priced at any confidence** — 930
Webster, 1309 Leonhard, 611 Maryland, 2411 Troy, 2224 Brandt Pike, 221 Alton, 1605 Mack.
The engine refuses them with *"every same-neighbourhood sale has fewer than 4 beds — the
bed floor cannot be met"*, and that refusal is correct.

This matters because **45404's live inventory is skewed to 4-bed**. Seven of the 25 leads
are 4-bed; the ZIP sells 4-bed at our own 4%. A wholesaler working this ZIP will keep
hitting leads that no comp set can support.

---

## Renovated band — 2.07× spread, again a size effect

| Address | Sold | Price | Sqft | $/sf |
|---|---|---|---|---|
| 310 Brandt St | 2026-06-08 | $147,000 | 1,389 | $105.83 |
| 1304 Valley St | 2026-05-29 | $135,900 | 1,051 | $129.31 |
| 203 Alaska St | 2026-08-10 | $218,000 | 1,685 | $129.38 |
| 257 Alaska St | 2026-07-10 | $185,000 | 1,296 | $142.75 |
| 634 Mentor Ave | 2026-09-01 | $295,000 | 1,870 | $157.75 |
| 405 Elverne Ave | 2026-09-01 | $180,000 | 1,028 | $175.10 |
| 241 Hypathia Ave | 2026-09-14 | $180,900 | 978 | $184.97 |
| 640 Prince Albert Blvd | 2026-09-08 | $119,000 | 561 | $212.12 |
| 736 Sagamore Ave | 2026-09-01 | $125,900 | 576 | $218.58 |

**median $157.75/sf · range $105.83–$218.58 · spread 2.07× · Pearson r(sqft, $/sf) = −0.724**

Same inverse size gradient as 45403 (r = −0.863), slightly weaker. Sub-1,000 sf renovations
sell around $185–219/sf; anything over 1,600 sf sits near $130–158/sf. **The pooled median
is never used as an ARV basis.** The engine's ±30% sqft gate applied it correctly — e.g.
532 Deeds Ave (850 sf) priced off a size-matched median of $175.10, not the $157.75 pooled
figure.

`anchor.py` returns **single distribution** (n=49, median $106.10/sf), so the ZIP median is
a valid sanity check only.

---

## Results — 25 leads

| Address | Ask | Repairs | ARV | MAO | Verdict |
|---|---|---|---|---|---|
| 532 Deeds Ave | $85,000 | $29,750 | $148,833 | $64,433 | NO |
| 1012 Saint Adelbert Ave | $105,000 | $47,040 | $182,867 | $70,967 | NO |
| 1225 Lamar St | $109,900 | $36,540 | $165,915 | $69,600 | NO |
| 544 Troy St | $114,900 | $65,660 | $242,711 | $94,238 | NO |
| 434 Grove Ave | $119,000 | $29,540 | $147,782 | $63,907 | NO |
| 417 Brandt St | $145,000 | $31,010 | $155,136 | $67,585 | NO |
| 4290 Old Troy Pike | $175,000 | $43,190 | $176,150 | $70,115 | NO |
| 6 Brighton St | $180,000 | $60,025 | $233,346 | $93,317 | NO |
| 609 Troy St | $184,900 | $60,550 | $235,387 | $94,221 | NO |
| 4405 Old Troy Pike | $185,000 | $66,640 | $246,334 | $95,794 | NO |
| 551 Maryland Ave | $205,000 | $43,050 | $175,579 | $69,855 | NO |
| 260 Alton Ave | $209,000 | $57,680 | $224,230 | $89,281 | NO |
| *13 more* | | | — | — | UNPRICED |

**Tally: 0 PRIORITY · 0 MARGINAL · 12 NO · 13 UNPRICED.**

**544 Troy St is the closest lead in the ZIP** — $114,900 ask against a $94,238 MAO. It
needs a 17% cut. Its ARV of $242,711 comes off a size-matched median of $129.38/sf, the
lower part of the band, so the miss is not a pessimistic comp choice.

### The 13 UNPRICED, by gate

**Bed floor (7)** — no renovated 4-bed comp exists: 930 Webster, 1309 Leonhard,
611 Maryland, 2411 Troy, 2224 Brandt Pike, 221 Alton, 1605 Mack.

**Comp count / size (6)** — fewer than 3 clean comps in the ±30% sqft window:
1312 Valley (674 sf), 1428 Valley (648 sf), 1539 Chapel (674 sf), 233 Notre Dame
(1,056 sf), 2431 Guernsey Dell (988 sf), 629 Little Meadow (2,589 sf).

The two ~650 sf leads (1312 and 1428 Valley) are below anything renovated that has sold
size-matched — the smallest renovated sales are 561 and 576 sf, which are a different
product (very small bungalows at $212–219/sf).

---

## Sensitivity

| Basis | Clears (of 12 priced) |
|---|---|
| Band low $105.83/sf | **0** |
| Band p25 $129.34 | **0** |
| Band median $157.75 | 1 |
| Band p75 $198.55 | 3 |
| Band maximum $218.58 | 7 |

45404 is the **most expensive ZIP of the seven on an entry basis** relative to its own
renovated band: the asks are high ($85,000–$289,900) while the band median is $157.75/sf.
Only at the band maximum do 7 of 12 work. As with 45402 and 45403, that is an upside case,
not a deal.

---

## Roster notes

- **11 of the 48 listings are new-construction plans, not properties.** Six are literally
  named floorplan products with no address: "Spruce with Full Basement Plan", "Hazel with
  Full Basement Plan", "Elder with Full Basement Plan", "Cedar with Full Basement Plan",
  "Birch with Full Basement Plan", "Tupelo with Full Basement Plan". Two more are
  subdivision builds priced from a builder sheet (4238 Weeping Willow, 4500/4501 Cardinal
  Flower). All rejected `new_construction`. These inflated the live count materially.
- **1047 Gerhard St** is listed under 45404 but its own FSBO copy says "Dayton, OH 45410".
- **221 Alton Ave** has no square footage in the listing; 1,600 sf was assumed for the
  repair estimate and the result is UNPRICED regardless.
- **930 Webster St** appears twice in the sold data — once as a sold duplex ($44,000,
  June) and once as an active lead ($70,000, mid-renovation). The sold record was used to
  confirm the property's scale, not to price the lead.

## Sold rows excluded

Land: 607 Waneta Ave (0.41 acre). New build: 4341 Purple Aster Ct ($335,000, Cedar model).
Multifamily (7): 3583 Golden Meadows, 440 Maryland, 69 Notre Dame, 1517 Chapel,
700-702 Webster, 930 Webster #932, plus 819 Waldrun and 700-702 Webster dropped for having
no square footage. Executive tier excluded via `different_tier`: 525 Recess Dr ($415,000),
505 Reading Rd ($390,000) — these are 2020s subdivision homes in a different market.

## Gates that failed — named

1. **D-37 (open):** `state/comps/_geo_45404.csv` does **not exist**. All subjects were
   given the same lat/lon; every "within 1.5 mi" line is void. Comp sets are size- and
   condition-matched only.
2. **Neighbourhood gating unverified.** Not obtained via Zillow `## Neighborhood:` or OSM
   for these 25 leads.
3. **ARV band: UNMEASURED.** No backtest for 45404. Figures are ESTIMATES.
4. **4-bedroom ARV structurally unsupported** — one 4-bed SFR sale in six months, condition
   unknown.

## Not done

- **45410 (78) is the last ZIP.**
- No geocode for 45404; D-37 stays open.
- No per-property assessor cross-check this sweep.

---

## Coverage after this sweep

| ZIP | examined | live |
|---|---|---|
| 45402 | **73** | **73** |
| 45403 | **69** | **69** |
| 45404 | **48** | **48** |
| 45405 | **114** | **114** |
| 45406 | **86** | **86** |
| 45410 | 2 | 78 |
| 45417 | **111** | **111** |
| **TOTAL** | **503** | **579 (86.9%)** |

**Six of seven ZIPs complete. 45410 (78 listings) is the last one.**
