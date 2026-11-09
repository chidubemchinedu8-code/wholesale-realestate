# Cleveland off-market universe — Cuyahoga County GIS, 2026-11-08

**The repo said Cuyahoga GIS was unreachable. It is reachable.** See `DEFECT_LOG.md` D-49.

Live endpoint:
```
https://gis.cuyahogacounty.gov/server/rest/services/CCFO/Parcel_Fabric_Taxparcels/FeatureServer/0/query
```
Returns JSON. 142 fields. Queryable, filterable, countable.

---

## 1. What the fields actually mean (read before using)

| field | truth | trap |
|---|---|---|
| `grand_total_balance` | **county tax + assessments owed to the county** | **NOT mortgage debt.** A $5,923 balance is not a cheap house |
| `lender` | `'NO LENDER'` or null | **`'NO LENDER'` = free and clear.** This is the gold flag |
| `foreclosure_flag` | integer `1` (not `'Y'`) | string comparison silently returns 400 |
| `parcel_zip` | **Double** | `parcel_zip='44102'` fails. Use `parcel_zip=44102` |
| `tax_market_total` | county market appraisal | lags the market badly — never an ARV |
| `property_class` | `'R'` residential | |

**The combination that matters: `foreclosure_flag=1` AND `lender='NO LENDER'`.** The county is
foreclosing on a property with **no mortgage to satisfy** — the seller's floor really is near the
tax bill, and there is nobody ahead of the county in line.

---

## 2. The universe (44102 / 44109 / 44111)

| screen | count |
|---|---|
| foreclosure, residential, ≥900 sf, countywide | 3,411 |
| foreclosure, ≥1,000 sf, 3 ZIPs | 322 |
| foreclosure, ≥1,200 sf, balance < $50,000 | 252 |
| foreclosure, ≥1,200 sf, balance < $30,000 | 246 |
| **foreclosure + NO LENDER, 1,200–2,600 sf** | **134** |
| **foreclosure + NO LENDER, 1,200–2,600 sf, balance < $15,000** | **116** |

**SUPERSEDED 2026-11-08 — the SFR universe is 78, not 116.** The 116 figure came from a
count that did not hold the single-family type filter, so it bundled duplexes, triplexes and vacant
lots. The reconciled count, including every parcel, is in `CLEVELAND_FULL_SCREEN_2026-11-08.md`:

| filter | count |
|---|---|
| SFR 1,200–2,600 sf, 3 ZIPs, free & clear, delinquent, `foreclosure_flag=1` | **78** |
| all SFR (any size) | 129 |
| all types, any size | 228 |

Every one of the 78 is enumerated in `CLEVELAND_LEAD_INVENTORY_2026-11-08.csv`.

---

## 3. THE CORRECTION — my previous "no deal" conclusion was wrong

Last turn I wrote that the assignment model cannot clear at $121/sf because a five-figure ask plus
$10,000 fee plus repairs exceeds `0.70 × ARV`.

**That was right about MLS listings and wrong as a general claim.** Both ARV *and* repairs scale
with square footage, so the margin per foot is a **constant**:

```
MAO = sf × (0.70 × $121.25 − $35) − $10,000
    = sf × $49.875 − $10,000
```

| sqft | ARV | repairs | ceiling | **MAO** |
|---|---|---|---|---|
| 990 | $120,038 | $34,650 | $49,376 | **$39,376** |
| 1,200 | $145,500 | $42,000 | $59,850 | **$49,850** |
| 1,500 | $181,875 | $52,500 | $74,812 | **$64,812** |
| 1,800 | $218,250 | $63,000 | $89,775 | **$79,775** |
| 2,400 | $291,000 | $84,000 | $119,700 | **$109,700** |
| 2,594 | $314,522 | $90,790 | $129,376 | **$119,376** |

**So the real thesis is: buy BIG square footage cheap, not small square footage cheap.**

The MLS shortlist was mostly 990–1,160 sf — those need a seller at $39,000–$45,000, which never
happens on the open market. A 2,400–2,600 sf subject supports a **$110,000–$120,000** seller MAO.

**This inverts the sweep's own ranking.** The 25-row shortlist was sorted by ask-per-foot, which
promoted the *smallest* houses. The correct sort for this business is **absolute dollar MAO**.

---

## 4. Lead rows pulled (verification pending)

| parcel | address | ZIP | sf | county bal | tax market | owner mail |
|---|---|---|---|---|---|---|
| 00226028 | 6604 Wakefield Ave | 44102 | 2,594 | $12,851 | $168,000 | in-state, same address |
| 01506111 | 4147 Storer Ave | 44109 | 2,440 | $4,721 | $86,000 | Cleveland |
| 01720012 | 3379 W 100th St | 44111 | 2,426 | **$1,655** | $99,000 | Cleveland |
| 00813007 | 3177 W 14th St | 44109 | 2,400 | $7,700 | $274,600 | **Castro Valley CA** |
| 01618068 | 3504 W 54th St | 44102 | 2,353 | **$5.47** | $68,600 | **Fairfield CA** |
| 01514056 | 3223 Daisy Ave | 44109 | 2,334 | $11,889 | $94,600 | Elyria OH |
| 01510158 | 3055 Sackett Ave | 44109 | 2,285 | $9,033 | $108,300 | Cleveland |
| 00731081 | 3211 W 33rd St | 44109 | 2,245 | $5,364 | $67,500 | Amherst OH (LLC) |
| 02126132 | 3343 W 130th St | 44111 | 2,172 | **$0** | $134,400 | Brunswick OH |
| 01808032 | 3372 Bosworth Rd | 44111 | 2,162 | $4,710 | $85,800 | Lakewood OH (LLC) |

### The three that read as genuine

1. **3504 W 54th St, 44102 — 2,353 sf, balance $5.47, absentee in Fairfield CA.**
   Free and clear, out-of-state owner, county foreclosing, owing essentially nothing. MAO
   ≈ $107,400. This is the strongest structure in the set.
2. **3177 W 14th St, 44109 — 2,400 sf, balance $7,700, absentee in Castro Valley CA.**
   MAO ≈ $109,700. Zoned MF-2. County market appraisal $274,600 is the highest in the group,
   which needs verification — it may be a different product than the SFR band.
3. **3343 W 130th St, 44111 — 2,172 sf, balance $0, absentee in Brunswick OH.**
   Owes the county nothing at all and is still in foreclosure. MAO ≈ $98,300.

**None of these are priced.** ARV requires 3 same-hood renovated comps per subject, and none has
been run. They are leads with a **ceiling**, exactly as `references/off-market.md` defines the
second channel.

---

## 5. Verification still owed before anything is called a deal

- [ ] **Does `foreclosure_flag=1` mean an active case, or merely "ever referred"?** Unverified. If
      it is historical, this whole list is stale. **This is the load-bearing assumption.**
- [ ] Occupancy and condition — county data says nothing about either.
- [ ] `zoning_code` `2F` (two-family) on several rows; the multifamily rows need same-type comps.
- [ ] `tax_market_total` vs a real ARV — county appraisals lag. Never price off this field.
- [ ] Whether the parcel is already in sheriff's sale and past the point of a private sale.
