# Pre-registration index

Each file in this folder is a scrubbed public copy of a pre-registration (or amendment) that was committed to the authors' private repository before the test it governs was run or rated, except where the note says otherwise. Times are commit times in UTC from `git log`.

**Timestamps live in a private repository; ask the authors for a verification** (they can show the commits).

**Paths and internal names inside the copies.** Paths into the private repository read `[private path]` and do not
resolve; earlier internal test names (such as FORMAT-20 or TOL-20) are kept so the text stays a faithful copy. In these
copies, "the team's" mesh w00 means the Vesuvius Challenge organizers' team's mesh, not ours. What this repo can rerun is
listed in the top-level README.

**Test names used in the README, with their copies here and their re-scoring scripts:**

| test name in the README | pre-registration copy (this folder) | script in `reproduce/` |
|---|---|---|
| HUMAN-TOL / HUMAN-TOL-SCORE | partsheet_tolerance.md, partsheet_tolerance_score.md | `humantol.py` |
| FULL-HOP-W | fullhop_w.md, fullhop_w_amend_F2.md | `fullhop.py` |
| TOL-814 | fullhop_s022814.md | `tol814.py` |
| CM2-READ | depth_w.md | `cm2read.py` |
| FRESH-WRAP | depth_s022814.md | `freshwrap.py` |
| SPIRAL-READ-0841 | spiral_field.md, spiral_field_amend3.md | `spiralread0841.py` |
| LINE-FIELD-READ | line_spacing.md | `linefieldread.py` |
| HUMAN-FLOOR | human_vs_agent.md | `humanfloor.py` |
| RAW-READ-9H | grown_field.md, grown_field_amend1_guard.md | `rawread9h.py` |
| NODE-FILL-READ / NODE-FILL-REREAD | no copy (both VOID; rules in `docs/evidence_A1.md`) | `nodefill.py` |
| W00-AUDIT-FRESH | audit_guidefree.md | `w00auditfresh.py` |
| MARK-2R | audit_guided.md | `mark2r.py` |
| TRUSTED-P | w00_trusted_crosses.md | `trustedp.py` |
| W00-NATIVE | w00_native_scan.md | `w00native.py` |
| REFINE-24 / MIDLINE / SHEETLINE | snapping_refine.md, snapping_midline.md, snapping_sheetline.md | `snap3arm.py` |
| PHASE-SYM-ROW7 | reader_phase.md | `phasesym.py` |
| COPY-FIX-9 + KEY2-STEP2 | handfix.md, handfix_key2.md | `copyfix9.py` |
| LASAGNA-FIT-9 | lasagna_fit.md, lasagna_fit_amend1.md | `lasagnafit9.py` |

| public slug | file | private commit (first add) | committed at (UTC) | later commits (UTC) | note |
|---|---|---|---|---|---|
| `partsheet_tolerance` | [partsheet_tolerance.md](partsheet_tolerance.md) | `724557744d6beeb775c4f8aef09b43985fb95937` | 2026-10-03T03:44:03Z | `db7081921` 2026-10-03T03:44:22Z<br>`509b98eb1` 2026-10-05T23:29:06Z | Original and amendment 1 committed before any rating. Amendment 2 (secondary agent-vs-human analysis) was committed on 2026-10-05, after the first rater's 2026-10-03 ratings and before the second rater's and before any scoring; the file itself discloses this. |
| `partsheet_tolerance` | [partsheet_tolerance_score.md](partsheet_tolerance_score.md) | `16247fbbb5846db88510ec2dcfd031341d8239a8` | 2026-10-07T04:27:43Z | `47d55bcb5` 2026-10-07T04:28:38Z | Both commits before any output (its Judge's check). |
| `depth_w` | [depth_w.md](depth_w.md) | `da2bf165440ce88c43fd93b54cdcff13a73c5a52` | 2026-10-06T01:07:02Z | `05d58d701` 2026-10-06T01:09:30Z | Original and amendment 1 committed and pushed before any output (its Judge's check). |
| `depth_s022814` | [depth_s022814.md](depth_s022814.md) | `ad690300dd3bde377e0d859f0ba2577b2596aa0b` | 2026-10-07T04:16:58Z | `ecd3e3686` 2026-10-07T04:19:31Z | Both commits pushed before the job was queued (its Judge's check). |
| `human_vs_agent` | [human_vs_agent.md](human_vs_agent.md) | `faaa82ea017d28d1410af3561f0ac56578aeff19` | 2026-10-06T03:24:47Z | none | Committed and pushed before any output (its Judge's check). |
| `audit_guided` | [audit_guided.md](audit_guided.md) | `f6f7dd0ec3bbb314b596e525232ed4baafbbdd5d` | 2026-10-06T14:20:47Z | `2a48de509` 2026-10-06T14:22:44Z | Original and amendment 1 (straight-line baseline) both committed before any output (its Judge's check). |
| `handfix` | [handfix.md](handfix.md) | `cf2d7d6187363bc4bcc640d0224ee2fdd3a29fb4` | 2026-10-06T22:36:21Z | `62c1a68bf` 2026-10-08T12:46:07Z | Original pushed before every output. The later commit (2026-10-08) changed the start surface; it came before the tool try and the timed session and changed no bar, metric or scorer (its Judge's check). |
| `handfix` | [handfix_key2.md](handfix_key2.md) | `27c9d342caf90fa190322ed9558e174ad58353ed` | 2026-10-09T01:10:12Z | `ca98394fb` 2026-10-09T01:13:11Z | Both commits pushed before every output (its Judge's check). |
| `grown_field` | [grown_field.md](grown_field.md) | `4020ceb49cd89e786d4c8d841833b5dd6c119e9a` | 2026-10-07T16:19:07Z | none | Committed and pushed before any output (its Judge's check). |
| `grown_field` | [grown_field_amend1_guard.md](grown_field_amend1_guard.md) | `2480a4044709b76df9be4195ffe3e2819cede611` | 2026-10-13T02:55:46Z | none | Amendment 1 (guard rule for the second read). Committed 66 s after the second-read page was built; the page was shown to the rater only after the push, before the rating (its Judge's check). |
| `fullhop_w` | [fullhop_w.md](fullhop_w.md) | `dcaf4984cf7556301d322b272a5db8d2d14e5a11` | 2026-10-08T13:09:08Z | none | Committed before the run's first output (its Judge's check). |
| `fullhop_w` | [fullhop_w_amend_F2.md](fullhop_w_amend_F2.md) | `a10666ff083c20ba4f34985ba6615b9e45d24f32` | 2026-10-11T17:24:38Z | none | Page amendment for the shared page; committed before the page build and before any rating (Judges' checks). |
| `fullhop_s022814` | [fullhop_s022814.md](fullhop_s022814.md) | `88da117addfcc647484488ebb4e1ff7dd66dc8ad` | 2026-10-08T13:31:54Z | `88c857c03` 2026-10-12T01:47:14Z, post-run, see the note at the end | This copy is the version of the first commit, made before any output (its Judge's check). A pointer note added after the ratings is reproduced at the end, labelled post-run. |
| `w00_trusted_crosses` | [w00_trusted_crosses.md](w00_trusted_crosses.md) | `7aa208df6ffeb1135b3b5b6003649a238d554452` | 2026-10-05T01:11:47Z | `d9e8e41b8` 2026-10-05T01:42:38Z<br>`ef1d4b7ad` 2026-10-05T02:20:54Z<br>`bdc71d6ab` 2026-10-05T03:49:23Z | Run in the main session, not by the station loop, so no loop Judge checked its timing. Timing of each amendment as stated in the file itself (amendments 1-2 before any rating or re-score, amendment 3 during the worked examples, before any real item). |
| `w00_native_scan` | [w00_native_scan.md](w00_native_scan.md) | `bc617bb5ae8d234959bee3780dfb8b48f6b41326` | 2026-10-05T05:05:03Z | none | Run in the main session, not by the station loop, so no loop Judge checked its timing; the file states it was pushed before any measurement on the native scan. |
| `snapping_refine` | [snapping_refine.md](snapping_refine.md) | `63dee78ddc68001457c6487e7b8d7f636805a6d0` | 2026-10-05T05:53:12Z | none | Run in the main session, not by the station loop, so no loop Judge checked its timing; the file states it was pushed before any agent saw a picture and before any refinement ran. |
| `snapping_midline` | [snapping_midline.md](snapping_midline.md) | `0b5692c1d3bc99233558e71aa85166f837178dfa` | 2026-10-05T12:55:45Z | `1c150ca1f` 2026-10-05T13:14:29Z | Run in the main session, not by the station loop, so no loop Judge checked its timing; amendment 1 (page size) states it came before any rating. |
| `snapping_sheetline` | [snapping_sheetline.md](snapping_sheetline.md) | `411fe0f873d943f26e81c34324928992b9b39c52` | 2026-10-05T19:30:19Z | `9b9bb5409` 2026-10-05T21:29:31Z<br>`2972ebcdf` 2026-10-05T21:54:50Z | Run in the main session, not by the station loop, so no loop Judge checked its timing; the file states it was pushed before any picture or page, and that amendments 1-2 came before any page or picture was seen. |
| `lasagna_fit` | [lasagna_fit.md](lasagna_fit.md) | `78efbb4a42744690f54f0506a1e4955469802b44` | 2026-10-07T19:19:46Z | `1ecc4e0d3` 2026-10-07T19:23:51Z | Original and fix commit both before any output (its Judge's check). |
| `lasagna_fit` | [lasagna_fit_amend1.md](lasagna_fit_amend1.md) | `732f49fc265e97cecf7aa2c5dccabc36ad96e621` | 2026-10-08T23:55:02Z | none | Amendment 1 (inward-ring route, larger box): pushed 6 min after the second job was launched, before any main output of that job existed (its Judge's check: a letter deviation, not a validity issue). |
| `audit_guidefree` | [audit_guidefree.md](audit_guidefree.md) | `bdc261bc08cdc32015759a69ea35a9c25206e37d` | 2026-10-09T12:56:05Z | `60d91cdd7` 2026-10-09T12:58:41Z | Both commits pushed before any output (its Judge's check). |
| `reader_phase` | [reader_phase.md](reader_phase.md) | `67882c2e0765ae08c06f8ee9279135c2d7c62ea0` | 2026-10-09T16:24:24Z | `1c0b048c8` 2026-10-09T16:29:09Z | Original and amendment both pushed before the first output (its Judge's check). |
| `line_spacing` | [line_spacing.md](line_spacing.md) | `c106700b081de85ed1b27139678b7bddbad3365a` | 2026-10-11T17:12:15Z | none | Committed before any output (its Judge's check). |
| `spiral_field` | [spiral_field.md](spiral_field.md) | `52381edc558167b62a1fe6aae73455c84bb37262` | 2026-10-13T03:05:22Z | `a439ffc42` 2026-10-13T03:08:48Z | Original and amendment both pushed before the first job (its Judge's check). |
| `spiral_field` | [spiral_field_amend3.md](spiral_field_amend3.md) | `351bc496ec36788b5f026de132946165083246a6` | 2026-10-13T15:02:26Z | none | Amendment 3 (no guard picture on one rater's page): pushed after both pages were built, but before either rating (its Judge's check). |

Timestamps live in a private repository; ask the authors for a verification.
