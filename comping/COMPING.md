# Comping & ARV — the rule, in one place

**Source of truth:** this file and `SKILL.md` rule 23. `superpowers` → `leadgen/README.md` §3 and `leadgen/pull_leads.py` implement the same median method for the bulk county pull; if the two ever disagree, this file wins and the implementation is the bug
(`build_comps`, `arv_for`, checks 10–14), and the three Akron correction documents
(`VERIFIED_COMPS_…`, `ZESTIMATE_offmarket_…`, `SEPARATION_…`).

This file exists because those rules were learned by making three expensive mistakes
and writing them down. When this file and a convenient instinct disagree, this file wins.
The executable version is `scripts/comp.py`; read this to understand it, run that to use it.

---

## 0. The one sentence

**ARV is `sqft × MEDIAN($/sqft of ≥3 arm's-length closed sales in the same
neighbourhood, within 1.5 mi, within 6–12 months, within ±30% sqft, at or above the
subject's bed count, in renovated condition)` — or it is blank.**

**One method. Median, not average, not a percentile tier, and no haircut.** The
median is used because one strange sale cannot drag the ARV: the lowest sale
cannot pull it down and the highest cannot inflate it. There is no second way to
compute an ARV in this system and there is nothing stacked on top of the median.

There is no third option. "Blank" is a legitimate, shippable answer; an invented number
is not. `NO COMPS` is a status, not a problem to be papered over.

---

## 1. Word discipline (this is where deals die)

| Term | What it means | What it is **not** |
|---|---|---|
| **ARV** | Post-repair value from closed sales, same neighbourhood, with the filter ladder below | A Zestimate, an asking price, a tax assessment, "what it'll be worth" |
| **As-is value** | not separately modelled — the ARV is the only figure | ARV. Do not invent a second number |
| **Zestimate** | An automated property-level estimate — **an anchor for off-market only** | An ARV. Never combined with, averaged into, or used to "support" an ARV |
| **Asking price** | What the seller wants | A comp. Asking prices set ceilings on *nothing* |
| **Ceiling** | `0.70 × value − repairs` | An offer. It is the most you may pay |
| **Contract** | `ceiling − $10,000 fee` | The same as the ceiling (never deduct the fee twice) |
| **REPAIRS** | A graded number from a walkthrough or itemised photo evidence | A guess. Ungraded = blank |

---

## 2. The comp filter ladder (run in this exact order)

**First: verify the subject across four sources.** MLS/agent remarks, public
records, Zillow, Redfin. **Public records win on hard facts** (beds, baths, sqft, year
built); **MLS/agent remarks win on condition language**. If sources genuinely disagree,
state the conflict — never silently pick one. `references/data-integrity.md` §provenance.

Comp universe first, then the ladder per subject. Constants are in `scripts/comp.py`
(`RADIUS_LADDER`, `MIN_COMPS`, `SQFT_BAND` in `scripts/comp.py`).

**Comp universe screen — drop a sale if any of these is true:**

| Drop | Rule | Why |
|---|---|---|
| geometry | no lat/lon | can't measure radius |
| sqft_or_price | sqft `< 400` or missing | not a house |
| price_floor | price `< $20,000` | quitclaim / family transfer / data error |
| ppsf | `$20 > $/sqft > $300` | same, and catches manufactured/land sales |
| window | sold older than the window | 6 months preferred, 12 months maximum |

**Per-subject ladder:**

1. **Same neighbourhood code, identical.** Not "nearby". Not "similar". Identical.
   In Akron the failure was ZIP-level: 44303 three-beds sell **$200K–$255K** and
   44302 three-beds sell **$74K–$120K**. Same city, same house, half the price.
2. **±30% sqft band** around the subject.
3. **Radius ladder `0.25 → 0.50 → 0.75 → 1.00 → 1.25 → 1.50` mi.** Use the *smallest*
   radius that yields **≥3** comps. Never keep widening to reach a number.
4. **Style preference:** if ≥3 in-radius comps share the subject's style, use only those.
5. **Under 3 comps at 1.50 mi → `NO COMPS`.** Do not widen, do not fall back to a ZIP
   band, do not average. Say it is unpriced and move on.

**Two filters run *inside the ladder*, not after it.** A radius is only accepted if
the set that survives every filter is still ≥3:

6. **Bed-count floor.** A comp may never have fewer beds than the subject. A 3-bed
   subject takes 3-bed-and-up comps only — no exceptions for a great $/sqft match.
   This is stated in `scripts/comp.py` as `check_7_bed_floor`.
7. **Renovated condition only.** ARV is value *after* repairs, so the ARV pool must
   already be in the target condition. Dated, distressed, auction and
   unknown-condition sales are **banned from the ARV number** — they may only inform
   the as-is floor or a repair-cost check. `check_8_renovated_only`.
8. **Consistency gate.** With ≥3 comps, drop any comp further than **±45%** from the
   comp-set median $/sf — the "$120K sitting next to a $50K" test. The gate **never
   puts an outlier back to reach a count**: if it leaves fewer than 3, the set is
   unpriced. `check_9_no_price_gap`.

If a radius cannot produce a clean set, the ladder tries the next radius and says so,
then stops at 1.50 mi. It never reinstates an outlier, and it never averages across
percentiles.

**Then:**

```
median = MEDIAN of $/sqft across the chosen comps
ARV    = round(subject_sqft × median)

spread = (p75 − p25) / median × 100          # REPORTED, not used
confidence = TIGHT if spread <= 25 else WIDE if spread <= 50 else VERY WIDE
```

One ARV. There is no LOW, no POINT, no HIGH, and no haircut. The p25–p75 spread
is printed next to the ARV as a **confidence** measure — a wide comp set is a
reason to trust the number less, not a reason to quote three different numbers
for one house.

**Why the median and not the average.** A single forced or distressed sale can
move an average by thousands of dollars per foot; the median ignores it by
construction. This is the whole reason for using it.

**Why no haircut.** A haircut on top of the median is a second opinion with no
evidence behind it. If the comp set is right, the median is the ARV. If the comp
set is wrong, a haircut does not fix it — better comps do. An arbitrary
percentage is unfalsifiable: it cannot be checked against a sale, so it can only
ever make the number wrong in a direction nobody measured. This is why the old
tier-and-haircut method was removed.

---

## 3. Exclusions that are not optional

These are the four errors that produced wrong numbers in production, in order of cost:

1. **Deed restrictions.** Two of Akron's four best 44305 five-bed sales were restricted
   to owner-occupants under 80% AMI. They are a **floor**, not market value. Using them
   understated 156 Colony Cres by ~$20,000. If the listing copy mentions AMI, income
   limits, or a restricted sale — exclude it from ARV and keep it as a floor.
2. **Newer build / different product.** A 2020s build in a 1920s block is not a comp
   (64 Byers Ave at $155/sqft vs $65–$86 for the street).
3. **Asking prices as comps.** Never. This inflated 141 Grand Ave by **85%**.
4. **Cross-ZIP / cross-submarket bracketing.** Highland Square ≠ Kenmore ≠ Ellet.
   When the honest answer is "no sold comp exists here", the answer is **UNPRICED** —
   Akron has no sold 2–4 unit in 44302/44303 in six months, and seven leads stayed
   unpriced because of it. That was correct.

**Condos, new construction, and flips within the window** are excluded unless the
subject is the same product type. **Non-arm's-length transfers** ($325 "sale" on a
$94,300 house) are never comps — verify with the county before relying on any
recorded consideration.

---

## 4. Two books, never mixed

| | **ON-MARKET** | **OFF-MARKET** |
|---|---|---|
| Has | asking price, DOM, agent, condition notes, MLS status | owner name, mailing address, tenure, occupancy |
| Lacks | — | asking price, DOM, agent, condition |
| Valued by | **closed-sale ARV** (the ladder above) | **Zestimate anchor** (property-specific), or UNPRICED |
| Then | `(ARV × 0.70) − repairs − $10,000` vs **asking** | `(anchor × 0.70) − $10,000` = **max contract ceiling** |
| Output | sale-to-list gap, discount needed | ceiling to dial with; **never** a discount |

**ChatARV / Zestimate prices a property, not a comparable.** A property-level estimate
belongs to exactly one row, labelled by source. It is never a comp, never applied to
another property, and never blended with a closed-sale ARV. An owner record with no
asking price can never be shown as "needs a 20% discount" — there is nothing to
discount from.

**A listing found in an owner export is on-market.** The county file has no listing
status field; 1366 Marcy St sat on the off-market tab at $79,999 until someone checked.

---

## 5. Economics (one model, two percentages)

```
CEILING      = round(0.70 × ARV − repairs)        # the most you may pay
OFFER LOW    = round(0.55 × ARV − repairs)        # open here
OFFER HIGH   = round(0.60 × ARV − repairs)        # never open here
FRICTION     = CEILING − OFFER HIGH               # 10–15% of ARV, this is the room
CONTRACT     = CEILING − 10,000                   # what you must buy at for the fee
```

- **70% is a cap. 55–60% is a target under the cap. The gap is the pay stack.**
- **Never deduct the fee twice.** Ceiling already excludes it; contract subtracts it once.
- Fee is **$10,000 whole**; JV split is **50%** → `MY SIDE = $5,000`. The split is an
  output, never a setting used to make a deal work.
- If a deal doesn't work: **lower the offer, never the fee.**

Worked examples that must always reproduce (they are asserted in `comp.py --selftest`):

| ARV | Repairs | Ceiling | Offer low | Offer high | Friction | Contract |
|---|---|---|---|---|---|---|
| $150,000 | $0 | $105,000 | $82,500 | $90,000 | $15,000 | $95,000 |
| $350,000 | $34,933 | $210,067 | $157,567 | $175,067 | $35,000 | $200,067 |
| $125,000 | $0 | $87,500 | $68,750 | $75,000 | $12,500 | $77,500 |

---

## 6. The six checks that make an ARV defensible

A number isn't done until all six pass. `scripts/comp.py` enforces these and fails loudly.

1. **Same neighbourhood** — comp neighbourhood == subject neighbourhood, exactly.
2. **≥3 comps**, never fewer.
3. **Radius ≤ 1.50 mi**, and it is reported.
4. **Every comp sale inside the window.**
5. **No invented ARV** — an unpriced row carries no ARV, no basis, no confidence value.
6. **No repairs without a grade** — `REPAIRS STATUS = UNGRADED` and the field is blank.

Every check must compare **two independent things**. A check that compares a constant to
itself is worse than no check: it manufactures a false PASS. And every check must be
**proven able to fail** — run `python3 scripts/comp.py --selftest`, which injects one defect per check.

---

## 7. Reporting format

Never report a single point estimate without its skeleton:

```
141 Grand Ave, 44302 — 3/1, 1,642 sf
ARV $137,012   basis: 1,642 sf × $83.44/sf MEDIAN   n=4   radius 0.50 mi   44302   TIGHT
Anchor used: none (on-market, comps available)
Ceiling $77,500 @ $10,000 repairs → contract $67,500 vs ask $95,000 → needs −29%   REJECT
```

Rules for the output:
- State **n**, **radius**, **neighbourhood**, **confidence** on every ARV. No exceptions.
- Report the comp-set **spread** as confidence. Never turn it into a range of ARVs.
- Label every number `ESTIMATE — not an appraisal, not an offer`.
- Name what you could not get (MLS access, interior, rent roll, county records) and how
  that weakens the number. An ARV with a hidden assumption is a lie with a decimal point.
- **`UNPRICED` is a complete answer.** Seven Akron leads were correctly left unpriced.
  The goal is to kill bad leads cheaply, not to give every property a number.
