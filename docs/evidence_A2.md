# Evidence, group A2: FULL-HOP-W, TOL-814, LINE-FIELD-READ, SPIRAL-READ-0841

All paths below are on private commit `60b819bd` unless marked "local only". The outline is
`submission/READABLE_SURFACE_BUDGET_OUTLINE.md` at 40f0e4211. (This audit checked that version; its WORDING_FLAGS were accepted by Chris and applied in outline cf541ce98, 2026-10-20.) The data files and their sha256 are listed in
`docs/manifest_A2.json`. Run a script with `python reproduce/<name>.py` (exit 0 = every number matches).

## FULL-HOP-W (`reproduce/fullhop.py`): MATCH

- **Outline:** "Failures and limits", bullet "~30 % on the wrong sheet still reads holds only for damage less than one
  sheet deep". This is also the "Correction to row 2".
- **Prereg:** `standalone/preregs/fullhop_w.md` (outcome rule L103-110; Stage 0b bar L76).
- **Item:** `[private path]`. Verdict L183-231.
- **Judge:** `[private path]` + `_out.txt` / `_out.json`.
- **Verdict:** FAIL = FULL-HOP-FAILS. Both raters valid (item L187).
- **Numbers checked:**
  - C70d: not rows for both raters (L199).
  - L70d: rows for Sebastien, strokes for Chris (L198).
  - L40d guard (60 % full hops): not rows for both (L200).
  - H50n (50 % holes): rows for both (L201).
  - Control L100: rows for both (L202).
  - Blanks: 3 of 3 rejected by each rater (L203).
  - Calibration: rows for both (L204).
  - The ratings sha256 match the Judge's (fc6cf6ff…, 998355af…).
  - Stage 0b, L70d: hop AUC 0.5755, bar 0.5756, margin **0.0001** (L207). The bar is recomputed as
    min(blank + 0.05, 0.62) = 0.5756.
  - Stage 0b, C70d: hop AUC 0.611, bar 0.614 (L207).
  - Floor 140 µm and far end 250 µm (`f140/surf.json`; L128).
- **Not recomputed:** the Stage 0b AUCs. They come from GPU ink maps, so they are re-read from the saved
  `fh_s0b_f140_result.json` (local only).
- **Wording note (do not change the script, flag only):**
  - The outline says "every damaged patch moved a full sheet (140-250 µm)". 140-250 µm is the hop law's floor and
    far end.
  - The measured L70d moves are p10 129 / p50 164 / p90 218 µm. About 10 % of L70d's moved vertices moved ≤ 130 µm
    (`f140/surf.json`; item L131).
  - Suggest "moved onto the neighbouring sheet by a 140-250 µm hop law (median ~164 µm)" or similar.
  - The Judge's own wording says the same thing (L215: "140-250 µm").

## TOL-814 (`reproduce/tol814.py`): MATCH

- **Outline:** the FULL-HOP-W bullet, sub-bullet "Second patch (TOL-814 ...)".
- **Prereg:** `standalone/preregs/fullhop_s022814.md` (outcome rule L108-116).
- **Item:** `[private path]`. Verdict L193-266.
- **Judge:** `[private path]` + `_out.json`.
- **Verdict:** FAIL = FAILS-814. 2 raters valid, ctrl814 rows for both (L197).
- **Numbers checked:**
  - Rows counts out of 2: ctrl 2, L85 2, L70 1, L55 1, H50 2 (L214-218; Judge `rows_count_of_2`).
  - Crossed calls: Chris called L70 strokes and L55 rows; Sebastien the reverse (L216-217, L223).
  - Blanks: 3 of 3 rejected by each rater.
  - The ratings sha12 match the Judge's (eeeae260532b, bf1847150a03).
  - Moved shares (> 50 µm, vertices): **0.165 / 0.322 / 0.476** (L233; `f170/surf.json`). These are vertex shares.
    The pixel shares (0.161 / 0.320 / 0.475) are different numbers; the outline correctly uses the vertex shares.
  - Median move ~200 µm (p50 198.2 / 199.7 / 200.0).
  - Floor 170 µm, constant 200 µm (L162).
  - Floor 140 failed: hop AUC 0.577 against a bar of 0.559 (L232).
  - Floor 170 passed: hop AUC 0.503, blank 0.495, bar 0.545 (L229).
- **Rounding:** the saved values have 4 decimals. The script rounds them half-up, as the verdict text does: 0.4945 →
  0.495. Python's float `round` gives 0.494.
- **Not recomputed:** the surfaces are 4.5 GB each and the AUCs need GPU maps. The script re-reads the saved stage
  outputs (local only).
- **Wording note:**
  - The outline says "hops had to be at least 170 µm". That is the law floor. The measured p10 of the moved vertices
    is 110 / 131 / 146 µm.
  - Same remark as for FULL-HOP-W: "a 170 µm floor law (median ~200 µm)" is exact.

## LINE-FIELD-READ (`reproduce/linefieldread.py`): MATCH (page black-share check not reproduced)

- **Outline:** section "Line spacing check with perfect lines".
- **Prereg:** `standalone/preregs/line_spacing.md` (arms L51-52; F3/F4 rule L129-140; wording + minutes L141-152).
- **Item:** `[private path]`. Verdict L355-479.
- **Judge:** `[private path]` + `_out.json`.
- **Verdict:** PASS = O2-READS; secondary arm O45-FAILS (O45-SPLIT) (L359).
- **Numbers checked against the ratings:**
  - O2: rows for both raters (L401).
  - O45: rows for Sebastien, strokes for Chris (L402).
  - Guard: only Sebastien rejected one, L55_814 (L404, L409-410).
  - H50_814: rows for both.
  - Chris called both L70_814 and O45 strokes (L411).
  - The page held 11 pictures (L383).
  - O2 and O45 were not adjacent on the page (L393).
- **Numbers recomputed with the arithmetic of `checks/.../ideas_forecast_odds.py`:**
  - Line count: 10 lines.
  - Spacing: 2.02 mm (O2) and 4.54 mm (O45), computed as (106 − 9) × 0.18732 / (n − 1).
  - Mean line length 11.8 mm and region area 2.1018 cm².
  - Forecast: **8.5-10.8 min/cm²** (O2) and 4.2-5.4 min/cm² (O45), computed as n × L / pace / A. The paces are
    FIBER-9B 6.623 mm/min (`fiber9b_speed.json`) and the clicked-span paces 5.22 / 6.17 mm/min. The clicked-span
    paces are hard-coded in `ideas_forecast_odds.py` L10 and come from BRIEF S8b (item L134).
  - The forecast source is item L36-38 and `ideas_forecast_odds_out.json`.
- **Re-read from a saved file:** O2's median distance from s022814 is **33 µm** (`field_O_result.json`, LINES-READ-814W
  folder, local only; item L125, L418).
- **NOT REPRODUCIBLE here:**
  - The Judge's black-share check of the JPEGs embedded in the page needs the 666 KB image page. That page is not
    carried because the package holds no images.
  - The saved result is `worst_gap_pts_vs_O` 0.1 (`judge_rescore_out.json`). The outline does not quote this number.
- **Note:**
  - The outline's "4.54 mm apart" for O45 is the builder's ring spacing along the grid. Stage 0 measured a mean
    z-spacing of 4.054 mm for the same 5 rings (`stage0.json` a0_ring). These are two different measures; both are
    in the saved files.
  - The outline's REAL-LINES-814 sentence ("7 of 9 lines ...") was outside this group's tests and was not checked.

## SPIRAL-READ-0841 (`reproduce/spiralread0841.py`): MATCH (pixel key-check not reproduced)

- **Outline:** "Failures and limits", bullet "One spiral-fit winding from one anchor point ...". The exposure counts
  also appear in the "Known-window ceiling" section.
- **Prereg:** `standalone/preregs/spiral_field.md` (classes and outcomes L108-126) and
  `standalone/preregs/spiral_field_amend3.md` (Sebastien: no guard; VALID only if he rejects every empty picture).
- **Item:** `[private path]`. Verdict L290-368.
- **Judge:** `[private path]` + `_out.json`.
- **Verdict:** FAIL = SPIRAL-NO-ROWS (one rater: Chris) (L296).
- **Numbers checked:**
  - Both raters VALID (L313-314).
  - Chris: strokes on A1 and A2. Sebastien: rows on A1 and A2 (L316).
  - Control: rows for both.
  - Empty pictures called rows: 0 of 4 for each rater.
  - Chris's guard: not rows.
  - Sebastien's page: no guard.
  - Pages: 9 pictures (Chris) and 8 pictures (Sebastien).
  - Both ratings were given after the page build time.
  - Sebastien's ratings sha begins 9085638c (L424).
  - Control exposure before this test (`planner_exposure_out.json`, `stage0.json`):
    - Chris saw it 6 times byte-identical, plus 2 re-framed.
    - Sebastien saw it once, plus 2 re-framed.
- **NOT REPRODUCIBLE here:** the Judge's pixel key-check, which matched every page JPEG to its tile, needs the
  pictures. The saved result is 9/9 and 8/8 slots matched (`judge_rescore_out.json`).
- **Ratings files:** they live in the test's work folder, not in `ratings/`. Chris's file sha256 is 35d6ce58…; it is
  not recorded in the item.

## Cautions for release

- `spiralread_key.json` holds the sha256 of every tile, including Chris's guard picture. That guard was a W picture
  he had already called not rows. Check that no live test still uses that picture as a guard before release.
- `fh_page_key.json` names H50n. Parked COLS-READ planned to use H50n as its guard, and the Judge called that guard
  burned (item 25 L210).
- Every ratings file and key in `data/` is local only (git-ignored in the team repo).
