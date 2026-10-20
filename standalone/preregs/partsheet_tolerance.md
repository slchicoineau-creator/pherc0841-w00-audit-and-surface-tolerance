> **Scrubbed public copy** (public name `partsheet_tolerance`). The original was first committed to the authors' private repository at `724557744` (2026-10-03T03:44:03Z). Later commits to the same file: `db7081921` (2026-10-03T03:44:22Z); `509b98eb1` (2026-10-05T23:29:06Z). Timing: Original and amendment 1 committed before any rating. Amendment 2 (secondary agent-vs-human analysis) was committed on 2026-10-05, after the first rater's 2026-10-03 ratings and before the second rater's and before any scoring; the file itself discloses this. Timestamps live in a private repository; ask the authors for a verification. Scrubbing removed mentions of non-public scrolls and local paths (paths into the authors' private repository read `[private path]` and do not resolve) and replaced internal item ids and test names with public slugs (unmapped internal ids read `[internal item]`); the scientific text is otherwise unchanged.

# Pre-registration: partsheet_tolerance, do human eyes read the TOL tiles the agent readers did not? (PHerc0841, known text)

- **Date:** 2026-10-02 (late evening, CDT), pushed before any human rating exists. Owner: Sebastien's side. Public data.
- **Why:** the surface bar (≥ ~85 % of a 20 x 12 mm field on the right sheet) and "holes don't read" come from Claude agent
  readers (TOL-20, TOL-20b, TOL-HOLES; the authors' private work log). Agreed step 1 of `24_Top5_Sheet_Tracing_Approaches.md`: if human
  eyes read rows at ~30 % wrong layer or ~30 % holes, the bar relaxes and "trace only where confident" comes back.
- **Raters:** Sebastien and Chris, independently, each on his own machine, before seeing the key or each other's answers.
  Neither has seen these tiles. Both know the tests' designs and the agents' summary results, but not which picture is which.

## Tiles (all exist already; no new render, no new model run)

- **8 level tiles** (the "rev" map each agent level was rated on): TOL-20 L100, L85, L70, L55 (dispersed ~1 mm hops,
  0/15/30/45 %); TOL-20b C85, C70 (clustered hops, 15/30 %); TOL-HOLES H70, H50 (clustered holes, 30/50 %).
  Note: C70's tile is at depth −22 (the old p99 pick); every other level tile is at +0.
- **8 blanks** (each level's "fwd" map), **1 calibration** (FORMAT-20 0009B known rows, `format20` f_05) and its blank
  (f_06). 18 pictures, 800 px, from the existing PNGs (stored as JPEG quality 92 so the page fits the 1 MB push limit).
- **Order, hardest first** (so the clearer versions of the same text cannot prime the harder ones), shuffled inside
  blocks with `numpy.random.default_rng(20261002)`:
  - Block A: L55, H50, C70, L70, H70 + their 5 blanks;
  - Block B: L85, C85 + their 2 blanks;
  - Block C: L100 + its blank, calibration, calibration blank.
- Same wording and answers as the agents and the earlier blind pages ("Rows / letters", "Strokes, no rows", "Nothing"; cautious
  when unsure), field described as about 20 mm tall and 12 mm wide. Page: `[private path]`; the key
  stays on Sebastien's machine and is pushed only after both have rated.

## Scoring (fixed now)

- **Valid rater:** calibration = "rows" and at most 1 of the 9 blanks = "rows". A level's call counts only if that
  level's own blank is not "rows" for that rater.
- **Per level:** "reads for humans" if both valid raters say "rows"; "split" if one does; "does not read" if neither.
- **Decision:**
  - **H70 reads for humans** → holes at ~30 % are tolerable to human eyes: "trace only where confident" returns as a route.
  - **C70 or L70 reads for humans** (and not for agents) → the wrong-layer bar relaxes toward ~30 % for human reading.
  - **None of H70 / C70 / L70 reads** → the agents' bar stands for humans too: ≥ ~85 % on the right sheet.
- Descriptive only: agreement with the agents' calls level by level.
- Results: the authors' private work log and the authors' private team issue.

## Amendment 1 (before any rating exists)

- JPEG quality 92 gave a 1,005,539-byte page, just over the 1,000,000-byte push limit; quality is **90** instead.
  Nothing else changes (same tiles, order, rng, wording, scoring).

## Amendment 2 (2026-10-05 evening, before any scoring; Sebastien accepted the strategy review's change 2)

- **Why:** the loop's new objective is "judged by reading". Those reads come from Claude agent readers that have
  never been checked against humans (`[private path]` §2 point 4, §6 change 2).
- **New, secondary analysis: do Sebastien's existing ratings agree with the agent readers?** The primary
  two-rater scoring above is unchanged and still waits for Chris.
  - **Agents' call per picture:** the majority of the 3 valid agent readers who rated that exact tile file:
    - TOL-20 L100/L85/L70/L55, TOL-20b C85/C70 and TOL-HOLES H70/H50 come from each test's `*_result.json`;
    - each level's blank uses those readers' "blank" answer;
    - the calibration and its blank use FORMAT-20's calib and blank09 (r1-r3).
    - C70's tile is the −22 tile, and it is the same file the agents read.
  - **Disagreement is binary:** "rows" vs not "rows". Strokes vs nothing does not count.
  - **Sebastien's validity is checked first,** with the rule above: calibration = rows and ≤ 1 of 9 blanks = rows.
    - If he is invalid, that is reported as the finding and nothing else is scored.
  - **Decision (threshold from the review):** disagreement on ≥ 2 of the 18 pictures means agent reads become
    **screening only**. Every "judged by reading" verdict then needs human reads. With ≤ 1 they stay as the reading
    instrument.
- **Blinding:**
  - Only the counts are pushed: valid yes/no, number of disagreements, decision.
  - The per-picture results stay git-ignored on Sebastien's machine until Chris has rated.
  - Sebastien is asked not to discuss any picture with Chris.
- **Disclosure:**
  - While checking the files' format for this amendment, Claude printed both the key and Sebastien's answers before
    writing this text.
  - The threshold (≥ 2/18) and the comparison were already written by the independent review before that.
  - The binary rows / not-rows reading follows this prereg's own scoring, which counts only "rows".
