> **Scrubbed public copy** (public name `audit_guidefree`). The original was first committed to the authors' private repository at `bdc261bc0` (2026-10-09T12:56:05Z). Later commits to the same file: `60d91cdd7` (2026-10-09T12:58:41Z). Timing: Both commits pushed before any output (its Judge's check). Timestamps live in a private repository; ask the authors for a verification. Scrubbing removed mentions of non-public scrolls and local paths (paths into the authors' private repository read `[private path]` and do not resolve) and replaced internal item ids and test names with public slugs (unmapped internal ids read `[internal item]`); the scientific text is otherwise unchanged.

# Pre-registration: audit_guidefree, do the team's old mesh w00 and Chris's guide-free 2.4 µm marks agree within 75 µm at fewer than 9 in 10 stations? (PHerc0841)

- **Date:** 2026-10-09, committed before any w00-vs-mark number is computed on these stations (the Critic's grep: no
  script ever compared w00 with Chris's fresh-along or cross marks; r44 scripts on these strips are mark-free; `of9.py`
  uses w00 only for the station-0 ring). Owner: Sebastien's side (station loop item `audit_guidefree`).
  Public data.
- **Human time:** none (Chris's marks already exist). GPU: none. CPU: < 15 min.
- **Why:** BRIEF "Truth caveat": "about 9 in 10" (w00 on its own sheet) was never confirmed without a guide line
  (audit_guided: 19/21 and 15/22, both raters saw w00's line to 0.3 mm). Package (b) (readable-surface budget) lists a "w00
  audit". This gives it one guide-free line with n = 82 and a CI. It does not move the minutes-per-cm² number.
- **Truth rule:** w00 is the AUDITED object, never the key. The key is Chris's blind, guide-free 2.4 µm marks (one rater;
  fresh repeats 9/9 within 75 µm, median 9.6 µm). His marks can sit on the wrong sheet too (KEY-FAR-24: per-mark rate
  ~0.065), so **every verdict is about the pair (w00, one rater)**, never about w00 alone.

## Data and why nothing can leak

- **Primary pool (frozen by presence before any position was read; `ideas_r48_audit_n_out.json`):**
  - ORIENT-FRESH-9's 10 kept fresh along strips (7 bend, 3 flat by w00's own sagitta), stations k = 1..6 where Chris
    placed a first-pass mark (tag `test`): **46** of 60 (14 can't-tells, per strip 6/4/4/1/2/5/6/6/6/6).
  - ORIENT-CROSS-9's 6 design cross strips (the 6 LINE-9 dev sites turned 90°), stations k = 1..6, first pass: **36** of 36.
    **XT30 is scored with its first pass** (its repeat followed the next sheet from station 2).
  - Station 0 excluded (it is the w00 ring, and Chris's mark next to it).
- **Frames:** fresh strips in ORIENT-FRESH-9's frames (`of9/cache/of9_frames.json`, `as_f`); design cross strips in
  ORIENT-CROSS-9's **own-normal** frames (`oc9/cache/oc9_frames.json`; never line9's: XT11/XT31 fail line9's placement);
  fresh cross strips (line 2) in `cf9/cache/cf9_frames.json`. Marks are in the same frames (the 2.4 µm pages are rendered
  in them).
- **Pinned inputs (sha256 in `wa.py` PINS):** `line9.py`, `line9_stage0.json`, of9 / oc9 frames, stage0, Chris key and page
  key files, cf9 frames and page key, the FOLLOW-UP LINE-9 key and page key (0d), r43's dev rows (0d), the r48 presence file.
- **Second line (replication in the bendier fresh direction; description, NOT part of the verdict):** CROSS-FRESH-9's 9
  fresh cross strips, stations 1..6, Chris's first-pass marks, once `cf9_chris_key.json` exists (build id must match the
  page key). Strips that fail Stage 0b are dropped from line 2 only.

## Scoring (one scorer, `[private path]`, used for 0c, 0d, primary and line 2)

- **w00 at a station:** `line9.p_trace` (w00's strip-plane trace: median n per 0.02 mm s-bin) at the station column,
  `np.interp` across the valid bins (as r43 / r44). **NO-W00** = column outside the valid bins' range: counted, excluded.
- **ON** iff |w00 − mark| ≤ 75 µm along the strip normal; **OFF** otherwise.
- n = ON + OFF over the primary pool (82 − NO-W00).

## Verdict (frozen rule, two outcomes)

- **AGREE-BELOW-9IN10** iff BOTH:
  - (a) one-sided exact binomial test of H0 p_on = 0.90 vs p_on < 0.90 gives p ≤ 0.05, i.e. OFF ≥ the smallest count with
    `binom.sf(OFF − 1, n, 0.10) ≤ 0.05` **recomputed at the real n** (14 at n = 82 and at n = 80);
  - (b) strip bootstrap: resample the strips that have ≥ 1 scorable station with replacement, 2000 draws,
    `numpy.random.default_rng(2026100901)`, pooled rate = ΣON / Σn per draw; `np.quantile(rate, 0.95) < 0.90`.
  - Wording: "w00 and Chris's guide-free 2.4 µm marks agree within 75 µm at fewer than 9 in 10 of these stations".
  - Labelled **(concentrated)** if dropping one strip turns the verdict off in ≥ 3 of the leave-one-strip-out runs
    (description).
- **NOT-SHOWN-BELOW** otherwise, written with the exact two-sided 95 % Clopper-Pearson interval: "consistent with 9 in 10
  down to <lower bound>", and with the can't-tell worst case. Never written as "w00 is 9 in 10".
- **Never write** "w00 is off its sheet at X %" or "w00 wrong 1 in N". Key noise alone (true w00 agreement 0.90, Chris
  wrong-sheet rate e = 0.065) makes AGREE-BELOW fire 0.26-0.34 of the time (Critic, `critic_cluster_keynoise_out.json`).
- **Scope (fixed):** "46 fresh-along stations + 36 cross stations at the 6 dev sites turned 90°; 0.75-4.5 mm from a shared
  w00 ring; bend-enriched (7 bend / 3 flat fresh strips; the cross direction bends ~2-3× more); one rater, guide-free".
  Never "82 fresh stations", never "w00-wide".

## Printed beside the verdict (description, no bar)

- Fresh-along alone and cross alone: counts, exact CI, and the frozen rule applied to each.
- Pooled count and verdict without XT30.
- Can't-tells (14 fresh): rate with them counted as OFF / as ON, and the rule with them as one extra pseudo-strip each way;
  the post-hoc fact that they sit at w00's sharp bends (12/35 flagged vs 2/25, item [internal item] Critic) biases the rate
  toward "agree".
- Bend vs flat fresh strips; OFF distance bins 75-150 / > 150 µm (one sheet ≈ 130-170 µm).
- w00's signed offset at ON stations (median, p10 / p90), + = w00 on the +n side of the mark (frame normal sign of
  `line9.frame` / `oc9.xframe`); inward / outward is not asserted.
- Strip-bootstrap two-sided 95 % CI of the pooled rate; NO-W00 count; stations interpolated across a w00 gap
  (nearest valid bin > 0.05 mm).
- Key-noise bracket: observed rate / (1 − e) for e = 0 (fresh repeats 9/9), 0.065 and 0.10 (KEY-FAR-24), capped at 1.
- Line 2 (CROSS-FRESH-9), same scorer and same rule, labelled replication / description.

## Stage 0 (sanity checks first, minutes; `wa.py selftest` then `wa.py stage0`)

| check | what | bar | if it fails |
|---|---|---|---|
| 0c | planted synthetic traces (flat and tilted sheet, offsets −40 to +123 µm) returned by the scorer; ON / OFF at 75 µm; NO-W00 past the strip end; verdict logic on synthetic counts (spread 20 OFF → AGREE-BELOW; 5 OFF → NOT-SHOWN; 14 OFF lumped in 3 strips → leg (a) yes, verdict NOT-SHOWN; threshold 14 at n = 82) | every trace within 1 µm, all cases as stated | exit 78: plain bug, the Runner fixes the scorer without touching a bar and reruns once; else STOP as VOID |
| 0e | input pins (re-checked at the start of `score`, which may run days after Stage 0) | all 16 sha256 equal | exit 78: inputs changed after the design; STOP, Runner asks the human (never re-power silently) |
| 0a | presence counts from the pinned files | 46 / 36 with the per-strip counts of `ideas_r48_audit_n_out.json`, the 10 + 6 strip names | exit 78: STOP as above |
| 0b | w00's trace at station 0 vs each strip's ring (seed n), mark-free | ≤ 1 µm on **all 16** primary strips | exit 78: the Runner may fix a plain loading bug (wrong frames file / frame conversion) and rerun once; if it still fails, **VOID** (a frame mix-up would show as "w00 OFF"). On the 9 line-2 strips a failure drops that strip from line 2 only |
| 0d | r43's public dev audit (LINE-9's 36 stations, FOLLOW-UP key, LINE-9 frames) with this scorer | 9/36 OFF and the same per-station flags as `ideas_w00_bendmiss_dev_result.json` | not fatal: report the r43 number and the new one side by side, continue |

Chance of no answer (Critic): ~1 in 10, only through 0b. **0b dry run done by the Planner before this file was committed, mark-free (frames only,
no key file opened):** max 0.039 µm on the 16 primary strips, 0.045 µm on the 9 line-2 strips (bar 1 µm;
`[private path]`).

## Hold (rule 5)

- The fresh centres are CROSS-FRESH-9's sites, where Chris is marking now. All w00-vs-mark numbers on these stations go
  only to `[private path]` (git-ignored). `wa_stage0.json` holds only
  mark-free numbers and the public 0d reproduction.
- `wa.py score` runs both lines in one pass when `[private path][internal item]/cf9_chris_key.json`
  exists. If it is not in by **2026-10-14**, it scores the primary only, still git-ignored. Before that it prints
  `WA_WAITING_CHRIS` and exits 0.
- No count, verdict or CI from this test goes into the item file, FACTS.md, BRIEF, BOARD or any commit until Chris's
  CROSS-FRESH-9 file is in. After that, counts only.

## Odds, seeds, budget, kill date

- Odds (Critic): AGREE-BELOW-9IN10 ~0.6; NOT-SHOWN-BELOW ~0.4. Power of the frozen rule at true agreement 0.75 / 0.80 /
  0.85: 0.83-0.96 / 0.52-0.75 / 0.22-0.30; false-BELOW at 0.90: 0.025-0.03 (strip-clustered simulation).
- Seeds: bootstrap `default_rng(2026100901)`. Compute: CPU < 15 min, ≤ 10 threads. Kill date: 2026-10-21 (unscored by
  then → closed as not run).
- If the primary is scored (from 2026-10-14) but still held on 2026-10-21 because Chris's CROSS-FRESH-9 file never
  arrived, the Runner does not decide: it asks the human with lettered choices (A) release the primary counts without
  line 2, B) close as not run).

## What each outcome changes

- **AGREE-BELOW-9IN10:** package (b) states "w00 and one rater's guide-free 2.4 µm marks agree at <rate> (CI) here", next
  to audit_guided's guided 19/21 and 15/22; the "about 9 in 10" phrase leaves the truth caveat for this pair and setting; the
  REDO list keeps w00 as a coarse reference only. It does not say which of the two is wrong.
- **NOT-SHOWN-BELOW:** package (b) states "consistent with 9 in 10 down to <CP lower bound>" with the can't-tell worst case;
  nothing about w00 is upgraded.
- Either way the minutes-per-cm² main line is unchanged.
