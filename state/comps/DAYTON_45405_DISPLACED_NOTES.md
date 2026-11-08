# 45405 method notes — displaced from DAYTON LEADS on 2026-11-08

While inserting the citywide sweep block below the curated rows, five paragraphs of
45405-specific method notes that occupied column B of rows 42–46 were overwritten by
the divider rows. The text below is the original, recovered verbatim from a read taken
immediately before the overwrite.

They are restored to the DAYTON LEADS tab below the sweep block, and kept here so the
content survives any future edit to that tab.

## 1

13 of 34 rows carry an ARV: 141 S Torrence, 152 & 218 E Parkwood, 45 E Parkwood, 46
Pointview, 127 Iroquois, 127 E Norman, 2326 Parkland, 633 Huffman, 27 Cliff, 104 E
Beechwood, 55 Ashwood, 23 E Parkwood. The 21 blanks are honest and each names its gate:
4 Santa Clara (no renovated cohort in 127 sales), 4 Fairview (pool BUILT, zero renovated
sales in it), 2 Harrison Township (outside the Dayton hood system), 1 hood UNKNOWN
(251 Castlewood — two independent gates), 3 bed-floor failures, 3 multi-unit, 1 REO, 3
with no pool built yet. COVERAGE: 118 listings advertised in 45405 across 2 pages; both
pages read, ~80 cards actually rendered. The remainder is not claimed — Zillow
lazy-loads, so "cards seen" is not "listings reviewed".

## 2

13 of 33 rows carry an ARV: 141 S Torrence, 152 & 218 E Parkwood, 45 E Parkwood, 46
Pointview, 127 Iroquois, 127 E Norman, 2326 Parkland, 633 Huffman, 27 Cliff, 104 E
Beechwood, 55 Ashwood, 23 E Parkwood. The 20 blanks are honest and each names its gate:
4 Santa Clara (no renovated cohort in 127 sales), 4 Fairview (pool BUILT, zero renovated
sales in it), 2 Harrison Township (outside the Dayton hood system), 3 bed-floor failures,
3 multi-unit, 1 REO. COVERAGE: the 45405 ZIP feed is 118 listings across 2 pages; both
pages are now read end to end. Precise x-of-y is not computable from the rendered feed
because Zillow serves ~40 cards per page and lazy-loads the rest — so the honest statement
is 118 advertised, ~80 cards read, and the unread remainder is not claimed.

## 3

Fairview is the SECOND-LARGEST hood in this ZIP and it cannot be priced by this method.
state/comps/dayton_45405_fairview_comps.csv holds every 45405 sale on the hood feed —
five rows, $15–$104/sf — and not one is renovated. The engine refuses, correctly. Re-mine
/fairview-dayton-oh/sold/ periodically: if renovators start trading there the pool becomes
buildable. Do NOT backfill from North Riverdale.

## 4

Every pool is committed and can be produced for any lead on request:
state/comps/dayton_45405_northriverdale_comps.csv (35 rows, 8 verified renovated),
dayton_45405_fairview_comps.csv (5 rows, 0 renovated — refused),
dayton_45403_burkhardt_comps.csv, dayton_45405_santaclara_comps.csv. Hood audit:
state/comps/DAYTON_45405_NEIGHBOURHOOD_CORRECTION.md. Defect history: DEFECT_LOG.md.

## 5

The hood URL /dayton-oh-45405/fairview/ silently redirects to the full 45405 ZIP feed,
which is 118 listings across 2 pages. The priced rows came off that feed and off its
"similar homes" carousels — 104 E Beechwood, 55 Ashwood, 23 E Parkwood, 129 Marathon and
4041 Old Riverside were all surfaced that way. Treat the carousels as a lead source,
never as a comp source.
