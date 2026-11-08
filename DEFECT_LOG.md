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
