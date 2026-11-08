# Comparable sales — the five-comp standard

Five credible sold comps, or the ARV is not supported. There is no third state.

## Comp selection, in priority order

1. Same ZIP code, then immediate neighbourhood
2. Same property type (SFR / duplex / multi / condo)
3. Same bed and bath count
4. Similar living area
5. Similar lot characteristics where relevant
6. Similar age and construction where relevant
7. Sold within the previous 6 months
8. As close to the subject as possible

**Start closest and most similar. Expand only when needed, and say why.** "Expanded
from 44302 to 44303" is a different claim from "expanded to 1.5 miles across a ZIP
line" — the first crosses a submarket and must be justified with a $/sqft comparison.

## Required field per comp

```
Address | Sale price | Sale date | Type | Beds | Baths | Living area
Distance from subject | Source | Direct URL | Condition at sale
Why comparable | Meaningful differences
Verified or reported
```

`Verified` = the county deed record or the listing's own sold record was read.
`Reported` = a secondary site states it. Most Redfin/Zillow sold data is `REPORTED`
for our purposes unless a county record was pulled — say which.

## Never

- Active, pending, or withdrawn listings as sold comps
- A Zestimate as a comp
- A neighbourhood or ZIP average as a substitute for comps
- Renovated and distressed sales averaged silently into one number
- Five comps assembled by lowering the bar until five appeared
- A sale you did not actually open
- Borrowing another submarket's prices because the ZIP has no sales

## Exclusions — these are not comps

| Exclude | Why |
|---|---|
| Deed-restricted / AMI-limited sales | A **floor**, not market value. Two of these understated a deal by $20,000 |
| Newer build in an older block | Different product. A 2020s build at $155/sqft is not evidence for a 1920s subject |
| Condos (unless the subject is a condo) | Different ownership product |
| Non-arm's-length transfers | Quitclaims, family transfers, $1 deeds, a $325 "sale" on a $94,300 house |
| As-is vs renovated mismatch | Keep the renovated set for ARV, the as-is set separately for the floor |

## ARV

Use the **renovated** comps for ARV, the distressed ones for the as-is floor.

```
p75 $/sqft of the chosen comps × subject sqft × 0.88
```

p75 prices the subject as one of the better houses in its own comp set — which is what
it becomes after the work. The 0.88 backs it off. Use both or neither.

Then report, always:

- Which comps are most relevant, and why
- Which comps were down-weighted, and why
- The supported **range** (low / working / high)
- The single **working ARV**
- Confidence: `HIGH` (5+ tight comps, same ZIP, similar size/type, all within 6 months),
  `MEDIUM` (5 comps but one or two weak matches, or a radius expansion),
  `LOW` (fewer than five, or heterogeneous)
- What uncertainty could materially change it

Under five comps: `ARV INSUFFICIENTLY SUPPORTED`. The property cannot be submitted.
Say so in the verdict, not in a footnote.

## Statement about what ARV is

An ARV is a **market-value estimate**, not an appraisal, and not an offer. Every report
says this in those words.
