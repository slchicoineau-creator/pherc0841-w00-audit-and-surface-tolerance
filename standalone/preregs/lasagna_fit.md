> **Scrubbed public copy** (public name `lasagna_fit`). The original was first committed to the authors' private repository at `78efbb4a4` (2026-10-07T19:19:46Z). Later commits to the same file: `1ecc4e0d3` (2026-10-07T19:23:51Z). Timing: Original and fix commit both before any output (its Judge's check). Timestamps live in a private repository; ask the authors for a verification. Scrubbing removed mentions of non-public scrolls and local paths (paths into the authors' private repository read `[private path]` and do not resolve) and replaced internal item ids and test names with public slugs (unmapped internal ids read `[internal item]`); the scientific text is otherwise unchanged.

# Pre-registration: lasagna_fit, does the organizers' lasagna route give a readable 20 × 12 mm field on PHerc0841's regular scan with no correction?

- **Date:** 2026-10-07 (~15:00 CDT), committed before any centre click, any lasagna inference on the window, any shell, fit, render or
  page for this test exists. Owner: Sebastien's side (station loop item `lasagna_fit`). Public data only.
- **Sebastien's choice:** B (2026-10-07 13:38): judge by a blind read, not by "right sheet?" crosses (the fresh 2.4 µm cross pool holds
  only 9 bend sites, item Plan). His 11:17 answer accepted ~10 min of centre clicks and 4-8 GPU-h.
- **Why:** the main line's zero-correction arm (BOARD decision 11). Lane A's question is human minutes per readable cm² on the 9.366 µm
  scan with the organizers' tools (BRIEF §1). Lasagna's own multi-winding fit was never run on 0841 (LASAGNA-COST used its channels only as a
  local cost, `KILLED.md:90`). The shipped seed fit ties one layer to itself one wrap later and counts sheets between them through grad_mag
  (`winding_density` 0.01): a global signal of the kind BRIEF S4 asks for.
- **Truth rule:** w00 (P) is used only for placement (the seed point, the display frame) and as the blind readable control. Nothing is
  scored against its position.

## Data, and why nothing leaks

- PHerc0841 regular scan `20250821151531-9.366um` level 0 (lasagna input) and level 2 (click slices); known-text region W, the FORMAT-20 S2
  window (20 × 11.7 mm on w00). Read pictures: the canonical 2.4 µm ink model at +0 on the 2.4 µm band (reading chain R1), as every earlier
  0841 read.
- The fit sees only: the lasagna UNet outputs (public checkpoint `scrollprize/lasagna` rev de45f011, sha `4cc0c40a…` = the PHercParis4
  production run), Sebastien's centre clicks, one seed point. It never sees w00, m7, ink maps or any read picture.
- **Seed (frozen):** native (x, y, z) = **(3696, 4054, 14558)**, the w00 vertex at the S2 window's centre
  (`[private path]`). Placement only, as the grower's seeds.
- The centre clicks are a global input (the scroll's axis), not a trace of W's sheet. Their minutes are logged as human minutes.

## The route (the organizers' shipped tools; deviations listed are engineering only)

1. **Centre clicks (Sebastien):** 5 whole-scroll slices at native z 12800, 13600, 14500, 15400, 16200 (level 2, 37.5 µm/px); one click on
   the spiral's centre per slice or "can't tell". Need ≥ 3 valid clicks incl. one at z ≤ 13600 and one at z ≥ 15400, else stop (ask).
   The clicks become `umbilicus.json` (lasagna's `control_points` format).
2. **Stage 0c (CPU):** every W vertex ≥ 214 vx (2.0 mm, xy) from the clicked axis at its z. Else **STOP-CORE**: W sits at the core and
   cylinder start rings make no sense there; no claim, ask Sebastien.
3. **Lasagna UNet inference (Windows, FIBER-9's frozen production settings):** a box centred on the axis, half-width = (max W-to-axis
   distance + 107 vx), z 13391-15700 (W's z range 13498-15593 ± 1 mm), aligned to 256. Projection = input voxels × 226 s per G vx (FIBER-9
   measured) + download at 25 MB/s (level 0 is uncompressed: 1 GB per G vx). **> 8 h → stop and ask** (STOP-BUDGET).
4. **Start shells:** `cyl_init_tool.py` with the shipped `configs/init_cyl.json` (the shipped shell config that has the cylinder-grow-refine
   stage; `init_cyl_fine.json` differs only in a 1.02 grow factor = many more shells), `--z-range 13391 15700`, `--shell-count 12`, continued
   with `--start-shell <last shell>` in +12 steps until the last shell's median radius ≥ the seed's radius + 107 vx (cap 60 shells; past the
   cap = engineering stop).
5. **Seed fit:** `fit.py` with the shipped `configs/init_snap_surf_self_full.json` unchanged (self-map `multi_wrap_full`, one layer wider
   than one wrap tied to itself one wrap later, `winding_density` 0.01, `data` 0, station anchor at the seed), `--seed 3696 4054 14558
   --model-w 1.25 --model-w-unit wraps --model-h 2309 --depth 1`, export to tifxyz.
6. **One-wrap cut (P-free):** in lasagna's own grid, keep the columns within ± half a wrap of the seed's column (columns per wrap from the
   unwrapped angle around the clicked axis). This removes the overlapping second turn without asking w00 which turn is right.
7. **Own-grid coverage gate:** share of valid, finite vertices in the patch of the cut grid with rows at W's z range and columns within
   ± 5.85 mm (arc length) of the seed column. **< 0.70 → KILL without a read** (TOL-HOLES: 30 % holes did not read). A fit that crashes is
   engineering; a fit that runs and returns NaN / leaves the patch counts against coverage.
8. **Render and pictures (job 3):** the cut surface through handfix's render path (`cf.py` render: band transform, crop near the S2 window
   with its 800 µm display limit, canonical model at +0 both orders), face order by the house face rule (`cf.face`, scroll mass centre; P-free),
   blank = the other order. One full-field S2 picture (L_level) and its blank (L_blank), FORMAT-20 size, as COPY-IN's tiles.
   - Grower picture (description only): GROW-20's raw seed-A surface (`[private path][internal item]/g/A`), same path.

Engineering deviations allowed (they change speed or plumbing, not the fitted maths): the cylinder tool and fit run in WSL (no MSVC on
Windows; lasagna's streaming loader hard-codes JIT CUDA kernels), `--sparse-prefetch-backend python-zarr` (tensorstore not installed),
`compile_cyl_normal` falling back to eager (the code does this itself), `--cuda-gridsample 0` (lasagna's own PyTorch path) if the dense
kernel does not build, a smaller inference tile on out-of-memory (FIBER-9 rule). Any other config change needs an amendment before outputs.

## Stage 0 (sanity checks first)

- **Stage 0a (job 1, ≤ 1 GPU-h, before Sebastien clicks anything): plumbing smoke of the exact chain on data we already have.** FIBER-9's
  n41 lasagna products (crop x 2816-4352, y 3328-4608, z 14080-14592), a DUMMY centre at the crop's xy centre (3584, 3968), `cyl_init_tool`
  with the shipped `init_cyl.json` (steps capped at 100) for 2 shells in z 14150-14520, then `fit.py` with the shipped self-map config
  (10 steps per stage), seed (4084, 3968, 14336), model-w 1.25 wraps, model-h 300, depth 1, tifxyz export. Smoke outputs are never
  rendered, read or scored; lesson 16: it times nothing for the real run.
  - **Bar:** WSL env builds; ≥ 2 shells written; the fit exits 0 and exports a tifxyz with ≥ 50 % finite valid vertices.
  - **Ladder:** WSL as shipped → WSL with `--cuda-gridsample 0` (only if the dense grid-sample kernel failed to build). If both fail, the
    job exits 78 with the class (env / compile / data / diverged / other) in `stage0.json`. **Fallback:** the Runner may make ONE engineering
    fix (≤ 1 h: a missing package, path or env var; no config change) and relaunch job 1; a data-extent failure may be rerun once with the
    smoke's z-range / seed moved inside the crop. If it still fails: stop as **"tool cannot run here"**, no claim, the code findings go to
    the October package note.
  - The click page is built only after Stage 0a passes, so Sebastien spends no minute on a chain that cannot run.
- **Stage 0b (clicks):** the ≥ 3 valid clicks rule above; else ask Sebastien (one re-click or stop).
- **Stage 0c (CPU, seconds):** W ≥ 2 mm from the axis (STOP-CORE above) and the projection ≤ 8 h (STOP-BUDGET above).
- **Read-page controls:** the guard is the partsheet_tolerance picture both humans called not-rows blind (`cf.guard()`, the only one, FACTS 586/611);
  the w00 control and the 0009B calibration read rows on every earlier human page. No new control is introduced, so no pilot is needed
  (lesson 18); if `cf.guard()` returns None the page is not built (INCONCLUSIVE by Stage 0, lesson 20).
- **Critic's "chance of no answer"** (10-06, for the cross design) does not carry over; for this design: ~0.15 the chain does not run
  (Stage 0a), ~0.15 STOP-CORE or STOP-BUDGET, ~0.10 a rater invalid.

## The read (both humans, blind)

- **Page (per rater, own random order, seeds 20261071 Seb / 20261072 Chris):** L_level, L_blank, C_level (w00, COPY-IN's `ctrl_level.png`),
  C_blank, C_repeat (the same w00 picture again, ≥ 3 places apart), G_level (grower, description only), calib (FORMAT-20 0009B `f_05.png`),
  blank09 (`f_06.png`), guard. Same wording, template and answer options as handfix's read page (Rows / Strokes, no rows / Nothing).
  Key in the git-ignored `lf9_key.json`; answers `lf9_read_seb_ratings.json`, `lf9_read_chris_ratings.json` (git-ignored).
- **Rater validity (`lf9.py checks`):** VOID if the calibration is not rows or a picture is unanswered; UNINFORMATIVE if the w00 control or
  its repeat is not rows, a blank (C_blank, blank09) is rows, or the guard is rows. L_blank rows → that rater's lasagna read is "not
  interpretable".
- **Who:** Sebastien and Chris, each alone, one look per picture. Chris's page is parked `[for Chris]`. Sebastien clicked the centre, which
  is a global input, not a trace of W; the page hides which picture is which.

## Verdict (frozen, `lf9.py verdict`, selftest in job 1)

- **PASS:** both raters valid and both read L_level as rows.
- **KILL:** the coverage gate fails, or any valid rater (interpretable lasagna read) reads L_level as not rows. Scope: "lasagna shipped
  self-map seed fit from clicked centre rings, 0841 9.366 µm, S2 window, no correction".
- **INCONCLUSIVE:** anything else (a rater invalid while the other reads rows; L_blank rows; a Stage 0 stop; the tool cannot run here).
- G_level and every "vs P" number (render-to-P distances inside the display) are description only.

## Seeds, compute, kill date

- Seeds: page orders 20261071 / 20261072; no other randomness (the fit is deterministic up to GPU arithmetic; one fit, no seed sweep: this
  is a reading test of the shipped route, not an effect size).
- Compute: job 1 ≤ 1 GPU-h + ≤ 30 min of downloads (WSL env ~3 GB, click slices ~1-2 GB). Job 2: 1-8 GPU-h, known after the clicks
  (STOP-BUDGET), plus the shells and the full fit, which the smoke cannot time (lesson 16): **frozen wall-time cap 4 h for shells + fit
  together**; past it the job stops as engineering and Sebastien is asked (no claim). Job 3: minutes (canonical model on two surfaces).
- Human time: Sebastien ~10 min clicks + ~5 min reading; Chris ~5 min reading. Correction minutes: 0.
- **Kill date: 2026-10-16.** Not run by then → INCONCLUSIVE (not run), no claim.

## What each outcome changes

- **PASS:** the first "human minutes per readable cm²" number on 0841's regular scan: ~10 click-minutes for a 2.3 cm² readable field
  (≈ 4 min/cm², and the clicks serve every winding of the scroll). Lasagna's route becomes lane A's base surface for COPY-FIX-style
  correction tests, and a package (b) headline; caveat: both humans know W's text (depth_s022814 checks the band on unseen text).
- **KILL:** a clean failure-atlas entry for package (b) ("the organizers' shipped lasagna seed fit does not give a readable field on 0841 at
  0 correction minutes"); lane A's zero-minute arm closes; human correction (handfix) stays the main route.
- **INCONCLUSIVE:** no claim; the engineering notes (WSL needs, centre input, kernel ladder) go to the package note.
