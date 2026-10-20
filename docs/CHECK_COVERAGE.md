# Check coverage: which README numbers the scripts recompute, re-read or do not check (2026-10-18)

One row per number (or per group of numbers from one sentence with the same status) in the README's findings sections:
"Read this first", the Findings table, "Failures and limits" and "Line spacing check". Verdict dates, commit ids,
prereg file names and setup facts (window size, model names, who rated when the README says "dropped") are left out.

**Labels**
- **RECOMPUTED**: the script derives the number from the shipped keys, rating files or marks (or, where named, from a
  shipped mesh / line export) and asserts it.
- **RE-READ**: the number comes from a saved output (GPU run, mesh run, Judge output, log) that the script reads and
  asserts, but cannot recompute without data this repo does not carry. Arithmetic on re-read values (a margin, a bar,
  a ratio, a rounding) is still RE-READ. A change to the saved file is caught; an error in how it was made is not.
- **RECOMPUTED from RE-READ rows**: statistics recomputed here from per-item values that were themselves re-read.
- **NOT CHECKED**: no script checks it.
- **FLAG n**: the script checks a different value than the README prints; see `docs/WORDING_FLAGS.md` item n.

`python reproduce/run_all.py` (2026-10-20): 18/18 MATCH (flags 1 and 4 applied in outline cf541ce98; until then `lasagnafit9` failed on purpose).

## Read this first: the known-window ceiling

| Number (README) | Test / script | Status |
|---|---|---|
| Chris saw W's control 6 times, Sebastien once (+2 re-framed each) | SPIRAL-READ-0841 / `spiralread0841.py` | RE-READ (`planner_exposure_out.json` totals; `stage0.json` guard_counts agrees for Chris) |
| never-exposed rater's files (10-14) never opened | process fact | NOT CHECKED |
| Sebastien rows on 19 of 20 surface pictures (HUMAN-TOL + CM2-READ) | `cm2read.py` | RECOMPUTED (HUMAN-TOL 8 + CM2-READ 12 level pictures, counted from both keys). FLAG 8: 20 showings of 19 different pictures (CM2-READ ctrl = HUMAN-TOL L100) |
| every 50 % holes picture after HUMAN-TOL called rows by >= 1 rater | `nodefill.py`, `fullhop.py`, `tol814.py`, `rawread9h.py` | RECOMPUTED (see row 2 below) |
| RAW-READ-9H GROWER-READS (two raters) | `rawread9h.py` | RECOMPUTED (key + both ratings; Chris rated after his COPY-FIX-9 read and INSET-NEG pages, stamps asserted) |
| row score 0.017 of the control's | `rawread9h.py` | RE-READ (`judge_rp_out_60b819bd.json` RP 0.399 / 23.338; ratio formed here) |
| agents rows 0 of 5 (control 5 of 5) | `rawread9h.py` | RECOMPUTED (recounted from the per-reader rows of `r9_screen_result.json`) |

## Findings table

| Row | Number (README) | Test / script | Status |
|---|---|---|---|
| 1 | (struck row: ~20 mm field, 10-14 mm tiles) | dropped | NOT CHECKED (dropped as written) |
| 2 | L70 / C70 (~30 % displaced) rows for both; HUMAN-TOL-SCORE branches; H70 split; H50 not rows for both | HUMAN-TOL-SCORE / `humantol.py` | RECOMPUTED (key + both ratings, sha-pinned; answer set and vocabulary asserted) |
| 2 | C70 at a -22-layer offset, about -53 µm | `humantol.py` | RE-READ offset (`tol20b_tiles.json`); µm = -22 x 48.1 / 20 computed here |
| 2 | Sebastien 10-03, Chris 10-06 | `humantol.py` | RECOMPUTED (rating-file `when` stamps, CDT) |
| 2 | Chris rejected the same H50 again on 10-08 (RAW-READ-9H guard) | `rawread9h.py` | RECOMPUTED (guard call); guard = HUMAN-TOL H50 by sha256 RE-READ (`tile_hashes.json`, PNGs not shipped) |
| 2 | both called H50 rows on 10-10 (NODE-FILL-REREAD, VOID) | `nodefill.py` | RECOMPUTED (validity, guard calls, dates); guard file = H50 by md5 pin (prereg L14) RE-READ from `tile_hashes.json` |
| 2 | NODE-FILL-READ fresh 50 % holes: 1 of 2, VOID | `nodefill.py` | RECOMPUTED |
| 2 | FULL-HOP-W H50n rows for both; TOL-814 H50_814 rows for both | `fullhop.py`, `tol814.py` | RECOMPUTED |
| 3 | CM2-READ WIDE-OUT, both raters, ">= 24 µm on both sides" | `cm2read.py` | RECOMPUTED (incl. INCOMPLETE / uncountable / unit10 branches; none fires) |
| 3 | s214732 rows for both | `cm2read.py` | RECOMPUTED |
| 3 | s214732 "~66 µm inward" | (another item's check) | NOT CHECKED |
| 3 | FRESH-WRAP: ±24 µm rows (CONFIRMED, two raters, never-seen text) | `freshwrap.py` | RECOMPUTED (fw.py rater()/combine() ported; equal to the saved scorer result; ratings sha-pinned at build) |
| 3 | +48 µm Chris strokes, -48 µm rows; Sebastien both rows; the only fresh depth picture called not rows | `freshwrap.py` | RECOMPUTED |
| 3 | 62-layer (~149 µm) slab | | NOT CHECKED |
| 3 | r 0.85-0.87 (±48 µm: 0.69) | `freshwrap.py` | RE-READ (`judge_rescore_60b819bd.json`; needs the ink maps) |
| 4 | (struck row: ~300 vs ~118 clicks/cm²) | dropped | NOT CHECKED (dropped) |
| 5 | 187 µm grid | `w00native.py` | RECOMPUTED (from `mesh_N94_meta.json`) |
| 5 | affine residual 14 µm (twice in row 5) | | NOT CHECKED (needs both full meshes; quoted from the prereg, 13.9 µm) |
| 5 | TRUSTED-P: 46 crosses, not on one sheet at 33 (clean 7/15, middle 12/16, suspect 14/15); calibration gate failed | `trustedp.py` | RECOMPUTED (key + ratings; gate fit balanced accuracy 0.696 < 0.80) |
| 5 | fresh h0/h2: w00 stayed on the sheet at 20/29 | `snap3arm.py` | RECOMPUTED |
| 5 | W00-NATIVE median 0.10 (copy and native); ±75 µm -> 0.11 / 0.13; Spearman 0.33; verdict G | `w00native.py` | RECOMPUTED from RE-READ rows (per-cross A25, `w00native_rows.csv`; A25 needs the CT) |
| 5 | 42/82 (0.51, CI 0.40-0.62) | `w00auditfresh.py` | RECOMPUTED from RE-READ rows (per-station `abs_um`, `wa_result.json`). FLAG 10: station-level CI; the prereg decision used the strip bootstrap (upper 0.637, asserted) |
| 5 | 10 fresh along strips, 7 bend / 3 flat, + 6 cross strips | `w00auditfresh.py` | RECOMPUTED (strip counts from the rows) |
| 5 | "within 4.5 mm of a shared w00 start" | | NOT CHECKED |
| 5 | replication 18/40 | `w00auditfresh.py` | RECOMPUTED from RE-READ rows (strip bootstrap upper 0.667 asserted) |
| 5 | 20 of 40 misses 75-150 µm; <= 0.57 at e <= 0.10; 16 of 22 replication misses > 150 µm | `w00auditfresh.py` | RECOMPUTED from RE-READ rows |
| 5 | sheet spacing 130-170 µm | | NOT CHECKED |
| 5 | bend 5/28 vs flat 14/18 (46 stations) | `w00auditfresh.py` | RECOMPUTED from RE-READ rows |
| 5 | MARK-2R: 25 sites, 18/20 within 75 µm, median 14 µm, 19/21 and 15/22, straight extension 23/25 | `mark2r.py` | RECOMPUTED (key + both raters' marks) |
| 5 | Chris repeats 0 of 2 (138 / 244 µm); Sebastien's repeat reliability unmeasured | `mark2r.py` | RECOMPUTED |
| 6 | w00 11/14 vs REFINE-24 9/14, MIDLINE 8/14 (h0); w00 9/15 vs REFINE-24 6/15, SHEETLINE 6/15 (h2); McNemar p 0.25-0.5 | `snap3arm.py` | RECOMPUTED |
| 7 | R2 0.27-0.62 (median 0.43) over 16 x 16 pairs; R 0.45-0.83 (median 0.59); own-phase effects 0.18 / 0.15 vs 0.18 / 0.22 | `phasesym.py` | RECOMPUTED (summaries) from RE-READ rows (256-pair table, `psym_result.json`; per-pair ratios need the PNG maps); the Judge's 5 re-scored pairs equal the table (asserted). FLAG 7: 0.625 is written 0.62 (half-up 0.63) |
| 7 | "the earlier 0.508" | `phasesym.py` | RE-READ and SAVED-NOT-REPRODUCED (`sorstrip_stage0a.json`; the current venv re-run gives 0.524). FLAG 6 |
| 8 | agents vs Sebastien disagree on 5/18; Sebastien and Chris agree 16/18 (κ 0.77); every disagreement = human rows, agents not; HUMANS-NOISY | `humanfloor.py` | RECOMPUTED (both ratings sha-pinned; agent calls from the saved agent result files) |

## Failures and limits

| Number (README) | Test / script | Status |
|---|---|---|
| LASAGNA-FIT-9: stage 3 stopped at 2459 of 10000 steps; `rel_improvement_100 < 1e-4` | `lasagnafit9.py` | RE-READ (parsed from `fit.log`) |
| ended 3.46 mm from the seed | `lasagnafit9.py` | RECOMPUTED (from the exported mesh `winding_0000_xyz.json`) |
| roughly 10-12 windings inward | `lasagnafit9.py` | FLAG 5: the script recomputes 11.5-12.7 from the mesh export + `umbilicus.json` |
| killed by the written coverage rule; coded check said covered | `lasagnafit9.py` | RECOMPUTED from the mesh export (share within one pitch 0.046 < 0.70 is the Judge's reading of step 7; coded gate 1.0) |
| within ~35 voxels of the seed through stage 2 | `lasagnafit9.py` | RE-READ (`runner_job2_drift.json`); max 34.7 vx (FLAG 4, applied) |
| self-snap loss 4.8e3 -> 4.9e2 | `lasagnafit9.py` | RE-READ (`fit.log`) |
| seed-anchor loss 0.0000 after the stage-3 re-set -> 19.5; 7.17 at the end of stage 2 | `lasagnafit9.py` | RE-READ (`fit.log`); 19.458 at the stop (FLAG 1, applied) |
| FULL-HOP-W: 140-250 µm full-sheet moves | `fullhop.py` | RE-READ law parameters (`f140_surf.json`). FLAG 2: measured p10 129 µm, median 164 µm, ~10 % <= 130 µm (asserted as measured) |
| Stage 0b passed by 0.0001 AUC for L70 | `fullhop.py` | RE-READ (`fh_s0b_f140_result.json`, 4-decimal values; the job's own hop_ok flag is asserted too); 0b unmoved gate and 0d DARK-HOPS gate re-applied to re-read values |
| guards: 60 % full hops not rows for both; 50 % holes rows for both | `fullhop.py` | RECOMPUTED |
| clustered not rows for both; dispersed not rows for Chris; control rows; every blank rejected; FULL-HOP-FAILS | `fullhop.py` | RECOMPUTED (ratings sha-pinned) |
| clustered picture at the -22-layer depth where even the control scores lower | | NOT CHECKED (the per-offset AUCs are in `fh_s0b_f140_result.json` but not asserted) |
| TOL-814: hops at least 170 µm | `tol814.py` | RE-READ law floor (`f170_surf.json`). FLAG 2: measured p10 110-146 µm (asserted as measured) |
| median ~200 µm; moved shares 16.5 / 32.2 / 47.6 % | `tol814.py` | RE-READ (`f170_surf.json`) |
| a 140 µm move still showed the true text | `tol814.py` | RE-READ (`t8_s0b_f140_result.json`: 0.577 > bar 0.559; bar rule min(blank + 0.05, 0.70)) |
| ~15 % rows for both; 30 % and 45 % rows for 1 of 2, crossed calls; FAILS-814 | `tol814.py` | RECOMPUTED (equals the scorer's saved verdict, asserted) |
| COPY-FIX-9: 89.2 min (load-included), 80-84 min (own reading) | `copyfix9.py` | RECOMPUTED from hand-transcribed timestamps (`session_times.json`, derived) |
| 17/24 vs 23/24 (KILL); 16/23 vs 19/23 (undecided); KEY-LIMITED; two sites from INCONCLUSIVE | `copyfix9.py` | RECOMPUTED (key + Chris's two mark sessions; the key's mesh crossings are pre-computed in `copyfix_key.json`) |
| its own start scored 16/24 | `copyfix9.py` | RECOMPUTED from marks, with the OVL start's crossings RE-READ (`ovlmarks_result.json`) |
| F read as rows | `copyfix9.py` | RECOMPUTED |
| straight guide alone within 75 µm at 22/24 | `copyfix9.py` | RECOMPUTED |
| SPIRAL-READ-0841: Chris both strokes, Sebastien both rows; SPIRAL-NO-ROWS (one rater) | `spiralread0841.py` | RECOMPUTED (both ratings sha-pinned to the Runner's record; the Judge's pixel key-check is RE-READ: all_match flags asserted) |
| Chris's control rows and guard held; Sebastien rejected all four empty pictures | `spiralread0841.py` | RECOMPUTED |
| control seen 6 times before (once called not rows, FIELD-R) | `spiralread0841.py` | 6: RE-READ (`planner_exposure_out.json`); FIELD-R call NOT CHECKED |
| SPIRAL-ACW-0841 parent claims (strip-scale progress bar; no better than a straight line on bends) | | NOT CHECKED |

## Line spacing check

| Number (README) | Test / script | Status |
|---|---|---|
| 10 lines 2.02 mm apart (O2) | `linefieldread.py` | 10 lines RECOMPUTED (`lines_O.json`); 2.02 mm = builder formula from the ring rows in `rings_O2.json`. FLAG 3 (coordinator's note): the built O2 lines measure 1.80 mm apart (mean z gap 192.4 voxels), same 0.89 ratio as O45 |
| 5 lines 4.54 mm apart (O45) | `linefieldread.py` | 4.54 = builder formula (`rings_O45.json`). FLAG 3: measured 4.054 mm from `lines_O45.json`, equal to `stage0.json` (both asserted) |
| O2-READS; O45-FAILS (O45-SPLIT) | `linefieldread.py` | RECOMPUTED (TOL-814 page key + both ratings, sha-pinned); Stage 0d frame gate RE-READ (`stage0.json`, asserted) |
| REAL-LINES-814: 7 of 9 lines drawn through the start point | | NOT CHECKED |
| forecast floor 8.5-10.8 min per cm² | `linefieldread.py` | RECOMPUTED arithmetic (`lines_O.json` length, `region.json` area, `fiber9b_speed.json` pace). FLAG 9: the 10.8 end uses the clicked-span pace 5.22 mm/min, a constant from ideas_forecast_odds.py, not a shipped file |
| depth best of 7 | | NOT CHECKED |
| median 33 µm from s022814 by construction | `linefieldread.py` | RE-READ (`field_O_result.json`) |
| 11-picture page; 50 % holes guard rows for both; Chris rejected no guard; READS rests on Sebastien's L55_814; Chris L70_814 and O45 strokes | `linefieldread.py` | RECOMPUTED |

## Notes

- **O2 measured 1.80 mm vs 2.02 mm by design** (and O45 4.054 vs 4.54 mm): the built lines sit ~0.89x the builder
  formula's spacing. Both the formula values (README-quoted) and the measured values are asserted.
- **w00auditfresh status per its script header (2026-10-18 14:56):** ON/OFF, the binomial rule, the strip bootstrap, the CI,
  the miss bins, the key-noise bracket and the bend/flat split are recomputed from the per-station `abs_um` rows of
  `wa_result.json`; the rows are cross-checked against Chris's mark files (which stations he marked; can't-tell counts
  14 / 14); his mark positions are tied to the w00 geometry at station 0 (the shared ring) against the Judge's
  station-0 output, and the wa.py sha256 pins are checked. LIMIT stated in the header: w00's trace position at
  stations 1-6 is not in any saved file, so `abs_um` there cannot be recomputed from the marks; a mark change confined to
  stations 1-6 that crosses no 75 µm line is not caught.
- The seven scripts edited by the other agent (w00auditfresh, humanfloor, mark2r, trustedp, w00native, snap3arm, copyfix9)
  were read last, at their 14:54-14:56 versions; their rows above follow those files.
- The key-release questions met while porting are in `docs/WORDING_FLAGS.md`; this file only says what is checked.
