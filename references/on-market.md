# On-market sourcing (primary channel)

## Source priority — Zillow first, Redfin second

**Zillow is the primary manual discovery reference. Redfin is a secondary
cross-check.** Discovery happens on Zillow property pages, read by a human (or by
a fetcher reading the page as a human would). Redfin is opened afterwards to
confirm or contradict what Zillow showed — DOM, sold records, agent detail.

Do not invert this. Do not treat "the Zillow filter URL failed" as "Zillow is
unusable": the filter form is unreliable, the property page is not. And do not
report a figure as confirmed because Redfin repeated it — one portal repeating
another portal is not a second source.

Neither site is licensed data. Everything read here is `REPORTED`. See
`references/data-access.md` for what a licensed feed would change.

Scan **by ZIP**, never by browsing a whole city.

## Source reality — tested, not assumed

| Source | Works | Does not work |
|---|---|---|
| **Zillow property pages (primary)** | Zestimate, rent estimate, price history, MLS number, comp blocks, beds/baths/sqft/lot, features | — |
| **Zillow ZIP-level filters (primary)** | — | `/25000-115000_price/` style filters return unfiltered results. Do not trust a Zillow filter URL |
| **Redfin `zipcode/<ZIP>/filter/include=sold-6mo` (cross-check)** | Sold filters, bed filters, city-level `max-price`/`min-beds`, detail pages with MLS#, DOM, agent name/email/phone | Multi-family filter silently fails on several ZIPs; only ~24 results per page and the tail lazy-loads |
| **Redfin `recently-sold` (cross-check)** | Sold list with dates and prices | No radius filter — it is ZIP-bounded |
| Realtor.com | — | `type-sold` ignored, serves a reCAPTCHA. Not used |
| MLS direct | — | No licence, no credentials. Zillow/Redfin sold data *is* MLS-sourced; say "read through a public site", never "MLS access". Licensing route: `references/data-access.md` |

If a filter silently fails, **notice it and say so**. The failure mode that cost a
whole Akron screen was generalising "Zillow's filters are broken" into "Zillow is
unusable", when property pages worked fine.

## Listing priorities — score, then decide

| Signal | Weight | Evidence needed |
|---|---|---|
| 60+ days on market | 20 | DOM on the listing card or detail page |
| 30–59 days on market | 12 | same |
| Price reduction(s) | 15 | reduction amount and date, or `observed` count from price history |
| Back on market | 10 | "back on market" status, or a prior pending → active transition |
| As-is / fixer / TLC language | 10 | quoted listing sentence |
| Dated interiors in photos | 10 | which photo shows what |
| Visible deferred maintenance | 10 | exterior/interior photo evidence |
| Estate / inherited / probate | 8 | listing text |
| Priced below renovated comps in the ZIP | 15 | asking vs the ZIP's renovated $/sqft |
| Absentee / out-of-state owner (if shown) | 5 | listing or county record |

Score out of 100 for research ordering only — it is not a valuation.

## Default rejections

Reject unless the evidence in the right column is present and recorded:

| Reject | Only exception |
|---|---|
| Under 14 days on market | Documented substantial mispricing: asking < 65% of the ZIP's renovated $/sqft ARV, or a verifiable distress event (auction date, probate, divorce filing) |
| Turnkey / fully renovated / retail-ready | None — there is no wholesale spread in retail pricing |
| Asking at ordinary retail market value | None |
| Insufficient comparable sales | None — this is the five-comp rule |
| Condition or value not assessable | None — `UNKNOWN` condition cannot be underwritten |
| Bank-owned / REO | Excluded from normal results; report separately only if explicitly requested |
| Multi-family/duplex with **zero** same-type sold comps in 6 months | Keep the lead, mark `UNPRICED`, do not present as a deal |

A single exterior photo is not a rejected property; it is a `POTENTIAL` property with
an unresolved condition question and a named path to get photos.

## Per-ZIP scan procedure

1. Pull active listings for the ZIP under the market's price band, all types.
2. Record every listing's address, price, DOM, status, reductions, beds/baths/sqft,
   and URL — including the ones you reject, with the rejection reason.
3. Apply the rejections above. Count the rejects by reason for the ledger.
4. For survivors, open the detail page and the full photo set.
5. Classify condition (`condition.md`). No classification, no shortlist.
6. Only then does the property move to comps.

## Coverage honesty

Report `x of y active listings reviewed` for every ZIP. A sweep of page 1 of 5 is
"page 1 of 5", not "the ZIP is done". If you sampled, say you sampled.

## Report zero

If a ZIP has no qualifying property, write `0 qualifying properties` and move on.
That is a complete, acceptable, and expected result. Padding the list is the failure.
