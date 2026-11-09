> ## ⚠️ SUPERSEDED IN PART — 3531 Woodbridge Ave is now PRICED
>
> The home-ID unlock (`stingray/do/location-autocomplete`) resolved condition on the comps after
> this file was written. Three sales grade **renovated** (3341 Woodbridge, 3407 Library, 3642 Marvin)
> and **3531 Woodbridge now prices: ARV $233,721, MAO $102,435 vs $25,973 arrears.**
> See `CLEVELAND_44109_3531_WOODBRIDGE.md`.
>
> **3701 Marvin and 3404 Woodbridge remain unpriced** — but not because of condition. At 1,260 and
> 1,263 sf the ±30% band leaves only **2** of the three renovated comps, so the floor fails on
> **size**, not condition. Everything below about bimodality still holds for mixed-condition use of
> the hood median and is retained as the audit trail.

# `02131` — worked, and correctly UNPRICED

**Result: no ARV for 3701 Marvin, 3531 Woodbridge or 3404 Woodbridge.** Not for want of leads or
sales — `02131` has 18 recent single-family transfers in the subject band. It is unpriced because
**the hood has no single $/sf**, and I could not establish condition on a single comp.

## 1. What I did

1. Queried the county for every `02131` parcel, 1,200–1,700 sf, transferred after 2025-11-08 —
   **18 sales** (a comp set can be built from the county directly; Redfin's ZIP feed had not
   surfaced these because they sit on page 2–3).
2. Attempted remark-based condition grading for each: **Redfin address-only URLs 404** and the
   `02131` sales are not in the page-1 feed chunks I could read. One sold page was reachable
   (2070 W 100th — wrong hood). **So condition is unestablished for all 18.**
3. Tested the distribution before pricing.

## 2. Why it is unpriced — the distribution has no centre

All 18 in-band sales, `$/sf` sorted:

| $/sf | address | | $/sf | address |
|---|---|---|---|---|
| 188.7 | 3407 Library Ave | | 83.7 | 3227 Trowbridge Ave |
| 159.9 | 3642 Marvin Ave | | 78.8 | 2914 Woodbridge Ave |
| 151.5 | 4020 Poe Ave | | 76.8 | 3719 Poe Ave |
| 138.6 | 3205 Trowbridge Ave | | 73.0 | 3517 W 32nd St |
| 132.3 | 3713 Library Ave | | 72.9 | 3218 Marvin Ave |
| 127.9 | 3107 Trowbridge Ave | | 63.2 | 3757 Trowbridge Ave |
| 124.3 | 3341 Woodbridge Ave | | 55.4 | 3618 Daisy Ave |
| 106.9 | 3712 Daisy Ave | | 49.0 | 3618 Marvin Ave |
| | | | 45.9 | 3942 Poe Ave |
| | | | 38.7 | 3617 Trowbridge Ave |

**An empty gap between $106.90 and $83.70 — $23/sf of nothing.** Two clusters: **$135.45 (n=8)** and
**$68.05 (n=10)**. The hood median, **$81.25**, falls **inside the empty space**. It summarises no
sale in the neighbourhood.

On the three leads that swings the answer **2×**:

| lead | sf | arrears | @ upper $135.45 | @ lower $68.05 |
|---|---|---|---|---|
| **3701 Marvin Ave** | 1,260 | **$37,811** | $170,667 | $85,743 |
| **3531 Woodbridge Ave** | 1,462 | $25,973 | $198,028 | $99,489 |
| **3404 Woodbridge Ave** | 1,263 | $1,731 | $171,073 | $85,947 |

**And the gap is not noise — it is exactly the renovation premium.** `02131` is Clark-Fulton /
Stockyards, a hood mid-transition: $68/sf buys the street as it was, $135/sf buys it renovated. Which
one a subject supports is a **condition** question, and condition is precisely what I could not
establish.

## 3. What this says about `02125`, where I did quote a number

Same two tests, both hoods (D-52):

| set | n | median | largest gap | leave-1-out swing |
|---|---|---|---|---|
| `02125` renovated (ARV pool) | 5 | **$102.70** | 18.0% | **10.5%** |
| `02131` all conditions | 18 | $81.25 | **28.3%** | 6.0% |

**`02131` is the more *stable* median and the less *valid* one.** With 10 low and 8 high sales, no
single removal can move the median out of the gap. Robustness is not validity — a lesson I nearly
missed by using the jackknife as the test.

`02125`'s 18.0% gap is above my own 15% line, so its **$102.70 carries a stated ±10.5% one-comp
sensitivity**. The six priced leads in `CLEVELAND_02125_SIZED_TO_COMPS.md` should be read with that
band, not as clean points.

## 4. The one thing that would price all three leads

**Condition on the comps.** Not more leads, not a wider radius, not a backtest. Every one of the 18
sales needs a `renovated / maintained / dated` grade from its listing remarks, which requires a
Redfin home-ID URL per property. With that:
- the upper cluster (n=8) becomes a legitimate renovated comp set and all three leads price off it;
- 3701 Marvin at **$37,811 arrears against a ~$170,000 ARV** is, on that basis alone, the strongest
  single lead found in this market.

**Until then these three carry no number.** A bare county $/sf here would put a 2× error into the
MAO, and the MAO is what the offer is built on.

## 5. Status

The three `02131` leads stay `UNPRICED-no-comp-set` in
`CLEVELAND_LEAD_INVENTORY_2026-11-08.csv`, with the reason recorded as **bimodal hood, no verified
condition** rather than "no comps" — because there are 18.
