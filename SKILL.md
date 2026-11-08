---
name: wholesale-realestate
version: 2.2.0
description: Use when any task involves US real estate wholesaling - finding investment properties, scanning Zillow/Redfin/PropWire, evaluating a property, estimating ARV or repairs, pulling comparable sales, calculating buyer maximum or seller MAO, preparing an offer, assigning a contract, or deciding whether a deal is worth pursuing
---

# Wholesale Real Estate — Sourcing and Underwriting

The single operating standard for US wholesale real estate. The repository is the
source of truth; this file is the entry point and `references/` is the detail.

**Core principle:** every number carries a source and a date, or it is `UNKNOWN`.
`UNKNOWN` stops the analysis. It never gets filled in to make a deal pass.

## Preflight — required before any sourcing or underwriting

```bash
bash scripts/preflight.sh
```

It verifies every file is present, prints the version, and runs all six script
selftests. If it fails, **STOP** and report exactly what is missing. Do not fall
back to generic property browsing, and do not work from memory of this file.

Then read the reference for the step you are on. Do not work from memory; the
references are the detail and they change.

| Step | Reference |
|---|---|
| ZIP research, ranking, scan bookkeeping | `references/market-research.md` |
| On-market scan (**Zillow primary, Redfin cross-check**) | `references/on-market.md` |
| Off-market scan (PropWire / county GIS) | `references/off-market.md` |
| Comps to the five-comp standard | `references/comps.md` |
| Photos and condition | `references/condition.md` |
| Repairs | `references/repairs.md` |
| Buyer ceiling, buyer max, seller MAO, fee | `references/underwriting.md` |
| Qualification gate, verdict, report format | `references/qualification.md` |
| Labels, provenance, anti-hallucination | `references/data-integrity.md` |
| Licensing, MLS/RESO routes, buying data | `references/data-access.md` |
| Deeper comp arithmetic (neighbourhood gate, radius ladder) | `comping/COMPING.md` |

## The pipeline

```
ZIP priority  ->  on-market scan  ----\
                                      >--  shortlist  ->  photos  ->  comps
              ->  off-market scan  --/                                 |
                                                                       v
                        repairs  ->  underwriting  ->  15-point gate  ->  verdict
```

Each stage can end the deal. A property never reaches underwriting without a
condition classification and a repair range.

## The scripts

| Script | Enforces |
|---|---|
| `scripts/preflight.sh` | The skill is intact and current — run it first |
| `scripts/rank_listing.py` | DOM/reduction priorities, the 14-day rejection |
| `scripts/comps.py` | Five-comp rule; no ARV under five |
| `scripts/comp.py` | ARV: neighbourhood gate, bed floor, renovated-only, consistency gate, radius ladder, LOW/POINT/HIGH × 0.88 |
| `scripts/anchor.py` | ZIP/neighbourhood median $/sf anchor, and bimodal detection |
| `scripts/underwrite.py` | Buyer max ≠ seller MAO; the $200K check |
| `scripts/zip_ledger.py` | What was scanned, and the duplicate guard |
| `scripts/gate.py` | The 15-point gate, mechanically |

Each has `--selftest`, and each selftest must pass before a number is quoted.

## Hard rules

1. **Verify the subject across four sources** — public records win on hard facts (beds, baths, sqft, year), MLS/agent remarks win on condition. State conflicts; never silently pick one.
2. **Five comps or no ARV.** Fewer than five credible sold comps means `ARV INSUFFICIENTLY SUPPORTED`, and the property is not a submission.
3. **No comp below the subject's bed count.** A 3-bed subject takes 3-bed-and-up only, no matter how good the $/sqft match.
4. **The ARV pool is renovated-condition only.** Dated, distressed, auction and unknown-condition sales inform the as-is floor — never the ARV number.
5. **The consistency gate never reinstates an outlier.** A price > ±45% from the comp-set median is dropped; if that leaves under 3, the answer is unpriced.
6. **Same ZIP or immediate neighbourhood first.** Expand only when needed, state why, and never force weak comps to reach a count.
7. **Active listings are never comps.** Only closed sales.
8. **Photos classify; descriptions do not.** Separate what is shown, what is inferred, and what cannot be confirmed remotely.
9. **Repairs are a range plus a contingency** unless an inspection or bid exists.
10. **Buyer max and seller MAO are different numbers.** Buyer max = `(ARV × 0.70) − repairs`. Seller MAO = buyer max − fee − wholesaler costs.
11. **Gross spread is not profit.** Say so every time it appears.
12. **RealVenture's buy box is a guideline, not a commitment.** No buyer has approved anything until that buyer says so.
13. **Report zero if zero qualify.** A ZIP with nothing is an honest result.
14. **No REO/bank-owned in normal results.** Separate channel, on request.
15. **New listings (<14 days) rejected by default** unless documented mispricing.
16. **A previously scanned property is not a new opportunity.** Check the ledger.
17. **Stop on missing evidence.** Unverified title, occupancy, access or structure caps a property at `POTENTIAL`.
18. **Never invent.** Address, URL, sold price, date, sqft, beds, DOM, owner, phone, equity, motivation, repair observation, buyer approval.
19. **Licensed data prices deals, it does not find them.** NAR model rules §4.4.1 forbid using MLS data for business solicitation, so no MLS licence can be a sourcing engine. Sourcing = county records + public sites + investor data. Valuation = licensed MLS. Never cross the line.
20. **Zillow is the primary manual discovery reference; Redfin is a secondary cross-check.** Neither is licensed data. Two portals agreeing is not verification — see `references/data-access.md`.
21. **UNKNOWN is never a pass.** A missing bed count, condition, location or address suffix does not satisfy a rule — it fails it. Excluding a comp for missing data is correct; admitting it is guessing.
22. **Whatever narrows the comp pool must be printed.** A filter that changes the ARV without appearing in the report is an invisible decision. Style, radius, condition, bed floor and consistency band all name their effect and their count.
23. **The buyer's ceiling is not the seller's MAO.** `BUYER MAX = (ARV x 0.70) - repairs`; seller MAO = buyer max - fee - wholesaler costs. Never label the first one MAO. A non-positive MAO is not a thin deal, it is no deal — refuse, do not format it.
24. **The arithmetic is unvalidated.** Every rule here is internally consistent and none has been checked against a real outcome. Say so before anyone stakes money on a number. See `AUDIT.md`.

## Red Flags

Each of these has already cost real money in this workflow.

| Thought | Reality |
|---|---|
| "It's cheap, so it's a deal" | Cheap in a $100K-ARV ZIP is a trap. The ratio to ARV decides |
| "That ZIP is close enough" | 44303 3-beds sell $200–255K; 44302 sells $74–120K. Same city, 2× |
| "I'll use the Zestimate as ARV" | An anchor for an off-market record, never a comp |
| "That AMI-restricted sale is a comp" | It is a floor. Using it understated a real deal by $20,000 |
| "Asking prices support the ARV" | This inflated one ARV by 85% |
| "I only found 3 comps" | Then there is no ARV. Say so |
| "4 comps is basically 5" | Then it is not a submission. The buyer pulls their own |
| "The spread is $70K, that's profit" | Gross. Commission, closing, holding, financing are not in it |
| "Buyer max is my offer" | Buyer max is the cap. Your offer is below your MAO |
| "Fee first, then see if it works" | Lower the offer, never inflate the fee |
| "Zillow filters didn't apply, so Zillow is unusable" | Its filters fail; its property pages work. Zillow is the primary discovery reference |
| "Redfin confirmed it, so it's verified" | Two portals repeating one feed is not a second source. Licensed MLS is |
| "I'll buy MLS data and use it for seller outreach" | NAR §4.4.1: MLS data may not be used for business solicitation. It prices deals, it does not find them |
| "No same-ZIP comps, use the next ZIP" | Then say the ARV is unsupported. Do not borrow a submarket |
| "Photos look fine so the roof is fine" | Photos cannot prove a roof, foundation, wiring, plumbing |
| "I'll fill the empty columns later" | `UNKNOWN` is the answer. Later never comes |
| "Six is better than zero, the client wants options" | Padding the report is the failure, not the empty ZIP |
| "The listing says updated" | Agent copy is a claim. The photo is the evidence |

## Output contract

Every shortlisted property gets the report in `references/qualification.md` §5 —
sixteen sections, all filled or marked `UNKNOWN`. Every factual claim carries
`VERIFIED` / `REPORTED` / `ESTIMATED` / `ASSUMED` / `UNKNOWN`, a source URL, and
the date checked.

Every report ends with `STRONG OPPORTUNITY`, `POTENTIAL OPPORTUNITY`, or `REJECT`,
and one sentence naming what would change it.

## Bookkeeping

```bash
python3 scripts/zip_ledger.py --list      # what was scanned, when, what it produced
python3 scripts/zip_ledger.py --due       # which ZIPs are owed a re-scan
```

**Ledgers are committed and append-only.** `state/zip_ledger.csv` and
`state/property_ledger.csv` are version-controlled on purpose: a fresh clone must
inherit the scan history, or the duplicate guard resets and old properties get
re-reported as new finds.

- **Never delete a row.** Update it in place (price change, status change, new verdict).
- **Never rewrite history** to make a report look tidier.
- **Never re-report a `SEEN` property as a new opportunity.** Report it as `SEEN`
  with its first-seen date and what changed.
- A property that comes back on market, or drops price, is a legitimate re-surface —
  log the change and say what changed.

`assets/zip_universe.csv` is the committed *plan*: markets, ZIPs, scores and the
evidence behind each. `state/` is the *history*: what was actually scanned and what
it produced. Keep them separate; the universe file is not a scan log.

## Markets and operating reality

Six markets only: Cleveland OH, Akron OH, Columbus OH, Dayton OH, Birmingham AL,
Atlanta GA. Only Akron and Cleveland have seeded ZIPs; the other four have no
evidence yet and must not be scored until researched.

The seller operates remotely from Nigeria, so every property needs a named path to
current photos or a walkthrough before it can be `STRONG`.

## The rest of the workflow

Sourcing and underwriting are the front of the deal. The later stages live below,
and they use the numbers this standard produces:

- **Stage 4 — the offer.** Open at `OFFER LOW` (55% of ARV − repairs), never above
  `OFFER HIGH` (60%). The room to negotiate is the 55→70% friction, which already
  exists. Offer script and PSA checklist follow.
- **Stage 5 — end buyer and assignment.** Assignment fee = end buyer price −
  contract price. The assignment agreement must reference the original contract.
- **Stage 6 — close.** Title company, title search, proof of funds, signed
  assignment, disbursement review, fee collected at closing.

---

## Stage 4: Make the Offer

```
"Hi [Seller], based on what the home needs and what similar homes
are selling for in the area, I can offer you $[OFFER] cash, as-is,
close in [14–21] days, no commissions, no contingencies.

Would that work for you?"
```

**Negotiation anchors**
- Open at `OFFER LOW` (55% of ARV − repairs); never open above `OFFER HIGH` (60%).
- Emphasise speed, certainty, and no repairs.
- If the seller counters high: "What's the lowest you'd go to close quickly?"

**Purchase and Sale Agreement checklist**
- Property address and legal description
- Purchase price = your offer
- Earnest money ($500–$2,000 typical)
- Due diligence period (7–14 days)
- **Assignment clause: "and/or assigns"** — critical
- Closing date
- As-is clause

## Stage 5: End Buyer and Assignment

**Where buyers come from:** your list · local REIA · "We Buy Houses [City]" groups ·
BiggerPockets · Craigslist "Real Estate Wanted" · co-wholesaling.

```
Assignment fee = end buyer's purchase price − your contract price
```

The assignment agreement must reference the original contract, name assignor and
assignee, state the fee, and transfer all rights and obligations.

## Stage 6: Close

- [ ] Investor-friendly title company selected
- [ ] Title search ordered — no liens beyond the seller's mortgage
- [ ] End buyer has proof of funds or hard money approval
- [ ] Assignment agreement signed and delivered to title
- [ ] Closing date confirmed with all parties
- [ ] Assignment fee collected at closing
- [ ] Disbursement sheet reviewed before signing

**Post-close:** add the buyer to your list with their criteria · thank the seller ·
log the deal (address, ARV, repairs, sale price, fee, close date) · review what
worked.

## Key formulas

| Formula | Equation |
|---|---|
| CEILING (max pay) | ARV × 0.70 − Repairs |
| OFFER LOW / HIGH | ARV × 0.55 / × 0.60 − Repairs |
| FRICTION | CEILING − OFFER HIGH (10–15% of ARV) |
| CONTRACT | CEILING − Fee (deducted once) |
| Buyer max contract | (ARV × 0.70) − Repairs − buyer costs |
| Seller-facing MAO | Buyer max − assignment fee − wholesaler costs |
| Buyer gross spread | ARV − Contract − Repairs (gross, not profit) |
| Subject ARV | Sqft × p75 $/sqft × 0.88 (see `references/comps.md`) |
| As-is value | Sqft × p25 $/sqft × 0.88 |
| Assignment fee | End buyer price − contract price |

## Quick commands

- User gives deal numbers → run `scripts/underwrite.py`, output CEILING, the
  55–60% range, and the deal scorecard. Never present a ceiling as an offer.
- User says "I have a deal" or names an address → Stage 1 qualification, then the
  pipeline above.
- User says "find deals in [city]" → `references/market-research.md` first, then
  scan ranked ZIPs only.
