# Evidence, group B: outline row 5 (the w00 audit)

Outline: `submission/READABLE_SURFACE_BUDGET_OUTLINE.md` @ 40f0e4211, row 5. (This audit checked that version; its WORDING_FLAGS were accepted by Chris and applied in outline cf541ce98, 2026-10-20.) All paths below are at `60b819bd`
(the private repository) unless marked "local only". Inputs and their sha256 are in `docs/manifest_B.json`.
Run: `python reproduce/<test>.py` (exit 0 = every compared number matches). Run 2026-10-18: all four exit 0.

## W00-NATIVE (`reproduce/w00native.py`)

- Prereg `standalone/preregs/w00_native_scan.md`. Pre-loop: no loop item or Judge verdict. Result in
  `[private path]` §7 + `[private path]`.
- Verdict label: **G, the mesh itself (its 187 µm grid) is the main cause** (PROPOSAL_truth.md line 163).
- Input: the per-cross A25 rows (`[private path]`, local only, 1.27 MB),
  converted without loss to CSV (0.77 MB). A25 itself needs the CT volumes, so it is not recomputed. The script re-applies
  the frozen `verdict()` rule from `w00native.py`.

| Number in outline | Source line | Status |
|---|---|---|
| median 0.10 on copy and on native | PROPOSAL l.158 (0.100 / 0.101) | MATCH |
| ±75 µm shift → 0.11 / 0.13 (copy arm) | PROPOSAL l.168 (0.113 / 0.133) | MATCH (native arm 0.120 / 0.139 also MATCH) |
| Spearman 0.33 with bend | PROPOSAL l.162 (0.327) | MATCH |
| verdict G (n 6479, median D 0.00, 2760 vs 2939, share > 0.3 0.170 / 0.169) | PROPOSAL l.159-163 | MATCH |
| 187 µm grid | PROPOSAL l.151, prereg l.14 | MATCH (meta.json scale 0.05 × 9.366 µm = 187.3 µm) |
| affine residual 14 µm | prereg l.15 ("13.9 µm") | NOT REPRODUCIBLE from small files: needs both full meshes (TIFFs over 1 MB) |

## TRUSTED-P (`reproduce/trustedp.py`)

- Prereg `standalone/preregs/w00_trusted_crosses.md`. Pre-loop: result in PROPOSAL_truth.md §6 +
  `checks/truth-audit/trustedP_fit.json`, `trustedP_ratings_counts.json`.
- Verdict label: **calibration gate FAIL** (balanced accuracy 0.696 < 0.80). One rater (Sebastien).
- Inputs: `[private path]` + `trustedP_seb_ratings.json` (both local only).

| Number in outline | Source line | Status |
|---|---|---|
| 33 of 46 not on one sheet (13 Yes, 33 No, 2 Can't) | PROPOSAL l.126 | MATCH |
| clean 7/15, middle 12/16, suspect 14/15 | PROPOSAL l.127 | MATCH (Can't tells left out of the denominator) |
| gate failed (BA 0.696, θA 0.10, θB 15, repeats 3/4) | PROPOSAL l.126, l.129; trustedP_fit.json | MATCH |
| fresh h0/h2 crosses: w00 stayed 20/29 | PROPOSAL l.186 (11/14 h0) + l.214 (9/15 h2) | NOT REPRODUCED here: this is the w00 arm of the row-6 tests (REFINE-24/MIDLINE/SHEETLINE), so it is checked against the text only. 11 + 9 = 20 and 14 + 15 = 29 agree. |

## W00-AUDIT-FRESH (`reproduce/w00auditfresh.py`)

- Prereg `standalone/preregs/audit_guidefree.md`; item `[private path]`
  (Runner result l.250-264, Judge verdict l.277-333); Judge script + output
  `[private path]`, `judge_rescore_out.json`.
- Verdict label: **PASS, outcome AGREE-BELOW-9IN10** (pair wording; item l.281).
- Input: `[private path]` (local only). It holds the w00-to-mark distance
  per station. w00's trace needs the mesh and the CT frames, so the script starts from these distances, as the Judge did.
  The script also checks the rows against Chris's guide-free mark files (`of9/oc9/cf9_chris_key.json` + page keys, local only):
  the same stations are marked and there are 14 + 14 can't-tells. The script checks the sha256 pins of `wa.py` PINS (@ 60b819bd)
  for the of9/oc9 mark files, all 3 page keys and the 3 frames files (`of9/oc9/cf9_frames.json`); cf9_chris_key.json has no pin
  (it arrived after the prereg).
- Mark positions vs w00 geometry: only at station 0. For every strip, (Chris's station-0 mark − the ring n from the frames
  file) × 1000 must equal the Judge's `station0_mark_minus_ring_um` (`[private path]
  judge_station0_result.json`, local only) within 0.5 µm, and w00 sits within 1 µm of the ring at station 0 on all 16 + 9 strips
  (`wa_stage0.json` b_ring). A 0.5 mm shift of one mark file now fails.
- **Limit:** w00's trace position at stations 1..6 is not in any saved file (wa.py computes it from the w00 mesh `mesh_P` and
  saves only the distances), so the per-station `abs_um` values are re-read, not recomputed from the marks. A mark change
  confined to stations 1..6 that crosses no 75 µm line is not caught.

| Number in outline | Source line | Status |
|---|---|---|
| 42/82 within 75 µm, 0.51, CI 0.40-0.62 | item l.250-251, Judge l.293 | MATCH (CP 0.3992-0.6242; crit OFF 14; bootstrap UB 0.6374) |
| 20 of 40 misses 75-150 µm | item l.256 | MATCH |
| key-noise e ≤ 0.10 → ≤ 0.57 | item l.260-261 (0.569), Judge l.305 | MATCH |
| replication 18/40, 16 of 22 misses > 150 µm | item l.263-264, Judge l.294, l.321 | MATCH (bootstrap UB 0.6667) |
| (H) fresh along bend 5/28 vs flat 14/18 (46 stations) | item l.255, Judge l.318 | MATCH (fresh along 19/46) |
| 10 fresh strips 7 bend / 3 flat + 6 cross strips | item l.79, l.270, l.330 | MATCH (strip kinds counted from the rows) |

## MARK-2R (`reproduce/mark2r.py`)

- Prereg `standalone/preregs/audit_guided.md`; item `[private path]`
  (Runner l.154-166, Judge verdict l.171-239); Judge script `[private path]`;
  scorer `[private path]`.
- Verdict label: **PASS (human floor KEY OK)**; row 5 = **MEASURED, not CONFIRMED**; flags "Chris repeats unreliable",
  "consistent with following the guide line" (item l.175-178).
- Inputs: `mark2r_key.json`, `mark2r_seb_ratings.json`, `mark2r_chris_ratings.json` (all local only). These marks are
  GUIDED (w00's line shown up to 0.3 mm before the spot), so the manifest tags them `ratings`, not `marks_2p4um`.
- Median rule: `sorted(d)[n // 2]` as in mark2r_score.py (14.4 µm). The Judge's low median gives the same 14.4 here.

| Number in outline | Source line | Status |
|---|---|---|
| human-human 18/20 within 75 µm, median 14 µm (CI 0.683-0.988) | item l.175 | MATCH |
| w00 continues 19/21 (Sebastien), 15/22 (Chris) | item l.163, l.176 | MATCH |
| straight extension 23/25 | item l.154, l.165 | MATCH |
| Chris repeats 0 of 2 within 75 µm (138 / 244 µm) | item l.166, l.177 | MATCH (137.8 / 243.5) |
| MEASURED not CONFIRMED; guide-line flag | item l.176-178 | MATCH |
| 14 µm affine residual | W00-NATIVE prereg l.15 | NOT REPRODUCIBLE (see W00-NATIVE) |

## Which preregs and items name each input file

Search: `git grep -l -F <file name>` over `[private path]` and `[private path]`, at `60b819bd` and at
`origin/the private repository = `2c28a25c0` (fetched 2026-10-18). The lists are **identical at both commits**.
Only paths were listed; no matched file was opened, and none of these items' statuses were checked.

- **of9_chris_key.json** (Chris, guide-free): prereg orientfresh9, orientclick9, laspresnap9, **laykey9**; items
  20261008-11 orient-fresh-9, 20261008-12 orient-click-9, 20261008-21 cross-fresh-9, 20261008-23 w00-bend-fresh,
  20261009-01 w00-audit-fresh, 20261010-07 las-presnap-9, **20261011-19 lay-key-9**.
- **oc9_chris_key.json** (Chris, guide-free): prereg orientcross9; items 20261008-15 orient-cross-9, 20261009-01.
- **cf9_chris_key.json** (Chris, guide-free): prereg crossfresh9, partner_w00bendpool9, w00auditfresh, laspresnap9;
  items 20261008-21, 20261009-01, 20261010-07 las-presnap-9, 20261011-04 one-end-9.
- **wa_result.json** (built from these marks): prereg partner_w00bendpool9, w00auditfresh, **laykey9**; items 20261009-01,
  20261010-06 key-tiebreak-9, **20261011-19 lay-key-9**.
- mark2r_seb_ratings / mark2r_chris_ratings: item 20261005-20 only. mark2r_key.json: prereg mark2r + item 20261005-20.
- trustedP_key.json, trustedP_seb_ratings.json: prereg trustedP + item 20261005-13 copy-flag.
- w00native_rows.json: no prereg or item names it.

**Open question before anything is published:** LAY-KEY-9 (`[private path]`, item 20261011-19) names
both `of9_chris_key.json` and `wa_result.json`. Its name falls under the brief's sealed or live-test patterns, so it was not
opened. Someone must check whether LAY-KEY-9, LAS-PRESNAP-9, KEY-TIEBREAK-9, ONE-END-9 or W00-BENDPOOL-9 still uses Chris's
of9/cf9 marks as a key before those files leave the private repo.
