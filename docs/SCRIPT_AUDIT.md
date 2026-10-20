> **Status 2026-10-18 evening:** the WEAK points below and the Gemini script findings were fixed in the scripts (each new check shown to fail under a mutation). Left: w00auditfresh stations 1-6 distances stay re-read (w00's station positions are in no saved file); lasagnafit9 fails on purpose until WORDING_FLAGS 1 and 4 are decided. Current per-number status: `CHECK_COVERAGE.md`.

# Script audit of `reproduce/` (2026-10-18)

Read-only audit of the 18 re-scoring scripts. For each script I compared it with its prereg text at
private commit `60b819bd`, with the Judge's verdict item, and with the Judge's `judge_rescore.py`. Nothing in
`reproduce/` or `data/` was changed. Every test ran on copies in a scratch folder.

**Mutation test.** One rating at a time was changed in a copied data folder:
- an answer flipped (rows ↔ nothing, strokes → rows);
- a mark moved by +200 µm;
- a "can't tell" turned off;
- a practice choice changed.

A shim made every sha check see the original file bytes, so a failure means a re-scored number changed, not only a hash.
As a baseline, re-writing each file without any change gave 0 failures. The 4 scripts with no ratings files got one change
to a main input and one change to a saved result file each.

**Verdicts:** OK = scores the written rule from the raw inputs and checks what it claims. WEAK = the quoted outcome is
right, but the script leaves out part of the rule, or it states a number it never checks against the data.
WRONG = none.

| Script | Verdict | Single changes caught | What the missed changes were | Main issue |
|---|---|---|---|---|
| cm2read | WEAK | 60/80 | all 20 in the bundled HUMAN-TOL file on pictures it does not use; all 44 CM2 changes caught | INCOMPLETE / "uncountable" branches missing |
| copyfix9 | OK | 58/65 | read-page pictures that carry no rule weight here (0009B blank; guard after a KILL-marks); key-2 items not in the key or with no recorded position | saved cf.py result compared but only printed |
| freshwrap | WEAK | 28/30 | 0009B blank (prereg: "reported only") | answered / INCOMPLETE / ctrl-blank VOID branches missing; r values taken from the Judge file |
| fullhop | OK | 18/18 | none | AUCs re-read from the Stage 0b output (declared) |
| humanfloor | WEAK | 36/36 | none | invalid Chris gives HUMANS-NOISY, not UNDECIDED; n = 5 hard-coded |
| humantol | OK | 36/36 | none | answer set and vocabulary not checked |
| lasagnafit9 | WEAK | fit.log and grid edits caught; Judge file unused | n/a | fails on purpose; "written rule" label is the Judge's reading |
| linefieldread | WEAK | 19/22 | 3 TOL-814 pictures that F3/F4 do not use | 2.02 / 4.54 mm are worked out from fixed numbers, not data |
| mark2r | OK | 42/76 | suspect and repeat sites (descriptive only), can't-tells with no position, 3 moves that crossed no 75 µm line | centre-bias flag not checked |
| nodefill | OK | 26/66 | 34 on HUMAN-TOL pictures it does not use (it reads one); 6 on arm calls (never scored: both tests VOID) or on a comparator kept out of the stability count by rule | sha check bundled into a verdict assert |
| phasesym | OK | pair-table edit caught; job summary and Judge file unused | n/a | Judge's 5-pair check printed, not asserted |
| rawread9h | OK | 12/12 | none | RP ratio comes from the Judge's saved output (declared) |
| snap3arm | OK | 95/95 | none | p-range line printed, not asserted |
| spiralread0841 | OK | 17/17 | none | only Sebastien's file hash is checked |
| tol814 | OK | 18/22 | the 4 LINE-FIELD-READ pictures on the shared page ("never count") | dose numbers re-read (declared) |
| trustedp | OK | 52/54 | 2 worked examples that are not in the key | none |
| w00auditfresh | WEAK | row edit caught; every mark position in one session's mark file shifted by 0.5 (file units, mm): NOT caught | n/a | distances re-read; never tied to the marks |
| w00native | OK | CSV edit caught; result file unused | n/a | row count and CSV hash not checked |

Totals: **12 OK, 6 WEAK, 0 WRONG.** For every WEAK script the quoted outcome still re-scores correctly on the shipped data.

## Re-read vs computed

- **Silent re-reads** (a quoted number taken from a saved output with no comment saying so): none found.
- **Declared re-reads** (they need images, meshes or GPU outputs that are not shipped):
  - freshwrap r values;
  - rawread9h RP and agent screen counts;
  - fullhop and tol814 dose AUCs and hop sizes;
  - lasagnafit9 stage-2 drift;
  - phasesym 256-pair table and the 0.508;
  - spiralread0841 exposure counts;
  - linefieldread 33 µm;
  - copyfix9 OVL crossings;
  - w00native per-cross A25 CSV;
  - w00auditfresh per-station distances.
- **Bundled but unused saved files** (changing them changes nothing; fine, but they are not cross-checks):
  - phasesym job summary fields;
  - `w00native_result.json`;
  - `mark2r_summary.json`;
  - `judge_patch_check.json`;
  - `trustedP_fit.json`.
- snap3arm and trustedp: the prereg comparison was done by a helper read-through; the mutation results are my own.

## Notes on the WEAK scripts

- **cm2read.** Prereg `standalone/preregs/depth_w.md`:
  - L76-81: "else INCOMPLETE if +12 or +24 is uncountable".
  - L84: s214732 is "uncountable if its blank reads rows".
  - L87: the 10 mm block is "Uncountable if either 10 mm blank reads rows".
  - The script uses `oc = "VOID" if not (valid and ctrl_ok) else ("WIDE-OUT" if o > 0 else ("ASYMMETRIC" if i == 24 ...`. That treats an uncountable tile as not rows and prints "NOT ROWS" for an uncountable s214732.
  - The per-rater 10 mm unit (1 cm² USABLE / 20 mm ONLY) is not computed.
  - Fix: add the INCOMPLETE and uncountable branches and the `unit10` rule, and assert them.
- **freshwrap.** Prereg L101-105:
  - "every picture answered" is not checked;
  - "ctrl blank rows → VOID" and "an arm whose blank is rows is uncountable → INCOMPLETE" are not scored.
  - The combined call is CONFIRMED or "other".
  - The r 0.85-0.87 / 0.69 values are read from `judge_rescore_60b819bd.json`. This is declared, but those numbers are only checked against themselves.
  - Fix: add the three branches, add a sha pin for both ratings files, and keep the "derived" label on r in the README.
- **humanfloor.** Prereg L40-41: "If not valid → UNDECIDED".
  - The script computes `chris_valid` but runs `v = "AGENTS-OFF" if k >= 4 and m <= 1 else ...` whatever its value.
  - On a copy with 2 of Chris's blanks flipped, `chris_valid` became False but the verdict stayed HUMANS-NOISY (through m = 2), where the prereg says UNDECIDED.
  - `sum(comb(5, i) ...)/32` hard-codes n = 5.
  - The prereg's two-sided sign test (L45) is missing.
  - Fix: `v = "UNDECIDED" if not valid else ...`, use `comb(len(disc), i) / 2**len(disc)`, add the two-sided p, and pin both file hashes as humantol.py does.
- **lasagnafit9.**
  - It exited 1 on purpose: the anchor value 0.0009 vs 0.0000 (WORDING_FLAGS item 1). Fixed 2026-10-20: flags 1 and 4 applied (outline cf541ce98); it now passes and run_all gives 18/18.
  - `verdict_by_written_rule` uses "share within one winding pitch < 0.70". That pitch band is the Judge's way of applying the prereg's step-7 "leaves the patch" clause. The literal coverage share in the prereg is 1.0 (`coded_gate_coverage`).
  - `nearest_vx_end_of_stage2` is re-read from `runner_job2_drift.json` (declared).
  - Fix: settle flag 1, then change EXPECTED; rename the key to `verdict_by_judge_reading_of_step7`.
- **linefieldread.**
  - `round((RING_G1 - RING_G0) * STEP_MM / (n - 1), 2)` works out the spacing from fixed numbers in the script, so it can never disagree with the data.
  - The measured 4.054 mm in `stage0.json` is printed but not checked (WORDING_FLAGS item 3).
  - The 33 µm construction distance is re-read (declared).
  - Fix: assert the measured spacing from `stage0.json` next to the design value.
- **w00auditfresh.**
  - ON/OFF, the binomial test, the bootstrap and the CI are re-computed from `wa_result.json` rows. Each row stores only `abs_um` and `signed_um`, not where w00 sits.
  - The cross-check with Chris's mark files tests which stations he marked, so a can't-tell change is caught. It does not test where the marks are.
  - On a copy, every recorded mark position in one session's mark file was shifted by 0.5 (the file's units look like mm). Every quoted number stayed the same.
  - Fix: ship w00's trace position per station (`w00_um`) and check `abs_um == |w00_um − mark_um|` from the mark files.

## Smaller fixes for OK scripts

- **Printed but not asserted:**
  - copyfix9: the line "cf.py saved result ... identical: True";
  - phasesym: the Judge's 5 window-level pairs ("same / DIFFERENT"), and the void-T-phase gate (prereg L44);
  - snap3arm: the p range 0.25-0.5;
  - mark2r: the centre-bias flag (prereg L64-65).

  Turn each of these into an assert.
- **Hashes and counts:** spiralread0841 checks only Sebastien's file hash. w00native has no row-count check (6 553) and no hash on the CSV.
- **humantol:** assert that the answer set equals the key's ids and that every answer is one of rows / strokes / nothing.
