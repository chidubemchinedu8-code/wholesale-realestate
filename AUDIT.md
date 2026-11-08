# Flaw audit — 2026-11-08

Written against `SKILL.md` v2.2.0, with the full suite and preflight green.
Every finding below was reproduced, not inferred. Reproductions are inline.
This file exists so the next session inherits the doubts as well as the code.

Severity: **S1** produces a wrong number or a wrong decision. **S2** produces
an unnoticed omission. **S3** cosmetic/robustness.

---

## S1-1. The duplicate guard is defeated by punctuation

`scripts/zip_ledger.py:126` normalises with `.strip().lower()` and nothing else.

```
$ python3 scripts/zip_ledger.py --check "141 Grand Ave" --city Akron --zip 44302
SEEN - first seen 2026-10-31, last 2026-10-31, verdict REJECT, price 95000

$ python3 scripts/zip_ledger.py --check "141 Grand Avenue" --city Akron --zip 44302
NEW - not in the property ledger
```

Same house, two spellings, reported as a new opportunity. Portals disagree on
`Ave`/`Avenue`, `St`/`Street`, `N`/`North`, and add `, Akron OH 44302`. This is
the exact failure the ledger was built to prevent, and a full test suite passes
while it fails.

**Fix:** suffix/directional/city/zip5 normalisation + a fuzzy fallback.

---

## S1-2. A negative MAO is quoted as a normal figure

`scripts/underwrite.py` returns `$-6,000` and exits `0`.

```
$ python3 scripts/underwrite.py --arv 120000 --repairs 90000 --fee 10000
  BUYER MAX CONTRACT      $-6,000
  SELLER-FACING MAO      $-16,000
$ echo $?
0
```

There is no deal, but the tool reports success and the caller sees a formatted
table. The repo's whole claim is that it refuses rather than guesses; here it
guesses at zero.

**Fix:** refuse on `seller_mao <= 0` with a distinct exit code, and fix the sign
formatting (`$-6,000` → `-$6,000`).

---

## S1-3. Zero reeds in the bed floor

`comp.py` drops a comp only when the bed count is *known* and below the subject:

```python
kept = [c for c in usable if c.beds_n is None or c.beds_n >= subject_beds]
```

A blank `beds` cell — i.e. `UNKNOWN` — passes. Reproduced with four comps at the
same address distance, where only the 2-bed comp can reach `n=3` at 0.25 mi:

| comps file | result |
|---|---|
| 2-bed comp present, beds known | n=3, `under_bed_floor: 1`, ARV LOW `$108,497` |
| **same file, beds cell blanked** | **n=4, `under_bed_floor: 0`, ARV LOW `$108,559`** |

The rule is "a comp may never have fewer beds than the subject". The code
implements "a comp may never have *fewer known* beds". Every `UNKNOWN` silently
joins the ARV pool. This contradicts hard rule 17 and `references/data-integrity.md`.

**Fix:** `UNKNOWN` beds fail the floor by default (exclude), with an explicit
opt-in to include them and a printed warning when it is used.

---

## S1-4. The style filter is silent, undocumented, and changes which comps win

Inside the radius loop, `comp.py` replaces the comp set when ≥3 comps share the
subject's style:

```python
styled = [c for c in cand if c.style and c.style == style]
cand = styled if len(styled) >= MIN_COMPS else cand
```

No check asserts it ran, no report line says it ran, and it is not in the
`comping/COMPING.md` ladder description the user validated. It can cut a 6-comp
pool to 3 that all happen to be colonials and move the ARV.

**Fix:** report it (`STYLE FILTER APPLIED n: 6 → 3`) so the choice is visible.

---

## S1-5. Nothing in the system can record a negative neighbour

`grep -ri "busy road|railroad|power line|industrial|highway|noise|odor|flood|
landfill|commercial adjacent"` returns nothing across `scripts/` and
`references/`. There is no field, no note, no check.

A textbook Akron subject 40 ft from an active rail line comps identically to the
same house two streets over. The system will price it the same and call it a
deal. `references/condition.md` covers the *building*; no reference covers the
*location* beyond "same neighbourhood code".

**Fix:** a required `LOCATION` block in the report with an explicit
"adverse external influence" question, and a cap to `POTENTIAL` when one is
present and unexplained.

---

## S1-6. The printed "MAO" is not the MAO the other script uses

`comp.py --repairs` prints a section titled **`MAO BY TIER (Step 9)`**, computed
as `(ARV × 0.70) − repairs`. That is the *buyer's maximum*, not the seller-facing
MAO.

At ARV $125,000 / repairs $65,000:

| script | label | value |
|---|---|---|
| `comp.py` | `MAO BY TIER` | **$22,500** |
| `underwrite.py` | `SELLER-FACING MAO` | **$12,500** |

A $10,000 gap — the fee — under the same three-letter label. The user's own spec
said buyer max and seller MAO are different numbers; `SKILL.md` rule 10 says so;
and then the comp engine prints the buyer's number labelled MAO.

**Fix:** rename the comp.py block to `BUYER MAX BY TIER` and print the
seller-facing figure beside it.

---

## S1-7. `AS-IS` and `ARV LOW` are the same number, presented as two findings

```python
result.arv_low = int(round(subject_sqft * p25 * HAIRCUT))
result.as_is   = int(round(subject_sqft * p25 * HAIRCUT))   # identical expression
```

The CLI prints them on consecutive lines as though they were independent
measures of two different conditions. They are one number. A reader reasonably
concludes the as-is value is 88% of the renovated low value; it is not, it is
the same field.

**Fix:** state plainly that `AS-IS` is an alias of `ARV LOW`, or drop one.

---

## S2-1. The universal engine assumes US/Akron geometry

`miles()` is a flat-earth approximation (`69 mi/degree`) with no state-plane or
projection handling, and `hood` is compared to a ZIP string. Inside Ohio this is
fine. The script is presented as universal and is silently wrong near a
projection boundary or where a "neighbourhood" is not a ZIP. Every fixture and
every selftest coordinate is `SYNTH-44302` / `41.079, -81.536`. There is no test
of the engine outside Akron.

---

## S2-2. Time is not adjusted for

ARV is computed from nominal sold prices. With a 180-day window, comps average
~3 months of lag:

| market growth | comps are, on average |
|---|---|
| 5%/yr | 1.25% under today |
| 12%/yr | 3.0% under today |
| 25%/yr | 6.25% under today |

In a flat Akron this is inside the noise. In Columbus/Atlanta it is not, and
nothing in the code or docs mentions a time adjustment. The window is treated as
though a 5-month-old sale and a 5-day-old sale are equivalent.

---

## S2-3. Conservative adjustments stack, and the product was never measured

For the worked example: p50 implies `$137,012` of market value. Then:

```
x 0.88 haircut          -> ARV POINT   $120,571
underwrite to p25       -> ARV LOW     $114,578
x 0.70 buyer cap                       $80,204
- repairs $57,470                      $22,734   <- printed as "MAO"
```

That is **16.6% of median market value**. Each step is defensible alone; nobody
ever multiplied them together. Either the stack is too conservative — you will
decline good deals — or the pieces are individually miscalibrated. The system has
no idea which, because it has never recorded an outcome to check against.

This is the most important limitation in the repo: **the arithmetic is internally
consistent and empirically unvalidated.** The suite proves the rules run as
written. No test checks that following them makes money.

---

## S2-4. Most "tests" assert text, not behaviour

Most condition-based checks in the suite are `grep`/file-existence
assertions; a minority execute an engine. "The rule is written down" and "the rule
holds" are different claims, and the pass count blurs them. The comp engine's own
checks are behavioural; the surrounding majority are mostly documentation lint.

---

## S2-5. Ledger state is only as good as manual entry

`load_comps` silently accepts:

- a comp with **no `condition` column** → `""` → treated as not-renovated and
  dropped, so a CSV with a missing column returns `NO COMPS` with no explanation
  that a column was missing. Correct refusal, unhelpful cause.
- `sold` in the future, silently kept (the window has no upper bound).
- duplicate rows for the same sale (double-counted in p25/p50/p75).
- a `hood` that is blank → matches nothing → `NO COMPS`.

Each is a silent-zero rather than an error.

---

## S2-6. The docs still overclaim in three places

- `README.md` calls the system "executable rules that fail loudly". Seven of the
  eleven failure modes this audit found exited `0`.
- `SKILL.md` implies the reference set is complete; there is no `references/location.md`.
- The preflight reports "PASSED" without ever exercising the comp ladder on a
  *real* fixture — only the synthetic selftest.

---

## S3-1. Cosmetic

- Negative money prints `$-6,000` (sign inside the dollar sign).
- `comp.py` docstring says v2.1 while `SKILL.md` is v2.2.0; they version the
  engine and the rulebook separately with no stated mapping.
- `--window` accepts any value ≤365 including negative; a negative window yields
  an empty universe → silent `NO COMPS`.

---

## What this audit does NOT claim

- That the comp ladder is wrong. It implements the user's spec faithfully; the
  discrepancies above are at the edges (unknowns, labels, normalisation).
- That the ARV is inaccurate. It is unaudited — nobody has compared 20 ARVs to
  actual outcomes.
- That the licensing recommendation is wrong. It is unverified against a live
  MLS contract, which cannot be done from here.

## The honest summary

The system is good at **refusing** and bad at **noticing**. It refuses well when
data is clean and present (no comps, no ARV, ungraded repairs). It notices badly
when data is dirty, missing, renamed, or inconvenient — and dirty data is the
normal state of real estate research. The suite mostly proves the documentation
matches the code. They do not prove the code matches reality.

## Fix log

| finding | status |
|---|---|
| S1-1 address normalisation | fixed — suffixed/directional/city/zip5 normalisation + fuzzy fallback |
| S1-2 negative MAO | fixed — refuses, exit 4, sign formatting corrected |
| S1-3 unknown beds | fixed — UNKNOWN fails the floor; opt-in flag prints a warning |
| S1-4 silent style filter | fixed — reported in output and in the result basis |
| S1-6 mislabelled MAO | fixed — now `BUYER MAX BY TIER`, with seller-facing printed beside |
| S1-7 as-is = arv low | fixed — labelled an alias in output and code comment |
| S2-5 silent CSV zeros | partly — missing-column and duplicate-sale now named in the refusal note |
| S1-5 no location field | open — needs a `references/location.md` and a gate field |
| S2-1 geometry assumptions | open — documented, not fixed |
| S2-2 no time adjustment | open — documented, not fixed |
| S2-3 unvalidated calibration | the 0.88 haircut is DELETED (removes 12% of the unexplained stack). **The 0.70 cap is RESOLVED as policy (2026-11-08): the operator confirmed 0.70 is a deliberate midpoint of a 0.65–0.75 operating range, chosen as the safe space, and will hold to it.** That makes it a stated buy-box rule, not a measured constant — which is the only claim this file ever made about it. Still genuinely open: the median $/sf basis itself has never been checked against an actual resale, and neither has any buyer's real maximum |
| S2-4 test kind blur | open — labelled in this file, not yet split in the suite |


---

## Resolution: the 0.70 cap (2026-11-08, user-directed)

The audit asked whether 0.70 was measured. The operator's answer: it was never
claimed to be measured. It is a deliberate operating range — 0.75 in a hot market
with a known scope, 0.65 in a slow market or an unknown scope — and 0.70 is the
safe-space midpoint, which is what the system will use.

**So the finding is closed as a policy decision, not as a measurement.** The
distinction matters and is kept in `references/underwriting.md`: a deal that only
clears at 0.75 is reported as such, and 0.70 is never silently replaced. What
remains unvalidated is upstream — the median $/sf ARV has no resale behind it.

## Post-audit correction: the 0.88 haircut (2026-11-08, user-directed)

The finding that mattered most was not in the list above. It was found by
comparing this system's ARV against RealVenture's published method:

> We take the median price per square foot across your five comps and multiply
> by your subject's size. Median, not average, so one strange sale cannot drag
> your ARV around.

This repo was computing `p75 × sqft × 0.88`, and defaulting to `p25 × sqft × 0.88`
whenever confidence was not HIGH. Both differ from the house method.

On 262 S Harris Ave:

| method | ARV | seller MAO | % of asking |
|---|---|---|---|
| median, no haircut | $169,200 | $69,240 | 86.7% |
| p50 x 0.88 | $148,896 | $55,027 | 68.9% |
| p25 x 0.88 | $124,202 | $37,741 | 47.2% |

The same house read as "MAYBE, a $10,660 gap" under the house method and "NO"
under mine. The verdict difference was produced entirely by a constant.

**The 0.88 had no source.** It is not in the user's ten-step spec, it is not an
appraisal adjustment, and it is not backed by any sale/resale observation. It was
in the repo before this session and was carried forward and defended in prose
("the 0.88 backs it off") without ever being justified. That is the exact failure
mode this file exists to catch: a number that looks like a rule and is actually a
guess.

**Deleted.** ARV is now `sqft × median $/sf`, one method, one number. The
p25–p75 spread is reported as confidence instead of being turned into three
different ARVs. A guard test fails the suite if a haircut, a percentile tier or
a second formula reappears in the engine.

Lesson for the next audit: the dangerous numbers are not the ones the code
computes, they are the constants it was told to use.
