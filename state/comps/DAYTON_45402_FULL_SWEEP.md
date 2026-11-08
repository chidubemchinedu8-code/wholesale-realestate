# Dayton 45402 — Full Sweep

**Date:** 2026-11-08 · **Coverage: 73 of 73 live listings examined (100%)** · **Filter: none**

Every active listing Redfin shows for 45402 was pulled and classified one by one. The
`$100,000 ask cap` and `3+ bedroom floor` that governed the earlier 45402 row were agent
inventions and are **withdrawn**; the roster counts rejects.

- Roster: `state/sweeps/roster/45402.csv` (73 rows)
- Sold master: `state/comps/dayton_45402_sold_master.csv` (65 rows, 6-month window)
- Pricing: `state/sweeps/dayton_45402_sweep_results.csv` (23 leads)

---

## Headline: 45402 clears nothing at any defensible basis

**Zero PRIORITY. Zero MARGINAL.** Of 23 underwritten leads: 12 NO, 1 above-MAO,
1 negative MAO, 9 UNPRICED. The single lead that clears at any mid-market comp is
**728 Lexington Ave** ($109,900, MAO $91,452 at the high-cluster median) — and it only
clears because its asking price sits $23,000 *above* the highest assessor value in the
ZIP, which makes it a lead I do not believe.

The reason is not asking prices. It is the 70% ceiling against a renovation cost that
45402's own comps demand.

---

## Why this ZIP is harder than 45405 or 45406

45402 is not one market. It contains at least **three**, and the sold data separates them
cleanly:

| Segment | n | $/sf | Note |
|---|---|---|---|
| **Mid-market renovated, LOW cluster** | 3 | $73.29 (range $65.79–$79.69) | large 1,680–2,128 sf houses |
| **Mid-market renovated, HIGH cluster** | 6 | $124.51 (range $98.21–$181.38) | 988–1,896 sf houses |
| **Downtown / Oregon District renovated** | 7 | $183.42–$261.51 | `different_tier`, excluded |
| New construction | 6 | — | `new_build`, excluded |
| Multifamily (duplex through 4-unit) | 6 | — | excluded |

**The mid-market band is itself bimodal.** Nothing sold between **$79.69 and $98.21/sf** —
an $18.52/sf hole in a 9-comp set. So the pooled "median $120.07/sf" is an artifact of
averaging across a gap, exactly the error `anchor.py` warns about. It is not used.

`anchor.py` on the full SFR set returns **BIMODAL** (low $8.87/sf n=1, high $84.23/sf n=30),
so the ZIP median of $84.13/sf is **not usable** either. The high cluster is the only
defensible renovated basis: **$124.51/sf, n=6**.

The downtown/Oregon District tier is a genuinely different product — $183–$262/sf against
$98–$131/sf for the same renovation grade in the surrounding blocks. Pricing any lead in
this ZIP off a pooled figure would quote a downtown number to a West Dayton subject.

---

## Results — 23 leads underwritten

Engine: `ARV = sqft × comp $/sf`; `ceiling = ARV×0.70 − repairs`; `MAO = ceiling − $10,000`.

| Address | Ask | Repairs | ARV | MAO | Verdict |
|---|---|---|---|---|---|
| 817 Faulkner Ave | $50,000 | $50,050 | $156,069 | $49,198 | above MAO (by $802) |
| 623 Anna St | $65,000 | $61,850 | $153,999 | $35,949 | NO |
| 860 N Euclid Ave | $75,000 | $53,340 | $149,671 | $41,430 | NO |
| 847 Dow St | $77,000 | $34,860 | $123,996 | $41,937 | NO |
| 1230 Wilson Dr | $90,000 | $42,420 | $150,887 | $53,201 | NO |
| 737 Leland Ave | $95,000 | $33,600 | $119,514 | $40,060 | NO |
| 728 Lexington Ave | $109,900 | $31,680 | $155,563 | $67,214 | NO |
| 740 Leland Ave | $114,900 | $18,480 | $115,032 | $52,042 | NO |
| 4017 Delphos Ave | $115,000 | $25,920 | $158,477 | $75,014 | NO |
| 2022 W Grand Ave | $120,000 | $42,840 | $152,381 | $53,827 | NO |
| 632 Yale Ave | $129,900 | $31,840 | $156,349 | $67,604 | NO |
| 1222 Everett Dr | $160,000 | $26,760 | $160,652 | $75,696 | NO |
| 27 N Paul Laurence Dunbar St | $180,000 | $29,040 | $158,470 | $71,889 | NO |
| 624 N Broadway St | $85,000 | $115,100 | $177,360 | **−$948** | NO — ceiling negative |
| 809 Faulkner Ave | $25,000 | $74,250 | — | — | UNPRICED |
| 1233 Windsor Ave | $59,900 | $70,000 | — | — | UNPRICED |
| 717 Shoop Ave | $75,000 | $26,880 | — | — | UNPRICED |
| 900 Crestmore Ave | $80,000 | $31,185 | — | — | UNPRICED |
| 832 Clarkson Ave | $89,500 | $14,880 | — | — | UNPRICED |
| 1253 Vernon Dr | $138,500 | $51,135 | — | — | UNPRICED |
| 1705 W 5th St | $159,900 | $70,000 | — | — | UNPRICED |
| 33 N Paul Laurence Dunbar St | $180,000 | $231,100 | — | — | UNPRICED |
| 1000 W Grand Ave | $395,000 | $206,600 | — | — | UNPRICED |

### The 9 UNPRICED, with the actual gate named

| Lead | Gate that failed |
|---|---|
| 1233 Windsor Ave (4bd, 1,400 sf) | fewer than 3 sales — nearest 4bd renovated sale is outside the pool |
| 809 Faulkner Ave (4bd, 1,485 sf) | consistency gate left 2 comps |
| 1253 Vernon Dr (4bd, 1,461 sf) | fewer than 3 sales |
| 900 Crestmore Ave (2bd, 891 sf) | fewer than 3 sales |
| 717 Shoop Ave (2bd, 768 sf) | fewer than 3 sales |
| 832 Clarkson Ave (2bd, 744 sf) | no sale within ±30% sqft (520–967 sf needed) |
| 1000 W Grand Ave (4bd, 4,132 sf) | no sale within ±30% sqft (2,892–5,371 sf needed) |
| 33 N Paul Laurence Dunbar St (4bd, 4,622 sf) | no sale within ±30% sqft (3,235–6,008 sf needed) |
| 1705 W 5th St (6bd, 2,000 sf) | **bed floor** — no renovated 6-bed sale exists; the 6-bed sales that do exist (928 Kumler $155,000, 1125 Superior $73,000) are multifamily |

Note the `fewer than 3 sales within 1.5 mi` wording on four of these is **D-37 output** —
every subject was handed the same lat/lon, so the radius test is vacuous. The underlying
gate is bed-count and size, not distance, and each is recorded above by the gate that
actually binds.

**The two 4,000+ sf houses (1000 W Grand, 33 N Paul Dunbar) cannot be priced at all.**
No renovated SFR within ±30% of that size has sold in 45402 in six months. They are
restoration-scale properties and this method has no basis for them.

---

## Sensitivity — the band does not rescue these

| Basis | Clears (of 13 priced) |
|---|---|
| LOW cluster $73.29/sf | **0** |
| High cluster p25 $77.05 | **0** |
| Pooled median $120.07 (rejected — sits in the gap) | 1 |
| High cluster median $124.51 | **1** |
| Band maximum $181.38 | 8 |

45402 needs the **maximum of a 9-comp band** before 8 of 13 leads work. Under
`underwriting.md` that is not a deal, it is a hope. The one lead that clears at the
defensible basis, 728 Lexington Ave, has an ask of $109,900 against an assessor value of
$86,670 and sits above the top of the ZIP's own assessment range — which is the classic
signature of a retail-priced listing, not a wholesale lead.

### Renovation cost is the binding constraint, not the ask

45402 asks are low ($25,000–$180,000). What kills the deals is that the renovation is
expensive relative to a $124.51/sf exit:

- **624 N Broadway St** — a gutted duplex conversion with "no mechanics, plumbing or
  electric on site", 2,302 sf, $115,100 of heavy work against a $177,360 ARV. The ceiling
  is **negative**: even at a $0 purchase there is no deal.
- **33 N Paul Dunbar St** — 4,622 sf, $231,100 of work against roughly $180,000 of ask.
- **817 Faulkner Ave** — the closest miss in the ZIP. $50,000 ask vs $49,198 MAO. It fails
  by $802, which is not a bid gap I would call a strategy; it is a coin flip.

---

## County cross-check — FIRST TIME THIS HAS BEEN POSSIBLE

Every prior Dayton ZIP (45405, 45406, 45417) reported county validation as **blocked**:
`mcrealestate.org` returned "unavailable due to maintenance" and `gis.mcohio.org` 404s.

That gate is still blocked at the county site, **but Zillow exposes the Montgomery County
assessor record inline** (parcel number, tax assessed value, annual tax). For
624 N Broadway St:

| Field | Value |
|---|---|
| Parcel | **R72075090012** |
| Zillow tax assessed value | **$29,020** |
| Annual tax | $719 (2025) |
| 2024 tax | $20,348 — **28× the 2025 figure** |
| Ask | $85,000 |
| Our ARV | $177,360 |
| Our ceiling | $9,052 |

Two things follow. First, the assessor value of $29,020 against an $85,000 ask and a
$177,360 ARV is a **6.1× spread between county appraisal and our ARV**. That is reported
as a red flag, not a confirmation — either the county is far behind the market, or the
ARV is inflated. Second, the prior owner paid $22,617 in November 2024 and the property is
now listed at $85,000 with no mechanics installed, which describes a stalled flip.

This is a **single property**, not a ZIP-wide validation. The county record route works
via Zillow and can be extended; county-direct access remains down.

---

## Rows removed from the sold master

**928 Dow St — $7,500 / 1,981 sf = $3.79/sf.** A gutted shell with utilities off
("cash or hard money offers only... bring a flashlight to your showing"). It is not an
inhabitable dwelling and cannot sit in a $/sf pool at all; the validator rejected it as
implausible, correctly, and it was **deleted rather than re-tagged**. The check was not
weakened. Same call as the $2.19/sf 8-unit row in 45405.

Also excluded: 5 land sales (808 N Broadway $9,883; 1147 W 2nd $800; 12 Dayton Ave
$2,500; 28 Sweetman $2,000; one unidentified parcel $415,900), 3 court-ordered
non-arms-length sales (1405 Superior $25,080; 533 Lexington $27,060; 725 Brooklyn
$29,260), and one 6-month duplicate (600 Yale Ave appears in both windows).

## Gates that failed — named

1. **D-37 (open, and now measured):** `state/comps/_geo_45402.csv` does **not exist**.
   No radius claim in this document is verified. I obtained one **sourced** coordinate
   from Zillow (624 N Broadway: 39.76236, −84.2147), which produced a real result when
   reverse-geocoded — see the hood finding below. The other 22 subjects were priced with
   the pool coordinate and their distance screening is void.
2. **Neighbourhood gating is not verified for the 23 leads.** Per
   `DAYTON_45405_NEIGHBOURHOOD_CORRECTION.md`, hood must come from Zillow's
   `## Neighborhood:` block or OSM. Zillow does **not** emit a neighbourhood block for
   45402 listings (624 N Broadway shows only "Subdivision: City/Dayton Rev"), so hood
   attribution for most subjects is unobtainable by the sanctioned route. Comp sets here
   are **condition- and size-matched, not hood-matched**, and that is stated rather than
   papered over.
3. **ARV band: UNMEASURED.** No backtest exists for 45402. Cuyahoga ±40% never imported.
   All figures are ESTIMATES.
4. **County validation: partial.** Works per-property via Zillow; county-direct still down.

### Side finding: the existing 45402 comp pool carries bad hood labels

`dayton_45402_daytonview_comps.csv` labels **545 Gramont Ave** as `45402-WEST DAYTON`.
Reverse-geocoding its sourced coordinate returns **Cornell Heights**. The pool labels were
assigned without the sanctioned source and should not be trusted for hood gating. I did
not use that pool's hood column. (Its listing text also says "Dayton's Westwood
neighborhood", which is a third answer and equally unusable — agent marketing is not a
neighbourhood.)

## Not done

- 45403 (69), 45404 (48), 45410 (78) — not started.
- No ZIP-wide geocode for 45402; 22 of 23 subjects lack a sourced coordinate.
- No assessor cross-check beyond 624 N Broadway.

---

## Coverage after this sweep

| ZIP | examined | live |
|---|---|---|
| 45402 | **73** | **73** |
| 45403 | 4 | 69 |
| 45404 | 2 | 48 |
| 45405 | **114** | **114** |
| 45406 | **86** | **86** |
| 45410 | 2 | 78 |
| 45417 | **111** | **111** |
| **TOTAL** | **392** | **579 (67.7%)** |

Four ZIPs complete: 45402, 45405, 45406, 45417 (**384** of the 392 examined are from the
four completed ZIPs). Remaining: 45403 (69), 45404 (48), 45410 (78).
