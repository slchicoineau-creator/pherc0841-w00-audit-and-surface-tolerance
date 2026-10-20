> **Scrubbed public copy** (public name `reader_phase`). The original was first committed to the authors' private repository at `67882c2e0` (2026-10-09T16:24:24Z). Later commits to the same file: `1c0b048c8` (2026-10-09T16:29:09Z). Timing: Original and amendment both pushed before the first output (its Judge's check). Timestamps live in a private repository; ask the authors for a verification. Scrubbing removed mentions of non-public scrolls and local paths (paths into the authors' private repository read `[private path]` and do not resolve) and replaced internal item ids and test names with public slugs (unmapped internal ids read `[internal item]`); the scientific text is otherwise unchanged.

# Pre-registration: reader_phase, with BOTH readers' tiles shifted, what is the Hecate 9.6 / Hecate 2.4 shape ratio on w00, and is its class phase-stable? (PHerc0841, known text)

- **Date and owner:** 2026-10-09, Sebastien's side (station loop item `reader_phase`, moved from lane B
  [internal item] at Sebastien's request; it is the phase-symmetric amendment that SOR-PHASE's Judge required before the parked
  SOR-STRIP `[internal item]` may resume, and it replaces that item). Pushed before any new reader map exists. Public data only.
- **Why:** package (b) row 7 (`submission/READABLE_SURFACE_BUDGET_OUTLINE.md:24`) quotes the coarse reader's share of the fine
  reader's letter detail (SURFACE-OR-READER 0.508, READER-LIMITED) and is marked "not ready" until a phase-symmetric re-test.
  SOR-PHASE (`[private path]`, PHASE-FRAGILE) moved only Hecate 9.6's tile phase (4 diagonal phases:
  0.533 / 0.468 / 0.410 / 0.400). Hecate 2.4 also tiles, and it picks the good windows; its phase was never moved.
- **Truth rule:** no position of the team mesh P is used. The reference is the team ink map; the registration uses CT only;
  no raters. Human time: none.

## Regions and data (all on disk; nothing held out can leak)

- **R** = 2.403 µm SV rows 10208-12992 × cols 9280-15776 (SoR's region; the 0.508 and SOR-PHASE were measured here, so R is
  post-hoc informed). **R2** = rows 1698-10208 × cols 10392-15268 (disjoint from R). Both are fully labelled.
- **R2 has never had a Hecate 2.4 map:** SOR-STRIP stopped at its check before R2's T runs (`sorstrip_checkR.json`). R2's
  plumbing (0f) and timing (0g) are first-ever runs.
- 2.4 µm input: `[private path]` (109 layers; rows 0-13000, cols 8000-17000). 9.366 µm input:
  `[private path]`, cropped by `get.py`'s rule plus an 82 px margin and zoomed 9.366/9.6 once per region (`pad80`,
  80 px at 9.6 µm). Team map: `[private path]`. Frozen CT shifts (`[private path][internal item]/sorstrip_reg.json`):
  R (−8, −8) check_r 0.951; R2 (−6, −9) check_r 0.949.
- Known limits (unchanged from SOR-STRIP): Hecate 9.6 was probably distilled on 0841 (optimistic H9); the team map comes from
  the same 2.4 µm scan as T (favours T). So READER-LIMITED stays conservative.

## Arms (tile phase = (−leading margin) mod stride; hecate tiles start at array pixel 0)

- **T (Hecate 2.4):** leading margins (my, mx) ∈ {0, 32, 64, 96}² px at 2.403 µm (stride 128; multiples of `xy_stride` 4):
  input = `sv24[:, y0 − my : y1, x0 − mx : x1]` (real context, never zero padding; the end tile stays end-anchored). The map is
  cropped back at native 2.403 µm (`[my:, mx:]`) and then zoomed to 9.6 µm as SoR. Command = the one that made `T.png`
  (Critic finding 8): `hecate.py --checkpoint hecate_2.4um.pth --spacing-um 2.4 --stride 128 --precision bf16` (default
  batch 1). Phase (0, 0) runs on `R_sv24.npy` / `R2_sv24.npy` directly.
- **H9 (Hecate 9.6):** leading margins (my, mx) ∈ {40, 48, 56, 64}² px at 9.6 µm (stride 32 → phases 24 / 16 / 8 / 0), trailing
  margin 40, all 16 trimmed from the one `pad80` volume of the region. Flags as SOR-STRIP / SOR-PHASE (bf16, default stride,
  batch 4, spacing 9.6). Both phase steps are 77 µm.
- **Controls:** positive = T vs Team; blank = T_rev (R: saved `T_rev.png`; R2: new run at phase (0, 0)) and H9_rev (new run on
  the (40, 40) input, both regions).
- 16 T × 16 H9 = **256 pairs per region**.

## Measure (unchanged from SURFACE-OR-READER / SOR-STRIP, scorer bodies copied verbatim from `sorstrip.py`)

- 9.6 µm grid; DoG σ 1.5 − σ 12; 128 px windows, step 64; ink window = ≥ 5 % of Team above Team's Otsu threshold; r_T, r_H9
  per ink window in DoG space. Good windows: r_T ≥ 0.5 and in the top third of r_T, **re-chosen for each T phase** (fewer
  than 10 → that T phase is VOID). Statistic: median r_H9 / r_T over good windows.
- **Two frozen conventions (written before any data, so the Judge can check them):**
  1. `at()` takes each arm's own leading margins (my, mx) instead of SOR-STRIP's fixed 40 (needed for asymmetric margins).
  2. H9 is scored **crop-first at the registered shift**: H9 grid = `H9map[my + dy : my + dy + h, mx + dx : mx + dx + w]`, then
     DoG. This matches how T is cropped back, how the published 0.508 was made and how SOR-PHASE's crop-first numbers were
     made, and it keeps the different margins from leaking border context into the phase effect (SOR-PHASE measured a padded
     vs crop-first gap up to 0.042). The padded-filter score is description only.

| Median ratio | Class |
|---|---|
| **≤ 0.60** | **READER-LIMITED** |
| **≥ 0.85** | **SURFACE-CANDIDATE** |
| in between | **MIXED** |

## Outcomes (per region; R2 primary, R reported as in SOR-STRIP)

- **VOID:** more than 4 of 16 T phases VOID (under the 0g fallback: more than 1 of 4).
- **CLASS-STABLE <class>:** every valid pair falls in the same class. Row 7 quotes "<class>, median m, range a-b over 16 × 16
  tile phases of both readers (conditional on CT registration)".
- **PHASE-DEPENDENT:** any two valid pairs disagree. Row 7 quotes "phase-dependent, a-b (median m)" and claims no class. This
  is SOR-PHASE's Judge's frozen wording: every phase must agree; no 90 % rule.
- **T's own phase (sub-answer):** for each H9 phase, the range over the valid T phases; then the median over the 16 H9 phases.
  **T-PHASE-MATERIAL** if > 0.10 (SOR-PHASE's bar); **T-PHASE-MINOR** if ≤ 0.05; otherwise the value is reported.
- **Headline:** R2's outcome. If R2 is VOID or UNINFORMATIVE by Stage 0, the headline is R's, labelled "R only (SoR's region,
  post-hoc informed)".
- **Descriptive only (never a verdict):** windows frozen at T phase 0 (all pairs); on the T phase-0 row and the H9 phase-0
  column only (31 pairs, to keep the score step short): unregistered ratios (H9 at shift (0, 0)), the padded filter score and
  the H9 best shift within ±2 px (Critic finding 10: lane B measured 0.624 vs 0.505 on R at one phase, so the
  class is conditional on the CT registration); mean of the 16 T maps vs mean of the 16 H9 maps; reverse controls at phase 0;
  R ∪ R2 pooled per pair; the H9-phase range per T phase.

## Stage 0 (sanity checks first; any failure → `exit 78`, numbers in `[private path]<stage>.json`, no verdict)

1. **(0a) code, CPU, seconds:** the copied scorer on the saved R maps gives 0.508 with 21 good windows. Planner ran it: PASS.
2. **(0e) code, CPU:** replaying SOR-PHASE's saved arms (`R_H9_m32/m24/m16/m40_b4.png`, crop-first, saved T) gives 0.533 /
   0.468 / 0.410 / 0.400 ± 0.005. Planner ran it: PASS (exact). Also a self-test of the shift finder: a planted (1, −2) slip is
   found exactly, and a map against itself gives (0, 0). Planner ran it: PASS. Fallback for 0a / 0e: fix the code.
3. **Inputs, CPU:** each region's `pad80` has shape interior + 160; its 40-px trim matches SOR-STRIP's 40-px pad with mean
   abs diff ≤ 0.5 grey levels and the best offset exactly (40, 40); R's interior matches `R_sv96.npy` (≤ 0.5).
4. **(0d) registration, CPU:** the CT rule on the new (40, 40) layout gives exactly the frozen shift for each region, check_r
   ≥ 0.90, not on the ±15 edge.
5. **(0c) every cut input:** its interior is bit-identical to the region's own crop (T: `R_sv24.npy` / `R2_sv24.npy`; H9: the
   `pad80` interior).
6. **(0b) T repeatability, GPU ~2 min:** the zero-change T rerun on R (exact command) vs the saved `T.png`: max |Δ| ≤ 1 grey
   level on the 128 px-trimmed interior, DoG r ≥ 0.98, ratio (with the saved H9) 0.508 ± 0.02. torch / CUDA / cuDNN versions
   are recorded. **Pre-registered fallback:** the saved map is from 09-29 and the venv may have changed since. If 0b misses,
   T runs once more on the same input (0b2): if rerun 2 vs rerun 1 has max |Δ| ≤ 1 and DoG r ≥ 0.98, the test continues,
   labelled "saved T.png not reproduced; every T arm from the current venv"; otherwise the outcome is **T-NOT-REPEATABLE**
   (a named answer: row 7 then says "the 2.4 µm reference itself varies run to run by …", with the two-run numbers; exit 78).
   Every T arm, the rerun included, uses batch 1.
7. **(0h) crop-back check, GPU ~5 min (exit 78 = BUILD_BUG):**
   - **Binding:** a phase-shifted map against the SAME reader's phase-0 map, in the same content frame, must line up at
     exactly (0, 0) by normalised cross-correlation: T at margins (96, 32), cropped back, vs T (0, 0) at native 2.403 µm
     (DoG σ 1 − σ 24, ±40 px, central 1280 × 3200 block); H9 at margins (40, 64) vs H9 (64, 64) on the 9.6 µm grid (DoG 1.5 / 12,
     ±15 px). Moving the tile grid moves no content, so any non-zero shift is a code bug.
   - **Reported, not binding (the Critic's form):** each map vs the team map (the `critic_shift_R.py` scan), shift within ±1 px of
     the same reader's phase-0 shift.
   - **Why the binding form changed:** the T-vs-team peak is almost flat (r 0.325 at (0, 0) vs 0.328 at its best,
     `critic_shift_R.json`), so the Critic's form could fail on noise, and a ±1 px tolerance cannot catch the 1 px slip it is
     meant to catch. The same-reader form demands an exact match, so it is stricter, not looser. The Planner's dry run on fake
     arms gave (0, 0) at r 1.000 / 0.999 (`checks/<id>/planner_dryrun.json`).
8. **(0f) plumbing per region, at T (0, 0) and H9 (40, 40), registered (σ 1 global Pearson vs Team; SOR-STRIP Stage 0 item 5):**
   T ≥ 0.75 with T_rev ≤ 0.25; H9 ≥ 0.60 with H9_rev ≤ 0.15 (R unregistered, 10-07: 0.832 / 0.182 / 0.746 / 0.036).
   - Controls clean but T or H9 below its bar → **pre-registered fallback:** that region's lower half (9.6 grid rows ≥ 1040,
     Otsu, windows and top third over that half), valid only if the lower half passes the same bars (R2 only, as SOR-STRIP).
   - Otherwise the region is **UNINFORMATIVE by Stage 0** and its remaining arms are skipped; the job continues with the other
     region. Both regions UNINFORMATIVE → exit 78.
9. **(0g) budget:** after R2's first T run, the job projects its total wall time (input cuts included; R2's cut time scaled
   from R's by area; + 0.25 h for the score step, which runs under the claim; after a stop and restart only recorded arm time
   counts from earlier launches). If the projection exceeds **3.5 h**, R2 runs T phases {0, 64}² only (4 × 16 pairs; VOID if more than 1 of
   4 T phases is VOID; row 7 wording then says "4 × 16 tile phases").

## Seeds, compute, kill date

- Deterministic (no seeds): Hecate inference bf16, fixed inputs; 0b / 0b2 test that.
- GPU (5070 Ti, home; the router keeps it here: Hecate 2.4 is 1.9-2.9× slower on [machine name removed]): T R ~2 min × 16, T R2 ~4.5 min × 16
  (+ ~1 min input cut each), 33 H9 runs ~0.5-1.5 min, 0b / T_rev ~0.2 h → ~2.3-2.8 h; **budget 3.5 GPU-h** with the 0g
  fallback. Peak VRAM < 16 GB (`T.png` was made on this card).
- CPU: ~1 h (cuts, Stage 0, score). Disk: one temporary input at a time (≤ 4.7 GB), deleted after its arm.
- Human time: none. **Kill date: 2026-10-12** (if not scored by then, stop as INCONCLUSIVE).

## What each outcome changes

- **CLASS-STABLE READER-LIMITED on R2:** row 7 becomes "READER-LIMITED on two regions, median m, range a-b over 16 × 16 tile
  phases of both readers, conditional on CT registration" and loses "not ready"; the BRIEF reader-gate line gets the range.
- **CLASS-STABLE MIXED or SURFACE-CANDIDATE on R2:** row 7, the BRIEF reader-gate line and HANDOVER_CHRIS item 3 say the 0.51
  was one phase draw at a ~75 µm misregistration; SURFACE-CANDIDATE goes to Chris (lane B) as a reader-gate question, with a
  held-out check first.
- **PHASE-DEPENDENT:** row 7 quotes "phase-dependent, a-b (median m)" and claims no class; the sub-answer says how much of the
  spread is T's own phase.
- **T-NOT-REPEATABLE:** row 7 says the 2.4 µm reference varies run to run by the measured amount; no class.
- **VOID / UNINFORMATIVE on both regions:** row 7 stays "not ready".
- Parked parent `[internal item]` (SOR-STRIP): the main session closes it into this item; this test does not touch it.

## Odds (Critic, kept)

- Stage 0 clean and a decisive class or wording for row 7: ~8.5 / 10 on R, ~9 / 10 for at least one region; ~7.5 / 10 that it
  also settles the class question (not T-NOT-REPEATABLE). Under the every-pair rule, PHASE-DEPENDENT is the likelier class
  outcome (H9 alone already spans 0.400-0.547 at T phase 0).

## Files

- Code: `[private path]` (scorer bodies copied verbatim from
  `[private path][internal item]/sorstrip.py`), `job.sh`. Planner checks:
  `[private path]` (0a / 0e PASS),
  `planner_dryrun.py` + `.json` (later stages on fake arms built from saved R maps).
- Results: `[private path]`; maps in the item's `data/`.
  Nothing is written into `[private path]` or the parent items' folders.
