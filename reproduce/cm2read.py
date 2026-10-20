"""CM2-READ re-score (outline row 3) + the 'rows on 19 of 20 surface pictures' count (outline "Known-window ceiling").

Rule (standalone/preregs/depth_w.md + amendment 1), as the loop Judge re-implemented it
([private path] @60b819bd):
  - valid = 22 answers, calibration 'rows', <= 1 of the 8 surface blanks 'rows';
  - an arm counts if its level picture is 'rows' and its own blank is not 'rows';
  - outward = 24 if p10 (+24 um) counts, else 12 if p5 (+12 um) counts, else 0; inward the same with m10 / m5;
  - a level whose own blank reads 'rows' is UNCOUNTABLE (prereg L68-69);
  - outcome (prereg L70-80): VOID unless valid and the P control counts; WIDE-OUT if +12 or +24 counts; else INCOMPLETE if
    +12 or +24 is uncountable; else ASYMMETRIC (-24 rows) / ASYMMETRIC-SHORT (-12 rows) / NARROW, with INCOMPLETE when the
    inward tile needed for that call is uncountable;
  - s214732 ROWS / NOT ROWS / UNCOUNTABLE (blank reads rows; prereg L83-84);
  - 10 mm unit (prereg L85-87): UNCOUNTABLE if either 10 mm blank reads rows; 1 cm2 USABLE if k_P >= 2 and k_S = 0;
    20 mm ONLY if k_P = 0 or k_S >= k_P; else DESCRIPTIVE. Two raters: a named unit only if both agree, else SPLIT.
Ceiling count (Judge finding 5, judge_discrimination.py): surface pictures = HUMAN-TOL's 8 level pictures + CM2-READ's
6 level pictures at 20 mm + 6 at 10 mm (w10_P / w10_S x top/mid/bot) = 20.
Counts only. Inputs: ../data/cm2read/. Run: python reproduce/cm2read.py
"""
import json, sys
from pathlib import Path

D = Path(__file__).resolve().parent.parent / "data" / "cm2read"
V = "[private path] @60b819bd"

EXPECTED = {
    # V L288 + L300-302: WIDE-OUT, both valid (0/8 blanks rows), outward 24, inward 24, s214732 ROWS
    "valid_seb": True, "valid_chris": True, "blank_rows_seb": 0, "blank_rows_chris": 0,
    "outcome_seb": "WIDE-OUT", "outcome_chris": "WIDE-OUT",
    "outward_um_seb": 24, "outward_um_chris": 24, "inward_um_seb": 24, "inward_um_chris": 24,
    "s214732_seb": "ROWS", "s214732_chris": "ROWS",
    # V L302-303: agreement 14/14 at 20 mm, 4/8 at 10 mm; 10 mm k_P/k_S = 3/3 (Seb), 2/0 (Chris)
    "agree_20mm": "14/14", "agree_10mm": "4/8",
    "k10_seb": "3/3", "k10_chris": "2/0",
    # V L271-273 + L302: unit10 Sebastien 20 mm ONLY, Chris 1 cm2 USABLE -> SPLIT (descriptive)
    "unit10_seb": "20 mm ONLY", "unit10_chris": "1 cm2 USABLE", "unit10_combined": "SPLIT",
    # no tile is uncountable for either rater (0/8 surface blanks rows), so no INCOMPLETE branch fires
    "uncountable_seb": [], "uncountable_chris": [],
    # V L321: first surface picture shown is the +24 um outward tile (c02 = p10)
    "first_level_shown": "p10",
    # V L313: HUMAN-TOL non-blank pictures called not-rows: Sebastien 1/8, Chris 3/8
    "humantol_surface_not_rows_seb": "1/8", "humantol_surface_not_rows_chris": "3/8",
    # V L314-315 (Judge finding 5); outline ceiling section "Sebastien called rows on 19 of 20 surface pictures"
    "surface_rows_seb_of_20": "19/20",
    "surface_rows_chris_of_20": "13/20",      # V L314-315 "Chris (rows on 13 of 20 incl. 2/6 at 10 mm)"
    "chris_10mm_rows": "2/6",
}

J = lambda n: json.loads((D / n).read_text(encoding="utf-8"))
key = J("cm2read_key.json")["images"]
got = {}
raters = {}
surf_rows = {}
for name in ("seb", "chris"):
    a = J(f"cm2read_{name}_ratings.json")["answers"]
    raters[name] = a
    lv, bl = {}, {}
    calib = None
    for cid, k in key.items():
        tag = k["arm"] + ("_" + k["pos"] if k["size"] == "10mm" and k["kind"] == "level" else "")
        if k["kind"] == "level":
            lv[tag] = a[cid]
        elif k["kind"] == "blank":
            bl[k["arm"]] = a[cid]
        elif k["kind"] == "calib":
            calib = a[cid]
    nb = sum(v == "rows" for v in bl.values())
    valid = len(a) == 22 and calib == "rows" and nb <= 1

    def st(arm):  # "rows" / "not rows" / "uncountable" for one level picture (its own blank decides countability)
        blank = bl[arm.split("_")[0] + "_" + arm.split("_")[1]] if arm.startswith("w10_") else bl[arm]
        if blank == "rows":
            return "uncountable"
        return "rows" if lv[arm] == "rows" else "not rows"
    cnt = lambda arm: st(arm) == "rows"
    o = 24 if cnt("p10") else (12 if cnt("p5") else 0)
    i = 24 if cnt("m10") else (12 if cnt("m5") else 0)
    ctrl_ok = cnt("ctrl")
    if not (valid and ctrl_ok):
        oc = "VOID"
    elif o > 0:
        oc = "WIDE-OUT"
    elif "uncountable" in (st("p5"), st("p10")):
        oc = "INCOMPLETE"
    elif st("m10") == "uncountable":
        oc = "INCOMPLETE"                       # the -24 tile decides ASYMMETRIC
    elif i == 24:
        oc = "ASYMMETRIC"
    elif st("m5") == "uncountable":
        oc = "INCOMPLETE"                       # the -12 tile decides ASYMMETRIC-SHORT vs NARROW
    else:
        oc = "ASYMMETRIC-SHORT" if i == 12 else "NARROW"
    got[f"uncountable_{name}"] = sorted(t for t in lv if st(t) == "uncountable")
    kP = sum(lv[f"w10_P_{p}"] == "rows" for p in ("top", "mid", "bot"))
    kS = sum(lv[f"w10_S_{p}"] == "rows" for p in ("top", "mid", "bot"))
    if "rows" in (bl["w10_P"], bl["w10_S"]):
        unit = "UNCOUNTABLE"
    elif kP >= 2 and kS == 0:
        unit = "1 cm2 USABLE"
    elif kP == 0 or kS >= kP:
        unit = "20 mm ONLY"
    else:
        unit = "DESCRIPTIVE"
    got[f"unit10_{name}"] = unit
    got.update({f"valid_{name}": valid, f"blank_rows_{name}": nb, f"outcome_{name}": oc, f"outward_um_{name}": o,
                f"inward_um_{name}": i, f"s214732_{name}": {"rows": "ROWS", "not rows": "NOT ROWS"}.get(st("s214732"), "UNCOUNTABLE"),
                f"k10_{name}": f"{kP}/{kS}"})
    n20 = sum(v == "rows" for t, v in lv.items() if not t.startswith("w10"))
    n10 = sum(v == "rows" for t, v in lv.items() if t.startswith("w10"))
    assert sum(not t.startswith("w10") for t in lv) == 6 and sum(t.startswith("w10") for t in lv) == 6
    surf_rows[name] = (n20, n10)
    if name == "chris":
        got["chris_10mm_rows"] = f"{n10}/6"

u = (got["unit10_seb"], got["unit10_chris"])
got["unit10_combined"] = u[0] if u[0] == u[1] and u[0] in ("1 cm2 USABLE", "20 mm ONLY") else "SPLIT"

ids20 = [c for c, k in key.items() if k["size"] == "20mm"]
ids10 = [c for c, k in key.items() if k["size"] == "10mm"]
got["agree_20mm"] = f"{sum(raters['seb'][c] == raters['chris'][c] for c in ids20)}/{len(ids20)}"
got["agree_10mm"] = f"{sum(raters['seb'][c] == raters['chris'][c] for c in ids10)}/{len(ids10)}"
got["first_level_shown"] = next(k["arm"] for c, k in sorted(key.items(), key=lambda x: int(x[0][1:])) if k["kind"] == "level")

n_cm2_levels = sum(k["kind"] == "level" for k in key.values())
assert n_cm2_levels == 12, n_cm2_levels

# HUMAN-TOL surface (= non-blank, non-calibration) pictures, as judge_discrimination.py groups them
hk = J("humantol_key.json")
for name, f in (("seb", "humantol_seb_ratings.json"), ("chris", "humantol_chris_ratings.json")):
    a = J(f)["answers"]
    surf = [p for p, k in hk.items() if k["kind"] not in ("blank", "blank09", "calib")]
    nr = sum(a[p] != "rows" for p in surf)
    got[f"humantol_surface_not_rows_{name}"] = f"{nr}/{len(surf)}"
    tot = len(surf) + n_cm2_levels      # CM2-READ's own level pictures (6 at 20 mm + 6 at 10 mm), counted from its key
    got[f"surface_rows_{name}_of_20"] = f"{len(surf) - nr + sum(surf_rows[name])}/{tot}"

bad = 0
print(f"CM2-READ re-score + ceiling count (expected values from {V})")
for kk, e in EXPECTED.items():
    g = got.get(kk)
    ok = g == e
    bad += not ok
    print(f"  {'MATCH   ' if ok else 'MISMATCH'} {kk:32s} got={g!r} expected={e!r}")
print("RESULT:", "ALL MATCH" if not bad else f"{bad} MISMATCH(ES)")
sys.exit(1 if bad else 0)
