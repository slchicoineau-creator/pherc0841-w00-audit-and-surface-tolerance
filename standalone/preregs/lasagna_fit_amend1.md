> **Scrubbed public copy** (public name `lasagna_fit`). The original was first committed to the authors' private repository at `732f49fc2` (2026-10-08T23:55:02Z). Timing: Amendment 1 (inward-ring route, larger box): pushed 6 min after the second job was launched, before any main output of that job existed (its Judge's check: a letter deviation, not a validity issue). Timestamps live in a private repository; ask the authors for a verification. Scrubbing removed mentions of non-public scrolls and local paths (paths into the authors' private repository read `[private path]` and do not resolve) and replaced internal item ids and test names with public slugs (unmapped internal ids read `[internal item]`); the scientific text is otherwise unchanged.

# lasagna_fit, prereg amendment 1 (written by the Runner, 2026-10-08 ~19:00, BEFORE any main-run output exists)

Authority: Sebastien's answer A, 2026-10-08 18:44 (item `## Human answer`): "amend the plan: their inward-growth switch + larger data box,
then run the whole thing (~5-9 GPU-h; stop and report if rings stop short of the patch)".

Why: probes (Stage 0d, never rendered / read / scored): `cyl_init_tool` fixes its first ring at radius 2000 vx (model.py:394) and the
shipped `init_cyl.json` grows outward; W is 693-1130 vx from the clicked axis. Probe 1: both outward rings at ~1810 vx, ifrac 0.56 / 0.96.

Changes to prereg "The route" steps 3-4 only (no bar, no verdict rule, no config FILE, no fit setting, no render/read/page rule):
1. Step 3 box: half-width 2400 vx around the clicked (tilted) axis over z 13391-15700 (was: max W-to-axis distance + 107 vx). Box
   lo (0, 1024, 13312), size (5888, 5376, 2560) = 81.0 Gvx. Projection 5.96 h at 226 s/Gvx (4.0 h at the 138 s/Gvx probe 1 measured).
   New STOP-BUDGET for this box: > 6.0 h projected -> stop and ask. Reasoning for 6.0: Sebastien accepted ~5-9 h in all; the frozen 4 h for
   shells + fit leaves ~5 h for download + inference, rounded to 6. The box is 81.0 Gvx, NOT the 72.8 Gvx quoted in the question (the price
   script clipped the axis' y range to one value; the axis also moves in y). The projection at the planning rate is 5.96 h; at the rate probe 1
   actually measured on this machine (138 s/Gvx) it is 3.1 h inference + 0.9 h download = 4.0 h.
2. Step 4 shells: `cyl_init_tool.py` with the shipped `init_cyl.json` plus the shipped `--inwards` switch (overrides `cyl_grow_direction`),
   `--z-range 13391 15700 --shell-count 12`, continued with `--start-shell <last> --shell-count 13 --inwards` until the last shell's median
   radius from the clicked axis <= seed radius - 107 vx (848.1 - 107 = 741.1; the mirror of the prereg's outward rule), cap 60 shells.
   Shells that stop short (tool stops growing, or no new shell) = STOP-RINGS-SHORT: no claim, ask Sebastien. Continuation runs write to
   separate out-dirs; duplicated start shells are dropped and the rest are renumbered outer -> inner into `main/shells` (`lf9.py merge_shells`).
3. Step 5 fit unchanged except the CLI form `--input=<path>` (run 4 finding) and `--cuda-gridsample 0` only if the dense kernel will not build.
4. Wall cap 4 h for shells + fit together, GPU job limit 10 h.
Engineering path/env deviations already listed in the item `## Run`: CPATH, libigl v2.6.0, `--input=`.
Sebastien's 4-8 GPU-h acceptance: projected 4.0-6.0 h inference+download, plus up to 4 h shells + fit (worst case ~10 h; he accepted "5-9").

Caveats written before the run (so nobody reads probe 2 as more than it was):
- Probe 2's second ring (median radius 798 vx, z 13833-15076, ifrac 0.92) is NOT evidence that inward growth works: a 1.1 grow step should
  shrink the ring by ~10 % (target circumference 12566 -> 11424, i.e. radius 2000 -> ~1820), and the ring that came out had drifted off the thin data slab.
  The earlier plain-words line "landed right where our patch is" overstated it. Expect ~10 inward steps (1826 -> 741 vx at 1.1 per step),
  so one continuation run is likely; the run tests inward growth for real and stops (STOP-RINGS-SHORT) if the rings do not get there.
- The fit's row-quality trim (`fit._trim_shell_for_anchor`) is applied only to the shell nearest the seed, not to every shell in the folder.
- Timing: probe 2 spent ~1.5 min on shell 1 and ~3.5 min on shell 2 at 190 vx tall; the real rings are ~2300 vx tall, so the 4 h cap is the
  only time bound known; the job stops at it.
