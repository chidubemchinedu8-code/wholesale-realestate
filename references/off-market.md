# Off-market sourcing (second channel)

Source: PropWire. This channel produces **unpriced leads with a ceiling**, not deals.

## What is reachable, and what is not

PropWire's search is a client-side app: without a logged-in session it renders the
filter shell and "0 Results". Property-detail URLs need an internal numeric ID and
return 404 without one. County GIS layers *are* queryable where published (Cuyahoga's
parcel layer is, with 142 fields including `foreclosure_flag`, `cert_sold_flag`,
`last_transfer_date`, `last_sales_amount`, `grand_total_balance`, `neighborhood_code`).

**State which of the two you actually used.** A county GIS pull is not a PropWire pull,
and a filtered Redfin search is neither.

### Sandbox reachability — tested 2026-11-08

| Target | From the Arena sandbox |
|---|---|
| Redfin (listings, sold-6mo, detail pages) | **Works** |
| Zillow property pages | Works via a fetcher; ZIP filters are ignored |
| `gis.cuyahogacounty.gov/server/rest/services/CCFO/Parcel_Fabric_Taxparcels/FeatureServer/0` | **WORKS — corrected 2026-11-08 (D-49).** Returns live JSON, 142 fields. The earlier "blocked" note tested a path (`/arcgis/rest/services`) that does not exist on this server; a 404 is a *successful* handshake |
| PropWire search | Not usable without a logged-in session |

The Cuyahoga block is the same one recorded in `leadgen/README.md`: DNS resolves and
TCP connects, then ClientHello dies. The working pattern is the existing
`.github/workflows/leadgen-pull.yml` — run the county pull on a GitHub Actions runner
and commit the CSV back to the branch. **Do not report "the county has no data" when
the truth is "this sandbox cannot reach the county."** Those are different claims.

## Signals

| Signal | Strength | Notes |
|---|---|---|
| Pre-foreclosure (lis pendens / notice of sale) | Strong | A clock, not a guarantee. Verify the case, not just the flag |
| Tax-delinquent / tax-lien sold | Strong | Owes money; may still refuse to sell |
| Vacant | Strong | Combined with absentee it is the strongest pair |
| Absentee owner / out-of-state mailing | Medium | Combined with long tenure it means tired landlord |
| High equity / free-and-clear | Medium | No mortgage floor — the only seller who can say yes to a steep number |
| Probate / estate (`ESTATE`/`HEIR`/`ET AL`/`LIFE EST` in owner name) | Medium | Name proxy, not a docket. Misses plain-name estates, catches mere co-owners |
| City code violations | Medium | Premium source usually; verify locally |
| Long tenure (10+ years) | Medium | Deferred maintenance, large equity, unmarketed |

**One flag is not motivation.** Rank on **stacked** signals. A pre-foreclosure with an
absentee out-of-state owner and a sold tax lien is a different phone call from a
`ET AL` owner who is simply a co-owner.

## The scoring model

Use the repo's existing, tested weights rather than inventing new ones:

```
40 pre-foreclosure + 30 probate + 25 stacking bonus (2+ clocks) + 15 tax-lien sold
+ 10 strong ZIP + 8 lien >= $3,000 + 8 out-of-state + 5 tax delinquent
+ 5 ARV > $200,000
```

`n_clocks` counts only true clocks (pre-foreclosure, probate, lien sold, delinquent).
A large lien is a **modifier** — `SIGNALS STACKED` can read 2 while the reason to call
reads "owes $63,496". Do not blur the two.

## Gates, in order

```
entity owner -> no living area (<500 sqft) -> ARV under floor -> institution owns it
-> transferred within 180 days
```

`NO COMPS` is **not** a gate — keep the row, leave the price blank, mark it `NO COMPS`.
Delinquency is off by default because turning it on moves nearly every row's priority
and invalidates comparisons with earlier pulls.

**Entity matching is whole-word by default** (`INC`, `LLC`, `CORP`, `LTD`, `GROUP`).
Substring matching silently deletes `MARY T VINCENT`, `LINCOLN SPENCER`, `SPENCER` —
a false drop of a real owner, the one error you cannot recover by calling.

## Contactability from Nigeria

Do not recommend buying large lists or mass outreach without a real contact path.
For each lead, state the channel honestly:

| Channel | Realistic for a remote wholesaler |
|---|---|
| Direct mail | Yes — but slow and needs a US fulfilment vendor |
| Cold call via a dialer/VoIP with a US number | Yes, with call-time discipline and time-zone care |
| SMS | Yes — check TCPA compliance; do not blast |
| Door knock | No |
| Agent-mediated (listing/agent contact) | Yes — fastest for on-market |

Label owner data: `VERIFIED` (county record or a source you actually read),
`REPORTED` (a third-party site claims it), `UNKNOWN`. Contact details are `UNVERIFIED`
until a call connects. **Never invent a phone number, email, motivation, or equity.**

## Pricing an off-market lead

There is no asking price, so there is no discount to compute.

```
max contract ceiling = (anchor × 0.70) − repairs − fee
```

`anchor` is a **property-level estimate** (Zestimate or a same-property CMA), labelled
by source, or `UNPRICED`. It is never applied to another property and never a comp.
Repairs unknown means the ceiling is quoted at $0, $40K, $60K side by side, and the
report says the walkthrough decides it.

## The two books, never mixed

| | On-market | Off-market |
|---|---|---|
| Has | asking price, DOM, agent, condition | owner, mailing address, tenure, occupancy |
| Lacks | — | asking price, DOM, agent, condition |
| Values by | closed-sale ARV | property-level anchor, or UNPRICED |
| Outputs | sale-to-list gap, discount needed | a ceiling to dial with |

A listing discovered inside a county export is **on-market** — the parcel file has no
listing-status field. Exactly that error put a live $79,999 listing on an off-market
tab.
