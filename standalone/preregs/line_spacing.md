> **Scrubbed public copy** (public name `line_spacing`). The original was first committed to the authors' private repository at `c106700b0` (2026-10-11T17:12:15Z). Timing: Committed before any output (its Judge's check). Timestamps live in a private repository; ask the authors for a verification. Scrubbing removed mentions of non-public scrolls and local paths (paths into the authors' private repository read `[private path]` and do not resolve) and replaced internal item ids and test names with public slugs (unmapped internal ids read `[internal item]`); the scientific text is otherwise unchanged.

# Pre-registration: line_spacing. On s022814's labelled window, do fields the computer builds from that surface's own lines, about 2 mm and 4.5 mm apart and joined by the sheet-direction fill, read rows for both blind raters on the page that carries fullhop_s022814's pictures?

- **Date and owner:** 2026-10-11 (CDT). Sebastien's side. Written by the Planner station of the lane-A loop (item
  `line_spacing`). Public data only (PHerc0841). Pushed before any O45 field, render, map, tile,
  page or rating exists. The Planner's dry run built only the 5-line ring plan; it then deleted those files.
- **Sebastien's choice (2026-10-11 12:01): option A.** The two line pictures go on the shared blind page that the two damage
  tests already planned (fullhop_w `fullhop_w` and fullhop_s022814 `fullhop_s022814`, both parked). Every picture of this window gets
  the same frame. Both damage tests are unparked and their plans amended before any picture is seen. Chris rates first, then
  Sebastien.
- **Why:** this is the read that LINES-READ-814W's kill row left open: "NOT closed: a blind human read of O beside C'".
  Its proxy (ink-map r 0.748 < 0.80) was never calibrated against a read. Two humans now do the read, with no proxy gate in
  front of it. The answer decides whether the line route can make a readable field at about 2 mm spacing at all. That in
  turn decides whether Sebastien's real-line session (~16-21 GPU-h of fibre inference plus his time) is worth running, and at
  which spacing.
- **Design:** the Ideas station's item, with the Critic's fixed design F1-F7 binding. Deviations have their own section.

## Truth rule (2026-10-05)

- w00 (P) is never read by any step.
- s022814 (the organizers' semi-automatic surface on this window) is used for:
  - the lines (its own constant-z curves);
  - the display region M;
  - the control ctrl814 (fullhop_s022814's undamaged picture of s022814);
  - the label-AUC order and depth pick (one frozen rule for every O arm; it picks, it decides nothing);
  - construction-only distances, always labelled "vs s022814, local errors" and never a criterion.
- **What decides:** a blind human read (rows / strokes / nothing) by both humans. Neither human traced or picked these
  fields: the computer builds them, so both may rate (truth rule).

## Data and leakage

- **Window:** depth_s022814's frozen window on s022814's 2.403 µm SV (rows 0-8320, cols 7644-12521), shown over region M
  (2.10 cm², between the first and last planned line). Region M is LINES-READ-814W's `region.npy`, frozen before any arm
  existed.
- **No new viewing of the window:** the page that carries fullhop_s022814's pictures brings both raters to this window once anyway.
  This item adds two pictures to it. No third labelled 0841 window exists (FACTS:1042).
- **Blinding:**
  - Masking (F2, binding) removes the one display cue found: the border. Unmasked, O2 shows 10.6 % black against 3.4 % for
    ctrl814. Grey tone already matches (Critic's `critic_tone_out.json`).
  - Everything that hints at a picture stays git-ignored: field / pick / frame / det numbers (`*_result.json`), tiles,
    maps and `lf_page_extra_key.json`.
  - `stage0.json` holds only gate flags and geometry numbers.
  - F6: before any page exists, the main session adds this item to `BLIND_EXTRA["chris"]` (`brainstorm_check.py:31`).
    The `[for Chris]` question gives only the time and "one page, one look per picture".
  - O's ink-map r is already public (FACTS:1048). It tells a rater that O differs from the control, but not which picture
    is O.

## Arms and controls

| picture | what it is | role |
|---|---|---|
| **O2** (primary) | LINES-READ-814W's saved O field: 10 of s022814's own constant-z lines, 2.02 mm apart, frozen ob9 fill, 12 fill rows per gap; its frozen pick (inked rev, a* = +10) | arm |
| **O45** (secondary) | same frozen builder with 5 lines (4.54 mm apart; the first and last ring are identical to O2's) and 24 fill rows per gap (~0.19 mm); its own order + depth by the same label rule (7 depths) | arm |
| ctrl814 level | fullhop_s022814's undamaged s022814 picture (its chain, fixed offset) | readable control (F3: a rater who does not call it rows is undecided for this window) |
| ctrl814 blank, L70_814 blank | fullhop_s022814's wrong-order pictures | validity (must not be rows) |
| L85 / L70 / L55_814, H50_814 | fullhop_s022814's damage ladder and its holes guard | fullhop_s022814's own arms; H50_814 and L55_814 are this item's leniency guards |
| 0009B calibration pair | FORMAT-20 `f_05` (rows) / `f_06` (blank) | validity |
| fullhop_w's W pictures | the other window | never count here |

- **Not shown:** O-L2 (layout fallback; description only), any 1 mm arm, an O2 wrong-order blank (F7 skipped: page size,
  see Deviations).
- **Chain difference (Critic item 8):** O goes through `lr814.py`'s chain (9.366 → 2.4 µm transform, label-picked depth).
  ctrl814 goes through `t8.py`'s chain at its fixed offset. Both reproduce the organizers' picture: r(C', SV) 0.9085 and
  r(ctrl814, depth_s022814 ctrl) 0.96. A FAIL may therefore carry a few % of chain or depth difference. The wording below
  accounts for that.

## Build (`[private path]`)

- **A wrapper, not a copy:**
  - It loads `lr814.py` (sha256 `ea01684d…`, never edited; its own pins cover ob9 / cf9 / fw / fiber9) and `t8.py`
    (sha256 `5edaa53d…`, with `FLOOR = 170`, the floor fullhop_s022814's tiles were built at).
  - Every write is re-pointed into this folder: `b45/`, `bL2/`, `arms/O45`, `arms/OL2`, `maps/*`, `tiles/`. The write
    paths are asserted to be inside this folder.
  - C', O2's maps, O2's pick and region M are read only from item 12. fullhop_s022814's maps, oks and mesh are read only from its
    folder.
  - `protect` / `protectcheck` hash 20 read-only inputs before and after each job. Any change means exit 1.
- **Job 1** (`job.sh`, CPU, ~1 h): `selftest` → `protect` → `rings45` (0a-ring) → `field45` (0a) → `fieldL2` (0c build) →
  render + project O45 and O-L2 → `protectcheck`.
- **Job 2** (`g2/job.sh`, GPU, ~1 h, refuses unless job 1 ran):
  1. `det` (0b);
  2. `pick O45` (8 maps, ~3.5 min each);
  3. `frame` (0d), which writes `tiles/` and `lf_page_extra_key.json`;
  4. `pick OL2` + `olr` (0c, description only, last, droppable);
  5. `protectcheck`.
- **No page and no key are built by either job.** The page is the Runner step below.

## Stage 0 (sanity checks first; order: CPU → GPU → human)

| check | when | bar | fail → |
|---|---|---|---|
| **0a-ring** | job 1, minutes | the 5-line plan's first and last ring are identical to item 12's, and region M rebuilt from it equals item 12's `region.npy` exactly | exit 78: O45's frame would differ from O2's. Fallback: the Runner relaunches job 1 with `SKIP_O45=1` (O2 alone) |
| **0a** O45 geometry | job 1 | coverage ≥ 0.90 of planned quads, fold-overs < 1 % (= LINES-READ-814W's 0f bars) | O45 dropped, O2 alone on the page; the job goes on (never 78) |
| **0c build** O-L2 | job 1 | none (description) | logged, the job goes on |
| **0b** determinism | job 2, ~4 min | O2's o+10 rev map, re-made from item 12's render: Pearson r ≥ 0.999 and median \|Δ\| ≤ 1e-3 vs the saved map (max \|Δ\| reported) | exit 78 (plumbing). Fallback: the Runner reruns job 2 once. If it fails again, O2's tile comes from this item's re-made map, and the verdict notes "O2 map re-made (not bit-stable)" |
| **0d** common frame | job 2, minutes | common mask = M ∩ O2.ok ∩ O45.ok ∩ ok of ctrl814 / L85 / L70 / L55; every picture of the window is tiled with t8's exact tile rule inside it. Two checks: (1) the black share (exact-zero pixels) of every non-guard 814 picture (ctrl814 level + blank, L85, L70, L55, L70 blank) is within 2 points of O2's and of O45's; (2) the moved-vertex share (> 50 µm) of L85 / L70 / L55 inside the mask is within ±0.02 of its whole-window value (dose unchanged) | exit 78: no page, ask Sebastien (lettered choices) |
| page size | page step | built page < 1 MB | fullhop_s022814's own fallback page carries the pictures (as its prereg says) |
| rater validity | after rating | F3 below | that rater is invalid; outcome rule below |

- **Chance of no answer:** ~0.21 by the Critic's model (`critic_odds_out.json`: LENIENT ~0.10, VOID / one-rater rows
  ~0.12). There is also a small risk at the page step (the amendments, or 0d → exit 78).

## Page (Runner step; NOT in the jobs)

It runs only when ALL of these hold:
1. job 2 ended `LF14_JOB2_DONE`;
2. the main session has unparked fullhop_w and fullhop_s022814;
3. their owner stations have committed their F2 prereg amendments, listed below;
4. the main session has added this item to `BLIND_EXTRA["chris"]`.

Amendments needed in the two damage tests (their own stations, their own prereg paths):
- **Masked pictures:** fullhop_s022814's 7 pictures on the page are the masked tiles listed in this item's
  `lf_page_extra_key.json` (same surfaces, orders and offsets, plus the common frame). Its damage law and doses inside the
  frame are unchanged (0d check 2).
- **`fh.py page`:** must accept extra items that carry their own `item` tag. Today `dict(item="fullhop_s022814", **meta)` raises
  on a meta that has an `item` key.
- **`fh.py rater`:** must skip `item == "line_spacing"`. Today it skips only fullhop_s022814, so O pictures would enter
  fullhop_w's validity.
- **`t8.py rater`:** already ignores anything but fullhop_s022814 + shared (checked in `lf14.py selftest`).
- **fullhop_s022814's own fallback page** (`t8.py page`): reads the same extra file when it is used.
- **No cross-scoring:** O2 / O45 never count toward any page-wide leniency, validity or HOLDS / FAILS line of fullhop_s022814 or
  fullhop_w.
- **Adjacency:** O2 and O45 are never adjacent. After the page's frozen shuffle, if they are, O45 swaps with the picture
  after it (the one before it if it is last). The swap is recorded in the page key.

Then the steps:
1. Build the page: `fh.py page [private path]`. If it is over
   1 MB, use fullhop_s022814's own page with the same extra file.
2. Ask Chris (`[for Chris]`), then Sebastien. Same wording as the damage tests' page (rows / strokes / nothing), one look
   per picture, no comparing notes.

## Outcome rule (`lf14.py score`, self-tested on 13 answer patterns + 4 checks before anything runs)

- **F3, valid rater (= fullhop_s022814's rule):** every fullhop_s022814, calibration and O picture answered; calib "rows"; the 0009B blank,
  ctrl814 blank and L70_814 blank each not "rows". Let d = the valid raters who call ctrl814 "rows".
- **F4, per arm X ∈ {O2 (primary), O45}:**
  - **X-READS:** both raters in d call X "rows", AND at least one of them calls H50_814 or L55_814 not "rows". fullhop_w's
    W guards never count.
  - **X-FAILS:** at least one rater in d calls X not "rows". This decides whatever the guards say. Labels: X-NO if both, X-SPLIT
    if one of two, "X-FAILS (one valid rater)" if d has one rater.
  - **X-LENIENT:** both "rows", but no 814 guard was called not rows → undecided.
  - **X-VOID:** d is empty. With one rater in d, that rater's "rows" is a one-rater lead (undecided).
- **F5, wording (frozen in `lf14.py wording`):**
  - **O2-FAILS:** "fields from perfect lines 2.02 mm apart + the frozen fill were not read as rows by both blind raters / one
    valid blind rater on s022814's window, while its organizers' surface was (one window, label-picked depth)". Never
    "perfect lines do not read".
  - **O2-READS:** "fields from perfect lines 2.02 mm apart + sheet-direction fill read rows for two blind raters on
    s022814's window; forecast floor at the measured fibre-tool pace 8.5-10.8 min/cm² (starts given, perfect lines, depth
    chosen by this window's own labels, one window)". Never "measured minutes per readable cm²", never "a readable surface
    method".
  - **O45:** the same wording with 4.54 mm and 4.2-5.4 min/cm². It is a secondary arm (its 4.5 mm fill rests on a
    descriptive check only, 0e 20/25).
- **Seeds and pace:** the minutes are FIBER-9B's measured pace (6.62 mm/min) applied to lines nobody drew. They are a
  forecast, not data.

## Deviations from the Critic's fixed design

1. **Wrapper instead of a copy of `lr814.py` (Critic item 10).** It changes the same three constants (`N_LINES`, `NSUB`,
   layout) without duplicating 760 lines. `lr814.py` is untouched and pinned. The write paths are asserted, and the inputs
   are hashed before and after each job.
2. **0b has a tolerance** (r ≥ 0.999, median |Δ| ≤ 1e-3) instead of "identical". Bit-identity fails on GPU fp16
   nondeterminism without any real difference.
3. **F7 (an O2 wrong-order blank) is skipped.** The page would carry ~18 pictures, and depth_s022814's 14-picture page was
   already 858 KB. fullhop_s022814's own prereg expects the 1 MB check to be tight.
4. **The common mask also includes the ok of the 814 field pictures.** Without it, ctrl814 / L-levels would keep black pixels
   that the O pictures lack (the reverse cue). H50_814 keeps its holes (it is a guard, and outside the black-share gate).

## Compute budget

- CPU ~1 h: O45 + O-L2 fields ~9 min each, renders ~15 min each, projections.
- GPU ~1 h: 1 + 8 + 8 maps at ~3.5 min (measured on item 12, 2026-10-11).
- Home machine, 5070 Ti, peak VRAM ~8.3 GB (item 12's g2 peak).
- Human: ~1 extra minute per rater, in the sitting both already owe.

## Seeds, tools, pins

- No new random seed. The fields are deterministic, and the page shuffle is the shared page's own (fullhop_w 20261008 or
  fullhop_s022814 20261009).
- Pins: `lr814.py` `ea01684d74841dbfb7ebc24350afd31eb3d191b49f5795308d14bedde3ef7798`, `t8.py`
  `5edaa53d2923d79b6f5f06cadb5b75eb34cbc41448d9c5f9f879aa516565f63a`. The O2 pick is asserted to be (rev, +10).

## Kill date

- If the rating sitting has not happened by **2026-10-25 23:59 CDT**, the item closes UNDECIDED (no package line).
- If 0d fails and Sebastien does not answer by then, the same applies.

## What each outcome changes

- **O2-READS:** package (b) gets the pass line with the forecast. If **O45-READS** too, the real-line session uses ~4.5 mm
  spacing. If O45 fails, it uses ~2 mm.
- **O2-FAILS:**
  - The line + ob9 fill route at ≥ 2 mm gets no session (LINES-READ-814W's H arm is not run at that spacing).
  - The next step is denser lines or a layout fix, chosen by 0c's description: O-L2's r vs C' against O's 0.748 says
    whether in-sheet layout (pairing) or between-line depth wander is the weak step.
- **LENIENT / VOID / one-rater lead:** nothing changes, and the window is not shown again for this question.
