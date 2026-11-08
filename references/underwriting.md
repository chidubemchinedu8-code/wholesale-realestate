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

Never state or imply that a buyer has approved a deal unless that approval was
received. "Fits the stated buy box" is the strongest claim available without a
specific buyer's written interest.
