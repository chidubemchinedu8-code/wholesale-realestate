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

Rows **1–21** are documented. None received an ARV because every reviewed lead was pending/sold/off market, lacked essential identifying facts, violated a hard rule, or had unverifiable current data. Rows 22–96 remain queued in order.
