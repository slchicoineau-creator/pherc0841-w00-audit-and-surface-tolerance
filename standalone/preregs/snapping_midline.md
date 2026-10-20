> **Scrubbed public copy** (public name `snapping_midline`). The original was first committed to the authors' private repository at `0b5692c1d` (2026-10-05T12:55:45Z). Later commits to the same file: `1c150ca1f` (2026-10-05T13:14:29Z). Timing: Run in the main session, not by the station loop, so no loop Judge checked its timing; amendment 1 (page size) states it came before any rating. Timestamps live in a private repository; ask the authors for a verification. Scrubbing removed mentions of non-public scrolls and local paths (paths into the authors' private repository read `[private path]` and do not resolve) and replaced internal item ids and test names with public slugs (unmapped internal ids read `[internal item]`); the scientific text is otherwise unchanged.

# Pre-registration: snapping_midline (Sebastien's centre-line idea) and a 3-arm blind rating: w00 copy vs snapping_refine vs snapping_midline (PHerc0841 dev crop h0)

- **Date and owner:** 2026-10-05. Written in the main session after Sebastien's "yeah go for it" (steps 1-3 of the
  snapping_midline prototype, then a blind side-by-side rating). Pushed before the snapping_midline surface is built and before any
  rating page exists.
- **Prototype already seen (exploratory, 3 z-slices of h0, `midline.py`):**
  - Centre lines follow separated sheets.
  - Fused sheets give a branching web, flagged by a band thickness > 1.6 × the median (about 30 µm). That is ~23 %
    of the centre-line length.
  - w00 sits a median 14 µm from a centre line.

## Part 1: the snapping_midline surface

- **The design rule:** snapping_midline = snapping_refine (`preregs/snapping_refine.md` part B) with **only the
  target changed**.
  - snapping_refine snaps each vertex to the centre of the nearest papyrus run along its normal, vertex by vertex.
  - snapping_midline snaps to the **one connected centre-line segment chosen for w00's sheet** in each z-slice.
  - The test is whether following one connected segment removes REFINE's wiggles in packed bundles.
- **Steps:**
  1. **Slices:** the band's level-0 z-slices through h0, every 4th slice (9.6 µm apart). Each slice is cut to the
     box of w00's trace in that slice ± 0.6 mm.
  2. **Per slice:**
     - Gaussian σ 1 voxel, then threshold at h0's τ (84, as in w00_trusted_crosses);
     - remove objects < 64 px and fill holes < 64 px;
     - skeletonize;
     - **prune spurs**: remove end points 12 times, which takes off branches ≤ ~29 µm;
     - **split into segments** by removing junction pixels (≥ 3 skeleton neighbours);
     - a segment is **merged** if its median band thickness (2 × the distance transform) > 1.6 × the slice median.
  3. **Choosing w00's segment:** each w00 trace point in the slice votes for its nearest segment pixel within 40 µm.
     A segment is **chosen** if it gets ≥ 3 votes and is not merged.
  4. **Targets:** for each moving vertex (snapping_refine's ×2 grid, h0 + 0.5 mm):
     - consider chosen points within 70 µm;
     - each has an offset along the vertex normal t = (c − p)·n and a lateral distance |c − p − t n|;
     - the target is the t of the point with the smallest lateral distance, if that is ≤ 12 µm and |t| ≤ 60 µm;
     - otherwise no target, weight 0.
     - There is no ambiguity weight (the segment choice replaces it).
  5. **The rest is snapping_refine unchanged:** λ = 4, conjugate gradient, 3 passes (the chosen points stay fixed; the
     targets are recomputed each pass), 120 µm cap, flags (no target in the last pass, or a move > 90 µm).
- **Also reported:** the share of h0's w00 area where the sheet lies within 30° of the z-plane (|n_z| > 0.866), where
  z-slices are poor. Flagged, never dropped.
- **Sanity sheet first:** 12 unrated h0 crosses, w00 | snapping_refine | snapping_midline side by side, made before the page.
  - If snapping_midline obviously fails, for example no target on most of the area or lines in empty space, **stop and
    report**. No rating page is built.

## Part 2: the 3-arm blind rating (Sebastien)

- **The fresh pool:** auditable h0 crosses ≥ 1 mm from every departure event, HUMAN-PICK / HUMAN-SLAB site (these
  include KEY-FIX), TWO-LINE pilot or main item, w00_trusted_crosses calibration cross and snapping_refine picture cross. They are
  also ≥ 1 mm from each other.
- **Drawn without reference to any arm's flags or gaps:** 21 crosses, 7 from each third of w00's A (seed 2026100540).
- **What the rater sees:**
  - each cross in all 3 arms, with the same two view planes (w00's frame at the cross), the same trace code, the same
    line style and contrast;
  - each arm's final surface as produced: the smoothed fill where it had no target, the same rule for all;
  - no arm names.
- **Order:**
  - Latin square: 3 blocks of 21. Each cross appears once per block, and the arm order rotates across blocks.
  - The order inside each block is shuffled.
  - 4 repeats placed ≥ 10 items after the first showing.
  - **67 items**, the same question and buttons as w00_trusted_crosses. Measured pace 38 s per item, so **about 40 minutes**,
    which can be split into sittings.
- **Scoring:**
  - Yes = stays on one sheet.
  - **Primary:** paired Yes per cross, with exact McNemar tests.
    1. **snapping_midline vs w00**, the primary claim;
    2. snapping_refine vs w00;
    3. snapping_midline vs snapping_refine.
  - "Better" needs p < 0.05 **and** a higher Yes rate. "Can't tell" pairs are left out.
  - The flagged share inside each rated window, per arm, is reported.
  - **Power, said plainly:** with 21 crosses only a large improvement can show, roughly ≥ 6 more Yes than No flips.
    A null result means "not large", not "none".
- **A (the off-papyrus measure)** is reported only as description: both refined arms are built to pass it.
- **Outputs:**
  - Counts: `[private path]`.
  - Git-ignored: the page, key and ratings in `[private path]`.

## Amendment 1 (before any rating): 14 crosses, not 21

- **What happened:** after the exclusions, the fresh h0 pool has only 89 crosses (30 / 28 / 31 per third of w00's A).
  With the ≥ 1 mm spacing, the seeded draw found **14 crosses** (7 / 3 / 4 per third), not 21.
- **What is kept:** the 1 mm spacing, so that rated windows do not overlap. Everything else is unchanged.
- **The page:** 14 crosses × 3 arms + 4 repeats = **46 items**, about 30 minutes.
- **Power is lower:** only a very large difference can reach p < 0.05, roughly ≥ 5 more Yes than No flips with no
  opposite flips.
- **snapping_midline build, recorded before the page:**
  - target share 0.53, so **47 % of the area is flagged** and shows the smoothed fill there;
  - conjugate gradient hit 2000 iterations in all 3 passes;
  - median move 13 µm, p90 46 µm;
  - the sheet lies within 30° of the z-plane on 0.1 % of the area.
  - The sanity sheet (`midline3/sanity_*.png`, local) showed no obvious failure, so the page was built.
