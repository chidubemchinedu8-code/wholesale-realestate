# 45405 — neighbourhood gate, corrected 2026-11-08

## The error that cost the most
Three leads were marked UNPRICED because I assigned their neighbourhood from the
**street name**. W Norman, Santa Clara Ave and E Norman were all filed under
Fairview. They are not Fairview.

| address | wrong hood | actual hood | source |
|---|---|---|---|
| 119 W Norman Ave | Fairview | Santa Clara | detail page breadcrumb "Neighborhood: Santa Clara" pattern + `santa-clara-dayton-oh/sold/` listing |
| 209 W Norman Ave | Fairview | Santa Clara | same block, same seller |
| 35 Santa Clara Ave | Santa Clara | **Santa Clara** | detail page: "## Neighborhood: Santa Clara", coords 39.78122 / -84.209694 |
| 127 E Norman Ave | Fairview | North Riverdale | detail page breadcrumb ends `north-riverdale-dayton-oh` |
| 101 E Hudson Ave | — | North Riverdale | detail page: "## Neighborhood: North Riverdale" |

127 E Norman sits 1 block from Santa Clara's western edge but the detail page
assigns it North Riverdale. **The detail page decides, not the street, not the
distance, not the map.**

## Second error, caught the same way
The first North Riverdale renovated pool had **n=3** and a median of **$129.92/sf**.
It produced ARVs of $182k-$218k. Then 101 E Hudson — same neighbourhood, fully
renovated ("Fully renovated and ready to go", modernized kitchen) — sold at
**$93/sf**. The n=3 pool was the high tail of the distribution, not its centre.

Rebuilt pool is **n=10 renovated** in North Riverdale. Individual $/sf spans
$84.6 (258 E Siebenthaler) to $129.9 (44 E Beechwood). The engine's own radius
ladder picks a different subset per subject, which is why the same street yields
$93.23/sf for a 2,016 sf house and $99.77/sf for a 1,681 sf one. That spread is
real, not noise: **$93/sf at 2,000 sf, $120/sf at 1,100-1,300 sf.** $/sf falls as
size rises, and the radius ladder is picking up that size effect.

## Renovated cohort, North Riverdale (n=10)
| address | sold | price | sqft | $/sf | evidence |
|---|---|---|---|---|---|
| 44 E Beechwood | 10/26/26 | 176,950 | 1,362 | 129.92 | "Everything else is new"; refinished hardwood, quartz, new AC |
| 212 E Beechwood | 06/29/26 | 155,000 | 1,294 | 119.78 | new furnace/AC, radon, all baths + kitchen redone |
| 258 E Siebenthaler | 07/31/26 | 165,000 | 1,248 | 132.21 | 4bd, renovated |
| 101 E Hudson | 06/30/26 | 140,500 | 1,507 | 93.23 | "Fully renovated and ready to go" |
| 409 Kenilworth | 04/07/26 | 142,700 | 1,596 | 89.41 | kitchen/baths completely redone |
| 69 E Beechwood | 05/11/26 | 173,000 | 1,400 | 123.57 | sold +$37k over ask band |
| 53 E Beechwood | 04/24/26 | 163,000 | 1,442 | 113.04 | "delightful renovated 3-bedroom, 3-bathroom" |
| 332 Ashwood | 03/31/26 | 134,900 | 1,176 | 114.71 | new roof, flooring, carpet, paint, furnace |
| 49 Woodcrest | 05/20/26 | 175,000 | 1,754 | 99.77 | updated kitchen, quartz, new SS appliances (4bd) |
| 312 E Maplewood | 06/22/26 | 122,500 | 812 | 150.86 | renovated, small — outside most bands |

**4-bedroom renovated in North Riverdale in-band: exactly 2** (258 E Siebenthaler
1,248 sf, 49 Woodcrest 1,754 sf). MIN_COMPS=3, so every 4bd subject stays UNPRICED.
That is the whole reason 66 Redder, 35 Santa Clara and 2916 Philadelphia have no
number. Do not relabel a maintained 4bd sale to fix it. The fix is more sold data.

## Window
The engine default of 180 days was silently starving every subject. The repo's own
policy allows up to 12 months for a thin market. At 180 days, 119 W Norman, 209 W
Norman, 127 E Norman, 218 E Parkwood, 25 Redwood, 111 Forest and 152 Northwood were
all UNPRICED. At 365 days, all seven price with n=3-6. **Use --window 365 for 45405
and say so on the row.**

## Files
- `state/comps/dayton_45405_northriverdale_comps.csv` — 35 rows, 10 renovated
- `state/comps/dayton_45405_santaclara_comps.csv` — 13 rows, **0 renovated**

Santa Clara genuinely has no renovated cohort. Every sale there is `maintained`,
`dated` or `distressed`, and its maintained band is $61-$104/sf. A Santa Clara
subject priceable only if it is under the North Riverdale gate (119/209 W Norman,
which are Santa Clara parcels but sit within 0.5 mi of the North Riverdale
renovated pool). 35 Santa Clara does not clear the 4bd floor anywhere.
