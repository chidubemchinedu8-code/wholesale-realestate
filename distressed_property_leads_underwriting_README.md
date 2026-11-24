# Distressed Property Leads — Sequential Underwriting Tracker

**Input:** `distressed_property_leads_master.csv` (96 leads, supplied by the user)  
**Working tracker:** `distressed_property_leads_underwriting_tracker.csv`

## Workflow

Leads are processed strictly in CSV order. A lead is considered **complete** only after one of these outcomes is documented in the tracker:

1. **Eligibility/status screen:** it is sold, pending, off market, an auction/REO, violates a stated property/price/condition rule, or cannot be identified from public facts.
2. **Full underwriting:** if it is a currently active and eligible listing, the tracker will include three to five validated renovated, closed comparable sales from the prior six months, ARV, repair scope, MAO, initial anchor, agent information, and a listing-specific negotiation point.

No ARV is inserted where a compliant 3–5 renovated-sale comp set or a verified current listing is absent. This avoids treating stale search snippets or noncomparable sales as an ARV.

## Formulas for eligible active leads

- **ARV:** average validated renovated comp $/sf × verified subject sq ft.
- **Rehab:** light $15–$25/sf; medium $30–$40/sf; heavy/full gut $45–$65+/sf.
- **MAO:** `(ARV × 70%) − rehab − $10,000 assignment fee`.
- **Initial anchor:** `MAO × 85%`.

## Current progress

Rows **1–22** are documented. Lead 001 was re-underwritten with a preliminary $130,000–$145,000 ARV (working midpoint $137,500), subject to a material 1,086-sf versus 1,794-sf public-record conflict. Lead 002 was re-underwritten with a preliminary $190,000–$210,000 ARV (working midpoint $200,000). Lead 003 was re-underwritten with a preliminary $195,000–$220,000 ARV (working midpoint $207,500); its renovated support is primarily current asks, so confidence is low. Lead 004 was re-underwritten with a preliminary $140,000–$155,000 ARV (working midpoint $147,500), contingent on confirming public-record GLA and contradictory listing status. Lead 005 was re-underwritten with a preliminary $200,000–$220,000 ARV (working midpoint $210,000); it had already closed, so it is retained solely as a retrospective market record. Lead 022 has a preliminary $125,000–$135,000 ARV screen (working midpoint $130,000). The remaining earlier status/eligibility screens will be revisited in sequence for address-level preliminary ARVs where the address is identifiable; status and filter fit are kept separate from valuation. Rows 23–96 remain queued after that catch-up sequence.
