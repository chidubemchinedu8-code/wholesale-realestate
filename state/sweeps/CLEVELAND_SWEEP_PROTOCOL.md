# Cleveland sweep — protocol derived from the Dayton failures

Written 2026-11-08 **before** the first Cleveland listing is read. Every rule below exists
because it was broken during the Dayton sweep and cost real numbers. Each cites the defect
that produced it. This file is the checklist a Cleveland ZIP must satisfy before it may be
called `scanned`.

---

## 0. The seven rules that would have prevented most of Dayton

| # | Rule | Born from |
|---|---|---|
| 1 | Recount the live total from the source on the day you report it. Never carry a stored denominator forward. | **D-36** — all seven Dayton ZIP denominators were 17–44% of live; "18% swept" was computed on counts missing two thirds of the market |
| 2 | `comp.py` exit **3** = genuine UNPRICED. Exit **1** = file/check failure and must abort the batch loudly. A harness may never map any non-zero exit to UNPRICED. | **D-39** — an invalid exclusion label made the whole comp file fail, and 46 leads were filed as honest refusals |
| 3 | ARV present + MAO absent = **parse bug**, never a refusal. MAO regex must accept `-?`. | **D-40** — 624 N Broadway St had ARV $177,360 and MAO −$948; the harness read a blank and filed it UNPRICED |
| 4 | A subject needs a **sourced** coordinate before any radius claim. No geocoder, no radius. | **D-37** — 34 leads shared one comp's coordinate and were priced off three Beechwood comps |
| 5 | `radius = None` must print as *no radius applied*. Never print `0.00 mi` for a measurement not taken. | **D-42** — a ZIP-wide run boasted a 1.5 mi radius check it never executed |
| 6 | Close every file before spawning a subprocess; reconcile at least one lead by hand per batch. | **D-38** — an unclosed CSV truncated, and 12% of leads returned UNPRICED with all checks PASS |
| 7 | "Bimodal" needs ≥3 sales on **both** sides of the gap. | **D-41** — one 4,798 sf junk parcel was declared a second market |

## The same class of error in the sheet layer

| # | Rule | Born from |
|---|---|---|
| 8 | `updated_rows: N` is not a receipt. Recount from the sheet. | **D-43** — a 48-row write silently dropped 20 |
| 9 | A row is cleared across **all 18 columns**, not column A only. | **D-44** |
| 10 | Never batch `delete_dimension` from a precomputed index list. One row per call, re-read the ID first. A falling `row_count` proves *a* row went, never *which*. | **D-45** — four live pipeline rows destroyed |

---

## 1. Discovery (before any number exists)

- **Zillow is primary.** Redfin and Realtor.com are cross-checks and must also be read.
  A figure is not "confirmed" because Redfin repeated Zillow — one portal echoing another
  is not a second source. (`references/on-market.md`)
- **Scan by ZIP**, all types, unfiltered. No asking-price cap, no bedroom floor. Those are
  NOT in this repo and inventing them is what made the Dayton coverage numbers meaningless
  (**D-34**, `AUDIT.md` A-7). The buy box caps the **ARV** ($125K–$900K) and the 70%
  ceiling — never the asking price.
- **Read the photos before scoring.** Photos classify condition; listing copy does not.
  If photos cannot be rendered, the lead is `CONDITION UNVERIFIED` — do not quietly
  substitute a Redfin gallery.
- **Record every listing including rejects**, with a reject reason. Count rejects by reason.
- **Coverage is `examined / live_total`.** A ZIP is `scanned` only when they are equal.
  Otherwise it is `partial` and says so.

## 2. Neighbourhood gate (protects the ARV)

- A ZIP is not a hood. Cleveland ZIPs split hard — 44102 alone spans Ohio City, Detroit
  Shoreway, Stockyards, Clark-Fulton, Cudell, Edgewater and more, with medians that are
  not the same product.
- Hood must come from a **named source**: Zillow `## Neighborhood:` block, then
  `Subdivision:` in Facts & features, then OSM `hamlet` (weak, geocodes to street), then
  listing copy (hint only, never proof).
- `UNKNOWN` and `CONFLICT` are terminal for pricing. Record the blank and the reason.
- **Never pool two hoods silently.** If pooling to reach n=3 is the only way to a number,
  say so out loud, justify adjacency and buyer pool, and show what the number would be
  without the pool. (**D-31**; worked example: 9453 McKinney St.)

## 3. Comps

- ARV needs **≥3** comps (`comping/COMPING.md` §0). **Five** is the separate *submission*
  standard (`SKILL.md` rule 2, `comps.py`). Do not confuse them.
- Renovated condition only in the ARV pool. A dated sale sets an as-is floor, never an ARV.
- ±30% sqft band, subject bed count as a floor, ±45% consistency gate that never
  reinstates an outlier.
- Every comp needs **sourced** coordinates. Coordinates estimated by eye void the number.
- A "similar homes" carousel is a **lead** source, never a comp source.
- Hood **sold** feeds are not hood-coherent — mine row-by-row through each comp's own
  breadcrumb, never import a feed as a pool.

## 4. Arithmetic

```
ARV      = subject_sqft x MEDIAN $/sf of the comp set      (one method, no haircut)
CEILING  = ARV x 0.70 - repairs                            (buyer max)
SELLER MAO = CEILING - $10,000                             (the fee, subtracted once)
OFFER LOW  = 0.55 x ARV - repairs
OFFER HIGH = 0.60 x ARV - repairs
```
- Repair tiers **$20 / $35 / $50 per sf** (LIGHT / MODERATE / HEAVY). A repair number with
  no grade is a defect.
- **Never deduct the fee twice.** Never lower the fee to make a deal work — lower the offer.
- A **negative MAO** is a hard walk and is reported as a number, not as a blank.
- **No error band outside a measured market.** The ±40% was measured on Cuyahoga 44102 —
  so Cleveland 44102 is the one place a band may be printed, and even then only if the
  backtest file supports the claim. Everywhere else: `ARV BAND NONE`. (**D-29**)

## 5. Cleveland-specific reality

- Cuyahoga County GIS is live (521,078 parcels, 142 fields) — unlike Wayne County (D-33),
  a real backtest is possible here. `state/backtest/cuyahoga_44102_walkforward.py` exists
  and produces `walkforward_result.json`. **Run it before quoting a Cleveland band.**
- Wayne County lesson does not apply: do not import a Detroit conclusion into Cuyahoga.
- 44102 and 44128 are flagged "strong ZIP" in the ranking weights; 44110 likewise.
  Priority is a *research order*, not a valuation.

## 6. Reporting

Every ZIP report states, in this order:

1. `examined / live_total` and the date the live total was counted
2. rejections counted **by reason**
3. `UNPRICED` rows listed with the failing gate named — a refusal is a deliverable
4. `NEGATIVE MAO` rows listed separately
5. leads by verdict (PRIORITY / MARGINAL / ABOVE-MAO / NO / UNPRICED)
6. what was NOT read (detail pages, photos, cross-checks) and why

**Never claim more listings reviewed than were actually read.**

---

## 7. HOOD-BY-HOOD IS THE ONLY WORKABLE UNIT — measured 2026-11-08

### The coverage ceiling is the fetcher, not the market

`fetch_page` returns roughly **40 cards per feed and then stops**. Chunks beyond that hold
the page footer, not more listings. Measured twice on the same day:

| Feed | Live total | Cards actually retrievable | % |
|---|---|---|---|
| Zillow ZIP `cleveland-oh-44102` | 281 | ~40 (chunks 0–1) | 14% |
| Zillow hood `stockyards-cleveland-oh` | 72 | 41 (chunks 0–5) | 57% |

Consequence: **a ZIP can never be swept to `examined == live_total` by this tool.** A hood
under ~40 listings can be fully covered; a hood above 40 cannot. Report the percentage and
the raw counts every time; never mark a feed `scanned` on a subset.

### Good news: Cleveland hood URLs DO filter

`https://www.zillow.com/stockyards-cleveland-oh/` returned title
`Stockyards Cleveland Real Estate - Stockyards Cleveland Homes For Sale` and a breadcrumb of
`Ohio > Cuyahoga County > Cleveland > Stockyards`. It is a genuine hood feed, not a ZIP
redirect. Unlike Dayton's `/dayton-oh-45405/fairview/` (D-4), the Cleveland slugs work.

**Still confirm on every hood, every time:** the `<title>` must name the hood and the
breadcrumb must end in it. A ZIP-level title means the slug failed.

### The hood feed is NOT ZIP-clean — check every row

The Stockyards feed returned 4 of 41 rows in the wrong ZIP: `3444 W 44th` and
`4501 Hyde Ave` (44109), `3296 W 44th` (44109), and `8162 Russell Ln` (**44144**, 8 miles
away, blank sqft, $12,500 — a plausible manufactured-home listing the buy box excludes).

**Record the ZIP of every row and flag leaks.** A hood feed is a starting point, not a
verified set.

### Verified Cleveland hood slugs (for future sweeps)

Confirmed working: `stockyards-cleveland-oh`.
Named in the Stockyards footer, therefore known-good slugs to test next:
`detroit-shoreway-cleveland-oh`, `cudell-cleveland-oh`, `clark-fulton-cleveland-oh`,
`brooklyn-centre-cleveland-oh`, `west-boulevard-cleveland-oh`, `jefferson-cleveland-oh`,
`edgewater-cleveland-oh`, `ohio-city-cleveland-oh`, `tremont-cleveland-oh`,
`old-brooklyn-cleveland-oh`, `kamms-corner-cleveland-oh`, `north-broadway-cleveland-oh`,
`goodrich-kirkland-park-cleveland-oh`, `south-broadway-cleveland-oh`,
`puritas-longmead-cleveland-oh`.

### Buy box — quoted from `references/underwriting.md`, not from memory

| Item | Value |
|---|---|
| Buyer pricing ceiling | ~70% of ARV (policy: midpoint of 0.65–0.75) |
| ARV range | **$125,000 – $900,000** |
| Types | SFR, **duplex**, **multifamily** — real property only |
| Excludes | manufactured/mobile on leased land, park models, condos, co-ops, REO |
| Condition | Any |
| Comps required (submission) | **Five**. ARV arithmetic needs ≥3 |
| Close | ~21–30 days |
| Terms | Cash or seller financing may be acceptable |

**Screen order is cheapest-first: type → ARV band → condition → comps.** A property failing
type never reaches `comp.py`, and the refusal note names the buy-box line, not the comp gap.

Two traps this creates in Stockyards specifically:
1. **Duplex is IN the box.** Many rows are duplexes and must not be rejected as "multi-family".
   But a duplex needs *same-type* sold comps; an SFR comp set does not price it.
2. **A 2bd/812sf SFR at $90,000 probably cannot reach a $125,000 ARV.** The ARV floor is a
   real reject, separate from the ask price. Small-house rows carry `ARV floor risk`.

### Repair-tier validity gate — apply BEFORE any `comp.py` run

`$20 / $35 / $50` per sf was calibrated on $120–180/sf SFRs. Check `ARV/sf` first:

| ARV $/sf | tier validity |
|---|---|
| ≥ $100/sf | behaves as calibrated |
| $60–100/sf | overstates repairs; needs a walkthrough scope |
| < $60/sf | **invalid — refuse to price** |

Cleveland hoods around $54k–$111k Zestimate medians (North Broadway $54,540, Goodrich-Kirkland
$80,471, Clark Fulton $106,254) sit squarely in the dangerous band. **Compute ARV/sf for every
subject before trusting a repair tier.**

## 8. Sqft integrity — the sweep column is a lead attribute (D-47)

**A search-results card never supplies sqft.** It supplies identity, price, beds, baths and
DOM. Sqft comes from the property page and is checked against public record before the row is
comped.

- **Every shortlisted subject gets its sqft re-verified before pricing.** `3308 W 88th St` swept
  at 1,727 sf from a Zillow card; the page and public record both say **1,155 sf**. That is 33%
  and it moved the ARV by $69,357.
- **Ranking by ask-per-foot ranks by an unverified denominator.** Treat any `$/sf` shortlist as
  provisional. 3308 W 88th fell from 5th-cheapest to 12th once corrected.
- **The direction of the error matters.** An inflated sqft makes an ask look cheaper and
  *promotes* the row through the screen. The defect flatters; it does not fail loudly.
- Redfin property pages retain the **full agent remarks on sold listings**; Zillow strips them.
  Condition evidence for comps therefore comes from Redfin, and `condition` is recorded per comp
  from that text — never inferred from photos, price, or `days on market`. (**D-48**)

## 9. Comps in these hoods are thin — expect UNPRICED

Measured on 3308 W 88th:

- A 180-day window produced **NO COMPS** (2 renovated in band, needs 3).
- 365 days produced exactly **3** — the floor.
- Of 20 candidate sales in radius, **5 were maintained/dated** (barred from ARV), **2 were
  duplexes**, **1 was a 2003 build**, and **4 renovated sales fell outside the ±30% band**.

**Consequence:** in a 44102/44109/44111 hood with a ~1,100–1,300 sf subject, the ARV pool will
routinely be n=3 at the full 12-month window. `UNPRICED` is a legitimate and common outcome here.
Do not widen the band, do not borrow a duplex, do not reinstate the 2003 build.

## 10. Assignability and remarks — the structure gate (D-48)

**Read the full agent remarks on every shortlisted row before comping it.** In one paragraph on
3322 W 54th St the remarks carried both:

- *"No wholesalers and no contract assignments/reassignments"* → **not assignable**; the
  assignment exit is closed and the row is a structural reject, not a discount.
- **1,102 sf** against the Zillow card's **1,916 sf** → 74% sqft defect.

`assignable: yes / no / unstated`. **`unstated` is not `yes`.** Phrases that force a `no`:
"no assignments", "no reassignments", "no wholesalers", "buyer may not assign".

Screen order with this gate inserted:

**type → assignable → ARV band → condition → comps**

### Comping without a home ID — the autocomplete unlock

Redfin **address-only URLs 404** (`/OH/Cleveland/3341-Woodbridge-Ave-44109` returns Page Not Found).
That is not a missing property and it was wrongly treated as one for two passes. Resolve the ID:

```
https://www.redfin.com/stingray/do/location-autocomplete?location=<addr>%2C%20Cleveland%2C%20OH%2044109&v=2
```

The response carries `payload.exactMatch.url` → `/OH/Cleveland/<Street>-<ZIP>/home/<id>`, which
serves the full agent remarks. **Use it before declaring a comp ungradeable**, and check
`payload.sections[].rows` for a `unit-` path: if the property has units it may be a duplex and
belongs outside an SFR comp set.

Grading `02131` took 6 autocomplete calls and 6 property pages and turned three `UNPRICED` leads
into one `PRICED` lead. That is the cheapest unblock in this market.

## 11. Channel 2 — county GIS is live (D-49)

The county endpoint works. **Query it before grinding more retail comps.**

```
/query?where=parcel_zip IN (44102,44109,44111)
       AND foreclosure_flag=1 AND lender='NO LENDER'
       AND total_res_liv_area BETWEEN 1200 AND 2600
&returnCountOnly=true&f=json
```

**Field traps (all fail with 400, never with a wrong number):**
- `parcel_zip` is a **Double** → `parcel_zip=44102`, never `'44102'`
- `foreclosure_flag` is an **int** → `=1`, never `'Y'`
- `lender='NO LENDER'` is the **free-and-clear flag** — the strongest single signal in the dataset
- `grand_total_balance` is **county tax owed, not mortgage**. Do not read it as debt on the house.

**And the sizing rule that decides whether a deal can exist at all:**

```
MAO = sf × (0.70 × hood_$psf − repair_$psf) − fee
```
~~At $121.25/sf and MODERATE repairs that is `sf × $49.875 − $10,000`.~~

**STRUCK 2026-11-08 (D-50, D-51). Do not use that shortcut.** Two independent defects:

1. **Wrong hood.** `$121.25/sf` is one 0.25 mi pocket in `02125`. It is not a 44109, 44111, or even
   a 44102 number. Every lead it was applied to was in a different hood.
2. **Wrong shape.** `$/sf` is **not constant in size.** Over 16 44102 comps:
   `$/sf = 113.1 − 0.0097 × sqft` — roughly **−$1.00/100 sf**. Even inside `02125`, hood-wide is
   **$102.70/sf**, not $121.25.

Compute per hood, per size band, from that hood's own comps. `MAO = sf × (0.70 × hood_$psf − repair_$psf) − fee`
remains the right *form*; it needs a local `$/psf`, and it needs a backtest before the output is
quoted as a band rather than a point.
