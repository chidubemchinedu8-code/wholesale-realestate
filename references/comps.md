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
45410 file were typed from memory: `164 Edgar Ave` 2026-09-15 and
`40 Indiana Ave` 2026-08-01.

- **`40 Indiana Ave` closed 2026-08-05, not 2026-08-01.** Four days wrong is
  still wrong, and wrong dates move sales in and out of the 180-day window.
- **`164 Edgar Ave` is a real sale.** Its hand-typed date was wrong — the sale
  closed **2026-07-06** at $169,900 — but the property is not invented. It is
  a 1,499 sf, 3 bd / 1.5 ba, built 1913, parcel R72034120008, MLS# 959119,
  listed 5/22/2026 at $159,900, pending 5/29, closed $169,900 (103% of list).
  Listing copy: brand-new carpet, updated eat-in kitchen, grey cabinets,
  brand-new appliances — **renovated**. It belongs in the ARV pool.

The rule: an undated row is dropped by the loader, so if a row is deliberately
left undated it must be *marked* in the exclusion column (`date_unverified`) —
otherwise it disappears silently and the comp set looks thicker than it is.
Section 9n of the test suite enforces both halves.

## "Not in this one list" is not "does not exist"

`164 Edgar Ave` was reported as a **phantom comp** because it did not appear in
Redfin's 45410 sold list, and the wrong date was taken as corroboration. That
was a false negative, and the correction matters:

- **Redfin's sold list is not the set of all sales.** It returned 87 homes for
  45410; Realtor.com returns ~271 four-bedroom sales for the same ZIP. A
  property can be absent from the filtered list and still be a real, recent,
  arm's-length sale.
- Absence from one aggregator must **never** be written up as "this sale does
  not exist". The honest finding is "I could not confirm it here", followed by a
  second source — Zillow by zpid, Realtor.com by address, or the county.
- A wrong *date* on a real property is a data-entry error. Treating it as proof
  of a fabricated property compounded one small error into a large one.

**Realtor.com is a first-class sold-date source and was missing from the ladder.**
It exposes exact sold dates, price history, year built, sq ft, lot, tax
assessment and **permit history** on a plain property page, and it is not
paywalled or bot-blocked the way the others can be. Use it as a cross-check on
every sold date before drafting, and use permit history as evidence of real
renovation work (a 2024 HVAC permit is stronger evidence than the word
"updated" in listing copy).
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

**Never build a comp set by joining two neighbourhoods.** The 4074 Middlehurst
row originally quoted three MAOs ($62,443 / $88,510 / $108,956) built from
2016 Kipling Dr — in the subject's own Cornell Heights — plus 1740 Burbank Dr,
**1.16 mi away in Upper Dayton View**. That is a comp set stitched across a
neighbourhood split, and it produced confident numbers from it. Every one of the
six verified 45406 sales in band turned out to be *updated* or *maintained*;
**not one was a full renovation**. Cornell Heights has only two sales in 180
days.

The correct answer was a clean `UNPRICED` with no band at all. A band is a
convenience that may only be offered when the underlying pool is legitimate;
attaching one to an illegal pool makes an unpriced deal look underwritten. When
a band is withdrawn, say so in the flags and leave the retired numbers visible
as retired — do not quietly delete them, because the operator may already have
used them.

The six verified sales still do useful work as an **as-is floor**: updated homes
$85–$137/sf, maintained $80–$85/sf, which for a 1,259 sf house is roughly
$103,000–$151,000. A floor is a legitimate output; an ARV is not available.


## Manufactured homes are not a comp set — and often not the asset you think

A manufactured home on a **leased lot** is personal property on a rented pad. It is not a
house, it does not finance like one, and `$/sf` medians do not transfer to it.

Zillow labels them `Home type: SingleFamily`. Do not trust that field. Check, in this order —
any one is disqualifying:

1. `sqft lot` shows `--` (no land in the sale).
2. `Parking features: Carport` on a "single family" home.
3. `Community` names a 55+/active-adult or assisted-living community.
4. Price per sqft far under the ZIP median (8823 Edgewood Blvd: **$55/sf** in a **$366K** ZIP).
5. The `Similar homes` carousel fills with "Mobile Home Sales" / "Mobile Home Brokers" agents.
6. Cross-check MHVillage, Homes.com, or the park's own website.

**Lot rent is the real variable, and it ratchets.** At Fountainview Estates the pad went
$645/mo (2019) → $690 (2021) → $1,050 (2026), about +63% while the homes depreciated. The park
owner captures the appreciation. A market like this shows up as endless "PRICE DROP" and
seller-financing ads — a captive market repricing its ground lease faster than its assets.

**Never build a comp pool from one 55+ park.** It is a captive market, not arm's-length
inventory. Refuse, and say why.
