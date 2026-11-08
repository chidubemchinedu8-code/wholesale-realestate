# Backtest — does the ARV method actually work?

**Date:** 2026-11-08 · **Market:** Cuyahoga County, Cleveland OH **44102** · **n=43 sales**
**Method under test:** `ARV = sqft × median($/sf of ≥3 renovated sales, same hood, ≤1.5 mi, ≤12 mo, ±30% sqft)`

## Verdict up front

**The method is unbiased but imprecise: median absolute error ≈ 40%, and a "TIGHT" comp set
does not predict accuracy.** Every ARV this engine produces should be read as a band, not a
point. The Cleveland `$172,328` is now published with a band of **$103,396 – $241,259**.

That is not a reason to stop using it. It is a reason to stop presenting a single number as
if it were an appraisal.

## Ground truth, and why it isn't the appraisal

The obvious test — "compare our ARV to the county's appraised value" — answers the wrong
question. Two independent facts kill it:

1. **The county's appraisal is stale by design.** Texas is annual; Ohio is a triennial update
   with a six-year full reappraisal. Values certified in 2024 are being compared to 2026 sales.
2. **It is measured, not guessed.** On these same 41 market sales the county's own figure has a
   **median absolute error of 30.0%** against the actual sale price (median appraisal ÷ sale
   price = 0.91). A stale tax figure is not a benchmark.

So the backtest uses **the recorded sale price** — the only unimpeachable number — and asks
whether our method, standing at the time of an *earlier* set of sales, would have predicted
*this* sale.

**Data source (this is the useful find):** Cuyahoga publishes the whole CAMA book as a queryable
ArcGIS layer, `gis.cuyahogacounty.gov/.../Open_Data_Parcels/MapServer/0`, carrying
`sales_amount`, `transfer_date`, `certified_tax_total`, `total_res_liv_area` and land-use code
per parcel. Filtered to `tax_luc_description = '1-FAMILY PLATTED LOT'` it gives every
single-family sale in the county, backtestable in bulk. This converts market research from
"open one Zillow page at a time" into a query.

## The test

Walk-forward, 43 sales in a 0.9-mile box around the subject, 2025-01 to 2026-02. Each sale is
priced using **only sales that closed before it**, inside 12 months, within ±30% living area,
minimum 3 comps, median $/sf — the engine's rules, applied honestly with no lookahead.

| test | median abs error | mean | within ±20% | median bias |
|---|---|---|---|---|
| **A. $/sf screen at ≤$250** | **39.5%** | 41.4% | 21% | −1.1% |
| B. no screen (raw county data) | 40.6% | 47.0% | 21% | −6.6% |
| C. screen + ±20% sqft band | 44.3% | 46.3% | 16% | −4.1% |
| D. screen + ±40% sqft band | 42.0% | 42.1% | 20% | −5.5% |

Tightening the square-footage band made it **worse** (C), which is the first hint that the error
is not in the comp *matching*.

Note the median signed bias is **−1.1%**. The method is well-centred. It is just wide.

## Two hidden landmines the backtest exposed

**A $2.2M "single-family sale" in 44102.** The first pass included it and it wrecked the
statistics. The county's `sales_amount` field carries **portfolio and bulk transfers** — one
buyer, many parcels, one consideration. Zillow shows these as ordinary sales, and a manual
comp set would never catch one because it only looks at the handful of houses it likes.
`$/sf ≤ $250` removes them (46 → 43 sales), but the field has no transaction-type flag, so
this screen is a proxy, not a filter.

**A same-parcel re-sale pair.** The subject's own comp, 3235 W 94th, appears **twice**: $60,000
in Jan 2026 and $146,000 in Jul 2026. A naive backtest counts both as market evidence. Any
backtest has to de-duplicate by parcel and use the last transfer.

## Why the error is 40%: dispersion, not bias

This was the surprise. I expected the error to live in **condition** — blended renovated and dated
sales, so the median lands in dead centre. The decomposition says no:

| subject type | n | median abs error | median signed bias |
|---|---|---|---|
| sold **above** median $/sf (retail proxy) | 20 | 37.4% | **−37.4%** |
| sold **below** median $/sf (dated proxy) | 19 | 46.3% | **+46.3%** |

The two groups are mirror images. Errors are big, but they cancel: **median bias −1.1%**. A
condition-matched comp set would fix the *bias* that is already near zero. It cannot fix the
spread, because the spread is real.

**The spread is real, and it is close to home.** On single streets inside this one ZIP, in
2025–2026, all single-family, all roughly the same size:

- **W 94th St** — six sales, **$47 to $78/sf** → 1.7× range
- **W 90th St** — four sales, **$44 to $91/sf** → 2.1× range
- **W 86th St** — four sales, **$45 to $121/sf** → 2.7× range

Two houses on the same block, same size, same side of the street, sold 2.7× apart per square
foot. Nothing in a comp database sees the difference — a flipped kitchen, a dead furnace, a
motivated estate, a tenant in place, a roof at end of life.

**Tightening geography does not fix it.** Same-street-only comps: 34.0% median error but only
6 of 43 sales priceable — no better, and it mostly just stops answering.

## The engine's confidence badge was lying

`comp.py` badged a comp set `TIGHT` when its p25–p75 $/sf spread was ≤25%, which reads as
"accurate". Tested against outcomes:

- **0 of 39** backtested comp sets were even badgeable TIGHT in this market.
- Correlation between comp-set spread and actual |error|: **not positive in the useful
  direction** — a narrow set did not produce a smaller miss.
- Banding the 46 sales by price shows the mechanism: **$29 – $223/sf, q1 $49, median $69,
  q3 $116 — a 2.4× interquartile range inside one ZIP and one property class.**

A 3-comp set drawn from that population has a wide median no matter how carefully the three are
chosen.

**Changed in `scripts/comp.py` (2026-11-08):**
- the `TIGHT` badge is gone; it now reads `MEASURED (uncalibrated)` or `UNUSABLE - comp set too
  dispersed` above 45%
- `ARV_MEDIAN_ABS_ERROR = 0.40` and `BACKTEST_BASIS` are declared as data, with the measurement
  in a comment
- every priced run now prints an **ARV BAND** and states what fraction of backtested sales
  landed inside ±20%
- a run with `n < 5` warns that n=3 is a floor, not a target
- 5 new tests lock this in (189 → 194)

## What this means for the Cleveland lead

`3216 W 95th St` — ARV **$172,328**, band **$103,396 – $241,259**.

The deal conclusion survives, and this is worth being precise about: the lower bound of the ARV
band is **$103,396** against a **$99,900** ask. Under *every* outcome the backtest observed, a
renovated 1,440 sf house here is worth at least roughly the asking price — but that is only
true of a **finished** house, and this one is not finished. The repairs come out of that band.

So the practical reading, unchanged but now quantified:

- the **case to buy is real** — the ARV floor sits at the ask
- the **case to buy at the ask is not** — at MODERATE ($50,400 repairs) the ceiling is $70,230
  and the MAO is **$9,530**
- and the ±40% error is exactly why the repair grade has to be **scoped on a walkthrough**,
  not guessed from a listing that says "diamond in the rough" and names no systems

One number, honestly labelled, per the standing rule: **an ARV of $172,328 ± 40% is not a
valuation, it is a range with a point estimate in the middle.** The buy box survives on the
bottom of the range, and that is the only part of it I would defend.

## Does the method make money? (the question that actually matters)

Pricing accuracy is not the same as profitability, so the same 39 priced sales were run
through the buy box as actual decisions. With
`offer = 0.70×ARV_est − repairs − $10k`, realised
`profit = ARV_true − offer − repairs − $10k`, which simplifies to
**`profit = ARV_true − 0.70×ARV_est`** — repairs and the fee cancel by construction.

| | result |
|---|---|
| deals taken | 39 |
| profitable | **28 (72%)** |
| lost money | 11 (28%) |
| median return on value | **+30.8%** |
| worst deal | **−82%** |
| break-even error | **+42.9%** |

**72% win rate, and that is entirely a consequence of the symmetric error.** A well-centred
estimator plus a 30% margin gives a positive-expectancy screen. The margin is doing the work;
the accuracy is not. Note the asymmetry the method can live with: an ARV that is 40% *too low*
costs a missed deal, an ARV 40% *too high* on a 70% offer still breaks even at 42.9%. The 70%
rule is a shock absorber for exactly the dispersion measured above.

**One real safeguard found by sensitivity:** buying at 70% → 72% profitable; at **60% → 92%**;
at 55% → 97%. The offer ladder's `0.55–0.60` target band is therefore not arbitrary — it is the
part of the range that survives the error. `BUYER_PCT = 0.70` should stay a **hard ceiling** and
never become the normal entry point.

### The assumption that breaks it

The simplification `profit = ARV_true − 0.70×ARV_est` holds **only if the repairs budgeted equal
the repairs actually needed.** That hides the bigger risk:

| repair overrun | profitable | median return |
|---|---|---|
| 0% | 72% | +30.8% |
| 25% | 62% | +18.8% |
| 50% | **54%** | +5.9% |
| 100% | **41%** | −19.8% |

**ARV error is symmetric; repair error is a one-way ratchet.** You cannot come in 30% *under* a
gutted kitchen — the floor is zero and the ceiling is open. On a 1,440 sf subject at $35/sf the
budget is $50,400, and a 50% overrun is $25,200 of loss against a MAO of $9,530.

So: the ARV is fit for purpose as a **screening** number. It is not fit to be the last number
before a contract. The repair grade on a walkthrough is the decision, not the ARV.

## Limits of this backtest — read before quoting it

1. **It tests the $/sf method, not the condition grade.** The county data has no condition
   field, so "renovated" could not be enforced. In production we hand-grade every comp, which
   should cut *bias* — a benefit this test could not measure. It does not cut dispersion.
2. **One ZIP, 13 months, 43 sales.** Not a national claim. Re-measure in each new market.
3. **43 sales is thin.** Treat the 39.5% as ±several points.
4. **44102 is a distressed submarket.** A bedroom community with homogeneous housing should
   test tighter, and if it doesn't, that is a finding.
5. **The ±30% band, radius ladder and median were all built before this test. The test did not
   tune them** — and where I tried (C, D), tuning made it worse. Do not tune to fit.
6. **Reproduce with:** `python3 state/backtest/cuyahoga_44102_walkforward.py` and
   `state/backtest/geo_tightness_test.py`, `state/backtest/county_value_benchmark.py`.
