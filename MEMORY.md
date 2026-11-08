# Memory: Wholesale Real Estate

- All real estate sourcing, comping, ARV, repair, underwriting and offer work is governed by one skill: `chidubemchinedu8-code/wholesale-realestate`, `SKILL.md`. The repository is the source of truth; conversation memory is not [added: 2026-11-08]
- Load it before any deal work: read `SKILL.md`, run `bash scripts/preflight.sh`, and require `PREFLIGHT PASSED` before quoting a number [added: 2026-11-08]
- If the skill or its preflight is missing or failing, STOP and report it. Never fall back to generic Zillow browsing or a remembered workflow [added: 2026-11-08]
- The stale older `superpowers/skills/real-estate-deal-sourcing` copy was DELETED 2026-11-08: it omitted comp.py, anchor.py and comping/COMPING.md, so it was a loadable instruction set with the ARV rules missing. `wholesale-realestate` is now the only copy; do not re-add it there [added: 2026-11-08]
- Business: Nigeria-based virtual US wholesaler operating through RealVenture. Markets: Cleveland OH, Akron OH, Columbus OH, Dayton OH, Birmingham AL, Atlanta GA. Buy box is a guideline, never a buyer commitment [added: 2026-11-08]
- Fee $10,000 whole, 50% JV split. Lower the offer, never the fee [added: 2026-11-08]
- Defects found by audit are recorded in `AUDIT.md` with reproductions. UNKNOWN never satisfies a rule; anything that narrows the comp pool must print its effect; buyer max is never labelled MAO; the arithmetic is internally consistent but UNVALIDATED against real outcomes [added: 2026-11-08]
- Zillow = primary discovery reference; **Redfin AND Realtor.com are read after it — all three, every scan**, enforced in `zip_ledger.py` (a single-source scan is refused). Neither is licensed data. **Photos are read on the Zillow page as part of discovery, before a lead is scored.** Scanning starts in the Zillow-primary market (Dayton OH); the scan ledger records which site discovered each ZIP. Operator restated this twice on 2026-11-08 after I started on Redfin/Cleveland — it is the standing norm, not a preference [added: 2026-11-08, reinforced]
- NAR model MLS rules §4.4.1 forbid using MLS/IDX data for business solicitation - a licensed feed prices deals, it cannot find them [added: 2026-11-08]
- Lead ledgers are COMMITTED, append-only history (`state/`), never gitignored: a fresh clone must inherit scan history or the duplicate guard resets and old properties get re-reported as new. Never delete a row, never rewrite history [added: 2026-11-08]
- ARV is ONE method: subject sqft x MEDIAN $/sf of the comp set. No haircut, no percentile tiers, no second route. The p25-p75 spread is reported as confidence only. User-directed 2026-11-08; the 0.88 haircut was mine, had no evidence, and is deleted permanently [added: 2026-11-08]
- Comping v2.1: bed-count floor, renovated-condition-only ARV pool, ±45% consistency gate that never reinstates an outlier, repair tiers $20/$35/$50 per sf [added: 2026-11-08]
- **ARV needs >=3 comps (`comping/COMPING.md` §0, `comp.py` MIN_COMPS=3). FIVE is the separate submission standard (`SKILL.md` rule 2, `comps.py`). `COMPING.md` governs ARV arithmetic.** Do not confuse the two [added: 2026-11-08]
- **DO NOT INVENT SOURCING FILTERS.** A Dayton sweep ran on a $100,000 max ASKING price and a 3+ bed floor — neither exists in the repo. The buy box caps the ARV ($125k-$900k) and the 70% ceiling, never the asking price. `on-market.md` requires ALL ACTIVE LISTINGS, ALL TYPES per ZIP, every one recorded with a reject reason, and `x of y` coverage reported. Coverage of 31/31 was withdrawn because it measured a self-selected subset. `AUDIT.md` A-7 [added: 2026-11-08]

- **A ZIP IS NOT A NEIGHBOURHOOD.** Dayton 45405 contains 14+ hoods whose medians differ by 2x (Grafton Hill $128,435 vs Southern Dayton View $48,455). Nine leads were priced off the wrong pool in one pass. No subject is priced until its hood is established from a named source and that source is written next to the number. `references/hood-verification.md` [added: 2026-11-08]
- **`DEFECT_LOG.md` is append-only institutional memory** — read it after preflight, every session. Never trim it. Preflight fails if it drops below 10 entries [added: 2026-11-08]
- **Zillow hood URLs silently redirect to the full ZIP feed** when the slug is not a real region. `/dayton-oh-45405/fairview/` returns all 118 listings of 45405. Check the page title names the hood [added: 2026-11-08]
- **Hood SOLD feeds are not hood-coherent** (Fairview sold → 45406 rows; Grafton Hill sold → Brookville 45309). Active feeds usually are. Never pool a sold feed wholesale [added: 2026-11-08]
- **A wrong-hood ARV is worse than a blank.** A blank gets re-worked; a wrong number gets quoted to a seller [added: 2026-11-08]
- **Verdicts are arithmetic, not judgement** (see DEFECT_LOG D-5): PASS = at/under MAO with 5-20% headroom; PRIORITY = at/under MAO with 20%+; MARGINAL = within 5% of MAO either side or under ceiling; NEGOTIATE = at/above ceiling [added: 2026-11-08]
- **`comp.py --tier` alone computes economics with $0 repairs.** Always pass `--tier` AND `--repairs sqft*rate` to get a real ceiling [added: 2026-11-08]

## Index

- [[wholesale-realestate]] — the full operating procedure: preflight, pipeline, hard rules, red flags, report contract
