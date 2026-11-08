# Dayton — does this actually conform to the repo framework?

Honest audit, 2026-11-08. Written because the question was asked directly, and the
right answer is a check, not a reassurance.

## Verdict: NO, not fully. 30 of 31 candidates examined, but the framework has steps beyond that.

The property sweep is close to done. **Framework conformance was not.** Four things were
missing or wrong, and they are now fixed or explicitly open.

---

## Gap 1 — the anchor step was skipped on every ZIP. FIXED, and now confirmed non-binding on comps.

`anchor.py` is step one of the framework and it had never been run on any Dayton ZIP.
It exists to sanity-check a comp pool before it is trusted. Run now:

| ZIP | anchor status | median $/sf | vs the band actually used |
|---|---|---|---|
| 45402 | OK (5 sales) | $120.07 | matches the $122.30 used |
| 45403 | **UNKNOWN** (4 sales, needs 5) | — | **$105.41 band is unanchored** |
| 45404 | OK (6 sales) | **$65.93** | **vs $128.76 used — 95% higher** |
| 45405 | OK (5 sales) | **$57.21** | **vs $129.92 used — 127% higher** |
| 45406 | **UNKNOWN** (2) | — | band already refused |
| 45410 | **UNKNOWN** (3) | — | band already refused |
| 45417 | **UNKNOWN** (2) | — | band already refused |

**This is the finding that matters most.** In 45405 and 45404 the ZIP-wide median $/sf is
roughly *half* the renovated band I priced against. That is not necessarily an error — the
anchor is the whole ZIP including dated stock, the band is renovated-only — but it means
every ARV in those two ZIPs rests on the claim that the comps really are renovated, and on
nothing else. In 45405 that claim is strong (three sales at $120–$132 with 4.8% spread).
In 45404 it rests on **two** sales, one of them (34 Ingleside) whose coordinate I cannot
verify in OSM.

**Confirmed non-binding on comps.** `comp.py` and `indicative_arv.py` contain zero
references to `anchor.py` — it cannot feed an ARV. Proven by running the same subject
before and after an anchor pass: ARV $154,516 both times, median $128.76/sf both times.

One honest defect found while proving it: `anchor.py` required 8 sales before testing for
bimodality, but printed "single distribution - the ZIP median is a usable sanity check"
when it had only 6 and had not tested at all. It now prints **NOT TESTED** with the reason.

**What it changes: nothing about the arithmetic, everything about confidence.** 1012 St
Adelbert's ARV of $154,516 is a renovated-band number in a ZIP whose overall median is
$65.93/sf. If 185 Grove and 34 Ingleside are not both genuine full renovations, that ARV
is roughly double reality. It is already a PASS at 87% over MAO, so the verdict holds —
but the ARV is the softest number in the set and should be labelled that way.

Three ZIPs (45403, 45406, 45410, 45417) have too few sales to anchor at all. Their bands
are stated, usable, and **unanchored**. That is the honest label.

## Gap 2 — the property ledger was empty for 20 of 24 Dayton properties. FIXED.

`state/property_ledger.csv` is append-only on purpose: "a fresh clone must inherit the
scan history, or the duplicate guard resets and old properties get re-reported as new
finds." It held 4 Dayton rows. I had just examined 20 more and written them to a markdown
file and a sheet, not the ledger. **All 20 are now logged** with verdict, price, comps,
repairs, MAO and the caveats — 24 Dayton rows total.

## Gap 3 — RESOLVED BY OPERATOR DECISION: discovery is all three feeds.

I logged `45403`, `45404`, `45406` with `source=realtor.com` and the test failed me. The
first fix (relabel to zillow-only) was too narrow: the operator's actual rule is **Zillow
primary, then go further into Redfin and Realtor.com — all three, for a wider margin.**

Rule and code now agree:

- `SKILL.md` rule 20 and `references/on-market.md` rewritten to the three-feed standard.
- `zip_ledger.py` accepts `zillow+redfin+realtor.com` and **still refuses** a scan that
  skipped Zillow, and **refuses a single-source scan** — one feed is not a cross-check.
- New selftest cases cover all three branches. The suite's own count is printed at
  the end of every run — do not hard-code it here, it rots the moment a test is added.
- All 7 Dayton ZIP rows now log `zillow+redfin+realtor.com`.

I logged `45403`, `45404`, `45406` with `source=realtor.com`. The test failed on it, and
it was right to: rule 20 is **Zillow discovers, Redfin/Realtor.com cross-check.** I had
used Realtor.com to *price*, which is allowed and in fact the strongest source available,
and then wrote it into the *discovery* field, which is a different claim. Corrected to
`zillow` with the distinction spelled out in notes. **This is the kind of error that makes
a ledger lie quietly.**

## Gap 4 — 45417 3 of 3. CLOSED.

Candidate 3 was never named in writing — my note said "3 candidates" but only one was
logged. Re-derived the buy box from Realtor.com and examined **162 Lorenz Ave**, $80,000,
3bd/1,344 sf, "Investor Special, sold as-is, will need renovation". Coverage is **31/31**.

It prices to UNPRICED, for a verified reason: all three renovated 45417 sales are
1.84–1.89 mi away, past the 1.5 mi cap.

## Also fixed
All 7 Dayton ZIPs are now scored in `assets/zip_universe.csv` with written evidence
(previously `UNRANKED`, blank score, `never scanned` — the file still said never scanned
after the work was done). Scored: 45417 74 A · 45405 74 A · 45410 60 B · 45406 58 B ·
45403 55 B · 45402 48 C · 45404 42 C. All 7 now have a `zip_ledger.csv` row.

`zip_ledger --due` is now clean for Dayton — no re-scans owed. Akron 44305 and 44302 are
due, unrelated to this work.

---

## What "done zip by zip" would actually require

- Anchors: enough recent sales in 45403/45406/45410/45417 for a 5-sale median, or those
  bands stay labelled unanchored
- 45404: one more genuine renovated sale, or independent confirmation that 34 Ingleside
  was a full renovation
- 45405 Fairview: one renovated in-band sale inside 180 days to unblock the three
  Fairview properties
- Every repair grade is still a guess from listing text. None of the 31 was walked.

## Gap 5 — TWO PRICING BUGS FOUND WHILE CLOSING 45417. FIXED.

Chasing 162 Lorenz exposed both, and neither would have shown up in a passing test run.

**Bug 1 — `indicative_arv.py` had no radius cap.** It printed a `mi` column and never
filtered on it. All three 45417 comps sat at 1.84–1.89 mi; `comp.py` correctly refused to
price, and `indicative_arv.py` priced off them anyway. A script that displays a distance
without acting on it is worse than one that omits the column.

**Bug 2 — `indicative_arv.py` never compared `hood`.** `comp.py` requires an exact
neighbourhood match. The same file, in the same runs, printed the subject's neighbourhood in
its header and never filtered on it. The 45402 pool holds Dayton View, West Dayton and
Cornell Heights sales; every 45402 ARV had been averaging across them.

**Published numbers that moved:**

| Candidate | Old ARV | Corrected | Old MAO | Corrected |
|---|---|---|---|---|
| 817 Faulkner Ave | $174,886 (n=2) | **$178,073 (n=1)** | $45,420 | **$47,651** |
| 623 Anna St | $151,282 (n=2) | **$148,525 (n=1)** | $27,897 | **$25,968** |
| 945 Vernon Dr | $154,829 (n=2) | **$157,651 (n=1)** | $54,070 | **$55,545** |
| 3619 Hoover Ave | $129,146 (n=2) | **$126,792 (n=1)** | $43,442 | **$41,794** |

**No verdict flipped.** But every 45402 ARV dropped from n=2 to **n=1** — the confidence is
now materially worse than the first table implied, even where the number barely moved.
817 Faulkner gets slightly better on the corrected basis, which is an accident of which
single comp survives, not new evidence.

Both bugs now have regression tests that fail if reintroduced.

## Fairview — pushed hard, still unpriced, now demonstrably so

- **525 W Fairview Ave, sold 2026-09-09, $73,471, 1,440 sf = $51/sf.** In Fairview, in band,
  in date. **Dated** — listed at $30,000 on 2026-05-07, sold 125 days later, a 145% uplift.
  That is a trade, not a renovation.
- **127 McDaniel St, sold 2026-09-23, $240,000, 1,398 sf = $172/sf.** Genuinely renovated,
  granite counters, 2 full baths, permits. But **McPherson Town Historic District**, a
  different submarket at 3.4x Fairview. Using it would triple every Fairview ARV.
- **50 Woodcrest, $155,000, 1,500 sf, 2026-05-01.** Still 11 days outside the window.

The Fairview gap survives a genuine search. One sale in the ZIP could price it and it is
eleven days too old.

## Bottom line

**Coverage is now 31/31** and the two bugs above are fixed and tested. Fairview is unpriced
on evidence that took real work to establish.

The **sourcing and pricing** is in good shape — 11 ARVs, 20 ledger rows, dated comps, and
the failures are real failures rather than blanks. The **bookkeeping and the anchor step**
were behind, and are now caught up except for the four items above. The two numbers I would
not put money behind without a walkthrough are **624 N Broadway's $303,534** (n=1, $115,000
repair assumption) and **1012 St Adelbert's $154,516** (n=2 in a ZIP whose own median is
half that).
