# Cleveland Wholesale Queue — Reconciliation and Triage

## Counting reconciliation

The local `distressed_property_leads_master.csv` and `distressed_property_leads_underwriting_tracker.csv` each have **96 physical data rows**, not 92.

The four-row difference is explained by four generic category/placeholder source rows — **006, 008, 009, and 010** — that do not identify a distinct property. Removing only those raw non-property rows yields the user-stated **92-row intended property-lead population**. No separate 92-row source file was located, so this is an explicit reconciliation rule rather than a claim that the local raw files themselves contain 92 rows.

### Reconciled population

| Lane | Count |
|---|---:|
| Strict operational wholesale queue | 25 |
| Material-fact / configuration hold — not operational | 9 |
| Reference / no-pursuit — not operational | 47 |
| REO / foreclosure / bank-owned / auction — excluded | 9 |
| No identifiable subject — not operational | 2 |
| **Reconciled intended population** | **92** |

Add the four generic non-property source rows back to reconcile to **96 raw local rows**.

## Strict action-queue rule

A lead is in the 25-row action queue only when it is an identifiable, currently publicly available candidate without a documented REO/auction classification, explicit anti-wholesale/no-assignment prohibition, fixed standing screen failure, or unresolved material fact/configuration issue. Inclusion is **not** an approval to contract or assign. First actions are confirmation of live status, seller/agent authority, written contract/assignment terms, access, title/occupancy, and condition. Each preliminary public-data ARV remains non-final; no rehab, MAO, or offer anchor was calculated.

## Explicit exclusions

- REO/foreclosure/bank-owned/auction: **027, 034, 049, 052, 059, 064, 070, 071, 079**.
- Generic non-property source rows: **006, 008, 009, 010**.
- No identifiable subject: **062, 096**.

## Generated files

- `cleveland_wholesale_action_queue.csv` — 25 action rows.
- `cleveland_wholesale_screening_holds.csv` — 9 non-operational holds.
- `cleveland_wholesale_reference_no_pursuit.csv` — 47 non-operational records.
- `cleveland_wholesale_reo_auction_exclusions.csv` — 9 excluded records.
- `cleveland_source_exceptions.csv` — 6 raw-source exception records.
- `cleveland_full_source_triage.csv` — the 96-row raw-source audit.
