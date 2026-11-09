# 3531 Woodbridge Ave, Cleveland OH 44109 — **PRICED**

**ARV $233,721** · median $159.86/sf × **1,462 sf** · n=3 renovated, 0.25 mi, hood `02131`.
**MAO MODERATE $102,435** against **$25,973** tax arrears — a **$76,462** spread.

> **Read the band, and read §4 first.** `02131` has **no backtest**. The error is UNMEASURED.
> The three comps are all at the *top* of a bimodal hood distribution. This is the only priced
> lead in Cleveland outside `02125`, and it is the least supported number in the file.

Parcel `01508119` · owner-mail Ohio · `payment_plan_flag=1` · arrears $25,972.59.

## 1. How it got priced — the ID unlock

The previous pass left this unpriced because Redfin address-only URLs 404 and the home IDs were
unknown. Resolved by:

```
https://www.redfin.com/stingray/do/location-autocomplete?location=<address>&v=2
```

which returns `exactMatch.url` → the `/home/<id>` path that actually serves remarks. **This is now
the way to grade any Cleveland comp** and it unblocked the hood in a handful of calls.

## 2. The comp set — all three county-coded and remark-graded

| comp | sold | price | sqft (county) | $/sf | condition | evidence |
|---|---|---|---|---|---|---|
| 3341 Woodbridge Ave | 2026-05-15 | $165,000 | 1,327 | $124.34 | **renovated** | "renovated from top to bottom… new cabinets/appliances, roof, siding, windows, electrical, water tank, porch" |
| 3642 Marvin Ave | 2026-05-04 | $235,000 | 1,470 | $159.86 | **renovated** | "updated from top to bottom… renovated kitchen, quartzite, new windows, siding, flooring, new A/C and 2024 furnace" |
| 3407 Library Ave | 2026-05-11 | $320,000 | 1,726 | $185.40 | **renovated** | "extensively renovated… granite, tile, stainless, new deck, EV charger" |

Median **$159.86/sf**, spread **19.1%**.

**Excluded, each for a stated reason:**
- **4020 Poe Ave** ($240,000, $151.52/sf) — **no remarks at all**, "Source: Public Records". Condition
  unknown, so it cannot enter an ARV pool (D-48).
- **3713 Library Ave** ($198,000, $132.26/sf) — *"blends old-world character with modern updates"* →
  **maintained**, not renovated.
- **3107 Trowbridge Ave** ($166,000, $127.89/sf) — *"well maintained… pride of ownership"* →
  **maintained**.
- **3218 Marvin Ave** ($115,000, $72.88/sf) — maintained, and below both the band and the gate.
- **3618 Daisy Ave** ($76,000, $55.35/sf) and **3617 Trowbridge** ($60,000, $38.69/sf) — **dated**.

Note the sqft correction: Redfin lists 3642 Marvin at 1,775 sf; the county says **1,470**. Public
record wins, which raises its $/sf from $132 to $160 — the single biggest input to this ARV.

## 3. Arithmetic

```
ARV = 1,462 sf × $159.86/sf = $233,721
```

| grade | repairs | ceiling (0.70×ARV − repairs) | **MAO** (−$10K) | vs $25,973 arrears |
|---|---|---|---|---|
| LIGHT ($20/sf) | $29,240 | $134,365 | **$124,365** | +$98,392 |
| **MODERATE ($35/sf)** | **$51,170** | **$112,435** | **$102,435** | **+$76,462** |
| HEAVY ($50/sf) | $73,100 | $90,505 | **$80,505** | +$54,532 |

**Downside stress** (44102's ±40% used as a stress test only — not a band, see D-29):

| scenario | ARV | MAO @MODERATE | vs arrears |
|---|---|---|---|
| point | $233,721 | $102,435 | +$76,462 |
| −20% | $186,977 | $69,714 | +$43,741 |
| −30% | $163,605 | $53,353 | +$27,380 |
| **−40%** | $140,233 | $36,993 | **+$11,020** |

**The MAO stays above the arrears in every scenario down to −40%.** That is the first lead in this
market where the downside does not erase the deal.

## 4. Why you should still not trust the point figure

1. **n=3 is the floor, not a target.** Leave-one-out moves the median **19.1%** — the widest of any
   priced subject here. Drop 3341 Woodbridge and the ARV falls to ~$204,000; drop 3407 Library and
   it rises to ~$178,000-$235,000 range depending on the pair.
2. **The ARV sits at 1.97× the hood median $/sf** ($159.86 vs $81.25). This whole thesis is that
   *this house is at the renovated end*. If it grades MODERATE-with-deferred-capex instead, the
   comp set is wrong by construction.
3. **No backtest for `02131`.** Everything above is an uncalibrated point.
4. **Bed count unknown on the subject** — the county records 8 rooms, not bedrooms. The bed floor
   did not run.
5. **Condition of the subject is unknown.** Repairs are modelled at three tiers precisely because
   nobody has walked it. `3404 Woodbridge` and `3701 Marvin` are in the same hood and could not be
   priced at all.
6. **Two of the three comps sold in May 2026** — a 6-month-old set in a rising market. The window
   is 12 months by rule, and this is close to the thin end of it.

## 5. What this does to the ledger

| | before | after |
|---|---|---|
| priced leads | 6 (`02125` only) | **7** |
| priced hoods | 1 | **2** |
| best spread @MODERATE | $41,128 | **$76,462** |

**3531 Woodbridge is the strongest single lead found in Cleveland to date** — larger arrears-adjusted
headroom than any `02125` property, and the only one that survives a −40% ARV.

**Action: drive it.** The next step is not more arithmetic, it is condition on the subject and on
`3404 Woodbridge` and `3701 Marvin`, which are the same street cluster and may price off the same
three comps once their footage band resolves.
