"""FRESH-WRAP re-score (outline row 3, second-wrap part).

Rule (standalone/preregs/depth_s022814.md: rater() and combine() below are ported line by line from the
scorer frozen in the prereg, [private path] @60b819bd L357-410:
  - valid = every picture answered, calibration 'rows', <= 1 of the surface blanks 'rows', >= 1 guard picture; else VOID;
  - ctrl blank 'rows' -> VOID (control); WINDOW-YES = ctrl rows, WINDOW-NO = ctrl not rows;
  - an arm (in24 / out24) whose blank reads 'rows' is uncountable -> depth INCOMPLETE; else WIDE-HOLDS / NARROW-OUT /
    NARROW-IN / NARROW-BOTH; lenient (> half of the guards 'rows') turns WIDE-HOLDS into ALL-ROWS;
  - 10 mm: UNCOUNTABLE if the 10 mm blank is 'rows', else 1CM-READS-PRIMED (both windows rows) / 20MM-NEEDED;
  - item verdict: CONFIRMED = WIDE-HOLDS from two valid raters, neither lenient; NARROWED / WINDOW-NO / ONE RATER / SPLIT /
    VOID as in the prereg;
  - edge arms in48 / out48: descriptive calls only (released in the item's Run section, L230).
Arms are mapped BY NAME (key 'arms': out = minus layers, because raw +o is inward on the organizers' SVs; prereg L47-53).
The ported rater() output is asserted equal, field by field, to the scorer's own saved result (freshwrap_result.json).
RE-READ, NOT RECOMPUTED: the map correlations (r vs ctrl) need the saved ink maps (~GB of .npy, not shipped). They are
copied from the Judge's saved output judge_rescore.json @60b819bd (kind 'derived'); this script only maps them to the
arms by name and rounds them as the README does. A changed r value in that file is caught; a wrong map is not.
Rating files: sha256 pinned at package build (2026-10-18); no earlier record of their hashes exists in the item.
Inputs: ../data/freshwrap/. Run: python reproduce/freshwrap.py
"""
import hashlib, json, sys
from pathlib import Path

D = Path(__file__).resolve().parent.parent / "data" / "freshwrap"
V = "[private path] @60b819bd"

EXPECTED = {
    # V L245 + L253: PASS = CONFIRMED (WIDE-HOLDS, two raters); both valid, neither lenient, guards 0/1 and 1/3, blanks 0/4
    "valid_seb": True, "valid_chris": True, "lenient_seb": False, "lenient_chris": False,
    "guards_rows_seb": "0/1", "guards_rows_chris": "1/3", "blanks_rows_seb": "0/4", "blanks_rows_chris": "0/4",
    "window_seb": "WINDOW-YES", "window_chris": "WINDOW-YES",
    "depth_seb": "WIDE-HOLDS", "depth_chris": "WIDE-HOLDS",
    "combined": "CONFIRMED (WIDE-HOLDS, two raters)",
    "cm2_seb": "20MM-NEEDED", "cm2_chris": "20MM-NEEDED",          # V L253
    # Run L230 + V L260-263; outline row 3: Chris +48 outward 'strokes', -48 (inward) rows; Sebastien both rows
    "edge_seb_out48": "rows", "edge_seb_in48": "rows",
    "edge_chris_out48": "strokes", "edge_chris_in48": "rows",
    "depth_arm_calls_not_rows_of_8": "1/8",                       # V L263 "the only fresh depth picture ... not rows"
    "surface_rows_seb": "6/7",                                    # V L260 "rows on 6 of 7 fresh surface pictures"
    "surface_rows_chris": "5/7",                                  # judge_rescore.json @60b819bd
    "arm_layers": {"ctrl": 0, "in24": 10, "out24": -10, "in48": 20, "out48": -20},   # prereg L52-53
    # derived (Judge output judge_rescore.json @60b819bd; V L256): r vs ctrl map
    "r_out24": 0.868, "r_in24": 0.851, "r_out48": 0.689, "r_in48": 0.691,
    "r_24_range_2dp": "0.85-0.87", "r_48_2dp": "0.69",            # outline row 3 "r 0.85-0.87 (+-48 um: 0.69)"
    # prereg L101: every picture answered (Sebastien 14, Chris 16 pictures); no uncountable arm, no VOID branch fired
    "missing_seb": [], "missing_chris": [], "n_pictures_seb": 14, "n_pictures_chris": 16,
    "ported_rater_equals_saved_seb": True, "ported_rater_equals_saved_chris": True,
    "sha12_seb": "4f1849080217", "sha12_chris": "088b9542f4c8",   # pinned 2026-10-18 at package build
    "combined_equals_saved": True,
}

ROWS = "rows"
J = lambda n: json.loads((D / n).read_text(encoding="utf-8"))


def rater(c):
    """fw.py @60b819bd L357-386, unchanged logic. c = {file name: answer or None} for that rater's page."""
    r = dict(missing=sorted(f for f, a in c.items() if a is None))
    blanks = [f for f in c if f.endswith("_blank")]; r["blank_rows"] = sum(c[f] == ROWS for f in blanks); r["n_blanks"] = len(blanks)
    r["calib"], r["blank09"] = c.get("calib"), c.get("blank09")
    g = [f for f in c if f.startswith("guard_")]; r["guard_rows"] = sum(c[f] == ROWS for f in g); r["n_guard"] = len(g)
    r["lenient"] = bool(g) and r["guard_rows"] * 2 > len(g)
    r["valid"] = not r["missing"] and c.get("calib") == ROWS and r["blank_rows"] <= 1 and bool(g)
    cnt = lambda arm: f"{arm}_blank" not in c or c[f"{arm}_blank"] != ROWS
    if not r["valid"]:
        r["window"] = "VOID (invalid rater)"; return r
    if not cnt("ctrl"):
        r["window"] = "VOID (control blank read as rows)"; return r
    r["edge"] = {k: c[f"{k}_level"] for k in ("in48", "out48") if f"{k}_level" in c}
    if c["ctrl_level"] != ROWS:
        r["window"] = "WINDOW-NO"; return r
    r["window"] = "WINDOW-YES"
    if not (cnt("in24") and cnt("out24")):
        r["depth"] = "INCOMPLETE"
    else:
        i, o = c["in24_level"] == ROWS, c["out24_level"] == ROWS
        r["depth"] = "WIDE-HOLDS" if i and o else "NARROW-OUT" if i else "NARROW-IN" if o else "NARROW-BOTH"
        if r["depth"] == "WIDE-HOLDS" and r["lenient"]:
            r["depth"] = "ALL-ROWS"
    if "H9_level" in c:
        r["reader"] = "UNCOUNTABLE" if not cnt("H9") else ("H9-ROWS" if c["H9_level"] == ROWS else "H9-NO-ROWS")
    else:
        r["reader"] = "H9 DROPPED"
    if "w10_top" in c:
        r["cm2"] = "UNCOUNTABLE" if not cnt("w10") else ("1CM-READS-PRIMED" if c["w10_top"] == ROWS and c["w10_bot"] == ROWS else "20MM-NEEDED")
    else:
        r["cm2"] = "10 MM DROPPED"
    return r


def combine(rs):
    """fw.py @60b819bd L389-410 (final scoring, both rating files present)."""
    v = {k: x for k, x in rs.items() if not x["window"].startswith("VOID")}
    if not v:
        return dict(verdict="VOID (no valid rater)")
    out = dict(n_valid=len(v), label="two raters" if len(v) == 2 else "one rater")
    w = {x["window"] for x in v.values()}
    if w == {"WINDOW-NO"}:
        out["verdict"] = "WINDOW-NO" + ("" if len(v) == 2 else " (one rater)"); return out
    if w != {"WINDOW-YES"}:
        out["verdict"] = "SPLIT (window)"; return out
    d = {x["depth"] for x in v.values()}
    if len(v) == 2 and d == {"WIDE-HOLDS"}:
        out["verdict"] = "CONFIRMED (WIDE-HOLDS, two raters)"
    elif len(v) == 2 and len(d) == 1 and d <= {"NARROW-OUT", "NARROW-IN", "NARROW-BOTH"}:
        out["verdict"] = "NARROWED: " + d.pop() + " (two raters, on a weaker surface)"
    elif len(v) == 1:
        out["verdict"] = "ONE RATER: " + next(iter(d)) + " (reported, no rewording)"
    else:
        out["verdict"] = "SPLIT / NOT DECIDED: " + " vs ".join(sorted(x["depth"] for x in v.values())) + " (reported, no rewording)"
    for k in ("reader", "cm2"):
        s_ = {x[k] for x in v.values()}; out[k] = (s_.pop() if len(s_) == 1 else "SPLIT") + (" (" + out["label"] + ")")
    return out


key = J("freshwrap_key.json")
fr = J("freshwrap_result.json")          # the scorer's own saved result (fw.py output)
got = {"arm_layers": key["arms"]}
depth_calls = []
rs = {}
for r in ("seb", "chris"):
    fname = f"freshwrap_{r}_ratings.json"
    got[f"sha12_{r}"] = hashlib.sha256((D / fname).read_bytes()).hexdigest()[:12]
    ans = J(fname)["answers"]
    c = {fn: ans.get(t) for t, fn in key["pages"][r].items()}
    got[f"n_pictures_{r}"] = len(c)
    x = rater(c)
    rs[r] = x
    got[f"ported_rater_equals_saved_{r}"] = x == fr["raters"][r]
    got[f"missing_{r}"] = x["missing"]
    rows = lambda f: c[f] == ROWS
    surf = [f for f in c if f.endswith("_level") or f in ("w10_top", "w10_bot")]
    got.update({f"valid_{r}": bool(x["valid"]), f"lenient_{r}": bool(x["lenient"]), f"window_{r}": x["window"],
                f"depth_{r}": x.get("depth"), f"cm2_{r}": x.get("cm2"),
                f"guards_rows_{r}": f"{x['guard_rows']}/{x['n_guard']}",
                f"blanks_rows_{r}": f"{x['blank_rows']}/{x['n_blanks']}",
                f"surface_rows_{r}": f"{sum(map(rows, surf))}/{len(surf)}",
                f"edge_{r}_out48": c["out48_level"], f"edge_{r}_in48": c["in48_level"]})
    depth_calls += [c[f"{y}_level"] for y in ("in24", "out24", "in48", "out48")]
comb = combine(rs)
got["combined"] = comb["verdict"]
got["combined_equals_saved"] = comb == fr["combined"]
got["depth_arm_calls_not_rows_of_8"] = f"{sum(x != 'rows' for x in depth_calls)}/{len(depth_calls)}"

# RE-READ (not recomputed): r vs ctrl from the Judge's saved output; fwd o = layers (out = negative)
jr = J("judge_rescore_60b819bd.json")["r_vs_ctrl"]
L = key["arms"]
got["r_out24"], got["r_in24"] = jr[f"fwd{L['out24']:+d}"], jr[f"fwd{L['in24']:+d}"]
got["r_out48"], got["r_in48"] = jr[f"fwd{L['out48']:+d}"], jr[f"fwd{L['in48']:+d}"]
lo, hi = sorted((got["r_out24"], got["r_in24"]))
got["r_24_range_2dp"] = f"{round(lo, 2):.2f}-{round(hi, 2):.2f}"
got["r_48_2dp"] = f"{round(got['r_out48'], 2):.2f}" if round(got["r_out48"], 2) == round(got["r_in48"], 2) else "differ"

bad = 0
print(f"FRESH-WRAP re-score (expected values from {V}); r values RE-READ from the Judge's saved output (not recomputed)")
for kk, e in EXPECTED.items():
    g = got.get(kk)
    ok = g == e
    bad += not ok
    print(f"  {'MATCH   ' if ok else 'MISMATCH'} {kk:30s} got={g!r} expected={e!r}")
print("RESULT:", "ALL MATCH" if not bad else f"{bad} MISMATCH(ES)")
sys.exit(1 if bad else 0)
