# Market and ZIP research

Six markets. Never scan a city as a block — scan ranked ZIPs, in priority order.

| # | Market | State | Notes |
|---|---|---|---|
| 1 | Cleveland | OH | Cuyahoga parcel GIS is public and queryable — the best data in the portfolio |
| 2 | Akron | OH | Summit County; 44302/44303/44307/44305 differ sharply within the same city |
| 3 | Columbus | OH | Deep landlord base, wider price band |
| 4 | Dayton | OH | Low basis, strong rent-to-price |
| 5 | Birmingham | AL | Low basis; check for local assignment/wholesale regulation |
| 6 | Atlanta | GA | Institutional buyer activity, fastest at scale |

## ZIP scoring

Score each ZIP 0–100 on five factors, then classify. These weights are a research
priority, **not** verified market statistics:

| Factor | Weight | How it is evidenced |
|---|---|---|
| Distressed and dated inventory | 25 | Count of dated/as-is/fixer listings and their share of active stock in the ZIP |
| Stale listings and price reductions | 20 | Count of 60+ DOM and reduced listings, and the median days on market |
| Investor transaction activity | 20 | Share of recent sales bought by entities, cash-sale share, repeat-sale frequency |
| Potential discount opportunities | 20 | Asking price as a percentage of renovated ARV in the same ZIP |
| Availability of relevant sold comps | 15 | Sold count in the last 6 months within the ZIP at the subject's size/type |

**Priority A = 75–100 · B = 60–74 · C = below 60.**

### Evidence rule

A factor with no evidence scores **nothing**, and the row records
`evidence: UNKNOWN` rather than a guess. Never manufacture a score. A ZIP with four
of five factors unknown is not A because the fifth is good — it is `UNRANKED` until
researched, and it does not get scanned ahead of a researched B.

Score provenance is `ESTIMATED` always: it is a research ordering, not a market fact.

## Scan order

1. All A ZIPs, highest score first.
2. B ZIPs, if A ZIPs produced fewer than 3 viable candidates.
3. C ZIPs only on explicit instruction.

Re-score after each cycle from what the ZIP actually produced. **A ZIP that has been
scanned twice with zero qualifying properties drops a category.** A ZIP that produced
a strong opportunity jumps to the top of its category.

## Ledger schema

`state/zip_ledger.csv`, one row per ZIP per scan:

```
city,zip,priority_score,priority_category,evidence,scanned,last_scan_date,
qualifying_count,potential_count,rejected_count,rejection_reasons,
best_opportunity,revisit,notes
```

`rejection_reasons` is a semicolon-separated tally of the gate code that killed each
row (see `qualification.md`). `best_opportunity` holds the address and verdict of the
single best find, or `none`.

## Cadence

| Priority | Re-scan interval |
|---|---|
| A | 7 days |
| B | 14 days |
| C | 30 days |

New listings appear constantly, so an A ZIP scanned 8 days ago is due. A ZIP that
produced nothing twice moves to B and its interval lengthens — effort follows
evidence, not habit.

```bash
python3 scripts/zip_ledger.py --due          # what is owed today, in scan order
python3 scripts/zip_ledger.py --list         # the whole picture
python3 scripts/zip_ledger.py --log --zip 44302 --city Akron --score 78 --category A \
    --qualifying 3 --potential 5 --rejected 41 --best "156 Colony Cres POTENTIAL"
```

## Property ledger

`state/property_ledger.csv` prevents the same address being reported as a new find.

```
address,city,zip,first_seen,last_seen,channel,status,last_verdict,last_price,
last_scan_date,notes
```

Check it before writing any report. A property already in the ledger is reported as
`SEEN` with its first-seen date and any price/status change — never as a new
opportunity. Price drops and status changes (active → pending → withdrawn → back on
market) are real signals and are the one legitimate reason to re-surface a property.

```bash
python3 scripts/zip_ledger.py --check 141 Grand Ave --city Akron --zip 44302
```
