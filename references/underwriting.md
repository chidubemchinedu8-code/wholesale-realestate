# Buyer and seller underwriting

Mandatory on every property. The two numbers are different and are never merged.

```
Step 1  screening ceiling   = ARV × 0.70
Step 2  buyer max contract  = (ARV × 0.70) − repairs − buyer costs
Step 3  seller-facing MAO   = buyer max − assignment fee − wholesaler costs
Step 4  opening offer       = below the MAO, justified by the seller's situation
Step 5  buyer gross spread  = ARV − contract price − repairs      (NOT profit)
Step 6  assignment fee      = what you actually keep, checked against buyer viability
```

Run it with the script rather than by hand:

```bash
python3 scripts/underwrite.py --arv 200000 --repairs 25000 --fee 10000
```

## Step 1 — screening ceiling

`ARV × 0.70`. This is RealVenture's stated screening guideline. It is **not** an offer
and **not** proof a buyer will pay it — it is a buy-box policy, not a market
measurement. **Confirmed by the operator (2026-11-08): 0.70 is the deliberate
midpoint of a 0.65–0.75 range.** They describe it as the safe space: 0.75 when the
market is hot and repair risk is known, 0.65 in a slow market or when the scope is
uncertain. **The system uses 0.70 on every deal.** The range exists only so you can
read a deal honestly when it sits on the boundary — it is not a dial to turn to make
a bad deal pass.

```
HOT  / scope known     0.75   -> a deal at 0.75 is real, but the buyer's margin is thin
STANDARD               0.70   -> every number this repo prints
SLOW / scope uncertain 0.65   -> a deal that only clears at 0.65 is not a deal yet
```

When an offer only clears at 0.75, say so and say the cap used was 0.70. Never
quote a 0.75 number as if it were the standard.

## Step 2 — buyer max contract price

`(ARV × 0.70) − repairs − buyer costs not already inside the 70%`.

Additional buyer costs to consider: closing costs, financing, holding costs, resale
costs, other buyer expenses.

**The arithmetic trap, and how this system resolves it.** The 70% rule is conventionally
"70% of ARV covers purchase + repairs + costs + profit". Subtracting repairs *and* a
full cost load from 70% therefore risks double-counting. There are exactly two honest
ways to do it, and the report must state which one it used:

- **Mode A — repairs inside the 70%** (the standard convention, and this system's
  default): buyer max = `(ARV × 0.70) − repairs`. The buyer's profit, closing, holding
  and resale are all assumed to live inside the remaining 30%.
- **Mode B — repairs and costs both deducted**: buyer max =
  `(ARV × 0.70) − repairs − buyer costs`. Only use this when you have a real cost
  figure, and say plainly that it is the more conservative of the two and why you
  chose it.

Never mix modes inside one report, and never deduct a cost twice. Where a cost cannot
be verified, name the omission and show the effect with a sensitivity line.

## Step 3 — seller-facing MAO

`buyer max − assignment fee − additional wholesaler costs`.

This is the highest price you can pay the seller and still keep the deal inside the
assumptions. It is a **ceiling**, not an offer, and not a prediction that the seller
will accept it.

## Step 4 — opening offer

Below the MAO, with a stated reason. The MAO is where you stop, not where you start.

Report: the opening offer · the MAO · the gap between asking and MAO · the negotiation
room · whether the asking price looks negotiable (DOM, reductions, as-is language,
estate) · whether the deal is realistically attainable.

**A number being below asking does not make an offer viable.** A seller needing
$95,000 against a $12,500 MAO is a rejection, not a negotiation.

## Step 5 — buyer gross spread

`ARV − contract price − repairs`.

Show it, then say: this is a **gross spread, not net profit**. It does not include
resale commission, closing costs, holding costs (taxes, insurance, utilities, loan
carry), financing points, or taxes. A credible net estimate is asked for separately
and labelled `ESTIMATED`.

## Step 6 — assignment fee

Show: proposed fee · buyer max · seller MAO · opening offer · expected gross spread ·
costs that could still move the economics.

The fee is the **last** variable, never the first. Lower the offer before lowering
the fee; lower the fee before telling a buyer an unrealistic number. A smaller fee on
a deal that closes beats a large fee on a deal that dies.

## Worked check — required arithmetic

```
ARV $200,000 · 70% ceiling $140,000 · repairs $25,000 · buyer costs $0
fee $10,000 · wholesaler costs $0

buyer max contract        = $140,000 − $25,000        = $115,000
seller-facing MAO         = $115,000 − $10,000        = $105,000
buyer gross spread at $105,000 = $200,000 − $105,000 − $25,000 = $70,000
```

`$70,000` is the simplified **gross spread**, not net profit. `underwrite.py --selftest`
asserts exactly these three figures; if it ever fails, the model changed and every
number downstream is suspect.

## RealVenture buy box — guideline, not commitment

| Item | Value |
|---|---|
| Buyer pricing ceiling | ~70% of ARV |
| ARV range | $125,000 – $900,000 |
| Types | SFR, duplex, multifamily |
| Condition | Any |
| Terms | Cash or seller financing may be acceptable |
| Close | ~21–30 days |
| Comps required | Five |

**Types means real property only.** `SFR / duplex / multifamily` excludes manufactured and
mobile homes on leased land, park models, condos and co-ops. A manufactured home sitting on
*owned* land may qualify as an SFR — verify the land is in the sale (`sqft lot` is populated)
before treating it as one.

### Run the buy-box screen FIRST

Order matters, and it is cheapest-first:

1. **Type** — real property in the buy box?
2. **ARV band** — can this clear $125,000?
3. **Condition** — is there a spread to capture?
4. *Then* comps.

A property failing step 1 never reaches `comp.py`. Refusal notes should name the buy-box line
that failed, not the comp gap — otherwise the note invites someone to go build a pool that was
never going to matter (D-19).

### The `$/sf` repair tiers collapse on low-basis assets

`light $20 / moderate $35 / heavy $50` per sf was calibrated on $120–$180/sf SFRs. Check
`ARV/sf` before using it:

| ARV $/sf | tier validity |
|---|---|
| ≥ $100/sf | behaves as calibrated |
| $60–100/sf | overstates repairs; needs a walkthrough scope |
| < $60/sf | **invalid — refuse to price** |

At $55/sf, "light" repairs of $20/sf are 37% of value. The engine emits a number anyway.
That gate is applied by hand, before the first `--tier` call on an unfamiliar market (D-18).

Never state or imply that a buyer has approved a deal unless that approval was
received. "Fits the stated buy box" is the strongest claim available without a
specific buyer's written interest.

## Comp traps — verified the hard way, 2026-11-08 (Dayton)

These four patterns all produced a *plausible* ARV that was wrong. Check each one
before a comp set is accepted.

**1. New construction is not renovation.** In 45406 the 2025-built homes at
2047 / 2052 / 2062 / 2068 Ravenwood Ave sold for $119–$121/sf against a
renovated-band of $85–$138/sf. They are Montgomery County Land Bank
"Welcome Home Ohio" builds — a different product with a new-build warranty,
sold under an income-eligibility programme. Including them lifts ARV by roughly
37%. Tag them `exclusion=new_build`; the engine already drops them.

**2. The nearest sale is often the condition floor, not the ARV.** 2233 Deering
Ave sits 116 feet from a 45406 subject, the same size, and sold for $96,000 —
$69.51/sf. It is a dated 1952 with original wood floors. Distance makes a sale
*relevant*, never *equivalent*. Read the listing copy for condition words
before it enters the pool: "original", "vintage", "dated", "bring it back to
life", "as-is" all mean floor. Only "renovated", "remodeled", "updated
throughout", "new kitchen and baths", "move-in ready" qualify for ARV.

**3. A low $/sf can mean a solid house, not a distressed one.** 21 S Philadelphia
St (45403) closed $115,000 for 1,700 sf = $68/sf, described as "100% move-in
ready" with a brand-new roof. That is below nearly every neighbouring sale. A
single such comp drags the median and blows the spread out (31.4% on 3206 E 5th
St). When one comp sits far below the rest, check whether it is simply the
cheapest *good* house — that is market evidence, not an error, and it belongs in
the pool while the spread is reported honestly.

**4. ZIPs split by condition before they split by geography.** 45406 dated stock
trades $61–$76/sf; updated stock trades $85–$138/sf. 45410 splits geographically
instead — Walnut Hills versus Hearthstone/Oakland 1.6 mi east, with almost no
cross-over. Price a ZIP's submarket, never the ZIP average, and never borrow
comps across a split.

**Never** widen the radius, average a short set, or reinstate an outlier to
manufacture the third comp. `UNPRICED` plus an explicit sensitivity band is the
honest answer, and it is what `comp.py` refuses to do anything else about.
