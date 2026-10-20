> **Scrubbed public copy** (public name `fullhop_s022814`). The original was first committed to the authors' private repository at `88da117ad` (2026-10-08T13:31:54Z). Later commits to the same file: `88c857c03` (2026-10-12T01:47:14Z, post-run, see the note at the end). Timing: This copy is the version of the first commit, made before any output (its Judge's check). A pointer note added after the ratings is reproduced at the end, labelled post-run. Timestamps live in a private repository; ask the authors for a verification. Scrubbing removed mentions of non-public scrolls and local paths (paths into the authors' private repository read `[private path]` and do not resolve) and replaced internal item ids and test names with public slugs (unmapped internal ids read `[internal item]`); the scientific text is otherwise unchanged.

# Pre-registration: fullhop_s022814. On a second labelled window (the organizers' own s022814 surface, nothing from w00), does a field with ~30 % of its area moved onto a real neighbouring sheet still read rows for BOTH humans?

- **Date:** 2026-10-08 (CDT), pushed before any damaged surface, render, map or tile of s022814 exists. Owner: Sebastien's side
  (station loop item `fullhop_s022814`; Sebastien chose "A) go ahead together with the sister test, one
  shared page" on 2026-10-08 07:30). Public PHerc0841 data only. Feeds package (b) (readable-surface budget), row 2.
- **Why:** partsheet_tolerance's "~70 % on the right sheet still reads" rests on one window (W), one picture per level, built from w00.
  fullhop_w (`preregs/fullhop_w.md`, running) asks it again on W with every damaged patch moved a full sheet. This
  test is its second window: the same damage law on depth_s022814's frozen s022814 window, whose undamaged picture both humans
  read as rows on 2026-10-07 (depth_s022814, WIDE-HOLDS, both valid).
- **Truth rule:** the verdict is a blind two-human read. Ink labels (the organizers' s022814 labels, independent of w00: Dice
  0.028) only gate the construction (Stage 0a plumbing, Stage 0b "is the true text gone from the moved pixels?"). No w00
  position is used anywhere: base surface, depth origin and doses are all s022814's. Agent readers are not used.
- **Disclosed before this file (construction-only numbers, none is a reading):** the Critic's fetch size
  (`[private path]`: 18.7 GB at ±330 µm, 100 %
  inside the volume) and the Planner's dry run `planner_tiny_out.json` (same folder): our render chain on a 1 mm² crop of the
  organizers' 2.403 µm s022814 tifxyz matches the organizers' own s022814 SV at r 0.993 (central layer, zero in-plane shift),
  layers in reverse order (r 0.986 flipped vs 0.04 same order), mesh normal pointing away from the scroll centre on 100 % of
  vertices (so our raw +o = outward and the inked order on our render is expected to be `rev`, as on W). The flip is exact:
  our layer k = their layer 108 − k (mean r 0.986; 107 − k 0.944, 109 − k 0.952), so our o = +1 window (layers 24-85, reversed)
  is depth_s022814's a* = 0 window (their layers 23-84, forward) layer for layer.
- **Disclosed:** both raters have seen this window's undamaged picture (and its ±24 / ±48 µm pictures) once, on 2026-10-07.
  Recognition biases toward "rows", so a FAILS-814 result is the more credible one. Sebastien has called rows on almost every
  surface picture so far (lesson 20), so in practice Chris's answers decide.

## Data and why nothing can leak

- **Base:** the organizers' `PHerc0841/segments/20260221022814-auto_grown_20260220174252405/mesh/20260221022814-on-20260319124803-2.403um.tifxyz`
  (733 × 955 grid, 48 µm step), cropped to grid rows 0-418, cols 380-630 (depth_s022814's frozen window, SV rows 0-8320, cols
  7644-12521 = grid rows 0-416, cols 382-627, plus a margin). Our pixel j = SV canvas column 7600 + j (dry run: shift 0).
- **Volume:** `PHerc0841/volumes/20260319124803-2.403um-0.2m-77keV-masked.zarr` (the band TOL-20 renders from).
- **Sheet map for the hop law:** public m7 (`...surface-m7-L2-th0.2.zarr`, level 2 = 9.612 µm, in the same 2.403 µm frame as
  the mesh; read directly, no transform), fullhop_w's lookup unchanged.
- **Labels and depth_s022814 references (read only):** `[private path],supervision,ok,sv24}.npy`
  and its control map `maps/ink_fwd_o+0.npy` (a* = 0 on the organizers' SV).
- **Fields:** levels: `default_rng(20261008)` standard normal on the crop grid, Gaussian σ 10.4 vertices (0.5 mm, TOL-20's law);
  holes guard: `default_rng(20261009)`, σ 30 vertices. Page shuffle (own page only): `default_rng(20261009)`.
- **Pictures for the humans:** `[private path]<id>/tiles/` (git-ignored); page list `t8_page_extra_key.json`, Stage 0 numbers
  `t8_s0a_result.json`, `t8_s0b_f<FLOOR>_result.json`, score `t8_score_result.json` are git-ignored (`*key*.json`, `*_result.json`).
  Only PASS / FAIL lines and construction numbers (masks, off-sheet shares, coverage) go into the item before both have rated.

## Arms

- **Hop law = fullhop_w's (so the two windows compare):** each hop vertex moves outward (away from the scroll centre,
  `fs_profile.centre_fn`, as fullhop_w) along the mesh normal to the centre of the nearest public-m7 run lying **140-250 µm**
  out (FLOOR 140); if none, a constant **150 µm**. Displacement field × hop mask, Gaussian σ 1 vertex.
  - **m7 support check (decides the law, not a stop):** share of base vertices with m7 foreground within ±2 level-2 voxels
    (±19 µm) along the normal. ≥ 0.50 → the law above; < 0.50 → constant 150 µm for every hop vertex (reported). The Critic's
    rule ("an m7 run centre within ±25 µm of the surface") is replaced by this foreground-within-±2-voxels share, the same
    measure fullhop_w's off-sheet check uses (±1 voxel there), so the support and DARK-HOPS numbers are on one scale.
  - **Changes from the Critic's design, with reasons:** (1) floor 140 µm, not 120, and (2) no CT-run fallback: both are
    fullhop_w's Planner changes (`preregs/fullhop_w.md`, "Changes"), kept identical so the windows compare; on
    W a CT point threshold called the true sheet itself "dark" 0.40-0.41, so a CT lookup picks near-random depths. (3) The m7
    map needs no 9.366 → 2.4 µm transform: it is on the 2.403 µm frame, like the mesh. (4) The Stage 0b fallback floor is 170
    (constant 200), fullhop_w's, not the Critic's 160.
- **Primary picture:** **L70_814** (top 30 % of the field hopped).
- **Levels (nested, same field):** **L85_814** (top 15 %, descriptive), **L70_814**, **L55_814** (top 45 %, guard).
- **Guard:** **H50_814** (50 % holes, TOL-HOLES law on this grid, base surface, no hops).
- **Controls:** **ctrl814** = our render of the undamaged crop (the readable control; the raters saw depth_s022814's near-identical
  ctrl once); wrong-order (fwd) blanks of ctrl814 and L70_814; the FORMAT-20 0009B calibration pair (shared with fullhop_w).
- **Readout:** `surfvol.render(..., BAND, 0, 2.403, 2.403, 161)` → central 109 layers; canonical 2.4 µm model (`tr._model` /
  `tr._infer`, 62-layer window at **o = +1 on our render, fixed for every picture** = depth_s022814's label origin a* = 0 window
  layer for layer, the Critic's item 4); rev = level, fwd = blank. Tile = depth_s022814 window (our pixels rows 0:8320, cols 44:4921), 800 px, bilinear, fixed
  clip 0-1. (fullhop_w picks its offset by the p99 depth-pick rule; the two windows differ in this, reported.)

## Stage 0 (sanity checks first; each exits 78 with its numbers in `t8_stage0.json`)

- **Sister gate (before anything; Sebastien's choice: this test's checks come after the sister's):** job.sh sleeps (no compute)
  up to 150 min until fullhop_w's Stage 0b is decided. Sister 0b passed (floor 140 or 170) → go. Sister stopped at 0c / 0d /
  coverage (not a reach result) → go alone. Sister "reader still reaches" (0b failed at 170) → **stop, INCONCLUSIVE, no GPU**
  (same law, same reader). Still undecided after 150 min → exit 78 WAIT-SISTER (Runner re-launches job.sh later; no fallback).
- **0d DARK-HOPS (CPU, before any render):** off-sheet(v) = no public-m7 foreground at the nearest level-2 voxel or ±1 voxel
  along the normal. **Bar, L70_814: off-sheet share of moved (> 50 µm) vertices at their smoothed positions ≤ off-sheet share of
  the SAME vertices on the base surface + 0.10.** Fail → **DARK-HOPS**: stop, UNDECIDED, no GPU, no page. (fullhop_w's metric;
  replaces the Critic's "≤ 0.3 below the CT Otsu threshold" for the reason in Arms (2).) L85 / L55 shares reported.
- **0a-ct PLUMBING (CPU, after the ctrl render, before the damaged renders):** our ctrl render layer k vs the organizers' SV layer
  108 − k over the whole window, mean Pearson r over k = 14, 22, …, 94 on pixels valid in both: **≥ 0.95** (dry run 0.986 on
  1 mm²). Fail → VOID (plumbing), stop.
- **Coverage (CPU, after the renders):** window valid fraction of each damaged render ≥ ctrl814's − 0.01. Fail → VOID, stop.
- **0a PLUMBING (GPU, first ~8 min):** ctrl814 maps at o = +1, on supervision pixels of the window: (i) label AUC(rev) −
  AUC(fwd) ≥ 0.10 (inked order = rev, as the dry run predicts); (ii) Pearson r of our rev map vs depth_s022814's control map ≥
  0.90; (iii) |label AUC(ours) − label AUC(depth_s022814's map), same pixels| ≤ 0.03 (depth_s022814: 0.868). Fail → VOID, stop.
- **0b hand-over (GPU, after the L70_814 maps):** at o = +1, supervision pixels valid in ctrl814 and L70_814:
  - **hop pixels** (moved > 50 µm, per-vertex displacement densified exactly as the render): label AUC(L70_814 rev) ≤
    **min(AUC(L70_814 fwd, same pixels) + 0.05, 0.70)**. (The absolute cap keeps a lenient blank from passing: depth_s022814's
    blanks were 0.60-0.65 on this window, ctrl 0.868.)
  - **unmoved pixels** (≤ 5 µm): AUC(L70_814 rev) ≥ AUC(ctrl814 rev, same pixels) − 0.02.
  - Fail → exit 78. **Pre-written fallback, once:** the Runner launches `job_f170.sh` (CPU; run law 170-250 µm, constant 200;
    folder `f170/`, nothing overwritten; 0d, coverage repeat) then `job2_f170.sh` (GPU). Fail again → **INCONCLUSIVE ("reader still
    reaches")**, no page.
  - Reported (git-ignored): AUC by band 50-120 / 120-150 / > 150 µm, ctrl on the hop pixels, all pixels.
- **Chance of no answer:** about 3 in 10 (Critic); Stage 0 part about 1 in 10 (plumbing nearly ruled out by the dry run; DARK-HOPS
  and 0b as on W, where 0d passed).

## Blind page (Runner step, NOT in the jobs; one sitting with fullhop_w, after Chris's handfix pages)

- **fullhop_s022814's 7 pictures:** ctrl814, L85_814, L70_814, L55_814, H50_814 level tiles; ctrl814 and L70_814 blanks. They join
  fullhop_w's page through `fh.py page [private path]<id>/t8_page_extra_key.json` (one shuffle, the shared 0009B calibration pair,
  ~16 pictures, ~8 min per rater; answers in `ratings/{seb,partner}/fullhop_ratings.json`). Same page wording; the question names
  no control. **Own page instead** if fullhop_w builds no page (it stopped in Stage 0 or was dropped), builds it without
  fullhop_s022814's pictures, or `fh.py page <extra>` fails its 1 MB size check (likely: depth_s022814's 14-picture page was already 858 KB,
  pictures ~45-70 KB each, so ~16 pictures may pass 1 MB): the Runner builds `t8.py page` (7 + the same calibration pair, ~5 min;
  answers `ratings/{seb,partner}/tol814_ratings.json`) and both pages are rated in the same sitting. `t8.py score` uses the
  shared key only if it holds fullhop_s022814's pictures, else its own key.
- Both rate independently, no comparing notes; Chris first if possible.

## Outcome rule (`t8.py score`, self-tested on 10 synthetic cases before anything runs)

- **Valid rater:** every fullhop_s022814 and calibration picture answered; calib "rows"; 0009B blank, ctrl814 blank and L70_814 blank
  each not "rows". A valid rater who does not call ctrl814 "rows" is UNDECIDED for this window ("window too weak").
- **UNDECIDED** if < 2 valid raters.
- **FAILS-814:** ≥ 1 valid rater with ctrl814 "rows" calls L70_814 not "rows".
- **HOLDS-814:** both valid raters call ctrl814 and L70_814 "rows", AND ≥ 1 of them calls H50_814 or L55_814 not "rows".
  fullhop_w's W guards never count toward HOLDS-814 (both raters know W well).
- **UNDECIDED:** a rater's ctrl814 not rows (and no FAILS from the other); no 814 guard called not rows (lenient on this window);
  DARK-HOPS / reader still reaches / VOID / sister stop from Stage 0.
- **L85_814 is descriptive** (one picture): if FAILS-814 and both valid raters read L85_814 rows, write "this window read with
  ~15 % deep hops, not ~30 %".
- **Cross-window line, only if both windows are decided:** both HOLDS → "~30 % one-sheet hops still read on two windows (both
  seen once before)"; both FAILS → "do not read on either window"; split → "window-dependent; s022814's map is weaker (label AUC
  0.868 vs 0.966)", never "a second wrap needs more".
- n = 2 raters, one picture per level, one window: a description of this window. A HOLDS shows rows, not the right text (the
  outward neighbour carries its own writing).

## Compute and dates

- job.sh (CPU, `gpu no`): sleep for the sister (≤ 150 min), then mesh crop, surfaces + m7 block (~5 min), 5 renders of 161
  layers (each fetches its chunks into RAM, ~11-19 GB, as fullhop_w, whose renders take ~20 min each; threads capped at 6).
  Limit set by `gpu_hours 3.5` (loop limit 6.25 h); a timeout is resumable (finished renders are skipped).
- job2.sh (GPU): 10 maps of 62 layers at o = +1 (~4 min each) ≈ 45 min; `--hours 1`. With the 170 fallback ≈ +4 renders + 8 maps.
- Disk ~40 GB of renders and maps under the item folder (git-ignored). Never writes into depth_s022814's or fullhop_w's folders.
- Human time: shared sitting with fullhop_w ~8 min each (alone ~5 min), only if Stage 0 passes.
- Kill date: 2026-10-24 (package (b) freezes ~Oct 25).

## What each outcome changes

- **HOLDS-814:** package (b) row 2 "~70 % right sheet reads" stands on a second window, built on the organizers' surface.
- **FAILS-814:** row 2 must say the ~30 % line does not hold on this second window (and per the cross-window line above).
- **UNDECIDED / DARK-HOPS / reader still reaches / VOID:** row 2 keeps its one-window wording; no second-window claim.


## Post-run note (public copy)

The original file received one more commit after both ratings (`88c857c03`, 2026-10-12T01:47:14Z, with the result digest).
It added only this pointer: the rated page used line_spacing's masked tiles of this test's 7 pictures (common frame, 84.6 %
of the window) plus its 2 line-field pictures, made by a page wrapper that leaves this test's scorer unchanged. That change
was bound in the line_spacing pre-registration (`preregs/line_spacing.md`, private commit `c106700b0`,
2026-10-11T17:12:15Z), before the page build and before any rating. Surfaces, orders, offset and the scorer are unchanged; the
2 line-field pictures never count toward this test.
