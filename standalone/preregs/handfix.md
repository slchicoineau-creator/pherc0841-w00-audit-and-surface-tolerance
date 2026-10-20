> **Scrubbed public copy** (public name `handfix`). The original was first committed to the authors' private repository at `cf2d7d618` (2026-10-06T22:36:21Z). Later commits to the same file: `62c1a68bf` (2026-10-08T12:46:07Z). Timing: Original pushed before every output. The later commit (2026-10-08) changed the start surface; it came before the tool try and the timed session and changed no bar, metric or scorer (its Judge's check). Timestamps live in a private repository; ask the authors for a verification. Scrubbing removed mentions of non-public scrolls and local paths (paths into the authors' private repository read `[private path]` and do not resolve) and replaced internal item ids and test names with public slugs (unmapped internal ids read `[internal item]`); the scientific text is otherwise unchanged.

# Pre-registration: handfix, given one good neighbouring wrap, does the organizers' copy model put a readable, on-sheet surface on PHerc0841's known-text winding on the REGULAR 9.366 µm scan, and if not, what do ≤ 90 timed minutes of hand correction buy?

- **Date:** 2026-10-06 (CDT), pushed before any handfix copy, picture or page exists. Owner: Sebastien's side (station loop item
  `handfix`). Public data only.
- **Sebastien's choice (item, 2026-10-06 17:11): B, two steps.** Step 1 = the copy only (~1 GPU h), then after Thursday Chris rates the
  uncorrected copy (~6 min) and marks 24 points (~10 min). Step 2 (Sebastien's 15-min untimed tool try + ≤ 90-min timed session + Chris's
  short second page) happens ONLY if step 1 does not end COPY-ONLY. Kill date for both steps: **2026-10-19**.
- **Question (BRIEF S7, the human-minutes question):** the organizers trace a scroll by copying a finished wrap onto the next one and then
  fixing the copy by hand; they quote ~35-40 expert min/cm² (`24_Top5_Sheet_Tracing_Approaches.md:358-362`). Nobody on the team has
  timed it on the eligible (9.366 µm) type of scan. This is the **best case** (a good neighbouring wrap exists): it
  measures the marginal cost of wrap n+1 given wrap n, not the first wrap (LINE-9's question).
- **Truth rule:** nothing decides on w00's (P's) position. The read is a blind human read with w00 as the readable control; the marks are
  Chris's blind 2.4 µm marks; the landing check is against the copy's own source surface. Distances to w00 appear only as labelled
  description ("vs P, local errors").

## Data and surfaces (one path for every arm, COPY-IN's)

- **Source wrap:** s022814 (`PHerc0841/segments/20260221022814-auto_grown_20260220174252405`, native 9.366 µm tifxyz, 187 µm grid), the
  winding next to w00 (FACTS:75, median 346.5 µm; FACTS:389, 0.878 within 200-500 µm). Copy input = COPY-IN's crop `surf/S0c`
  (S2 window ± ~4 mm, sha256 of x/y/z.tif recorded in `stage0.json`).
- **Copy model:** `copy_displacement_latest` (`[private path]`), `infer_rowcol_triplet_wraps`, level 0 of
  `PHerc0841/volumes/20250821151531-9.366um-1.2m-113keV-masked.zarr`, **COPY-IN's frozen settings** (`stage0c.json`: no TTA, default
  displacement scale; argv `--no-tta`, the meta's "mirror" label is a villa quirk, COPY-IN Run 00:34).
- **Arms (all carried to the 2.4 µm band by the w00 `toband` affine, rendered 109 layers, canonical 2.4 µm ink model at +0, the surface's
  own face-rule order, P-frame FORMAT-20 S2 tile 20 × 11.7 mm, COPY-IN's `ci.py` code copied unchanged for these steps):**
  - **C (control):** w00's native 9.366 µm mesh, COPY-IN's `a/N2` render and its fixed control mask `mask_ctrl.npy` (reused byte for byte,
    sha-checked; Sebastien read it rows on COPY-IN, agents screened it rows).
  - **R (raw copy, 0 hand minutes):** the C field with the k-step inward copy of s022814 pasted into a 10 × 10 mm **inset**, 0.3 mm linear
    feather at the inset edge. Inside the inset R's own coverage counts: where the copy left a hole the picture is black (holes count).
  - **F (step 2 only):** the same field with Sebastien's corrected copy pasted into the same inset, same feather.
  - **Blanks:** each arm's wrong-order picture (C blank field with the arm's blank inset).
- **Inset placement (fixed before any copy; P-free):** 10 × 10 mm (4161 × 4161 S2 tile px), columns centred (offset 358 px); row offset
  = the position closest to the window centre (steps of 0.5 mm) where **s022814's own coverage AND the control mask** each cover ≥ 95 %
  of the inset. Placement uses the SOURCE surface only, never the copy, so the copy's own holes count against it. None → Stage 0 fail.
- **No leak:** 0841 is not in the copy model's training sets (COPY-IN premise, checkpoint config). The S2 window lies mostly in the
  sheettrace held-out zone (FACTS:108,113): F (a human trace) must never become sheettrace development data.

## Copy rule (k steps, fixed by Stage 0c on a small crop, then run on the full crop)

- One copy run gives a `front` and a `back` output. **Direction** = the output whose median move points to w00's side (COPY-IN's
  `toward_med_um` sign: a frame sign, never a score). Every chained step continues in that direction; a step whose signed toward-move is
  ≤ 0 makes the copy not interpretable (Stage 0 fail).
- **Landing (P-free):** |median signed offset| from the source s022814 to the k-step copy, along s022814's normal (COPY-IN's `shift()`),
  must lie in **250-420 µm** (about one winding; ruler 329 µm). One copy step on 0841 is sheet-sized (COPY-IN Stage 0c: front −181 µm,
  back +197 µm), so **k = 2** is the primary; **k = 3** is the one pre-registered fallback if the 2-step landing is < 250 µm. Outside the
  band at k = 2 and k = 3 (or > 420 at k = 2) → Stage 0 fail.

## Who reads and marks (people)

- **Chris only rates and marks.** Sebastien never rates (he makes F) and is not the second marker.
- **Sebastien stays blind through step 1:** he never sees the step-1 read page, any R or C ink tile of this item, the marks page,
  Chris's marks file or any per-site result until F is saved. The step-2 question tells him the aggregate step-1 class only, no
  pictures. (The step-2 correction rule forbids ink maps and the 2.4 µm band; R's tile is a 2.4 µm ink map, the marks show the sheet.)
- Agent readers: none (screening only since 2026-10-05; nothing here needs a screen: the control already read rows for a human).

## Step 1 read page (Chris, ~6 min; the standard page template, JPEG ≤ 1 MB, rows / strokes / nothing)

- 8 pictures, one seeded shuffle (seed 20261016) with the C repeat ≥ 3 positions from C: **C level, C blank, R level, R blank, C level
  repeat, the FORMAT-20 0009B calibration (`f_05`), its reverse (`f_06`), the guard picture**.
- **Guard picture (recognition check):** the first partsheet_tolerance level tile in the order L55, H50, C70, L70, H70, L85, C85 that BOTH humans
  called not rows on partsheet_tolerance (`ratings/seb/` and `ratings/partner/humantol_ratings.json`, read by the job, never staged). Its identity
  goes only in the git-ignored key. None qualifies → no guard; every "R rows" outcome is then labelled weak.
- Key `copyfix_key.json`, ratings `copyfix_read_chris_ratings.json`, result `copyfix_result.json` (all git-ignored).

## Marks (Chris, ~10 min; KEY-FIX's display and page, unchanged except the item list)

- **Sites:** a 6 × 4 grid of cell centres inside the inset (1.67 mm × 2.5 mm spacing; every site ≥ 0.8 mm from the inset edge, outside
  the feather). Site = C's carried point at that S2 tile pixel (C is the readable control; arms are never shown).
- **Frame:** n = C's normal averaged within 0.125 mm of the site; e1 = C's grid-row tangent made orthogonal to n, e2 = n × e1. View
  centre = site + δ·n, **δ ~ U(−160, +160) µm** (seed 20261017), so clicking the middle of the line does not score. Two orthogonal 2.4 µm
  planes (along e1 and e2, side sign seeded), s from −0.9 to +0.2 mm, ±0.3 mm along n, WebP q45, contrast from the 1-99.5 % band values
  around the sites, dashed view line at s = 0, green = C's trace on s ∈ [−0.9, −0.3] mm (KEY-FIX's guide).
- 24 items, seeded order and random 3-digit ids; Chris clicks where the followed sheet crosses the dashed line, or "Can't tell". Page
  in the git-ignored `cache/` (delivered by the main session). Marks file `copyfix_marks_chris_ratings.json`, key in `copyfix_key.json`.
- **Arm crossing rule (fixed now):** an arm's dense carried surface (native grid densified to ~4.7 µm, then `toband`), points within
  6 µm of the view line and |t| ≤ 300 µm, split into crossings where sorted t jumps > 30 µm; crossing t = the cluster median.
  **0 crossings → off (hole). ≥ 2 crossings → off**, counted and reported separately (never the crossing nearest the mark).
- **On:** exactly one crossing and |t_arm − t_mark| ≤ 75 µm (KEY-FIX's identity radius). Valid sites = sites with a mark; "Can't tell"
  dropped and counted.
- **Mark rule (Critic finding 4, site by site against C on the same valid sites):** **PASS-marks:** X_on ≥ C_on − 2 and
  X_on ≥ 0.75 × valid. **KILL-marks:** X_on ≤ C_on − 5. Otherwise **MIDDLE**. Needs ≥ 18 valid sites.
- **Guide bias (stated, not corrected):** the green guide is C's trace, so marks lean toward C; this is conservative against R and F.
  Descriptive, reported beside every verdict (audit_guided amendment 1): the straight-line baseline (C's green trace on s ∈ [−0.5, −0.3] mm
  extended to s = 0) and Chris's share of marks within 75 µm of it, plus the **discriminating sites**: sites where the R (or F) and C
  crossings differ by > 150 µm, and how many of Chris's marks there side with the arm vs with C (closer one within 75 µm).
  **Wording rule:** if Chris's marks lie within 75 µm of the extended guide line at least as often as they are on C, every mark-based
  verdict carries "consistent with following the guide line" (the verdict rules do not change).
- **audit_guided link** (prereg `preregs/audit_guided.md` audits single-rater keys, including these check points):
  - audit_guided **KEY OK** → the marks decide as written.
  - audit_guided **NOT A SINGLE-RATER KEY** → every mark-based part is labelled "single-rater key, unproven"; COPY-ONLY then needs the read
    as well (as written it already does); a KILL or PASS resting on the marks alone becomes INCONCLUSIVE.
  - audit_guided **UNDECIDED or not yet scored** → the verdict is stated with "pending audit_guided"; the Judge applies the line above when it lands.
  - The step-1 split (below) runs on the marks regardless: it only decides whether to ask Sebastien for time, it claims nothing.

## Step 1 outcome (scorer frozen in `cf.py`, `selftest` on synthetic files)

- **VOID (rater):** a picture unanswered, or the calibration not called rows.
- **UNINFORMATIVE (control):** C level not rows, C repeat not rows, or C blank rows.
- **UNINFORMATIVE (marks):** < 18 valid sites.
- **R read:** "rows" if R level rows and R blank not rows; "not interpretable" if R blank rows (treated as not rows for the split).
- **COPY-ONLY** (best case ≈ 0 hand minutes): R read rows AND R PASS-marks. Labelled **weak** if the guard was called rows (or no
  guard). The item closes; Sebastien is never asked for the session; next test is a worse source wrap (Ideas).
- **Every other valid outcome → STEP 2** (`loop.py human` asks Sebastien for the 15-min tool try and the ≤ 90-min session, aggregate class
  only). Sub-labels carried into the question: **COPY OFF** (R KILL-marks; if R read rows too: "the read cannot see the inset, F is
  decided by the marks alone"), **COPY UNCLEAR** (R MIDDLE), **COPY ON, NOT READ** (R PASS-marks, R read not rows).

## Step 2 (only if step 1 says STEP 2; rules fixed now)

- **Tool try (untimed, ~15 min, Sebastien):** VC3D on the 9.366 µm volume, on any 9.366 µm surface (e.g. s022814's full native mesh)
  OUTSIDE S2 **and outside the sheettrace held-out zone** (regular z 14080-16000 + 100 margin, FACTS:108,113): one visible
  control-point (or brush) edit, save as tifxyz, reload. The Runner checks the saved mesh differs from its input only near the edit
  (vertices > 1 mm from the edit move < 10 µm, ≥ 1 vertex near it moves ≥ 20 µm). Fail → `loop.py human` (training, or drop).
- **Timed session (Sebastien, cap 90 min wall clock including load and navigation):** VC3D on the 9.366 µm volume only (no 2.4 µm band,
  no w00, no ink maps, no marks). **Starting surface:** R cut to the inset + 0.3 mm (`cf.py cut` → `surf/R_inset`, meta with
  format/type/uuid/name), so the surface's own edges show him the inset and no minute goes outside it; vertices he adds outside the
  inset + 0.3 mm are ignored (the composite uses the inset only). Screenshot of the open volume/surface list at start and end; whatever
  exists at the cap is F. Minutes per cm² = wall-clock minutes ÷ inset area covered by F (description, next to the 35-40 min/cm²
  benchmark).
- **Second page (Chris, ~5 min):** F level, F blank, C level, the calibration pair, the guard (same files), seeded shuffle. F's mark
  score is computed from the step-1 marks (no new marks).
- **F verdict:** **PASS:** F read rows, F PASS-marks, C rows on this page. **PASS-weak:** F read rows and F MIDDLE. **KILL:** C rows and F
  read not rows, or F KILL-marks. **INCONCLUSIVE:** F's wrong-order blank read rows (F's read is untestable). If step 1 flagged "the read cannot see the inset": F is decided by the marks alone (PASS-marks → PASS
  marks-only, KILL-marks → KILL, MIDDLE → INCONCLUSIVE). VOID / UNINFORMATIVE as in step 1. Every KILL is scoped "first timed session of a
  new user with ≤ 90 min"; it does not bound the expert route.

## Stage 0 (sanity checks first, inside `job.sh`, before any long GPU run or human minute)

- **0a (inputs, CPU, seconds):** COPY-IN's `a/N2/*`, `mask_ctrl.npy`, `surf/S0c`, `tiles/ctrl_level.png` + `ctrl_blank.png` exist; shas
  recorded. Missing → exit 3 (bug).
- **0b (inset placement, CPU, minutes):** the placement rule above finds a 10 × 10 mm inset with s022814 coverage ≥ 95 % and control
  mask ≥ 95 %. None → **exit 78, UNINFORMATIVE by Stage 0** (fallback: none; s022814 covers 0.911 of the whole control mask, so a fit is
  expected).
- **0c (copy landing on a small crop, GPU, ~3-6 min):** a 21 × 21-cell (~4 × 4 mm) crop of S0c around the inset centre; k = 2 (fallback
  k = 3) chained steps in the chosen direction; landing 250-420 µm; every step's toward-sign > 0; each output keeps ≥ 50 % of its input
  vertices; output metadata step 20 / retarget 1 / 9.366 µm area and output ≠ input (else exit 3, bug). Fail → **exit 78, UNINFORMATIVE**
  (Critic "chance of no answer" ~3 in 10 overall; this gate is the copy part of it).
- **0d (full copy, after the ~1 h run):** the same landing band and toward-sign on the full crop. Fail → exit 78 (no page, no human
  minute). R's coverage of the inset is reported (holes count against R, no gate).
- **0e (marks display, gate, before the page goes to Chris):** C (the readable control) has exactly ONE crossing of the view line AND a
  band voxel ≥ the sites' Otsu τ lies on the line within 25 µm of it, at **≥ 75 % of the sites (≥ 18 of 24)**, with ≥ 20 sites kept (a site
  the control does not cover moves ≤ 0.3 mm to the nearest covered pixel, else it is dropped). This tests the display plumbing (frame,
  sign of t), not any arm: a broken display would sit near chance (~half of a line's length is papyrus), w00 itself is off papyrus at
  ~1 cross in 10. Fail → **exit 78, UNINFORMATIVE by Stage 0, no human minute** (the Runner first looks for a display bug; a fix is an
  amendment pushed before any page goes out). Reported beside it: the straight-line baseline's share within 75 µm of C (aggregate only).
- The VC3D-ready copy and the tool try belong to step 2, not to `job.sh`.

## Compute, seeds, budget, kill date

- GPU ~1.5 h on the RTX 5070 Ti (Stage 0c ~5 min, two chained steps on S0c ~55 min, canonical maps for R both orders ~15 min); CPU
  renders, tiles, mark planes ≤ 10 threads, ~1 h. Claimed inside the job wrapper (`station-runner`). Cloud: none. Chris's machine: none.
- Seeds: 20261016 (read page order), 20261017 (δ, slice sides), 20261018 (mark page order and ids), 20261019 (contrast sample).
- People: Chris ~16 min after Thursday 10-08 (after his LINE-9 trace page); Sebastien 0 min in step 1, ~2 h in step 2 only if asked.
- **Kill date: 2026-10-19.** Step 1 not rated by then → closes as not run (UNDECIDED). Step 2 that cannot fit by then: the step-2
  question offers to move the date.
- Scripts: `[private path]` (Stage 0 + copy + R + pages), `cf.py` (copied from COPY-IN's
  `ci.py` for surfaces / copy / render / tiles / read page and from KEY-FIX's `keyfix.py` for the marks page; scorer + `selftest`).

## What each outcome changes

- **COPY-ONLY:** package (b) gets "given one good wrap, the copy model alone puts a readable, on-sheet 1 cm² on 0841's regular scan
  (0 hand minutes, best case)"; the minutes question moves to a worse source wrap and to the first wrap (LINE-9).
- **Step 2 PASS / PASS-weak:** package (b) gets the first timed copy-and-fix number on the eligible scan (minutes per readable cm², first
  session of a new user) next to the 35-40 min/cm² benchmark.
- **Step 2 KILL:** "copy plus ≤ 90 min of a new user's fixing does not reach readable on 0841, even in the best case" (scoped as above).
- **UNINFORMATIVE / VOID / UNDECIDED:** no package line; the reason is logged.

## Amendment (2026-10-08, Planner digest of OVL-START-9, before the practice pair or F exists; no bar, metric or scorer changed)

- **Starting surface of the timed session = `[private path][internal item]/surf/OVL_inset`** (the same inset + 0.3 mm
  square re-made with `--bbox-overlap 0.5` through both chained steps, no TTA; meta tifxyz / seg / name `ovlstart9_OVL_inset`), replacing
  `surf/R_inset`. Sebastien chose this (OVL-START-9, choice A, 2026-10-08 07:30). Reason: R_inset carries ~10 block-edge break lines (E 0.198 /
  0.155 at its seams); OVL_inset removes them (E 0.006 / 0.014; OVL-START-9 PASS, FIXED-IN-CHAIN).
- **Baseline (descriptive, not a bar):** OVL_inset is a different surface from R (~19 % of inset cells land >= 75 um away), so R's unfixed
  mark score does not transfer. F's report shows, beside F's mark score, OVL_inset's own unfixed mark score at the same step-1 marks, as
  already computed by OVL-MARKS (item [internal item], git-ignored `ovlmarks_result.json`; class KILL-marks). Per-point numbers stay out of
  committed text and away from Sebastien until F is saved.
- Unchanged: inset, 90-min cap, 9.366 um volume only, vertices outside the inset + 0.3 mm ignored, F verdict rules, second page, kill date.
