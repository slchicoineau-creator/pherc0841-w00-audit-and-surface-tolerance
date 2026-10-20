> **Scrubbed public copy** (public name `w00_native_scan`). The original was first committed to the authors' private repository at `bc617bb5a` (2026-10-05T05:05:03Z). Timing: Run in the main session, not by the station loop, so no loop Judge checked its timing; the file states it was pushed before any measurement on the native scan. Timestamps live in a private repository; ask the authors for a verification. Scrubbing removed mentions of non-public scrolls and local paths (paths into the authors' private repository read `[private path]` and do not resolve) and replaced internal item ids and test names with public slugs (unmapped internal ids read `[internal item]`); the scientific text is otherwise unchanged.

# Pre-registration: w00_native_scan, is P off its sheet because of the scan-to-scan transfer, or because of the mesh itself?

- **Date and owner:** 2026-10-05 ~00:15. Written in the main session, approved by Sebastien before he went to bed ("yes
  let's do that"). Pushed before any measurement on the native scan.
- **Why:**
  - Sebastien's blind ratings (prereg `preregs/w00_trusted_crosses.md`, gate FAIL) show P = w00 on the 2.4 µm scan leaving
    its sheet in most 1.5 mm stretches.
  - w00 was grown on the **9.366 µm scan** (`20250821151531`; `mesh/intermediate/tifxyz_original/meta.json`, source
    `vc_grow_seg_from_seed`).
  - The copy we use (`-on-20260319124803-2.403um`, a scan of 21 Jul 2025) is a transferred copy.
  - The organizers say these transforms "haven't gotten lots of scrutiny" and that the 2.4 to 9.4 µm transform
    "could be much improved" (villa#1912, jrudolph, 2026-09-28).
- **Measured before this prereg (geometry only, no CT):**
  - The native mesh has 211 × 238 vertices at **187 µm** spacing. The copy has 823 × 928 at 48 µm.
  - The copy = one affine of the edge-aligned bilinear upsample of the native grid. Residual median 13.9 µm, p90
    39.9 µm, p99 78 µm. Scale 1.0044 / 1.0033 / 1.0008.
  - So the copy's fine geometry is no better than the 187 µm native grid.
- **The two candidate causes:**
  - **T (transfer):** w00 sits on its sheet in its own scan, and the transfer moves it off.
  - **G (mesh grid):** w00's 187 µm grid cannot follow tight bends and folds, so it cuts across gaps even in its own
    scan.

## Measurement (computer only, CT only)

- **Sites:** the 6 553 auditable crosses of the w00_trusted_crosses audit (0.25 mm grid of P in the 7 dev crops).
  - Each cross maps to the native mesh by grid parameter: copy index → native index × (210/822, 237/927), the
    edge-aligned map above.
- **Copy arm:**
  - The copy (densified ×5) on **band level 2** of the 2.4 µm scan (9.612 µm voxels), the voxel coordinates our dev
    crops use: L2 = (L0 − 1.5) / 4.
- **Native arm:**
  - The native mesh (densified ×20, ~9.4 µm spacing) on the **native 9.366 µm scan**, level 0.
  - Both arms are at about the same voxel size, so resolution does not favour either.
- **Per cross, in each arm:**
  - Two slices along the two mesh-grid directions, both containing the mesh normal averaged over ±0.125 mm.
  - The trace is the median offset per 0.02 mm bin of the mesh points within ±0.75 voxel of the slice. The window is
    |s| ≤ 0.75 mm.
  - **A25 = the share of trace points with no voxel ≥ τ within 25 µm along the normal.** τ = per-scan Otsu on 200 000
    seeded voxels within 0.3 mm of the mesh. This is the w00_trusted_crosses feature A, at ~9.5 µm.
  - **Sensitivity copies:** the same mesh shifted +75 µm and −75 µm along its normal.
- **Bend measure (secondary):** the angle between native-grid vertex normals two vertices apart (374 µm), at the
  native vertex nearest each cross.

## Rules (fixed now)

- **Sensitivity gate:** in each arm, the median A25 must exceed the unshifted median for both the +75 µm and −75 µm
  shifts. Otherwise the arm's metric is blind at this resolution → INCONCLUSIVE.
- **The paired difference:** D = A25(copy) − A25(native) per cross, over the crosses auditable in both arms.
- **Verdicts:**
  - **T is a major cause** if:
    - median D ≥ 0.05;
    - the sign test gives p < 0.001;
    - the native share of crosses with A25 > 0.3 is ≤ half the copy's share.
  - **G is the main cause** if:
    - |median D| < 0.03;
    - the native share with A25 > 0.3 is ≥ 0.75 × the copy's share.
  - **MIXED** otherwise. Both arms are reported in full.
- **Secondary, reported:** the Spearman correlation of native A25 with the bend measure. G predicts a positive
  correlation.
- **Look by eye:** 12 crosses are shown side by side (native vs copy), seeded: 4 from each third of copy A25.
  - The pictures are made after the numbers are frozen, for Sebastien to look at in the morning.
  - They are not scored, and they change no verdict.
- **Outputs:**
  - Counts: `[private path]`.
  - Pictures and caches: `[private path]`, git-ignored where large.
