# 9453 McKinney St, Detroit MI 48224 — ARV

**Verdict: UNPRICED.** No ARV issued. Two renovated comps verified, three required.

> The address arrived with no ZIP. It is **48224**, not the 48213 I first tried — Zillow's
> `_rb` URL redirected. Confirmed by parcel `21068303` and by the listing's own MLS #50221646.

## The subject

| Field | Value |
|---|---|
| Type | SFR, **Bungalow**, 1.5 story, brick |
| Built | 1928 |
| Beds/baths | **2 / 1** |
| Living area | **900 sf above ground** (total structure 1,600; below grade 0) |
| Basement | Full, unfinished |
| **Upside** | Stairs to an **unfinished attic** "with room for another bath and 2 more bedrooms" |
| Lot | 3,920 sf (35 × 115) |
| Parcel | 21068303 · Subdivision: Leigh G Cooper |
| Cooling | Not stated — **must be confirmed** |
| Ask | **$29,900** (listed 9/13/26 $30,000, cut twice, 56 DOM) |
| Terms | Cash, **FHA 203K** — a rehab loan, which is the seller telling you it needs work |
| Tax assessed | $26,600 · $1,438/yr |
| Notes | "Needs TLC but is a real money maker." Prior use unclear. **Seller requires the buyer to remove the existing steps to the church parking lot**, eliminating the easement. |
| Neighbourhood | **Outer Drive-Hayes** |

## The comps

| comp | sold | price | sf | $/sf | style | source |
|---|---|---|---|---|---|---|
| **9452 Lakepointe St** | 2026-10-28 | $130,000 | 954 | **$136.27** | Bungalow | MLS #20261083401 |
| **9803 Nottingham Rd** | 2026-10-20 | $145,000 | 971 | **$149.33** | Bungalow | MLS #20261079682 |
| 3560 Guilford St | 2026-10-30 | $135,000 | 1,456 | $92.72 | Colonial | MLS #20261066452 |
| 4828 Bishop St | 2026-10-02 | $165,000 | 1,498 | $110.15 | Colonial | — |
| 11500 Laing St | 2026-10-08 | $130,000 | 1,284 | $101.25 | Colonial | — |
| *11119 Whitehill St* | 2026-11-01 | $73,000 | 1,152 | $63.37 | — | **dated, not renovated** |

### The two that count — both verified flips, both in the subject's own neighbourhood

- **9452 Lakepointe** — listed for sale 10/14/26 at $145,000 (+360% change = it had been a
  rental at $1,150/mo), pending same day, **sold 10/28/26 at $130,000**. Now listed for rent
  at $1,400/mo. A buy-renovate-rent flip, closed four days before this comp set was built.
- **9803 Nottingham** — **$50,000 pending in June 2026 → sold 10/20/2026 at $145,000.** A
  **+190%** spread in four months. Same pattern, same neighbourhood, now rented at $1,500/mo.

These two are the best possible evidence that this pocket rewards renovation: the same
900–970 sf bungalow that trades at $50K dated trades at $130–145K finished. That is a 3×
spread on the identical floorplan.

## The gate that failed

```
ARV  NO COMPS - only 2 renovated comp(s) within 1.5 mi (needs 3)
```

The subject is **900 sf**. The ±30% band is therefore **630–1,170 sf**. Only Lakepointe (954)
and Nottingham (971) fit. The three Colonials at 1,284 / 1,456 / 1,498 sf are **not** errors to
be fixed — they are 43–66% larger and the band is the rule. `comp.py` listed them as near-misses
rather than silently discarding them, which is the behaviour I want.

**I did not:** average the two, widen the band, substitute the dated $73,000 sale, or reach into
another Detroit ZIP. Unpriced is the answer.

## Conditional arithmetic — NOT an ARV, do not quote it as one

If a third renovated 900–1,100 sf sale confirms this band, the method would give:

```
median of $136.27 and $149.33 = $142.80/sf  (n=2, 9.6% apart)
900 sf x $142.80             = $128,520
```

On a **moderate** grade ($35/sf × 900 = $31,500 repairs):

| line | value |
|---|---|
| ceiling (0.70 × 128,520 − 31,500) | $58,464 |
| seller MAO (−$10,000 fee) | **$48,464** |
| ask | $29,900 |
| **headroom** | **$18,564 (38% under MAO)** |

**That would be a PRIORITY-shaped deal at the ask.** Which is exactly why it is worth the
effort of finding a third comp — and exactly why I will not call it before I have one.

The repair ladder is valid at this basis: $142.80/sf ARV is above the $100/sf threshold in
`references/underwriting.md`, so the $20/35/50 tiers behave as calibrated (D-18 does not bite).

## Two things that could move this either way

1. **The attic is upside nothing above captures.** 900 sf is the *finished* area; the listing
   puts 2 more bedrooms and a bath in the unfinished attic. Finished, this becomes ~1,300 sf
   and comps to the larger band. My arithmetic charges repairs on 900 sf and gives no credit
   for that — so it is conservative, not optimistic. But it is also unverified scope.
2. **900 sf 2-bed is a thinner buyer pool than 971 sf 3-bed.** Both comps are 3-bed. Applying
   their $/sf to a smaller 2-bed house probably overstates the finished value somewhat — a
   second reason the conditional figure is a ceiling, not a target.

## The warning that matters

**The ±40% error band does not come with this house.** That figure was measured on **Cuyahoga
County 44102** (`state/comps/BACKTEST_44102.md`) and it does not transfer to a market I have not
backtested. On this small Detroit sample the spread is $63–$149/sf across renovated and dated
sales — a 2.4× range, comparable to or wider than Cleveland's.

So the conditional $128,520 carries an **unmeasured** error, plausibly wider than ±40%. At ±40%
the band would be $77,112 – $179,928. The **buy box needs an ARV of $125,000+**, and the bottom
of that range fails it outright.

## Buy-box screen

| step | result |
|---|---|
| Type — real property only | **PASS.** SFR, parcel 21068303, no HOA, no senior community, lots in the sale |
| ARV band $125,000–$900,000 | **UNRESOLVED.** Conditional $128,520 clears by $3,520. Inside the error band, it may not. |
| Condition — is there a spread? | **PASS, strongly.** $50K dated → $130–145K finished, twice, same block profile |
| Terms | Cash / FHA 203K — cash likely required given condition |
| Comps — five required | **FAIL.** 2 verified; the buy box asks for 5 |

Two buy-box lines fail, so this does not reach a number. That is the complete answer.
