# Memory: Wholesale Real Estate

- All real estate sourcing, comping, ARV, repair, underwriting and offer work is governed by one skill: `chidubemchinedu8-code/wholesale-realestate`, `SKILL.md`. The repository is the source of truth; conversation memory is not [added: 2026-11-08]
- Load it before any deal work: read `SKILL.md`, run `bash scripts/preflight.sh`, and require `PREFLIGHT PASSED` before quoting a number [added: 2026-11-08]
- If the skill or its preflight is missing or failing, STOP and report it. Never fall back to generic Zillow browsing or a remembered workflow [added: 2026-11-08]
- A fuller fork-local copy also exists at `chidubemchinedu8-code/superpowers` → `skills/real-estate-deal-sourcing`, but this session's GitHub App cannot write to that repo (403 on push). `wholesale-realestate` is the writable, authoritative copy [added: 2026-11-08]
- Business: Nigeria-based virtual US wholesaler operating through RealVenture. Markets: Cleveland OH, Akron OH, Columbus OH, Dayton OH, Birmingham AL, Atlanta GA. Buy box is a guideline, never a buyer commitment [added: 2026-11-08]
- Fee $10,000 whole, 50% JV split. Lower the offer, never the fee [added: 2026-11-08]
- Zillow = primary MANUAL discovery reference; Redfin = secondary cross-check. Neither is licensed data [added: 2026-11-08]
- NAR model MLS rules §4.4.1 forbid using MLS/IDX data for business solicitation - a licensed feed prices deals, it cannot find them [added: 2026-11-08]
- Lead ledgers are COMMITTED, append-only history (`state/`), never gitignored: a fresh clone must inherit scan history or the duplicate guard resets and old properties get re-reported as new. Never delete a row, never rewrite history [added: 2026-11-08]
- Comping v2.1: bed-count floor, renovated-condition-only ARV pool, ±45% consistency gate that never reinstates an outlier, LOW/POINT/HIGH ARV, repair tiers $20/$35/$50 per sf, MAO per ARV tier [added: 2026-11-08]

## Index

- [[wholesale-realestate]] — the full operating procedure: preflight, pipeline, hard rules, red flags, report contract
