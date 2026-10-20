> **Scrubbed public copy** (public name `audit_guided`). The original was first committed to the authors' private repository at `f6f7dd0ec` (2026-10-06T14:20:47Z). Later commits to the same file: `2a48de509` (2026-10-06T14:22:44Z). Timing: Original and amendment 1 (straight-line baseline) both committed before any output (its Judge's check). Timestamps live in a private repository; ask the authors for a verification. Scrubbing removed mentions of non-public scrolls and local paths (paths into the authors' private repository read `[private path]` and do not resolve) and replaced internal item ids and test names with public slugs (unmapped internal ids read `[internal item]`); the scientific text is otherwise unchanged.

# Pre-registration: audit_guided, do two people marking the sheet blind at 2.4 µm agree with each other, and with w00, at fresh random w00 sites? (PHerc0841, 7 dev crops)

- **Date:** 2026-10-06 (CDT), pushed before any audit_guided site, picture or page exists. Owner: Sebastien's side (station loop item
  `audit_guided`). Public data only. CPU only.
- **Sebastien's choice (item, 2026-10-06 08:12): C.** Full page (25 random + 10 suspect + 3 repeats). Sebastien marks as soon as the page
  exists; Chris marks only AFTER his LINE-9 tracing is done (LINE-9 comes first), before about Oct 13.
- **Why:** several keys rest on ONE person's 2.4 µm mark: Chris's LINE-9 reference line, the copy-and-fix check points, and row 5 of
  package (b) ("w00 sits where Chris marks it at about 9 points in 10": Chris alone, 22/25 within 75 µm, median 21.6 µm, 3 can't tell, at 25
  HUMAN-PICK/SLAB control sites, not random; `[private path]`). No human–human agreement at a
  point has ever been measured. `REDO_AFTER_GOOD_MESH.md` candidate 3 assumes it.
- **Truth rule:** the verdicts rest on human 2.4 µm marks only. w00 is the object audited, never the key.
- **What this does NOT test:** sheet identity. Both raters follow w00's own green line up to 0.3 mm before the view line, so if the green
  line is already on the wrong sheet, both follow it. The w00 number therefore only says whether w00 **continues its own sheet across a
  0.3 mm gap**. Our 2.4 µm copy of w00 is one affine of the 9.4 µm mesh (residual 14 µm); w00 distances include that error.

## Sites (seeded, `numpy.random.default_rng(2026100620)`)

- **Pool:** w00_trusted_crosses's auditable 0.25 mm grid crosses on w00 in the 7 dev crops (`trustedP_features.npz`: aud = 1, A and B finite). It is
  not all of w00; the result is stated for this pool.
- **Excluded (≥ 1 mm, 3-D distance in global band level-0 coordinates, any crop: crops overlap):** every site a human has already rated
  or traced: w00_trusted_crosses page (52), 3-arm pages h0/h2 (95; snapping_refine, snapping_midline, snapping_sheetline), HUMAN-PICK (66) and HUMAN-SLAB (17) sites (KEY-FIX
  used their 28 controls), TWO-LINE pilot + main (60); the 9 LINE-9 strips (rectangle grown by 1 mm on every side; Sebastien traced them,
  Chris will trace them before this page); crop h0 within 1 mm in z of the two FORK-SPLIT EYE-test planes (z 700 and 3100), whose fork
  coordinates were not saved. **Not excluded:** grower departures (Critic finding 7: excluding them would tilt the sample toward easy
  places); 20 mm reading tiles (other display, no point marked); FORK-SPLIT Stage 1 overview pictures (no per-spot answer).
  Planner dry check (`[private path]`): 646 fresh crosses, 152 with
  A ≥ 0.2; per crop c0 76, c1 35, c2 57, h0 23, h1 298, h2 124, h3 33.
- **Draw:** one seeded permutation of the fresh pool. **Random** (primary): the first 25 crosses in that order that are ≥ 1 mm from every
  site already taken and eligible. **Suspect** (descriptive only): then the first 10 crosses of the same order with A ≥ 0.2 under the same
  rules. **Sanity** (Stage 0b only, never on the page): then the next 5.
- **Frame and jitter: HUMAN-PICK's own site builder** (`humanpick.site_view`, kind "control"): normal from the grown surface within 0.3 mm,
  else P's normal averaged over 0.5 mm; view centre = site + δ·n with **δ ~ U(−160, +160) µm**, so clicking the middle of the line does not
  score; side of each slice as HUMAN-PICK. w00's position on the view line is t = −δ exactly (the site is a w00 point).
- **Eligibility (replacement rule):** a cross is skipped and the next one in seeded order is tried if neither picture has green on ≥ 50 %
  of the displayed 0.01 mm bins (after masking against sites already drawn), or a picture has ≥ 5 % out-of-volume pixels. Final masking
  is redone against all sites; pictures that fall under 50 % after it are counted and reported, not replaced.

## Display (KEY-FIX's, `[private path]`)

- Two orthogonal 2.4 µm planes per site, s from −0.9 to +0.2 mm, ±0.3 mm along n; WebP q45; contrast per crop as keyfix.py; dashed view
  line at s = 0; green = w00's trace from −0.9 to −0.3 mm. **One change:** green is masked within 0.5 mm of every other page or sanity site's
  w00 point (HUMAN-PICK's `MASK_MM`), so no picture shows w00 near another site.
- **Page:** 25 random + 10 suspect + 3 repeats (3 random sites drawn by the seed, same pictures, new ids, each ≥ 10 items after its
  original) = 38 items, shuffled, random 3-digit ids. Each rater clicks where the followed sheet crosses the dashed line, or presses
  "Can't tell". About 14 min. The page lives in the item's git-ignored `cache/` (≈ 1.3 MB, over the 1 MB push limit) and is delivered by
  the main session, as the w00_trusted_crosses page was. Key `mark2r_key.json` and rating files `mark2r_<name>_ratings.json` are git-ignored.
- **Blindness:** each rater works alone and never sees the other's marks, the key or w00 at the site. **Scoring waits until BOTH rating
  files exist** (`mark2r_score.py` refuses otherwise); Sebastien's file is only checked for completeness until then.

## Metrics (75 µm = identity radius, as KEY-FIX and HUMAN-PICK)

- Distance between two marks = |Δt| along the view line (both pictures show the same 3-D line).
- **Human floor (primary, binary)**, random stratum, first presentations, sites marked by both (Can't tell excluded and counted):
  shared n ≥ 15, else **UNDECIDED**. **KEY OK** if within 75 µm at ≥ ⌈0.8 n⌉ sites; otherwise **NOT A SINGLE-RATER KEY** (two raters
  disagree: a single-rater 2.4 µm mark is unproven as a point key; keys need two raters who agree). Exact 95 % CI and the median distance
  are always reported. (Cost of a binary bar: at a true agreement of 85 % it fails about 1 time in 6 at n ≈ 20.)
- **w00 (row 5 audit line), per rater:** the share of that rater's marked random sites within 75 µm of w00, exact 95 % CI, median.
  **CONFIRMED** ("w00 continues its own sheet across a 0.3 mm gap at about 9 in 10 random sites, two blind raters") only if BOTH per-rater
  shares are ≥ 85 %. Otherwise row 5 prints the two measured per-rater rates with that same wording. Never "w00 is right 9 in 10 at a point".
- **Repeats:** a rater is flagged unreliable if within 75 µm of their own first mark on < 2 of 3 repeat pairs (not assessable if < 2 pairs
  marked). A flag is printed next to the verdict; it does not change it.
- **Descriptive only (no verdict):** agreed-subset w00 rate (w00 vs the two raters' mean mark where they agree), number of sites dropped for
  disagreement and w00's distance there; the 10 suspect sites (human–human floor and per-rater w00 rate at hard spots); per-crop counts.
- **Centre bias (report):** the centre-click baseline (share of random sites with |δ| ≤ 75 µm; expected ≈ 0.47, HUMAN-PICK controls 7/14)
  and, per rater, the share of marks within 20 µm of the view centre; above 1/3 is flagged (it would inflate both rates).

## Stage 0 (sanity checks first; inside `job.sh`, before the page is built; minutes)

- **0a (enough sites):** exactly 25 random and 5 sanity sites drawn under the rules above. Fail → exit 78, **UNDECIDED, no human time**
  (fallback: none; the dry check found 646 fresh crosses, so a fail means a bug, to be fixed and re-registered). Suspect stratum: fewer than
  10 is reported; fewer than 5 → stratum dropped, test continues.
- **0b (papyrus at the view line):** on the 5 sanity sites (not on the page), a voxel ≥ the crop's Otsu τ (w00_trusted_crosses's `tau`) on the view
  line within 25 µm of w00's crossing, in ≥ 1 of the 2 pictures, at **≥ 4 of 5**. Fail → exit 78, **UNDECIDED, no human time**. The same
  count over the 35 page sites is reported (descriptive). The 5 sanity pictures are saved (`s0/sanity_*.png`) and the Runner looks at them
  as a screening step (agent look = screening only; it may stop the page, never decide a verdict).
- **0c (report only):** centre-click baseline and frame sources (grower / P-smooth).

## Compute, people, dates

- CPU only (≤ 10 threads), level-0 band chunks streamed from the public S3 bucket: ~10-30 min. GPU 0 h. Seeds: 2026100620 (draw, δ),
  +1 (contrast sample), +2 (page order, repeats, ids).
- People: Sebastien ~14 min (now); Chris ~14 min, after LINE-9, before ~Oct 13.
- **Kill date:** 2026-10-16. If Chris's file has not come by then, the item closes as UNDECIDED (Sebastien's marks alone decide nothing;
  his repeats and centre-bias numbers are reported).
- Scripts: `[private path]` (Stage 0 + page), `mark2r.py` (copied from keyfix.py + critic_pool.py,
  HUMAN-PICK site builder), `mark2r_score.py` (rules above; `--selftest` on synthetic ratings).

## What each outcome changes

- **KEY OK:** a single rater's 2.4 µm mark may stand as a point key (LINE-9's reference, copy-and-fix check points, redo-list candidate 3),
  with the measured median human–human distance as its error bar.
- **NOT A SINGLE-RATER KEY:** every Chris-keyed point test is scored with two raters who agree (or reports the single-rater key as
  unproven); redo-list candidate 3 is weakened; row 5 says so.
- **w00 CONFIRMED / MEASURED:** row 5 of package (b) gets the two-rater random-site line in the finding-5 wording, with the suspect-site
  numbers beside it.
- **UNDECIDED:** row 5 keeps "Chris alone, 25 non-random sites"; the single-rater key stays unproven.

## Amendment 1 (2026-10-06, same Planner run, before the first push; no audit_guided data exists)

- **Controls.** Blank / reverse control: none, because there is no "no sheet" answer to score; the 3 repeats are the reliability check.
  Positive control: none (KEY-FIX's 25 sites are already known to Chris; reusing them would not be blind). Two **baselines** replace
  them, both descriptive and reported next to the verdicts: the centre-click baseline (above) and a new **straight-line baseline**.
- **Straight-line baseline.** The ±160 µm jitter defeats clicking the middle of the line, but not extending the green line straight
  across the last 0.3 mm. Per site: fit t = a + b·s to the displayed green trace on s ∈ [−0.5, −0.3] mm (after the final mask; the
  picture with more bins, ≥ 5 bins; none if neither) and extend it to s = 0. Reported: share of random sites where that extension lies
  within 75 µm of w00 (Stage 0c, aggregate only; per-site values stay in the git-ignored key); per rater, the share of marks within
  75 µm of the extension; the number of random sites where the two raters agree with each other but both lie > 75 µm from the extension
  (sites where reading the scan, not the guide line, decided).
- **Wording rule.** If the straight-line baseline is ≥ the lower per-rater w00 rate, the human-floor verdict and row 5 both carry
  "consistent with following the guide line" (the verdict rules themselves do not change).
- **Page text:** identical to KEY-FIX's instructions except the item count, time and file name (no hint about where the sheet lies).
