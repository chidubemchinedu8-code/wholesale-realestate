# Dayton — ARV for every named candidate (2026-11-08)

Every named candidate now carries either an **ARV** or a **stated reason there isn't one**.
Nothing is left blank.

Two strengths are used and they are never conflated:

- **STRICT** — n≥3 in-band renovated comps, ran through `scripts/comp.py`. Conforms to the rule.
- **INDICATIVE** — n=1 or 2. Same method, same arithmetic, **labelled and carrying its n**.
  Produced by `scripts/indicative_arv.py`, which refuses to report n≥3 as indicative.
  Re-run through `comp.py` the moment a third in-band sale exists.

`ARV = sqft x MEDIAN $/sf renovated in-band · BUYER MAX = (ARV x 0.70) - repairs · MAO = BUYER MAX - $10,000`

---

## 45405 — NORTH RIVERDALE (strict: 3 comps, $129.92/sf, spread 4.8%, TIGHT)

Pool `state/comps/dayton_45405_pointview_comps.csv` — 10 verified sales, 3 renovated:
44 E Beechwood $176,950/1,362 · 212 E Beechwood $155,000/1,294 · 258 E Siebenthaler $165,000/1,248

| Candidate | Ask | SF | ARV | Repairs (tier) | Buyer max | MAO | Verdict |
|---|---|---|---|---|---|---|---|
| 49 Pointview Ave | $59,900 | 1,778 | **$230,996** | $62,230 (mod) | $99,467 | $89,467 | **WATCH** — pending 15 mo, short sale. Backup $45–52k |
| 152 E Parkwood Dr | $39,900 | 1,240 | **$161,100** | $62,000 (heavy) | $50,770 | $40,770 | **MARGINAL** — ask is $870 under ceiling; agent-owned, cash-only |
| 2326 Parkland Ave | $65,000 | 1,248 | **$162,139** | $43,680 (mod) | $69,817 | $59,817 | **MARGINAL** — ask 8.7% over MAO; negotiable |
| 46 Pointview Ave | $85,000 | 1,388 | **$180,328** | $48,580 (mod) | $77,650 | $67,650 | **NO** — ask 26% over MAO |

## 45405 — FAIRVIEW (UNPRICED, and the reason is specific)

Pool would be 545 Gramont ($120.07) + 839 Dow ($124.53) — both renovated and in-band, but
**neither is in Fairview**, they are West Dayton / Dayton View. The Fairview sales that do
exist are all **updated, not renovated**, or fall outside the 180-day window:
214 W Fairview ($100,000, 2025-05-08), 217 W Norman ($138,500, 2025-08-11),
1046 Shakespeare ($78/sf, updated), 110 E Fairview ($78,000), 23 W Norman ($39,000).

| Candidate | Ask | SF | ARV | Verdict |
|---|---|---|---|---|
| 119 W Norman Ave | $80,000 | 1,681 | **UNPRICED** | Two live neighbouring listings at $80,000 (209 W Norman) against a street where 217 W Norman sold $138,500 in Aug 2025 and 204 W Norman $43,000 — a 3.2x spread in one street. Cannot price without knowing condition. |
| 209 W Norman Ave | $80,000 | 1,640 | **UNPRICED** | Same seller, same street, same problem. **Ask about a package price for both.** |
| 35 Santa Clara Ave | $84,900 | 1,680 | **UNPRICED** | 4-bed; Fairview has no renovated 4-bed sale in 180 days |

**Manual check that unblocks all three:** a renovated Fairview sale in the last 12 months.
50 Woodcrest (3bd, 1,500 sf, $155,000, 2026-05-01) is the closest candidate — **11 days outside
the window**. A renovation contract date on 214 W Fairview would also do it.

## 45402 — DAYTON VIEW / WEST DAYTON (indicative: 2 comps, $122.30/sf, spread 3.6%)

Pool `state/comps/dayton_45402_daytonview_comps.csv`. Three verified flips, all documented
buy-renovate-sell:
- **840 N Broadway** $50,150 (2022) → **$250,000** 2026-09-01 · $131.86/sf · 1,896 sf
- **839 Dow St** $65,000 (Nov 2024) → **$131,500** 2026-09-04 · $124.53/sf · 1,056 sf · permits Apr 2026
- **545 Gramont** $35,000 (Feb 2025) → **$140,000** 2026-09-04 · $120.07/sf · 1,166 sf · "Remodeled, Quartz"

| Candidate | Ask | SF | ARV | n | Repairs (tier) | Buyer max | MAO | Verdict |
|---|---|---|---|---|---|---|---|---|
| 817 Faulkner Ave | $50,000 | 1,430 | **$174,886** | 2 | $67,000 (heavy) | $55,420 | $45,420 | **MARGINAL** — ask $4,580 over MAO. Roof/siding/windows/electrical already done, so heavy is conservative and the finish work is still real |
| 624 N Broadway St | $85,000 | 2,302 | **$303,534** | 1 | $115,000 (shell) | $97,474 | $87,474 | **BEST ARITHMETIC IN THE SET** — ask $2,474 *under* MAO. But n=1 and repairs are a guess |
| 623 Anna St | $65,000 | 1,237 | **$151,282** | 2 | $68,000 (heavy) | $37,897 | $27,897 | **NO** — ask 2.3x MAO |
| 945 Vernon Dr | $86,999 | 1,266 | **$154,829** | 2 | $44,310 (mod) | $64,070 | $54,070 | **NO** — ask 61% over MAO |
| 3619 Hoover Ave | $99,900 | 1,056 | **$129,146** | 2 | $36,960 (mod) | $53,442 | $43,442 | **NO** — ask 2.3x MAO |

## 45403 — EAST DAYTON (strict: 3 comps, $105.41/sf, spread 19.2%, TIGHT)

Pool `state/comps/dayton_45403_e5th_comps.csv`.

| Candidate | Ask | SF | ARV | Repairs (tier) | Buyer max | MAO | Verdict |
|---|---|---|---|---|---|---|---|
| 141 S Torrence St | $74,900 | 1,458 | **$153,681** | $29,160 (light) | $78,417 | $68,417 | **BEST NEGOTIATION IN THE SET** — ask only 9.5% over MAO; all-brick, cosmetic only |
| 633 Huffman Ave | $44,900 | 1,683 | **$177,397** | $84,150 (heavy) | $40,028 | $30,028 | **NO** — $26.68/sf screams structural, and heavy repairs eat the deal |
| 237 N Irwin St | $74,900 | 1,246 | **UNPRICED** | — | — | — | ±30% band leaves under 3 renovated sales; tenant-occupied, landlord model anyway |

## 45404 — KOSSUTH COLONY / OLD NORTH DAYTON (indicative: 2 comps, $128.76/sf, spread 2.2%)

Pool `state/comps/dayton_45404_oldnorth_comps.csv`.
185 Grove $184,900/1,420 renovated 2026-10-29 · 34 Ingleside $165,000/1,296 flipped from
$58,000 in Dec 2025, sold 2026-10-09.

| Candidate | Ask | SF | ARV | n | Repairs (tier) | Buyer max | MAO | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1012 St Adelbert Ave | $105,000 | 1,200 | **$154,516** | 2 | $42,000 (mod) | $66,161 | $56,161 | **NO** — ask 87% over MAO |
| 1309 Leonhard St | $99,900 | 1,290 | **UNPRICED** | — | — | — | — | 4-bed; the two renovated comps are 3-bed, and the bed floor is absolute. Also 1 of 6 in a package |

## 45406 — (UNPRICED, verified)

| Candidate | Ask | SF | ARV | Verdict |
|---|---|---|---|---|
| 3395 Brumbaugh Blvd | $109,900 (cut from $124,900) | 984 | **UNPRICED** | Every in-band 45406 sale in 180 days is **updated or maintained** — zero renovated. Six comps, all excluded on condition. This is a real answer, not a gap. |

---

## What this changes about the earlier picture

**Three findings the ARV work surfaced that the listing sweep missed:**

1. **45402 is a real flip market and it was invisible in my earlier work.** Three documented
   buy-renovate-sells at $120–132/sf, all in the last 70 days, one of them 0.13 mi from Faulkner
   buying at $50,150 and selling at $250,000. 817 Faulkner and 624 N Broadway sit in that market.
2. **624 N Broadway has the best arithmetic of anything priced** — $303,534 ARV on 2,302 sf against
   an $85,000 ask. It is also the single least trustworthy number here: n=1, and "no mechanics,
   plumbing or electric on site" is a $115,000 assumption, not a quote.
3. **The Pointview MAO of $89,467 is the outlier, not the rule.** Most of this set fails the
   70% rule outright. That is the market telling you Dayton sub-$100k is priced about right.

## Manual verification list — what you can check that I cannot

| # | Property | What to confirm |
|---|---|---|
| 1 | 817 Faulkner | Interior scope. With roof/siding/windows/electrical done, is $67,000 right or is it $40,000? That single number swings MAO from $45,420 to $72,420. |
| 2 | 624 N Broadway | Confirm mechanics truly absent, and get a mechanical + electrical quote. n=1 ARV. |
| 3 | 152 E Parkwood | Interior condition. Agent-owned, cash-only, $39,900 — is it a light rehab or a heavy one? |
| 4 | 141 S Torrence | Confirm "cosmetic updates" really is cosmetic. This is the closest thing to a clean deal in the set. |
| 5 | 119 + 209 W Norman | Get a package price. Two houses, one seller. |
| 6 | 35 Santa Clara | Condition. Unpriced only because Fairview has no renovated 4-bed. |
| 7 | 2326 Parkland | Walk it. $65,000 against a $59,817 MAO is a $5,183 conversation. |
| 8 | 1309 Leonhard | Becomes priceable if it is really a 3-bed, or with a renovated 4-bed 45404 sale. |
| 9 | 3395 Brumbaugh | Unpriceable without a renovated 45406 comp. |

## Standing caveats

- Every repair figure is **graded from listing text, not an inspection**. None was walked.
- 34 Ingleside Ave has no OSM record; its coordinate is approximate to Kossuth Colony, so its
  distance to the 45404 subjects is ±0.3 mi.
- 49 Pointview's ask was corrected from $39,900 to $59,900 this session. Do not reuse $39,900.
