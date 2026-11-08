# Comparable sales — the five-comp standard

Five credible sold comps, or the ARV is not supported. There is no third state.

## Step 0 — verify the subject across four sources

Before any comp is pulled, establish the subject from **MLS/agent remarks, public
records, Zillow and Redfin**. Never finalize from one source.

| Source | Wins on |
|---|---|
| Public records (county assessor / recorder) | beds, baths, sqft, year built, lot, platted subdivision |
| MLS / agent remarks | condition language, days on market, disclosures, showings |
| Zillow property page | price history, Zestimate, rent estimate, MLS number |
| Redfin | DOM, sold records, agent contact, photo set |

If two sources disagree, **state the conflict and both values**, name which is more
reliable and why, and never quietly pick the one that helps the deal.

**Subdivision / plat check.** Confirm the subject's actual platted subdivision from
public records — not an aggregator's drawn "neighbourhood" polygon, which blends
different eras and tiers together. Where the plat is unavailable, say so, and treat
the neighbourhood gate in `comping/COMPING.md` as ZIP-level only.

Comps are split by condition tier: **ARV uses the renovated pool only**; the
distressed/dated pool may only inform the as-is floor. Never blend the two into one
average, and never let a distressed sale into the ARV number.

## Comp selection, in priority order

1. Same ZIP code, then immediate neighbourhood
2. Same property type (SFR / duplex / multi / condo)
3. Same bed and bath count
4. Similar living area
5. Similar lot characteristics where relevant
6. Similar age and construction where relevant
7. Sold within the previous 6 months
8. As close to the subject as possible

**Start closest and most similar. Expand only when needed, and say why.** "Expanded
from 44302 to 44303" is a different claim from "expanded to 1.5 miles across a ZIP
line" — the first crosses a submarket and must be justified with a $/sqft comparison.

## Required field per comp

```
Address | Sale price | Sale date | Type | Beds | Baths | Living area
Distance from subject | Source | Direct URL | Condition at sale
Why comparable | Meaningful differences
Verified or reported
```

`Verified` = the county deed record or the listing's own sold record was read.
`Reported` = a secondary site states it. Most Redfin/Zillow sold data is `REPORTED`
for our purposes unless a county record was pulled — say which.

## Never

- Active, pending, or withdrawn listings as sold comps
- A Zestimate as a comp
- A neighbourhood or ZIP average as a substitute for comps
- Renovated and distressed sales averaged silently into one number
- Five comps assembled by lowering the bar until five appeared
- A sale you did not actually open
- Borrowing another submarket's prices because the ZIP has no sales

## Exclusions — these are not comps

| Exclude | Why |
|---|---|
| Deed-restricted / AMI-limited sales | A **floor**, not market value. Two of these understated a deal by $20,000 |
| Newer build in an older block | Different product. A 2020s build at $155/sqft is not evidence for a 1920s subject |
| Condos (unless the subject is a condo) | Different ownership product |
| Non-arm's-length transfers | Quitclaims, family transfers, $1 deeds, a $325 "sale" on a $94,300 house |
| As-is vs renovated mismatch | Keep the renovated set for ARV, the as-is set separately for the floor |

## ARV

Use the **renovated** comps for ARV. Distressed sales are not a second valuation.

```
MEDIAN $/sqft of the chosen comps × subject sqft
```

Median, not average, so one strange sale cannot drag the ARV. No haircut, no
percentile tier, no second method — the median is the number. The p25-p75 spread
is reported as confidence, never as a range of ARVs.

Then report, always:

- Which comps are most relevant, and why
- Which comps were down-weighted, and why
- The supported **range** (low / working / high)
- The single **working ARV**
- Confidence: `HIGH` (5+ tight comps, same ZIP, similar size/type, all within 6 months),
  `MEDIUM` (5 comps but one or two weak matches, or a radius expansion),
  `LOW` (fewer than five, or heterogeneous)
- What uncertainty could materially change it

Under five comps: `ARV INSUFFICIENTLY SUPPORTED`. The property cannot be submitted.
Say so in the verdict, not in a footnote.

## Statement about what ARV is

An ARV is a **market-value estimate**, not an appraisal, and not an offer. Every report
says this in those words.

## Two data defects found in the wild (2026-11-08, Dayton)

Both were found by re-reading the source pages rather than trusting the comp
file. Both had already survived a "clean" preflight, so neither is theoretical.

**A comp file must never carry a hand-typed sold date.** A date is a fact about
a parcel; it comes off the property page or it is not a date. Two dates in the
45410 file were typed from memory: `164 Edgar Ave` 2026-09-15, and
`40 Indiana Ave` 2026-08-01. Re-fetching the sold list showed:

- **`164 Edgar Ave` does not exist in 45410's sold list at all.** The nearest
  real properties are 32 Edgar ($144,900, 1,541 sf, 3 bd), 40 Edgar ($170,000,
  1,415 sf, 3 bd) and 416-418 Edgar (a 6-bd duplex). A phantom comp had been
  shaping a comp set.
- **`40 Indiana Ave` closed 2026-08-05, not 2026-08-01.** Four days wrong is
  still wrong, and wrong dates move sales in and out of the 180-day window.

The rule: an undated row is dropped by the loader, so if a row is deliberately
left undated it must be *marked* in the exclusion column (`date_unverified`) —
otherwise it disappears silently and the comp set looks thicker than it is.
Section 9n of the test suite now enforces both halves.

**An exclusion tag the engine does not recognise must refuse the file, not be
ignored.** The 45417 file tagged a court-ordered auction sale
`auction_not_arms_length`. The engine's recognised reasons included
`non_arms_length`, so the tag did not match, the sale was **not** excluded, and
a $35,860 court-ordered transfer joined the ARV pool as an ordinary open-market
comp. It only stayed out of the final maths because two other comps were
undated, not because anything caught it.

Fixed two ways: `EXCLUSION_ALIASES` maps the common misspellings
(`auction_not_arms_length`, `sheriff_sale`, `foreclosure`, `land_bank`,
`income_restricted`, …) onto the real reasons, and `load_comps` now raises on
any tag that is still unknown. A comp file that cannot be read unambiguously
gets corrected — never averaged over.

**Related bug, same round:** an unpriced row with a graded repair figure always
reported `FAIL no repair number without a grade`, because the check demanded a
ceiling that an unpriced deal can never have. That is dangerous: a permanent
false failure trains the operator to ignore the one check that stops a ceiling
being invented. An unpriced row now passes when it quotes no ceiling.

**A band near-miss must be reported, not swallowed.** 512 Campbell St (1,132 sf)
against a 1,628 sf subject is 7 square feet outside the ±30% band on the low
side (floor 1,139.6). The engine dropped it silently: it left `usable`, was
never added to `rejected`, and never printed. The report therefore said "fewer
than 3 sales within 1.5 mi" — which reads as *the market is thin*, when in fact
a relevant, renovated, verified sale was sitting almost exactly on the boundary.

The band is correct and must not be widened for a near-miss. But the operator
needs to *know* the near-miss happened, because it changes the answer from
"nothing here" to "one more ~1,500 sf sale resolves this". Out-of-band comps are
now listed closest-miss-first with their square-foot gap and counted as
`sqft_band` in the filter tally.

**When only two comps survive, print the dispersion before concluding.** For
330 Bolander the two survivors were $130.29/sf and $78.66/sf — a **1.66×**
spread. That number is the finding. It explains why two comps can never set a
median, and it lets a reader see that the verdict flips across the band
(MAO $22,660 at the low comp, $81,502 at the high one). Quote the spread, not
just the word UNPRICED.
