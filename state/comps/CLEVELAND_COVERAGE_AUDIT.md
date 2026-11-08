# Coverage audit — how many leads do we actually have?

**6 captured. 228 exist. That is 2.6% of the county's free-and-clear delinquent foreclosure
inventory across 44102/44109/44111.** One slice is genuinely finished; everything else is untouched.

## The honest denominator

Filter throughout: `foreclosure_flag=1 AND lender='NO LENDER' AND total_net_delq_balance>0`.

| slice | universe | captured | coverage |
|---|---|---|---|
| **Everything, any size or type** | **228** | **17** | **7.5%** |
| 2–3 family, all sizes | 49 | 10 | 20% |
| SFR 900–1,200 sf | 40 | 0 | **0%** |
| SFR 1,200–1,700 sf | 84 | **6** | 7% |
| SFR 1,200–2,600 sf | 134 | 6 | 4% |
| SFR 1,700–2,300 sf | 31 | 0 | **0%** |
| **`02125` SFR 1,200–1,700 sf** | **6** | **6** | **100% ✓** |

*(17 = the 6 current leads plus the 11 from the earlier pass. The 6 current rows replaced the 11 in
the CSV; the other 11 remain valid identifying records, listed in the session ledger.)*

## What "all the leads" would actually require

**Only one slice is complete: `02125` single-family 1,200–1,700 sf, 6 of 6.** That is the slice that
matters most, because it is the one where a comp set and a $/sf both exist.

**222 parcels are un-worked.** In practice:

- **78 more SFR in the 1,200–1,700 band** across 44102 (31), 44109 (21), 44111 (11) and other 44102
  hoods — but each hood needs its **own** comp set before it can be priced (D-50), and only `02125`
  has one. Pulling these rows without building their hood comps would produce exactly the
  `UNSOURCED` column we just retracted.
- **31 SFR at 1,700–2,300 sf** — a second, larger size band that no hood has been calibrated for.
  Note `$/sf` **falls** ~$1.00/100 sf, so this band needs its own arithmetic, not a scaled-up 1,204 sf
  number.
- **49 duplex/triplex**, 9 of which are already captured. These need a **separate** comp pool: same
  type and same unit count, and duplex $/sf is not SFR $/sf. No such pool exists yet.
- **40 SFR below 1,200 sf** — deliberately skipped, and correctly. A 990 sf subject cannot absorb a
  $10,000 fee plus repairs; the arithmetic rules this band out. Leaving it at 0% is the right call,
  not a gap.

## Why this is defensible rather than lazy

The screen order is **type → assignable → ARV band → condition → comps**, and the binding
constraint is **comps**, not candidates. 228 parcels is not a lead shortage — it is a calibration
shortage. Working all 228 before any hood outside `02125` has a verified `$/sf` would generate 228
unsourced numbers, which is D-50 repeated at scale.

**The correct order is hood-by-hood: build the comp set, then pull every parcel in that hood.**
`02125` is done. The next hood with real depth is 44102's `02121` corridor (W 85th–W 101st), which
has 8 comp sales already coded and 7 live leads — it needs 2–3 more comps and a wider price read,
not a fresh start.

## Bottom line

- **Answered the question asked:** no, not all the leads. 6 of 228.
- **One slice is complete and priced** — that is real, not a sample.
- **Next highest-value move is a second hood comp set (`02121`)**, which would roughly double
  priced inventory, rather than bulk-pulling the remaining 222 rows into an uncalibrated table.
