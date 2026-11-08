# Wholesale Real Estate — operating notes

Detail lives in `SKILL.md` and `references/`. This file is the short index of
where each rule is enforced and how to prove it still holds.

- Entry point: the only copy is `SKILL.md` at the repo root; `scripts/preflight.sh` loads it and prints its version, so never hard-code a version here - it drifts [added: 2026-11-08]
- Comp/ARV arithmetic, deeper rulebook: `comping/COMPING.md`; executable in `scripts/comp.py` — neighbourhood gate, radius ladder 0.25→1.50 mi, ≥3 comps same neighbourhood, **sqft × median $/sf, no haircut**, `NO COMPS` rather than a widened radius [added: 2026-11-08]
- Five-comp submission standard: `references/comps.md`; enforced by `scripts/comps.py` (no ARV under five) [added: 2026-11-08]
- On-market priorities and the 14-day rejection: `references/on-market.md`; enforced by `scripts/rank_listing.py` [added: 2026-11-08]
- Off-market signals, PropWire limits, county GIS workaround: `references/off-market.md` [added: 2026-11-08]
- Buyer max ≠ seller MAO, gross spread ≠ profit: `references/underwriting.md`; enforced by `scripts/underwrite.py` — the $200K/$25K/$10K case must print 115,000 / 105,000 / 70,000 [added: 2026-11-08]
- 15-point gate and the 16-section report: `references/qualification.md`; enforced by `scripts/gate.py` [added: 2026-11-08]
- Five provenance labels; the never-rules live in SKILL.md (rules 1-20) with provenance in `references/data-integrity.md` [added: 2026-11-08]
- ZIP scoring, ledger schema, cadence: `references/market-research.md`; enforced by `scripts/zip_ledger.py` (duplicate guard) [added: 2026-11-08]
- Subject verified across four sources (public records win on hard facts, MLS remarks on condition); platted subdivision beats an aggregator polygon [added: 2026-11-08]
- Repair tiers: light $20/sf, moderate $35/sf (default when unconfirmed), heavy $50/sf, sized as a ±15% range [added: 2026-11-08]
- Median anchor: `scripts/anchor.py` — ZIP/neighbourhood median $/sf plus bimodal detection; refuses to invent a median under 5 sales [added: 2026-11-08]
- Data access and licensing: `references/data-access.md` - MLS/RESO routes, per-market boards, and why a licensed feed may price deals but may never source them [added: 2026-11-08]
- Known defects and their fixes: `AUDIT.md` - reproduced findings, what is fixed, what is still open (location risk, geometry assumptions, no time adjustment, unvalidated calibration). Read before trusting a number [added: 2026-11-08]
- Photograph limits — never claim a roof/foundation/electrical is sound: `references/condition.md` [added: 2026-11-08]
- Known blocker: `gis.cuyahogacounty.gov` is unreachable from the Arena sandbox (TLS closed by egress). Use the GitHub Actions pattern in `references/off-market.md`; do not report "the county has no data" [added: 2026-11-08]
- Known blocker: PropWire search needs a logged-in session; property-detail URLs 404 without an internal ID [added: 2026-11-08]
