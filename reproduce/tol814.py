"""TOL-814 re-score (outline: "Failures and limits", FULL-HOP-W bullet, "Second patch (TOL-814 ...)").

Ports the Judge's independent re-score ([private path]
at private commit `60b819bd`), which applies the prereg outcome rule (standalone/preregs/fullhop_s022814.md to the
saved page key + both blind ratings files. Dose numbers (moved shares, hop sizes, Stage 0b/0d AUCs and shares) are RE-READ from the saved
CPU/GPU stage outputs (f170/surf.json, t8_s0b_f140/f170_result.json); they are not recomputed (that needs the 4.5 GB surfaces).

Stdlib only. Paths are relative to this file. Exit 0 only if every number matches EXPECTED.
"""
import hashlib
import json
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "tol814"
ITEM = "[private path] @60b819bd"

EXPECTED = {
    # ITEM L197: "FAIL = FAILS-814 (2 of 2 raters valid, ctrl814 rows for both, L70_814 not rows for 1 valid rater)"
    "verdict": "FAILS-814",
    "valid_raters": 2,
    "window_ok": 2,
    # checks/20261007-26-*/judge_rescore_out.json "rows_count_of_2" (@60b819bd); ITEM L214-L218
    "rows_count_of_2": {"ctrl814_level": 2, "L85_814_level": 2, "L70_814_level": 1, "L55_814_level": 1,
                        "H50_814_level": 2},
    # ITEM L216-L217 + L223: crossed calls. Chris: L70 strokes, L55 rows. Sebastien: L70 rows, L55 strokes.
    "L70_L55_calls": {"chris": ("strokes", "rows"), "seb": ("rows", "strokes")},
    # ITEM L219 / L242: all three blanks rejected by both
    "blanks_rejected_of_3": {"chris": 3, "seb": 3},
    # judge_rescore_out.json "sha12" (@60b819bd)
    "sha12": {"seb": "eeeae260532b", "chris": "bf1847150a03"},
    # ITEM L233: "Vertices moved > 50 um: 0.165 / 0.322 / 0.476 (L85 / L70 / L55). Median move ~200 um."
    "moved_gt50_vertex_frac": {"L85_814": 0.165, "L70_814": 0.322, "L55_814": 0.476},
    "median_move_um_rounded_10": {"L85_814": 200, "L70_814": 200, "L55_814": 200},
    # ITEM L162: "run law 170-250 um (constant 200 um)"
    "floor_um": 170,
    "const_um": 200,
    # ITEM L232: "At floor 140 the reader still reached the true text (0.577 vs bar 0.559)"
    "f140_hop_auc": 0.577,
    "f140_bar": 0.559,
    "f140_hop_ok": False,
    # ITEM L229: "0b at floor 170: the hop pixels' label AUC is 0.503 vs blank 0.495 (bar 0.545)"
    "f170_hop_auc": 0.503,
    "f170_blank": 0.495,
    "f170_bar": 0.545,
    "f170_hop_ok": True,
    # prereg L86: unmoved pixels, AUC(L70_814 rev) >= AUC(ctrl814 rev, same pixels) - 0.02, at both floors; job flags too
    "f140_unmoved_ok": True, "f170_unmoved_ok": True,
    "job_flags_hop_unmoved": {"f140": [False, True], "f170": [True, True]},
    # prereg Stage 0d (t8.py DARK_OVER 0.10): off_sheet_moved <= off_sheet_same_vertices_on_base + 0.10, each level
    "s0d_dark_hops_ok": {"L85_814": True, "L70_814": True, "L55_814": True},
    # the scorer's own saved result (t8.py score) gives the same verdict as the re-score above
    "saved_score_verdict": "FAILS-814",
    # MEASURED hop sizes at floor 170 (f170_surf.json, moved > 50 um vertices). The README's "hops had to be at least
    # 170 um" is the hop LAW floor above, not these: the measured p10 is below it (docs/WORDING_FLAGS.md flag 2).
    "measured_p10_um": {"L85_814": 110.3, "L70_814": 130.5, "L55_814": 145.7},
    "measured_p50_um": {"L85_814": 198.2, "L70_814": 199.7, "L55_814": 200.0},
}

fails = []


def r3(x):
    """Round half-up to 3 decimals, as the verdict text does (saved values carry 4 decimals, e.g. 0.4945 -> 0.495;
    Python's round() on the float gives 0.494)."""
    from decimal import Decimal, ROUND_HALF_UP
    return float(Decimal(str(x)).quantize(Decimal("0.001"), rounding=ROUND_HALF_UP))


def check(name, got, exp):
    ok = got == exp
    print(f"{'OK      ' if ok else 'MISMATCH'} {name}: got {got!r}  expected {exp!r}")
    if not ok:
        fails.append(name)


key = json.loads((DATA / "t8_page_key.json").read_text(encoding="utf-8"))
name = {}
for q, m in key.items():
    if m["item"] == "TOL-814":
        name[q] = f'{m["surface"]}_{m["kind"]}'
    elif m["item"] == "shared":
        name[q] = m["kind"]          # LINE-FIELD-READ's O2 / O45 never count here (prereg; t8.rater skip list)
out = {}
for who, fn in (("seb", "seb_tol814_ratings.json"), ("chris", "chris_tol814_ratings.json")):
    raw = (DATA / fn).read_bytes()
    ans = json.loads(raw)["answers"]
    c = {name[q]: ans.get(q) for q in name}
    answered = all(v is not None for v in c.values())
    valid = answered and c["calib"] == "rows" and all(c[b] != "rows" for b in ("blank09", "ctrl814_blank", "L70_814_blank"))
    out[who] = dict(c=c, valid=valid, window_ok=valid and c["ctrl814_level"] == "rows",
                    sha=hashlib.sha256(raw).hexdigest()[:12])
V = [r for r in out.values() if r["valid"]]
W = [r for r in V if r["window_ok"]]
if len(V) < 2:
    verdict = "UNDECIDED (<2 valid)"
elif any(r["c"]["L70_814_level"] != "rows" for r in W):
    verdict = "FAILS-814"
elif len(W) == 2 and all(r["c"]["L70_814_level"] == "rows" for r in W) and \
        any(r["c"][g] != "rows" for r in W for g in ("H50_814_level", "L55_814_level")):
    verdict = "HOLDS-814"
else:
    verdict = "UNDECIDED"

lv = ["ctrl814_level", "L85_814_level", "L70_814_level", "L55_814_level", "H50_814_level"]
check("verdict", verdict, EXPECTED["verdict"])
check("valid_raters", len(V), EXPECTED["valid_raters"])
check("window_ok", len(W), EXPECTED["window_ok"])
check("rows_count_of_2", {s: sum(r["c"][s] == "rows" for r in out.values()) for s in lv}, EXPECTED["rows_count_of_2"])
check("L70_L55_calls", {w: (r["c"]["L70_814_level"], r["c"]["L55_814_level"]) for w, r in out.items()},
      EXPECTED["L70_L55_calls"])
check("blanks_rejected_of_3",
      {w: sum(r["c"][b] != "rows" for b in ("blank09", "ctrl814_blank", "L70_814_blank")) for w, r in out.items()},
      EXPECTED["blanks_rejected_of_3"])
check("sha12", {w: r["sha"] for w, r in out.items()}, EXPECTED["sha12"])

surf = json.loads((DATA / "f170_surf.json").read_text(encoding="utf-8"))
S = surf["surfaces"]
check("moved_gt50_vertex_frac", {s: round(S[s]["moved_gt50_vertex_frac"], 3) for s in S}, EXPECTED["moved_gt50_vertex_frac"])
check("median_move_um_rounded_10", {s: int(round(S[s]["moved_um_pct"]["p50"], -1)) for s in S},
      EXPECTED["median_move_um_rounded_10"])
check("floor_um", surf["floor_um"], EXPECTED["floor_um"])
check("const_um", int(surf["c0_um"]), EXPECTED["const_um"])
# MEASURED hop sizes, asserted (WORDING_FLAGS flag 2: law floor 170 um, measured p10 110-146 um, median ~200 um)
check("measured_p10_um", {s: S[s]["moved_um_pct"]["p10"] for s in S}, EXPECTED["measured_p10_um"])
check("measured_p50_um", {s: S[s]["moved_um_pct"]["p50"] for s in S}, EXPECTED["measured_p50_um"])
check("s0d_dark_hops_ok", {s: S[s]["off_sheet_moved"] <= S[s]["off_sheet_same_vertices_on_base"] + 0.10 for s in S},
      EXPECTED["s0d_dark_hops_ok"])

b140 = json.loads((DATA / "t8_s0b_f140_result.json").read_text(encoding="utf-8"))
b170 = json.loads((DATA / "t8_s0b_f170_result.json").read_text(encoding="utf-8"))
# bar = min(blank + 0.05, 0.70): TOL-814's own cap (prereg L84, t8.py @60b819bd L35 HOP_MAX_ABS = 0.70), NOT
# FULL-HOP-W's 0.62. The cap does not bind here (blank + 0.05 = 0.559 / 0.5445), so the bars are the same either way.
for tag, b in (("f140", b140), ("f170", b170)):
    check(f"{tag}_bar recomputed", round(min(b["auc_blank_same_px"] + 0.05, 0.70), 4), round(b["bar_hop"], 4))
    check(f"{tag}_unmoved_ok", b["auc_unmoved"] >= b["auc_unmoved_ctrl"] - 0.02, EXPECTED[f"{tag}_unmoved_ok"])
check("job_flags_hop_unmoved", {t: [b["hop_ok"], b["unmoved_ok"]] for t, b in (("f140", b140), ("f170", b170))},
      EXPECTED["job_flags_hop_unmoved"])
check("f140_hop_auc", r3(b140["auc_hop"]), EXPECTED["f140_hop_auc"])
check("f140_bar", r3(b140["bar_hop"]), EXPECTED["f140_bar"])
check("f140_hop_ok", b140["auc_hop"] <= b140["bar_hop"], EXPECTED["f140_hop_ok"])
check("f170_hop_auc", r3(b170["auc_hop"]), EXPECTED["f170_hop_auc"])
check("f170_blank", r3(b170["auc_blank_same_px"]), EXPECTED["f170_blank"])
check("f170_bar", r3(b170["bar_hop"]), EXPECTED["f170_bar"])
check("f170_hop_ok", b170["auc_hop"] <= b170["bar_hop"], EXPECTED["f170_hop_ok"])

saved = json.loads((DATA / "t8_score_result.json").read_text(encoding="utf-8"))
check("saved_score_verdict", saved["verdict"], EXPECTED["saved_score_verdict"])
check("saved_score_verdict == re-scored verdict", saved["verdict"] == verdict, True)

print(f"\nTOL-814: {'MATCH' if not fails else 'MISMATCH ' + ', '.join(fails)}  (source: {ITEM})")
sys.exit(1 if fails else 0)
