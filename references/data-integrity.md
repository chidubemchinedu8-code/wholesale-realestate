# Data integrity and anti-hallucination

The rules that make every other reference trustworthy. A number that cannot be
sourced is `UNKNOWN`, and `UNKNOWN` stops the analysis.

## Five labels. Use them on every material claim.

| Label | Meaning |
|---|---|
| `VERIFIED` | Directly supported by a primary source you actually read (county record, the listing itself, a contractor bid) |
| `REPORTED` | A source states it and you did not independently confirm it |
| `ESTIMATED` | Calculated from available evidence |
| `ASSUMED` | An explicit underwriting assumption, stated so it can be challenged |
| `UNKNOWN` | Unavailable or not established |

## Provenance ledger

Every important factual claim keeps its source URL and the date checked. Put it in the
report as a short table, not a vague "sources: Zillow, Redfin":

```
Claim                              | Value        | Label    | Source URL        | Checked
Asking price                       | $95,000      | VERIFIED | redfin.com/...    | 2026-11-08
Sold 135 Byers Ave                 | $100,000     | REPORTED | redfin.com/...    | 2026-11-08
DOM                                | 3            | VERIFIED | redfin.com/...    | 2026-11-08
Repairs                            | $55k–$75k    | ESTIMATED| photo set (6)     | 2026-11-08
Buyer max                          | $18,394      | ESTIMATED| this file         | 2026-11-08
Seller motive                      | unknown      | UNKNOWN  | —                 | —
```

Two sources where possible. When they disagree: show both values, name the more
reliable one and why, and **never silently pick the number that makes the deal look
better**. A $10,000 disagreement between Zillow and the county record is a finding, not
an inconvenience.

## Never

1. Invent a property address.
2. Invent a listing URL.
3. Invent a sold price or sale date.
4. Invent property characteristics (sqft, beds, baths, year, lot).
5. Invent days on market or price reductions.
6. Invent owner information — name, phone, email, equity, motivation.
7. Invent a repair observation.
8. Invent buyer approval.
9. Invent a seller's motivation.
10. Present an estimate as a verified fact.
11. Present an active listing as a sold comp.
12. Use a neighbourhood average as a substitute for comps.
13. Claim to have opened photos you did not open.
14. Claim to have swept a ZIP you only sampled.
15. Call a property a deal because it is cheap.
16. Hide missing data.
17. Silently substitute a source when the required one is unavailable.
18. Fabricate a result to make a report look productive.

## When tools fail

If a site will not load, a filter silently fails, a page returns a captcha, or a
search returns nothing usable: **stop that analysis and say so.** Report what you
attempted, what came back, and what is therefore unknown. A clear "Zillow filters are
ignored, so these prices are `UNKNOWN`" is a finished answer. A silent switch to a
different source is a lie with a citation.

## Language rules

- "Zillow's ZIP filters are ignored; its property pages work" — not "Zillow is broken".
- "MLS-sourced data read through Redfin" — not "MLS access".
- "The comp set supports $118K–$132K" — not "the ARV is $125K" without the range.
- "No sold duplex in this ZIP in six months, so unpriced" — not a bracket from five
  miles away.
- "Fits the stated buy box" — not "the buyer will buy it".

## Self-audit before sending any report

```
[ ] Every address and URL in the report was actually opened
[ ] Every sold price has a source and a date
[ ] Every ARV states n, radius, ZIP, confidence
[ ] Every repair line has an observed or reported basis
[ ] Every claim carries one of the five labels
[ ] Buyer max and seller MAO are shown as separate numbers
[ ] Gross spread is labelled gross
[ ] Every ZIP reports reviewed-of-total, and zero where zero
[ ] No property appears twice as new
[ ] The verdict is one of the three, with a reason
```
