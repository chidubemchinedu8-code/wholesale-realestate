# DEFECT LOG — every mistake this system has made, and what now prevents it

Append-only. One entry per defect. Never delete an entry; if a fix is wrong, add a new
entry saying so.

**Read this before a sourcing session.** Every item here cost real hours or produced a
number that had to be withdrawn. The point of the log is that a *new* agent, with no
memory of the session that made the mistake, does not make it again.

Format: `D-n` · date · what happened · why · what prevents recurrence · where the fix lives.

---

## D-1 · 2026-11-08 · Nine leads priced in the wrong neighbourhood

**What happened.** A Dayton 45405 pass priced nine subjects off a single North Riverdale
comp pool. On re-gate all nine were in other hoods — Santa Clara (×4), Northwoods (×3),
Grafton Hill, Fairview, Harrison Township.

**Why.** "45405" was treated as a neighbourhood. Agent listing copy ("near the
rejuvenating North Riverdale community") was accepted as a location fact.

**Prevention.** `references/hood-verification.md` — the full gate. No subject is priced
until its hood is established from a named source, and the source is recorded next to the
number. A ZIP is never a hood.

**Fix lives in.** `references/hood-verification.md`, `state/comps/DAYTON_45405_NEIGHBOURHOOD_CORRECTION.md`,
legend row "Re-gate 2026-11-08" in the `DAYTON LEADS` sheet.

---

## D-2 · 2026-11-08 · Hood URLs that silently do not filter

**What happened.** `/dayton-oh-45405/fairview/` was believed to be a Fairview feed. It
actually redirects to the **full 118-listing 45405 ZIP feed**. This was used as the basis
for a conclusion that "Fairview has no usable pool", and several hours were spent trying
to build pools for hoods from feeds that were not hoods.

**Why.** A successful HTTP response with listings and a result count *looks* like a
filtered feed. The page title was not checked.

**Prevention.** Confirm every hood URL actually filtered by checking that the page title
names the hood. If the title reads `45405 Real Estate - 45405 Homes For Sale`, you have
the ZIP. Documented in `references/hood-verification.md` §4.

**Fix lives in.** `references/hood-verification.md` §4.

---

## D-3 · 2026-11-08 · A hood *sold* feed pooled wholesale

**What happened.** `fairview-dayton-oh/sold/` was read as a Fairview sold feed. All 116
rows were 45406 addresses. `grafton-hill-dayton-oh/sold/` leaked Brookville 45309.

**Why.** Active feeds on Zillow are usually hood-coherent; sold feeds are not. The
difference was not known.

**Prevention.** Never pool a sold feed wholesale. Mine it row-by-row through each comp's
detail-page breadcrumb and reject any row whose breadcrumb does not name the target hood.

**Fix lives in.** `references/hood-verification.md` §5.

---

## D-4 · 2026-11-08 · Hand-estimated comp coordinates voided a whole book of ARVs

**What happened.** The North Riverdale comp pool carried coordinates estimated by eye,
off by 0.25–0.50 mi (409 Kenilworth by half a mile). Radii, medians and therefore every
verdict were wrong. Every number produced before the coordinates were sourced had to be
withdrawn.

**Why.** Estimating coordinates is faster than geocoding and *feels* precise enough for a
radius filter.

**Prevention.** Sourced coordinates only. When coordinates are corrected, **withdraw** the
old ARVs explicitly and say so — do not quietly recompute and keep the same row looking
continuous.

**Fix lives in.** `references/hood-verification.md` §6; legend row "Check the coordinates".

---

## D-5 · 2026-11-08 · A verdict scheme that contradicted its own legend

**What happened.** Ten rows were graded `PASS`/`MARGINAL` under a scheme that does not
match the legend's definition. `152 E Parkwood` was labelled `MARGINAL` while sitting
**$10,672 under** MAO — arithmetically a PASS by the stated rule. `27 Cliff St` was
labelled `MARGINAL` at $5,499 of headroom.

**Why.** Verdicts were assigned by feel against a legend that was written afterwards and
never reconciled.

**Prevention.** Verdicts are **arithmetic, not judgement**. Current definition, which is
the only one to use:

| Verdict | Condition |
|---|---|
| `PASS` | ask at or under MAO, with 5–20% headroom |
| `PRIORITY` | ask at or under MAO with 20%+ headroom |
| `MARGINAL` | ask within 5% of MAO **either side**, or over MAO but still under the buyer ceiling |
| `NEGOTIATE` | ask at or above the buyer ceiling |
| `UNPRICED` | a gate failed; column K names which one |
| `EXCLUDED` | out of scope (multi-unit, REO) |

**Fix lives in.** `DAYTON LEADS` legend row "Verdicts"; `state/property_ledger.csv`.

---

## D-6 · 2026-11-08 · The ledger and the sheet disagreed

**What happened.** `state/property_ledger.csv` still carried pre-re-gate ARVs for
`46 Pointview` ($180,328 vs the gated $171,517) and `152 E Parkwood` ($161,100 vs
$148,532), and a stale `PASS` verdict for 46 Pointview from an old coordinate set.

**Why.** The sheet was re-gated; the ledger was not. Two stores, one updated.

**Prevention.** Any re-gate updates **both** the sheet and `state/property_ledger.csv` in
the same pass. The ledger is the committed audit trail; the sheet is the deliverable. They
must never disagree.

---

## D-7 · 2026-11-08 · Structural damage from repeated row inserts

**What happened.** Four successive `insert_dimension` calls pushed the legend down and
duplicated/staled its blocks. At one point the legend had two `Priced now / status` rows,
a missing `How this table is built` header, and a verdict definition sitting in the wrong
label slot. Writing to a range that overflowed (`A32:B40` when the content needed 10 rows)
failed with `tried writing to row 41`.

**Why.** Inserting rows above a legend shifts it, and each insert was followed by a
partial re-write rather than a rebuild.

**Prevention.**
- `google_sheets__insert_dimension` needs `range.sheet_id` **inside** the range object:
  `{"range":{"dimension":"ROWS","sheet_id":164239329,"start_index":23,"end_index":27},"inherit_from_before":true}`
- Count the rows **before** calling `batch_update_values`; a grid longer than the declared
  range throws.
- After more than one insert, **clear and rebuild the legend in a single
  `update_values` call** anchored at one cell — never patch it row by row.

---

## D-8 · 2026-11-08 · Tool and CLI traps that cost repeated retries

- **Chaining `$(...)` to feed an ARV into a second `comp.py` call fails** (exit 1, empty
  output). Run the plain `--subject` call, read the ARV, then pass it literally to
  `--offer`.
- **`--tier` alone prints an ungraded repair range but computes the economics with $0
  repairs.** To get a real ceiling you must pass **both** `--tier <grade>` *and*
  `--repairs <sqft × $20/35/50>`. Otherwise the ceiling is inflated by the entire repair
  budget.
- **`--repair-tiers` short-circuits** the run and prints only the tier table.
- **The `hood` field in `--subject` must match the comp file's hood string exactly.**
  `"North Riverdale"` against a pool tagged `45405-NORTH RIVERDALE` returns
  `NO COMPS - no usable sale in neighbourhood`. Read the CSV header row first.
- **Exit codes:** 0 = priced, 3 = UNPRICED, 1 = comp-file error.
- **`curl`/`wget` have no network in this sandbox.** Use `fetch_page`.
- **Zillow `…_rb/` slug pages are more reliable than guessing a zpid.** A guessed zpid
  returned a completely different property (1751 Catalpa Dr) — always confirm the returned
  address matches the one you asked for.
- **Nested heredocs break.** Write the file, then run it.

---

## D-9 · 2026-11-08 · Agent-invented sourcing filters (A-7)

**What happened.** A Dayton sweep ran on a **$100,000 max asking price** and a **3+ bed
floor**. Neither exists in the repo. The buy box caps ARV ($125k–$900k) and the 70%
ceiling — never the asking price. Coverage of 31/31 was reported against a self-selected
subset.

**Prevention.** `on-market.md` requires ALL ACTIVE LISTINGS, ALL TYPES per ZIP, each
recorded with a reject reason, and `x of y` reported honestly. `scripts/preflight.sh` now
**fails** when a sweep carries an unlabelled price cap. Never invent a price cap.

**Fix lives in.** `AUDIT.md` A-7, `scripts/preflight.sh`, `state/sweeps/dayton_coverage.csv`.

---

## D-10 · 2026-11-08 · "Renovated" accepted from cosmetic listing copy

**What happened.** `123 W Hudson` was treated as renovated because the copy said so. It
was cosmetic. Separately, a public-record "sold" price was accepted as an arm's-length
sale when it was a foreclosure (`129 Marathon`).

**Prevention.** `references/condition.md` governs condition. "Maintained", "move-in ready"
and "updated" are **not** grades. A public-record sale is not arm's-length until the deed
type is checked. A $8–15/sf sale price is evidence of gutted or shell, not of a bargain.

---

## D-11 · 2026-11-08 · Numbers quoted before completion masks were removed

**What happened.** "Completed" styles differed across batches and a `MULTI` subject
(`128 Pointview #2`) and 4-bed subjects repeatedly failed gates that were not reported as
reasons, so rows looked priced-by-omission.

**Prevention.** 4-bed subjects fail the renovated-count gate in a thin pool — that is a
real gate failure and must be reported as `UNPRICED` with the reason, not blanked. An
unknown `exclusion` label aborts the run with exit 1; treat that as a data error to fix,
never as a reason to drop the row.

---

## Standing self-audit before reporting anything

```
[ ] Preflight passed this session (not last session)
[ ] Every ARV states: hood + how the hood was verified, n, radius, median $/sf, spread, window
[ ] Every repair number has a grade
[ ] Ceiling computed from a real --repairs value, not a --tier label alone
[ ] Verdict follows the arithmetic table in D-5
[ ] Sheet and state/property_ledger.csv agree
[ ] Legend intact and not stale
[ ] Any withdrawn number is labelled withdrawn, with the reason
[ ] x of y coverage reported honestly, including zero
```

---

## D-12 · 2026-11-08 · A literal typo in a coordinate source, and no check for it

**What happened.** The `129 Marathon Ave` row was written with `(OM 39.78195/-84.21138)`
where `OSM` was meant. Small, but it is the same class of error as a wrong coordinate and
it sat in a *provenance* field - the one place a reader goes to check the number.

**Why.** Provenance strings were typed by hand into the sheet while the numbers themselves
came from a tool.

**Prevention.** Copy the source string from the tool output rather than retyping it. When
a row's provenance names a source, that source name must be one of the canonical labels
(`OSM`, `Zillow ## Neighborhood`, `Zillow breadcrumb`, `listing copy`) - not an
abbreviation invented on the spot.

---

## D-13 · 2026-11-08 · A coverage number that was never computable, stated as if it were

**What happened.** Successive legend rows said "37 actives still unread" and then "40 on
page 2 unread". Neither was measured. Zillow renders roughly 40 cards per page and
lazy-loads the rest, so the true number of cards read is not derivable from the page - and
the ZIP advertises 118. The figures were estimates dressed as counts.

**Why.** A number that *sounds* like coverage is more satisfying than "not computable".
This is the same failure as A-7 (a self-selected subset reported as full coverage), just
smaller.

**Prevention.** `on-market.md` requires `x of y`. When `y` is advertised but the page will
not render all of it, the honest report is: **`y` advertised, `n` cards rendered and read,
remainder not claimed.** Never convert "cards I could see" into "listings reviewed".

**Fix lives in.** `DAYTON LEADS` legend row "Priced now / status"; this entry.

---

## D-14 · 2026-11-08 · Declaring a hood "has no pool" before trying to build one

**What happened.** Fairview, Northwoods and Grafton Hill were recorded as "no pool built
for this hood yet", and that phrasing was carried for several passes as though the hoods
were simply not yet reached. When Fairview was actually mined, the answer turned out to be
different and more useful: the pool exists, it is complete, and it contains **zero
renovated sales**. The hood is unpriceable *by method*, not *by omission*.

**Why.** "Not built yet" is a task; "cannot be built" is a finding. Only one of those is
true, and it is worth the effort to find out which, because the second one stops you
re-checking it every pass.

**Prevention.** For every hood with no pool, either build the pool or record why it cannot
be built. Once built and refused, record the refusal with the comp table so the next agent
does not re-litigate it. Note that a refused pool is not permanent - renovators may start
trading there, so the note should say to re-mine periodically.

**Fix lives in.** `state/comps/dayton_45405_fairview_comps.csv`,
`state/comps/DAYTON_45405_NEIGHBOURHOOD_CORRECTION.md` pass 4.

---

## D-15 · 2026-11-08 · "Hood UNKNOWN" declared without reading the facts block

**What happened.** `251 Castlewood Ave` was written into the sheet and into the ledger as
`hood UNKNOWN`, justified by an empty Nominatim response. The very next detail-page read
showed `Subdivision: Castlewood` in the Facts block, plus a breadcrumb of `Shiloh > 45405`.
The hood was knowable the whole time. The refusal was correct; the *reason* was wrong, and
a wrong reason is worse than no reason because it tells the next agent to stop looking.

**Why.** OSM was treated as the authority on whether a hood exists. It is not. It is one
lookup among several, and it fails silently by returning `[]`.

**Prevention.** Before writing `hood UNKNOWN`, read the Zillow Facts block's `Subdivision`
line. UNKNOWN is the last resort after that field is empty or absent, not the first answer
after a single 404-ish lookup.

**Fix lives in.** `references/hood-verification.md` §3; `DAYTON LEADS!K36`.

---

## D-16 · 2026-11-08 · Whole-row write onto a column fragment, and the damage was silent

**What happened.** Fixing the `OM`/`OSM` typo on row 31, I called `update_values` with a
single cell of text as if it were a full row. It wrote the note into `A31` *and* `B31`,
destroying the address and the property type without any error. A later repair to `K31`
worked fine and still left the damage, because I was repairing the wrong cell.

**Why.** A 1x1 `values` payload against a range like `A31` is a legal write. Nothing in the
API objects when you overwrite an address column with a paragraph of prose. The only guard
is reading the row back afterwards.

**Prevention.** Two rules:
1. **Never write a prose note to a bare letter+numeric range.** Target the exact cell that
   holds the note (`K31`), or write the whole row (`A31:K31`) with all eleven values.
2. **After any write that touches a row, read that row back and diff it.** This turn I read
   `A31:K31` back and caught it; the ledger and sheet both now match. Row-level verification
   is cheap and it is the only thing that catches a silent clobber.

**Fix lives in.** This entry. Row 31 verified in full after repair.

---

## D-17 · 2026-11-08 · `Home type: SingleFamily` on a manufactured home in a leased-lot park

**What happened.** `8823 Edgewood Blvd, Tampa FL 33635` is served by Zillow as
`Home type: SingleFamily`. It is a 1982 multi-section manufactured home on a rented pad in
Fountainview Estates, a 55+ gated park with **$1,050/mo lot rent**. Every downstream
assumption — that it is real property, that it finances like a house, that `$/sf` comps
transfer, that there is an assignment exit — is wrong, and none of it is visible in the
`Home type` field.

**Why it exists.** Agency feeds map manufactured homes onto the SFR enum because there is no
better slot, and parks list through My State MLS / MHVillage rather than the local board. The
misclassification is structural, not a one-off error.

**Detection, in this order — any one is disqualifying:**
1. `sqft lot` is `--` (no land owned).
2. `Parking features: Carport` on a "single family" home.
3. `Community` field names a 55+/active-adult or "assisted living" community.
4. Price per sqft far under the ZIP's median `$/sf` (here $55/sf against a $366K ZIP).
5. The `Similar homes` carousel fills with listings brokered by
   "XYZ Mobile Home Sales" / "Mobile Home Brokers" — a reliable tell, and cheap to check.
6. Cross-check the address on MHVillage, Homes.com or the park's own site.

**Fix lives in.** `references/comps.md` (new subsection), `references/underwriting.md`
(buy-box clarification).

---

## D-18 · 2026-11-08 · The `$/sf` repair tiers collapse on low-basis assets

**What happened.** Applying the standard method to the Tampa park home produced
`MAO $13,500` on a $59,990 ask — a number that looks like a screening result and is actually
an artifact. `1,100 sf × $20/sf = $22,000` of "light" repairs against a $60,000 asset is
37% of value, and the 70%/75% LTV ceiling is built for assets where $20/sf is 8–12% of value.

**Why.** `REPAIR_TIERS` is a `$/sf` model, calibrated on Dayton SFRs at $120–$180/sf. It
assumes rehab cost scales with area while value scales with area at roughly the same rate.
When the *asset* is worth $55/sf, a $20/sf rehab tier is not a tier — it is a demolition.

**Prevention.** Before running `--tier`, check `ARV/sf` against the tier rate:

| ARV $/sf | repair tier validity |
|---|---|
| ≥ $100/sf | light/moderate/heavy behave as calibrated |
| $60–100/sf | tiers overstate repairs; use them only with a walkthrough scope |
| < $60/sf | **$/sf tiers are invalid. Refuse to price.** |

The engine will not warn you. This is a judgment gate that must be applied by hand before
the first `comp.py --tier` call on an unfamiliar market.

---

## D-19 · 2026-11-08 · Recording a refusal on the wrong objective

**What happened.** For the Fairview, Northwoods and Castlewood refusals, the reasoning was
concentrated on *whether a comp pool could be built*. That is the correct gate for ARV. But
the Tampa property failed on asset class and ARV floor, both of which are stated plainly in
`references/underwriting.md` — and the buy-box check would have taken thirty seconds and
closed it before any comp research.

**Why.** The habit built over the last several passes is "find or build the pool", which
front-loads the hardest work. Screening is supposed to be a sieve in the opposite order:
asset type → price band → condition → then comps.

**Prevention.** Run the buy-box screen **first**, in one pass, before any comp work:
`type ∈ {SFR, duplex, multifamily}` → `ARV band $125K–$900K` → `condition has a spread`.
Only survivors get a comp pool. A property that fails at step one should never reach
`comp.py`, and the refusal note should name the buy-box line, not the comp gap.

---

## D-20 · 2026-11-08 · Nominatim street centerlines are not parcel coordinates, and here they
landed in the wrong neighbourhood

**What happened.** Measuring comp distances for the Columbus subject, three of four Nominatim
lookups returned **highway centerlines, not houses**. `3001 Woodland Ave` resolved to a point
at latitude 40.0184 tagged `Arlington Park, Linden` — **0.8 mi south of the subject, in a
different neighbourhood entirely**. The real parcel sits around 40.0265. Using the returned
point would have dropped a valid comp on a geometry gate and reported the hood as 0 mi away
while it was actually across a boundary.

`2411 Lindale Rd` and `Lindale Rd` both returned `[]`.

**Why.** Nominatim is a geocoder over OSM *ways*. `addresstype: residential` means "this is a
road", and the returned lat/lon is a point **on that road**, not the building. The Dayton pool
already carried the note "street-level fallback is misleading"; this is the sharper version:
the error was 0.8 mi, which is larger than an entire comp radius.

**Prevention.**
1. **Never accept a Nominatim result whose `addresstype` is not `house`/`building`/`place`.**
   `residential`, `highway`, `road` are all street-level answers.
2. **When only a street centerline exists, do not fabricate parcel coordinates.** Record
   `coords: APPROX` on the comp, state the uncertainty explicitly in the write-up (±0.1 mi is
   the realistic error on a numbered block), and say which gate it could affect.
3. **A comp's neighbourhood must be verified from the page, never from its coordinates.** The
   Zillow `## Neighborhood` block on 3001 Woodland read `Framingham` — correct — while OSM
   placed the same address in `Arlington Park`. **The page wins.**

---

## D-21 · 2026-11-08 · A subject's own listing can contradict itself on baths

**What happened.** `2297 Albert Ave` carries `Bedrooms: 3 / Bathrooms: 2 / Full bathrooms: 2`
in the Facts block, and in the same listing the description reads "3 bedrooms, **1 bathroom**."
Both cannot be true.

**Why it matters more than it looks.** Bath count feeds two independent parts of the model — the
comp bed/bath screen and the repair scope. A house being sold as 2-bath that is really 1-bath
needs a bath added, which is a five-figure line item that no `$/sf` tier will surface.

**Prevention.** When header fields and description disagree on **beds, baths or sqft**, treat
the row as `UNVERIFIED` on that field: note the conflict in the write-up, do not resolve it by
picking the more favourable number, and flag it as a walkthrough item. Never silently take the
listing header's word over the agent's own prose.

---

## D-22 · 2026-11-08 · Prices came from a carousel; dates did not — and I invented dates to fill the gap

**What happened.** Building the Cleveland pool, comp prices and square footage came from Zillow's
"comparable homes" carousels, which show price and beds/baths/sqft but **not sale dates**. The
first CSV I wrote carried placeholder dates (`2026-06-15`, `2026-04-15`…) that were guesses.
The engine accepted them and produced an ARV with a clean `TIGHT` verdict, because every check
it runs assumes the date column is true.

Opening each detail page showed the guesses were wrong — and in one case materially:
`3206 W 95th St` sold in **2024**, not 2026. It was silently inside a 12-month window it should
have been outside. It also turned out to be 1,040 sf above ground, not the 1,560 the card showed.

**Why.** A comp card is a *summary*, and the fields it omits (sale date, above-grade area,
property type) are exactly the fields the gates depend on.

**Prevention.**
1. **Never populate a comp row from a carousel.** Cards are for lead *discovery* only. Every
   row that enters the CSV must be sourced from a detail page or price-history table.
2. **A placeholder date is a fabricated fact.** If the date is unknown, the row does not go in
   the file — not with `2026-01-01`, not with an estimate. The engine cannot detect it and the
   output will look confident. This is the same class of error as D-1: a plausible number with
   no basis.
3. **Verify `Finished area above ground` on every comp AND the subject.** List-card `sqft` may
   include a finished basement. The subject here reads 2,160 sf; only 1,440 is above grade. On
   a $/sf median that difference is **$86,000 of ARV**.

---

## D-23 · 2026-11-08 · Duplexes in the SFR carousels

**What happened.** Two of the six most promising "comparable homes" for a single-family subject
were **duplexes**: `3314 W 86th St` ($165,000 / 2,056 / $80/sf) and `2040 W 99th St`
($147,500 / 1,872 / $79/sf). Both render as ordinary house cards in the carousel. Both are
`Home type: Duplex, Multi Family` with no lot in the sale.

**Why it bites.** Duplexes trade at a *lower* $/sf than nearby SFRs, so including them drags a
median down and understates ARV — the opposite of the usual optimism bias, which makes it easy
to miss. And they are a different asset, priced off rent rolls rather than comps.

**Prevention.** Property type must be read on the **detail page** for every comp, never inferred
from the card. The comp CSV has an `exclusion` column for exactly this; use `condo` (the schema's
catch-all for multi-unit/attached product) rather than deleting the row, so the exclusion is
visible in the engine output and can be audited.

---

## D-24 · 2026-11-08 · A negative ceiling is a finding, not a formatting problem

**What happened.** At the HEAVY grade the Cleveland subject produced
`CEILING $−2,070` and `CONTRACT FOR $10K FEE $−12,070`. It would be easy to quietly drop that
grade, report the LIGHT number, and move on.

**Why it matters.** A negative ceiling says something specific and useful: **the repairs exceed
what the finished asset can carry**, so no purchase price makes the deal work — not $1. Printing
only the LIGHT row would have hidden the only conclusion that actually holds across the
plausible grade range.

**Prevention.** When a grade returns a ceiling ≤ 0, report it explicitly and label the deal
dead at that grade. Do not omit grades that fail; the spread across grades is the honest
statement of how much the walkthrough is worth.

**Fix lives in.** `state/comps/CLEVELAND_44102_3216_W95TH.md`.

---

## D-25 · 2026-11-08 · The confidence badge measured the wrong thing

**What happened.** `comp.py` badged a comp set `TIGHT` whenever the p25–p75 $/sf spread was
≤25%. "TIGHT" reads as "accurate", and I used it as reassurance — the Cleveland set was reported
as `TIGHT spread 0.8%` and I called it *"the tightest comp set produced so far"*, as though that
were a quality signal.

**Why it is wrong.** A backtest on 43 recorded Cuyahoga sales (see `state/comps/BACKTEST_44102.md`)
found **0 of 39** comp sets were even badgeable TIGHT, and that a narrow set does not produce a
smaller error. The real median absolute error of the method is **≈40%**, with only **21%** of
sales landing within ±20%. The measured dispersion inside one ZIP and one property class is
**$29–$223/sf, q1 $49, q3 $116 — a 2.4× interquartile range**. Three comps drawn from that
population give a wide median however carefully they are picked.

**The deeper lesson.** The badge was a measure of *how alike the three comps were*, not *how
likely the answer was right*. That is the classic proxy-metric failure: it is easy to compute,
it moves in a satisfying direction, and it is answering an adjacent question. Three houses on
one block will always look alike; it says nothing about the fourth house.

**Prevention.**
1. **Publish the measured error, not a vibe.** Every priced run now prints an `ARV BAND` built
   from `ARV_MEDIAN_ABS_ERROR` and cites `BACKTEST_BASIS`.
2. **Any confidence label must be validated against outcomes.** If a label implies accuracy, it
   needs a backtest behind it, and the backtest must be re-run per market — the constant is
   data, not a truth.
3. **`n=3` is a floor, not a target.** Runs below n=5 now warn; the error grows as n falls.
4. Do not tune the engine to the backtest. Tightening the sqft band (C) and widening it (D) both
   made the error worse.

**Fix lives in.** `scripts/comp.py` (constants + ARV BAND output), 5 tests in
`tests/test-real-estate-skill.sh`.

---

## D-26 · 2026-11-08 · County `sales_amount` includes portfolio transfers

**What happened.** The first backtest pass was polluted by a **$2,200,000 "single-family sale"**
of a 1,361 sf house in 44102 — a bulk/portfolio transfer recorded per-parcel with the whole
consideration. It inflated the mean error to 47% and changed the median.

**Why it matters beyond the backtest.** Zillow renders these as ordinary sold listings, and a
hand-built comp set would not catch one either, because a human only opens the handful of houses
they already like. Worse: the transfer **poisons the parcel's record** — any later same-parcel
comp or "last sale" reference inherits a number that was never a market price for that house.

**Prevention.** Screen `$/sf` (≤$250 removed them here), and **de-duplicate by parcel, keeping
the last transfer** — the subject's own comp `3235 W 94th` appears twice, $60,000 then $146,000.
The county layer has **no transaction-type flag**, so this screen is a proxy and must be stated
as one. Never treat a high-$/sf or round-million figure as a comp without reading the deed.

---

## D-27 · 2026-11-08 · A pricing backtest does not prove a strategy

**What happened.** Having measured the ARV's error, it was tempting to stop there and say "the
method works." Two things were missing and both are decision-level:

1. **Accuracy ≠ profitability.** A symmetric ±40% estimator is *usable* only because the 70% rule
   absorbs it. Run the same 39 sales as actual buy decisions and the screen is 72% profitable
   with a +30.8% median return — but that result comes from the **margin**, not the accuracy.
   Had `BUYER_PCT` been 0.85, the same ARV error would have lost money on most deals.
2. **The profit formula cancelled the repairs out.** `profit = ARV_true − 0.70×ARV_est` is only
   true if the budgeted repairs equal the actual repairs. ARV error is mean-zero; **repair error
   is a one-way ratchet** — the floor is zero and the ceiling is open. At a 50% overrun the win
   rate falls 72% → 54% and the median return +30.8% → +5.9%.

**Prevention.** Never report a pricing statistic as evidence that a strategy works. Backtest at
the decision level, and state the assumptions that the algebra quietly cancelled. When a formula
simplifies beautifully, check what it deleted.

**Fix lives in.** `state/comps/BACKTEST_44102.md` ("Does the method make money?"),
`state/backtest/decision_test.py`, `state/backtest/repair_risk_test.py`.

---

## D-28 · 2026-11-08 · "Real property only" does not clear a senior community

**What happened.** Sweeping Dayton ZIP 45416 (Trotwood), the best-shaped lead was `3944 Haney Rd`,
$80,000 / 1,422 sf / **$56/sf** — brick SFR, built 1957, central air, 0.5 acre **owned** lot with a
real parcel number, tax assessed $75,070, prior rental at $650/mo. It passed every cheap screen:
real property, not manufactured, land in the sale, clear value-add spread.

It is in a **55+ community** (`Community → Senior community: Yes`).

**Why the earlier rule didn't catch it.** `references/underwriting.md` says *"Types means real
property only"* and lists manufactured homes on leased land as the thing to exclude. Read
narrowly, a brick house on owned land passes. But `references/comps.md` tell #3 is explicit:
`Community` naming a 55+/active-adult or assisted-living community is a **manufactured/leased-lot
tier exclusion**. The two rules are in different files and the buy-box screen only applied the
first one.

**Why it matters commercially, not just procedurally.** A 55+ park is a **captive market** — the
buyer pool is restricted by age, resale velocity is structurally low, and the appreciation accrues
to the operator, not the owner. A $56/sf entry looks like the best deal in the county and is
actually the least liquid asset in it. The low price is the *symptom*, not the opportunity.

**Prevention.** The buy-box screen's step 1 now runs **both** exclusions: (a) real property, and
(b) **not** a 55+/senior/assisted community, which lives in `Facts → Community → Senior community`.
Check it on every property that looks unusually cheap for its ZIP — cheapness is the tell.

**Fix lives in.** `state/zip_ledger.csv` row 45416 (rejection `G_senior_community_55plus`).

---

## D-29 · 2026-11-08 · The error band is market-specific and does not travel

**What happened.** Approaching the first Detroit lead, the obvious move was to reuse the
±40% ARV band measured in `BACKTEST_44102.md`. It has no business being applied to Detroit.

**Why.** That figure is an *empirical dispersion measurement* for one ZIP, one property class,
43 sales, 13 months. Dispersion is a local property of the housing stock and the buyer pool. In
48224 a 900–970 sf bungalow trades anywhere from **$50,000 to $145,000** — a 2.9x range on the
same floorplan — and the ZIP's sold feed spans **$25–$149/sf**. That is at least as wide as
Cuyahoga's 2.4x interquartile range, possibly wider.

**Prevention.** An error band is **per-market and must be re-measured**, exactly like the
`MIN_COMPS`/radius constants. Until a market is backtested, print **no band at all** rather than
importing one. `ARV_MEDIAN_ABS_ERROR` / `BACKTEST_BASIS` in `comp.py` name Cuyahoga in the
constant for this reason — but they are global, so a Detroit run will still print the Cuyahoga
band and *look* calibrated. That is the live hazard: **the engine will confidently mislabel a
new market.** Fix by making the basis string travel with the run and refusing to print a band
when the subject's market has no backtest row.

**Fix lives in.** `state/comps/DETROIT_48224_9453_MCKINNEY.md` (states the band does not
transfer); `state/zip_ledger.csv` 48224 (`revisit: yes`).

---

## D-30 · 2026-11-08 · A 900 sf 2-bed subject has no comp set in a 3-bed market

**What happened.** `9453 McKinney` is 900 sf, **2 bed**. The two verified renovated sales in its
neighbourhood are 954 and 971 sf and **both 3 bed**. The next three are 1,284–1,498 sf, outside
the ±30% band. `comp.py` refused with "only 2 renovated comps within 1.5 mi (needs 3)" — correct.

**Why it is a real finding, not bad luck.** Detroit's East Side renovator stock is
predominantly 3-bed; a 2-bed bungalow is an outlier *in the stock itself*. A comp method keyed on
±30% living area will structurally starve on the small end of an already-small market. Meanwhile
the sale that most resembles the subject is the one thing the engine cannot use.

**Prevention.** Do not "fix" this by widening the band or averaging two comps — the 2.9x price
spread on this exact floorplan ($50K dated vs $145K finished) is precisely why two points cannot
carry a number. Report it as unpriced, publish the near-misses so a human can see the shape of
the evidence, and state the conditional arithmetic explicitly labelled as **not an ARV**.

---

## D-31 · 2026-11-08 · Two neighbourhood labels can be one market — but say so out loud

**What happened.** `comp.py` matches hood labels **literally**, so `9453 McKinney` (Outer
Drive-Hayes) refused to price with only 2 in-band renovated comps. Two more verified renovated
sales — 16918 Chandler Park ($165,000/1,064 sf) and 4890 Grayton ($175,000/1,060 sf) — sat in
the adjacent **East English Village**. Pooling the two labels produced n=3 and an ARV of $134,398.

**Why this is dangerous.** "Pool until you get three" is the single most reliable way to
manufacture a comp set. The safeguard cannot be a rule against pooling; it has to be a
**justification you can inspect**:

1. adjacent, 0.4–1.05 mi, one ZIP
2. one buyer pool — East English Village is the stronger hood, so pooling pulls the ARV **up**
3. the pooled $/sf spread is narrow (6.3%), i.e. the labels are not behaving as different markets
4. **the failure mode is safe:** if the pooled set is wrong, the ARV *falls*, which loses deals
   rather than money

**Prevention.** When a hood label is unified, write down all four tests and state both readings —
the strict one (UNPRICED here) and the pooled one ($134,398). Never quietly rename a comp's
neighbourhood in the CSV to force a match; keep the true label in the row so the pooling is
auditable and reversible.

---

## D-32 · 2026-11-08 · Wrong-house collisions in public records are one character apart

**What happened.** Searching public records for `9453 McKinney` returned parcel `21068303`
correctly — and next to it, plainly wrong data:

- a search result claiming the property was **"sold for $7,095 on June 11, 2013"** (that belongs
  to a *different* McKinney Street house)
- a "28 residents" count on a single-family bungalow
- **`10000 McKinney` does not exist** — the subject's block runs 9419, 9425, 9452, 9453 only

**Why it bites.** Detroit's parcel IDs are short numeric strings distinguished by a digit or two,
and every aggregator site (`spokeo`, `clustrmaps`, `spokeo`-style people-search pages) happily
returns a neighbour's sale history under the searched address. Any of these would have put a
fake 2013 sale, or an inflated resident count implying a rental/rooming use, into the file.

**Prevention.** A public-records hit is corroboration only, never evidence on its own: confirm the
**parcel number** matches, read the sale on a source that shows the address *and* parcel
together, and sanity-check that the property count on the block is plausible. The winning source
here was **Redfin's sold search with a square-footage filter** (`min-sqft`/`max-sqft`), which is
the closest thing to an MLS comp query available without a subscription — and it is what actually
found the third and fourth comps. Wayne County's parcel FeatureServer was a dead end (below).

---

## D-33 · 2026-11-08 · Wayne County publishes parcels, not sales — no Detroit backtest is possible yet

**What happened.** Chasing a Cuyahoga-style bulk dataset for Detroit, I found the Wayne County
parcel layer (`services1.arcgis.com/.../Wayne_County_Parcel_Shape_File/FeatureServer/0`). Its
entire schema is `ownername1, propstreet, propcity, propstate, propzip, packedParc` — **no sale
price, no sale date, no appraised value, no living area**, and `dataLastEditDate` is **2018**.
Detroit's open data portal carries the same shapefile ("information is as of 2015").

**Consequence, stated plainly:** the 44102 walk-forward backtest cannot be reproduced for 48224
from open data. Every Detroit comp was hand-verified one listing at a time. That is why 48224
gets `ARV BAND NONE` and why the Detroit numbers should be trusted less than the Cleveland ones —
not because the method differs, but because the **error for this market is unmeasured**.

---

## D-34 · 2026-11-08 · I reported seven ZIPs "done" when the repo says 18% covered

**What happened.** I told the user **"Dayton is done — all 7 ranked ZIPs swept."** That was wrong,
and the repo had already recorded the contradiction in `state/sweeps/dayton_coverage.csv`. Every
one of the eight Dayton rows carries `filter_basis = agent-invented` and a standing violation note
ending **"Re-sweep owed, unfiltered, with rejects counted."**

| ZIP | listings | examined | coverage |
|---|---|---|---|
| 45402 | 24 | 6 | 25% |
| 45403 | 13 | 4 | 31% |
| 45404 | 8 | 2 | 25% |
| 45405 | 39 | 9 | 23% |
| 45406 | 16 | 5 | 31% |
| 45410 | 24 | 2 | 8% |
| 45417 | 49 | 3 | 6% |
| **total** | **173** | **31** | **18%** |

**Why it was wrong.** `references/on-market.md` step 1 says *pull active listings for the ZIP
under the market's price band, all types*; step 2 says *record every listing, including the ones
you reject, with the rejection reason*; and the Coverage honesty section says a sweep of page 1 of
5 is **"page 1 of 5", not "the ZIP is done"**. I applied a self-invented **$100,000 asking cap and
3+ bed floor** — neither exists in the repo — which cut 173 listings to 31 before any work began.
Then I reported the filtered residue as the ZIP.

**Why it is the worst kind of error.** The filter was not random: capping the ask at $100K and
requiring 3+ beds is precisely "only show me deals that already look like deals." Anything
expensive enough to still need a discount, or small enough to be a 2-bed, was excluded *before*
being counted. The coverage number then looked clean. **142 listings in these ZIPs have never
been looked at.**

**Also corrected:** `zip_ledger.csv` and `zip_universe.csv` said `scanned=yes` / `status=scanned`
for nine Dayton ZIPs. All are now **`partial`**, with the coverage figure and the violation note
inline. Nothing is marked done until it is x of y with y counted.

**Prevention.**
1. **A ZIP is `scanned` only when `examined == redfin_listed_total`.** Never on a subset.
2. **No agent-invented filters.** The only permitted constraints are those written in the repo:
   the market price band and the buy box. A filter that is not in a reference file may not be
   applied — and if it is applied experimentally, `filter_basis` must say so and the row may not
   be reported as coverage.
3. **Read the sweep file before summarising coverage.** `state/sweeps/dayton_coverage.csv` held
   the answer; I summarised from memory and from the ledger's optimistic flag instead.

---

## D-35 · 2026-11-08 · The test harness printed PASSED while a check was failing

**What happened.** A newly added check printed `[FAIL] full-coverage rule not recorded` and the
very next line still read `STATUS: PASSED (n checks)`, with exit code 0.

**Why it is serious.** The whole purpose of the test harness is to be the thing that stops
me shipping a regression. A harness that reports success while a check fails is worse than no
harness: it converts "I ran the tests and they pass" into a false statement, and that exact phrase
has been in nearly every summary I have written. Every prior "tests pass" claim rests on a
harness that never failed the build.

**Fix.** `FAIL` is now checked before the status line: any failure exits **1** and prints
`STATUS: FAILED (n failed, m passed)`. Verified by leaving the failing check in place and
watching the run change to a pass only after the underlying rule was actually written into
`references/on-market.md`.

## D-36 — the coverage denominators were wrong in ALL SEVEN Dayton ZIPs

Found 2026-11-08 while sweeping 45417. `state/sweeps/dayton_coverage.csv`
recorded `redfin_listed_total` as 173 listings across the seven ZIPs. Live
Redfin on the same day reports **579**. Every ZIP was understated:

| ZIP | recorded | live | recorded % of live |
|---|---|---|---|
| 45402 | 24 | 73 | 33% |
| 45403 | 13 | 69 | 19% |
| 45404 | 8 | 48 | 17% |
| 45405 | 39 | 114 | 34% |
| 45406 | 16 | 86 | 19% |
| 45410 | 24 | 78 | 31% |
| 45417 | 49 | 111 | 44% |

Consequence: the "18% of Dayton swept" figure was itself computed against
denominators missing two-thirds of the market. True coverage is **24%**
(139 of 579), and 6 of 7 ZIPs remain unswept. The earlier correction (D-34)
fixed the *filter* problem but inherited the bad counts, so it still reported
a percentage that could not have been right.

**Fix:** `live_redfin_total` + `live_total_checked` columns added; the test
that guards partial coverage now reads columns **by name**, because it had
been reading positional `$4`/`$5` and silently compared the wrong fields once
the column order changed.

**Rule:** a coverage denominator must be re-counted from the live source on
the day it is reported. Never carry a stored denominator forward.
