# 45405 / 45403 neighbourhood correction — 2026-11-08

**This file previously claimed the opposite of what follows.** An earlier version
argued that 119 and 209 W Norman were Santa Clara parcels that could still be priced
off the North Riverdale pool "because they sit within 0.5 mi of it". That was wrong,
and `comping/COMPING.md` says so in one line:

> Same neighbourhood code, identical. Not nearby. Not similar. Identical.

There is no distance exception. n=1 is UNPRICED. This file now records only what was
verified, and what it invalidated.

## Rule

Neighbourhood comes from **Zillow's `## Neighborhood:` block or the breadcrumb
(`…/45405/<Hood>/<Address>`)**, else OpenStreetMap's `display_name`. It never comes
from the listing description, the street name, a subdivision name, or distance to a
hood centre. Each of those produced a wrong answer at least once.

Coordinated rule: a comp needs a **sourced coordinate**. Hand-estimated coordinates
were found to be 0.25–0.50 mi off across this pool.

## Leads whose neighbourhood was wrong

| Lead | Was gated as | Verified hood | Source |
|---|---|---|---|
| 124 Victor Ave | North Riverdale | **Santa Clara** | Zillow `## Neighborhood:` |
| 119 W Norman Ave | North Riverdale | **Santa Clara** | Zillow breadcrumb |
| 209 W Norman Ave | North Riverdale | **Santa Clara** | Zillow breadcrumb |
| 2015 N Main St | North Riverdale | **Santa Clara** (subdiv. Elmwood) | Zillow breadcrumb |
| 111 Forest Ave | North Riverdale | **Grafton Hill** | listing text + OSM |
| 25 Redwood Ave | North Riverdale | **45405 / Northwoods** | Zillow hood string |
| 152 Northwood Ave | North Riverdale | **45405 / Northwoods** (subdiv. Northwoods) | Zillow hood string + OSM |
| 66 Redder Ave | North Riverdale | **45405 / Northwood** | Zillow hood string |
| 35 Santa Clara Ave | North Riverdale | **Fairview** | OSM |
| 2916 Philadelphia Dr | North Riverdale | **Harrison Township** | OSM — outside the city hood system |

**124 Victor is the instructive one.** Its own listing remark reads "near the ever
expanding and rejuvenating North Riverdale community". Agent marketing is not a
neighbourhood. Zillow's `## Neighborhood:` field says Santa Clara, and that governs.

## Comp rows removed from the North Riverdale pool

| Comp | Was gated as | Verified hood | Source |
|---|---|---|---|
| 409 Kenilworth Ave | North Riverdale | **Daytonview** | OSM; stored coord was 0.5 mi off |
| 49 Woodcrest Ave | North Riverdale | **Fairview** | OSM |

Pool goes from 10 renovated comps to **8**. Both removals were `renovated`, so they
were carrying ARV weight.

## Consequence by neighbourhood

- **Santa Clara — n=1, cannot produce an ARV.** The full 127-sale Santa Clara feed was
  read. Exactly one sale is renovated: 202 Santa Clara Ave, $125,400 / 1,302 sf /
  $96.31 per sf. Every other candidate failed on condition or size:
  55 W Norman (no condition data), 147 Niagara (sold as-is), 136 Niagara (no condition
  language), 123 W Hudson (no renovation language), 96 & 87 W Hudson (multifamily),
  129 Marathon (the $119,197 "sale" was a foreclosure; Zillow now lists it bank-owned
  at $55,000), 104 W Norman, 138 W Norman (non-arm's-length), 302 Fountain and
  321 W Norman (out of band).
  **124 Victor, 119 W Norman, 209 W Norman, 2015 N Main are therefore UNPRICED.**
  Their previously published ARVs ($203,454 / $167,717 / $174,504 / $187,955) are
  withdrawn.
- **North Riverdale — n=8 renovated, verified.** Four leads price cleanly:
  152 E Parkwood, 218 E Parkwood, 127 E Norman, 2326 Parkland.
- **Burkhardt — newly built.** 141 S Torrence and 633 Huffman are Burkhardt, not East
  Dayton. A 4-comp pulled pool supports both. The `$105.41/sf` figure previously
  quoted for 45403 was **one comp (15 Parnell) repeated three times**, not a median.
- **Grafton Hill, Northwoods/45405, Fairview — no pool built.** Leads in those hoods
  stay unpriced until one exists.
- **Bed-floor failures** (66 Redder, 35 Santa Clara, 2916 Philadelphia) fail the 4-bed
  rule on top of the hood problems above.

## North Riverdale renovated pool, current state

| Comp | Price | Sqft | $/sf | Verified coord |
|---|---|---|---|---|
| 44 E Beechwood Ave | $176,950 | 1,362 | $129.92 | 39.7902448, −84.2120874 |
| 212 E Beechwood Ave | $155,000 | 1,294 | $119.78 | 39.7902698, −84.2080889 |
| 258 E Siebenthaler Ave | $165,000 | 1,248 | $132.21 | 39.7984764, −84.2129620 |
| 101 E Hudson Ave | $140,500 | 1,507 | $93.23 | 39.7843250, −84.2062810 |
| 69 E Beechwood Ave | $173,000 | 1,400 | $123.57 | 39.7904105, −84.2118458 |
| 312 E Maplewood Ave | $122,500 | 812 | $150.86 | 39.7920002, −84.2079874 |
| 53 E Beechwood Ave | $163,000 | 1,442 | $113.04 | 39.7904082, −84.2121811 |
| 332 Ashwood Ave | $134,900 | 1,176 | $114.71 | 39.7975686, −84.2096566 |

Note the spread: $93.23 to $150.86 per sf. That is why the median method matters and
why no single comp should ever be quoted as "the" $/sf.

## Reproduce

```
python3 scripts/comp.py \
  --comps state/comps/dayton_45405_northriverdale_comps.csv \
  --as-of 2026-11-08 --window 365 \
  --subject '{"address":"127 E Norman Ave","hood":"45405-NORTH RIVERDALE",
              "sqft":1188,"beds":"3 bd","lat":39.7855184,"lon":-84.2064888,
              "style":"TRADITIONAL"}'
```

Exit 0 = priced, 3 = UNPRICED, 1 = comp-file error.

---

## Pass 3 - seven further leads off the 118-listing 45405 ZIP feed (2026-11-08)

The `/dayton-oh-45405/fairview/` URL **silently redirects to the whole-ZIP feed**, which
serves 118 listings. That feed, plus the "similar homes" carousels on the detail pages of
leads already in the book, produced seven more priceable subjects. All seven were gated
on hood before they were priced, and all seven passed as **North Riverdale**.

| Subject | Sqft | Ask | ARV | Median | n / radius | Spread | Repairs | Ceiling | MAO | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| 27 Cliff St (FSBO) | 1,466 | $60,000 | $181,156 | $123.57 | 3 / 0.25 mi | 6.8% TIGHT | MOD $51,310 | $75,499 | **$65,499** | **PASS (+$5,499)** |
| 104 E Beechwood Ave | 1,479 | $80,000 | $179,961 | $121.68 | 4 / 0.25 mi | 5.8% TIGHT | HEAVY $73,950 | $52,023 | $42,023 | NEGOTIATE |
| 55 Ashwood Ave | 1,488 | $85,000 | $181,056 | $121.68 | 6 / 0.75 mi | 10.2% TIGHT | MOD $52,080 | $74,659 | $64,659 | NEGOTIATE |

### Why only three of the cheap ones were priced

- **420 Geyer St** ($85,000, 3/1, 1,128 sf) - OSM puts it in **McPherson Town Historic
  District / Riverdale**, not North Riverdale. Not pooled.
- **1315 Riverside Dr** ($76,900) - OSM: **Riverdale**. Not pooled.
- **129 Marathon Ave** ($55,000, 153 DOM) - OSM: **Fairview**. Not pooled.
- **252 Marathon Ave** ($60,000) - OSM: **Fairview**. Not pooled.
- **421 Delaware Ave** ($79,000, 4bd) - OSM: **Daytonview**, and the 4-bed floor bites.
- **228 W Fairview Ave** ($175,000) - 3 DOM, priced like a finished product, not a deal.

### Grade notes that change the answer

**27 Cliff St** is the first row in this book that clears the bar on the *asking price*
with no negotiation: MAO $65,499 against a $60,000 ask. Treat it as conditional, not
banked. The FSBO listing publishes no condition detail whatsoever, so the moderate grade
is an assumption. At HEAVY ($73,300) the MAO collapses to $43,509 and the row inverts.
Grading it correctly is worth $22,000 of negotiating room.

**104 E Beechwood** says "needs complete repair and total renovation" and "beware while
walking through the property". That is a gut job and it is graded heavy. Its 87 DOM
overstates motivation: it was off market from 4/1 to 8/13, so it has 73 days of true
marketing.

### Reproduce

```bash
python3 scripts/comp.py \
  --comps state/comps/dayton_45405_northriverdale_comps.csv \
  --subject '{"sqft":1466,"hood":"45405-NORTH RIVERDALE","lat":39.7925696,"lon":-84.2156301,"style":"TRADITIONAL","beds":3}' \
  --as-of 2026-11-08 --window 365
# then feed the printed ARV back in literally:
python3 scripts/comp.py ... --tier moderate --repairs 51310 --offer <ARV> --ask 60000
```

---

## Pass 4 - Fairview pool built and REFUSED (2026-11-08)

`state/comps/dayton_45405_fairview_comps.csv` now exists. It contains **every 45405
transaction on the Fairview sold feed** - five rows - and the engine will not price
anything off it. That is the correct answer, not a gap to be filled.

| Comp | Sold | Price | Sqft | $/sf | Bd | Condition |
|---|---|---|---|---|---|---|
| 2041 Mayfair Rd | 2026-08-21 | $155,000 | 1,488 | $104.17 | 4 | maintained |
| 510 W Fairview Ave | 2026-10-19 | $60,000 | 1,008 | $59.52 | 3 | maintained |
| 2064 Rustic Rd | 2026-11-06 | $50,100 | 1,312 | $38.19 | 2 | dated |
| 618 W Fairview Ave | 2026-04-02 | $56,600 | 1,350 | $41.93 | 4 | dated |
| 2024 Rustic Rd | 2026-05-14 | $20,000 | 1,296 | $15.43 | 3 | shell |

**Zero rows are `renovated`.** Fairview's 45405 sales are $15-$104/sf and the two
highest are a 4-bed (above a 3-bed subject's bed floor is fine, but it is the ONLY
3+-bed sale above $100/sf) and the rest are $15-$60/sf distressed trades.

### What that means

`MIN_COMPS=3` cannot be met from a renovated cohort in Fairview, so **every Fairview
subject stays UNPRICED**: 144 Niagara Ave ($120,000), 129 Marathon Ave ($55,000, 153 DOM),
252 Marathon Ave ($60,000), 35 Santa Clara Ave ($84,900).

Substituting North Riverdale comps would produce a number - roughly $120-$132/sf against
Fairview's own $38-$104/sf - and that number would be wrong by roughly 2-3x. This is
exactly defect D-1 restated. Do not do it.

### Cost of the finding

Fairview is the second-largest active hood in the 45405 feed and it is **unpriceable by
this method**. That is a real limitation of the ARV model, not a data-collection failure:
the neighbourhood has no renovated-sale cohort to anchor to. If renovators start trading
there, the pool becomes buildable - so re-mine `/fairview-dayton-oh/sold/` periodically
rather than treating this as permanently closed.

### Reproduce

```bash
python3 scripts/comp.py --comps state/comps/dayton_45405_fairview_comps.csv \
  --subject '{"sqft":1055,"hood":"45405-FAIRVIEW","lat":39.7798360,"lon":-84.2117102,"style":"TRADITIONAL","beds":3}' \
  --as-of 2026-11-08 --window 365
# -> exit 3, "NO COMPS ... do not widen further, do not average"
```
