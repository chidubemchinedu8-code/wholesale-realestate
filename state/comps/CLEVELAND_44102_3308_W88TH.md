# 3308 W 88th St, Cleveland OH 44102 — ARV

**ARV $140,041** · median $121.25/sf × **1,155 sf** · n=3 renovated Colonial, 0.25 mi.

> **Read the band, not the point.** Walk-forward backtest on 43 Cuyahoga sales puts this method's
> median error at **±40%** (`state/comps/BACKTEST_44102.md`). The honest range is
> **$84,024 – $196,057**. Only 21% of backtested sales landed within ±20%.

Hood **West Boulevard** (Zillow `## Neighborhood`). Listed 11/04/26, 2 DOM, MLS# 5259055.

## ⚠️ The sqft defect — read this first

The sweep recorded this subject at **1,727 sf**, taken from the Zillow card. Redfin and the
county public record both say **1,155 sf**. That is a **572 sf / 33% overstatement**, and it
inflated the ask-per-foot from **$82.25** to the **$55.01** that got it onto the shortlist.

**Public records win on hard facts** (`comping/COMPING.md` §2). The subject is priced on
**1,155 sf**. This defect is now `DEFECT_LOG.md` **D-47** and it invalidates any
`$/sf` ranking built on Zillow card data alone.

Had the error stood, the ARV would have been **$209,398** — **$69,357 (50%) too high**, and
the three "cheapest per foot" rows in the sweep would have been fiction.

## The subject

| Field | Value |
|---|---|
| Type | SFR, 2-story Colonial |
| Built | 1915, vinyl siding |
| Beds/baths | 3 / 1 |
| **Living area** | **1,155 sf** (Redfin + public record) |
| Lot | 4,338 sf |
| Parking | 2-car garage |
| Condition | "investors… make a few improvements… **as-is**", **now vacant** |
| Terms | Seller AS-IS |

As-is language, cosmetic updates needed, vacant. That is a **MODERATE** grade by default —
LIGHT would need a walkthrough showing recent systems, and this listing names none.

## The comps

| comp | sold | price | sqft | $/sf | bd | condition | mi |
|---|---|---|---|---|---|---|---|
| 3197 W 90th St | 2026-05-08 | $125,000 | 1,296 | $96.45 | 3 | **renovated** | 0.21 |
| 3428 W 90th St | 2026-04-14 | $153,500 | 1,266 | $121.25 | 3 | **renovated** | 0.24 |
| 3435 W 91st St | 2026-06-18 | $135,000 | 968 | $139.46 | 3 | **renovated** | 0.24 |

- **3197 W 90th** — "totally remodelled colonial… new cabinets, granite, stainless, new
  furnace". A full renovation.
- **3428 W 90th** — "updated top to bottom", new cabinetry, custom tiled shower, new
  plumbing/electrical/windows. The strongest renovation in the set.
- **3435 W 91st** — "beautifully remodeled… move-in ready", new LVT, new windows, painted
  inside and out. Note: **kitchen and bath not described** — cosmetic-grade remodel.

**The 180-day window returned NO COMPS** (only 2 renovated in band). The ladder permits up to
**12 months**; at 365 days it yields exactly 3. That is the floor, not a comfortable set.

**Excluded and it matters:** `1338 W 89th St` at $250,000 / $172 per sf is a **2003 build** —
a different product, and the obvious trap in this pool. `3151 W 94th St` at $147,000 is a
**duplex**. `3210 W 90th St` ($175,000) and `3211 W 90th St` ($150,000) are renovated and
tempting but fall **outside the ±30% sqft band** — the band is the rule, not a suggestion.

**Five maintained/dated sales sat in radius and were correctly barred from the ARV pool:**
$90,000 / $95,000 / $101,000 / $125,000 / $127,400. They set the **as-is floor at roughly
$78–90/sf** — which is where the $95,000 ask actually lives.

## Arithmetic

```
ARV = 1,155 sf × $121.25/sf = $140,041
```

| grade | repairs | ceiling (0.70×ARV − repairs) | **MAO** (−$10K fee) | offer low/high |
|---|---|---|---|---|
| LIGHT ($20) | $23,100 | $74,929 | **$64,929** | $53,923 / $60,925 |
| **MODERATE ($35)** | **$40,425** | **$57,604** | **$47,604** | $36,598 / $43,600 |
| HEAVY ($50) | $57,750 | $40,279 | **$30,279** | $19,273 / $26,275 |

**Verdict: WALK at the ask. NEGOTIATE only below ~$48,000.**

At MODERATE the seller MAO is **$47,604** against a **$95,000** ask — a **50% cut**. The ask is
also *above the LIGHT ceiling of $74,929*, meaning even a light-repair assumption needs a
$20,000 reduction before any fee.

The spread exists only in the bottom half of the band. At the −40% ARV ($84,024) the ceiling is
**$18,392** and the MAO is **$8,392** — the deal evaporates entirely, and that outcome is
inside one standard backtest error.

## Honest caveats

1. **n=3 is the floor.** The engine warns it. A single wrong condition grade in that set moves
   the median materially — 3435 W 91st at $139/sf is pulling the top.
2. **3435 W 91st may be over-graded.** "Remodeled" with new floors and paint but no kitchen or
   bath work is cosmetic, not renovated. If it is downgraded, n drops to 2 and this becomes
   **UNPRICED**. That is a live risk to the whole number, not a footnote.
3. **Hispanic/latino corridor pricing.** The three comps are all on W 88th–91st; the subject is
   on W 88th. Radius is genuinely tight (0.25 mi) — this is not a pooled number.
4. **The ±40% band is $112,033 wide.** Narrow comp spread (17.7%) is *not* evidence of accuracy;
   the backtest found the opposite.
5. **Repairs charged on 1,155 sf only.** A 1915 house at 4,338 sf lot with a garage is likely
   to carry roof/HVAC/electrical exposure the listing does not name. HEAVY is plausible.
6. **Comp condition sourced from Redfin listing remarks**, not from photos or a walkthrough.
   Remarks are an agent's characterisation — the best available evidence, not proof.
