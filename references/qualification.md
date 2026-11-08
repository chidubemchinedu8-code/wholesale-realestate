# Qualification gate, verdict, and report

## 1. The fifteen-point gate

Every property is checked, in order. Each check has a code so the ledger can tally
rejections without prose.

| # | Check | Code |
|---|---|---|
| 1 | Within an intended market and property type | `G01_market` |
| 2 | Listing or ownership information credible | `G02_credible` |
| 3 | Asking price potentially negotiable | `G03_negotiable` |
| 4 | Evidence of an actual discount opportunity | `G04_discount` |
| 5 | Five credible sold comps | `G05_comps` |
| 6 | ARV supported by those comps | `G06_arv` |
| 7 | Repair estimate defensible | `G07_repairs` |
| 8 | Buyer-side arithmetic works | `G08_buyer` |
| 9 | Seller MAO leaves room for the fee | `G09_mao` |
| 10 | Asking at or below MAO, or a credible negotiation path | `G10_path` |
| 11 | Buyer spread sufficient after other costs | `G11_spread` |
| 12 | Condition verifiable adequately | `G12_condition` |
| 13 | Current photos or a walkthrough obtainable | `G13_photos` |
| 14 | Timeline realistic (21–30 day close) | `G14_timeline` |
| 15 | Title, occupancy, access, legal, other due-diligence concerns clear enough | `G15_dd` |

Any `FAIL` on 5, 6, 7, or 8 means the property cannot be `STRONG`, whatever else
passes. Gaps on 12–15 cap it at `POTENTIAL`.

## 2. The three verdicts

**STRONG OPPORTUNITY** — all fifteen pass. Evidence supports the valuation, the deal
works under conservative underwriting, there is a credible path to contract, buyer
economics are attractive, and the major unknowns are manageable. Still says what a
walkthrough could change.

**POTENTIAL OPPORTUNITY** — promising, but one or more important facts are unverified.
Names exactly which gate codes are open and what closes each one. **Not submittable.**

**REJECT** — the numbers do not work, the discount is insufficient, the comps are weak,
repair risk destroys the margin, the seller is unlikely to reach the required price,
it is retail-priced or turnkey without a compelling discount, or the information is too
incomplete to underwrite. **Always states which of those.**

A rejection is a successful outcome. It costs a phone call and saves a contract.

## 3. Verdict matrix

| Condition | Verdict |
|---|---|
| <5 comps, or ARV unsupported | REJECT (`G05`/`G06`) — cannot submit |
| 5+ comps but seller MAO < 80% of asking | REJECT (`G10`) unless DOM/reductions prove movement |
| MAO < asking but seller has 90+ DOM and 2 reductions | POTENTIAL — a negotiation path exists |
| Deal works but no interior photos | POTENTIAL (`G12`/`G13`) |
| Deal works, 5 tight comps, photos complete, agent responsive | STRONG |
| Repairs unknown and the deal only works at the low end | POTENTIAL (`G07`) |
| REO/bank-owned | Excluded from results; list separately, unverdict |

## 4. Numbers to quote in the verdict

- Asking, working ARV, repair range, buyer max, seller MAO, opening offer, gross spread
- MAO as a percentage of asking — the single most useful rejection figure
- The fee at the MAO, and whether it survives

## 5. Required report — sixteen sections, in this order

**A. Property identification** — address · city, ZIP · listing URL · source · asking ·
status · DOM · reductions and dates · type · beds/baths · living area · lot size.

**B. Why it was selected** — the specific, evidenced opportunity. Not "good
potential". Name the signal: 361 DOM with zero reductions at 116% of the ZIP's
renovated $/sqft; estate sale, as-is, cash-only, 11 DOM.

**C. Condition assessment** — photo observations · classification (turnkey / light /
medium / heavy / unknown) · what the photos show · what is inferred · what cannot be
confirmed remotely · major risks · unknowns.

**D. Comparable sales** — five comps in a table with every required field from
`comps.md`, including URL, distance, condition at sale, why comparable, differences,
and verified-vs-reported. State any radius expansion and why.

**E. Valuation** — supported range (low / working / high) · working ARV · which comps
drove it · which were down-weighted and why · confidence · what could materially move
it.

**F. Underwriting** — every line separately: ARV · 70% screening ceiling · repairs ·
additional buyer costs (and whether Mode A or B) · buyer max contract · assignment fee
· wholesaler costs · seller MAO · asking · opening offer · expected gross spread ·
costs not yet confirmed.

**G. Deal verdict** — STRONG / POTENTIAL / REJECT · reasons · the gate codes that are
open · what must be verified next · recommended next action.

**H. Remote due diligence** — the named person or source for current photos, video
walkthrough, access, or documents, and what to ask them for.

**I. Provenance table** — claim / value / label / source URL / date checked.

**J. Estimator's note** — what this report is not: not an appraisal, not an offer, not
an inspection, not buyer approval.

## 6. Report header

```
DEAL REPORT — 141 Grand Ave, Akron OH 44302
Report date: 2026-11-08 · Market: Akron OH · ZIP priority: A (78)
Verdict: REJECT · Confidence in verdict: HIGH
ARV $125,000 (MEDIUM, n=5, 0.5 mi, 44302) · Repairs $55K–$75K (ESTIMATED, photos)
Buyer max $12,500 · Seller MAO $2,500 · Asking $95,000 (MAO = 3% of asking)
```

That header alone tells the operator not to make the call. That is the point of the
format.
