---
name: wholesale-realestate
description: Full wholesale real estate workflow — search for deals in a city/area, analyze numbers (ARV by comps, ceiling, repair costs), make an offer, and close/assign the contract. Use when user mentions wholesaling, finding deals, searching for properties, making offers, assigning contracts, or asks about real estate investment analysis.
tools: Read, Write, Glob, Grep, Bash, WebSearch, mcp__plugin_context-mode_context-mode__ctx_fetch_and_index, mcp__plugin_context-mode_context-mode__ctx_search, mcp__plugin_context-mode_context-mode__ctx_batch_execute
---

# Wholesale Real Estate — Full Workflow

Guide the user through every stage of a wholesale real estate deal from lead to close.

> **Read `comping/COMPING.md` before quoting any value.** It is the binding comp/ARV
> standard (derived from the `superpowers` → `leadgen` work and its three ARV
> corrections), and `comping/comp.py` is the executable version. Where this file and
> that standard disagree, the standard wins.

---

## Stage 0: Deal Finder (Search by City / Area)

**Trigger:** User says "find deals in [city]", "search [area]", "what's available in [zip/city]", or similar.

### Step 1 — Collect search parameters

Ask the user:
```
City or area to search:
Property types (SFR, multi-family, both):
Max price (leave blank for no limit):
Min bedrooms (default: 2):
Any specific zip codes or neighborhoods? (optional):
```

### Step 2 — Run motivated-seller searches

Use **WebSearch** with the following query patterns (substitute user's city/area):

```
Motivated seller search queries to run in parallel:

1. site:zillow.com "[CITY]" "price reduced" "as-is" -agent
2. site:craigslist.org "[CITY]" "motivated seller" OR "must sell" OR "as-is" real estate
3. site:redfin.com "[CITY]" "fixer" OR "TLC" OR "as-is" "days on market"
4. "[CITY] foreclosure listings" OR "[CITY] pre-foreclosure homes for sale"
5. "[CITY] tax delinquent property list [YEAR]" OR "[CITY] tax lien properties"
6. site:facebook.com "marketplace" "[CITY]" "we buy houses" OR "FSBO" OR "cash only"
7. "[CITY] probate real estate listings" OR "[CITY] estate sale homes"
8. "[CITY] absentee owner properties for sale"
```

Run at minimum queries 1, 2, 3, and 4. Run all 8 for a thorough search.

### Step 3 — Fetch and index promising results

For each promising URL found in search results, use `ctx_fetch_and_index(url, source)` to pull the full listing details. Label the source as `"deal-[address]"` so results can be searched later.

### Step 4 — Score and filter leads

For each property found, score it on the **Motivated Seller Score (MSS)**:

| Signal | Points |
|--------|--------|
| Listed as "as-is" or "fixer" | +2 |
| Price reduced (any reduction) | +2 |
| DOM > 60 days | +2 |
| DOM > 90 days | +3 |
| Listed below estimated ARV by >30% | +3 |
| Foreclosure / pre-foreclosure | +3 |
| Probate / estate sale | +2 |
| Tax delinquent | +3 |
| FSBO (no agent) | +1 |
| Vacant / abandoned indicator | +2 |

**Score thresholds:**
- 8+ points → Hot Lead (pursue immediately)
- 5–7 points → Warm Lead (worth investigating)
- < 5 points → Skip

### Step 5 — Present results table

Output a ranked table of the top leads found:

```
## Deal Finder Results — [CITY/AREA]
Search date: [today's date]

| # | Address | Price | Est. ARV | Est. Repairs | MSS | Status | Source |
|---|---------|-------|----------|--------------|-----|--------|--------|
| 1 | ...     | $...  | $...     | $...         | 10  | Hot    | Zillow |
| 2 | ...     | $...  | $...     | $...         | 7   | Warm   | CL     |
...

Hot Leads: X | Warm Leads: Y | Total found: Z
```

For ARV and repair estimates, use neighborhood price data from search results and apply conservative estimates (note they are estimates until comps are run).

### Step 6 — Offer next action

After presenting results, ask:
```
Which property would you like to dig deeper on?
→ Type a number to run full deal analysis (Stage 2 onward)
→ Type "search more" to expand the search
→ Type "export" to save results to a file
```

If user says **"export"**, write the results table to `wholesale-leads-[CITY]-[DATE].md` in the current directory.

If user picks a property, automatically continue to **Stage 2** (Deal Analysis) with that property pre-filled.

---

## Stage 1: Qualify an Existing Lead

Ask the user for the property address or lead source, then help them qualify the lead.

**Motivated Seller Checklist:**
- Distressed property (visible repairs, code violations, tax liens)?
- Owner situation: divorce, probate, foreclosure, out-of-state landlord, tired landlord?
- Days on market (DOM > 90 = motivated)?
- Asking price vs. estimated ARV?

**Lead Sources to suggest if user has no deal yet:**
- Driving for dollars (Propstream, DealMachine)
- Direct mail (tax delinquent lists, absentee owners)
- MLS — expired/cancelled listings
- Bandit signs, Facebook Marketplace FSBO, Craigslist
- Probate court records, foreclosure auction lists

---

## Stage 2: Analyze the Deal

Collect the following inputs from the user, then calculate the offer.

### Inputs to Gather
```
Property address:
Bedrooms / Bathrooms / Sqft:
Year built:
Estimated ARV (After Repair Value): $
Estimated repair costs: $
Your wholesale fee target: $
End buyer's desired profit margin (default 20%):
Holding/closing costs estimate (default 10% of ARV):
```

### Ceiling Formula (the most you may pay)
```
CEILING      = ARV × 0.70 − Repairs          # cap. Fee NOT deducted here
OFFER LOW    = ARV × 0.55 − Repairs          # open here
OFFER HIGH   = ARV × 0.60 − Repairs          # never open here
FRICTION     = CEILING − OFFER HIGH           # 10–15% of ARV — this is the room
CONTRACT     = CEILING − Wholesale Fee        # buy at this to make the fee

Example (ARV $200,000, repairs $30,000, fee $10,000):
  × 70%:        $140,000  − repairs  → CEILING     $110,000
  × 55%:        $110,000  − repairs  → OFFER LOW    $80,000
  × 60%:        $120,000  − repairs  → OFFER HIGH   $90,000
  FRICTION (55% → 70% of ARV):                       $20,000
  CEILING − fee                      → CONTRACT    $100,000
```

**70% is a cap, 55–60% is a target under the cap, and the gap is the pay stack.**
**Never deduct the fee twice** — it comes off once, at the contract step. The old
`MAO = ARV × 0.70 − Repairs − Fee` formula double-charges it, and starting at MAO−10%
puts the opening offer below 55% of ARV with repairs already removed.

Verify any numbers with `python3 comping/comp.py --offer <ARV> --repairs <graded>`.

### Deal Scorecard
| Metric | Value | Pass? |
|--------|-------|-------|
| Contract ≤ CONTRACT target | | ✅ / ❌ |
| ARV from comps, with n / radius / confidence | | ✅ / ❌ |
| Repairs graded (not guessed) | | ✅ / ❌ |
| End buyer identified | | ✅ / ❌ |
| Assignment fee ≥ $5,000 | | ✅ / ❌ |

Output the completed scorecard and state whether the deal passes.

---

## Stage 3: Run Comps (ARV Estimation)

**The rule lives in `comping/COMPING.md`; run it with `comping/comp.py`. It is not a judgement call.**

```
ARV = subject_sqft × p75($/sqft of ≥3 arm's-length closed sales, SAME neighbourhood,
      ≤1.5 mi, inside 6–12 months, ±30% sqft) × 0.88
```

**Ladder, in this order:** identical neighbourhood code → ±30% sqft band → radius
`0.25 → 0.50 → 0.75 → 1.00 → 1.25 → 1.50` mi, using the *smallest* radius with **≥3**
comps → style preference when ≥3 share it. **Under 3 comps at 1.50 mi → `NO COMPS`,
unpriced. Do not widen, do not average, do not fall back to a ZIP band.**

**Excluded from ARV** (keep as a floor only, and say so): deed-restricted / AMI sales,
newer builds, condos, non-arm's-length transfers, and every asking price. Asking prices
are not comps — using them is what inflated 141 Grand Ave by **85%**. ZIP ≠ neighbourhood:
44303 three-beds sell $200K–$255K, 44302 three-beds sell $74K–$120K.

**Confidence** is `HIGH` at n ≥ 6, `LOW` below that. Report `n`, radius, neighbourhood
and confidence with every number, or the number is not reportable.

**Never report a single point estimate without its skeleton**, and label it
`ESTIMATE — not an appraisal, not an offer`. `UNPRICED` is a complete answer.

**Run it:**
```bash
python3 comping/comp.py --selftest        # prove the 6 checks can fail
python3 comping/comp.py --exclusions      # the not-a-comp list
python3 comping/comp.py --comps comping/fixtures/akron_44302_worked_example.csv \
  --as-of 2026-10-31 --repairs 65000 \
  --subject '{"address":"141 Grand Ave","sqft":1642,"hood":"44302","lat":41.079,"lon":-81.536,"style":"COLONIAL"}'
```

**If user has no comps yet**, pull closed sales from MLS-sourced data (Redfin
`include=sold-6mo`, Zillow property pages, Realtor.com), or Propstream/BatchLeads for
off-market, or ask a local agent for a CMA. Zillow's ZIP-level *filters* are unreliable;
its property pages are fine. A Zestimate is an **anchor for off-market records only** —
never a comp, never blended with an ARV.

---

## Stage 4: Make the Offer

### Offer Conversation Script
Present this to the user to use with the seller:

```
"Hi [Seller], based on what the home needs and what similar homes
are selling for in the area, I can offer you $[OFFER] cash, as-is,
close in [14–21] days, no commissions, no contingencies.

Would that work for you?"
```

**Negotiation anchors:**
- Open at `OFFER LOW` (55% of ARV − repairs) and never above `OFFER HIGH` (60%).
  The room to negotiate up is the 55→70% friction, which already exists — do not
  manufacture more by discounting below the low anchor
- Emphasize speed, certainty, and no repairs needed
- If seller counters high, ask: "What's the lowest you'd go to close quickly?"

### Purchase and Sale Agreement checklist
- Property address (legal description)
- Purchase price = your offer
- Earnest money deposit (typically $500–$2,000)
- Inspection / due diligence period (7–14 days)
- **Assignment clause**: "And/or assigns" after buyer's name — CRITICAL
- Closing date
- As-is clause

---

## Stage 5: Find an End Buyer & Assign the Contract

### End Buyer Sources
- Your existing cash buyer list
- Local REIA (Real Estate Investor Association) meetings
- Facebook Groups: "We Buy Houses [City]", local investor groups
- Bigger Pockets forums
- Craigslist "Real Estate Wanted" section
- Other wholesalers (co-wholesale)

### Assignment of Contract
```
Assignment Fee = End Buyer's Purchase Price − Your Contract Price

Example:
  Your contract:    $100,000
  End buyer pays:   $110,000
  Your fee:         $10,000
```

**Assignment Agreement must include:**
- Original contract reference
- Assignor (you) and Assignee (end buyer) details
- Assignment fee amount
- End buyer takes over all rights and obligations

---

## Stage 6: Close the Deal

### Closing Checklist
- [ ] Title company / closing attorney selected (use investor-friendly title co.)
- [ ] Title search ordered — confirm no liens beyond seller's mortgage
- [ ] End buyer has proof of funds or hard money approval
- [ ] Assignment agreement signed and delivered to title
- [ ] Closing date confirmed with all parties
- [ ] Assignment fee collected at closing (wire or cashier's check)
- [ ] Disbursement sheet reviewed before signing

### Post-Close
- Add end buyer to your buyers list with purchase criteria
- Send thank-you to seller
- Track deal in your CRM: address, ARV, repair, sale price, fee, closing date
- Analyze: what went right / wrong for next deal

---

## Key Formulas Reference

| Formula | Equation |
|---------|----------|
| CEILING (max pay) | ARV × 0.70 − Repairs |
| OFFER LOW / HIGH | ARV × 0.55 / × 0.60 − Repairs |
| FRICTION | CEILING − OFFER HIGH (10–15% of ARV) |
| CONTRACT | CEILING − Wholesale Fee (fee deducted once) |
| Assignment Fee | End Buyer Price − Contract Price |
| Comp $/sqft | Comp Sale Price ÷ Comp Sqft |
| Subject ARV | Subject Sqft × p75 $/sqft × 0.88 (see Stage 3) |
| As-is value | Subject Sqft × p25 $/sqft × 0.88 |
| Net to Seller | Contract Price − Seller's Liens − Closing Costs |

---

## Quick Commands

When the user provides deal numbers, automatically run Stage 2 analysis and output the CEILING, the 55–60% offer range and the Deal Scorecard without asking for permission. Never present a ceiling as an offer.

When the user says "I have a deal" or provides an address, start at Stage 1 and walk through each stage sequentially, asking only for the inputs needed at each step.
