> **Scrubbed public copy** (public name `handfix`). The original was first committed to the authors' private repository at `27c9d342c` (2026-10-09T01:10:12Z). Later commits to the same file: `ca98394fb` (2026-10-09T01:13:11Z). Timing: Both commits pushed before every output (its Judge's check). Timestamps live in a private repository; ask the authors for a verification. Scrubbing removed mentions of non-public scrolls and local paths (paths into the authors' private repository read `[private path]` and do not resolve) and replaced internal item ids and test names with public slugs (unmapped internal ids read `[internal item]`); the scientific text is otherwise unchanged.

# Pre-registration: handfix second-key step, is the hand-fix's mark verdict the same when Chris's second marking session is the key? (PHerc0841, 9.366 µm scan)

- **Date:** 2026-10-08 (evening CDT), committed before Sebastien's timed session exists: no `f_src.json`, no `a/F` in handfix's
  folder, and FIX-FIELD's watcher has logged only the t00 starts plus the unedited working copy `edit/F_work` (x/y/z equal to the
  frozen OVL_inset t00 copy, sha_x `38a9df44…`). Owner: Sebastien's side (station loop item `handfix`).
  Public data. CPU only. Human time: 0 (Sebastien 0, Chris 0).
- **Add-on, not a change:** this file adds one label to handfix step 2 (`preregs/handfix.md`) and FIX-FIELD leg A
  (`[private path]`). Their verdicts stand exactly as pre-registered; nothing here overrides them.
- **Why:** both parents score F at Chris's 24 blind 2.4 µm marks (key 1). Chris re-marked the same 24 sites a day later with a far
  guide (KEY-FAR-24, key 2); the two sets agree within 75 µm at 18 of 23 sites (`FACTS.md:856`). FIX-FIELD's MIDDLE band is 3 sites
  wide, narrower than that repeat noise, so F's class may depend on which session is the key. This test says whether it does.
- **Truth rule:** nothing is scored against P (w00). Both keys are Chris's blind marks; C (the readable control) is scored at the
  same marks, as in the parents. P never decides.

## Data (held-out issues)

- Key 1: `[private path]` + `copyfix_key.json` (24 sites; C's and
  R's stored crossings; F's after step 2's `cf.py cross F`). Key 2: `[private path][internal item]/
  keyfar_marks_chris_ratings.json` + `keyfar_key.json` (all git-ignored; local only).
- **Key 2 in key 1's frame:** t₂ = t_new + delta_um − delta_old_um (KEY-FAR page jitter removed), site `old_id` → key-1 id (one-to-one,
  checked). "Can't tell" stays invalid. Premise: after this shift C's crossing on the two pages agrees to ≤ 0.1 µm at 24/24 sites
  (`[private path]`).
- Leak guard: key 2 was made blind of R and F; F does not exist at this commit. All key-2 counts of R / OVL / F / checkpoints are
  **sealed** (below).

## Arms and controls

- **Scored arms:** handfix's R (step 1, start reference) and F (step 2), from the stored crossings; FIX-FIELD's F30, F60, F_end and
  its start snapshot, using the exact snapshot paths and route that `fixfield_result.json` / FIX-FIELD's `stage0.json` record (crossings
  recomputed with `ff.site_cross`, unique tags, in memory; `copyfix_key.json` is never written).
- **Control:** C (N2) at both keys: key 1 23/24, key 2 19/23 (counts of C only).
- **Reference bars this implies for F:** key 1 PASS ≥ 21, KILL ≤ 18; key 2 PASS ≥ 18 (the 0.75 floor binds), KILL ≤ 14.

## Metric (frozen; handfix's rule imported unchanged)

- Per arm and key: `cf.mark_counts` (exactly one crossing within 75 µm of the mark = on), `cf.mark_class` (KILL ≤ C_on − 5; PASS ≥
  C_on − 2 and ≥ 0.75 × valid; else MIDDLE; < 18 valid → TOO FEW). C_on and valid are recomputed on each key.
- **Two-key class** of an arm = its class if key 1 and key 2 give the same class, else **KEY-LIMITED**.
- **Two-key T\*** (FIX-FIELD leg A): per checkpoint a combined class = PASS-marks if PASS under both keys, KILL-marks if KILL under
  either, MIDDLE otherwise (TOO FEW under a key → that checkpoint dropped, like a missing one); then FIX-FIELD's own `ff.classes`
  (CHEAP-30 / T\* 30-60 / T\* 60-T_end / NOT-REACHED). **30-NOT-ENOUGH** = F30 KILL-marks under either key.
- **Consistency gate:** the key-1 counts this scorer recomputes must equal the parents' own (handfix `copyfix_result.json` step2
  marks; FIX-FIELD's per-checkpoint marks). Any difference → INCONCLUSIVE (scorer mismatch).
- **Descriptive (sealed):** each arm's class at the 18 stable sites (both marks within 75 µm; C 18/18 → PASS ≥ 16, KILL ≤ 13).

## Stage 0 (sanity checks first; job.sh, seconds, C-only counts)

- **selftest (synthetic):** key-2 mapping and one-to-one check, two-key and combined classes, `ff.classes` on combined classes,
  `mark_counts` on a toy site pair. Fail → exit 3 (bug).
- **0a frame:** C's shifted crossing reproduces handfix's at ≤ 1 µm at ≥ 23 of 24 sites, map one-to-one over 24 sites.
- **0b control on key 2:** valid ≥ 18 and C_on ≥ 0.75 × valid (known: 19 of 23).
- **0c:** R's stored crossings present at 24/24 sites (shape only; no mark compared).
- **0d:** every output path is git-ignored. Fail → exit 3.
- **0e too late (VOID):** judged at this file's commit time: `f_src.json` or `a/F` existed; or FIX-FIELD's `watch_log.jsonl` holds a
  `"change"` record whose folder write time (`mtime`) is before the commit and whose `sha_x` is not one of the two frozen t00 start
  shas; or `edit/F_work`'s x/y/z differs from
  the frozen OVL_inset t00 copy (checked at commit). → **VOID (too late)**, exit 78.
- 0a / 0b / 0c fail → **UNINFORMATIVE by Stage 0**, exit 78: the parents keep their single-key verdicts with the label "key repeat
  18/23 untested on F". Dry run at this commit: selftest OK; 0a 24/24 (max 0.1 µm); 0b key 1 23/24, key 2 19/23; 0c 24/24; 0d clean;
  0e: 1 change record (F_work, sha = OVL t00), F_work = t00 OVL, no `f_src.json`, no `a/F` → not void.

## Outcome

- **TWO-KEY (PASS):** F's class is the same under both keys. Frozen wording: "same verdict at Chris's two marking sessions (same
  rater)". Never "two-key confirmed" or "two independent keys": one rater, sessions a day apart, sites seen before, different guide.
- **KEY-LIMITED (FAIL):** the classes differ. The parents' verdicts stand; every package or outside sentence quoting them carries
  "inside the key's own repeat noise (Chris's two mark sets give different classes)". FIX-FIELD leg B or a second rater firms it up.
- F = handfix's stored F crossings; if those never exist by the kill date, FIX-FIELD's F_end (the same folder, its route).
- **INCONCLUSIVE:** consistency gate fails, or F is TOO FEW under a key. **VOID:** Stage 0e, or a parent is VOID. **Not run:** no F by
  2026-10-19.
- Inherits handfix's audit_guided link (single-rater key wording) for every class.
- Odds (Ideas' Monte Carlo, `checks/handfix/ideas_key2_odds_out.json`): TWO-KEY likely only for a near-
  perfect or clearly failed F; a partial fix (18-21 on at key 1) is likely KEY-LIMITED.

## Hold rule (sealed)

- Every key-2 count, class or T\* of R, OVL, F and the checkpoints goes to `key2_result.json` (git-ignored) only. Until handfix step
  2 is judged, committed text may say only "scored, sealed" and the Stage 0 C counts. Stdout prints none of them.

## What each outcome changes

- TWO-KEY: handfix step 2's mark verdict and FIX-FIELD's T\* may be quoted in package (b) with the same-rater wording.
- KEY-LIMITED: the minutes number is quoted only with the noise label; firming it up needs leg B (whole-field read) or a second rater.

## Compute, kill date

- CPU only, no GPU. Kill date **2026-10-19**. `job.sh` never waits: selftest + Stage 0 (seconds), then it scores only if both parents
  have scored (handfix `copyfix_result.json` holds `step2`, which needs Chris's page-2 read, so no blind rating is pending; and
  FIX-FIELD's `fixfield_result.json` exists) or the kill date has passed; else it exits 0 with `KEY2_WAITING`, and the Runner holds
  the item and relaunches the same `job.sh` later (Stage 0 is re-run each time, 0e still judged at this file's commit time).
  Scoring ~10 min. (The loop runs at most 2 CPU jobs and FIX-FIELD's watcher holds one, so a days-long poller is ruled out.)
- `gpu: no`, `gpu_hours 1` (wall limit ≈ 2.5 h per launch).
- Scripts: `[private path]`, `job.sh`, `.gitignore`.
