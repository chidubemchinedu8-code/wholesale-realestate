# Dayton — does this actually conform to the repo framework?

Honest audit, 2026-11-08. Written because the question was asked directly, and the
right answer is a check, not a reassurance.

## Verdict: NO, not fully. 30 of 31 candidates examined, but the framework has steps beyond that.

The property sweep is close to done. **Framework conformance was not.** Four things were
missing or wrong, and they are now fixed or explicitly open.

---

## Gap 1 — the anchor step was skipped on every ZIP. FIXED.

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

## Gap 3 — I invented a discovery source. FIXED, and the test caught it.

I logged `45403`, `45404`, `45406` with `source=realtor.com`. The test failed on it, and
it was right to: rule 20 is **Zillow discovers, Redfin/Realtor.com cross-check.** I had
used Realtor.com to *price*, which is allowed and in fact the strongest source available,
and then wrote it into the *discovery* field, which is a different claim. Corrected to
`zillow` with the distinction spelled out in notes. **This is the kind of error that makes
a ledger lie quietly.**

## Gap 4 — 45417 is still 2 of 3. OPEN.

Not closed out, not marked done. One candidate unexamined. Coverage is **30/31**, and the
row in the sheet says so.

## Also fixed
All 7 Dayton ZIPs are now scored in `assets/zip_universe.csv` with written evidence
(previously `UNRANKED`, blank score, `never scanned` — the file still said never scanned
after the work was done). Scored: 45417 74 A · 45405 74 A · 45410 60 B · 45406 58 B ·
45403 55 B · 45402 48 C · 45404 42 C. All 7 now have a `zip_ledger.csv` row.

`zip_ledger --due` is now clean for Dayton — no re-scans owed. Akron 44305 and 44302 are
due, unrelated to this work.

---

## What "done zip by zip" would actually require

- 45417 candidate 3 examined → 31/31
- Anchors: enough recent sales in 45403/45406/45410/45417 for a 5-sale median, or those
  bands stay labelled unanchored
- 45404: one more genuine renovated sale, or independent confirmation that 34 Ingleside
  was a full renovation
- 45405 Fairview: one renovated in-band sale inside 180 days to unblock the three
  Fairview properties
- Every repair grade is still a guess from listing text. None of the 31 was walked.

## Bottom line

The **sourcing and pricing** is in good shape — 11 ARVs, 20 ledger rows, dated comps, and
the failures are real failures rather than blanks. The **bookkeeping and the anchor step**
were behind, and are now caught up except for the four items above. The two numbers I would
not put money behind without a walkthrough are **624 N Broadway's $303,534** (n=1, $115,000
repair assumption) and **1012 St Adelbert's $154,516** (n=2 in a ZIP whose own median is
half that).
