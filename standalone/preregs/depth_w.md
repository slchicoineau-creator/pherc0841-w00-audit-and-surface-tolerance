> **Scrubbed public copy** (public name `depth_w`). The original was first committed to the authors' private repository at `da2bf1654` (2026-10-06T01:07:02Z). Later commits to the same file: `05d58d701` (2026-10-06T01:09:30Z). Timing: Original and amendment 1 committed and pushed before any output (its Judge's check). Timestamps live in a private repository; ask the authors for a verification. Scrubbing removed mentions of non-public scrolls and local paths (paths into the authors' private repository read `[private path]` and do not resolve) and replaced internal item ids and test names with public slugs (unmapped internal ids read `[internal item]`); the scientific text is otherwise unchanged.

# Pre-registration: depth_w, do human eyes confirm the agents' depth budget around P, s214732's "no rows", and the 20 mm field size? (PHerc0841, known text)

- **Date:** 2026-10-05 (evening, CDT), committed before any tile copy, 10 mm window, page or human rating of this test
  exists. Owner: Sebastien's side. Public data. Station loop item `depth_w`.
- **Approved through `HUMAN.md`:** Sebastien chose option A on 2026-10-05 19:41: "build a second blind page; Chris rates it
  Thursday right after the tolerance page, and you rate it too only if you never saw these depth pictures with their names".
- **Why:** the October package (b) "readable-surface budget on PHerc0841" states a depth line (outward < 12 µm,
  inward ≥ 24 µm around P) and a field size (rows need ~20 × 12 mm). Both come from Claude agent readers only (DEPTH-READ,
  DEPTH-READ-15, READ-S214732, FORMAT-20 / GROWN-TILE READ). Since partsheet_tolerance amendment 2 (Sebastien vs agents disagree on
  5 of 18 pictures), agent reads are screening only. The only human data at 10 mm (earlier tiles) already contradicts the agents'
  "10 mm = strokes": Sebastien read 10/20 0841 known-text 10 mm tiles as rows (blanks 0/20).
- **Scope of any claim:** the budget is measured from **P's own +0** (the team mesh w00 over the known-text window W), not
  from "the inked layer". Every package sentence must say "around the team surface, in this one window". P is the readable
  control here, not a position key (truth rule 2026-10-05).

## Pictures (22; all from saved files, no new model run)

- **20 mm (FORMAT-20 S2 window on P, 800 px long side):** DEPTH-READ's tiles of P at +0 (ctrl), −12 µm (m5), −24 µm (m10),
  +12 µm (p5), +24 µm (p10), each with its blank (reverse depth order, same offset) = 10 pictures, the exact bytes the
  DEPTH-READ / DEPTH-READ-15 agents read (fingerprint `eb6c4179…`). Sign: + = outward (away from the scroll centre),
  − = inward, toward s214732 (`[private path][internal item]/planner_sign.json`:
  99.9 % of P's normals point away from the centre; s214732 sits at −66 µm). READ-S214732's s214732 level tile and its blank
  (2 pictures, the bytes its agents read).
- **10 mm (secondary):** three 4160 × 4160 px windows (9.996 mm at 2.403 µm), top / middle / bottom (offsets 0, 2080,
  4160 px inside the 20 mm window: 50 % overlap), x centred, cut from the **same saved maps** as the 20 mm level tiles
  (P: `[private path]`; s214732: `[private path]`, rule order rev), plus one
  blank per surface (middle window, fwd order, +0) = 8 pictures. Output 800 × 800 px, as GROWN-TILE's agent 10 mm tiles and
  the earlier human tiles.
  - **Contrast (Critic rule "same stretch"):** no tile in this chain uses a percentile stretch. Every tile, 20 mm and 10 mm,
    uses the same fixed mapping clip(0, 1) × 255, outside-data = 0 (`ws.py tile`), so the rule is met by construction.
    Stage 0 proves it by re-making the 20 mm tiles from the maps with the same function.
  - On the page every picture is shown 800 px wide, so a 10 mm window shows ~1.2× more map pixels per screen pixel than a
    20 mm tile's width; the 10 mm windows therefore carry more native detail per screen inch. Recorded, not corrected.
- **Calibration:** FORMAT-20's 0009B known-rows tile `f_05` and its blank `f_06` (2 pictures).
- **Overlap with partsheet_tolerance (Critic finding 2):** ctrl = partsheet_tolerance's L100 tile and f_05 / f_06 are on the partsheet_tolerance page.
  The pre-registered partsheet_tolerance page is not changed; this is a second page, rated in the same sitting **after** partsheet_tolerance.
  Chris's two calls on the identical control and calibration are a free repeat check: reported, never gating.

## Page

- Builder `[private path] build` (from `[private path]`): the standard
  page template, same three answers and wording as partsheet_tolerance and the agents ("Rows / letters", "Strokes, no rows",
  "Nothing"; cautious when unsure), JPEG quality 90 (85, then 80 if the page is over 1,000,000 bytes; if still over, the
  page goes to Chris outside git). Each picture carries a size line ("about 20 mm tall and 12 mm wide" / "about 10 mm × 10
  mm"), because the agents were told the field size.
- **Order, hardest first** (the same text is in every P picture, and Chris has just seen L100 = ctrl on the partsheet_tolerance page;
  the clear versions must not prime the hard ones), shuffled inside blocks with `numpy.random.default_rng(20261007)`:
  - Block A (10): p10, p5, m10, m5, s214732 levels + their 5 blanks;
  - Block B (8): the six 10 mm windows + 2 blanks;
  - Block C (4): ctrl level + blank, f_05, f_06.
  - This replaces the idea's draft order (10 mm first), which would have let the sharp 10 mm P windows prime the depth
    tiles. Any "rows" call may still be primed by the partsheet_tolerance page seen just before: recorded as a limitation.
- Key `cm2read_key.json`, tiles and Stage 0 numbers stay git-ignored. The **key and the partsheet_tolerance key are released only
  after Chris has rated both pages** (and Sebastien too, if he rates).

## Raters

- **Chris** first (Thursday 2026-10-08, right after partsheet_tolerance); the tile folders were never pushed, so he has not seen them.
- **Sebastien** only if he confirms in writing that he never opened these tiles or a report showing them with their labels;
  otherwise Chris alone, and every verdict line says "one rater".
- The rater who saves the ratings file names it `cm2read_<name>_ratings.json` in the item folder.

## Scoring (fixed now; `cm2.py score`, self-tested on synthetic answers before commit)

- **Valid rater:** all 22 answered; calibration f_05 = rows; at most 1 of the 8 surface blanks (6 at 20 mm, 2 at 10 mm)
  = rows; the confirmation above. f_06 (calibration blank) is reported, not gating (Critic's rule counts the 8 surface
  blanks; partsheet_tolerance's 9-blank rule is not used).
- **A level counts** only if its own blank is not "rows" for that rater (partsheet_tolerance rule); a level that does not count is
  "uncountable".
- **20 mm block (primary), per valid rater:**
  - VOID: ctrl not rows, or ctrl's blank rows, or invalid rater.
  - Outward line = furthest + tile that reads rows (none / +12 / +24); inward line = furthest − tile that reads rows
    (none / −12 / −24). A non-monotone pattern (+24 rows with +12 not; −24 rows with −12 not) keeps the furthest tile and
    is flagged.
  - **WIDE-OUT:** +12 or +24 reads rows → the agents' outward line is wrong; the package states the human line.
  - else **INCOMPLETE** if +12 or +24 is uncountable;
  - else **ASYMMETRIC** (agents confirmed): −24 rows → "outward < 12 µm, inward ≥ 24 µm";
  - else **ASYMMETRIC-SHORT:** −12 rows, −24 not → "outward < 12, inward 12-24 µm";
  - else **NARROW:** ±12 both not rows → "< 12 µm both sides";
  - (an uncountable inward tile needed for the call → INCOMPLETE, reported tile by tile).
- **Two valid raters:** per side the stricter (narrower) line, both printed; the outcome name follows the combined lines.
  A rater whose call is INCOMPLETE is reported tile by tile and the combined call uses the other rater ("one rater").
- **s214732 (B2), separately:** rows / not rows per rater (uncountable if its blank reads rows). All countable valid raters
  "not rows" → B2 human-confirmed; all "rows" → B2's agent-only line is removed; otherwise SPLIT.
- **10 mm block (secondary: unit of a timed tracing session),** per valid rater, k_P / k_S = P's / s214732's windows read
  rows (0-3): **1 cm² USABLE** if k_P ≥ 2 and k_S = 0; **20 mm ONLY** if k_P = 0 or k_S ≥ k_P; otherwise DESCRIPTIVE
  (e.g. k_P = 1, k_S = 0). Uncountable if either 10 mm blank reads rows. Two raters: a named unit only if both agree.
- Odds (Critic): first rater lands on a named answer ~75 %; ASYMMETRIC exactly as the agents read it ~40 %.

## Stage 0 (sanity check first; `job.sh`, ~2-5 CPU min, no human)

| Check | Bar | Fallback if it fails |
|---|---|---|
| a. DEPTH-READ tiles = the bytes the agents read | combined fingerprint = `eb6c4179…`; DEPTH-READ-15 copies md5-identical | `build --rerender`: re-make every 20 mm tile from the saved `.npy` maps with the same function; the page and the verdict say "re-rendered, not the agents' exact bytes" |
| b. Calibration pair | `format20_key.json`: f_05 = calib, f_06 = blank09 | stop, INCOMPLETE by Stage 0 (no valid rater possible) |
| c. s214732 tiles = what its agents read | sha256 of `tiles/level.png`, `blank.png`, f_05, f_06 = the only hashes of each kind in `reads214732/blind/` (`rs_key.json`) | as a. (`--rerender`) |
| d. 10 mm windows share the 20 mm tiles' map and mapping | re-tiling the four saved 20 mm tiles (P ctrl level/blank, s214732 level/blank) from the maps gives decoded pixels within 1 grey level | `build --drop10`: the 10 mm block is dropped (14 pictures), the primary stays; the 10 mm question stays open |
| e. 10 mm windows hold data | each of the 6 windows ≥ 90 % inside the data mask | as d. (`--drop10`) |
| f. Labelled files stay local | `tiles/`, `stage0.json`, key, result, ratings git-ignored | fix the item `.gitignore`, re-run |

Job exits 78 on any fail, with its numbers in `stage0.json` (git-ignored).

## Compute, seeds, kill date

- GPU none. CPU < 0.5 h. Humans: ~8 min per rater. Seed 20261007 (page order only).
- Kill date: 2026-10-15. No valid human rating by then → closed as INCONCLUSIVE (no human read); the package's depth and
  field-size rows stay marked "read by AI readers only".

## What each outcome changes

- **ASYMMETRIC:** package (b) may state "around the team surface, in this window: outward < 12 µm, inward ≥ 24 µm, human-read
  (one / two raters)"; BRIEF R4 / B1 depth line loses its agent-only tag.
- **ASYMMETRIC-SHORT / NARROW:** the package states the human line (narrower than the agents'); BRIEF R4 / B1 are rewritten.
- **WIDE-OUT:** the agents' outward line is wrong for humans; the package states the human line; BRIEF R4 / B1 rewritten.
- **VOID / INCOMPLETE:** the package's depth row stays "AI-read only".
- **s214732 rows:** B2 ("78 µm away reads strokes") loses its agent-only line; not rows: B2 human-confirmed.
- **1 cm² USABLE:** a timed tracing session may be scored on 1 cm² tiles; **20 mm ONLY:** it must be scored on a 20 × 12 mm
  field; DESCRIPTIVE: open.
- Results: item file, then the authors' private work log; tile-by-tile calls stay in git-ignored files until both
  raters are done.

## Amendment 1 (2026-10-05, same evening, before any tile copy, page or rating exists)

- **Correction:** the "~1.2× more map pixels per screen pixel" line above measures display scale, not detail. Each 20 mm
  tile is shrunk to 469 × 800 px before the page stretches it to 800 px wide: about **25 µm of papyrus per tile pixel**
  (8320 map px → 800). Each 10 mm window is 4160 map px → 800 px: about **12.5 µm per tile pixel**. So the 10 mm pictures
  are sampled about **2× finer**, while both show at roughly the same on-screen scale.
- **Limit on what the 10 mm block can change:** it answers "can a full-resolution 1 cm² tile score a timed tracing
  session?" only. It does not separate field size from sampling, so a 10 mm "rows" result alone does **not** rewrite the
  agents' 20 × 12 mm field-size line (BRIEF R2); the package's field-size row may only say "1 cm² at 12.5 µm per pixel
  reads / does not read for humans".
- **Key release:** the partsheet_tolerance key stays local until Chris has rated **both** pages (partsheet_tolerance and this one); the Runner's
  question to Sebastien says so.
- Nothing else changes (pictures, order, seed, wording, scoring, Stage 0).
