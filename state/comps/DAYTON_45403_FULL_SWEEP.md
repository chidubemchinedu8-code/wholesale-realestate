# Dayton 45403 — Full Sweep

**Date:** 2026-11-08 · **Coverage: 69 of 69 live listings examined (100%)** · **Filter: none**

Every active listing Redfin shows for 45403 was pulled and classified one by one. No
invented price cap, no bedroom floor. The roster counts rejects.

- Roster: `state/sweeps/roster/45403.csv` (69 rows)
- Sold master: `state/comps/dayton_45403_sold_master.csv` (92 rows, 6-month window)
- Pricing: `state/sweeps/dayton_45403_sweep_results.csv` (29 leads)

---

## Headline: 45403 clears nothing, and the reason is not the asking prices

**Zero PRIORITY. Zero MARGINAL.** Of 29 underwritten leads: 18 NO, 3 above-MAO,
8 UNPRICED.

This is the fourth ZIP in a row to come back empty, but 45403 fails differently from
45405, 45406 and 45402 — and the difference matters more than the tally.

**45403 is the only one of the four where the comp band is rich.** Renovated stock sells
at a median **$140.63/sf**, the highest of any Dayton ZIP swept so far (45406 $119.78,
45402 $124.51, 45405 North Riverdale $117.25). The exit values are real. The problem is
that the *entry* prices are retail — 12 of the 29 leads are already retail-ready and were
rejected as turnkey, and the rest are asking prices set against a renovated number without
leaving room for the renovation.

---

## The size effect — this ZIP's defining feature

The renovated band has a **3.01× spread** ($67.65–$203.66), which normally means an
unusable band. It isn't noise. It is almost entirely explained by house size:

| Size | n | median $/sf |
|---|---|---|
| under 1,100 sf | 5 | **$174.83** |
| 1,300 sf and up | 5 | **$108.09** |

**Pearson r(sqft, $/sf) = −0.863.** In 45403 small renovated houses command a premium and
large ones are discounted — the opposite of a suburban market and consistent with a
buyer pool paying for a finished small home rather than a big one to maintain.

All 12 renovated comps:

| Address | Sold | Price | Sqft | $/sf |
|---|---|---|---|---|
| 21 S Philadelphia St | 2026-10-14 | $115,000 | 1,700 | $67.65 |
| 15 Parnell Ave | 2026-10-30 | $159,900 | 1,517 | $105.41 |
| 127 Stainton Ave | 2026-10-16 | $155,000 | 1,434 | $108.09 |
| 15 Drury St | 2026-06-12 | $181,000 | 1,464 | $123.63 |
| 715 Gondert Ave | 2026-08-06 | $200,000 | 1,494 | $133.87 |
| 756 Alexander Dr | 2026-09-11 | $119,700 | 864 | $138.54 |
| 1717 Speice Ave | 2026-08-14 | $158,000 | 1,107 | $142.73 |
| 50 Murray Hill Dr | 2026-07-29 | $185,000 | 1,262 | $146.59 |
| 421 Alexander Dr | 2026-05-27 | $135,000 | 831 | $162.45 |
| 41 N Westview Ave | 2026-06-12 | $150,000 | 858 | $174.83 |
| 1919 Suman Ave | 2026-08-07 | $165,000 | 864 | $190.97 |
| 116 Mcclure St | 2026-07-02 | $178,000 | 874 | $203.66 |

`anchor.py` returns **single distribution** on the whole SFR set (n=56, median
$101.11/sf), so the ZIP median is a valid sanity check but is **not** a comp basis — it
mixes condition. The size-matched renovated band is the basis, and the engine's ±30% sqft
gate applies it correctly.

**The pooled median of $140.63/sf is never quoted as an ARV basis.** It sits between two
size clusters and would overprice every large house in the ZIP.

---

## Results — 29 leads underwritten

| Address | Ask | Repairs | ARV | MAO | Verdict |
|---|---|---|---|---|---|
| 633 Huffman Ave | $44,900 | $84,150 | $194,995 | $42,346 | above MAO (by $2,554) |
| 124 N Harbine Ave | $65,000 | $28,420 | $141,958 | $60,951 | above MAO |
| 141 S Torrence St | $74,900 | $51,030 | $187,719 | $70,373 | above MAO |
| 237 N Irwin St | $74,900 | $43,610 | $160,424 | $58,687 | NO |
| 3111 E 5th St | $89,900 | $41,720 | $167,637 | $65,626 | NO |
| 35 N Philadelphia St | $90,000 | $37,520 | $157,147 | $62,483 | NO |
| 124 S Philadelphia St | $109,900 | $26,680 | $171,754 | $83,548 | NO |
| 155 N Quentin Ave | $112,900 | $34,930 | $146,300 | $57,480 | NO |
| 240 Bierce Ave | $119,000 | $58,030 | $192,098 | $66,439 | NO |
| 1807 Gondert Ave | $129,000 | $36,400 | $152,456 | $60,319 | NO |
| 1655 Suman Ave | $129,900 | $19,680 | $159,856 | $82,219 | NO |
| 624 Greenlawn Ave | $135,000 | $39,900 | $167,116 | $67,081 | NO |
| 125 Pleasant St | $137,000 | $25,200 | $162,227 | $78,359 | NO |
| 135 Drummer Ave | $149,000 | $49,000 | $180,252 | $67,176 | NO |
| 921 Huffman Ave | $150,000 | $71,190 | $219,854 | $72,708 | NO |
| 304 Sheridan Ave | $150,000 | $30,170 | $145,368 | $61,588 | NO |
| 941 Springfield St | $165,000 | $32,970 | $158,859 | $68,231 | NO |
| 945 Springfield St | $170,000 | $30,030 | $144,693 | $61,255 | NO |
| 139 Columbus St | $172,900 | $51,240 | $188,492 | $70,704 | NO |
| 67 Burlington Ave | $174,000 | $49,000 | $180,252 | $67,176 | NO |
| 719 Kirk Lynne St | $184,900 | $54,740 | $201,367 | $76,217 | NO |
| *8 more* | | | — | — | UNPRICED |

**Tally: 0 PRIORITY · 0 MARGINAL · 3 above-MAO · 18 NO · 8 UNPRICED.**

The closest thing to a deal is **633 Huffman Ave** — a $44,900 ask, $84,150 of heavy work,
$42,346 MAO. It misses by $2,554. A 5.7% price cut would clear it at the median band. That
is the only negotiable lead in the ZIP and it depends entirely on the work actually being
heavy.

### The 8 UNPRICED, gate named

| Lead | Gate |
|---|---|
| 2105 E 5th St (3bd, 2,636 sf) | no sale within ±30% sqft (1,845–3,426) |
| 103 S Sperling Ave (4bd, 2,200 sf) | no sale within ±30% sqft (1,540–2,860) |
| 118 Linden Ave (4bd, 2,582 sf) | no sale within ±30% sqft (1,807–3,356) |
| 1704 Mclain St (5bd, 1,742 sf) | **bed floor** — no renovated 5-bed sale; comps max at 4 bed |
| 2610 E 4th St (4bd, 1,741 sf) | fewer than 3 clean comps |
| 57 S Torrence St (4bd, 1,971 sf) | fewer than 3 clean comps |
| 44 Springfield St (4bd, 1,429 sf) | fewer than 3 clean comps |
| 148 Stainton Ave (4bd, 1,344 sf) | fewer than 3 clean comps |

Renovated comps by bed count: **2bd × 2, 3bd × 8, 4bd × 2.** There is no 5-bed renovated
sale anywhere in six months, and only two 4-bed. Every 4-bed refusal above traces to that
thinness, not to distance.

---

## The assumption that decides this ZIP

**16 of the 29 leads carry no condition information in the listing at all** — no
"renovated", no "needs TLC", nothing. I assigned them `moderate` ($35/sf). That single
choice is doing most of the work, so here it is laid out:

| Address | Ask | @$20/sf MAO | @$35/sf MAO | @$50/sf MAO | Clears at |
|---|---|---|---|---|---|
| 237 N Irwin St | $74,900 | $87,742 | $69,052 | $50,362 | **light only** |
| 44 Springfield St | $99,000 | $102,097 | $80,662 | $59,227 | **light only** |
| 3111 E 5th St | $89,900 | $83,506 | $65,626 | $47,746 | never |
| 124 N Harbine Ave | $65,000 | $53,697 | $41,517 | $29,337 | never |
| 118 Linden Ave | $199,000 | $192,543 | $153,813 | $115,083 | never |
| *11 more* | | | | | never |

Only **2 of 16** unknown-condition leads clear even at the most generous repair tier, and
at the median band even they fail. So the answer is robust to the assumption — the tier
does not flip the ZIP. But it does identify the two leads worth a walkthrough, because if
237 N Irwin and 44 Springfield are genuinely light-rehab they become live.

The reverse error matters too: assuming `unknown` means `light` would have manufactured
false positives. I did not.

---

## Sensitivity

| Basis | Clears (of 13 priced) |
|---|---|
| Band low $67.65/sf | **0** |
| Band median $140.63/sf | 2 |
| Band maximum $203.66/sf | 9 |

As in 45402, this ZIP needs the top of its own comp band before most leads work. Under
`underwriting.md` that is a documented upside case, not a deal.

---

## Gates that failed — named

1. **D-37 (open):** `state/comps/_geo_45403.csv` does **not exist**. Every subject was
   given the same lat/lon, so all "within 1.5 mi" output is void. Comp sets are size- and
   condition-matched, **not distance-verified**.
2. **Neighbourhood gating unverified.** Per `DAYTON_45405_NEIGHBOURHOOD_CORRECTION.md`,
   hood must come from Zillow's `## Neighborhood:` or OSM. Not obtained for the 29 leads.
   (St. Anne's Hill and Huffman Historic are named repeatedly in listing prose — prose is
   explicitly not a hood source, so they were not used for gating.)
3. **ARV band: UNMEASURED.** No backtest for 45403. Figures are ESTIMATES.
4. **County validation: not attempted per-property this sweep.** The Zillow assessor route
   proven on 45402 is available but was not run for these 29.
5. **Six-bed and five-bed leads are structurally unpriceable** — no renovated sale exists.

## Sold rows excluded

Land: 2205 E 5th $8,000, 112 Centre $5,500. Court-ordered: 1809 Suman $42,130.
Multifamily (16 rows): 108 Boltin, 100 N Irwin, 57 Drummer, 3213 E 5th, 321 S Harbine,
59 Parnell, 110-112 S June, 100 Boltin, 1303 Huffman, 1315 Chardon, 218 N Delmar,
3705 E 3rd, 808 Huffman, 24-26 More, 1528-1530 Mclain, 1620 Gondert. New build:
153 High St (2014 rebuild after fire). Duplicates removed: 1528 McLain (same property as
1528-1530), 1425 Huffman, 49 S Terry.

## Roster notes

- **152 High St and 154 High St #152-154 are the same property.** Redfin lists it twice at
  $235,000 with identical copy, as the 69th of the "69 homes". Counted once, so the ZIP
  holds 68 distinct properties.
- **1807 Gondert Ave** appears under 45403 but the listing title reads "45410". The URL is
  under 45403 and it is counted in the 69.
- Commercial: 1620 E 5th (salon/spa) and 1519 E 5th (office) rejected as `commercial_use`.

## Not done

- 45404 (48), 45410 (78) — not started. **These are the last two ZIPs.**
- No geocode for 45403; D-37 stays open.
- No per-property assessor cross-check this sweep.

---

## Coverage after this sweep

| ZIP | examined | live |
|---|---|---|
| 45402 | **73** | **73** |
| 45403 | **69** | **69** |
| 45404 | 2 | 48 |
| 45405 | **114** | **114** |
| 45406 | **86** | **86** |
| 45410 | 2 | 78 |
| 45417 | **111** | **111** |
| **TOTAL** | **457** | **579 (78.9%)** |

**Five of seven ZIPs complete.** Remaining: 45404 (48), 45410 (78) — 126 listings.
