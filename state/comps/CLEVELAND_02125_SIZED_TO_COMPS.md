# Cleveland 44102 / `02125` — screening from *where the comps are*

**The screen was backwards.** Daisy Ave started with the biggest house available and then asked
whether a comp set could be built around it. It could not, and it never was going to: 44109 has 24
sales ≥1,600 sf in a year. This run starts from the pool that is **deep** and asks which foreclosure
parcels land inside it.

**Result: 6 of 6 leads priced. No `UNPRICED`.** That has not happened in this market before.

---

## 1. Where the depth actually is — measured

| pool | 6-month 44109 sales |
|---|---|
| houses ≥1,600 sf (Daisy's band) | **24** — "page 1 of 1" |
| houses 1,200–1,700 sf | **86** |

**3.6×** the comp depth for a house 30% smaller. The Daisy band was not merely thin; it was the
thinnest band in the ZIP.

County foreclosure supply runs the same direction — free-and-clear, delinquent, `foreclosure_flag=1`:

| ZIP | 1,200–1,700 sf | 1,700–2,300 sf |
|---|---|---|
| 44102 | **44** | — |
| 44109 | 29 | — |
| 44111 | 11 | — |
| **3-ZIP total** | **84** | **31** |

**44102 holds the most supply and the deepest comps at once.** So the intersection is 44102 in the
1,200–1,700 sf band — 30 single-family rows once the 1-family type is enforced.

`02125` is the county's code for the W 86th–W 95th corridor, **verified by query, not by memory**
(that error is D-30). 3308 W 88th was `02125`; so were 12 of the pool sales.

---

## 2. The six priced leads

All `02125`, all `foreclosure_flag=1`, all `lender='NO LENDER'`, all delinquent, all single-family,
1,204–1,562 sf, priced from the **same hood's** comp file
(`cleveland_44102_hoodcoded_comps.csv`, hood codes county-verified).

| address | parcel | sf | style | ARV | $/sf | n | conf | MAO L / **M** / H | tax owed | headroom @M |
|---|---|---|---|---|---|---|---|---|---|---|
| **3350 W 86th St** | 01730053 | 1,204 | COL | **$132,951** | 110.42 | 4 | 24.4% | $58,986 / **$40,926** / $22,866 | $7,545 | **$33,381** |
| **3206 W 90th St** | 01702035 | 1,300 | COL | **$143,552** | 110.42 | 4 | 24.4% | $64,486 / **$44,986** / $25,486 | $7,543 | **$37,443** |
| **3400 W 95th St** | 01725121 | 1,416 | COL | **$143,229** | 101.15 | 4 | 8.4% | $61,940 / **$40,700** / $19,460 | $4,618 | **$36,083** |
| **3211 W 92nd St** | 01702047 | 1,375 | COL | **$136,952** | 99.60 | 3 | 3.1% | $58,366 / **$37,741** / $17,116 | $4,372 | **$33,370** |
| **3392 W 94th St** | 01728063 | 1,346 | COL | **$138,234** | 102.70 | 5 | 21.1% | $59,844 / **$39,654** / $19,464 | $2,598 | **$37,056** |
| **7270 Wentworth Ave** | 00628091 | 1,562 | COL | **$155,578** | 99.60 | 3 | 3.1% | $67,665 / **$44,235** / $20,805 | $3,106 | **$41,128** |

**Combined MODERATE headroom against tax owed: $218,461** across six properties.

`MAO = 0.70 × ARV − (sf × repair $/sf) − $10,000`, repairs at $20/$35/$50 per sf.
The tax balance is the **opening ask proxy** on a free-and-clear tax foreclosure, not a purchase
price — the county wants its arrears, and the surplus goes through the sheriff's process.

### Caveats that are load-bearing

1. **`ARV BAND NONE` on all six.** There is **no backtest for `02125`**. The error is *unmeasured*,
   and D-29 forbids importing 44102's ±40% band. These point figures are the least supported
   numbers in the file.
2. **Bed counts are absent.** The county records *rooms*, not bedrooms. `comp.py` correctly refuses
   to guess, which means **the bed floor did not run on any of the six** — a pass in the table is
   not the same as a passed gate. A 2-bedroom 1,300 sf house would price identically to a 3-bedroom.
3. **Condition is unknown on every subject.** Repairs are modelled at all three tiers precisely
   because nobody has walked these houses.
4. **Two are on payment plans** (3350 W 86th, 7270 Wentworth) — a plan in place usually means the
   owner is trying to keep the house, so expect a slower or refused conversation. Not disqualifying,
   but it changes the approach to owner outreach.
5. **`foreclosure_flag=1` still does not mean active litigation** (this remains the open
   assumption from the previous pass).
6. **Hood-wide `$/sf` is 3.1%–24.4% dispersed.** The comp sets are tight in count, not in price.

---

## 3. The measured error swamps the whole list — read this before the table

`02125` has no backtest. The nearest measured figure is 44102's walk-forward **±40%** MAPE. That
band is **not** transferable (D-29), so the following is a **stress test, not a band**:

| address | ARV −40% | MAO @MODERATE | verdict |
|---|---|---|---|
| 3350 W 86th | $79,771 | $3,699 | survives, barely |
| 3206 W 90th | $86,131 | $4,792 | survives, barely |
| 3400 W 95th | $85,937 | $596 | **effectively zero** |
| 3211 W 92nd | $82,171 | **−$605** | **gone** |
| 3392 W 94th | $82,940 | $948 | **effectively zero** |
| 7270 Wentworth | $93,347 | $673 | **effectively zero** |

**At the measured error rate this list is worth roughly one deal, not six.** The MAO collapses to
near zero because repairs and fee are fixed costs against a shrinking ARV. Saying "six priced
leads, $218K of headroom" without this paragraph would be the D-50 mistake again in a new costume.

---

## 4. The finding that matters more than the six leads

**`$121.25/sf` was 18% too high, and it was the number the whole Cleveland thesis rested on.**

Recomputing `02125` hood-wide rather than on a 0.25 mi pocket:

| basis | n | $/sf | ARV on 1,155 sf |
|---|---|---|---|
| 0.25 mi pocket (as published) | 3 | **$121.25** | **$140,041** |
| hood-wide `02125`, renovated | 5 | **$102.70** | **$118,619** |
| hood-wide `02125`, all conditions | 12 | **$100.20** | $115,731 |

The tight radius did not find *comparable* houses; it found the **three most expensive $/sf sales in
the hood**, because renovated stock clusters in a small pocket on W 88th–91st. Tightness felt like
rigour and behaved like an outlier filter. (D-51)

**Consequences:**

- **3308 W 88th's ARV is overstated by ~$21,400 (15%)**, and its MAO by ~$15,000. It was already
  a WALK at the $95,000 ask; at $102.70/sf it is a much deeper walk. The verdict does not change,
  the margin does.
- **`/sf` is not constant across size.** Regressing the 16-comp 44102 file:

  ```
  $/sf = 113.1 − 0.0097 × sqft      →  $103 @1,000 sf,  $100 @1,300,  $97 @1,700
  ```

  $/sf falls about **$1.00 per 100 sf**. The flat-$/sf method systematically **overvalues large
  houses and undervalues small ones** — which is a second, independent reason Daisy could not be
  priced honestly, and a reason every MAO on a 2,300+ sf subject was overstated.
- **The `$49.875/sf` shortcut is now dead twice over**: wrong hood (D-50) *and* wrong at any size
  other than ~1,155 sf.

---

## 5. What this says about the business

The Channel 2 thesis survives with a sharper edge. The spread on these six is **$33K–$41K per
property at MODERATE**, against tax arrears of **$2.6K–$7.5K**. That is not a marginal trade.

But the binding constraint moved: **it was never lead supply — 84 candidates — it was comp
calibration.** And calibration only exists where a backtest exists, which is nowhere in Cleveland
yet. The next honest step is not another lead list. It is a **walk-forward backtest for `02125`**,
which would turn six point estimates into six bands and tell us whether the $33K spreads are real.

## Files

- `cleveland_44102_hoodcoded_comps.csv` — the comp set, hood codes county-verified.
- `CLEVELAND_44102_3308_W88TH.md` — carries a correction notice for D-51.
- `DEFECT_LOG.md` — D-50, D-51.
