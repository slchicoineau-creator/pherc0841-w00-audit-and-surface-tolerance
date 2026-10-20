> **Scrubbed public copy** (public name `grown_field`). The original was first committed to the authors' private repository at `2480a4044` (2026-10-13T02:55:46Z). Timing: Amendment 1 (guard rule for the second read). Committed 66 s after the second-read page was built; the page was shown to the rater only after the push, before his rating (its Judge's check). Timestamps live in a private repository; ask the authors for a verification. Scrubbing removed mentions of non-public scrolls and local paths (paths into the authors' private repository read `[private path]` and do not resolve) and replaced internal item ids and test names with public slugs (unmapped internal ids read `[internal item]`); the scientific text is otherwise unchanged.

# grown_field: amendment 1 (per-rater guard picture for read 2)

- **Date:** 2026-10-12 (evening). Made at Sebastien's decision (main session, 2026-10-12 21:50). Written by the Runner station of item
  `grown_field`; filed under `[private path]<item>/` because that folder is committed and pushed by
  the loop's own sync. It amends `preregs/grown_field.md`. No page built under this amendment has been shown to a rater when this
  text was written. The page is shown only after this file is on `origin` and its sha256 matches the one recorded in the item's `## Run`.
- **Why:** BRIEF lesson 20 and KILLED row NODE-FILL-REREAD. partsheet_tolerance's H50 (the guard of the original pre-registration) was called rows by
  BOTH raters on its second viewing (NODE-FILL-REREAD, 2026-10-10). Every 50 % holes guard on the S2 window since partsheet_tolerance has been rows for at
  least one rater. A fresh holes picture on S2 is not calibrated either.

## What changes

1. **Sebastien's read 2 uses his own guard picture.** For Sebastien (only), the picture in role `guard` is one picture of this window that
   **he himself already called not rows, blind**, chosen by the frozen rule below. Its identity lives only in the git-ignored
   `guard_seb_key.json`. The other five roles, the page order seed (20261078), the caption and the scorer's class logic are unchanged.
2. **Chris's read 1 stands as pre-registered** (rated 2026-10-08, sealed; guard H50). Verdict text carries this label: Chris's guard (H50) was
   rated before by both raters and was called rows by both on 2026-10-10 (after his read), so it checked a "rows to everything" rater
   only loosely. His page and key entry are not rebuilt (hash-checked by `job3.sh`).
3. **Question text (lesson 21):** the question Sebastien sees names only the time and the page. It names no control, guard or re-shown picture.

## Frozen rule for Sebastien's guard (`seb_guard_rule.py`, same folder; deterministic)

- **Pictures:** the `level` pictures Sebastien rated blind on the S2-window pages partsheet_tolerance, depth_w, COPY-IN, fullhop_w, NODE-FILL-READ,
  NODE-FILL-REREAD (his saved ratings in `ratings/seb/` and the item folders). One picture = one exact PNG (sha256). A picture with no saved
  file (depth_w, COPY-IN) is its own picture. fullhop_s022814, line_spacing and the ENS pages are other windows and are not counted.
- **Eligible:** he answered strokes or nothing on **every** showing, and it was shown to him **at most once** before.
- **Order:** "strokes" pictures before "nothing" pictures, then by (page, picture id). One picture is drawn with
  `numpy.random.default_rng(20261012).integers(n)` over the first non-empty group.
- **Zero eligible pictures:** exit 78; the Runner asks Sebastien with lettered choices. A burned picture is never used.
- Counts at the time of writing (aggregate only): 30 distinct level pictures; 2 eligible (both "strokes", one earlier showing each);
  H50 and BL45 are not eligible (each was shown to him twice; H50 was called rows on its second showing).

## Showings before this read (per rater, counts only)

| Rater | His guard picture | Readable control (exact w00 control file) | Calibration pair |
|---|---|---|---|
| Sebastien | 1 earlier showing (the picture the rule draws) | 1 (COPY-IN, called rows) | at least 4 (partsheet_tolerance, depth_w, COPY-IN, fullhop_w) |
| Chris (read 1, 10-08) | H50: at least 1 earlier showing (partsheet_tolerance); 10-10 viewing came after his read | seen on handfix | seen before |

The ladder picture of this window (L100) was shown to Sebastien 4 times; it is not the control and not a guard.

## Unchanged

Outcome classes, Chris sets the class, Sebastien can only upgrade, kill date 2026-10-19, labels "one window, known text" and "one grow per
seed", READS = "reads rows; the read does not show the sheet". Ratings, keys and results stay in git-ignored files. No agent read decides.
