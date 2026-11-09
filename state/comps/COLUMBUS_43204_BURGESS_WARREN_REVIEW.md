# Columbus follow-up — 2026-11-08

## 176 S Burgess Ave — PRICED estimate

1210sf; ask $64,900; Central Hilltop. Saved pool:
`columbus_43204_2bd_comps.csv`. This is an **at-least-two-bed** pool,
not five exact two-bedroom sales. The rule permits higher bed counts.
Median $151.571856/sf; ARV $183,402; MOD allowance $42,350;
buyer max $86,031; seller MAO $76,031; margin to ask $11,131;
indicative offer $58,521–$67,691. Walkthrough must confirm repair scope.

Explicit radius expansion: 0.25mi has three; 0.50mi has five. Spread 2.5%.
No backtested local error band; these are not precise appraised values.
Engine rerun via import with `MIN_COMPS=5` in memory (D-56), no production change.
Sheet identity verified by address: row 10, not the stale row 25 in prior notes.
Formula median lives in T4; T2 is unchanged. No blanket reuse for other leads.

## 691 S Warren Ave — UNPRICED

Gutted subject, 1288sf; ask $102,500. Requires HEAVY scope if eventually priced.
South Central Hilltop feed:
https://www.redfin.com/neighborhood/151053/OH/Columbus/South-Central-Hilltop/filter/include=sold-6mo

Four verified renovated closed sales saved in
`columbus_43204_scentralhilltop_comps.csv`: 704 S Ogden, 610 S Terrace,
511 S Wayne, 799 S Wayne. The 912sf Wayne comp is INSIDE ±30% of 1288sf
(901.6–1674.4), not outside. Four is insufficient: no ARV submitted.
554 S Ogden is unknown: roof/electrical work alone does not establish finished interiors.
564 S Wayne is in overlapping neighbourhood feeds; resolve hood before using it.
716 S Ogden is ACTIVE at $170,000, not a closed comp. 651 S Terrace sold
April 17, outside the 180-day window. 774 Racine has potential/dated copy.
954 Clarendon is a renovated ranch but not added merely to force five;
its exact submarket comparability still requires review.

Opened evidence:
- https://www.redfin.com/OH/Columbus/704-S-Ogden-Ave-43204/home/75594291
- https://www.redfin.com/OH/Columbus/610-S-Terrace-Ave-43204/home/79549307
- https://www.redfin.com/OH/Columbus/511-S-Wayne-Ave-43204/home/79544544
- https://www.redfin.com/OH/Columbus/799-S-Wayne-Ave-43204/home/79566642
- https://www.redfin.com/OH/Columbus/554-S-Ogden-Ave-43204/home/79528412
- https://www.redfin.com/OH/Columbus/716-S-Ogden-Ave-43204/home/75594292

Discard all prior scratch Warren calculations: active-sale contamination,
mis-copied coordinates and tuple-index arithmetic made them invalid.
Sheet row 6 remains UNPRICED; no Warren dollar outputs written.

Updated sweep counts: 2 PRICED, 1 MAYBE, 5 UNPRICED, 22 CANDIDATE,
23 REJECT, 2 SEPARATE (55). This is still a partial ZIP scan.
