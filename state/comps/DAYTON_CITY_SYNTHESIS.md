# Dayton, OH — Cross-ZIP Synthesis

**Date:** 2026-11-08 · **Coverage: 579 of 579 live listings across 7 ZIPs (100%)** · **Filter: none**

- ZIPs: 45402, 45403, 45404, 45405, 45406, 45410, 45417
- Source of truth: `state/sweeps/dayton_<zip>_sweep_results.csv`
- Coverage: `state/sweeps/dayton_coverage.csv` (all seven rows 100%)
- Per-ZIP write-ups with full comp sets: `state/comps/DAYTON_<zip>_FULL_SWEEP.md`
- Priced leads: 222 · Deliverable: Google Sheet "Dayton OH — Full Sweep (7 ZIPs, 579 listings swept)"

---

## Headline

**6 PRIORITY · 3 MARGINAL · 7 ABOVE-MAO · 112 NO · 93 UNPRICED · 1 NEGATIVE MAO.**

Out of 579 live listings, **ten clear MAO at all**. That is not a thin market — it is a market
priced *above* what the 70% rule can pay, almost everywhere, and the numbers say so with unusual
consistency across seven separate ZIPs.

The single most important number in this document is **93**. Forty-two per cent of the leads
could not be priced, and every one of those refusals is a real structural gap in the sold data,
not a shortcut. See §3.

---

## 1. Per-ZIP totals

| ZIP | live = examined | leads | PRIORITY | MARGINAL | ABOVE-MAO | NO | UNPRICED | NEG |
|---|---|---|---|---|---|---|---|---|
| 45417 | 111 | 25 | 2 | 0 | 1 | 5 | 17 | 0 |
| 45405 | 114 | 34 | 2 | 3 | 1 | 6 | 22 | 0 |
| 45406 | 86 | 45 | 1 | 0 | 1 | 30 | 13 | 0 |
| 45402 | 73 | 23 | 0 | 0 | 1 | 12 | 9 | 1 |
| 45403 | 69 | 29 | 0 | 0 | 3 | 18 | 8 | 0 |
| 45404 | 48 | 25 | 0 | 0 | 0 | 12 | 13 | 0 |
| 45410 | 78 | 41 | 1 | 0 | 0 | 29 | 11 | 0 |
| **TOTAL** | **579** | **222** | **6** | **3** | **7** | **112** | **93** | **1** |

Beds across all 222 leads: 3-bed 121, 2-bed 61, 4-bed 32, 6-bed 5, 5-bed 3.
Median ask **$107,000**. Median sqft **1,267**.

---

## 2. The find — six PRIORITY, and only one of them is well supported

| ZIP | Address | Beds/SqFt | Ask | Grade | Repairs | ARV | MAO | Comps |
|---|---|---|---|---|---|---|---|---|
| 45406 | **1816 Auburn Ave** | 2 / 1524 | $25,000 | heavy | $76,200 | $185,881 | **$43,917** | n=8, 8.7% |
| 45405 | 124 Victor Ave | 3 / 1566 | $39,999 | heavy | $78,300 | $193,513 | $47,159 | n=3, 4.1% |
| 45405 | 49 Pointview Ave | 3 / 1778 | $39,900 | heavy | $88,900 | $219,710 | $54,897 | n=3, 4.1% |
| 45410 | 819 Wyoming St | 3 / 1456 | $60,000 | moderate\* | $50,960 | $204,750 | $82,365 | n=11, 20.4% |
| 45417 | 2520 Germantown St | 2 / 1163 | $17,500 | heavy | $58,150 | $136,448 | $27,364 | LOW, ZIP-wide |
| 45417 | 361 Adelite Ave | 3 / 1148 | $19,900 | heavy | $57,400 | $134,689 | $26,882 | LOW, ZIP-wide |

\* 819 Wyoming's grade is **assumed**; the listing carries no condition detail.

**1816 Auburn Ave is the only PRIORITY in the city that would survive an honest challenge.**
Eight comps, 8.7% spread, ask at 57% of MAO, and the repair grade is *heavy* — the most
conservative assumption already built in. Nothing about it depends on a favourable guess.

**The two 45417 PRIORITYs are arithmetic, not evidence.** Their ARV uses a ZIP-wide $/sf
because no block-level comp set exists; 45417 has zero renovated 2-bed sales in the 180-day
window. At the two lowest renovated comps 361 Adelite *loses* money (−$14,089 to −$2,533), and
365 Adelite — same block — sold for $26,000 ($21/sf) on 2026-09-14. Both carry
`conf = "LOW - ZIP-wide basis, block unproven"` in the source file.

**The two 45405 PRIORITYs sit on n=3.** Three comps at 4.1% spread is tight, but three is the
engine's *floor*, not a measure of strength. Treat them as leads to verify, not deals.

---

## 3. The 93 refusals are the most useful output in the sweep

42% of leads could not be priced. The reasons cluster into four mechanical gates, and each one
tells you something about what the city's sold data can and cannot support.

| Gate | Count | What it means |
|---|---|---|
| Zero renovated sales at that bed count in the ZIP | ~55 | Mostly 2-bed (33) and 4-bed (30). 45417 has no renovated 2-bed sale at all; 45404 has essentially one 4-bed SFR sale in six months. |
| Fewer than 3 comps inside 1.5 mi | ~20 | Consistency gate left 2 comps after filtering. 45406's whole refusal set is this. |
| Subject outside the ±30% sqft band | ~12 | 4,132 sf, 2,636 sf, 2,589 sf — these houses have no peer in their own ZIP. |
| Listing reports no living area | 2 | 307 Xenia Ave and 569 Corwin Ave. No sqft, no ARV, full stop. |

**Why this matters for how you read the headline.** It would be easy to sell "6 deals in 579
listings" as a barren market. It is more accurate to say: **of the 129 leads that could be
priced honestly, 10 clear MAO — a 7.8% hit rate — and 93 more were never testable.** The 2-bed
and 4-bed homes are where the untested inventory is, and they are exactly the product the
refusal gates reject. A human comp search (wider radius, longer window, explicit bed-count
adjustment) is the only way to know what is in those 93.

---

## 4. Primary-market evidence beats ZIP-level $/sf — the 45410 warning

45410 illustrates the limit of the engine's method better than any other ZIP.

- 45410 is the **only ZIP where a 4-bed SFR market genuinely exists** — roughly 18+ renovated
  4-bed sales in six months, against 45404's one.
- 125 Perrine St sold at **$249,000 / 1,336 sf = $186.38/sf**, fully renovated, South Park.
  Park Drive runs $112–$146/sf. The renovated band in 45410 is **not tight** — spreads of
  18–42% are routine in the priced set.
- **51 of the 129 priced leads city-wide have a comp spread above 20%** (or are flagged WIDE).
  A median $/sf applied across a 20%+ spread band produces an ARV with a ±20% error bar, and a
  70% ceiling built on it inherits that error directly.

**The lesson generalises:** where the ZIP's own comps are dispersed, a ZIP-level median $/sf is
a weak instrument, and primary-market evidence — an actual recent sale on the same block, or
the same street — should override it. 45417's Adelite block is the clearest case: the block has
its own price level ($21/sf) and the ZIP-wide median does not see it.

---

## 5. Repair-grade sensitivity — the whole thesis rests on one assumption

Repair grade is the analyst's read of listing photos and agent language. It is the softest input
in the model. So the model was stress-tested: **step every priced lead one grade heavier**
(light→moderate, moderate→heavy) and re-run the verdict.

**Eight verdicts collapse.** Nothing improves — the test can only hurt, which is the point.

| Was | Becomes | Count | Which leads |
|---|---|---|---|
| PRIORITY | MARGINAL | 1 | 819 Wyoming St (45410) |
| MARGINAL | NO | 3 | 428 Geyer, 129 Marathon, 97-99 Fernwood — **all of 45405's MARGINAL tier** |
| ABOVE-MAO | NO | 4 | 141 S Torrence, 124 N Harbine, 4074 Middlehurst, 817 Faulkner |

Two conclusions:

1. **All three MARGINAL leads are one grade away from being NOs.** The entire MARGINAL tier is
   a condition judgement, not a margin. If those houses are worse than the photos suggest, there
   is nothing there.
2. **The heavy-grade PRIORITYs are immune to this test — because they are already at the worst
   grade.** 1816 Auburn, 124 Victor, 49 Pointview, and both 45417 leads cannot get worse. That
   asymmetry is a genuine strength: their verdicts do not depend on a favourable condition read.

The four PRIORITYs graded heavy are the most robust rows in the entire sweep. Everything graded
moderate or light is a bet on the photos.

---

## 6. What is not verified

- **No ARV in any of the seven ZIPs is county-confirmed.** `mcrealestate.org` failed three times
  across three sessions; `gis.mcohio.org` returns 404. Every ARV rests on Redfin sold comps only.
- **No physical inspection.** Condition grades come from listing photos and agent language.
- **No title or lien work** on any lead.
- **Comp counts are thin by construction.** Median n across the 124 leads that carry an n is 6;
  30 of them rest on exactly 3.

---

## 7. What to do next, in order

1. **Call on 1816 Auburn Ave.** n=8, 8.7% spread, ask 57% of MAO, already at heavy grade. It is
   the only lead in the city whose verdict does not depend on a guess.
2. **Walk 819 Wyoming St before believing it.** The one 45410 PRIORITY is a moderate-grade
   assumption with a 20.4% spread. If it is heavy, MAO falls to $60,525 and it is a NO.
3. **Verify the three 45405 MARGINALs on site.** They are all one grade from NO, and they are
   the entire MARGINAL tier.
4. **Then work the 93.** A human comp search on the 2-bed and 4-bed refusals is the only place
   left with untested inventory — 63 of the 93 sit at those two bed counts.
5. **Establish a county data path.** Until ARVs can be checked against the auditor, every
   ceiling in this document carries an unquantified error bar.

---

*Method: `ARV = sqft × median comp $/sf`. `CEILING = ARV × 0.70 − repairs`. `MAO = CEILING −
$10,000`. Repairs light $20/sf, moderate $35/sf, heavy $50/sf. PRIORITY = ask ≤ 0.85 × MAO;
MARGINAL = ask ≤ MAO; ABOVE-MAO = ask ≤ ceiling; else NO. Under five comps the ARV is flagged
`INSUFFICIENTLY SUPPORTED`; the Cuyahoga ±40% ARV band is not applied to Dayton — every Dayton
ZIP reports `ARV BAND: NONE — error UNMEASURED`.*
