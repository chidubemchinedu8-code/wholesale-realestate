# 8823 Edgewood Blvd, Tampa FL 33635 — why there is no ARV

**Request:** price this lead.
**Answer:** UNPRICED. Not a data failure — the asset is outside the buy box and outside
the method. Asking $59,990 (FSBO, 43 DOM, cut twice from $69,999).

## What the property actually is

| Field | Value | Source |
|---|---|---|
| Type | SingleFamily on Zillow | detail page |
| Reality | **Manufactured home, multi-section, on a LEASED lot** | community listing copy, MHVillage, Homes.com |
| Community | **Fountainview Estates**, a 55+ gated park | `## Neighborhood: Town 'n' Country`; Cal-Am Properties |
| Lot rent | **$1,050/mo** | current community listings; was $690 in 2021, $645 in 2019 |
| Built | 1982 | detail page |
| Beds/baths | 2 / 2, 1,100 sf | detail page |
| Parking | carport | detail page |
| Condition | **already updated** — updated kitchen, refreshed baths, new flooring | listing copy, 19 photos |

Zillow's `Home type: SingleFamily` is a misclassification. The community's own listings
describe "double-wide manufactured homes", and the `Community` field on the same Zillow page
reads *Doorman, Fitness Center, Fifty Five Plus Active Community, Assisted Living Community*.

> **The land is rented.** This is not a house on a lot. It is a vehicle on a rented pad.
> Financing, insurability, resale liquidity and resale value all follow from that.

## Why no ARV — four independent reasons

1. **The buy box excludes it.** `references/underwriting.md`: *Types — SFR, duplex,
   multifamily.* A manufactured home on leased land is personal property, not real property.
2. **ARV floor is $125,000.** The buy box states $125,000–$900,000. The best sale in this
   entire community, ever recovered, is **$138,000** (8825 Edgewood, 2017 build, 1,344 sf,
   Aug 2021) — and that was a *newer* home in a *lower-lot-rent* era. Nothing here clears the
   floor with room to work.
3. **Five comps cannot be assembled.** The buy box requires five. The only pool is 55+
   park homes in one community, which are not arm's-length comparable inventory — they are
   a captive market priced against a lot rent the buyer does not control.
4. **There is no rehab spread.** The home is already "beautifully updated". We buy condition
   problems; this has none.

## What the market actually looks like (asks and one sale — NOT an ARV)

| property | built | sf | beds | price | notes |
|---|---|---|---|---|---|
| 8825 Edgewood Blvd | 2017 | 1,344 | 3/2 | **$138,000 SOLD 8/2021** | the only recovered sale |
| 8828 Edgewood Blvd | 2026 | — | — | $219,900 ask | new build, park-dealer owned |
| 8823 Edgewood Blvd | 1982 | 1,100 | 2/2 | **$59,990 ask** ← subject | cut from $69,999 |
| 9119 Berkshire Ln | — | — | — | $139,900 ask | |
| 8813 Lochmoor Rd | 1999 | 1,488 | 3/2 | $97,900 ask | |
| 8819 Wellington Dr | 1993 | 990 | 3/2 | $94,900 ask | |
| 9143 Berkshire Ln | — | 1,240 | 3/2 | $89,900 ask | |
| 8832 Nautilus Dr | — | 1,536 | 2/2 | $82,500 ask | |
| 9017 Nautilus Cir | — | 1,344 | 3/2 | $52,900 ask | |
| 8815 Westchester Rd | 1980 | 960 | 2/1.5 | $39,900 ask | |
| 9010 Nautilus Dr | 1982 | 924 | 2/2 | $37,900 ask | reduced |
| 9117 Berkshire Ln | — | 1,056 | 3/2 | $18,900 ask | |

The subject at $59,990 is at the **top of its 1980s cohort**, not a discount. Several
comparable 2/2s in the same park ask **less than half**.

**Do not average these into an ARV.** They are asks in one park, cross-topic on lot rent, and
mixed across a $18,900–$219,900 span that reflects decade of manufacture more than condition.

## The structural trap: lot rent is ratcheting

The lot rent on this pad went **$645 (2019) → $690 (2021) → $892–$1,050 (2026)** — roughly
+63% in seven years, while the homes themselves depreciate. The park owner captures the
appreciation; the homeowner does not.

This shows up in the data as a market that will not clear: the same 33635 mobile-home feed is
full of "$25K PRICE DROP", "$30K PRICE DROP", "$40K PRICE DROP" and seller-financing offers.
That is not a coincidence. It is what a captive market looks like when the ground lease
reprices faster than the asset.

**Consequence for a wholesaler:** the exit is to a cash buyer who must also accept the lot
rent and the 55+ age restriction. That buyer pool is thin, slow, and price-sensitive — the
opposite of what an assignment needs.

## The arithmetic, shown so the refusal is falsifiable

If a generous ARV of $65,000 were accepted and the engine run:

```
ceiling = 65,000 × 0.70 − repairs
light    = 1,100 sf × $20 = $22,000
ceiling  = 45,500 − 22,000        = $23,500
MAO      = 23,500 − 10,000 fee    = $13,500
```

A $22,000 "light" rehab against a $60,000 home is nonsense — you would replace the structure
for that. This is not a conservative answer, it is a broken one, and it exposes the real
defect: **the `$/sf` repair tiers do not transfer to manufactured housing.** Rehab cost there
does not scale with floor area the way it does on stick-built, and the asset value per sf is
too low to absorb a percentage-of-value rehab at all.

## Disposition

- **Verdict: UNPRICED.** Gate: wrong asset class + below ARV floor + already renovated.
- **Not added to the ZIP universe.** 33635 is not a market we scan; this was a one-off
  inquiry. Adding a ZIP implies coverage we have not earned.
- **Not added to the property ledger.** The ledger is a Dayton/Akron/Cleveland duplicate
  guard; a Tampa park home in it would pollute the duplicate check.
- If the user wants Florida manufactured housing as an asset class, that needs its own
  method — starting with a lot-rent-adjusted valuation, not a `$/sf` comp median.
