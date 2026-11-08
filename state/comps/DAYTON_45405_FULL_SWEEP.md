# 45405 — full unfiltered sweep, 2026-11-08

114 of 114 active listings examined against live Redfin. No price cap, no bed
filter. Every listing recorded, including rejects. Roster:
`state/sweeps/roster/45405.csv`.

## Coverage

| | count |
|---|---|
| Redfin active total | 114 |
| recorded in roster | 114 |
| of which rejected | 56 (49%) |
| priced through `comp.py` | 12 |
| UNPRICED (correct refusal) | 22 |

## Rejects — 56 of 114

| reason | n |
|---|---|
| multifamily above ARV band / needs 3-4 unit comps | 18 + 2 |
| duplex (needs 2–4 unit comps, engine is SFR) | 9 |
| above market ARV band | 6 |
| condo (excluded by buy box) | 5 |
| land, no structure | 5 |
| turnkey / retail-ready | 4 |
| tenant-occupied, landlord model | 4 |
| court-ordered auction | 1 |
| not residential (2,212 N Main, 4,000 sf studio) | 1 |

45405 is a **multifamily-heavy ZIP**: 29 of 114 listings are 2–4 unit or larger
apartment buildings, against 45417's 3. Duplexes cannot be priced by an engine
built for SFR comps, and the 18 larger buildings are all above the ARV band.

## The comp pool — 45405 is BIMODAL

66 sold homes in 90 days. `anchor.py` returns:

```
BIMODAL: low cluster $15.29/sf (n=3), high cluster $79.35/sf (n=45)
BIMODAL - the ZIP blends two markets. Drop to a named-neighbourhood
or plat-level median and say why. A single ZIP median is not usable here.
```

So the ZIP median ($77.03/sf) is **not usable**. Pricing must be per
neighbourhood, per `DAYTON_45405_NEIGHBOURHOOD_CORRECTION.md`.

### Verified neighbourhood band — North Riverdale

10 renovated comps, using only the repo's sourced pool (coordinates included):

| comp | sold | price | sf | $/sf |
|---|---|---|---|---|
| 409 Kenilworth Ave | 2026-04-07 | $142,700 | 1,596 | 89.41 |
| 101 E Hudson Ave | 2026-06-30 | $140,500 | 1,507 | 93.23 |
| 49 Woodcrest Ave | 2026-05-20 | $175,000 | 1,754 | 99.77 |
| 53 E Beechwood Ave | 2026-04-24 | $163,000 | 1,442 | 113.04 |
| 332 Ashwood Ave | 2026-03-31 | $134,900 | 1,176 | 114.71 |
| 212 E Beechwood Ave | 2026-06-29 | $155,000 | 1,294 | 119.78 |
| 69 E Beechwood Ave | 2026-05-29 | $173,000 | 1,400 | 123.57 |
| 44 E Beechwood Ave | 2026-10-26 | $176,950 | 1,362 | 129.92 |
| 258 E Siebenthaler Ave | 2026-07-31 | $165,000 | 1,248 | 132.21 |
| 312 E Maplewood Ave | 2026-06-22 | $122,500 | 812 | 150.86 |

**Median $117.25/sf, range $89.41–$150.86, spread 1.69×.**

## Results — the honest version

`comp.py` at the median comp prices 12 leads and refuses 22. But 1.69× spread
means the median alone is not a verdict. Run across the whole band:

| address | ask + repairs = basis | MAO @ low | MAO @ median | MAO @ high | verdict @ median |
|---|---|---|---|---|---|
| 49 Pointview Ave | $128,800 | $12,381 | **$47,026** | $88,863 | PRIORITY |
| 124 Victor Ave | $118,299 | $9,712 | $40,226 | $77,075 | MARGINAL |
| 97/99 Fernwood Ave | $92,840 | $23,767 | $47,617 | $76,419 | NO |
| 129 Marathon Ave | $102,880 | $27,740 | $54,396 | $86,586 | NO |
| 428 Geyer St | $126,140 | $34,251 | $65,505 | $103,248 | NO |
| 152 E Parkwood Dr | $101,900 | $5,609 | $29,771 | $58,948 | NO |
| 2326 Parkland Ave | $108,680 | $24,429 | $48,747 | $78,113 | NO |
| 1315 Riverside Dr | $124,640 | $27,630 | $54,208 | $86,303 | NO |

**Read the low column.** At the lowest renovated comp in the neighbourhood,
every single one of these deals loses money against its basis. At the highest,
all eight clear. That is not a deal screen — it is a coin flip on which
renovated comp the finished house resembles.

Only **49 Pointview Ave** clears at the median with room, and it is the one
worth a walkthrough: 1,778 sf for a $39,900 ask, $88,900 of heavy repairs.

## Two defects this sweep found

**D-37 — subject coordinates were never sourced, so every radius check in
45405 was vacuous.** `state/comps/_geo_45405.csv` is an empty file: header
only, zero rows. Without subject coordinates the engine measures distance from
whatever lat/lon it is handed. In this sweep every subject initially received
the *pool's first row* coordinates, which made all 34 subjects price off the
same three Beechwood comps and report "radius 0.25 mi" — a distance measured
from 44 E Beechwood, not from the subject. Caught before any number was
published. Any earlier 45405 radius claim should be treated as unverified
until `_geo_45405.csv` is populated from a real geocoder.

**D-38 — a batched `comp.py` run silently returned UNPRICED for 22 leads.**
Cause: the harness rewrote the comp CSV and invoked the subprocess before the
file handle closed, so the engine read a truncated file and reported "no usable
sale in neighbourhood". Caught by running one lead by hand and getting a price
where the batch had reported UNPRICED. Batched engine calls must close the
file (context manager) before spawning the subprocess, and any batch that
returns a suspiciously high UNPRICED rate must be reconciled against a manual
run.

## Excluded from the comp file

400 Fountain Ave (8bd, 6,864 sf, $15,000 = **$2.19/sf**) was removed from
the sold master rather than kept as a marked row. It is an 8-unit building
sold in bulk, not a house sale, and the comp-integrity check correctly refuses
a comp at $2.19/sf. Recorded here so the exclusion is visible.

## Not done

- **County validation still blocked.** `mcrealestate.org` is still returning
  "The system is currently unavailable due to maintenance"; `gis.mcohio.org`
  404s. No ARV here is county-confirmed.
- No 45405 backtest → `ARV BAND NONE — error UNMEASURED`.
- 22 leads genuinely UNPRICED: 2-bed subjects have fewer than 3 renovated
  2-bed comps, 6-bed subjects exceed every comp's bed count, and several
  neighbourhoods have no renovated sale in the window.
- Five ZIPs remain unswept: 45402 (8%), 45403 (6%), 45404 (4%), 45406 (6%),
  45410 (3%).
