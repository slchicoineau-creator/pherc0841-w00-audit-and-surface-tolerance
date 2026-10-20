> **Scrubbed public copy** (public name `grown_field`). The original was first committed to the authors' private repository at `4020ceb49` (2026-10-07T16:19:07Z). Timing: Committed and pushed before any output (its Judge's check). Timestamps live in a private repository; ask the authors for a verification. Scrubbing removed mentions of non-public scrolls and local paths (paths into the authors' private repository read `[private path]` and do not resolve) and replaced internal item ids and test names with public slugs (unmapped internal ids read `[internal item]`); the scientific text is otherwise unchanged.

# Pre-registration: grown_field, does the standard grower, one seed click and 0 correction minutes on PHerc0841's regular 9.366 µm scan, give a 20 × 12 mm surface that reads rows for a blind human?

- **Date:** 2026-10-07 (~11:00 CDT). Committed and pushed before any grow, render, ink map, tile or page of this test exists.
  Owner: Sebastien's side (station loop item `grown_field`, Critic PASS with fixes 3-8). Public data
  only. Claim: yes only on the two-rater line below.
- **Question (the objective's zero-minute row, first-wrap case):** with no finished neighbouring turn to copy from, what does the
  organizers' standard tracing tool give when nobody corrects it? Grow VC3D's `vc_grow_seg_from_seed` on public m7 L0 of the
  9.366 µm scan from one seed click, over the whole 20 × 11.7 mm S2 text window, and have blind humans read it next to the
  team surface. Wording everywhere: **"one seed click placed on the team mesh, 0 correction minutes"** (never "0 hand minutes").
- **Truth rule:** nothing is decided by w00's (P's) position. P is used only as (1) the place the seed clicks sit, (2) the
  crop-sizing box, (3) the image frame (each P pixel shows the grown surface mapped to it), (4) the readable control picture
  (w00's native mesh, rendered through the same path). Distances to P are written only as "vs P, local errors" in a
  git-ignored description file.
- **Not an unpark:** RAW-READ (`[internal item]`, parked by Sebastien) read band-L2 9.6 µm grows with agent readers under the old
  objective. This is the human-read rewrite on the eligible scan that `[private path]` asks for.

## Planner checks (mechanics only; no grow, no render, no ink)

- `[private path]` (`plan_crops.py`): native m7 L0 shape
  (19400, 7703, 7703). Snaps: A 7.14 vx (66.9 µm), B 2.24 vx (20.9 µm), B2 0, B3 0. Growth-sized crops 15.07 / 16.57 /
  15.13 / 15.98 G voxels (A / B / B2 / B3), none clamped. Every secret path below is git-ignored (`secrecy_not_ignored: []`).
- `r9.py selftest`: the frozen scorer passes 18 synthetic cases (every rater branch and the four two-rater combinations).

## Data, recipe, and why nothing can leak

- **Grower (c1grow recipe, `[private path]`):** public m7 L0 of volume 20250821151531 (the 9.366 µm scan),
  `step_size` 20, `voxelsize` 9.366, the standard grower params, `thread_limit` 4, normal grids `--grid-step 64 --prune-min-length-px 20
  --spiral-step 20 --sparse-volume 1`, Docker image `vc3d-deps` sha-0c371b1, `--cpus 4`. Changes: **`generations` 46** and
  growth-sized crops. m7 knows nothing of P or the labels.
- **Seeds (P sv row, col; GROWN-READ-20's points):** **A** (10751, 12830), **B** (6600, 12830), each snapped to the nearest m7 L0
  foreground voxel within ±8 vx (`c1grow.seeds()` rule). Backups **B2** (5800, 12830) then **B3** (6600, 14200), grown in that
  order only while gate (a) is below 0.95. Each seed's snap distance is reported. A seed that snaps onto a neighbouring sheet is
  the tool's behaviour and counts.
- **Crop per seed (Critic GROW-ARM-9 finding 3):** bbox of mesh_P points within 13 mm (3-D) of the snapped seed, + 2 mm (214 vx)
  on every face, clamped to the volume. A grown bbox within 20 vx of a crop face that is not the volume edge is a crop artefact:
  that face is extended by 4 mm (428 vx) and the seed regrown once. Still touching → execution failure, excluded, reported.
  **Crash rule:** non-zero Docker exit or no `saving` line → execution failure (job exits 5, fix and relaunch; finished grows are
  reused), never data. A completed grow with no output is NO-GROWTH (counts as tool behaviour).
- **No P-based seed gate:** unlike GROWN-READ-20 there is no winding gate (g2). Every grown seed enters the field.
- **Render (native path, COPY-IN's `ci.py` with the crop origin added):** crop-local grown mesh + crop origin → band frame by
  the w00 2.4 µm transform (`C.toband`); each seed's grid cropped to the vertices whose nearest P point lies in the S2 window ± 800 sv px
  (+10 vertices; in-plane only, **no distance cut before the render**); 109 layers at 2.4 µm (`src_vox_um` 9.366); canonical
  2.4 µm model at **+0**, both orders (R3).
- **Face order per seed:** `gr20.face_order` rule (outward fraction vs the scroll centre from band L5; P-free). Level = the seed's
  own order, blank = its other order.
- **P-frame assembly (fu.py / rr.py):** each 2-px cell is mapped to P (nearest P point refined along P's tangents). A P pixel of
  the S2 window (sv rows 4511-12830, cols 10392-15268) is covered by a seed if an interior cell (80-iteration erosion, ≤ 1 mm from
  P) maps within 8 sv px; among covering seeds it takes **the seed nearest in (row, col)**, never chosen by depth. **Holes stay
  black.** The 1 mm cut and the nearest-seed rule are image-frame choices: the share of in-window cells dropped by the cut and
  the share covered by two or more seeds are reported (Critic finding 7). A grow one or two windings off (~330-660 µm) is shown.
- **Masks:** control mask Mc = COPY-IN's fixed control mask (S2 ∩ P ok ∩ native w00 coverage). Grown tile mask = Mc ∩ the grown
  union's own coverage: holes the grower leaves count against it.
- **No leak / blinding:** the pictures are made by code from existing models; nothing is tuned on them. Tiles, pages, keys,
  ratings, results and every distance number are git-ignored (`[private path]<id>/.gitignore`, repo rules `*key*.json`,
  `*_ratings.json`, `*_result.json`); `r9.py stage0` refuses to run if any of those paths is not ignored. Committed job files
  (`stage0.json`, `select.json`, `render.json`, `tiles.json`) hold mechanics only (snaps, crops, timing, margins, stop
  generations, areas, coverage, hole share, plumbing pass/fail).

## Pictures on each page (6; standard page template, rows / strokes / nothing, JPEG q 90, the grown tile never first)

| Role | Picture |
|---|---|
| grown | the assembled grown tile, each seed in its face-rule order at +0, on Mc ∩ own coverage |
| grown_blank | the same in each seed's other order (a wrong-order blank) |
| ctrl | native w00's level tile on Mc (COPY-IN `tiles/ctrl_level.png`, re-made pixel for pixel by this code in Stage 0 b) |
| calib | FORMAT-20 0009B calibration `f_05` |
| blank09 | its reverse `f_06` |
| guard | the partsheet_tolerance surface picture that **both** humans called not rows blind (picked by rule in Stage 0 c; named only in a git-ignored file while depth_s022814's rating is pending) |

## Raters and order (Critic finding 5 and GROW-ARM-9 finding 9)

- **Read 1, Chris (sets the class):** his own page (`cache/rawread9h_read_chris.html`), rated **after** his handfix read page and
  INSET-NEG's page (the scorer labels a broken order from the pages' `when` stamps). Neither human made the grown surface.
- **Read 2, Sebastien (can only upgrade):** his own page (`cache/rawread9h_read_seb.html`, other picture order), only after
  handfix step 2 resolves (F saved, or step 2 declined or killed), because handfix's inset is 43 % of this window
  (prereg copyfix9 :51-53). His wait ends at the latest on **2026-10-19**; if he has not rated by then, the result is reported
  with Chris's class alone.
- **Sealed until read 2:** Chris's class stays in the git-ignored `rawread9h_result.json` (the scorer prints only "sealed") until
  Sebastien has rated or his read is declined / timed out, so nothing reaches Sebastien before his own read.
- **Agent screen (Stage 0 d):** 5 fresh `general-purpose` agents on the grown tile and 5 on the control (RAW-READ's prompt
  wording, neutral folder `[private path]`). **Screening only: reported, never decides, never gates a human page.**

## Outcome (scorer frozen in `r9.py`: `rater_class`, `combine`; selftest 18 cases)

- **Per rater:** **VOID** if a picture is unanswered, the calibration or the w00 control is not called rows, a wrong-order blank
  (grown_blank or blank09) is called rows, or the guard is called rows. Else **GROWER-READS** if the grown tile is called rows,
  **GROWER-FAILS** otherwise (strokes or nothing).
- **The result's class is Chris's:**
  - Chris VOID → **VOID**.
  - Chris GROWER-READS + Sebastien GROWER-READS → **GROWER-READS (two raters)**: package (b) line "the standard grower, one seed
    click and 0 correction minutes on the regular scan, gives a 20 mm field that reads rows for two blind humans (one window,
    known text, one grow per seed)". It is the objective's first zero-minute number in the first-wrap case.
  - Chris GROWER-READS + Sebastien not rows → **GROWER-READS (one rater: Chris)**, reported as a split; no two-rater claim.
  - Chris GROWER-FAILS + Sebastien rows → stays **GROWER-FAILS (one rater: Chris)**; his read is reported beside it with his known
    lean (1/8 partsheet_tolerance surfaces called not rows).
  - Chris GROWER-FAILS + Sebastien not rows → **GROWER-FAILS (both raters)**: "uncorrected standard grower does not read (one
    window, this grow pair)"; the zero-minute row is then the copy (handfix) where a neighbour exists, and correction minutes
    are needed otherwise.
  - Sebastien VOID or not rated by 2026-10-19 → Chris's class, labelled "one rater (Chris)".
- **Fixed wording labels:** every line says "one window, known text" (both raters know W's text, depth_s022814 caveat) and "one grow
  per seed" (a FAIL says "this grow pair", not "the grower"). A READS line says **"reads rows; the read does not show the sheet"**
  (a field on a consistent neighbouring winding would read that winding's text; package (b) must not say "stays on the sheet").
  A FAILS line carries the hole share of the control field ("fails; holes X %"). The guard has been seen before by both raters,
  so it checks a "rows to everything" rater only loosely. The control, the 0009B pair and the guard are pictures Chris has rated
  before; only the grown pair is new to him.
- **UNINFORMATIVE:** gate (a) fails, or Chris has not rated by **2026-10-19** (kill date).

## Stage 0 (sanity checks first; `job.sh` runs them before any mask write or grow)

- **Selftest:** scorer on synthetic answers. Fail → exit 3 (bug).
- **Secrecy:** every tile / page / key / rating / result / prompt / neutral-folder path git-ignored; neutral folder empty. Else
  exit 3.
- **(c) Guard (CPU, seconds):** the partsheet_tolerance level pictures whose raw answers are not "rows" for both raters (rating files
  hash-checked against `hts.py`'s). The count must equal the Critic's `critic_guard_exists.json` (1); a different count → exit 3
  (bug). Zero → exit 78 (the read waits; it never runs without a guard).
- **(b) Control plumbing (CPU, ~5 min):** this code's assembly, sampling and image functions re-make COPY-IN's
  `tiles/ctrl_level.png` and `ctrl_blank.png` **pixel-identical** and its `mask_ctrl.npy` identical, from COPY-IN's `a/N2` maps.
  Else exit 3.
- **(e) Native plumbing (CPU, ~10 min; Critic finding 6):** old C1-GROW seed 2 (`[private path]`, same point as seed A) goes
  through the NEW crop-origin → band → render → fine-map → P-frame code. On pixels ≤ 25 µm from P: **≥ 50,000 px, raw layer 54 vs
  P's p109 layer 54 r ≥ 0.4, and r < 0.15 with a 1 mm shift** (GROWN-READ-20's bar, 0.65 vs 0.06). Fewer than 50,000 px → the
  same check on old seed 1 (`g/1`); still too few, or a failed bar → exit 3 (BUG: fix the port, never read).
- **Mask timing (Critic finding 8):** seed A's mask write is timed before any grow starts (masks are written one at a time with
  ≤ 10 workers, then the two Dockers run in parallel). Over 150 min → exit 78; the Runner asks Sebastien whether to continue.
- **(a) Coverage (after the grows):** union coverage of the S2 window's P-valid mesh_P vertices (20-px grid) within 30 sv px of an
  interior forward-mapped point (≤ 1 mm from P) **≥ 0.95**, else backups B2 then B3; still < 0.95 → exit 78, **UNINFORMATIVE (no
  20 mm field)**, shares reported. Each seed's footprint, stop generation, crop margins and coverage alone are reported.
- **Tile plumbing (job 2, bug gate, rr.py's):** with ≥ 50,000 px ≤ 25 µm from P on the grown mask: raw layer 54 r ≥ 0.4 and
  > r_shift1mm + 0.2, else exit 3. Numbers go to the git-ignored description file; the committed `tiles.json` says only the gate.
- **(d) Agent screen:** reported only (above).

## Compute, budget, kill date

- **Job 1 (`job.sh`, CPU, gpu no):** ~4-6 h wall (two 15-17 G-voxel masks, two parallel 46-generation grows at 4 CPUs each, renders);
  the time limit is set through the item's `gpu_hours` 7 (11.5 h). Backup seeds or a re-crop add ~2 h each.
- **Job 2 (`job2.sh`, GPU):** canonical maps at +0, both orders, per rendered seed, ~0.5-1 GPU-h; tiles, two pages, agent prompts.
- **Human:** Chris ~3 min; Sebastien ~3 min later. No money beyond the loop's daily budget. No seeds to set (deterministic grows;
  page orders from fixed seeds 20261077 / 20261078; agent image order 71100 + n).
- **Kill date: 2026-10-19** (Chris's queue: handfix pages, INSET-NEG, key-fix file and others wait on him).

## What each outcome changes

- **GROWER-READS (two raters):** package (b) gets "~0 human minutes per readable cm² where public m7 is as good as at W" for the
  first-wrap case (one window, known text, one grow per seed; the read does not show the sheet). Next: a window of text neither
  human has seen, and more grows per seed before any rate is quoted.
- **GROWER-READS (one rater) / split:** reported as one-rater results; no package claim.
- **GROWER-FAILS:** package (b) says the uncorrected standard grower does not read on this window; correction minutes are the
  measure for the first-wrap case (handfix's timed session, lasagna_fit).
- **VOID / UNINFORMATIVE:** no claim; the cause (rater validity, coverage, Chris's time) is reported.
