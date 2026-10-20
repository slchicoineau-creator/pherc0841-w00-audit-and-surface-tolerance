> **Scrubbed public copy** (public name `w00_trusted_crosses`). The original was first committed to the authors' private repository at `7aa208df6` (2026-10-05T01:11:47Z). Later commits to the same file: `d9e8e41b8` (2026-10-05T01:42:38Z); `ef1d4b7ad` (2026-10-05T02:20:54Z); `bdc71d6ab` (2026-10-05T03:49:23Z). Timing: Run in the main session, not by the station loop, so no loop Judge checked its timing. Timing of each amendment as stated in the file itself (amendments 1-2 before any rating or re-score, amendment 3 during the worked examples, before any real item). Timestamps live in a private repository; ask the authors for a verification. Scrubbing removed mentions of non-public scrolls and local paths (paths into the authors' private repository read `[private path]` and do not resolve) and replaced internal item ids and test names with public slugs (unmapped internal ids read `[internal item]`); the scientific text is otherwise unchanged.

# Pre-registration: w00_trusted_crosses, where is the answer key P (team mesh w00) on one papyrus sheet? (PHerc0841 dev crops)

- **Date and owner:** 2026-10-04 evening, written in the main session (Sebastien's side) after his choices on
  `[private path]`: Q1 A, Q2 A, Q3 A.
- **Frozen before anything is computed:** this file is pushed before any audit number, any calibration page and any
  re-score is computed.
- **Why:**
  - At TWO-LINE practice pair p448 and HUMAN-SLAB control v581, P leaves the papyrus at full resolution (2.4 µm), as
    `checks/truth-audit/` shows.
  - Every "on the true sheet" score uses P as its key, so we need to know where P can be trusted.
- **Data:**
  - Band `20260319124803-2.403um-0.2m-77keV-masked.zarr`, **level 0 (2.4 µm)**, read in RAM (`SV_MEMCACHE=1`).
  - P = `mesh_P` densified ×5, as used everywhere.
  - Only the 7 dev crops c0-c2 and h0-h3. The 5 held-out seeds stay sealed.
- **The CT alone decides.** m7, the grower and every other model output play no part in the audit, so the re-scores of
  m7-against-P tests cannot be circular.

## 1. The audited unit: a "cross"

- A cross is centred on a P point q.
- **Its two slices:**
  - Both contain P's normal n, averaged over 0.25 mm.
  - Each runs along one of P's two mesh-grid directions, made perpendicular to n.
- **P's trace** in a slice is the median over 0.02 mm bins of the P points within ±0.75 L2 vx (±7 µm) of the slice
  plane.
- **The audited window** is |s| ≤ 0.75 mm on both slices.
- **Can't audit:** if the trace covers < 80 % of the window bins on either slice, the cross is "not auditable" and
  counts as untrusted.

## 2. Features (2.4 µm CT only)

- **τ, the papyrus threshold of each crop:** Otsu on 200 000 seeded random level-0 voxels within 0.3 mm of P.
- **A (off papyrus):**
  - Per trace point: the distance along the slice's normal direction to the nearest voxel ≥ τ, searched within
    ±60 µm and capped at 60.
  - A = the share of trace points of both slices with a distance > 7 µm (3 voxels).
- **B (crossing sheets):**
  - Per trace point: the angle between P's normal and the local CT sheet normal.
  - The CT sheet normal is the main eigenvector of the structure tensor: gradient σ 1.5 voxels, window σ 6 voxels.
  - B = the 90th percentile of that angle over both traces, in degrees.
- **The rule:** a cross is **untrusted** if A > θA or B > θB, or if it is not auditable.

## 3. Calibration by Sebastien (sets θA and θB once)

- **The sites: 48 crosses.**
  - **Pool:**
    - every auditable cross on a 0.25 mm grid of P;
    - ≥ 1 mm from every departure event, every HUMAN-PICK / HUMAN-SLAB site and every TWO-LINE pilot / main item;
    - ≥ 1 mm from each other.
  - **Draw:** 16 from each third of the combined rank max(rank A, rank B), seeded. Within each third the crops are
    taken in turns.
  - **Repeats:** 4 seeded repeats added for consistency, so 52 items.
- **The page:**
  - Two level-0 slices per item, showing |s| ≤ 1.0 mm with ticks at ±0.75 mm and t ±0.4 mm.
  - The green trace is drawn. A Hide-line toggle and zoom are available.
  - Contrast fixed per crop.
  - **Question:** "Inside the ticks, does the green line stay on ONE papyrus sheet in both pictures?"
    Yes / No / Can't tell.
  - **Two worked examples first, not scored:**
    - p448's 2.4 µm view: No;
    - TWO-LINE control p357: Yes.
- **Fitting:**
  - θA ∈ {0.02, 0.05, 0.10, 0.15, 0.20, 0.30}, θB ∈ {10, 15, 20, 25, 30, 40, ∞}.
  - Choose the pair with the best balanced accuracy, where No = untrusted. "Can't tell" and the repeats' second
    answers are left out.
  - Ties go to the stricter pair: smaller θA, then smaller θB.
- **Reliability gate:**
  - The audit is used only if balanced accuracy ≥ 0.80, with ≥ 8 Yes and ≥ 8 No, and the repeats agree ≥ 3 / 4.
  - **Otherwise the audit FAILS.** No re-score is claimed, the recorded verdicts stay with a note, and the loop stays
    paused while new options go to Sebastien.

## 4. How a test uses the map (fixed now)

- **The map:** each P point on the 0.25 mm grid is trusted or untrusted by §3.
- **A site** is untrusted if its nearest grid cross (≤ 0.18 mm) is untrusted.
- **An area metric** drops every P point within 0.18 mm of an untrusted cross.

### HUMAN-SLAB #27

- Controls whose key cross is untrusted are **void**.
- **PASS requires correct / valid ≥ 12 / 14 (0.857).** For example, 11 / 13 = 0.846 is still FAIL.
- The tests are re-scored on trusted sites as a secondary result.
- No new rating is made, and the void rule never counts a click as right.

### HUMAN-PICK #11

- Re-scored by the same rule, on controls and tests.

### NG-TRACE #18, M7-RERUN #21, SOFT-M7 #01, ORACLE-FILL #37, CORRECT-PICKS #06, GROWER-DIAG

- Each scoring script is re-run on the CPU with untrusted P removed. Its own verdict rule stays unchanged.
- GROWER-DIAG is the pre-loop result (`[private path]`): "the grower hops on ~40 % of the area".
- **Order:**
  1. HUMAN-SLAB
  2. NG-TRACE
  3. GROWER-DIAG
  4. the rest

### #35 FOLLOW-UP

- Its reading verdict is judged as written.
- The share of its click sites on untrusted P is reported with it.

### TWO-LINE #39

- It is rebuilt under its own new prereg.
- Only pairs whose whole drawn green line and P candidate lie on trusted crosses are kept.
- Pictures are at 2.4 µm.
- A fresh seed sets the order, ids and letters.

### Reporting

- Every re-scored verdict is reported next to its original.
- Any change goes to Chris's /judge.

## 5. Outputs

- **Committed, counts only:** `[private path]`.
- **Git-ignored:**
  - the page, at `[private path]`;
  - the key, `trustedP_key.json`;
  - the ratings, `trustedP_seb_ratings.json`.

## Amendment 1 (2026-10-04 ~21:30, before any calibration page, rating or re-score)

- **Why:** a smoke run (12 h0 crosses) and a check on 13 crosses showed the two features as first written measure the
  wrong thing. Evidence: `[private path]` and the numbers below.
  - **A at 7 µm measures mesh precision, not error.** P usually sits 10-30 µm beside the papyrus surface. At 7 µm,
    0.27 of known-good p357 counts as "off".
  - **At 25 µm the feature separates the cases:**
    - known-bad v581: 0.89;
    - known-good p357: 0.03;
    - 10 random h0 crosses: 0.00-0.67.
  - **B at level-0 scale (σ 1.5 / 6 voxels) follows fibre texture.** Its 90th percentile was 30-65° everywhere.
- **Changes:**
  - **A:** the share of trace points with **no voxel ≥ τ within 25 µm**.
  - **B:** the **median** angle. The structure tensor is computed on **level 1 (4.8 µm)**, gradient σ 1.5 and
    window σ 6 L1 voxels (= 3 / 12 L0 voxels), on every 4th trace point.
  - **Grids:** θA ∈ {0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.50}, θB ∈ {15, 20, 25, 30, 40, ∞}.
  - Everything else is unchanged: the sites, the page, the fitting rule, the gate and the uses.

## Amendment 2 (2026-10-04 ~22:45, before any re-score; Sebastien's objection to "void only")

- **Why:** voiding a control whose key is bad assumes the rater's click there was wrong. The fair fix is a **corrected
  key, set blind**. Sebastien cannot set it, because he is the rater. Claude cannot either: it knows HUMAN-SLAB missed
  the bar by one.
- **The marker:** Chris (partner), on `[private path]` (built by `keyfix.py`).
  - **What he sees:** all **28 control sites** of HUMAN-PICK (14) and HUMAN-SLAB (14), on the same two planes Sebastien
    saw, at **2.4 µm**, with the same green context and the dashed view line. The display covers s −0.9 to +0.2 mm
    and ±0.3 mm along the view normal.
  - **What he does not see:** any click of Sebastien's, any key and any result.
  - **What he does:** clicks where the followed sheet crosses the view line, or "Can't tell".
  - **Why all 28:** so he cannot tell which sites are in question.
- **Rule for HUMAN-PICK and HUMAN-SLAB controls:**
  - **Primary, at sites the audit marks untrusted:**
    - Chris's mark is the key, and Sebastien's click is judged with the original 75 µm rule against it.
    - If Chris chose "Can't tell", the site is void.
    - The bar stays correct / valid ≥ 12 / 14.
  - **Secondary, reported:**
    - Chris's mark is the key at every site where it differs from P by more than 75 µm.
    - Agreement between Chris and P is reported over all 28.
  - **If the audit gate FAILS:** the secondary rule becomes the re-score.
  - **Not covered:** a click made at a slider offset other than 0 (HUMAN-SLAB) keeps its original judgement. The
    marks are for the central plane only.
- **Reporting:** any verdict that changes goes to /judge, with the old and new scores side by side.

## Amendment 3 (2026-10-04, while Sebastien was on the worked examples, before any real item was answered)

- **What changed:** worked example ex2 (TWO-LINE control p357, labelled "Yes" by Claude) is removed from the page.
- **Why:**
  - Sebastien judged it "No": the line crosses a dark gap and moves onto another sheet.
  - The example label was Claude's own reading, not a verified answer. A wrongly labelled example would teach the wrong
    standard.
- **What stays the same:** ex1 (p448, "No") is kept. Examples are never scored. The 52 rated items, their order and ids
  are unchanged.
- **A note for the scope:** p357 was a TWO-LINE control chosen because P sits on m7 there. If P leaves its sheet even
  there, P errors may be more common than the 25 µm feature suggests. The calibration on Sebastien's ratings sets the
  thresholds either way.
