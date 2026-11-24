# Distressed Property Leads — Sequential Underwriting Tracker

**Input:** `distressed_property_leads_master.csv` (96 leads, supplied by the user)  
**Working tracker:** `distressed_property_leads_underwriting_tracker.csv`

## Workflow

Leads are processed strictly in CSV order. A lead is considered **complete** only after one of these outcomes is documented in the tracker:

1. **Eligibility/status screen:** it is sold, pending, off market, an auction/REO, violates a stated property/price/condition rule, or cannot be identified from public facts.
2. **Preliminary retrospective ARV:** for an identifiable historical/off-market row, the tracker will record a clearly labeled public-data range and midpoint, material subject/comp caveats, and a dossier. It is not a final ARV, and it includes no rehab, MAO, or offer anchor.
3. **Full underwriting:** if it is a currently active and eligible listing, the tracker will include three to five validated renovated, closed comparable sales from the prior six months, a final ARV, repair scope, MAO, initial anchor, agent information, and a listing-specific negotiation point.

A final ARV is not inserted where a compliant 3–5 renovated-sale comp set or a verified current listing is absent. Identifiable historical properties instead receive a clearly caveated preliminary public-data ARV; unidentifiable source/category rows receive a documented no-ARV exception.

## Formulas for eligible active leads

- **ARV:** average validated renovated comp $/sf × verified subject sq ft.
- **Rehab:** light $15–$25/sf; medium $30–$40/sf; heavy/full gut $45–$65+/sf.
- **MAO:** `(ARV × 70%) − rehab − $10,000 assignment fee`.
- **Initial anchor:** `MAO × 85%`.

## Current progress

Rows **1–22** are documented. Lead 001 was re-underwritten with a preliminary $130,000–$145,000 ARV (working midpoint $137,500), subject to a material 1,086-sf versus 1,794-sf public-record conflict. Lead 002 was re-underwritten with a preliminary $190,000–$210,000 ARV (working midpoint $200,000). Lead 003 was re-underwritten with a preliminary $195,000–$220,000 ARV (working midpoint $207,500); its renovated support is primarily current asks, so confidence is low. Lead 004 was re-underwritten with a preliminary $140,000–$155,000 ARV (working midpoint $147,500), contingent on confirming public-record GLA and contradictory listing status. Lead 005 was re-underwritten with a preliminary $200,000–$220,000 ARV (working midpoint $210,000); it had already closed, so it is retained solely as a retrospective market record. Lead 007 was re-underwritten with a preliminary $400,000–$440,000 ARV (working midpoint $420,000); it is a closed fire-damaged Lakewood duplex and remains ineligible for a normal wholesale assignment. Lead 011 was re-underwritten with a preliminary $80,000–$100,000 ARV (working midpoint $90,000); its one-bedroom/594-sf configuration has no close current detached-sale set, so confidence is low. Lead 012 was re-underwritten with a preliminary $155,000–$175,000 ARV (working midpoint $165,000); it had already closed and is retained solely as a retrospective market record. Lead 013 was re-underwritten with a preliminary $125,000–$140,000 ARV (working midpoint $132,500), subject to a material public GLA/bed-count conflict. Lead 014 was re-underwritten with a preliminary $150,000–$170,000 ARV (working midpoint $160,000); it had already closed and is retained solely as a retrospective market record. Lead 015 was re-underwritten with a preliminary $135,000–$155,000 ARV (working midpoint $145,000); its base 2-bedroom public record conflicts with later post-sale 3-bedroom rental marketing, so the range remains low-to-moderate confidence. Lead 022 has a preliminary $125,000–$135,000 ARV screen (working midpoint $130,000). The remaining earlier status/eligibility screens will be revisited in sequence for address-level preliminary ARVs where the address is identifiable; status and filter fit are kept separate from valuation. Rows 23–96 remain queued after that catch-up sequence.
