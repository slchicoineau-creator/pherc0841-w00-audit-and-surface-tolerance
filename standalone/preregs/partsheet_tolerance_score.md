> **Scrubbed public copy** (public name `partsheet_tolerance`). The original was first committed to the authors' private repository at `16247fbbb` (2026-10-07T04:27:43Z). Later commits to the same file: `47d55bcb5` (2026-10-07T04:28:38Z). Timing: Both commits before any output (its Judge's check). Timestamps live in a private repository; ask the authors for a verification. Scrubbing removed mentions of non-public scrolls and local paths (paths into the authors' private repository read `[private path]` and do not resolve) and replaced internal item ids and test names with public slugs (unmapped internal ids read `[internal item]`); the scientific text is otherwise unchanged.

# Pre-registration: partsheet_tolerance scoring, the 10-02 two-rater Decision of partsheet_tolerance, scored once (PHerc0841, known text)

- **Date:** 2026-10-06 (late evening, CDT), pushed before the primary partsheet_tolerance scoring has been computed by anyone.
  Owner: Sebastien's side. Station loop item `partsheet_tolerance`. Public data.
- **Why:** `preregs/partsheet_tolerance.md` "## Scoring" fixed a two-rater rule and a 3-branch Decision on 10-02, before
  any rating. Sebastien rated 2026-10-03T14:00Z, Chris 2026-10-06T16:29Z. Amendment 2 (agent agreement) and human_vs_agent
  (rater agreement) have been scored; the primary Decision has not. It decides whether package (b) row 2 ("how much damage
  still reads", `submission/READABLE_SURFACE_BUDGET_OUTLINE.md:19`) rests on two blind humans or on agent readers only.
- **Human time:** none (both ratings exist). **Compute:** CPU seconds, no GPU.

## Data (all exists; nothing new is rendered, rated or read)

- Key: `[private path]` (git-ignored, Sebastien's machine): 18 ids p01-p18, kinds `level` (8),
  `blank` (8, one per level), `calib` (1), `blank09` (1).
- Ratings (untracked, not ignored; never staged by any station), pinned now:
  - `ratings/seb/humantol_ratings.json` sha256 `f81d3a3cbc05fde7ee448f872551587246383f90df9cfd422da299d9e4971ed9`
    (= `[private path]`, pushed before Chris rated);
  - `ratings/partner/humantol_ratings.json` sha256 `b647c0aa40c701f7d8313459b66fb2c7bff41f43a478c6a35a0f131f1ce1049e`
    (hashed by the Planner on 10-06 without printing any answer).
- Agents' level calls (descriptive and for the "and not for agents" clause): `[private path],tol20b,tolholes}/*_result.json`
  "per_level" → valid readers' "level" answers.
- No leak path: the rule, the files and the key are all fixed; the scorer reads nothing else.

## Scoring (verbatim from the 10-02 prereg, edge cases settled now)

- **Valid rater:** calibration = "rows" and at most 1 of the 9 blanks (8 level blanks + the calibration blank) = "rows".
- **Masked call:** a rater's call on a level counts only if that level's own blank is not "rows" for that rater. A masked
  call is treated as not "rows" and reported as "masked" (so that level can be at most "split").
- **Per level:** "reads for humans" if both valid raters say "rows" (unmasked); "split" if exactly one does; "does not read"
  if neither. "Split" is not "reads": it fires neither (i) nor (ii) and counts as not reading for (iii).
- **Agents' call per level:** the TOL tests' own rule, binary: the level "reads for agents" if ≥ 2 of its valid readers in
  the `*_result.json` said "rows" (not `agentcheck.py`'s three-way majority).
- **Decision (10-02 text):**
  - **(i)** H70 reads for humans.
  - **(ii)** C70 reads for humans and not for agents, or L70 reads for humans and not for agents. If a level reads for both
    humans and agents in the files, (ii) does not fire for it (literal reading) and this is reported as a contradiction
    with the record (TOL-20 / TOL-20b agents: not rows).
  - **(iii)** none of H70, C70, L70 reads for humans.
  - (i) and (ii) can both fire. L100, L85, C85, L55, H50: per-level calls, descriptive.
- Descriptive only: level-by-level agreement with the agents; the line "Sebastien is the more lenient reader (rows on
  19/20 surface pictures, `[private path]`), so under the both-say-rows rule each level's call rests in
  practice on the stricter rater."

## Amendment to the 10-02 text (narrows claims only; no output exists)

- **(a)** One H70 clause about another scroll is not used (it is removed from this public copy). Every line is about 0841 known text.
- **(b)** No "with / without Sebastien" split: his answers were sha-pinned on 10-03 and the rule fixed on 10-02, both before
  amendment 2's disclosure (10-05), so the exposure noted there cannot bias them. Removing a rater would turn the
  registered two-rater rule into a one-rater rule. One verdict, as written.

## Allowed wording (fixed now, applies at release)

- Every line: "on one 20 × 12 mm known-text window of PHerc0841, two blind humans …". One picture per level, n = 2 raters.
- Every dose: "as built from w00" (e.g. "~30 % clustered hops off w00's sheet"); w00 is ~9 in 10 right within 75 µm, so
  no claim about the true sheet's tolerance in general. C70 is worded "at −22 µm" (its tile's depth; others at +0).
- Not allowed: "humans tolerate 30 % holes" in general.
- What each outcome changes (at release): (i) row 2 = "30 % clustered holes (as built from w00) still read for two blind
  humans (agents: no)", and the human-minutes route "trace only where confident, leave hard folds as holes" returns;
  (ii) row 2 bar = "≥ ~70 % on the right sheet (as built from w00)"; (iii) row 2 = "≥ ~85 % right sheet, confirmed by two
  blind humans". Every outcome: row 2's "who read it" becomes "two blind humans (pre-registered 10-02)"; BRIEF B1's
  tolerance line is rewritten. L85 by call: reads → strike "dispersed 15 % hops kill rows"; split → a one-rater line;
  does not read → "kills rows for two blind humans".

## Stage 0 (sanity check first; exit 78 on any failure, CPU seconds)

- (a) Both ratings files' sha256 equal the two hashes above.
- (b) Both files hold 18 answers, ids = the key's ids, every answer in {rows, strokes, nothing}.
- (c) The key is present with 8 levels, 8 matching blanks, 1 calib, 1 blank09.
- (d) Both raters valid by the rule above.
- (e) The three agent result files exist and hold H70, H50, C85, C70, L100, L85, L70, L55.
- (f) `git check-ignore` confirms the result and detail paths are ignored, and neither ratings file is staged.
- Fallback (pre-written): "partsheet_tolerance unscorable: <failed check>", nothing about levels; item INCONCLUSIVE
  (UNINFORMATIVE by Stage 0). The Critic's dry run already passed (a)-(c) for Sebastien's file; chance of no answer ~0.5 in 10.

## Blinding and release (depth_s022814 hold)

- Per-level calls, fired branches and agent comparison go only to git-ignored
  `[private path]` and `..._detail_key.json`.
- Every other channel (job stdout, run logs, the item's Run / Verdict sections, FACTS.md, the pushable
  `[private path]`, any question to a human)
  says only "scored: yes / both raters valid / sealed until release", and must not hint at which branch fired.
- **Release** (the scorer's `release` step writes the verdict lines only when one holds):
  (a) the depth_s022814 item is digested, closed or killed (all its raters done, or the test dropped; one rater's file alone
  is not enough, since its rater choice may be both humans); (b) the date is 2026-10-13 or later; (c) Sebastien picks
  "release now" in a lettered question.
- After release: verdict in the authors' private work log, one FACTS.md line, BRIEF B1 / outline row 2 / BOARD rewrite by the Planner
  digest. The the authors' private team issue post is the main session's, not a station's.

## Seeds, budget, kill date

- No randomness. CPU < 1 min. Scored the day the job runs; released by 2026-10-13 at the latest (kill date for the hold).
