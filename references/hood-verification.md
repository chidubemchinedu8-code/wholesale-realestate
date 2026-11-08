# Neighbourhood verification — the gate that protects the ARV

`comping/COMPING.md` says it in one line: *"Same neighbourhood code, identical. Not
nearby. Not similar."* This file is the operating procedure for actually establishing
that, because getting it wrong is the single most expensive mistake this system has made.

**A wrong-hood ARV is worse than a blank.** A blank gets re-worked. A wrong-hood number
gets quoted to a seller and then defended.

---

## 1. Why this file exists

A Dayton 45405 pass priced nine leads off a North Riverdale comp pool without checking
which neighbourhood each subject was actually in. On re-gate, **every one of nine** was in
a different hood:

| Subject | Assumed | Actually | Source |
|---|---|---|---|
| 124 Victor Ave | North Riverdale | Santa Clara | Zillow breadcrumb |
| 119 W Norman Ave | North Riverdale | Santa Clara | breadcrumb |
| 209 W Norman Ave | North Riverdale | Santa Clara | breadcrumb |
| 2015 N Main St | North Riverdale | Santa Clara (subdiv. Elmwood) | breadcrumb |
| 111 Forest Ave | North Riverdale | Grafton Hill Historic | listing copy |
| 25 Redwood Ave | North Riverdale | Northwoods (45405) | Zillow hood string |
| 152 Northwood Ave | North Riverdale | Northwoods (45405) | Zillow hood string |
| 66 Redder Ave | North Riverdale | Northwoods (45405) | breadcrumb |
| 35 Santa Clara Ave | North Riverdale | Fairview | OSM |
| 2916 Philadelphia Dr | North Riverdale | Harrison Township | OSM |

Two comps in the pool were also wrong-hood and had to be thrown out entirely: **409
Kenilworth** (Daytonview) and **49 Woodcrest** (Fairview).

The root cause was not carelessness about arithmetic. It was that *"45405" was treated as
a neighbourhood.* A ZIP is not a hood. Dayton 45405 contains at least fourteen distinct
neighbourhoods, and their medians differ by more than 2x:

North Riverdale $76,869 · Fairview $79,975 · Santa Clara $66,323 · Five Oaks $88,512 ·
Cornell Heights $78,835 · Hillcrest $88,873 · Riverdale $65,430 · **Grafton Hill $128,435**
· Old Dayton View $120,767 · Dayton View Triangle $132,589 · Daytonview · Northwoods ·
College Hill $103,367 · Southern Dayton View $48,455 · Wesleyan Hill $84,365

Pricing a Santa Clara house off North Riverdale comps is not a rounding error. It is a
different product.

---

## 2. The rule

**No subject is priced until its neighbourhood is established from a named source, and
that source is written down next to the number.**

Three states a hood can be in, and only two of them permit pricing:

| State | Permitted action |
|---|---|
| `VERIFIED` — named source, subject inside that hood | price it |
| `UNKNOWN` — sources disagree, or none resolves it | **do not price it.** Record the blank with the reason |
| `CONFLICT` — two sources give different hoods | do not price until resolved; record both |

Never "pick the nearest hood", never "borrow the pool", never average two hoods.

---

## 3. Source hierarchy — use in this order

1. **Zillow detail page `## Neighborhood:` block.** Authoritative. It renders near the
   bottom of **chunk 1** of the detail page, after the schools and flood-zone sections.
   It states the hood in plain text, e.g. `## Neighborhood: North Riverdale`.
2. **Zillow listing breadcrumb / hood string.** Second best. A breadcrumb of `45405` with
   no hood name is **not** a hood — it is a refusal, and it means Northwoods or similar
   unmapped area.
3. **OSM / Nominatim** via `fetch_page` on
   `https://nominatim.openstreetmap.org/search?q=<address>&format=json&addressdetails=1&limit=3`.
   Read `address.hamlet` (and `address.neighbourhood` if present) in `display_name`.
4. **Listing copy self-identification** only as a hint — "near the rejuvenating North
   Riverdale community" is agent marketing, not a hood. 124 Victor Ave is the canonical
   example of copy lying about location.

### OSM is a weaker source than the Zillow neighbourhood block, and it fails in two ways

- **It geocodes to the street, not the parcel.** A query for `23 E Parkwood Dr` returns
  the *road* `West Parkwood Drive` tagged `Fairview`. The Zillow block for the same
  property says `North Riverdale`. **The Zillow block wins.** Record the loser rather than
  silently discarding it, so the conflict is auditable.
- **A missing hood is not evidence of a different hood.** When Nominatim returns no
  `hamlet`, the answer is `UNKNOWN`, not "somewhere else". 127 Iroquois Ave has no hood in
  its `display_name`; it is North Riverdale on the Zillow block.
- **Street-level fallback is misleading.** `218 E Parkwood Dr` returned `[]`. Only trust
  hits whose `addresstype` is `place` or `house` **and** whose `house_number` matches.
- **A municipality is not a neighbourhood.** `4020 Daleview Ave` returns
  `municipality: Harrison Township`, not a `hamlet`. That is a real, useful answer: the
  parcel is outside Dayton's hood system and no Dayton comp pool applies to it. Do not
  round it to the nearest Dayton hood. Same for `2916 Philadelphia Dr`.
- **An empty array is a lookup miss, not a hood.** `251 Castlewood Ave` and
  `4041 Old Riverside Dr` both return `[]`. Record `hood UNKNOWN` and do not price.
  Do **not** infer the hood from nearby listings or from the ZIP.

### When every source fails, the answer is UNKNOWN

`251 Castlewood Ave` ($69,900, 2/1, 912 sf) is the worked example: OSM `[]`, no Zillow
`## Neighborhood` block captured, and a 2bd bed count that already fails the bed floor.
Two independent reasons not to price it. **`hood UNKNOWN` is a terminal state for that
row** — it is not a prompt to guess, and it is not cleared by a provider later offering a
ZIP-level guess.

---

## 4. The trap: hood URLs that do not filter

**`https://www.zillow.com/dayton-oh-45405/<hood-slug>/` silently redirects to the whole
ZIP feed whenever the slug is not a real supported region.**

This wasted more time than any other single error. `/dayton-oh-45405/fairview/` returns
the **full 118-listing 45405 feed**, not Fairview. The response still looks correct — it
has listings, a title, a result count — so it is easy to believe you filtered when you
did not.

**Always confirm a hood URL actually filtered** by checking that the result count is
plausible for a neighbourhood and that the breadcrumb/title names the hood. If the title
reads `45405 Real Estate - 45405 Homes For Sale`, you got the ZIP, not the hood.

Verified-working hood slugs: `north-riverdale-dayton-oh`, `santa-clara`.
Verified-broken: `northwood` (404). `fairview-dayton-oh` **sold** feed leaks 45406.
`grafton-hill-dayton-oh` **sold** feed leaks Brookville 45309.

---

## 5. Hood *sold* feeds are not hood-coherent — never pool one wholesale

Active feeds are usually coherent. **Sold feeds are not.** Observed on 2026-11-08:

- `fairview-dayton-oh/sold/` — 116 transactions, rows are **45406** addresses
  (1254 Brentwood, 2071 Auburn, 2015 Emerson, 1955 Rugby). Not Fairview at all.
- `grafton-hill-dayton-oh/sold/` — 28 results, leaked **Brookville 45309**.

Mine these row-by-row through each comp's own detail-page breadcrumb, and reject every
row whose breadcrumb does not name the subject's hood. Never import a feed as a pool.

---

## 6. Comp pool hygiene

- Every comp needs **sourced coordinates**, not hand-estimated ones. A historical pool had
  coordinates estimated by eye that were 0.25–0.50 mi off; correcting them changed radii,
  medians and verdicts. **Any number produced before the coordinates were sourced is
  void** — say so explicitly rather than quietly recomputing.
- Any comp that fails the hood gate is removed from the pool with an `exclusion` reason,
  not merely ignored. Use the `EXCLUSION_REASONS` keys:
  `deed_restricted, new_build, non_arms_length, condo, not_sold, different_tier`.
  An unknown `exclusion` label aborts `comp.py` with exit 1.
- A "similar homes" carousel is **not** a comp source (127 Stainton → Springfield), but it
  *is* an excellent **lead** source. Use it for discovery, never for ARV.

---

## 7. Checklist — run before any ARV is quoted

```
[ ] Subject's hood established from a NAMED source, and the source is written next to the number
[ ] If Zillow hood block and OSM disagree: Zillow wins, both recorded
[ ] If no source resolves the hood: row is UNPRICED with "hood unresolved" as the reason
[ ] Hood URL, if used, confirmed to have actually filtered (title names the hood)
[ ] No comp in the pool is off-hood; removals carry an exclusion reason
[ ] Every comp coordinate is sourced, not estimated
[ ] Any ARV computed before coordinates were sourced has been withdrawn, not silently updated
```
