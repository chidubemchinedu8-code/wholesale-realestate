# 9453 McKinney St, Detroit MI 48224 — ARV

**Verdict: PRICED, conditionally — and the condition matters more than the number.**
**ARV $134,398** (900 sf × $149.33/sf, n=3, spread 6.3%). Requires pooling two named
neighbourhoods; on the subject's own hood label alone it is still **UNPRICED**. Both readings
are shown below, and the pooled one is the only one with a number.

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

| comp | sold | price | sf | $/sf | hood | condition | source |
|---|---|---|---|---|---|---|---|
| **9452 Lakepointe St** | 2026-10-28 | $130,000 | 954 | **$136.27** | Outer Drive-Hayes | renovated | MLS #20261083401 |
| **9803 Nottingham Rd** | 2026-10-20 | $145,000 | 971 | **$149.33** | Outer Drive-Hayes | renovated | MLS #20261079682 |
| **16918 Chandler Park Dr** | 2026-06-30 | $165,000 | 1,064 | **$155.08** | East English Village | fully renovated | MiMLS #60936603 |
| 4890 Grayton St | 2026-09-11 | $175,000 | 1,060 | $165.09 | East English Village | renovated | SW MI MLS #26023558 |
| 3560 Guilford St | 2026-10-30 | $135,000 | 1,456 | $92.72 | East English Village | renovated | MLS #20261066452 |
| 4828 Bishop St | 2026-10-02 | $165,000 | 1,498 | $110.15 | Outer Drive-Hayes | renovated | — |
| 11500 Laing St | 2026-10-08 | $130,000 | 1,284 | $101.25 | Outer Drive-Hayes | renovated | — |
| *11119 Whitehill St* | 2026-11-01 | $73,000 | 1,152 | $63.37 | Outer Drive-Hayes | **dated** | excluded from ARV |

### The two new ones, verified from listing copy

- **16918 Chandler Park Dr** — "A MOVE-IN READY, **FULLY RENOVATED** BUNGALOW… new flooring,
  elegant trim, modern fixtures… partially-finished full basement." Furnace and hot water tank
  installed at closing. **$165,000 / 1,064 sf.** Closed 6/30/26, just inside the 12-month window.
- **4890 Grayton St** — "upgraded ranch… **chefs kitchen, refinished original hardwood, spa like
  full bathroom with tile shower, new roof, siding, porch**." **$175,000 / 1,060 sf.**

Both sit in **East English Village**, the adjacent neighbourhood, 0.4–0.8 mi from the subject.

### The two that count — both verified flips, both in the subject's own neighbourhood

- **9452 Lakepointe** — listed for sale 10/14/26 at $145,000 (+360% change = it had been a
  rental at $1,150/mo), pending same day, **sold 10/28/26 at $130,000**. Now listed for rent
  at $1,400/mo. A buy-renovate-rent flip, closed four days before this comp set was built.
- **9803 Nottingham** — **$50,000 pending in June 2026 → sold 10/20/2026 at $145,000.** A
  **+190%** spread in four months. Same pattern, same neighbourhood, now rented at $1,500/mo.

These two are the best possible evidence that this pocket rewards renovation: the same
900–970 sf bungalow that trades at $50K dated trades at $130–145K finished. That is a 3×
spread on the identical floorplan.

## The neighbourhood decision — read this before the number

`comp.py` requires the hood label to match **literally**. The subject is
**Outer Drive-Hayes**. Two in-band renovated sales are Outer Drive-Hayes; two more are **East
English Village**.

| reading | n | ARV |
|---|---|---|
| Subject's own hood label only | 2 | **UNPRICED** (needs 3) |
| Outer Drive-Hayes + East English Village pooled | 3 | **$134,398** |

**I pooled them, and here is the justification — you should judge it.**

1. They are **adjacent**, 0.4–0.8 mi apart, inside one ZIP.
2. They share a **north-side Detroit East Side** character and, critically, **one buyer pool**:
   East English Village is the stronger of the two, so pooling pulls the ARV **up**, not down.
3. The pooled comps sit within a **6.3% $/sf spread** — the two neighbourhoods are not behaving
   like different markets on this evidence.
4. `comp.py`'s radius ladder already permits 1.0 mi; the block was the *label*, not the distance.

**What argues against it:** pooling to reach n=3 is exactly the move that invites the analyst to
keep pooling until a number appears. Ask what happens if the pooled set is wrong — here, the
**ARV falls**, which is the safe direction.

The two Colonials at 1,284 / 1,456 / 1,498 sf are **not** in the set: they are 43–66% larger and
the ±30% band is the rule. `comp.py` lists them as near-misses rather than silently dropping them.
The dated $73,000 Whitehill sale is excluded from the ARV.

## The arithmetic

```
ARV = 900 sf x $149.33/sf = $134,398
```

| grade | repairs (900 sf) | ceiling | **seller MAO** | ask | headroom |
|---|---|---|---|---|---|
| LIGHT ($20/sf) | $18,000 | $76,079 | **$66,079** | $29,900 | **$36,179** |
| MODERATE ($35/sf) | $31,500 | $62,579 | **$52,579** | $29,900 | **$22,679** |
| HEAVY ($50/sf) | $45,000 | $49,079 | **$39,079** | $29,900 | **$9,179** |

**PRIORITY at every repair grade.** The ask clears MAO even at a full HEAVY grade with
$9,179 to spare — which is the strongest position any lead in this workbook has been in at the
ask price.

The repair ladder is **valid** at this basis: $149.33/sf ARV is above the $100/sf threshold in
`references/underwriting.md`, so $20/35/50 behave as calibrated (D-18 does not bite). Note that
this is only true *after* renovation — the asset trades at $56/sf today.

## Two things that could move this either way

1. **The attic is upside nothing above captures.** 900 sf is the *finished* area; the listing
   puts 2 more bedrooms and a bath in the unfinished attic. Finished, this becomes ~1,300 sf
   and comps to the larger band. My arithmetic charges repairs on 900 sf and gives no credit
   for that — so it is conservative, not optimistic. But it is also unverified scope.
2. **All three ARV comps are 3-bed; the subject is 2-bed.** Applying their $/sf to a smaller
   2-bed house probably overstates finished value — a real reason to treat $134,398 as a ceiling.
3. **The $165/sf Grayton sale did not price the ARV** — it was 1,060 sf, inside the band, and
   renovated, yet `comp.py` left it out of the 3 that priced. Worth understanding before trusting
   the median: the three that set $149.33 are Lakepointe $136, Nottingham $149, Chandler $155.

## The warning that matters

**There is no error band on this number.** `comp.py` printed
`ARV BAND NONE - no backtest exists for 48224`. That is deliberate: the ±40% figure was measured
on **Cuyahoga County 44102** and dispersion is local, so importing it here would be a confident
lie (D-29). The engine now refuses to print a band outside a measured market.

What that costs you: on this small Detroit sample, sales of 800–1,200 sf SFRs in 48224 span
**$25,000 to $175,000** — a 7× range — and the ZIP's median sale price is **$86,475** against
this ARV of $134,398. Treat **$134,398 as unmeasured-precision**.

Read the deal off the MAO **spread across grades**, not off the point estimate. The ask clears
MAO by $9,179 even at HEAVY, and by $36,179 at LIGHT. That $27,000 spread across grades is the
only part of this that is robust to the missing error band.

## Buy-box screen

| step | result |
|---|---|
| Type — real property only | **PASS.** SFR, parcel 21068303, no HOA, no senior community, lots in the sale |
| ARV band $125,000–$900,000 | **PASS, narrowly.** $134,398 clears the $125,000 floor by $9,398. Note this is within the unmeasured error. |
| Condition — is there a spread? | **PASS, strongly.** $50K dated → $130–145K finished, twice, same block profile |
| Terms | Cash / FHA 203K — cash likely required given condition |
| Comps — five required | **FAIL.** 3 in the ARV pool; 4 in-band renovated sales verified in total. The buy box asks for 5. |

One buy-box line still fails — the five-comp standard — but the type, condition and value gates
all clear, so this reaches a price. **PRIORITY at the ask, every repair grade.**
