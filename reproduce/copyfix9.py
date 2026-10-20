"""Failures: COPY-FIX-9 (standalone/preregs/handfix.md) + its second-key label KEY2-STEP2 (standalone/preregs/handfix_key2.md).

Re-scores, from the saved key, Chris's blind 2.4 um marks (two marking sessions) and his two 20 mm read pages:
  - step 1 (R, the uncorrected copy) and step 2 (F, the hand-fixed square) verdicts, ported verbatim from
    [private path] at 60b819bd (constants lines 31-33, mark_counts 593-607,
    mark_class 616-623, read_checks 626-633, verdict1 636-648, verdict2 651-670, score 681-690);
  - the margin to INCONCLUSIVE and the radius sensitivity (Judge check checks/20261005-16-.../judge_margin.py);
  - F vs its own start surface OVL_inset (checks/20261005-16-.../f_vs_ovl_sites.py; OVL crossings from OVL-MARKS'
    ovlmarks_result.json per_site);
  - the second-key counts and classes (checks/20261008-19-key2-step2-is-the-copy-f/judge_rescore.py: key-2 mark mapped
    to the key-1 site by old_id, t2 = t + delta_um - delta_old_um) and the two-key class (prereg key2step2 line 38:
    "same class under both keys, else KEY-LIMITED");
  - the session minutes from the saved timestamps (session_times.json);
  - asserted gates: cf.py's saved result (copyfix_result.json) equals this re-score; KEY2-STEP2's consistency gate (prereg
    key2step2 L42-43: key-1 counts recomputed by the two-key scorer == copyfix_result.json step1/step2 marks, else both
    two-key classes become "INCONCLUSIVE (scorer mismatch)"; the FIX-FIELD half of that gate is not shipped here);
    TOO FEW under a key -> INCONCLUSIVE (key2step2 L69); the guide-line wording flag (copyfix9 prereg L86-87: marks within
    75 um of the extended guide line at least as often as on C); the MARK-2R link (copyfix9 prereg L88-92: the marks decide
    as written only if MARK-2R is KEY OK, re-scored here from ../data/mark2r/ with mark2r.py's human-floor rule).

Run: python reproduce/copyfix9.py   (stdlib only)
"""
import json, math, sys
from datetime import datetime
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "copyfix9"
def J(f):
    with open(DATA / f, encoding="utf-8") as fh: return json.load(fh)

# cf.py constants (lines 31-33)
ID_R, DISC_UM, VALID_MIN = 75.0, 150.0, 18

IC = "[private path]"   # at 60b819bd
IK = "[private path]"   # at 60b819bd
EXPECTED = {
    "step1_outcome": "STEP 2: COPY OFF (the read cannot see the inset: F is decided by the marks alone)",  # IC:388
    "R_key1": "14/24",                 # IK:218 "R ... KILL-marks at both (14/24, 14/23)"
    "step2_outcome": "KILL (first timed session of a new user with <= 90 min)",                            # IC:376, 388
    "F_key1": "17/24",                 # IC:388 "valid 24, C on 23, F on 17"; outline "17/24"
    "C_key1": "23/24",                 # IC:388; outline "control 23/24"
    "F_key1_class": "KILL-marks",      # IC:388
    "F_read": "rows",                  # IC:388 "F read rows"
    "guard_read2": "strokes",          # IC:388 "guard not rows"
    "sites_from_inconclusive": 2,      # IC:389 "KILL two sites from INCONCLUSIVE" (19 = MIDDLE, IC:391); outline "two sites from INCONCLUSIVE"
    "F_on_by_radius_50_75_100": (13, 17, 20),   # IC:392
    "C_on_by_radius_50_75_100": (20, 23, 24),   # IC:392
    "straight_guide_within75": "22/24",         # IC:397; outline "the straight guide alone lands within 75 um at 22/24"
    "OVL_start_key1": "16/24",         # IC:404 "moved F from 16/24 (OVL start)"; outline "its own start scored 16/24"
    "F_vs_start_gained_lost": (4, 3),  # IC:404 "Paired: 4 sites gained, 3 lost"
    "F_key2": "16/23",                 # IK:213 "key 2 16/23 vs C 19 -> MIDDLE"; outline "16/23 vs 19/23"
    "C_key2": "19/23",                 # IK:213
    "F_key2_class": "MIDDLE",          # IK:213 (outline: "undecided")
    "R_key2": "14/23",                 # IK:218
    "R_two_key_class": "KILL-marks",   # IK:218 "two-key KILL"
    "F_two_key_class": "KEY-LIMITED",  # IK:206 "FAIL (prereg outcome KEY-LIMITED)"
    "F_onoff_same_both_keys": "16/23",  # IK:215
    "minutes_sheet_rule": 89.2,        # IC:366 / IC:408 "89.2 min by the sheet rule"
    "minutes_own_reading": "80-84",    # IC:366 / IC:408 "80-84 by his own reading"
    "cf_saved_result_identical": True,       # copyfix_result.json step1/step2 outcomes + marks == this re-score
    "key2_consistency_gate": True,           # key2step2 prereg L42-43
    "guide_line_wording_flag": False,        # prereg L86-87: straight guide 22/24 < on C 23/24, so no "following the guide line" label
    "mark2r_human_floor": "KEY OK",          # prereg L88-89: MARK-2R KEY OK -> the marks decide as written (mark2r item L175)
}


def mark_counts(sites, marks, arm):
    on_c = on_x = valid = cant = multi_x = hole_x = 0; disc = dict(n=0, side_arm=0, side_C=0, neither=0); ext = dict(n=0, within75=0)
    for s in sites:
        mk = marks.get(s["id"], {})
        if mk.get("cant") or mk.get("t_um") is None:
            cant += 1; continue
        valid += 1; t = float(mk["t_um"]); cC, cX = s["cross"].get("N2") or [], s["cross"].get(arm) or []
        okC = len(cC) == 1 and abs(cC[0] - t) <= ID_R; okX = len(cX) == 1 and abs(cX[0] - t) <= ID_R
        on_c += okC; on_x += okX; multi_x += len(cX) >= 2; hole_x += len(cX) == 0
        if len(cC) == 1 and len(cX) == 1 and abs(cC[0] - cX[0]) > DISC_UM:
            disc["n"] += 1; disc["side_arm" if okX else ("side_C" if okC else "neither")] += 1
        if s.get("ext_t_um") is not None:
            ext["n"] += 1; ext["within75"] += abs(s["ext_t_um"] - t) <= ID_R
    return dict(valid=valid, cant=cant, on_C=on_c, on_X=on_x, multi_X=multi_x, hole_X=hole_x, discriminating=disc,
                marks_within75_of_straight_line=ext)


def mark_class(mc):
    if mc["valid"] < VALID_MIN:
        return "TOO FEW"
    if mc["on_X"] <= mc["on_C"] - 5:
        return "KILL-marks"
    if mc["on_X"] >= mc["on_C"] - 2 and mc["on_X"] >= 0.75 * mc["valid"]:
        return "PASS-marks"
    return "MIDDLE"


def read_checks(c, arm, repeat=True):
    if any(v is None for v in c.values()) or c.get("calib") != "rows":
        return "VOID (rater: calibration missed or pictures unanswered)", None, None
    if c.get("C_level") != "rows" or c.get("C_blank") == "rows" or (repeat and c.get("C_repeat") != "rows"):
        return "UNINFORMATIVE (control not read as rows, its repeat disagreed, or its blank read rows)", None, None
    rd = "not interpretable" if c.get(f"{arm}_blank") == "rows" else ("rows" if c.get(f"{arm}_level") == "rows" else "not rows")
    return None, rd, c.get("guard", "absent")


def verdict1(c, mc):
    st, rd, g = read_checks(c, "R")
    if st:
        return dict(outcome=st)
    cls = mark_class(mc)
    if cls == "TOO FEW":
        return dict(outcome=f"UNINFORMATIVE (marks: {mc['valid']} valid sites < {VALID_MIN})", R_read=rd)
    weak = g in ("rows", "absent")
    if rd == "rows" and cls == "PASS-marks":
        return dict(outcome="COPY-ONLY" + (" (weak: guard picture read rows or absent)" if weak else ""), R_read=rd, R_marks=cls, split="close")
    sub = {"KILL-marks": "COPY OFF" + (" (the read cannot see the inset: F is decided by the marks alone)" if rd == "rows" else ""),
           "MIDDLE": "COPY UNCLEAR", "PASS-marks": "COPY ON, NOT READ"}[cls]
    return dict(outcome="STEP 2: " + sub, R_read=rd, R_marks=cls, split="step2", marks_only_for_F=bool(cls == "KILL-marks" and rd == "rows"))


def verdict2(c, mc, marks_only):
    st, rd, g = read_checks(c, "F", repeat=False)
    if st:
        return dict(outcome=st)
    cls = mark_class(mc)
    if cls == "TOO FEW":
        return dict(outcome="UNINFORMATIVE (marks)", F_read=rd)
    if marks_only:
        o = {"PASS-marks": "PASS (marks only)", "KILL-marks": "KILL", "MIDDLE": "INCONCLUSIVE"}[cls]
    elif rd == "not interpretable":
        o = "INCONCLUSIVE (F's wrong-order blank read rows: F's read is untestable)"
    elif cls == "KILL-marks" or rd != "rows":
        o = "KILL"
    elif cls == "PASS-marks":
        o = "PASS"
    else:
        o = "PASS-weak"
    if o == "KILL":
        o += " (first timed session of a new user with <= 90 min)"
    return dict(outcome=o, F_read=rd, F_marks=cls, guard=g)


def calls(ratings_file, images):
    a = J(ratings_file)["answers"]
    return {v["role"]: (str(a[k]).strip().lower() if k in a else None) for k, v in images.items()}


def on(cross, t):
    return len(cross) == 1 and abs(cross[0] - t) <= ID_R


def mark2r_floor():
    """MARK-2R human floor (prereg standalone/preregs/audit_guided.md L53-55, as reproduce/mark2r.py): random sites marked by both,
    n >= 15 else UNDECIDED; KEY OK if within 75 um (distances rounded to 0.1 um) at >= ceil(0.8 n)."""
    M2 = DATA.parent / "mark2r"
    with open(M2 / "mark2r_key.json", encoding="utf-8") as fh: S = json.load(fh)["sites"]
    m = {}
    for r in ("seb", "chris"):
        with open(M2 / f"mark2r_{r}_ratings.json", encoding="utf-8") as fh: it = json.load(fh)["items"]
        m[r] = {s["id"]: (None if (not it.get(s["id"]) or it[s["id"]].get("cant") or "t_um" not in it[s["id"]]) else float(it[s["id"]]["t_um"]))
                for s in S}
    hh = [round(abs(m["seb"][s["id"]] - m["chris"][s["id"]]), 1) for s in S if s["stratum"] == "random"
          and None not in (m["seb"][s["id"]], m["chris"][s["id"]])]
    if len(hh) < 15: return "UNDECIDED"
    return "KEY OK" if sum(d <= ID_R for d in hh) >= math.ceil(0.8 * len(hh) - 1e-9) else "NOT A SINGLE-RATER KEY"


def main():
    kj = J("copyfix_key.json"); sites = kj["marks"]["sites"]
    m1 = J("copyfix_marks_chris_ratings.json")["items"]
    got, show = {}, {}

    # --- COPY-FIX-9 step 1 / step 2 (cf.py score) ---
    mR = mark_counts(sites, m1, "R"); v1 = verdict1(calls("copyfix_read_chris_ratings.json", kj["read1"]["images"]), mR)
    mF = mark_counts(sites, m1, "F"); v2 = verdict2(calls("copyfix_read2_chris_ratings.json", kj["read2"]["images"]), mF, v1.get("marks_only_for_F", False))
    show["step1"] = dict(v1, marks=mR); show["step2"] = dict(v2, marks=mF)
    got["step1_outcome"] = v1["outcome"]; got["R_key1"] = f"{mR['on_X']}/{mR['valid']}"
    got["step2_outcome"] = v2["outcome"]; got["F_key1"] = f"{mF['on_X']}/{mF['valid']}"; got["C_key1"] = f"{mF['on_C']}/{mF['valid']}"
    got["F_key1_class"] = mark_class(mF); got["F_read"] = v2.get("F_read"); got["guard_read2"] = v2.get("guard")
    got["sites_from_inconclusive"] = (mF["on_C"] - 5 + 1) - mF["on_X"]     # first MIDDLE count minus F's count
    e = mF["marks_within75_of_straight_line"]; got["straight_guide_within75"] = f"{e['within75']}/{e['n']}"

    # --- radius sensitivity (judge_margin.py) ---
    def on_at(arm, r):
        n = 0
        for s in sites:
            m = m1.get(s["id"], {})
            if m.get("cant") or m.get("t_um") is None: continue
            c = s["cross"].get(arm) or []
            n += len(c) == 1 and abs(c[0] - m["t_um"]) <= r
        return n
    got["F_on_by_radius_50_75_100"] = tuple(on_at("F", r) for r in (50, 75, 100))
    got["C_on_by_radius_50_75_100"] = tuple(on_at("N2", r) for r in (50, 75, 100))

    # --- F vs its own start OVL_inset (f_vs_ovl_sites.py) ---
    ov = {p["id"]: p for p in J("ovlmarks_result.json")["per_site"]}
    o_on = gain = lost = nv = 0
    for s in sites:
        m = m1.get(s["id"], {})
        if m.get("cant") or m.get("t_um") is None: continue
        t = float(m["t_um"]); f = on(s["cross"].get("F") or [], t); o = on(ov[s["id"]]["ovl"], t)
        nv += 1; o_on += o; gain += f and not o; lost += o and not f
    got["OVL_start_key1"] = f"{o_on}/{nv}"; got["F_vs_start_gained_lost"] = (gain, lost)

    # --- KEY2-STEP2 (judge_rescore.py) ---
    def val(mk):
        return None if (not mk or mk.get("cant") or mk.get("t_um") is None) else float(mk["t_um"])
    k1 = {s["id"]: val(m1.get(s["id"])) for s in sites}
    kk = J("keyfar_key.json")["sites"]; m2raw = J("keyfar_marks_chris_ratings.json")["items"]
    assert len({s["old_id"] for s in kk}) == len(kk) == 24
    k2 = {}
    for s in kk:
        v = val(m2raw.get(s["id"]))
        k2[s["old_id"]] = None if v is None else v + float(s["delta_um"]) - float(s["delta_old_um"])

    def count(key, arm):
        v = c = x = 0
        for s in sites:
            t = key.get(s["id"])
            if t is None: continue
            v += 1; c += on(s["cross"].get("N2") or [], t); x += on(s["cross"].get(arm) or [], t)
        return dict(valid=v, on_C=c, on_X=x)
    two = {}
    for arm in ("R", "F"):
        a, b = count(k1, arm), count(k2, arm)
        ca, cb = mark_class(a), mark_class(b)
        tk = "INCONCLUSIVE (TOO FEW under a key)" if "TOO FEW" in (ca, cb) else (ca if ca == cb else "KEY-LIMITED")
        two[arm] = dict(key1=dict(a, cls=ca), key2=dict(b, cls=cb), two_key=tk)
    saved = J("copyfix_result.json")
    gate = all({k: saved[st]["marks"][k] for k in ("valid", "on_C", "on_X")} == {k: two[arm]["key1"][k] for k in ("valid", "on_C", "on_X")}
               for arm, st in (("R", "step1"), ("F", "step2")))
    if not gate:
        for arm in two: two[arm]["two_key"] = "INCONCLUSIVE (scorer mismatch)"
    got["key2_consistency_gate"] = gate
    show["key2step2"] = two
    got["F_key2"] = f"{two['F']['key2']['on_X']}/{two['F']['key2']['valid']}"; got["C_key2"] = f"{two['F']['key2']['on_C']}/{two['F']['key2']['valid']}"
    got["F_key2_class"] = two["F"]["key2"]["cls"]; got["R_key2"] = f"{two['R']['key2']['on_X']}/{two['R']['key2']['valid']}"
    got["R_two_key_class"] = two["R"]["two_key"]; got["F_two_key_class"] = two["F"]["two_key"]
    both = [i for i in k1 if k1[i] is not None and k2.get(i) is not None]
    sd = {s["id"]: s for s in sites}
    same = sum(on(sd[i]["cross"].get("F") or [], k1[i]) == on(sd[i]["cross"].get("F") or [], k2[i]) for i in both)
    got["F_onoff_same_both_keys"] = f"{same}/{len(both)}"

    # --- minutes (session_times.json) ---
    st = J("session_times.json"); tm = lambda h: datetime.strptime(h if h.count(":") == 2 else h + ":00", "%H:%M:%S")
    got["minutes_sheet_rule"] = round((tm(st["f_state_save"]) - tm(st["vc3d_in_use_first_record"])).total_seconds() / 60, 1)
    lo = int((tm(st["f_state_save"]) - tm(st["sebastien_reported_start"])).total_seconds() // 60)
    hi = int((tm(st["vc3d_closed_reported"]) - tm(st["sebastien_reported_start"])).total_seconds() // 60)
    got["minutes_own_reading"] = f"{lo}-{hi}"

    got["cf_saved_result_identical"] = (saved["step1"]["outcome"] == v1["outcome"] and saved["step2"]["outcome"] == v2["outcome"]
                                        and saved["step2"]["marks"] == mF and saved["step1"]["marks"] == mR)
    got["guide_line_wording_flag"] = e["within75"] >= mF["on_C"]
    got["mark2r_human_floor"] = mark2r_floor()

    print(json.dumps(show, indent=1))
    ok = True
    for k, v in EXPECTED.items():
        g = got[k]
        m = (abs(g - v) < 1e-9) if isinstance(v, float) else (g == v)
        ok &= m
        print(f"{'MATCH   ' if m else 'MISMATCH'} {k}: got {g} expected {v}")
    print("ALL MATCH" if ok else "SOME MISMATCH")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
