Wholesale Real Estate - Sourcing & Underwriting System

  >>> START HERE: this repository is the single source of truth for all deal
  >>> sourcing, comping and underwriting. Run `bash scripts/preflight.sh` first.
  >>> The binding rulebook is SKILL.md. Nothing else in this repo overrides it.

  One skill, one procedure, executable rules that fail loudly:
  SKILL.md (entry) + references/ (detail) + comping/ (arithmetic) +
  scripts/ (enforcement) + fixtures/ (proof) + state/ (history).

  Prove it still holds:
      bash scripts/preflight.sh               # must print PASSED
      bash tests/test-real-estate-skill.sh    # must print STATUS: PASSED
      python3 scripts/comp.py --selftest      # must print 9/9, 9 injected defects caught

  Exit codes are the contract. No count is written down here on purpose: a
  documented number rots the moment a test is added, and a stale claim in a
  doc is exactly the kind of inaccuracy this repo is built to refuse.

  >>> Read AUDIT.md before trusting a number: the arithmetic is internally
  >>> consistent and has never been checked against a real outcome.
  >>> There is exactly ONE SKILL.md. If you find a second copy of this skill
  >>> anywhere on the machine, it is stale - use the one that preflight loads.

What this is

  A wholesale real-estate sourcing and underwriting procedure, written as a
  Claude Code skill and enforced by code. It is deliberately rigid: the value is
  in the refusals, not the suggestions.

What it does

  Sourcing (Zillow primary, Redfin cross-check)
    Scans by ZIP, never by browsing a city. Ranks listings on days on market,
    price reductions, back-on-market, as-is language and photo evidence, then
    rejects on the 14-day rule, turnkey condition, and unsupported comps.
    Licensed MLS data is NOT used for sourcing - NAR rules forbid it. See
    references/data-access.md.

  Valuation (rule-based, not vibes)
    ARV = subject sqft x the comp set's $/sqft, anchored in the same
    neighbourhood and ZIP. Filters run inside the radius loop: bed floor,
    renovated-only, +/-30% sqft, +/-45% consistency. Report LOW / POINT / HIGH,
    never a single number. Under 3 comps the answer is NO COMPS.
    Under 5 comps it is not a submission. The rulebook is comping/COMPING.md;
    scripts/comp.py runs it and proves every rule can fail.

        python3 scripts/comp.py --selftest
        python3 scripts/comp.py --comps fixtures/akron_44302_worked_example.csv \
            --as-of 2026-10-31 --tier moderate

  Underwriting
    Buyer max = (ARV x 0.70) - repairs. Seller MAO is a different, lower number.
    Gross spread is not profit. Repairs are tiered (light $20 / moderate $35 /
    heavy $50 per sqft) and blank until condition is graded.

  Gate
    15-point qualification and the report format. A property that misses the
    gate is reported as POTENTIAL or REJECTED, with the reason - never padded.

How to run it

  Open this repository in a session. CLAUDE.md / AGENTS.md / GEMINI.md /
  .cursorrules all route here. Then:

      bash scripts/preflight.sh
      cat SKILL.md                      # the binding rulebook
      python3 scripts/zip_ledger.py --due    # what is owed a re-scan

  The ledgers in state/ are committed on purpose: a fresh clone must inherit
  what has already been analysed, or the duplicate guard resets.

Non-negotiables

  - Every number carries a source and a date, or it is UNKNOWN.
  - UNKNOWN stops the analysis. It is never filled in to make a deal pass.
  - No comps, no ARV. No ARV, no offer.
  - Report zero if zero qualify.
