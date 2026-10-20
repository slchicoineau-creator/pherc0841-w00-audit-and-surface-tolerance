> **Scrubbed public copy** (public name `spiral_field`). The original was first committed to the authors' private repository at `351bc496e` (2026-10-13T15:02:26Z). Timing: Amendment 3 (no guard picture on one rater's page): pushed after both pages were built, but before either rating (its Judge's check). Timestamps live in a private repository; ask the authors for a verification. Scrubbing removed mentions of non-public scrolls and local paths (paths into the authors' private repository read `[private path]` and do not resolve) and replaced internal item ids and test names with public slugs (unmapped internal ids read `[internal item]`); the scientific text is otherwise unchanged.

# Amendment 3 to preregs/spiral_field.md (spiral_field): no guard picture on Sebastien's page

- **Date:** 2026-10-13 (CDT), written by the Runner station on Sebastien's answer A (2026-10-13 09:50, control panel). Before any page
  exists (cache/ is empty; job 2 stopped at the guard step with exit 78). To be copied to `[private path]` and pushed by the Planner / main
  session before either page is shown to a rater (the Runner may not write `[private path]` or commit).
- **Why:** the Guard rule (prereg "Guard") found no eligible picture for Sebastien (eligible 0: a sibling test took his last one since the
  Planner's check). BRIEF lesson 20 forbids a burned guard. His choices were A (no guard, stricter blank rule), B (a twice-seen picture),
  C (Chris only), D (drop); he chose **A**.
- **Change (Sebastien's page only; Chris's page and every other rule are unchanged):**
  1. His page has **8 pictures** (A1, A1-blank, A2, A2-blank, C, C-blank, calib, blank09; 6 if A2 is dropped by Stage 0). No guard
     tile is built for him, no guard is drawn (seed 20261044 unused), and the Stage 0f frame check covers the pictures that exist.
  2. His class: VOID if a picture is unanswered, calib is not rows, or his answers pre-date the page. INVALID if more than 1 empty
     picture (C-blank, A1-blank, A2-blank, blank09) is called rows. UNINFORMATIVE-C if C is not rows.
     **VALID only if he calls EVERY empty picture "not rows"** (strokes or nothing). Exactly one empty picture called rows =
     **VALID-LENIENT** (his "rows" calls do not count toward a READS outcome; his "not rows" calls still count), the same as a
     rater who calls the guard rows.
  3. Outcome rules (NO-ROWS / READS / READS-WITH-PICK / SPLIT / INCONCLUSIVE / UNINFORMATIVE) and the kill date are unchanged.
     Consequence kept in plain sight: without a guard, a "rows" read by him on an arm cannot be told apart from a lenient habit
     except through the empty pictures; so a READS outcome is weaker than the original design, while NO-ROWS (robust direction) is as strong.
- **Code:** `sr07.py` (`NOGUARD`, `rater_class(..., noguard)`, `guard`, `items`, `page`, `score`); selftest 38 cases pass (10 new: noguard
  VALID / LENIENT / INVALID / VOID / UNINFORMATIVE-C). `job3.sh` (CPU) rebuilds the guard step and writes both pages from job 2's kept maps.
- **Chris:** his guard is re-drawn at rebuild time from the current pool by the same frozen rule and seed (prereg: counts recomputed
  at page-build time); the earlier draw was never shown to anyone.
- **Lesson 21:** unchanged: the question the raters see names only the time (~4 min) and the page order, never the controls.
