> **Scrubbed public copy** (public name `snapping_refine`). The original was first committed to the authors' private repository at `63dee78dd` (2026-10-05T05:53:12Z). Timing: Run in the main session, not by the station loop, so no loop Judge checked its timing; the file states it was pushed before any agent saw a picture and before any refinement ran. Timestamps live in a private repository; ask the authors for a verification. Scrubbing removed mentions of non-public scrolls and local paths (paths into the authors' private repository read `[private path]` and do not resolve) and replaced internal item ids and test names with public slugs (unmapped internal ids read `[internal item]`); the scientific text is otherwise unchanged.

# Pre-registration: VISION-CHECK (can Claude vision agents judge P like Sebastien?) and snapping_refine (w00 refined at 2.4 µm on one crop)

- **Date and owner:** 2026-10-05 morning. Written in the main session, on Sebastien's request ("do these two and send me
  an email when you have the result"). Pushed before any agent sees a picture and before any refinement runs.

## Part A: VISION-CHECK

- **Question:** do Claude vision agents, shown exactly the pictures Sebastien rated on the w00_trusted_crosses page, give the same
  Yes / No? If they do, they could screen a mesh for him.
- **Items:** the 52 rated items of `[private path]` (48 crosses + 4 repeats).
  - Each item is one PNG: two 2.4 µm slices stacked, the green trace and the yellow ticks drawn exactly as on the page
    (1x).
  - Order and ids are re-randomised (seed 2026100510).
  - No worked examples are given with answers. The p448 example's description is given in words only.
- **Raters:** 3 independent general-purpose agents (Claude, default model).
  - Each gets the same written instructions as Sebastien's page and reads every image itself.
  - Each must not open any other file. The keys, ratings and features are never in their folder.
  - Each returns one line per item: Yes / No / Cant.
- **Scoring:** against Sebastien's 46 first-showing Yes / No answers. His "Can't tell" items and the repeats' second
  answers are left out, as in the w00_trusted_crosses fit.
  - **Per agent:** balanced accuracy (No = positive), agreement %, and its own repeat agreement.
  - **Majority of 3:** the same numbers. A "Cant" from an agent counts as no vote. A tie or no vote counts as "No" in a
    triage use (conservative), and is reported separately.
  - **Usable as a screen** if the majority's balanced accuracy ≥ 0.85 **and** it catches ≥ 90 % of Sebastien's No
    answers.
  - **Partial** if the balanced accuracy is 0.70-0.85.
  - **Not usable** if it is < 0.70.
  - For reference, the computer features reached 0.70 (w00_trusted_crosses fit).
- **Blinding:** the main session does not look at Sebastien's per-item answers until the agents have returned. Scoring
  is a script.

## Part B: snapping_refine

- **Question:** can w00 be refined on the 2.4 µm scan so that it sits on papyrus, without a human, over one dev crop?
  And where can it not?
- **Crop:** **h0**. It has the most off-papyrus P (w00_trusted_crosses: A median and the share > 0.3 the highest of the 7) and
  includes p448 and v581.
- **Method, fixed now:**
  1. **Start:** the 2.4 µm copy of w00 (`c1k1/mesh_P`) on the band's level-0 grid, inside h0 plus a 0.5 mm margin,
     densified ×2 (≈ 24 µm spacing).
  2. **Per vertex:**
     - sample the level-0 CT along the vertex normal over ±150 µm;
     - smooth with a Gaussian σ 1.5 voxels;
     - threshold at τ, the crop's Otsu as in w00_trusted_crosses;
     - find the papyrus runs;
     - target = the centre of the run nearest the current position, if it lies within 60 µm;
     - otherwise **no target**, weight 0, and the vertex is flagged.
     - Weight halves if a second run is within 15 µm of the same distance (ambiguous).
  3. **Solve** for an offset field d along the normal: minimise Σ w (d − target)² + λ Σ |Δd|² on the grid, with
     λ = 4, by conjugate gradient.
  4. Move the vertices, recompute the normals, and repeat **3 times**. The total move is capped at 120 µm per vertex.
  5. **Output:**
     - the refined mesh (git-ignored);
     - a **flag map**: vertices with no target in the last pass, or a total move > 90 µm;
     - counts.
- **Evaluation:** w00_trusted_crosses's A feature (no papyrus within 25 µm, 2 slices × 1.5 mm) at h0's auditable crosses,
  before vs after. The refined mesh is evaluated at the same cross centres, mapped by grid index.
  - **Reported:**
    - median A;
    - the share of crosses with A > 0.3;
    - the share of flagged area;
    - median and p90 of the total move.
  - **"Worth continuing"** if the share with A > 0.3 drops by ≥ half **and** the flagged area is ≤ 20 %.
  - **Caveat, stated now:** A is the computer feature that only partly agrees with Sebastien (balanced accuracy 0.70).
    A good A score is necessary, not sufficient. The real check is Sebastien's (or Chris's) eyes on a fresh blind
    sample, and a read.
- **Pictures:** 12 h0 crosses, before | after side by side, seeded, chosen from **unrated** crosses (≥ 1 mm from every
  calibration and HUMAN-* site). 4 per third of the "before" A.
- **Not claimed:** refined P is not a new key until a blind human check passes. The fold cut-across cases (v581
  style) are expected to stay flagged. Fixing them needs the fork step (human or other).
