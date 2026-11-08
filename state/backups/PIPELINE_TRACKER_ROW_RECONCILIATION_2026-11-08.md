# PIPELINE TRACKER — row reconciliation after the 2026-11-08 deletion (D-45)

Source of truth: the full sheet text pasted into chat on 2026-11-08. Column A is the `#`
column. Numbers below are **ID values in column A**, never physical row positions.

## The arithmetic closes

| | count |
|---|---|
| Data rows in the pasted sheet | **104** (99 with a numeric ID + 5 with a blank ID) |
| Rows deleted by the D-45 batch | **19** |
| **Pre-edit data rows** | **123** |

The registry held **118 numbered IDs** (1–121 minus the three that never existed:
#100, #105, #117) plus **5 blank-ID rows** = **123**. The two counts agree exactly, so the
deleted set is fully accounted for and nothing is unexplained.

The 5 blank-ID rows, for the record: 12830 Riad St · 11422 Stockwell St · 35 Santa Clara Ave ·
28956 Weber Ave · 4222 Osceola St. All five survive intact; their IDs were always blank.

## What the 19 deleted rows were

**15 were correctly deleted — these were the `Dead` rows:**

`#10` 4824 Cortland · `#11` 5540 Guilford · `#12` 545 Rosedale Ct · `#13` 3021 Carter St ·
`#14` 5310 Grayton St · `#15` 12783 Littlefield · `#16` 11368 Nardin Dr · `#17` 10280 Nardin Dr ·
`#18` 15421 Mapleridge · `#19` 8788 Dexter Ave · `#20` 20475 San Juan Dr · `#26` 3161 W 38th St ·
`#27` 3301 W 32nd St · `#92` 14612 Kingsford Ave · `#99` 15509 Fernway Dr

**4 were live rows destroyed in error:**

| ID | what is known | inferred from the ID slot |
|---|---|---|
| `#25` | **nothing** — never read | sat between `#24` 16772 Ferguson St (Detroit 48235) and `#26` 3161 W 38th St (Cleveland) → a **Cleveland** row |
| `#90` | **nothing** — never read | sat between `#89` 4904 E 109th St (Garfield Hts 44125) and `#91` 15802 Judson Dr (Cleveland 44128) → a **Cleveland-metro 44125/44128** row |
| `#108` | **nothing** — never read | sat between `#107` 17015 Glendale Ave (44128) and `#109` 4072 E 72nd St (44105) → a **Cleveland 44105/44128** row |
| `#121` | **nothing** — never read | after `#120` 16155 Trinity St → followed the Detroit block |

The inferred city/ZIP is a slot deduction from neighbouring IDs, **not recovered data**. The
address, stage, price, ARV, repairs, contact and notes for all four are unknown.

**4 `Dead` rows survived** (their index was never reached): `#21` 4274 Cortland St,
`#96` 3833 E 144th St, `#98` 18033 Marcella Rd, `#107` 17015 Glendale Ave.

## Is anything recoverable?

- `state/backups/PIPELINE_TRACKER_dead_rows_2026-11-08.csv` — holds only the 19 `Dead` rows,
  by design. It does **not** contain `#25/#90/#108/#121`.
- `git log --all` — no commit anywhere in this repository contains those addresses.
- No sweep CSV, ledger, or comps file in `state/` contains them.
- **Conclusion: they are unrecoverable from this workspace.** Only Google Sheets
  File → Version history can restore them.

## What the surviving sheet is now

103 data rows once the 4 stragglers are removed for a clean finish:
`Lead` 72 · `Reached Out` 22 · `Negotiating` 1 · blank 5 · **`Dead` 4**.

Verified against `query_table select B, count(A) group by B`: Dead 4, Lead 72,
Reached Out 22, Negotiating 1 — matches the pasted text.

## Rules carried forward (also logged as D-45)

1. Delete **one row per call**, and re-read the `#` in that row immediately before the call.
2. A falling `grid_properties.row_count` proves *a* row went, never *which* one. The real
   receipt is re-reading column A and diffing against the full ID registry.
3. Back up **every** row before a destructive edit, not just the rows targeted for deletion —
   a backup scoped to the target set cannot detect collateral damage.
