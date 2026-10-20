> **Scrubbed public copy** (public name `fullhop_w`). The original was first committed to the authors' private repository at `dcaf4984c` (2026-10-08T13:09:08Z). Timing: Committed before the run's first output (its Judge's check). Timestamps live in a private repository; ask the authors for a verification. Scrubbing removed mentions of non-public scrolls and local paths (paths into the authors' private repository read `[private path]` and do not resolve) and replaced internal item ids and test names with public slugs (unmapped internal ids read `[internal item]`); the scientific text is otherwise unchanged.

# Pre-registration: fullhop_w. Does W's ~30 % damage dose still read rows for BOTH humans when every damaged patch is moved onto a real neighbouring sheet, out of the 2.4 µm reader's reach?

- **Date:** 2026-10-08 (CDT), pushed before any deep surface, render, map or tile exists. Owner: Sebastien's side (station
  loop item `fullhop_w`; Sebastien chose "A) go ahead now" on 2026-10-08 07:30). Public PHerc0841
  data only. Feeds package (b) (readable-surface budget), row 2: "~30 % wrong sheet still reads".
- **Why:** partsheet_tolerance (`preregs/partsheet_tolerance.md`, scored by partsheet_tolerance scoring) has both humans calling the L70 and C70
  pictures "rows" (30 % of vertices hopped). The Critic's CPU check (item file, Critic §1;
  `[private path]`) found those hops mostly moved
  less than a sheet: in pixels moved > 50 µm the 2.4 µm reader still shows the true text (label AUC 0.65 / 0.79 vs blank
  ~0.5; 32-39 % of moved vertices ≤ 100 µm). So package (b) must already say "~30 % displaced 50-250 µm" (free wording fix,
  not part of this test). This test asks the stronger question: with every damaged patch truly on another sheet, do both
  humans still see rows?
- **Truth rule:** the verdict is a blind two-human read. Ink labels only gate the DOSE (Stage 0b: "is the true text gone
  from the moved pixels?", a construction property). w00 (P_W) is the base surface, not a key; all doses are "as built from
  w00". Agent readers are not used.
- **Disclosed before this file (construction-only numbers, none is a reading):** the Critic's Stage 0a above, the Critic's
  dark-hop check (`critic_darkhop_out.json`), and three Planner checks in the same folder: `planner_taper_out_f120.json` /
  `_f140.json` (smoothing taper), `planner_ctblock_out.json` + `planner_ctstats_out.json` (9.6 µm band CT at P),
  `planner_dark24_out.json` (2.4 µm render CT at P). They only shaped the design below.

## Data and why nothing can leak

- **Base:** `[private path]` (w00 over the labelled window W), outward normal by TOL-20's rule (`[private path]`).
- **Sheet map for the hop law:** public m7 (`...surface-m7-L2-th0.2.zarr`, band level 2 = 9.612 µm), TOL-20's lookup.
- **Masks (unchanged from the rated pictures):** TOL-20 field `default_rng(20261002)`, σ 10.4 vertices; TOL-20b field
  `default_rng(20261003)`, σ 30 vertices. New field for the holes guard only: `default_rng(20261008)`, σ 30.
- **Pictures for the humans:** new tiles in `[private path]<id>/tiles/` (git-ignored: item `.gitignore`); manifest
  `fh_key.json`, page key `fh_page_key.json`, Stage 0b numbers `fh_s0b_f<FLOOR>_result.json` and the score
  `fh_score_result.json` are git-ignored by the repo rules (`*key*.json`, `*_result.json`). Only PASS / FAIL lines and
  construction numbers (masks, off-sheet shares, coverage) go into the item file before both humans have rated.
- Nobody traced or picked these arms by hand; both raters are equally blind to the new pictures (each has seen L100 and the
  0009B calibration pair before; that is intended: L100 is the seen readable control).

## Arms

- **Hop law (the ONE change from TOL-20 / TOL-20b):** each hop vertex moves outward along P_W's normal to the centre of the
  nearest public-m7 run lying **140-250 µm** outward (FLOOR = 140); if none, a constant **150 µm**. Then TOL-20's smoothing:
  displacement field × hop mask, Gaussian σ = 1 vertex. Everything else as TOL-20: same base, same masks, same readout.
- **Changes from the Critic's fixed design, with reasons (made before any deep surface exists):**
  1. **Floor 140 µm, not 120.** The Critic's floor "74.5 + 22 + margin" read the −22 offset as µm. It is −22 LAYERS =
     −52.9 µm (`tr.py`: `s0 = c − 31 + o`, ±5 layers = ±12.0 µm). A −22 window reaches 74.5 + 52.9 ≈ 127 µm back toward P,
     and C70's rated tile came from −22. Measured cost (planner_taper, m7-only): run found at 0.62 of vertices (0.72 at 120);
     moved vertices ≤ 130 µm 10 % / 4 % (L70d / C70d) vs 12 % / 6 % at 120; median 164 µm.
  2. **The band-CT run fallback is dropped.** A CT point threshold cannot tell sheet from gap in this window: at 9.6 µm the
     block Otsu (τ 82) calls P's own vertices dark 0.40, P ± 75 µm 0.45-0.46, P + 150 µm 0.48; at 2.4 µm (render, τ 84)
     P 0.41 vs depths ±36-108 µm 0.42-0.47. A CT-run lookup would therefore pick near-random depths. Vertices with no m7 run
     in 140-250 µm take the constant 150 µm (the item's original law).
  3. **DARK-HOPS is measured with m7 relative to P, not with a CT threshold of 0.30** (reason 2: by CT, the true sheet
     itself would already be "dark" > 0.30). See Stage 0d.
- **Primary pictures:** **L70d** (TOL-20 field, top 30 %), **C70d** (TOL-20b field, top 30 %).
- **Guards:** **L40d** (TOL-20 field, top 60 %, same law; nested: L70d's hops ⊂ L40d's) and **H50n** (50 % holes, TOL-HOLES
  law on the new field, fixed +0). On W, both humans called H50 "not rows", and L55 split.
- **Controls:** **L100** (the rated partsheet_tolerance L100 level tile, byte copy, md5), the wrong-order (fwd) blanks of L70d and C70d,
  and the FORMAT-20 0009B calibration pair (`[private path]` calib, `f_06.png` its blank).
- **Readout (identical to TOL-20):** render 161 layers → central 109 (`sv.render(..., C.BAND, 0, 2.403, 2.403, 161)`), canonical
  2.4 µm model (`tr._model` / `tr._infer`, TOL-RERENDER's reproduced path) at −22 / +0 / +22 layers, rev = level, fwd = blank;
  each tile's offset by the p99 depth-pick rule (highest 99th percentile inside the valid mask), level and blank picked separately as
  TOL-20 `tiles()`; H50n fixed +0 (TOL-HOLES). Tile = S2 window rows 11:8331, cols 12:4889, 800 px, bilinear. "C70's rated tile
  came from −22, kept" is read as: the same p99 rule for every deep map; whether C70d's pick lands on −22 is reported.

## Stage 0 (sanity checks first, smallest decisive set first; each exits 78)

- **0c (CPU, ~1 min): tile code.** Re-tile the rated L100 / L70 / C70 level and blank tiles from their saved maps. **Bar: 6 / 6
  pixel-identical** (TOL-RERENDER passed 16 / 16 on the same code). Fallback: none (VOID, plumbing).
- **0m (CPU, with the surfaces): masks.** The rated parent's moved (> 50 µm) vertices lie inside the new hop mask (1-vertex
  dilation) for L70d, C70d, L40d. **Bar: ≥ 0.99 each.** Fallback: none (VOID, plumbing).
- **0d (CPU, before any render or GPU): DARK-HOPS.** off-sheet(v) = no public-m7 foreground at the nearest level-2 voxel or
  ±1 voxel (9.6 µm) along the normal. **Bar, L70d and C70d each: off-sheet share of moved (> 50 µm) vertices at their final
  smoothed positions ≤ off-sheet share of the SAME vertices on P + 0.10.** (The true sheet, which reads, sets the baseline; m7
  has holes and P sits at a face, so the baseline is not 0.) Fail → **DARK-HOPS**: stop, UNDECIDED, no GPU, no page, no
  human minute. Reported: P's own share, the rated parents' share, L40d's share.
- **Coverage (CPU, after the renders):** valid fraction of each deep render inside the S2 window ≥ L100's − 0.01 and the same
  grid shape as L100 (the item marked band coverage at P + 250 µm UNVERIFIED). Fallback: none (stop, report).
- **0b (after the 12 primary maps, ~35 min GPU): hand-over check at the PICKED offset.** On R5's pixel set (`ws.pix_P`), for
  L70d and C70d separately, at the offset the p99 rule picks for the level tile:
  - **hop pixels** (moved > 50 µm): label AUC ≤ **min(blank + 0.05, 0.62)**, blank = the same deep surface's fwd map at the
    SAME offset on the same pixels. (The absolute 0.62 stops a lenient blank: the shallow C70's −22 blank was 0.62 on its
    hop pixels; FACTS W blanks 0.54-0.58.)
  - **unmoved pixels** (≤ 5 µm in both the deep surface and its rated parent): label AUC ≥ the rated parent's AUC at the same
    offset − 0.01 (the deep build must not disturb the unmoved part more than the shallow one did; the item's "within 0.01
    of L100" was replaced because the RATED shallow L70 already misses it: 0.9585 vs 0.9698).
  - Fail → exit 78. **Pre-written fallback, once:** the Runner re-runs `job.sh` with `FLOOR=170` (run law 170-250 µm, constant
    200 µm; new folder `f170/`, nothing overwritten; all Stage 0 checks repeat). Fail again → stop as **INCONCLUSIVE
    ("reader still reaches")**, no page.
  - Reported descriptively (git-ignored): AUC by band 50-120 / 120-150 / > 150 µm, L100 at the same offset, all pixels.
- **Chance of no answer:** about 3 in 10 overall (Critic), of which Stage 0 about 1 in 10 (DARK-HOPS unlikely: m7-law hops sit
  on run centres; 0b may need the 170 fallback because of smoothing taper at hop borders, 4-10 % of moved vertices ≤ 130 µm).

## Blind page (Runner step, NOT in job.sh; after Chris's handfix pages)

- **9 pictures:** L70d, C70d, L40d, H50n level tiles; L70d and C70d blanks; L100 level; 0009B calib + its blank. Opaque ids
  `q01..`, one shuffle `default_rng(20261008)`, JPEG q90, page < 1 MB (`fh.py page`), the partsheet_tolerance page template and wording
  (20 × 12 mm; Rows / letters, Strokes no rows, Nothing; the question names no control). Answers saved as
  `ratings/seb/fullhop_ratings.json` and `ratings/partner/fullhop_ratings.json` (sha256 recorded by the scorer).
- **Shared sitting with fullhop_s022814 (Sebastien's choice A):** if fullhop_s022814's pictures exist when this page is built, the Runner passes
  them to `fh.py page <extra.json>`: one page, one shuffle, the shared calibration pair. Each item is scored ONLY on its own
  pictures by its own pre-registration; this scorer ignores fullhop_s022814's pictures. Not waiting for fullhop_s022814 if it is not ready.
- Both humans rate independently and do not compare notes; Chris rates first if possible (Sebastien says "rows" on almost
  every surface: lesson 20).

## Outcome rule (`fh.py score`, self-tested on 8 synthetic cases before anything runs)

- **Valid rater:** every own picture answered; calib "rows"; 0009B blank, L70d blank and C70d blank each not "rows"; L100 "rows".
- **UNDECIDED** if < 2 valid raters.
- **FULL-HOP-FAILS:** ≥ 1 valid rater calls L70d or C70d not "rows". Row 2 becomes: "rows with ~30 % part-sheet displacement
  (as built from w00); with ~30 % full one-sheet hops, not rows for ≥ 1 of 2 blind raters".
- **FULL-HOP-HOLDS:** both valid raters call "rows" on both L70d and C70d, AND ≥ 1 valid rater calls L40d or H50n not "rows".
  The ~70 % line then stands with truly wrong patches (one window, one picture per level). Written as "rows are visible",
  not "the right text is": the neighbouring sheets carry their own text.
- **UNDECIDED (lenient page):** both say rows on both primaries and nobody calls a guard not rows.
- **DARK-HOPS / INCONCLUSIVE "reader still reaches" / VOID:** by Stage 0 above (no page).
- n = 2 raters, one picture per level, one window: a description of this window, as partsheet_tolerance scoring.

## Compute and dates

- CPU: surfaces ~2 min; 4 renders of 161 layers (TOL-20 timing; threads capped at 8). GPU: 12 primary + 6 L40d + 2 H50n maps
  ≈ 20 × 2.75 min ≈ 1 h; with the 170 fallback ≈ +50 min. `gpu_hours` 1.0, cap 2.5; claim in the loop's job wrapper. Disk ~25 GB
  of renders and maps under the item folder (git-ignored). Never writes in `[private path]`, `tol20b`, `tolholes` (asserted).
- Seeds: fields 20261002 / 20261003 (rated), 20261008 (H50n), page shuffle 20261008. Inference deterministic.
- Human time: Sebastien ~5 min, Chris ~5 min (shared sitting with fullhop_s022814 ~8 min), only if Stage 0 passes.
- Kill date: 2026-10-24 (package (b) freezes ~Oct 25). Job: `[private path]`
  (last line `FULLHOP_PICTURES_DONE`).

## What each outcome changes

- **FULL-HOP-FAILS:** package (b) row 2 is rewritten as above; the hand-correction budget (human minutes per readable cm²)
  must count every one-sheet hop, not only the big ones.
- **FULL-HOP-HOLDS:** row 2 keeps "~70 % right sheet reads" with truly wrong patches, for this window.
- **UNDECIDED / DARK-HOPS / reader still reaches:** row 2 keeps only the free wording fix ("~30 % displaced 50-250 µm; the reader
  still sees part of the true text there"); no stronger claim.
