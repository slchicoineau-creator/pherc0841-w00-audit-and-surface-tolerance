> **Scrubbed public copy** (public name `human_vs_agent`). The original was first committed to the authors' private repository at `faaa82ea0` (2026-10-06T03:24:47Z). Timing: Committed and pushed before any output (its Judge's check). Timestamps live in a private repository; ask the authors for a verification. Scrubbing removed mentions of non-public scrolls and local paths (paths into the authors' private repository read `[private path]` and do not resolve) and replaced internal item ids and test names with public slugs (unmapped internal ids read `[internal item]`); the scientific text is otherwise unchanged.

# Pre-registration: human_vs_agent, are the agent readers the odd one out on the 18 partsheet_tolerance pictures, or do two people disagree as much? (PHerc0841 + 0009B, known text)

- **Date:** 2026-10-05 (22:25 CDT). Station loop item `human_vs_agent`. Owner: Sebastien's side.
  Public data. Pushed before Chris opens the partsheet_tolerance page (planned Thu 2026-10-08).
- **Why:** BRIEF B1 makes agent readers "screening only" because they disagree with Sebastien on 5 of the 18 partsheet_tolerance
  pictures (`preregs/partsheet_tolerance.md` amendment 2). That treats one human as the reference. No human-human
  baseline exists on these pictures, so 5/18 cannot yet be read as "agents are worse than a person". Feeds package (b)'s
  blind-protocol row ("how AI agent readers compare with a human") and the weight of every one-rater line in it.
- **Relation to partsheet_tolerance:** a separate test that only reads partsheet_tolerance's ratings. It changes nothing in the partsheet_tolerance
  page (`[private path]`), its order, its key or its primary two-rater scoring.
- **Truth rule:** no surface position anywhere. Only reader calls on identical picture bytes decide.
- **Disclosure:** a Claude run has seen Sebastien's per-picture answers and the key (partsheet_tolerance amendment 2). The bars
  below are symmetric (they name either reader as the odd one) and are fixed before Chris rates. This Planner run printed
  only counts and booleans from Sebastien's file.

## Readers and data (no new page, no new picture, no new rating time)

- **Pictures:** the 18 partsheet_tolerance pictures (8 levels, 8 level blanks, the 0009B calibration f_05 and its blank f_06).
- **Sebastien:** `ratings/seb/humantol_ratings.json` (rated 2026-10-03; sha256 in `[private path]`).
- **Chris:** his partsheet_tolerance answers, default path `ratings/partner/humantol_ratings.json` (the page's download, renamed as
  `ratings/README.md` says); another path is passed with `--chris`.
- **Agent majority:** per picture, the binary majority (rows vs not-rows) of the 3 valid agent readers who read that
  exact tile file: TOL-20 / TOL-20b / TOL-HOLES `*_result.json` (level and blank), FORMAT-20 `format20_result.json`
  (calib, blank09). Same sources as amendment 2. A straight binary majority equals amendment 2's most-common-answer rule
  on all 18 (0 three-way splits, 0 ties; `[private path]`).
- **Why nothing can leak:** the agent calls were fixed days ago; Sebastien rated on 2026-10-03; Chris has not seen the
  key, Sebastien's answers or the per-picture agent calls (all git-ignored or unpushed). Sebastien's file is untracked
  and Stage 0 checks it stays so.

## Metric (every call binary: "rows" vs not)

- **Discordant set:** the pictures where Sebastien and the agent majority differ (5 of 18, reproduced in Stage 0).
- **k** = on the 5 discordant pictures, how many times Chris sides with Sebastien.
- **m** = on the 13 concordant pictures, how many times Chris differs from both.
- Chris's calls: all 18 binary calls, as amendment 2 used for Sebastien. partsheet_tolerance's per-level blank mask is NOT applied
  here (it stays in partsheet_tolerance's own primary scoring).

## Decision (fixed now; gap-free, every (k, m) has exactly one verdict)

- **Valid Chris first (partsheet_tolerance's rule):** calibration = rows and at most 1 of the 9 blanks = rows. If not valid →
  **UNDECIDED**; Chris's invalidity is reported as the finding; nothing else is scored.
- **AGENTS-OFF:** k ≥ 4 of 5 **and** m ≤ 1 of 13.
- **SEB-OFF:** k ≤ 1 **and** m ≤ 1.
- **HUMANS-NOISY:** every other outcome (including m ≥ 2 at any k, and k = 2-3).
- The exact sign test on k of 5 is reported (one- and two-sided). With 5 discordant pictures it cannot fall below
  0.031 one-sided / 0.0625 two-sided, and the write-up says so. Under chance (Chris random on the discordant 5),
  k ≥ 4 comes up 6 times in 32.

## What each outcome changes (bounded claims)

- **No outcome makes the agents the reading instrument again.** B1 stays as written whatever the result (18 pictures).
- **AGENTS-OFF:** package (b)'s protocol row may say "on these 18 pictures, the agent readers disagreed with either human
  more than the two humans disagreed with each other".
- **HUMANS-NOISY:** one human is not a reliable reference here. Package lines resting on one rater (snapping_refine, snapping_midline,
  snapping_sheetline, FORK-SPLIT ratings and similar) get flagged "one rater"; two-rater consensus is required wherever the
  package claims a read.
- **SEB-OFF:** goes to Sebastien as a decision (`loop.py human`), with lettered choices; every Sebastien-only verdict is
  marked "one rater" meanwhile.
- **UNDECIDED:** nothing is claimed; B1 unchanged.

## Secondary (descriptive only, never a verdict)

- The same k / m on the 9 levels + calibration only (blanks are near-certain "not rows" and inflate agreement).
- Cohen's κ for each pair (Seb-Chris, Seb-agents, Chris-agents) on the 18 calls; κ reported as null if both raters give
  one same call to every picture. Raw agreement out of 18 for each pair.
- **Cross-page (depth_w):** Chris vs the agent majority on depth_w's 5 DEPTH-READ-15 level pictures (arms ctrl, m5, p5,
  m10, p10; agent call = rows if rows × 2 > valid readers in
  `[private path][internal item]/dr15_result.json`): agreement count only. Computed only after
  depth_w has its own scoring done with both raters. The other depth_w pictures (blanks, s214732, 10 mm, calibration
  pair) are **not computed** (no per-picture agent blank calls on disk, or already counted here).
- **ANCHOR-READ** is not used: that item was dropped (Sebastien's choice C), so its pictures were never rated.
- depth_w's own repeat check (`preregs/depth_w.md:35-37`) is reported alongside, not reused as a test.

## Stage 0 (sanity checks first; `hf.py stage0`, seconds, run by `job.sh` before anything else)

| Check | Bar | Fallback if it fails |
|---|---|---|
| a. partsheet_tolerance key | 18 pictures, 8 blanks + blank09 + calib | INCONCLUSIVE by Stage 0 |
| b. Sebastien's file | sha256 = `seb_ratings_sha256.txt`; 18/18 ids match the key | `loop.py human`: blinding or input changed, no scoring |
| c. Sebastien's file untracked | `git ls-files --error-unmatch` fails | `loop.py human`: his answers may be visible to Chris |
| d. Page unchanged | `humantol_rating.html` tracked and equal to HEAD | `loop.py human`: Chris must rate the committed page |
| e. Agent majority | 3 valid readers per picture, 0 ties; 5 disagreements with Sebastien; Sebastien valid | INCONCLUSIVE by Stage 0 |
| f. Outputs hidden | `humanfloor_detail_key.json`, `humanfloor_result.json`, `humanfloor_status.json`, job log all git-ignored | fix the item `.gitignore`, then rerun |
| g. Prereg timing (at score time) | Chris's file `when` later than this file's first commit | the numbers are reported as **descriptive only**, never as a verdict |
| h. Chris's file (at score time) | 18/18 ids match the key, each answer rows / strokes / nothing; Chris valid | file incomplete → UNDECIDED; Chris invalid → UNDECIDED (that is the finding) |

- Check g is a proxy: git's commit time, not push time. The loop pushes this file right after the commit; Chris rates
  on Thursday.
- The scorer self-test (`hf.py selftest`) runs first: every (k, m) of the 6 × 14 grid, the m = 2 corners at k = 0, 1, 4, 5,
  84 synthetic answer sets, invalid Chris (calibration not rows; 2 blanks rows; blank09 counted), κ edge cases, the sign
  test floor, short / mismatched / unknown-answer files. Planner run: pass, 0 failures
  (`[private path]`). Stage 0 a-f dry run: all pass.

## Outputs, blinding, budget

- Per-picture three-reader table: `[private path]`
  (git-ignored). Counts: `humanfloor_result.json` (git-ignored) and
  `[private path]` (counts only; pushed after
  Chris has rated). Nothing per-picture reaches stdout or a committed file before both humans have rated.
- Seeds: none (no sampling). Compute: CPU, seconds; GPU no. Human time: 0 extra (Chris's partsheet_tolerance rating is already
  planned).
- **Kill date: 2026-10-15** (same as depth_w). No valid Chris partsheet_tolerance file by then → INCONCLUSIVE (no second human).
- Result: the item file, the authors' private work log pointer, FACTS.md counts.
