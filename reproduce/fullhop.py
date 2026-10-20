"""FULL-HOP-W re-score (outline: "Failures and limits", FULL-HOP-W bullet).

Ports the Judge's independent re-score ([private path]
at private commit `60b819bd`) and applies the pre-registered outcome rule (standalone/preregs/fullhop_w.md
to the saved page key + both blind ratings files. The Stage 0b dose margin is re-read from the saved Stage 0b output
(GPU-derived; the bar and the Stage 0b / 0d gates are recomputed from the prereg's formulas, the AUCs and the
off-sheet shares themselves are RE-READ, not recomputed here). Measured hop sizes are re-read from f140_surf.json.

Stdlib only. Paths are relative to this file. Exit 0 only if every number matches EXPECTED.
"""
import hashlib
import json
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "fullhop"
ITEM = "[private path] @60b819bd"

EXPECTED = {
    # ITEM L187: "Verdict by the pre-written rule: FAIL = FULL-HOP-FAILS (2 of 2 raters valid ...)"
    "verdict": "FULL-HOP-FAILS",
    "valid_raters": ["chris", "seb"],
    # ITEM L198-L199 (table) + L205-L206: C70d not rows for both, L70d split (Chris strokes, Sebastien rows)
    "C70d_not_rows": {"seb": True, "chris": True},
    "L70d_not_rows": {"seb": False, "chris": True},
    # ITEM L200 + L209: L40d (60 % full hops) guard not rows for both; H50n (50 % holes) rows for both
    "L40d_not_rows": {"seb": True, "chris": True},
    "H50n_rows": {"seb": True, "chris": True},
    # ITEM L202-L204 + L211: control L100 rows for both, all three blanks rejected by both, calibration rows for both
    "L100_rows": {"seb": True, "chris": True},
    "blanks_rejected_of_3": {"seb": 3, "chris": 3},
    "calib_rows": {"seb": True, "chris": True},
    # judge_rescore_out.json (checks/20261007-25-*/, @60b819bd) "sha256" per rater
    "sha256": {
        "seb": "fc6cf6fff25c6a33c24d8f5de5692b4f9ee45cf50304f15370454acf8b62734d",
        "chris": "998355afebd8b040086432302fb31e19b57befd930f3d5599d8d2e2a7f2334dd",
    },
    # ITEM L207: "L70d (+0) hop-pixel AUC 0.5755 vs bar 0.5756 (blank 0.526) ... (L70d by 0.0001)"
    "L70d_hop_auc": 0.5755,
    "L70d_bar": 0.5756,
    "L70d_margin": 0.0001,
    # ITEM L207: "C70d (-22) 0.611 vs bar 0.614 (blank 0.564)"
    "C70d_hop_auc": 0.611,
    "C70d_bar": 0.614,
    # ITEM L128 / L191: floor 140 um, no 170 fallback; prereg hop law far end 250 um (outline "140-250 um")
    "floor_um": 140,
    "far_um": 250,
    # MEASURED hop sizes (f140_surf.json, moved > 50 um vertices). These are what the surface really did; the README's
    # "every damaged patch moved a full sheet (140-250 um)" is the hop LAW above, not these (docs/WORDING_FLAGS.md flag 2).
    "measured_L70d_p10_um": 129.1, "measured_L70d_p50_um": 163.8, "measured_L70d_share_moved_le130": 0.1019,
    "measured_C70d_p10_um": 149.2, "measured_C70d_p50_um": 163.5, "measured_C70d_share_moved_le130": 0.0416,
    # prereg L74-81 Stage 0b gates, recomputed from the saved AUCs, and the job's own flags (all must be True)
    "s0b_hop_gate": {"L70d": True, "C70d": True},          # auc_hop <= bar_hop
    "s0b_unmoved_gate": {"L70d": True, "C70d": True},      # auc_unmoved >= auc_unmoved_rated_parent - 0.01
    "s0b_job_flags": {"L70d": [True, True], "C70d": [True, True]},   # saved [hop_ok, unmoved_ok]
    # prereg L67-71 Stage 0d DARK-HOPS: off_sheet_moved <= off_sheet_same_vertices_on_P + 0.10
    "s0d_dark_hops_ok": {"L70d": True, "C70d": True},
}

fails = []


def check(name, got, exp):
    ok = got == exp
    print(f"{'OK      ' if ok else 'MISMATCH'} {name}: got {got!r}  expected {exp!r}")
    if not ok:
        fails.append(name)


key = json.loads((DATA / "fh_page_key.json").read_text(encoding="utf-8"))
raters = {}
for who, fn in (("seb", "seb_fullhop_ratings.json"), ("chris", "chris_fullhop_ratings.json")):
    raw = (DATA / fn).read_bytes()
    ans = json.loads(raw)
    ans = ans.get("answers", ans) if isinstance(ans, dict) else ans
    calls = {}
    for tid, m in key.items():
        if m.get("item") not in ("FULL-HOP-W", "shared"):
            continue
        nm = m["kind"] if m["item"] == "shared" else f"{m['surface']}_{m['kind']}"
        calls[nm] = ans.get(tid)
    # prereg L103: every own picture answered; calib rows; 0009B blank, L70d blank, C70d blank each not rows; L100 rows
    valid = (all(v is not None for v in calls.values()) and calls["calib"] == "rows" and calls["blank09"] != "rows"
             and calls["L70d_blank"] != "rows" and calls["C70d_blank"] != "rows" and calls["L100_level"] == "rows")
    raters[who] = dict(valid=valid, calls=calls, sha256=hashlib.sha256(raw).hexdigest())

V = sorted(w for w in raters if raters[w]["valid"])
if len(V) < 2:
    verdict = "UNDECIDED"
elif any(raters[w]["calls"][s] != "rows" for w in V for s in ("L70d_level", "C70d_level")):
    verdict = "FULL-HOP-FAILS"
elif any(raters[w]["calls"][s] != "rows" for w in V for s in ("L40d_level", "H50n_level")):
    verdict = "FULL-HOP-HOLDS"
else:
    verdict = "UNDECIDED (lenient page)"

c = {w: raters[w]["calls"] for w in raters}
check("verdict", verdict, EXPECTED["verdict"])
check("valid_raters", V, EXPECTED["valid_raters"])
check("C70d_not_rows", {w: c[w]["C70d_level"] != "rows" for w in c}, EXPECTED["C70d_not_rows"])
check("L70d_not_rows", {w: c[w]["L70d_level"] != "rows" for w in c}, EXPECTED["L70d_not_rows"])
check("L40d_not_rows", {w: c[w]["L40d_level"] != "rows" for w in c}, EXPECTED["L40d_not_rows"])
check("H50n_rows", {w: c[w]["H50n_level"] == "rows" for w in c}, EXPECTED["H50n_rows"])
check("L100_rows", {w: c[w]["L100_level"] == "rows" for w in c}, EXPECTED["L100_rows"])
check("blanks_rejected_of_3",
      {w: sum(c[w][b] != "rows" for b in ("L70d_blank", "C70d_blank", "blank09")) for w in c},
      EXPECTED["blanks_rejected_of_3"])
check("calib_rows", {w: c[w]["calib"] == "rows" for w in c}, EXPECTED["calib_rows"])
check("sha256", {w: raters[w]["sha256"] for w in raters}, EXPECTED["sha256"])

# Stage 0b dose check (saved output; bar = min(blank + 0.05, 0.62), prereg L76)
s0b = json.loads((DATA / "fh_s0b_f140_result.json").read_text(encoding="utf-8"))
for s in ("L70d", "C70d"):
    bar = round(min(s0b[s]["auc_blank_same_offset"] + 0.05, 0.62), 4)
    check(f"{s}_bar (recomputed from saved blank AUC)", bar, round(s0b[s]["bar_hop"], 4))
check("L70d_hop_auc", s0b["L70d"]["auc_hop"], EXPECTED["L70d_hop_auc"])
check("L70d_bar", s0b["L70d"]["bar_hop"], EXPECTED["L70d_bar"])
check("L70d_margin", round(s0b["L70d"]["bar_hop"] - s0b["L70d"]["auc_hop"], 4), EXPECTED["L70d_margin"])
check("C70d_hop_auc", round(s0b["C70d"]["auc_hop"], 3), EXPECTED["C70d_hop_auc"])
check("C70d_bar", round(s0b["C70d"]["bar_hop"], 3), EXPECTED["C70d_bar"])

# Stage 0b gates (prereg L74-81). NOTE: L70d passes the hop gate by 0.0001 at the 4-decimal rounding the job saved
# (0.5755 <= 0.5756); the unrounded AUCs are not shipped, so the recomputed gate below and the job's own hop_ok flag
# (computed by the job on unrounded numbers) are both asserted, and the README margin "by 0.0001" relies on the flag.
check("s0b_hop_gate", {s: s0b[s]["auc_hop"] <= s0b[s]["bar_hop"] for s in ("L70d", "C70d")}, EXPECTED["s0b_hop_gate"])
check("s0b_unmoved_gate", {s: s0b[s]["auc_unmoved"] >= s0b[s]["auc_unmoved_rated_parent"] - 0.01 for s in ("L70d", "C70d")},
      EXPECTED["s0b_unmoved_gate"])
check("s0b_job_flags", {s: [s0b[s]["hop_ok"], s0b[s]["unmoved_ok"]] for s in ("L70d", "C70d")}, EXPECTED["s0b_job_flags"])

surf = json.loads((DATA / "f140_surf.json").read_text(encoding="utf-8"))
check("s0d_dark_hops_ok", {s: surf["surfaces"][s]["off_sheet_moved"] <= surf["surfaces"][s]["off_sheet_same_vertices_on_P"] + 0.10
                           for s in ("L70d", "C70d")}, EXPECTED["s0d_dark_hops_ok"])
check("floor_um", surf["floor_um"], EXPECTED["floor_um"])
check("far_um", int(surf["far_um"]), EXPECTED["far_um"])
# MEASURED hop sizes, asserted (WORDING_FLAGS flag 2: the README quotes the law's 140-250 um, the measured 10th
# percentile of L70d's moved vertices is below the 140 um floor because of smoothing taper at hop borders).
for s_ in ("L70d", "C70d"):
    p = surf["surfaces"][s_]["moved_um_pct"]
    check(f"measured_{s_}_p10_um", p["p10"], EXPECTED[f"measured_{s_}_p10_um"])
    check(f"measured_{s_}_p50_um", p["p50"], EXPECTED[f"measured_{s_}_p50_um"])
    check(f"measured_{s_}_share_moved_le130", surf["surfaces"][s_]["share_moved_le130"],
          EXPECTED[f"measured_{s_}_share_moved_le130"])
    print(f"INFO     {s_} moved um p90 = {p['p90']}")

print(f"\nFULL-HOP-W: {'MATCH' if not fails else 'MISMATCH ' + ', '.join(fails)}  (source: {ITEM})")
sys.exit(1 if fails else 0)
