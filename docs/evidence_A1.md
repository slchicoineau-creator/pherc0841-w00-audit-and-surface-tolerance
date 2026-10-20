# Evidence, group A1: human-read tolerance tests (outline rows 2, 3, 8 and "Known-window ceiling")

Outline: `git show 40f0e4211:submission/READABLE_SURFACE_BUDGET_OUTLINE.md`. Evidence commit: `60b819bd` (This audit checked that version; its WORDING_FLAGS were accepted by Chris and applied in outline cf541ce98, 2026-10-20.)
(the private repository). "V Lnnn" = line nnn of that test's item file at 60b819bd. Every script is in `reproduce/`, reads
only `data/<test>/` (inputs listed with sha256 in `docs/manifest_A1.json`), prints counts and labels only, and exits 0 only
when every expected value matches. All six were run on 2026-10-18 from outside the repo folder: **all exit 0**.

## HUMAN-TOL + HUMAN-TOL-SCORE (`reproduce/humantol.py`): MATCH
- Outline: row 2 (and the ceiling section through CM2-READ below).
- Prereg: `standalone/preregs/partsheet_tolerance.md`, `standalone/preregs/partsheet_tolerance_score.md`.
  Item: `[private path]`. Judge script: `checks/20261006-10-*/judge_rescore.py`.
- Verdict: **PASS**, branches (ii) C70 + L70 (V L257, L267). The preregs define no PASS rule of their own; the Judge's PASS
  means "a pre-registered verdict was obtained". The script reproduces the branches and quotes the label without computing it.
- Rating dates (US Central): Sebastien 2026-10-03, Chris 2026-10-06. These match the outline's "Sebastien 10-03, Chris 10-06".
- Numbers: L70 and C70 rows for both (V L313-316); H70 split; H50 not rows for both (V L316); L85, C85 and L100 rows for both; L55 split.
  Agents read only L100 and C85 (V L268-269). Rating sha prefixes f81d3a3c / b647c0aa match (V L266); Sebastien's file also
  matches the tracked `[private path]`.
- C70 render offset: `tol20b/tiles.json` (60b819bd) gives level offset −22 layers. At 2.405 µm per layer (FRESH-WRAP prereg
  L52-53: 20 layers = 48.1 µm) that is −52.9 µm, so the outline's "about −53 µm" holds. **Wording note:** the verdict's
  proposed BRIEF line (V L314) says "C70, at −22 µm". That line is wrong (it should say −22 layers). The outline already
  carries the corrected "−22-layer … about −53 µm" (Chris's C1 fix).

## HUMAN-FLOOR (`reproduce/humanfloor.py`): MATCH
- Outline: row 8. Prereg `standalone/preregs/human_vs_agent.md`; item `20261005-14-human-floor-is-the-agent.md`.
- Verdict: **FAIL = HUMANS-NOISY** (V L208).
- Numbers: k = 3 of 5 and m = 0 of 13 (V L218). Agreement out of 18: Sebastien-Chris 16, Sebastien-agents 13 (so 5/18
  disagreements), Chris-agents 15. κ Sebastien-Chris 0.769, which rounds to 0.77 (V L218-219). Agents said "not rows" where
  a human said rows on 5 of 5 (Sebastien) and 3 of 3 (Chris) disagreements, and never the reverse (V L223-225).

## CM2-READ (`reproduce/cm2read.py`): MATCH
- Outline: row 3 and the ceiling section. Prereg `standalone/preregs/depth_w.md`; item `20261005-07-cm2-read-can-a-blind-hum.md`.
- Verdict: named outcome **WIDE-OUT**; loop verdict FAIL against the agents' depth budget (V L288).
- Numbers: both raters valid, outward 24 and inward 24, so "≥ 24 µm on both sides" (V L300-305). s214732 ROWS for both.
  The raters agree on 14/14 pictures at 20 mm and 4/8 at 10 mm.
- Ceiling count: surface pictures = HUMAN-TOL's 8 levels + CM2-READ's 6 at 20 mm + 6 at 10 mm = 20.
  Sebastien said rows on 7 + 6 + 6 = **19/20**; Chris on 5 + 6 + 2 = 13/20 (V L313-315, Judge finding 5). Not-rows calls on
  HUMAN-TOL surface pictures: Sebastien 1/8, Chris 3/8. The 20 are page showings, not 20 different images: CM2-READ's
  20 mm control is byte-identical to HUMAN-TOL's L100 (HUMAN-TOL-SCORE verdict finding 4). The count matches the verdict
  either way.
- Not checked here: the "~66 µm inward" for s214732 comes from another item's check
  (`checks/20261004-33-depth-read-does-p-itself/planner_sign.json`). Only the citation (V L306-307) was confirmed.

## FRESH-WRAP (`reproduce/freshwrap.py`): MATCH for the reads; the r values come from saved files
- Outline: row 3. Prereg `standalone/preregs/depth_s022814.md`; item `20261006-02-fresh-wrap-on-s022814-s.md`.
- Verdict: **PASS = CONFIRMED (WIDE-HOLDS, two raters)** (V L245).
- Numbers: ±24 µm rows for both (WIDE-HOLDS each). Guards rows 0/1 and 1/3, blanks 0/4 (V L253). At ±48 µm (descriptive,
  Run L230, V L263): Chris out48 (outward) strokes, in48 rows; Sebastien both rows. That is 1 not-rows call out of 8 depth
  calls. Arms are mapped by name: out = −layers, because raw +o points inward on the organizers' surfaces (prereg L47-53).
- r vs ctrl map: out24 0.868, in24 0.851, out48 0.689, in48 0.691, so "0.85-0.87" and "0.69" hold (V L256).
  **Taken from a saved Judge output.** The ink maps (`maps/*.npy`) exist locally but break the package's data rule
  (no volumes, nothing over 1 MB). So the values come from the Judge's saved `judge_rescore.json` @60b819bd
  (kind "derived"); the script checks only that they are consistent with each other. The "62-layer (~149 µm) slab" is a property of
  the reader (V L255) and is not recomputed.

## RAW-READ-9H (`reproduce/rawread9h.py`): MATCH (RP comes from a saved file)
- Outline: ceiling section; row 2 "Chris rejected the same H50 again on 10-08".
- Prereg `standalone/preregs/grown_field.md` + amendment 1 (`checks/20261007-07-*/amend1_guard_rule.md`).
  Item `20261007-07-raw-read-9h-does-the-sta.md`.
- Verdict: **PASS = GROWER-READS (two raters)** (V L415, L430). The script also confirms the Runner's outcome in its result file.
- Numbers: agents rows 0/5 on the grown tile and 5/5 on the control (from `r9_screen_result.json`; V L446).
  Frozen row score RP 0.399 vs 23.338, ratio 0.017 (V L443-444). **RP is taken from a saved Judge output:** the PNG tiles and `rs20.py` it
  needs exist locally but break the package's data rule, so the value comes from the Judge's saved `judge_rp_out.json` @60b819bd.
- Chris's guard sha equals HUMAN-TOL's `tolholes/tiles/level_H50.png` (b650c087…), and his call on it was not rows. This
  confirms the outline's "rejected the same H50 again on 10-08" (his rating is stamped 2026-10-08T20:37Z).
- Not portable: the Judge's check that every page picture matches its key bytes (it needs the page HTML and the tiles).

## NODE-FILL-READ + NODE-FILL-REREAD (`reproduce/nodefill.py`): MATCH
- Outline: row 2 holes sentences; row 8 "50 % holes … not a usable guard".
- Preregs `[private path]`, `[private path]`.
  Items `20261008-18-node-fill-read-with-the.md`, `20261010-04-node-fill-reread-with-th.md`.
- NODE-FILL-READ: **VOID** with 1 of 2 raters valid (V1 L293). The fresh 50 % holes guard H50f was called rows by 1 of 2;
  sha prefixes d42c180f / 1ea995fd (V1 L298-300).
- NODE-FILL-REREAD: **VOID** with 0 of 2 valid (V2 L286). Its guard is HUMAN-TOL's H50 file itself (md5 49968cf2). Both raters
  called it rows (2/2); each failed only that check; L100 was rows 2/2 and the blanks not rows 4/4 (V2 L291-298). On HUMAN-TOL
  both had called the same file not rows (2/2). Calls were stable between sittings for 6/6 (Sebastien) and 4/6 (Chris) (V2 L305-307).
  Sha prefixes 3d76bcb8 / 01ce291f. Both raters rated on 2026-10-10 US Central (Chris's stamp 01:47Z is 10-11 UTC; V2 L318),
  which matches the outline's "on 10-10".
- No arm call (NF30, NF45, BL45) is printed. Both page keys are still unreleased (the Judges said "no third viewing").

## Not covered by A1 (other groups)
FULL-HOP-W's H50n and TOL-814's H50_814 holes calls (row 2), and the exposure counts (SPIRAL-READ-0841) in the ceiling section.

## Manifest notes
- "local only" files are git-ignored (keys, ratings) or untracked in the private repo. Each was copied byte for byte, so its
  sha256 equals the source. Files marked 60b819bd were taken with `git show 60b819bd:<path>`.
- `tile_hashes.json` (in rawread9h and nodefill) holds sha256 and md5 of three PNG tiles, computed on 2026-10-18 from the
  local working tree. The images themselves are not copied.
- The HUMAN-TOL key and ratings are copied into four test folders (same sha256).

## Cautions
- Several inputs here are page keys or rating files that the Judges kept out of git: HUMAN-TOL, CM2-READ, FRESH-WRAP,
  RAW-READ-9H and both NODE-FILL keys. They are released with both authors' OK, file by file.
- HUMAN-TOL's H50 picture served as a guard in RAW-READ-9H and NODE-FILL-REREAD. RAW-READ-9H amendment 1 also drew
  Sebastien's guard from his earlier rejected pictures. **Unverified:** whether any HUMAN-TOL / CM2-READ picture is still a
  guard or key in a live test. Checking that would mean opening paths this brief forbids.
