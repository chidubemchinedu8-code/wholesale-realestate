# Dayton 45406 — Full Sweep

**Date:** 2026-11-08 · **Coverage: 86 of 86 live listings examined (100%)** · **Filter: none**

Every active listing Redfin shows for 45406 was pulled and classified one by one. The
`$100,000 ask cap` and `3+ bedroom floor` that governed the earlier 45406 row were
agent inventions, not repo rules, and are **withdrawn**. The roster counts rejects.

- Roster: `state/sweeps/roster/45406.csv` (86 rows)
- Sold master: `state/comps/dayton_45406_sold_master.csv` (62 usable rows)
- Pricing: `state/sweeps/dayton_45406_sweep_results.csv` (46 leads)

---

## Headline: 45406 clears nothing

Of 46 leads underwritten, exactly **one** scored PRIORITY — 1816 Auburn Ave, the
$25,000 gut-rehab with a full scope of work. It **fails on an all-in basis**: the
listing carries **$37,246 in back taxes**, so the true entry cost is ~$62,246 against a
median-case seller MAO of $41,581. At the low comp it loses by $44,103; at the median it
loses by $20,665; it only works at the top of the band.

Everything else is above MAO or cannot be priced at all. **This ZIP does not clear at
current asks.** That is the finding, and it is consistent with 45405 (one marginal
clears) and 45417 (zero robust clears).

---

## Why 45406 is the condition-split ZIP

The decisive number this sweep produced is not a ZIP median — it is the gap between
condition tiers.

| Basis | n | $/sf |
|---|---|---|
| **Renovated sales only** | 14 | **$119.78** (range $97.81–$143.94) |
| All SFR sales | 50 | $89.40 |
| **Condition gap** | | **+34%** |

`anchor.py` returns **SINGLE DISTRIBUTION** on 45406 (n=50, spread $21.76–$185.19/sf).
Unlike 45405 and 45417, the ZIP median here *is* a valid sanity check — but it is
**not a comp basis**, because the ZIP mixes renovated stock with dated and distressed
stock. Pricing a renovated subject off the $89.40 ZIP median would understate the ARV
by a third; pricing a dated subject off the $119.78 renovated median would overstate it
by a third. Neither error is acceptable, so subject condition drives the band choice.

**Spread within the renovated band is 1.47×** — tighter than 45405's North Riverdale
(1.69×), which is the one encouraging data point in this ZIP.

### The 14 renovated comps

| Address | Sold | Price | Sqft | $/sf |
|---|---|---|---|---|
| 549 Kenwood Ave | 2026-09-01 | $255,000 | 2,607 | $97.81 |
| 473 Marathon Ave | 2026-09-01 | $269,000 | 2,500 | $107.60 |
| 3351 Glen Helen Rd | 2026-10-23 | $181,000 | 1,668 | $108.51 |
| 1381 Catalpa Dr | 2026-09-01 | $225,000 | 2,051 | $109.70 |
| 1819 Auburn Ave | 2026-09-01 | $239,000 | 2,110 | $113.27 |
| 2527 Auburn Ave | 2026-08-14 | $174,900 | 1,540 | $113.57 |
| 2015 Emerson Ave | 2026-09-04 | $179,000 | 1,508 | $118.70 |
| 2719 Earlham Dr | 2026-09-01 | $144,900 | 1,199 | $120.85 |
| 2520 England Ave | 2026-09-01 | $185,000 | 1,503 | $123.09 |
| 1318 Princeton Dr | 2026-09-01 | $170,000 | 1,361 | $124.91 |
| 4634 Eichelberger Ave | 2026-09-01 | $142,500 | 1,066 | $133.68 |
| 1614 Catalpa Dr | 2026-09-01 | $296,500 | 2,178 | $136.13 |
| 1312 Canfield Ave | 2026-10-13 | $170,000 | 1,239 | $137.21 |
| 5107 Elyria Ln | 2026-09-01 | $190,000 | 1,320 | $143.94 |

Excluded from this band: **2047 Ravenwood Ave** ($173,000) — Welcome Home Ohio land-bank
new build, `new_build`, not a renovation comp. Multi-unit sales (3546 Stanford, 20 Wroe,
812 Neal, 3648 Otterbein, 626 Salem, 822 Harvard, 2071 Auburn, 816-818 Harvard, 810 Uhrig)
are out of the SFR pool entirely. Non-arms-length: 3716 Evansville $28,781 (court-ordered
auction), 4512 St Johns $13,797.

---

## Results — 46 leads underwritten

Engine: `ARV = sqft × comp $/sf`; `ceiling = ARV×0.70 − repairs`; `MAO = ceiling − $10,000`.
Repairs at $20/$35/$50 per sf by tier.

| Address | Ask | Repairs | ARV | MAO | Verdict |
|---|---|---|---|---|---|
| 1816 Auburn Ave | $25,000 | $76,200 | $185,881 | $43,917 | **PRIORITY** (fails all-in) |
| 4074 Middlehurst Ln | $64,990 | $44,065 | $156,113 | $55,214 | above MAO |
| 3395 Brumbaugh Blvd | $99,900 | $34,440 | $131,538 | $47,637 | NO |
| 3100 Princeton Dr | $99,000 | $50,680 | $178,230 | $64,081 | NO |
| 317 Bellevue Ave | $89,000 | $52,500 | $184,631 | $66,742 | NO |
| 2424 Ulrich Ave | $70,000 | $39,130 | $149,451 | $55,486 | NO |
| 3733 El Paso Ave | $49,899 | $66,600 | $163,952 | $38,166 | NO |
| 403 Kenwood Ave | $195,000 | $38,000 | $220,658 | $106,461 | NO |
| 1533 Olmsted Pl | $214,000 | $45,940 | $250,621 | $119,495 | NO |
| *+21 more NO* | | | | | see CSV |
| **13 UNPRICED** | | | — | — | bed-floor refusal |

**Tally: 1 PRIORITY · 1 above-MAO · 30 NO · 13 UNPRICED · 1 withdrawn.**

### The 13 UNPRICED are a real refusal, not a thin market

`comp.py` refuses these with *"no radius up to 1.5 mi produced a clean comp set"*. **That
message is misleading and traces to D-37** — every subject was given the same lat/lon, so
distance screening is vacuous. The true cause is the bedroom floor:

- Renovated comps by bed count: **3bd × 6, 4bd × 6, 5bd × 2**
- **Renovated 2-bed comps in 45406: ZERO**

Every one of the 13 unpriced leads is a 2-bed (4913/4904 Genesee, 2436 Ulrich, 4920 Queens,
2303 Arlene, 2150 Kensington, 3648 W Siebenthaler, 4428 Eichelberger, 4642 W Hillcrest,
3938 Necco) or a 6-bed (1967 Rugby). A 2-bed ARV cannot be built from 3- and 4-bed
renovated sales without a bed adjustment the repo does not license. **Unpriced is the
answer**, and it stays unpriced until a verified geocode and a bed-matched comp set exist.

---

## Sensitivity — the band is the whole argument

| Lead | Low $97.81 | Median $119.78 | High $143.94 |
|---|---|---|---|
| 1816 Auburn ($25,000) — **all-in $62,246** | loses −$44,103 | **loses −$20,665** | clears +$5,110 |
| 4074 Middlehurst ($64,990) | loses −$32,855 | loses −$13,493 | clears +$7,799 |
| 3395 Brumbaugh ($99,900) | loses −$76,968 | loses −$61,835 | loses −$45,194 |
| 3100 Princeton ($99,000) | loses −$60,540 | loses −$38,271 | loses −$13,782 |
| 317 Bellevue ($89,000) | loses −$48,800 | loses −$25,731 | loses −$363 |

Only 1816 Auburn and 4074 Middlehurst are band-sensitive enough to flip, and each flips
only at the very top of a 14-comp band. A deal that requires the maximum observed $/sf to
work is not a deal — under `underwriting.md` it is a NO with a documented upside case.

---

## Gates that failed — named

1. **D-37 (open):** `state/comps/_geo_45406.csv` **does not exist**. No radius claim in
   this document is verified. Comp sets are *bed- and condition-matched*, not
   distance-verified, and every "within 1.5 mi" line in engine output is an artifact.
2. **ARV band: UNMEASURED.** No backtest exists for 45406. The Cuyahoga ±40% figure is
   never imported. All figures here are ESTIMATES.
3. **County validation: impossible.** `mcrealestate.org` returned "unavailable due to
   maintenance" for the third consecutive attempt; `gis.mcohio.org` 404s. No appraised
   value comparison was possible for any 45406 subject. This is a blocked gate, not a
   passed one.
4. **2-bed ARV: structurally unsupported.** Zero renovated 2-bed sales in the 180-day window.

## Defect filed

**D-39** — a `comp.py` file error was being silently reported as UNPRICED. Tagging
multi-unit rows `multifamily` (not a valid exclusion reason) made the engine reject the
entire comp file, and the batch harness mapped any non-zero exit to "UNPRICED", producing
46 legitimate-looking refusals instead of one loud failure. Only exit 3 is a refusal;
exit 1 must abort. The first run of this sweep produced exactly that false result and was
caught and re-run.

## Not done

- 45402 (73), 45403 (69), 45404 (48), 45410 (78) — not started.
- No geocoder run for 45406; the radius gate stays closed.
- No county/appraised cross-check for any subject.
