# Evidence, group C: rows 6 and 7, and two Failures entries

All paths are on private commit `60b819bd` unless a path is marked "local only". The outline is
`submission/READABLE_SURFACE_BUDGET_OUTLINE.md@40f0e4211`. (This audit checked that version; its WORDING_FLAGS were accepted by Chris and applied in outline cf541ce98, 2026-10-20.) Input files are listed with their sha256 values in
`docs/manifest_C.json`. Run each script from the package root with `python reproduce/<name>.py`. Each exits 0 only
when every expected number matches.

## snap3arm: REFINE-24 / MIDLINE / SHEETLINE (outline row 6)

- **Preregs:** `standalone/preregs/snapping_refine.md` (REFINE-24), `standalone/preregs/snapping_midline.md`
  (h0 3-arm page, amendment 1: 14 crosses) and `standalone/preregs/snapping_sheetline.md` (h2 3-arm page, amendments 1-2).
- **Item / verdict:** none. This is a pre-loop test, so there is no Judge verdict. The results are in
  `[private path]` §8 (lines 177-221). The saved counts are
  `[private path]` and `midline3arm_result_h2_sheet.json`.
- **Label:** inconclusive, one rater (Sebastien). No arm beats w00 (better = p < 0.05 and more Yes).
- **Rule:** port of `[private path]` `score()`. It uses first showings only and pairs Yes/No
  answers per cross. The exact McNemar p is the two-sided binomial on the discordant pairs.
- **Expected numbers and their sources, all MATCH:**
  - h0: w00 11/14 (§8:186), REFINE-24 9/14 (:187), MIDLINE 8/14 (:188).
  - h0 McNemar: MIDLINE vs w00, 0 better / 3 worse, p 0.25 (:190); REFINE-24 vs w00, 0 / 2, p 0.5 (:190).
  - h0 repeats agreed 4/4 (:182).
  - h2: w00 9/15 (:214), REFINE-24 6/15 (:215), SHEETLINE 6/15 (:216).
  - h2 McNemar: SHEETLINE vs w00, 1 / 4, p 0.375 (:218); REFINE-24 vs w00, 1 / 4, p 0.375 (saved JSON).
  - h2 repeats agreed 4/4 (:209-210).
  - The outline's "p 0.25-0.5" is the range over these four comparisons with w00.
  - Row 5's "20/29" equals 11/14 + 9/15 and reproduces from the same files.
- **Status: MATCH.**
- **Note:** the h2 result JSON's `prereg` field names `midline3arm.md`. The h2 page is governed by `sheetline3arm.md`,
  which reuses the midline3arm design.

## phasesym: PHASE-SYM-ROW7 (outline row 7)

- **Prereg:** `standalone/preregs/reader_phase.md`.
- **Item:** `[private path]`. The Verdict starts at line 209, and
  the Result lines are 204-206.
- **Checks:** `[private path]` (`psym_result.json`,
  `judge_rescore.py/.json`).
- **Label:** PASS = PHASE-DEPENDENT. R2 is the headline and R is reported. The sub-answer is T-PHASE-MATERIAL on both.
- **Expected numbers and their sources, all MATCH within 0.0015:**
  - R2 over 256 pairs: median 0.426, range 0.268-0.625, PHASE-DEPENDENT (item:204). 253 of the 256 pairs are
    READER-LIMITED (item:211).
  - R2 phase effects: T-phase 0.176, H9-phase 0.175 (item:204).
  - R: median 0.588, range 0.452-0.827, PHASE-DEPENDENT; T-phase effect 0.149, H9-phase effect 0.215 (item:205).
  - The earlier 0.508 (item:53, :82) is read from `sorstrip_stage0a.json` (derived). Caveat (item:223,
    SAVED-NOT-REPRODUCED): 0.508 rests on a saved T map that the current venv no longer reproduces; the current-venv
    equivalent is 0.524 (or 0.533 at T (0, 0) / H9 (40, 40)). Row 7 quotes 0.508, so the caveat should travel with it.
  - Recomputing from the 3-decimal pair table gives 0.1755 for R2's H9 effect and 0.1495 for R's T effect, a +0.0005
    rounding difference.
- **Status: MATCH for everything derived from the saved 16 × 16 pair table.** The per-pair ratios themselves (the
  windowed band-pass correlations) are **NOT REPRODUCIBLE** here, because they need the 2.4 µm / 9.6 µm ink PNG maps and
  `team_ink.tif`, which are images. The Judge's independent window-level re-score of 5 pairs (`judge_rescore.json`,
  derived) equals the job at all 5. The script prints that comparison.
- **Cosmetic:** the outline writes 0.625 as "0.62" but 0.215 as "0.22". Rounding half-up gives 0.63 and 0.22. The
  outline's 0.62 copies the job's own `row7_wording`.

## copyfix9: COPY-FIX-9 + KEY2-STEP2 (Failures: "A coached first hand fix did not reach the marked sheet")

- **Preregs:** `standalone/preregs/handfix.md` and `standalone/preregs/handfix_key2.md`.
  - The brief named `2026-10-08_partner_copyfix.md` for KEY2-STEP2. That file is the partner's COPYFIX TTA test, not
    KEY2-STEP2. The KEY2-STEP2 verdict cites `seb_key2step2.md`.
- **Items:**
  - `[private path]`: Verdict at line 372, label FAIL = KILL
    (marks-only branch).
  - `[private path]`: Verdict at line 202, label FAIL =
    KEY-LIMITED.
- **Inputs:** Chris's 2.4 µm marks from both sessions, his two read pages and both keys. All are "local only"
  (git-ignored).
  - No sha256 of these inputs was recorded in any Judge or stage-0 output, so there is nothing to cross-check.
  - All the tests that scored against these marks are closed: FIELD-R, OVL-MARKS, KEY-FAR-24 and K-COUNT-9 (killed).
- **Expected numbers and their sources** (IC = COPY-FIX-9 item, IK = KEY2-STEP2 item):
  - Step 1 = STEP 2: COPY OFF (marks-only); R 14/24 (IC:388).
  - Step 2 = KILL: F 17/24 vs control 23/24, F read as rows, guard "strokes" (IC:376, 388).
  - Two sites from INCONCLUSIVE (IC:389-391).
  - F / C on-count at 50 / 75 / 100 µm: 13 / 17 / 20 vs 20 / 23 / 24 (IC:392).
  - Straight guide within 75 µm of the mark at 22/24 (IC:397).
  - Own start (OVL_inset) 16/24; paired, 4 sites gained and 3 lost (IC:404).
  - Second session: F 16/23 vs C 19/23 = MIDDLE (IK:213). R 14/23, two-key KILL (IK:218). F two-key = KEY-LIMITED
    (IK:206). F's on/off is the same under both keys at 16/23 (IK:215).
  - Minutes: 89.2 by the sheet rule, 80-84 by his own reading (IC:366, 408). These come from the saved timestamps
    12:58:49 / 13:08 / 14:28:03 / 14:32 in `timed/SESSION_TIMES.md`.
- **Status: MATCH (23/23).** The re-score is also identical to the Runner's saved `copyfix_result.json`.

## lasagnafit9: LASAGNA-FIT-9 (Failures: "The organizers' lasagna multi-winding fit with zero corrections did not hold our sheet")

- **Prereg:** `standalone/preregs/lasagna_fit.md`.
- **Item:** `[private path]`, Verdict section.
- **Checks:** `[private path]`
  and `runner_job2_drift.json`.
- **Label:** KILL, entered as FAIL (written coverage rule; the coded gate was defective).
- **Inputs:**
  - `main/fit.log` and the exported `winding_0000` x/y/z grid are local only. The grid was converted from `.tif` to JSON
    once; the source tif sha256 values are stored inside that file.
  - `umbilicus.json` (the clicked axis).
- **Expected numbers and their sources** (all from the item's Verdict findings 1 and 4):
  - Stopped at 2459/10000 by `rel_improvement_100 < 1e-4`: MATCH.
  - Nearest exported vertex 369.3 vx = 3.46 mm from its own seed: MATCH (recomputed from the grid).
  - 11.5-12.7 windings inward along the seed's ray: MATCH. The outline's "roughly 10-12" follows the Judge's own
    instruction for outside wording. Non-blocking wording note: the measured top end (12.7) is above 12; the Judge's
    proposed BRIEF line says "~12".
  - Seed-patch share within one pitch 0.0456 (Judge 0.046) vs the coded gate's 1.0, so KILL by the written rule: MATCH.
  - "Within 28 vx through stage 2": 28.1 at the end of stage 2 (derived from `runner_job2_drift.json`, which needs the
    torch snapshots): MATCH. Wording caveat: the first three snapshots read 34.7 / 33.9 / 33.9 vx. The value is ≤ 28.1
    only from the `model_stage1_000200` snapshot on. Non-blocking.
  - Self-snap loss (`smap`) 4.8e3 → 486.5 in stage 3: MATCH.
  - **Seed-anchor loss (`station_t`) "0.0009 → 19.5": MISMATCH at the start value.**
    - The log's progress table is fixed-width. On the `stage3 0/...` row the it/s field is blank, so a whitespace split
      shifts every value one column left.
    - Aligned to the header, `station_t` is **0.0000** at the start of stage 3 and **19.458** at step 2459. The 9.0e-04
      belongs to the next column (the `step` term).
    - Parser-independent check: the `stage3 1/...` row has its it/s value (5.1), and a plain whitespace split of that row
      already gives `station_t` 0.0000 and `step` 9.0e-04. The script prints this check.
    - The anchor is re-set at each stage start. The log shows the anchor 37.4 vx from the seed when stage 3 began, and
      `station_t` was already 7.17 at the end of stage 2.
    - The mechanism sentence still holds (the anchor loss rose while self-snap fell). Suggested wording: "the
      seed-anchor loss rose from 0 to 19.5 (re-set at the stage start)".
- **Status: MISMATCH (1 number). Everything else MATCH. The script exits 1 by design.**
