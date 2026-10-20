> **Scrubbed public copy** (public name `snapping_sheetline`). The original was first committed to the authors' private repository at `411fe0f87` (2026-10-05T19:30:19Z). Later commits to the same file: `9b9bb5409` (2026-10-05T21:29:31Z); `2972ebcdf` (2026-10-05T21:54:50Z). Timing: Run in the main session, not by the station loop, so no loop Judge checked its timing; the file states it was pushed before any picture or page, and that amendments 1-2 came before any page or picture was seen. Timestamps live in a private repository; ask the authors for a verification. Scrubbing removed mentions of non-public scrolls and local paths (paths into the authors' private repository read `[private path]` and do not resolve) and replaced internal item ids and test names with public slugs (unmapped internal ids read `[internal item]`); the scientific text is otherwise unchanged.

# Pre-registration: snapping_sheetline, Sebastien's sheet-scale centre line, rated blind against w00 and snapping_refine (PHerc0841 dev crop h2)

- **Date and owner:** 2026-10-05 evening. Sebastien: "Go ahead". Pushed before any h2 surface, picture or page is
  made.
- **Background:**
  - `preregs/snapping_midline.md`: on h0, layer-scale snapping_midline 8/14, snapping_refine 9/14, w00 11/14.
  - `[private path]` amendments 2-4: sheet scale fixed with Sebastien.
- **Framing, stated before any result:**
  - The fork split never made a correct "two sheets" call on fresh joins (fork test 3 passed 10/12 only through
    "same sheet" calls).
  - **The split is therefore not used.** snapping_sheetline is the sheet-scale centre line on its own.
  - What is tested is whether centre lines at Sebastien's sheet scale make a better surface than w00.

## The surfaces (crop h2, never used in a rated test)

- **w00:** the 2.4 µm copy, as before.
- **snapping_refine:** `refine24.py` unchanged, run on h2.
- **snapping_sheetline:** `midline3.py` with only the centre lines changed. The centre-line settings are those of forksplit
  amendments 2-4.
  - **Per z-slice:**
    - Gaussian σ 1, τ = h2's w00_trusted_crosses threshold;
    - remove objects < 64 px;
    - closing with a disk of radius 4 px;
    - fill holes < 400 px, plus every enclosed hole ≤ 110 µm wide;
    - skeletonize;
    - prune 25;
    - segments = the skeleton minus the junctions.
  - **No "merged" exclusion:** at sheet scale every band counts as one sheet. Lenses wider than 110 µm stay open, as two
    sheets.
  - **The rest is snapping_midline unchanged:**
    - every 4th z-slice;
    - w00's trace votes within 40 µm;
    - a segment needs ≥ 3 votes;
    - targets lie along each vertex normal within 12 µm laterally and 60 µm along;
    - snapping_refine's solver (λ 4, 3 passes, 120 µm cap, flags).
- **Sanity sheet first:** 12 unrated h2 crosses × 3 arms. Stop rule as before: if the target share is < 50 % of the
  area, or the lines run in empty space, stop and report.

## The blind rating

- **The design of `preregs/snapping_midline.md`, on h2:**
  - **The fresh pool:** auditable h2 crosses ≥ 1 mm from every departure, every HUMAN-* / TWO-LINE / w00_trusted_crosses
    calibration site, the sanity crosses and each other.
  - **The draw:** up to 7 per third of w00's A (seed 2026100600). Each cross is shown in all 3 arms with the same
    planes and style, in a Latin square, plus 4 repeats.
- **Scoring:**
  - paired Yes per cross with exact McNemar tests;
  - **snapping_sheetline vs w00** is the primary claim;
  - snapping_sheetline vs snapping_refine and snapping_refine vs w00 are secondary;
  - "better" = p < 0.05 and a higher Yes rate;
  - A (the off-papyrus measure) is reported only as description.
- **The size is whatever the pool allows,** up to 21 crosses. With about 14, only a very large difference can show.

## Amendment 1 (stop rule triggered; Sebastien "yes try it", before any page or picture)

- **The first snapping_sheetline build on h2 stopped by the rule:**
  - target share 0.46 < 0.50, so 54 % of the area is flagged;
  - the sheet-scale band width median is **96 µm**, close to Sebastien's 100 µm;
  - only 44 % of w00's trace points voted within 40 µm.
- **The cause:** w00 sits near a sheet's face, while the sheet-scale centre line runs mid-sheet, ~50 µm deeper. The 40 µm
  vote radius and the 60 µm snap limit were sized for ~30 µm layer lines.
- **Change, snapping_sheetline only:**
  - the vote radius goes to **75 µm** (half a ~100 µm sheet + 25 µm; the neighbouring sheet's centre is ≥ ~150 µm
    away);
  - the snap limit along the normal goes to **90 µm**.
  - Everything else, including the stop rule, is unchanged.

## Amendment 2 (before Sebastien sees any h2 picture): exclude only what he has seen

- **The problem:** the page build on h2 found only **6 crosses**. With the full exclusion list (every grower departure,
  the TWO-LINE main items), h2's fresh pool is too small.
- **What exactly is excluded:** the departure and TWO-LINE-main exclusions protected TWO-LINE's blinding, and TWO-LINE
  is shelved with its main page never shown.
  - **Now excluded (≥ 1 mm):** only sites Sebastien has seen. That means HUMAN-PICK, HUMAN-SLAB, the TWO-LINE pilot
    items, the w00_trusted_crosses calibration crosses and the h2 sanity crosses.
  - **The pool:** 130 crosses, about 16 that are ≥ 1 mm apart.
- **Unchanged:** draw up to 7 per third of w00's A (seed 2026100600), the Latin square, 4 repeats, scoring.
- **Noted:** crosses near grower departures can now be drawn. The draw is still stratified by w00's A, the same for
  all arms.
