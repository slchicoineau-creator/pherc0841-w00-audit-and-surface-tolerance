"""LINE-FIELD-READ re-score (outline: "Line spacing check with perfect lines").

1. Ports the Judge's independent re-score ([private path]
   at private commit `60b819bd`): prereg F3/F4 (standalone/preregs/line_spacing.md applied to TOL-814's
   page key + both blind ratings files (the O2 / O45 pictures sat on TOL-814's 11-picture page).
   NOT ported: the Judge's black-share check of the JPEGs embedded in the rating page (needs the 666 KB HTML page with
   images, which this package does not carry); the saved Judge output is in data/linefieldread/judge_rescore_out.json.
2. Recomputes the BUILDER-FORMULA line spacing (2.02 / 4.54 mm = (last ring row - first ring row) x grid step / (n - 1);
   ring rows read from the saved rings_O2.json / rings_O45.json) and the forecast floor (8.5-10.8 min/cm2) with the
   arithmetic of checks/20261011-14-*/ideas_forecast_odds.py (@60b819bd) from the saved line set, region and paces.
   The 10.8 end uses the clicked-span pace 5.22 mm/min, a constant in ideas_forecast_odds.py L10 (BRIEF S8b), not data here.
   Also MEASURES the spacing of the built lines (mean z gap between consecutive lines, in 9.366 um voxels) from the saved
   line sets lines_O.json (O2) and lines_O45.json (O45): O2 1.80 mm, O45 4.054 mm (= stage0.json a0_ring). The lines came
   out ~0.89x the builder formula (docs/WORDING_FLAGS.md flag 3); both are asserted.
3. Re-reads the construction distance of O2 from s022814 (median 33 um) from the saved field_O_result.json (local only).

Stdlib only. Paths are relative to this file. Exit 0 only if every number matches EXPECTED.
"""
import hashlib
import json
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "linefieldread"
ITEM = "[private path] @60b819bd"

EXPECTED = {
    # ITEM L359: "PASS = O2-READS (primary). Secondary arm O45-FAILS (O45-SPLIT). 2 of 2 raters valid, ctrl814 rows for both."
    "O2_verdict": "READS",
    "O45_verdict": "FAILS (SPLIT)",
    "n_valid_ctrl_rows": 2,
    # ITEM L401-L402: O2 rows / rows; O45 Sebastien rows, Chris strokes
    "O2_rows_of_2": 2,
    "O45_rows_of_2": 1,
    "O45_calls": {"seb": "rows", "chris": "strokes"},
    # ITEM L404 + L409-L411: guard (L55_814 / H50_814) rejected only by Sebastien (L55_814); H50_814 rows for both;
    # Chris called L70_814 and O45 strokes in the same sitting
    "guard_rejected_by": ["seb"],
    "H50_814_rows_of_2": 2,
    "chris_L70_814_and_O45": ("strokes", "strokes"),
    # ITEM L383 (11 pictures) + L393 (O2 q10 and O45 q08 not adjacent)
    "page_pictures": 11,
    "O2_O45_adjacent": False,
    # judge_rescore_out.json (@60b819bd) "sha256"
    "sha256": {"seb": "eeeae260532b0c1ad5a1d38623f5b586b1f0b589bafeb31ab0b67b902d8418df",
               "chris": "bf1847150a030fbe399ce9e5eeebb9717fb25e04cebf2a47c12bed539bb0ecdb"},
    # prereg L51-L52: O2 = 10 lines 2.02 mm apart; O45 = 5 lines 4.54 mm apart
    "O2_n_lines": 10,
    "O2_spacing_mm": 2.02,
    "O45_spacing_mm": 4.54,                                   # README-quoted; builder formula, not measured
    # MEASURED spacing of the built lines (mean z gap x 9.366 um); WORDING_FLAGS flag 3
    "measured_O2_spacing_mm": 1.802,
    "measured_O45_spacing_mm": 4.054,                         # = stage0.json a0_ring.mean_z_spacing_mm
    "stage0_O45_mean_z_spacing_mm": 4.054,
    "ring_rows_first_last": {"O2": (9.0, 106.0), "O45": (9.0, 106.0)},   # rings_*.json grid_rc rows
    # prereg Stage 0d frame gate (stage0.json d0_frame): ok, black_ok, moved_ok all True
    "stage0_d0_frame": {"ok": True, "black_ok": True, "moved_ok": True},
    # ITEM L36-L38 (Idea): lines average 11.8 mm, region M 2.10 cm2; O2 8.5-10.8 min/cm2, O45 4.2-5.4 min/cm2
    "line_len_mm_mean": 11.8,
    "area_cm2": 2.1018,
    "O2_min_per_cm2": (8.5, 10.8),
    "O45_min_per_cm2": (4.2, 5.4),
    # ITEM L125 / L418: "median 33 um from s022814 by construction"
    "O2_median_um_from_s022814": 33.0,
}

fails = []


def check(name, got, exp):
    ok = got == exp
    print(f"{'OK      ' if ok else 'MISMATCH'} {name}: got {got!r}  expected {exp!r}")
    if not ok:
        fails.append(name)


ROWS = "rows"
key = json.loads((DATA / "t8_page_key.json").read_text(encoding="utf-8"))


def name(m):
    return m["kind"] if m["item"] == "shared" else f"{m['surface']}_{m['kind']}"


R = {}
for w, fn in (("seb", "seb_tol814_ratings.json"), ("chris", "chris_tol814_ratings.json")):
    raw = (DATA / fn).read_bytes()
    a = json.loads(raw)["answers"]
    c = {name(m): a.get(q) for q, m in key.items()}
    valid = all(v is not None for v in c.values()) and c["calib"] == ROWS and \
        all(c[b] != ROWS for b in ("blank09", "ctrl814_blank", "L70_814_blank"))
    R[w] = dict(valid=valid, ctrl_rows=c["ctrl814_level"] == ROWS, calls=c, sha256=hashlib.sha256(raw).hexdigest())

arms = {}
for x in ("O2", "O45"):
    d = [r for r in R.values() if r["valid"] and r["ctrl_rows"]]
    nots = [r for r in d if r["calls"][f"{x}_level"] != ROWS]
    guard = any(r["calls"][g] != ROWS for r in d for g in ("H50_814_level", "L55_814_level"))
    if not d:
        v = "VOID"
    elif nots:
        v = "FAILS (" + ("NO" if len(nots) == len(d) == 2 else "SPLIT" if len(d) == 2 else "one valid rater") + ")"
    elif len(d) == 1:
        v = "UNDECIDED (one-rater lead)"
    else:
        v = "READS" if guard else "LENIENT"
    arms[x] = dict(verdict=v, n=len(d), rows=len(d) - len(nots),
                   guard_rejected_by=[w for w, r in R.items() if r in d and
                                      any(r["calls"][g] != ROWS for g in ("H50_814_level", "L55_814_level"))])

order = sorted(key)
pos = {name(key[q]): i for i, q in enumerate(order)}
check("O2_verdict", arms["O2"]["verdict"], EXPECTED["O2_verdict"])
check("O45_verdict", arms["O45"]["verdict"], EXPECTED["O45_verdict"])
check("n_valid_ctrl_rows", arms["O2"]["n"], EXPECTED["n_valid_ctrl_rows"])
check("O2_rows_of_2", arms["O2"]["rows"], EXPECTED["O2_rows_of_2"])
check("O45_rows_of_2", arms["O45"]["rows"], EXPECTED["O45_rows_of_2"])
check("O45_calls", {w: R[w]["calls"]["O45_level"] for w in R}, EXPECTED["O45_calls"])
check("guard_rejected_by", arms["O2"]["guard_rejected_by"], EXPECTED["guard_rejected_by"])
check("H50_814_rows_of_2", sum(R[w]["calls"]["H50_814_level"] == ROWS for w in R), EXPECTED["H50_814_rows_of_2"])
check("chris_L70_814_and_O45", (R["chris"]["calls"]["L70_814_level"], R["chris"]["calls"]["O45_level"]),
      EXPECTED["chris_L70_814_and_O45"])
check("page_pictures", len(key), EXPECTED["page_pictures"])
check("O2_O45_adjacent", abs(pos["O2_level"] - pos["O45_level"]) == 1, EXPECTED["O2_O45_adjacent"])
check("sha256", {w: R[w]["sha256"] for w in R}, EXPECTED["sha256"])

# Spacing + forecast: same arithmetic as ideas_forecast_odds.py (@60b819bd)
VOX_MM = 9.366 / 1000                  # s022814 native voxel (lines_O*.json coordinates are in these voxels)
STEP_MM = 20 * VOX_MM                  # native grid step = 0.18732 mm (lr814.py GRID_MM)
J = lambda f: json.loads((DATA / f).read_text(encoding="utf-8"))
rings = {"O2": J("rings_O2.json")["rings"], "O45": J("rings_O45.json")["rings"]}
check("ring_rows_first_last", {a: (r[0]["grid_rc"][0], r[-1]["grid_rc"][0]) for a, r in rings.items()},
      EXPECTED["ring_rows_first_last"])
line_sets = {"O2": [l for l in J("lines_O.json")["lines"] if l], "O45": [l for l in J("lines_O45.json")["lines"] if l]}
lines = line_sets["O2"]
L = sum((len(l["k"]) - 1) * STEP_MM for l in lines) / len(lines)
A = J("region.json")["area_cm2"]
pace_saved = J("fiber9b_speed.json")["pace_mm_per_min"]
# 5.22 / 6.17 mm/min = FIBER-9B clicked-span pace, hard-coded in ideas_forecast_odds.py L10 (from BRIEF S8b; ITEM L134)
paces = [pace_saved, 5.22, 6.17]
check("O2_n_lines", len(lines), EXPECTED["O2_n_lines"])
check("line_len_mm_mean", round(L, 2), EXPECTED["line_len_mm_mean"])
check("area_cm2", A, EXPECTED["area_cm2"])
for arm, n in (("O2", 10), ("O45", 5)):
    assert len(rings[arm]) == n and len(line_sets[arm]) == n, (arm, len(rings[arm]), len(line_sets[arm]))
    g0, g1 = rings[arm][0]["grid_rc"][0], rings[arm][-1]["grid_rc"][0]
    check(f"{arm}_spacing_mm (builder formula)", round((g1 - g0) * STEP_MM / (n - 1), 2), EXPECTED[f"{arm}_spacing_mm"])
    # measured: each line lies at one z (a z-contour); mean gap between first and last line
    zs = [l["P"][0][2] for l in line_sets[arm]]
    assert all(len({p[2] for p in l["P"]}) == 1 for l in line_sets[arm])
    check(f"measured_{arm}_spacing_mm", round((zs[-1] - zs[0]) / (n - 1) * VOX_MM, 3), EXPECTED[f"measured_{arm}_spacing_mm"])
    mins = [round(n * L / v / A, 1) for v in paces]
    check(f"{arm}_min_per_cm2", (min(mins), max(mins)), EXPECTED[f"{arm}_min_per_cm2"])

fo = json.loads((DATA / "field_O_result.json").read_text(encoding="utf-8"))
check("O2_median_um_from_s022814", fo["dist_vs_s022814_construction_only"]["median_um"],
      EXPECTED["O2_median_um_from_s022814"])

st = J("stage0.json")
check("stage0_O45_mean_z_spacing_mm", st["a0_ring"]["mean_z_spacing_mm"], EXPECTED["stage0_O45_mean_z_spacing_mm"])
check("stage0_d0_frame", {k: st["d0_frame"][k] for k in ("ok", "black_ok", "moved_ok")}, EXPECTED["stage0_d0_frame"])
print("NOT REPRODUCED here: page black-share check (needs the image page); saved Judge value worst_gap_pts_vs_O = "
      f"{json.loads((DATA / 'judge_rescore_out.json').read_text(encoding='utf-8'))['worst_gap_pts_vs_O']}")

print(f"\nLINE-FIELD-READ: {'MATCH' if not fails else 'MISMATCH ' + ', '.join(fails)}  (source: {ITEM})")
sys.exit(1 if fails else 0)
