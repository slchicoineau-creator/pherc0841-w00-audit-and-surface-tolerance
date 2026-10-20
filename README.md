# PHerc0841: an audit of the organizers' w00 mesh and blind human tests of surface-error tolerance

## Why this matters

We set out to measure what a surface mesh must get right on PHerc0841 before ink stops looking like text rows to blind human raters, extending mesh-audit evaluation work like `villa` #1912 (on PHerc0139) to a second scroll with blind human checks. For people building and refining surfaces, this shows which errors still leave the row pattern visible—such as shallow offsets under a sheet deep or uniform depth shifts within ±24 µm—and which errors actually break the row pattern, while giving concrete evidence toward the 2026 "Label quality" open problem (*"… a smaller set of precise labels in the hardest regions may matter more than a larger set of easy ones"*). Two results surprised us: displacing ~30 % of the window by less than a sheet still looked like rows to both raters while a full-sheet hop on ~30 % broke the row pattern for at least one rater, and with a guide line shown, the marks agreed with the organizers' `w00` mesh far more often (`w00` continued its own sheet at 19 of 21 and 15 of 22 random sites, 0.3 mm past the shown line) than Chris's guide-free marks did (within 75 µm at only 42 of 82 stations, 0.75-4.5 mm from a shared start on strips chosen to include bends; agreement was lower at tight bends, noticed after the test). We trust the pre-registered blind counts most, especially the pictures the raters called not rows, such as the full-sheet hop, because nearly every picture on this window was called rows by at least one rater. We are less sure of the guided vs. guide-free contrast (two separate tests on different sites) and of the bend vs. flat difference (noticed after the test, one marker), and we do not claim a universal readability threshold or an absolute `w00` error rate: seeing "rows" does not mean the letters were read, both raters already knew these PHerc0841 windows (making rows easier to spot on damaged surfaces), and the 42/82 score is strictly two-way agreement between `w00` and a single human marker rather than ground truth.

## Author's note

I (Sebastien Chicoineau) designed and ran the tests, did the coached hand fix in VC3D (`COPY-FIX-9`), and rated every blind page except COPY-FIX-9's two read pages (I made that fix, so Chris rated them alone). My teammate Chris Thomas (`@Baz248`) made all the guide-free 2.4 µm station marks, rated every two-rater page, and reviewed the results before packaging. Claude Code (Anthropic) wrote the scripts, built the blind pages, scored each test by its pre-registered rule, wrote the "Judge" verdicts quoted below, ran the review passes Chris signed off, and drafted the evidence tables and the README frame. Every human rating and mark in this repository was done blindly by either Chris or me.

## Who rated


**Status (2026-10-18):** no more tests. The four package tests planned for 10-25 (REAL-LINES-814-V2, FRESH-RATER-NF,
LAY-KEY-9, LAY-GROWN-W) were dropped by Sebastien on 2026-10-17 before any scored session, so every human read below is
by the two team members (Sebastien, Chris), who both know these windows (one never-exposed rater's files from 10-14 were never opened; see the ceiling section), and Chris is the only guide-free 2.4 µm key
marker (Sebastien made guided marks in MARK-2R).



## What is in this repo

| Path | What |
|---|---|
| `README.md` | this file |
| `reproduce/` | one script per test: re-scores the saved keys, ratings and marks and asserts the numbers quoted below (what is recomputed, what is re-read from a saved output, and what no script checks: `docs/CHECK_COVERAGE.md`) |
| `reproduce/run_all.py` | runs them all; exit 0 only if every asserted number matches |
| `data/` | the inputs (page keys, rating files, 2.4 µm marks); see `data/README.md` and `MANIFEST.md` |
| `docs/` | per-test evidence notes (prereg, verdict, where each number comes from) |
| `figures/` | three figures: two of the rated pictures with both raters' calls, pre-rendered from the blind rating pages (the pages and the figure script are not in this repo), and the w00 off-papyrus measure (see `figures/README.md`) |
| `MANIFEST.md` | every input file with its source and sha256 |
| `standalone/` | a second, independent re-check: its own code recomputes the numbers from small exported files, plus `score_surface.py` to score any tifxyz surface of the window against the audit marks (see `standalone/README.md`) |

Each test's pre-registration is in `standalone/preregs/` (scrubbed copies; commit times in `PREREG_INDEX.md`), and its
rule and source lines are in `docs/evidence_*.md`. Files that exist only in the authors' private repository are written
`[private path]`.

"Judge" below means the verdict a Claude Code session wrote for each test by applying its pre-registered rule; it is not
an outside or human judge.


## Read this first: the known-window ceiling

- Both raters know the PHerc0841 known-text window W, and had seen s022814's window before LINE-FIELD-READ. Exposure:
  before SPIRAL-READ-0841, Chris had seen W's control 6 times and Sebastien once (+2 re-framed each).
- No never-exposed read is reported. One never-exposed person did rate (FRESH-RATER-NF and its LAY-GROWN-W add-on, 10-14),
  but both tests were dropped on 10-17 below their rater counts, and those two files were never opened or scored. They
  stay unopened for this package.
- "Rows" saturates on W: nearly every surface picture shown on W was called rows by at least one rater (Sebastien called
  rows on 19 of 20 surface pictures on the HUMAN-TOL and CM2-READ pages (20 showings of 19 pictures)), and every 50 % holes picture shown to both raters
  after HUMAN-TOL was called rows by at least one of them (row 2). So a "rows" call here is a lower bar than reading new
  text, and the useful results are the pictures that were NOT rows.
- A grown field with zero corrections, part of it very likely another winding, also read rows for both raters on W
  (RAW-READ-9H, PASS = GROWER-READS (two raters)). Its frozen row score was 0.017 of the control's, and AI agents saw rows
  0 of 5 times (control 5 of 5).
- "Rows" means row structure is visible, not that the right text is read: displaced patches can carry the neighbour's
  surface (HUMAN-TOL-SCORE finding 7, (H)).

## Findings, with what each rests on

| # | Finding | Evidence | Who read it | Ready? |
|---|---|---|---|---|
| 1 | ~~Rows of 0841-scale text need a ~20 mm field; 10-14 mm tiles show strokes even on the team mesh~~ | FORMAT-20, GROWN-TILE READ, R2 | AI agent readers only (screening) | **dropped as written**: agent reads only, and the blind human reads (CM2-READ, FRESH-WRAP) do not support it as worded. The 20 × 12 mm read format stays as protocol (row 8), not as a finding |
| 2 | Part-sheet displacement, human reads: on one 20 × 12 mm known-text window, pictures with ~30 % of the field displaced by less than one sheet (dispersed L70; clustered C70, read at a −22-layer render offset, about −53 µm) still showed rows to both raters (HUMAN-TOL-SCORE, PASS by its 10-02 rule; one picture per level; label: Chris may have seen the clean version of the same text a minute before rating). Rows visible, not the right text read (see the ceiling section). Doses built from w00 (added on top of its own errors: conservative). Holes: unstable on this window, no threshold. In HUMAN-TOL (Sebastien 10-03, Chris 10-06), 30 % holes (H70) split the raters and 50 % holes (H50) was not rows for both. Chris rejected the same H50 again on 10-08 (his RAW-READ-9H guard), but both raters called it rows on 10-10 (NODE-FILL-REREAD, VOID). Every fresh 50 % holes picture later shown to both raters was called rows by at least one of them: NODE-FILL-READ's (1 of 2, VOID), and by both raters on two valid pages (FULL-HOP-W's H50n on W, TOL-814's H50_814 on s022814). Full-sheet hops: see FULL-HOP-W and TOL-814 under Failures | HUMAN-TOL / HUMAN-TOL-SCORE, FULL-HOP-W, TOL-814 (the agent rows TOL-20/20b/TOL-HOLES are screening only) | humans (Sebastien, Chris) | ready with the labels; the Failures section replaces the old agent wording |
| 3 | Uniform depth shift, human reads: "≥ 24 µm on both sides of P's own +0; no human edge found in the tested range" (CM2-READ, outcome WIDE-OUT, both raters; vs w00, not point-precise; one tile per arm). The organizers' second auto-grown surface of this region, s214732, ~66 µm inward along P's normal, also read rows for both (CM2-READ). On a second wrap (s022814), read blind by two raters who had never seen that text, a whole surface shifted evenly by 24 µm in either direction still reads as rows with the organizers' 2.4 µm ink model (FRESH-WRAP). At ±48 µm on the same page, Chris called +48 µm outward "strokes" (the only fresh depth picture either rater called not rows) and −48 µm rows; Sebastien called both rows (descriptive, one picture per arm; the claim is ±24 µm only). Why ±24 µm is easy: the 2.4 µm model reads a 62-layer (~149 µm) slab, and its ±24 µm maps correlate with the unshifted map at r 0.85-0.87 (±48 µm: 0.69), so this measures the reader's input depth more than depth precision (FRESH-WRAP Judge). Not claimed: that local or dispersed depth errors are harmless, or that 1 cm² tiles do not read. The agent-read "+12 µm outward loses rows" (DEPTH-READ) is withdrawn | CM2-READ, FRESH-WRAP (DEPTH-READ, DEPTH-READ-15 = agents, superseded) | humans (Sebastien, Chris) | ready (FRESH-WRAP wording without the "staying on the right sheet is" clause, per its correction) |
| 4 | ~~A grown surface slid through ~300 correct clicks/cm² reads; ~118/cm² did not~~ | PICK-READ, #35 FOLLOW-UP, FBL5-REREAD | agents; clicks taken from w00 | **dropped**: it scores against w00's position as truth, which the team's truth rule forbids, and the reads are agent reads |
| 5 | **The w00 audit:** w00 is the organizers' semi-automatic growth on the 9.366 µm scan, with a 187 µm grid (copied to the 2.4 µm scan by one affine, residual 14 µm). It cuts across gaps at bends and folds, in its own scan too. On 46 blind 1.5 mm crosses at 2.4 µm, drawn evenly from three audit-suspicion thirds, Sebastien said w00 did not stay on one sheet at 33 (clean 7/15, middle 12/16, suspect 14/15; any short excursion counted; TRUSTED-P, one rater; its calibration gate failed; not a point-error rate). On fresh h0/h2 crosses he said w00 stayed on the sheet at 20/29 (row 6). A computer measure (share of the trace with no papyrus within 25 µm) gives the same median, 0.10, on w00's own 9.366 µm scan and on its 2.4 µm copy, and it rises with bend sharpness (Spearman 0.33) (W00-NATIVE, verdict G: the transfer does not change the off-papyrus share (a weak measure: a ±75 µm shift moves it only to 0.11 / 0.13); villa #1845 found a render-path cost for ink AUC on PHerc0139 that this does not test). Guide-free: "w00 and one rater's guide-free 2.4 µm marks agree within 75 µm at 42/82 stations (0.51, CI 0.40-0.62) on bend-enriched strips of PHerc0841 within 4.5 mm of a shared w00 start" (10 fresh along strips, 7 bend / 3 flat, + 6 cross strips at the dev sites; the CI treats stations as independent, strip-cluster upper bound 0.64; 14 can't-tell stations excluded, and 14 in the replication); a fresh cross-direction replication gave 18/40 (description) (W00-AUDIT-FRESH, one rater: Chris; pair wording: it does not say which is on the true sheet). In the 42/82 pool, 20 of the 40 misses are 75-150 µm, under one sheet spacing, so agreement within 75 µm is not a wrong-sheet rate; corrected for the rater's own sheet switches (e ≤ 0.10) it is still ≤ 0.57. In the 18/40 replication, though, 16 of the 22 misses are beyond 150 µm, about one sheet spacing (130-170 µm). Post hoc (H), fresh along strips only (46 stations): bend 5/28 vs flat 14/18. Guided (MARK-2R, its Judge's Claim wording): "Two blind raters, 2.4 µm, 25 fresh random sites on w00: human–human 18/20 within 75 µm (median 14 µm), consistent with following the guide line; w00 continues its own sheet across a 0.3 mm gap at 19/21 and 15/22 marked sites, consistent with following the guide line (the raters saw w00's line up to 0.3 mm before each spot; a straight extension alone lands within 75 µm of w00 at 23/25); 14 µm affine residual in the 2.4 µm copy." Printed with it, as MARK-2R's prereg requires: "w00 row 5 = MEASURED, not CONFIRMED" and the flag "Chris repeats unreliable" (0 of 2 repeat pairs within 75 µm, 138 / 244 µm apart; Sebastien 1 of 1, one pair, so his repeat reliability is still unmeasured). "About 9 in 10" is not confirmed | W00-NATIVE (`standalone/preregs/w00_native_scan.md`), TRUSTED-P (`standalone/preregs/w00_trusted_crosses.md`); results of both in `[private path]` §6-7 (pre-loop, no loop Judge verdict), W00-AUDIT-FRESH (`standalone/preregs/audit_guidefree.md`, `docs/evidence_B.md`), MARK-2R (`docs/evidence_B.md`), all on private commit `60b819bd` (KEY-FIX: background) | humans (Sebastien alone for TRUSTED-P; Chris guide-free; Sebastien and Chris guided) + one computer measure | ready (Chris's /judge 2026-10-13, with conditions R2-R3 applied) |
| 6 | Three local snapping methods did not beat w00 on two small crops: snapping w00 to the nearest papyrus at 2.4 µm (REFINE-24), a threshold centre line (MIDLINE) and a sheet-scale centre line (SHEETLINE), rated blind 3-arm by one rater (Sebastien: is the surface on the sheet at each 1.5 mm cross?): w00 11/14 vs REFINE-24 9/14 and MIDLINE 8/14 on h0; w00 9/15 vs REFINE-24 6/15 and SHEETLINE 6/15 on h2; not significant (McNemar p 0.25-0.5). Inconclusive and narrow: it does not test learned or interactive label refinement (e.g. the August 2026 nnInteractive award) | REFINE-24, MIDLINE, SHEETLINE (`standalone/preregs/snapping_refine.md`, `standalone/preregs/snapping_midline.md`, `standalone/preregs/snapping_sheetline.md`; results in `[private path]` §8) | Sebastien only | ready as a one-rater, inconclusive appendix note |
| 7 | On the same w00 surface, the ratio of the public 9.6 µm reader's letter-shape signal to the 2.4 µm reader's (windowed band-pass correlation with the organizers' 2.4 µm ink prediction, which favours the 2.4 µm reader) depends on tile phase: 0.27-0.63 (median 0.43) on fresh strip R2 (the pre-registered headline), over 16 × 16 tile-phase pairs, conditional on CT registration; no phase-stable class is claimed. Reported, not fresh: on strip R, where the earlier 0.508 was found (0.524 on re-run), 0.45-0.83 (median 0.59); the region difference is a post-hoc description. The 2.4 µm reader's own tile phase moves the ratio about as much as the 9.6 µm reader's (0.18 / 0.15 vs 0.18 / 0.22 on R2 / R) | PHASE-SYM-ROW7 (prereg `standalone/preregs/reader_phase.md`, PASS = PHASE-DEPENDENT, headline R2, R reported; supersedes SURFACE-OR-READER / FOLLOWUP-SOR-STRIP) | numbers (no rater) | ready as a reader-calibration benchmark of Hecate 9.6 (not a progress bar) |
| 8 | Protocol: blind pages with a readable control, wrong-order blanks, a calibration pair and guards; scoring scripts. AI agent readers vs humans: agents and Sebastien disagree on 5/18 HUMAN-TOL pictures; with both humans (HUMAN-FLOOR, FAIL = HUMANS-NOISY by its rule), Sebastien and Chris agree on 16/18 (κ 0.77), and in every disagreement the agents said "not rows" where a human said rows, so agents are a screen only. Limits learned: wrong-order blanks do not catch a lenient rater, and a 50 % holes picture, fresh or reused, is not a usable guard on W or s022814 for these two raters (row 2) | scoring: `reproduce/humantol.py`, `reproduce/humanfloor.py` (the page builders are not in this repo); HUMAN-FLOOR (`docs/evidence_A1.md`) | n/a | ready (scripts portable: `reproduce/`) |

## Failures and limits (what did not work, with its scope)

- **The organizers' lasagna multi-winding fit with zero corrections did not hold our sheet (LASAGNA-FIT-9).**
  - **Setup:** one run of the shipped self-map seed fit (`init_snap_surf_self_full.json`, unchanged),
    started from cylinder rings grown inward (amendment 1) around a scroll centre clicked by a non-specialist;
    PHerc0841, 9.366 µm, no correction. Stage 3 stopped itself early, at 2459 of 10000 steps, by the tool's own
    `rel_improvement_100 < 1e-4` rule.
  - **Result:** in its last stage the fit left its own seed point. It ended 3.46 mm from the point it was told to hold
    (nearest vertex); along the seed's ray it sat roughly 11-13 windings inward, so it never covered the known-text patch. It was killed by the Judge's reading of the
    prereg's coverage rule (a fit that leaves the patch counts against coverage); our coded check measured the surface's
    own grid and said covered, and no picture was read. Judge verdict FAIL, 2026-10-09.
  - **Mechanism (measured):** the surface stayed within ~35 voxels of the seed through stage 2. In stage 3 the self-snap
    loss fell (4.8e3 → 4.9e2) while the seed-anchor loss rose again (0.0000 after the stage-3 re-set → 19.5; it had reached 7.17 by the end of
    stage 2): the self-snap term pulled the layer off
    its anchor, which points at a weighting the organizers could tune (H, untested: a run with the anchor weight raised
    would tell weighting from data).
  - **Scope:** one run, the organizers' shipped settings, no other settings tried. This does **not** show that lasagna
    fails on 0841 or that the organizers' tool is broken.
  - **Evidence** (public copies; originals on private commit `60b819bd`): `standalone/preregs/lasagna_fit.md`; `docs/evidence_C.md`
    (Verdict); `docs/evidence_C.md`.

- **"~30 % on the wrong sheet still reads" holds only for damage less than one sheet deep (FULL-HOP-W).**
  - **Setup:** the two "30 % damaged" pictures both humans had read as rows (dispersed L70, clustered C70) were rebuilt
    with every damaged patch moved a full sheet (by a 140-250 µm hop law; measured median ~164 µm; ~10 % of moved points
    under 130 µm) onto the real neighbouring sheet, where the 2.4 µm reader no
    longer sees the true text (Stage 0b dose check, passed by a margin of 0.0001 AUC for L70). PHerc0841 known-text window,
    w00 base surface, one picture per level (doses as built from w00, so added on top of w00's own errors: conservative),
    rated blind by Chris then Sebastien on two pages in one sitting (the pre-written 1 MB fallback) with a control, three
    blanks, a calibration pair and two guards (60 % full hops: not rows for both; 50 % holes: rows for both).
  - **Result:** the clustered full-hop picture was not rows for **both** raters; the dispersed one was not rows for
    Chris. The undamaged control read as rows for both and every blank was rejected, so both ratings count. Verdict by
    the pre-written rule: FULL-HOP-FAILS (Judge FAIL, 2026-10-11).
  - **Correction to row 2:** the field reads when the damage is less than a sheet deep; with ~30 % moved a full sheet,
    it is not rows for at least 1 of 2 blind raters. For hand correction this means every one-sheet hop must be counted
    in the hand-fix budget, not only the large ones (on s022814, 15 % full hops still read rows for both raters, but the
    same raters split on the 30 % and 45 % pictures: TOL-814 below).
  - **Scope:** one text window, one picture per level, two raters, one sitting. The clustered picture sat at the
    -22-layer depth where even the control scores lower (Judge finding 7). A description, not a threshold.
  - **Evidence** (public copies; originals on private commit `60b819bd`): `standalone/preregs/fullhop_w.md`; `docs/evidence_A2.md`
    (Verdict); `docs/evidence_A2.md`.
  - **Second patch (TOL-814; same two raters, same sitting, not an independent replication):** on the organizers'
    labelled surface s022814 (nothing from w00), hops followed a hop law with a 170 µm floor (measured median ~200 µm; 10th percentile 110-146 µm; a 140 µm move still showed the true text, so the
    170 µm floor / constant 200 µm fallback ran; moved shares 16.5 / 32.2 / 47.6 %). The ~15 % picture read rows for both
    raters. The ~30 % picture (L70_814) and the nested ~45 % picture (L55_814, every 30 % hop plus 15 % more) each read
    rows for 1 of 2, with the calls crossed: Chris called 30 % strokes and 45 % rows, Sebastien the reverse. By the
    pre-written rule the 30 % "not rows" decides (FAILS-814, Judge FAIL, 2026-10-11), but this window places no threshold
    between ~15 % and ~45 % full hops (one picture per level, descriptive).
    Evidence (public copies; originals on private commit `60b819bd`): `standalone/preregs/fullhop_s022814.md`; `docs/evidence_A2.md` (Verdict).

- **A coached first hand fix did not reach the marked sheet (COPY-FIX-9).**
  - **Setup:** Sebastien, a new VC3D user (voice coach for the interface only), corrected a two-step copy that we made with
    the organizers' neural copy tool (overlap 0.5) from their neighbouring-wrap surface s022814, cut to a 1 cm² square of
    PHerc0841's 9.366 µm scan. The session clock was not started; the minutes were rebuilt from the saved files (89.2 min
    by the load-included rule, 80-84 min by his own reading).
  - **Result:** 17/24 vs control 23/24 at Chris's first marking session (KILL); 16/23 vs 19/23 at his second (undecided):
    inside the key's own repeat noise (Chris's two mark sets give different classes), same rater (KEY2-STEP2, FAIL =
    KEY-LIMITED). By the pre-written rule this is FAIL (KILL-marks), two sites from INCONCLUSIVE; its own start scored
    16/24. The hand-fixed square is not on Chris's blind 2.4 µm marked sheet at the 75 % floor; the 20 mm read could not
    separate it from the control (he read it as rows). No minutes-per-readable-cm² number exists.
  - **Scope:** one person, one coached session, one 1 cm² square, one rater's guide-shown marks (w00's trace drawn; the
    straight guide alone lands within 75 µm at 22/24).
  - **Evidence** (public copies; originals on private commit `60b819bd`): `standalone/preregs/handfix.md`; `docs/evidence_C.md` (Verdict);
    `docs/evidence_C.md` (Verdict).

- **One spiral-fit winding from one anchor point does not read as a whole field for one of two raters (SPIRAL-READ-0841; added for judging).**
  - **Result first:** the automatic spiral fit, placed by one anchor point, split the two raters on both nearest windings
    over the 20 × 11.7 mm known-text window: Chris called both strokes, Sebastien called both rows. By the pre-written
    rule one valid rater's not-rows decides (rows would have needed both): SPIRAL-NO-ROWS (one rater). Judge FAIL, 2026-10-13.
  - **Wording (local Judge's Claim, with the parent's qualifier and Chris's 10-13 /judge conditions):** "the spiral fit passes
    a strip-scale progress bar on one rater's marks (SPIRAL-ACW-0841) but does not read as a whole 20 × 12 mm field from one
    anchor point (one rater, Chris; Sebastien, with no guard picture, called rows; both raters know the field)". Without the
    qualifiers: no claim. The parent strip test carries no outside claim of its own (its Claim is "no"): its strips were
    re-anchored on Chris's first mark, and on bends the spiral did no better than a straight line.
  - **Setup:** the automatic spiral fit (Nieuwlaar's PHerc. 343 recipe, run on PHerc0841, 9.366 µm) placed by one anchor
    point; the two windings nearest the anchor shown over the window, blind, mixed with a readable control (w00), four
    empty pictures and a calibration pair; one page per rater.
  - **Detail:** Chris's control read rows and his guard picture held; Sebastien had no guard on his page (amendment 3), his
    control read rows and he rejected all four empty pictures.
  - **Scope:** one seed, one anchor, one field; both raters know the field. Two process slips, neither voids the result:
    (a) amendment 3 was pushed after both pages were built, though before any rating; (b) a loop question visible before
    Chris rated told raters each page held "one extra check picture, one that the rater already called not rows once",
    which can make the deciding rater more cautious. Strictness: the only check that Chris is not too strict is the control,
    which he had seen 6 times before (and once called not rows, FIELD-R); there was no fresh, slightly degraded but readable
    picture. A follow-up must add sheet-identity help along the field (A-or-B picks), not re-read this one.
  - **Evidence** (public copies; originals on private commit `60b819bd`): `standalone/preregs/spiral_field.md` + `standalone/preregs/spiral_field_amend3.md`;
    `docs/evidence_A2.md` (Verdict); parent
    `docs/evidence_A2.md` (Judge, L440-443); `docs/evidence_A2.md`.

## Line spacing check with perfect lines (no line was traced in the scan)

- **Perfect sheet lines 2 mm apart plus the sheet-direction fill keep the rows (LINE-FIELD-READ).** On the organizers'
  labelled next-turn patch (s022814), 10 constant-height lines cut from that surface itself (~2 mm apart by design, 1.80 mm measured, O2) and joined
  by the sheet-direction fill read rows for two blind raters, as the organizers' surface did; with 5 lines ~4.5 mm apart by design
  (4.05 mm measured, O45) it was not rows for 1 of 2. Judge PASS (O2-READS; O45-FAILS (O45-SPLIT)), 2026-10-11. This is an oracle check of line
  spacing, not a tracing route: no line was drawn in the scan. Our only real-line session (REAL-LINES-814) ended
  incomplete (7 of 9 lines drawn through the start point instead of out from it) and its redo was dropped, so no
  line-route number is quoted from real lines.
  - **Forecast only:** 10 lines per field gives a **forecast floor** of 8.5-10.8 min per cm² (8.5 at the fibre-tool pace measured
    in FIBER-9B, 6.62 mm/min; 10.8 at the clicked-span pace, 5.22 mm/min; perfect lines, starts given, no fixing, depth chosen with the patch's labels, one patch). It is
    arithmetic, not a measured cost.
  - **Limits:** O2 is a sparse resampling of the organizers' own surface (median 33 µm from it by construction), and its
    depth is the best of 7 chosen by this window's labels. O2 and O45 were rated on the same 11-picture page and in the same
    sitting as TOL-814, by raters who had seen this window before in FRESH-WRAP. On that page the 50 % holes guard read rows
    for both and Chris rejected no guard; READS rests on Sebastien's one rejected guard (L55_814), though Chris called L70_814
    and O45 strokes in the same sitting.
  - **Evidence** (public copies; originals on private commit `60b819bd`): `standalone/preregs/line_spacing.md`; `docs/evidence_A2.md`
    (Verdict); `docs/evidence_A2.md`.


## Reproduce

From the repo root:

```
pip install -r requirements.txt          # numpy, scipy
python reproduce/run_all.py              # Python 3.10+
```

CPU only, a few seconds. No scan data is needed: the scripts re-score saved keys, ratings and marks, and re-read some
saved GPU or mesh outputs (listed in `docs/CHECK_COVERAGE.md`). A test whose `data/<test>/` folder is missing prints
`SKIPPED`. Rendering the pictures again (public PHerc0841 volumes + the organizers' 2.4 µm ink model) is not part
of this repo.

Second check, independent code (Python 3.11+), from the repo root:

```
cd standalone
pip install -r requirements.txt
python reproduce.py
python audit/score_surface.py score <surface.tifxyz>   # your own surface of this window; w00: scripts/download_public_inputs.md
```

## Credits

The organizers' w00, s022814 (with its ink labels) and s214732 surfaces; the canonical 2.4 µm reader; the public m7
surface predictions (the hop doses use m7 runs); Hecate 9.6; VC3D (neural copy `copy_displacement`, fibre/line tool,
lasagna; commits used 7d6a82c and villa f4570bf / 0fb38c45; GPLv3, linked, not vendored); Nieuwlaar's PHerc. 343
recipe; villa #1912 and #1937; Benjamin Hamm's nnInteractive label refinement (August 2026); the PHerc1667 expert
tracing benchmark. Cited, not claimed: the copy model's mirror-TTA sign fix is @khj1222's villa #1796 (merged
2026-10-08). The copy overlap seams were reported by Sebastien (villa #2040); the fix PR is another contributor's
(villa #2138).

## Related work

- SirColton, `pherc0841-9um-letter-test` (October 2026): on held-out PHerc0841, blind readers named reference letters
  from 9 µm and 2.4 µm ink maps; its readers are fresh AI agents. This repo asks a different question (how much surface
  error a reader tolerates) and uses two blind human raters.
- robertlangdonn, `vesuvius-readability-gate` (July 2026): predicts whether a surface will yield legible ink and notes
  that the canonical ink model reads a 62-layer (~149 µm) depth window, the same window row 3 relies on.
- villa #1845 (kadenpool): on PHerc0139 ink AUC, the coarse-mesh cost; the transform's share is an upper bound and is
  not separated from renderer interpolation. Row 5 here measures only the off-papyrus share, a different quantity.

## Licence

Code: MIT (`LICENSE`); the copyright covers our code only. The figures, surface coordinates and mark positions are
derived from Vesuvius Challenge open data (PHerc0841 scans and the organizers' w00, s022814 and s214732 surfaces,
`s3://vesuvius-challenge-open-data/`) and are shared under CC BY-NC 4.0
(https://creativecommons.org/licenses/by-nc/4.0/), with attribution to the Vesuvius Challenge; we changed them by
rendering, cropping and labelling. VC3D is GPLv3 and is linked, not included.
