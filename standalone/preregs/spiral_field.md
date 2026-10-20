> **Scrubbed public copy** (public name `spiral_field`). The original was first committed to the authors' private repository at `52381edc5` (2026-10-13T03:05:22Z). Later commits to the same file: `a439ffc42` (2026-10-13T03:08:48Z). Timing: Original and amendment both pushed before the first job (its Judge's check). Timestamps live in a private repository; ask the authors for a verification. Scrubbing removed mentions of non-public scrolls and local paths (paths into the authors' private repository read `[private path]` and do not resolve) and replaced internal item ids and test names with public slugs (unmapped internal ids read `[internal item]`); the scientific text is otherwise unchanged.

# Pre-registration: spiral_field. Does SPIRAL-ACW-0841's automatic spiral fit, placed with ONE frozen anchor point, read rows over the whole 20 x 11.7 mm known-text window of PHerc0841 for both blind raters, as the readable control does on the same page?

- **Date and owner:** 2026-10-12 (CDT). Sebastien's side. Written by the Planner station of the lane-A loop (item
  `spiral_field`). Public data only (PHerc0841). Committed and pushed before any render, map, tile, page or
  rating of this test exists. The Planner ran only the scorer self-test, the secrecy check and a counts-only guard-pool check.
- **Parent:** SPIRAL-ACW-0841 (`[private path]`, item `[internal item]`, PASS = GO-READ: post-snap 33/59,
  7/12 strips; flat anchor-depth null 19/59; strip scale only, each strip re-anchored on Chris's first mark). Its Judge named
  this read as the next step.
- **Sebastien's choices:** A on 2026-10-12 21:11 (go ahead; ~1 GPU-h after the test that holds the card; ~4 min of rating
  each). His decision of 21:50 replaces the trap (guard) picture with the per-rater "already rejected" rule below.
- **Design:** the Ideas station's item with the Critic's fixes 4 (exposure counts) and 5 (Stage 0 (f) frame check) binding.
  Deviations have their own section.

## Question

Over the whole S2 window W (w00 SV rows 4511-12831, cols 10392-15269, ~20 × 11.7 mm, FORMAT-20, known rows), does ONE
continuous winding of the saved spiral fit, picked by ONE frozen anchor point, show rows of text to a blind rater, while the
readable control C shows rows on the same page? The parent tested 59 short strips, each re-started on a human mark; long-range
sheet identity over a whole field was never tested.

## Truth rule (2026-10-05)

- w00 (P) is used ONLY to place one anchor point (its vertex at W's centre, as lasagna_fit's frozen seed) and, inside
  handfix's unchanged render path, as `crop_near`'s 800 µm patch selection (keeps the part of the winding near W; never a
  score). Every distance to P is printed as "vs P, local errors, description only". No bar uses P's position.
- **What decides:** a blind human read (rows / strokes / nothing) by both humans. Nobody picked the field, the arms or the
  pictures (all by frozen rules), so both may rate. Agent readers: none in the verdict (screening only, and none planned).

## Data and leakage

- **Fit:** `[private path][internal item]/out/post/` (120 windings, tifxyz step 20, 9.366 µm scan).
  Pinned: `w054/x.tif` sha256 `2f03ebac…166c`, `w055/x.tif` `44e7b13e…0270`; handfix's `cf.py` `209409ba…3468`.
- **No mark leaks into this field:** none of the parent's 112 strip stations lies within 0.5 mm of W (median 9.4 mm away;
  `[private path]`). Chris's marks are not read by any step.
- **Both raters know W.** Their "rows" is weak evidence and their "not rows" is robust (FIELD-R). Every outcome line says so.
- **Blinding:**
  - Everything that names a picture stays local and git-ignored: `tiles/`, `s0/`, `a/`, `surf/`, `cache/` (folder
    `.gitignore`), `spiralread_key.json`, `sr07_guard_key.json`, `sr07_guard_cands_key.json`, the ratings files and every
    `*_result.json`. Stage 0h (`sr07.py secrecy`) checks this with `git check-ignore` and exits 3 on a leak.
  - `stage0.json`, `arms.json`, `render.json`, `tiles.json` hold only gate flags, counts and geometry numbers.
  - **Lesson 21:** the question the raters see names only the time (~4 min) and the page order, never the controls or the guard.
  - Before Chris's page exists, the main session adds this item to `BLIND_EXTRA["chris"]` (`brainstorm_check.py`).
  - Chris's page goes to Drive `rating_pages/`; Sebastien's page stays in `cache/`.

## Arms and controls (frozen)

| picture | what it is | role |
|---|---|---|
| **A1** | post-snap winding nearest the anchor (×10 densified, point-to-surface; expected **w054**, 5.73 vx) | arm |
| A1-blank | A1's map in the wrong layer order | validity (must not be rows) |
| **A2** | second-nearest winding (expected **w055**, 8.52 vx; the anchor sits between the two) | pre-declared second arm (the one A-or-B fork decision 13 allows) |
| A2-blank | A2's wrong layer order | validity |
| C | w00's own W render (COPY-IN's `ctrl_level`), rebuilt pixel-identical (Stage 0g), then masked to the shared frame | readable control |
| C-blank | COPY-IN's `ctrl_blank` maps, masked to the shared frame | validity |
| guard (per rater) | a W picture THIS rater already called not rows blind, by the rule below, masked to the shared frame | leniency guard |
| calib / blank09 | FORMAT-20 `f_05.png` (0009B rows) / `f_06.png` (0009B blank) | validity; exempt from the frame check (other scan) |

- **Chain (handfix, unchanged):** `cf.crop_near` (pad 800 SV px, DMAX 800 µm) → `sv.render` to the 2.4 µm band (109
  layers) → `fwd2.npz` (80-px erosion) → canonical 2.4 µm model `r152_3ddec_v2_l5_epoch13` at +0, both orders
  (`infer_crop.py`) → `_assemble1` into W's frame → face rule picks the inked order (`cf.face`, BRIEF R3).
- **Shared frame:** S = control mask (`mask_ctrl.npy`) ∩ coverage(A1) ∩ coverage(A2). Every W picture is 0 outside S
  (holes and border identical across pictures, so no CH arm). The guard tile is masked by S taken to tile size with the same
  resize as the tiles (a tile pixel is outside when the resized mask is 0).
- **Pre-snap is not an arm** (more exposure of a known field; its nearest winding is a different file).

## Guard (Sebastien's decision 2026-10-12 21:50; frozen rule, `sr07.py guard_pool` / `guard_pick`)

1. **Pages:** every W page whose answers are rows / strokes / nothing and whose ratings file exists for that rater:
   partsheet_tolerance, depth_w, COPY-IN (Sebastien), fullhop_w, NODE-FILL-READ, NODE-FILL-REREAD (both); handfix read 1 and 2,
   INSET-NEG, grown_field, FIELD-R, FIELD-R ovl (Chris). One picture = one exact PNG (sha256; key `file` or `sha` resolved).
2. **Eligible** for a rater iff: a surface (level) picture (not a blank, not calib / blank09); the rater answered strokes or
   nothing on EVERY showing and it was shown to him **exactly once** before; it was never shown on a page whose result is still
   sealed (grown_field while `rawread9h_seb_ratings.json` is missing: the guard's identity would reveal the sealed call; such
   pages still count as showings); its PNG exists and has W's tile shape (800 × 469);
   it is not a guard already chosen for a sibling item (any `sha` in `*guard*key*.json` of grown_field or COLS-READ at
   build time); after masking with S its black share is within 2 points of C's (so it passes Stage 0f by construction; this
   drops holes pictures, which are burned on W anyway, BRIEF lesson 20).
3. **Order:** "strokes" pictures before "nothing" pictures, sorted by (page, picture id); one is drawn from the first non-empty
   group with `numpy.random.default_rng(20261043)` (Chris) / `(20261044)` (Sebastien) `.integers(n)`.
4. **None eligible for a rater:** job 2 exits 78 before any page; the Runner asks Sebastien with lettered choices and a
   step sheet. A burned guard is never used.
- **Planner check (counts only, before the shared mask exists, frame filter on the control mask alone = conservative):**
  a guard is available for both raters, both from the "strokes" group
  (`[private path]`; full counts git-ignored,
  because Chris's sealed grown_field calls feed them). Sebastien's pool is small: if COLS-READ draws the same picture first,
  this test's build excludes it and may hit point 4.

## Exposure (Critic fix 4; showings on answered pages)

- **Control C, byte-identical earlier showings:** Chris 6, Sebastien 1 (full W-page registry, `guardcount`); plus the
  re-framed L100 level on partsheet_tolerance and fullhop_w for both (2 each). On this page C is re-framed (masked to S), not fresh.
  Chris called C rows on ~5 of 6 showings before (FIELD-R's miss = the 4th).
- **Guard:** exactly 1 earlier showing for each rater, by the rule.
- Both counts are recomputed at page-build time and written to `stage0.json` (`guard_counts`), because other W pages
  (grown_field's second read, COLS-READ) may be rated in between.

## Page (one per rater; the standard page template)

- **Pictures:** A1, A1-blank, A2, A2-blank, C, C-blank, guard, calib, blank09 (9; 7 if A2 is dropped). ~4 min.
- **Order:** `numpy.random.default_rng(20261041)` (Chris) / `(20261042)` (Sebastien) permutation, redrawn until no arm is
  first and A1 and A2 are not adjacent. JPEG q 90 (85, 80 if the page would exceed 1 MB). Caption on every picture:
  "This piece: about 20 mm tall and 12 mm wide." Built once, never rebuilt.
- **Files:** `cache/spiralread_read_<rater>.html`; answers `spiralread_<rater>_ratings.json` in the job folder; key
  `spiralread_key.json` (git-ignored).

## Metric and outcomes (frozen; `sr07.py rater_class` / `outcome`, selftest-covered)

**Per rater** ("strokes" and "nothing" are both "not rows"):
- **VOID:** a picture unanswered, calib not rows, or the answers' `when` earlier than the page build.
- **INVALID:** more than 1 of the blanks (C-blank, A1-blank, A2-blank, blank09) called rows.
- **UNINFORMATIVE-C:** C not rows (FIELD-R).
- **VALID**, or **VALID-LENIENT** when the guard is called rows: a lenient rater's "rows" calls do not count toward a READS
  outcome; his "not rows" calls still count.

**Outcome (first match wins):**
1. **SPIRAL-NO-ROWS** (kills the one-anchor whole-field claim): a valid (or valid-lenient) rater calls every shown arm not
   rows. One rater suffices (robust direction for raters who know W); labelled "(one rater)" unless both.
2. **SPIRAL-READS:** both raters VALID (not lenient) and both call A1 rows. Labelled "raters know the field".
3. **SPIRAL-READS-WITH-PICK:** both VALID, A1 fails for at least one, both call A2 rows. Best-of-two: shows only that a readable
   winding lies one fork from the anchor; kept apart from the main claim, never merged into it.
4. **SPLIT:** anything else with two valid raters. Reported, no claim.
5. **INCONCLUSIVE:** exactly one valid rater and no NO-ROWS (one rater cannot carry READS).
6. **UNINFORMATIVE:** no valid rater, or Stage 0 exit 78.

- **Kill date:** 2026-10-19 23:59 CDT. Before it, `sr07.py score` waits for both files. After it, it scores the files present
  (a missing rater counts as not valid: NO-ROWS (one rater) or INCONCLUSIVE are then the only decided rows).
- **Package (b) wording.** READS: "one continuous spiral-fit winding, placed with the 5 centre clicks + one anchor point, reads
  rows over a 20 × 12 mm known-text field for two blind raters who know the field". NO-ROWS: "passes a strip-scale progress bar
  but does not read as a whole field (one anchor)". READS-WITH-PICK: "a readable winding lies one A-or-B pick from the anchor
  (best of two; who picks without seeing ink is untested)".
- **Description only (never a bar):** per arm, vs P local errors over S (median µm, share ≤ 75 / ≤ 150 µm), the face order,
  share of W vertices closer to A2 (`arms.json`, `sr07_desc_result.json`).

## Stage 0 (sanity checks first; numeric bars; pre-written fallbacks)

Job 1 (`job.sh`, CPU, before any render):
- **0h secrecy:** every tile / page / key / ratings / result path is git-ignored → else exit 3 (bug).
- **0c arms reproduce:** the script re-derives A1 / A2 = nearest / second-nearest post-snap winding to the anchor (×10
  densified, all 120) and checks the pinned `x.tif` shas → must give w054 / w055, else exit 3.
- **0d separation:** median over W's vertices of the distance from A1's nearest point to A2 ≥ 24 µm (the human depth tolerance
  tested, depth_w) → else A2 is dropped (pre-declared), A1 alone is shown.
- **0e seam:** share of W's footprint on a winding's first / last 2 grid columns ≤ 0.01 (premise: 0.0) → A2 failing: A2
  dropped; A1 failing: exit 78 (UNINFORMATIVE; fallback = an amendment that stitches w_k + w_k+1 by the frozen amendment-2
  orientation A, Sebastien asked first).
- `LOOP_DRY_RUN=1` stops here (exit 0).

Job 2 (`job2.sh`, GPU canon ~0.5 h, then CPU):
- **0g control rebuild:** the imported code rebuilds COPY-IN's `ctrl_level.png` pixel for pixel (max |diff| = 0) before any
  re-masking → else exit 3.
- **0a coverage:** |S| / |control mask| ≥ 0.80 (forecast ~0.97) → else, if |C ∩ A1| ≥ 0.80, A2 is dropped and S = C ∩ A1;
  else exit 78.
- **0b blanks are blanks:** r(Ai, Ai-blank) ≤ r(C, C-blank) + 0.10 on S (stride 4) → A2 failing: A2 dropped; A1 failing:
  exit 78.
- **guard:** per rater by the rule above → none for a rater: exit 78 (ask Sebastien).
- **0f frame (Critic fix 5):** every W picture of the page (arms, their blanks, C, C-blank, each rater's guard) has the same
  pixel shape and a black share within 2 points of C's → else exit 78. calib / blank09 are exempt (other scan; as on every
  earlier page).
- Read-only inputs (cf.py, COPY-IN's control arrays and tiles, the two windings, FORMAT-20 pair) are hashed before job 1 and
  re-checked after each job (`protect` / `protectcheck`; any change → exit 1).

## Seeds

Page order 20261041 (Chris), 20261042 (Sebastien); guard draw 20261043 (Chris), 20261044 (Sebastien). One fit seed (the
parent's), no re-fit.

## Compute budget

- Job 1: CPU ~1 h (two renders of ~3-4 cm² each; handfix's R, 5.3 cm², took ~30 min), ~15-20 GB disk.
- Job 2: GPU ~0.5 h (canon, 2 arms × 2 orders; handfix's R took ~16 min for both orders), CPU ~15 min. ≤ 1 h →
  5070 Ti by router rule 3; home only (`needs: local_inputs`). Cap: 2.5 h per job.
- Human: ~4 min per rater, both.

## What each outcome changes

- **READS:** package (b) gets a "5 centre clicks + one anchor per 20 × 12 mm field" row on the 9.366 µm scan's own surface,
  and the next test is a fresh field (other windows, other seeds).
- **NO-ROWS:** the parent PASS stays strip-scale only; package (b) says so; "one anchor click per field" is closed for this
  fit, and any follow-up must add sheet-identity help (e.g. A-or-B picks along the field), not a re-read.
- **READS-WITH-PICK:** a follow-up must test whether a person can choose the right winding without seeing ink.
- **SPLIT / INCONCLUSIVE / UNINFORMATIVE:** nothing goes into the package from this test.

## Odds (forecast, not data)

READS (A1, both) ~0.1-0.2; READS-WITH-PICK ~0.07-0.1; NO-ROWS ~0.45-0.6; SPLIT / INCONCLUSIVE / UNINFORMATIVE ~0.25
(Ideas; Critic `critic_odds_out.json`).

## Deviations from the Ideas / Critic design

1. **Guard:** Sebastien's per-rater "already rejected" rule replaces `cf.guard()` / partsheet_tolerance's H50 (burned, BRIEF lesson 20).
   The frame-black eligibility filter is new: without it a holes picture would fail Stage 0f for nothing.
2. **One valid rater, no NO-ROWS:** named INCONCLUSIVE (the Ideas list left this case unnamed).
3. **0b on A2** drops A2 instead of stopping (A2 is the secondary arm); 0b on A1 stops (exit 78).
4. **Seam stitching** is not coded (premise 0.0 edge share); if 0e fails for A1 the job stops (exit 78) and an amendment adds it.
5. **One page per rater**, because each rater has his own guard.
