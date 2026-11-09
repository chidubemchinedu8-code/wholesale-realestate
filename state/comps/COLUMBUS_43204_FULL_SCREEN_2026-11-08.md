# Columbus OH 43204 — on-market full screen, 2026-11-08

First Columbus sweep under this protocol. Order: Zillow primary (196 active in ZIP), Redfin
cross-check (191 active, 54 in the working band), Redfin sold feed (350 in 6 mo, 96 in the
neighbourhood), Zillow property pages for facts and price history, photos via image search.

**Nothing in this file is licensed data.** Every figure was read off a public site and is `REPORTED`.

## Coverage — stated honestly

| item | count | source |
|---|---|---|
| Live active listings, all types, 43204 | **196** | Zillow, read this session |
| Live active, cross-check | **191** | Redfin, read this session |
| Houses only, $40k–$175k — **the working band** | **54** | Redfin filter, 2 pages, read complete |
| Rows in `columbus_43204_sweep_results.csv` | **55** | reconciled to the 54 map pins by price |

**Coverage = 54/196 = 27.6% of the ZIP's active stock, and 100% of the screened band.** This is a
**partial** scan and the word *scanned* is not claimed for 43204. The 142 listings outside the band
were not read; they are condos, 55+ park homes, multifamily, new builds and retail above $175k.

Why a $175k ceiling exists **on the asking side only here**: at the hood's $151/sf renovated median,
a $175,000 ask is $1,159/sf-basis of $1,159 — it already needs the full 0.70 cap with zero repairs.
Anything above that cannot clear a MAO at any repair grade. The ceiling is a *reading order*, not a
buy-box rule, and it is named here so it is not mistaken for one. **D-34 is not being repeated: this
is not an invented filter applied to a coverage claim — coverage is reported against the full 196.**

## Headline

**54 examined → 1 PRICED · 1 MAYBE · 5 UNPRICED · 23 CANDIDATE · 23 REJECT · 2 SEPARATE.**

- **PRICED: 247 S Terrace Ave** — ARV $255,462, MAO-M $118,516 vs $95,000 ask.
  See `COLUMBUS_43204_247_S_TERRACE.md`.
- **MAYBE: 262 S Harris Ave** — the existing 43204 worked example. ARV $169,200, MAO-M $69,240 vs
  $79,900 ask. Already in `property_ledger`; not re-underwritten.
- **23 CANDIDATES are not deals.** They are leads with a size and a price that survive the first
  screen and have no condition evidence yet. Calling them deals is what the Dayton sweep did wrong.
- **23 REJECTS, by reason:** turnkey 6 · size/price 6 · 14-day rule 1 · REO/auction channel 1 ·
  property type 1 · package/multi-property 1 · and the remaining 7 spread across the same codes.

## What the ZIP is made of

Central Hilltop and its neighbours are a **$124–$210/sf renovated market with a $151 median.** The
spread is the whole story: 204 S Wheatland sold at $124/sf and 131 S Eureka at $177/sf, both
renovated, both in band, 0.3 and 0.5 mi apart. That ±20% is why a single point ARV is a screening
number and not a valuation.

The acquisition side is denser than Cleveland's Channel 2 was. 43204 had **54 house listings under
$175k on one day**, against a Cleveland universe built from county delinquency records. Columbus
sourcing here is on-market, not distress-list-driven — which changes the job: the constraint is not
finding leads, it is finding a lead whose **condition is unknown enough to be cheap and known enough
to underwrite.** Most of the 23 candidates fail the second half.

## The blocker to name

**The hood field is the bottleneck, not the comps.** Only 4 of 55 rows carry a verified hood, because
hood comes from the Zillow `## Neighborhood` block on each property page — one page read per lead.
The five renovated sold comps I pulled are all **Central Hilltop**, so any lead in *South Central
Hilltop*, *Hilltop-Wicklow*, *Hilltop*, *Highland West*, *Hillcrest* or *Brookshire* has **no pool
built yet**, and reusing the Central Hilltop pool would be a silent cross-hood pool (D-31).

Concretely: **691 S Warren Ave** would otherwise be the second most interesting lead in the ZIP —
1,288 sf, $102,500, gutted with a new roof — and it is **UNPRICED purely because its own Zillow
neighbourhood is South Central Hilltop.** That is not a failure, it is the gate working.

## Next sweep, in order

1. **691 S Warren Ave** — build the South Central Hilltop pool (5 renovated solds, 6 mo). Highest
   expected value: distress + size + price already align.
2. **133 S Wheatland Ave** $149,000/1,346 sf = $111/sf and **314 N Burgess Ave** $129,900/1,484 sf =
   $88/sf. Cheapest basis in the band. Both need hood + pool.
3. **2-bedroom pool** — 11 candidates are 2bd and the renovated 2bd solds have not been pulled. One
   pool unlocks all of them at once. That is the highest-leverage pull in the file.
4. **446 S Powell, 28 S Warren, 2732 Dibblee, 475 S Richardson** — read the Zillow page, take the
   hood and the photos, grade condition.

## Protocol compliance

- Zillow read first, Redfin second, both read. ✔ (Redfin-only would have been a single-source scan.)
- Every listing recorded **including rejects**, with a reject reason. ✔ 55 rows, 23 rejects coded.
- Coverage is `examined / live_total` = 54/196 and is called **partial**. ✔
- Hood from a **named source only**; `UNVERIFIED` is recorded where unread. ✔ 51 rows say so.
- No ARV without ≥3 renovated comps in the subject's own hood, ±30% sqft, bed floor, ±45% gate. ✔
- Conditions graded from **named upgrades or photos**, never from a generic adjective. ✔
- Photos: Zillow/Redfin image CDNs are blocked in this sandbox (`curl` → 000). Used `image_search`
  on the full address, which is the documented fallback, and said so. ✔
- **Active listings were never used as comps.** Every comp above is a closed sale. ✔
