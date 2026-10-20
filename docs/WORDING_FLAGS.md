# Wording flags found while re-scoring (all 16 accepted by Chris on 2026-10-20 and applied)

The README copies the judged outline verbatim. Re-scoring every quoted number from the saved files against outline
40f0e4211 (`python reproduce/run_all.py`: 17/18 MATCH then) found the points below. Chris accepted all 16 on 2026-10-20
(in the authors' private tracker); they are applied, with the proposed words where a flag gave them, in outline
cf541ce98, which the README now copies (`run_all.py`: 18/18 MATCH). The text below is the record of what was found.

## Must fix (a number in the text is wrong)

1. **LASAGNA-FIT-9, "seed-anchor loss rose (0.0009 → 19.5)".** The 0.0009 is the next column of `fit.log`
   (`step`, 9.0e-04): the stage-3 step-0 row has an empty `it/s` field, so a space split shifts every value one
   column left. The step-1 row (it/s filled) shows `station_t` = 0.0000, then 13.4 at step 950, 17.9 at 2000, 19.458
   at the end. Checked by hand in `data/lasagnafit9/fit.log` (header line 113 and the two rows below it).
   **Also (Gemini review, verified in fit.log lines 95-96):** `station_t` was already 7.17 at the end of stage 2; the
   anchor was re-set at the start of stage 3 (seed_dist 37.4 vx), so it restarts at 0.0000. Proposed: "the seed-anchor
   loss rose again (0.0000 after the stage-3 re-set → 19.5; it had reached 7.17 by the end of stage 2)". The mechanism
   sentence still holds.
   `reproduce/lasagnafit9.py` exits 1 on purpose until this is decided.

## Should fix (text is looser than the measurement)

2. **FULL-HOP-W "every damaged patch moved a full sheet (140-250 µm)" and TOL-814 "hops had to be at least 170 µm".**
   These are the hop law's limits, not measured moves: the measured 10th-percentile move is 129 µm on L70d (about
   10 % of moved vertices ≤ 130 µm) and 110-146 µm on s022814 (`docs/evidence_A2.md`). Proposed (Gemini: say the low tail
   too): "by a 140-250 µm hop law (measured median ~164 µm; ~10 % of moved points under 130 µm)" and "by a hop law
   with a 170 µm floor (measured median ~200 µm; 10th percentile 110-146 µm)".
3. **LINE-FIELD-READ "5 lines 4.54 mm apart (O45)".** 4.54 mm is the builder's formula spacing; Stage 0 measured a
   4.054 mm mean z-spacing (both in `data/linefieldread/`). Proposed: "5 lines ~4.5 mm apart by design (4.05 mm
   measured)".
4. **LASAGNA-FIT-9 "stayed within 28 voxels of the seed through stage 2".** The first three snapshots read 34.7,
   33.9, 33.9 vx (`docs/evidence_C.md`). Proposed: "within ~35 voxels".
5. **LASAGNA-FIT-9 "roughly 10-12 windings inward".** Measured 11.5-12.7. Proposed: "roughly 11-13 windings".
6. **PHASE-SYM row 7 "where the earlier 0.508 was found".** The current venv gives 0.524 for it (item line 223);
   add "(0.524 on re-run)" or drop the number.

7. **Row 7 rounding.** R2 max is 0.625 and is written 0.62, while 0.215 in the same sentence is written 0.22.
   Proposed: "0.27-0.63" (half-up, as elsewhere).
8. **Ceiling "19 of 20 surface pictures".** CM2-READ's control is byte-identical to HUMAN-TOL's L100, so these are 20
   showings of 19 different pictures. Proposed: add "(20 showings of 19 pictures)".
9. **Forecast "8.5-10.8 min per cm²".** 8.5 comes from the FIBER-9B pace (6.623 mm/min); 10.8 from the clicked-span pace
   (5.22 mm/min, BRIEF). Proposed: name both paces.
10. **Row 5 "42/82 (0.51, CI 0.40-0.62)".** That is the station-level Clopper-Pearson interval; the prereg's decision
    used the strip-cluster bootstrap (95 % upper 0.637; replication 0.667), and 14 + 14 can't-tell stations were
    excluded. Proposed: keep 0.40-0.62 but add "(stations treated as independent; strip-cluster upper bound 0.64)" and
    the can't-tell counts.
11. **Row 5 repeats.** The README gives Chris's 0/2 but not Sebastien's 1/1 (one pair: still "unmeasured").
12. **Row 8 'Ready?' cell "needs the scripts made portable (relative paths)"** is now stale (done). The column itself
    holds content for the dropped rows, so it stays; only this cell needs new words.
13. **'Who rated' (Status paragraph)** reads as if nobody else rated, until the ceiling section says one never-exposed
    person did (files unopened). Proposed: add "(one never-exposed rater's files from 10-14 were never opened; see the
    ceiling section)".

14. **LINE-FIELD-READ "2.02 mm apart (O2)".** Like O45, 2.02 mm is the builder's grid formula; the saved line points
    (9.366 µm voxels) give a measured mean z gap of ~1.80 mm (same 0.89 ratio as O45's 4.05 / 4.54). Proposed: "10
    lines ~2 mm apart by design (1.80 mm measured)", with flag 3.
15. **LASAGNA-FIT-9 "killed by the prereg's written coverage rule".** Read literally, the prereg's coverage metric
    (share of valid finite vertices in the patch, L44-46) is what the coded gate computed (1.0, "covered"); the KILL
    (0.046) rests on the Judge's reading of "a fit that leaves the patch counts against coverage" (verdict finding 2:
    a vertex counts only within one winding pitch of the seed's radius). Proposed: "killed by the Judge's reading of
    the prereg's coverage rule (a fit that leaves the patch counts against coverage); our coded check measured the
    surface's own grid and said covered".

16. **Row 5 "the mesh grid, not the transfer" (L4-01 critic).** villa #1845 (kadenpool) reads as the opposite slogan
    ("the transform, not the grid") for ink AUC on PHerc0139; no contradiction (different measure), but a judge sees two
    opposite slogans. Proposed: "the transfer does not change the off-papyrus share (a weak measure); #1845 found a
    render-path cost for ink AUC on PHerc0139 that this does not test", and drop the "grid" cause.

## Claims no script checks (say so in the README, or add a check)

- s214732 "~66 µm inward"; the "62-layer (~149 µm) slab"; REAL-LINES-814 "7 of 9 lines"; the SPIRAL-ACW-0841 parent
  claims; the 14 µm affine residual.

## Not reproducible from small files (quoted from the saved Judge outputs; README can say so)

- w00 copy affine residual 14 µm (needs both full meshes; prereg line 15 says 13.9 µm).
- FRESH-WRAP r 0.85-0.87 / 0.69 (needs the ink maps); RAW-READ-9H row score 0.017 (needs the tiles);
  FULL-HOP-W Stage 0b margin 0.0001 AUC (saved GPU output); PHASE-SYM per-pair ratios (re-derived from the saved
  256-pair table only); LINE-FIELD-READ black-share check and SPIRAL-READ pixel key-check (need the images).

## Release questions seen while porting (settled before release: Chris OK'd his files, Sebastien his, and no live test uses a released key)

- Chris's 2.4 µm marks (`kind marks_2p4um`, 5 files) and the W00-AUDIT-FRESH page keys are still NAMED by
  LAY-KEY-9 (dropped 10-17), and by LASPRESNAP-9, KEY-TIEBREAK-9, ONE-END-9 and partner_w00bendpool9 (status not checked;
  `docs/evidence_B.md`). The COPY-FIX-9 marks are used only by closed lane-A items (FIELD-R, OVL-MARKS, KEY-FAR-24, K-COUNT-9);
  lane B not inspected (v7).
- NODE-FILL-READ / -REREAD page keys were never released ("no third viewing").
- SPIRAL-READ key holds the sha256 of Chris's guard tile: confirm no live test reuses that guard.
- The figures (`figures/`) label each picture with its name and both calls: publishing them = releasing the
  HUMAN-TOL, FULL-HOP-W and TOL-814 page keys.
- KEY2-STEP2's prereg is `standalone/preregs/handfix_key2.md` (not the partner copyfix prereg).
