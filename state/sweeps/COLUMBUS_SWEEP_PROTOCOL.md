# Columbus sweep — protocol derived from the 43204 run

Written 2026-11-08, **after** the first Columbus ZIP (43204) was swept and priced. Cleveland's
`CLEVELAND_SWEEP_PROTOCOL.md` was written *before* its first listing; this one is written *after*,
so it records what actually bit rather than what was expected to. Both apply. Read them together.

Sections 0–6 are inherited from Cleveland and still bind. Sections 7+ are new to Columbus and are
measured facts, not guesses.

---

## 0. The inherited rules (unchanged, do not re-derive)

The seven Dayton rules, the three sheet-layer rules, the hood gate, the comps gate, the arithmetic,
and the reporting order are all in `CLEVELAND_SWEEP_PROTOCOL.md` §0–§6. They were not weakened by
anything found in Columbus. Summary of the ones that fired in 43204:

| # | Rule | Fired in 43204? |
|---|---|---|
| 1 | Recount the live total on the day you report it | **Yes** — 196 Zillow / 191 Redfin, both read same day |
| 2 | `comp.py` exit 3 = UNPRICED; exit 1 = abort loudly | Yes — used correctly, 5 exits of 3 |
| 4 | Sourced coordinate before any radius claim | Yes — every comp geocoded, all 5 within 0.5 mi |
| 5 | No radius printed if no radius applied | Not triggered |
| 8 | `updated_rows: N` is not a receipt | **Yes** — see §12 |

---

## 1. Discovery — measured 43204

- **Zillow is primary** (196 active). Redfin cross-check (191 active). A 5-listing gap between
  portals is normal and is not evidence either is wrong.
- **Realtor.com is unusable** — reCAPTCHA wall. Do not spend a pass on it.
- **The working band was houses, $40k–$175k** → 54 after filtering. That is a *reading order*,
  not a buy box: coverage is reported against the full 196. See D-53's closing note.
- **Sold feeds:** `redfin.com/zipcode/<ZIP>/filter/include=sold-6mo` → 347 for 43204, 96 for the
  Central Hilltop neighbourhood. The ZIP sold feed is **not hood-coherent**; mine it row by row.

## 2. Hood — the binding constraint, and it is a labour cost

**Only 5 of 55 rows in 43204 carry a verified neighbourhood.** Hood comes from the Zillow
`## Neighborhood:` block, which exists on the property page and nowhere in the feed. That is one
page fetch per lead, and it is the single biggest cost in the sweep.

Consequence, stated as a rule:

> **A lead without a verified hood cannot be priced, and saying so is the correct output.**
> `UNVERIFIED` in the Hood column is a deliverable, not a gap to be filled by inference from the
> ZIP, from the price, or from "most of this ZIP is Hilltop".

Do not de-duplicate hoods by assumption either. 691 S Warren Ave reads as Hilltop in a Zillow
Neighborhood block and as **SOUTH CENTRAL HILLTOP** on Redfin; the Zillow value wins and the
difference is enough to kill a pricing run.

## 3. Comps — 43204 reality

- The renovated pool in Central Hilltop **is thin but sufficient**: n=5 in 6 months inside 0.5 mi,
  median **$151.07/sf**, p25–p75 spread **10.4%** (TIGHT). See
  `state/comps/columbus_43204_centralhilltop_comps.csv`.
- **The bed floor binds hard.** All five comps are 3bd. Every 4bd and 5bd subject in the ZIP is
  UNPRICED for that reason alone (569 S Terrace, 223 N Wayne, 827 S Harris, 53 N Wayne).
- **A 2bd pool is the highest-leverage missing artefact.** 21 of 55 rows are 2bd. One pool unlocks
  all of them.
- The ±30% sqft band dropped exactly one real comp (192 S Harris, 1,153 sf against a 1,410 sf
  median subject basis) and the ±45% gate dropped 131 S Eureka. Neither was reinstated.
- **Excluded and why:** 236 S Hague $80,000/1,548 sf is distressed (not an ARV input, usable only
  as an as-is floor); 1930 Floral $220,000/1,328 sf failed the size band; 229 S Richardson
  $165,000/1,168 sf failed it too.

## 4. Arithmetic — no change

```
ARV        = subject_sqft × MEDIAN $/sf of the renovated comp set   (no haircut)
CEILING    = ARV × 0.70 − repairs                                   (buyer max)
SELLER MAO = CEILING − $10,000
OFFER LOW  = 0.55 × ARV − repairs
OFFER HIGH = 0.60 × ARV − repairs
MAO < 80% of ask ⇒ REJECT unless DOM/reductions prove movement
```

Repairs $20 / $35 / $50 per sf, valid only at ARV ≥ $100/sf, refused below $60/sf. In 43204 the
median ARV basis is ~$151/sf so the tiers sit in the calibrated band — the Cleveland §7 warning
about $54k–$111k hood medians **does not apply here** and must not be imported.

**ARV BAND = NONE for 43204.** There is no Franklin County walk-forward. The Cuyahoga 44102 ±40%
band is a different county, a different product and a different decade of housing stock (D-29).
The 10.4% comp spread is a *measured dispersion*, not an error band; do not print one as the other.

## 5. Reporting — 43204 as the template

`state/comps/COLUMBUS_43204_FULL_SCREEN_2026-11-08.md` is the shape every future Columbus ZIP
should follow: coverage table with both portals, headline counts by status, reject counts by
reason, the named blocker, the ordered next pull, and an explicit compliance checklist.

**Coverage was 54/196 = 27.6% and was called partial.** That sentence is mandatory.

## 6. Sheet layer — what the 43204 tab proved

The delivery tab is `COLUMBUS 43204 LEADS`, sheet_id `881913520`, in workbook
`1Hsqo4SvnfyTXfFCLndN2BqFJsFGXqoDooUKz7aUs6S4`. Seven columns of prose per row means the sheet is
a report, not a spreadsheet — plan for widths first.

| # | Rule | Born from |
|---|---|---|
| 11 | **Never apply a currency number format across a range that contains text columns.** `F2:P56` currency turned `Style`, `DOM`, `Status` and `Tier` into `$15`, `$TRADITIONAL`. Format the money columns individually (F, L, M, N, O, P), then re-read A1:R6 to confirm. | observed this session |
| 12 | **No magic numbers in a live formula.** `=ROUND(1691*151.0714,0)` is unauditable — the sqft and the median are both invisible. Put the sweep input in a labelled cell (here `T1:T3`) and reference it: `=ROUND(E2*$T$2,0)`. | observed this session |
| 13 | **A formula row must be reconciled to `comp.py` before it is trusted**, and the reconciliation is a `get_values` read, not an eyeball. | inherited (D-40 class) |
| 14 | Every tab gets a READ ME sibling. Cleveland has `CH2 READ ME`; Columbus has `COLUMBUS READ ME`. The READ ME states coverage, status counts, what the numbers mean, **what would make them wrong**, and the next pull — in that order. | pattern |

## 7. Columbus-specific traps found in 43204

1. **Auction minimum bid ≠ asking price.** 569 S Terrace carried a "$79,900" that is a bid floor in
   an online auction closing Dec 6. It was recorded, flagged, and excluded from any $/sf ranking of
   sells. Never treat a bid floor as a negotiable ask.
2. **`UNVERIFIED` hood is common enough to be the default.** 50 of 55 rows. Budget the fetches.
3. **Redfin ZIP pages leak neighbouring ZIPs.** Same defect as Cleveland §7; verify the ZIP on
   every row before ledgering it.
4. **The 43204 filtered count is not the 43204 total.** 54 ≠ 196. Both numbers get reported.
5. **Package and multi-property listings exist in this band** and are coded SEPARATE, not REJECT —
   they are real assets in the wrong channel, exactly like the condo and the duplex.

## 8. What was NOT done in 43204, and must be said out loud

- 142 of 196 active listings were never opened. They are condos, 55+ park homes, multifamily, new
  builds and retail above $175k. Coverage is 27.6%.
- Photos came from `image_search` because `bash` has no egress to the listing CDNs. That is the
  documented fallback and it was stated in the deliverable, not hidden.
- No Franklin County backtest exists, so no ARV band is quoted.
- No `state/zip_ledger.csv` row exists for any Columbus ZIP beyond 43204, and no Columbus ZIP has
  been scored against the 25/20/20/20/15 weights. **Do not call a Columbus ZIP "ranked".**

## 9. The order of work for the next Columbus ZIP

1. Count live actives on both portals, same day. Write the denominator down first.
2. Pull the sold-6mo feed and the hood feed; do not pool them.
3. Read the band, record every row including rejects.
4. Read hoods **only for shortlisted rows** — hood is expensive and a reject never needs one.
5. Build the pool, run `comp.py`, reconcile by hand on one lead.
6. Write the `.md` deliverable and the CSV.
7. Push to Sheets: data first, then formats, then READ ME. Re-read after every format call.
