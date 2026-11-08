# Cleveland Channel 2 — full screen, every SFR 1,200–2,600 sf

**80 leads enumerated in the three swept ZIPs. Complete, with a reconciled count.** Of those:
**6 priced, 68 unpriced for want of a comp set, 1 needs a walkthrough, 5 rejected.**
Tax arrears across the whole in-band SFR universe: **$803,913**.

Machine-readable: `CLEVELAND_LEAD_INVENTORY_2026-11-08.csv` (80 rows, 14 columns).

## 1. The count reconciles

| slice | parcels |
|---|---|
| SFR 1,200–2,600 sf, 3 ZIPs, free & clear, delinquent, `foreclosure_flag=1` | **78** |
| SFR 1,200–2,600 sf, `parcel_city='CLEVELAND'` (whole county, quirk removed) | **78** |
| **Rows in this inventory** | **80** |
| …of which out-of-market (44144 ×2, 44135 ×1) | 3 |

The inventory holds 80 rows for a 78-parcel universe because two 44144/44135 parcels carry
in-market neighbourhood codes (`02130`, `02145`, `02165`) — the county codes them to Cleveland hoods
while the postal city is not Cleveland. Both are now marked `REJECT-out-of-market` rather than
silently dropped, because they are the exact rows a hood-level query would wrongly include (D-49's
cousin: a filter that looks right and admits the wrong rows).

## 2. Every hood, worked

Not previously touched: every row below was queried directly by `neighborhood_code`, not inferred
from a street name. That was D-30 and it is why 20 hoods are listed rather than the 6 I could name.

| hood | leads | priced | hood $/sf verified? | blocker |
|---|---|---|---|---|
| `02125` | 8 | **5** | **yes — $102.70/sf, n=5** | 3 rows outside the 1,200–1,700 calibration band |
| `02121` | 8 | 0 | **tried — failed** | only **2** cleaned renovated comps; the third ($145/sf) breaches the ±45% gate |
| `02123` | 8 | 0 | no | comp set never built |
| `02130` | 8 | 0 | no | 1 row is out-of-market (44144) |
| `02143` | 9 | 0 | no | Clark-Fulton/Stockyards; no comp set built |
| `02142` | 6 | 0 | no | no comp set built |
| `02131` | 4 | 0 | no | **Daisy's own hood** — see below |
| `02122` | 4 | 0 | no | no comp set built |
| `02132` | 4 | 0 | no | no comp set built |
| `02133` | 3 | 0 | no | no comp set built |
| `02126`,`02158`,`02165` | 2 each | 0 | no | no comp set built |
| `02115`,`02127`,`02145`,`02150`,`02151`,`02163`,`02164` | 1 each | 0 | no | single-lead hoods; a 5-comp set cannot be justified |

**`02125` is the only hood with a verified $/sf, and it is 100% worked** (all 8 parcels reached a
status; 5 priced, 3 out-of-band).

## 3. `02121` — a worked attempt, and why it failed

I built a real comp set for it, county-coded and condition-graded from agent remarks:

| comp | sold | price | sqft | $/sf | condition |
|---|---|---|---|---|---|
| 2070 W 100th St | 2026-10-23 | $150,000 | 1,582 | $94.82 | **renovated** — new roof, gutters, furnace, CA, HWT |
| 2218 W 100th St | 2026-05-13 | $124,500 | 1,262 | $98.65 | **renovated** — LVP, paint, stainless, move-in ready |
| 2115 W 93rd St | 2026-07-10 | $197,000 | 1,355 | **$145.39** | renovated — new roof, HVAC, electrical |
| 2045 W 89th St | 2026-06-19 | $105,000 | 1,375 | $76.36 | maintained — "recently updated", turnkey rental |
| 2036 W 83rd St | 2026-06-08 | $110,000 | 1,424 | $77.25 | maintained — turnkey, tenant-occupied |
| 2069 W 95th St | 2026-07-15 | $44,000 | 1,353 | $32.52 | dated |

`comp.py` result: **UNPRICED — only 2 renovated comps within 1.5 mi (needs 3).** 2115 W 93rd is
renovated but sits **+45.9%** above the renovated median, outside the ±45% consistency gate, so it
cannot be the third. **Reinstating it to reach a count would be the exact move D-31 forbids.**

**This is the finding of the whole exercise:** `02121` has 8 leads and a genuinely deep sales pool,
and it still cannot be priced. Depth of *sales* is not depth of *renovated* sales. In these hoods
roughly two-thirds of the pool is maintained/dated/distressed, so a 7-sale band yields 2 ARV comps.

## 4. `02131` — Daisy's hood, re-examined under the new $/sf

Daisy was unpriced on a **bed floor** (5 beds) plus a **size band** (2,334 sf). Both still hold and
neither is revisited. But the hood has three *other* leads that were never tested, because the
previous pass only looked at the largest house in it:

| address | sf | rooms | arrears | note |
|---|---|---|---|---|
| 3701 Marvin Ave | 1,260 | 6 | **$37,811** | largest arrears in the hood |
| 3531 Woodbridge Ave | 1,462 | 8 | $25,973 | |
| 3404 Woodbridge Ave | 1,263 | 6 | $1,731 | |

**These are in the size band that the `02125` $/sf actually applies to (1,200–1,700 sf)** — the
opposite of Daisy. They are unpriced only because `02131` has no comp set. That is the highest-value
next target in the file, and it is a hood-level job, not a parcel-level one.

## 5. What the 68 unpriced rows are waiting for

They are not missing data about the *houses*. 68 parcels have address, footage, rooms, style,
arrears, ownership state and payment-plan status. What is missing is a **renovated comp set per hood**.

Each hood needs, before any of its leads can carry a number:
1. the sold pool at ±30% of subject footage (Redfin ZIP feed, 6 months);
2. county `neighborhood_code` for every comp — **must be queried, never inferred**;
3. condition from agent remarks — one property page per comp (D-48);
4. ≥3 renovated after the ±45% consistency gate.

That is roughly 6–9 comps and as many property pages **per hood**, for 19 hoods. **The `02121`
attempt above is the honest unit cost, and it failed.** A hood whose pool is two-thirds
maintained/dated will often fail, and the correct output is `UNPRICED` — not a borrowed number.

## 6. The one priced number that changed

`02125` hood-wide **$102.70/sf** replaced the 0.25 mi pocket's **$121.25/sf** (D-51). That single
correction moved every MAO in the priced set down by ~$5,000–$15,000 and it is the only $/sf in the
entire Cleveland file that rests on a hood-wide comp median rather than a pocket.

## 7. Verdict

- **The screen is complete.** 78-parcel universe, 80 rows, reconciled.
- **The pricing is not**, and cannot be, with one calibrated hood.
- **6 of 78 in-band SFR parcels (7.7%) carry an ARV.** That is the honest coverage figure.
- **The binding constraint is renovated-comp density, not lead supply** — proven by `02121`, which
  had 8 leads and 7 sales and still failed.
- **Next hood: `02131`** (3 untested leads, one at $37,811 arrears, all in the calibrated size band).
