"""MARK-2R re-score (outline row 5; prereg standalone/preregs/audit_guided.md, item
[private path], @ 60b819bd).

Two raters (Sebastien, Chris) marked where the sheet crosses a view line at 2.4 um, GUIDED: w00's line was drawn up to
0.3 mm before each spot. Same scoring as [private path] @ 60b819bd
(75 um tolerance on distances rounded to 0.1 um, as mark2r_score.py rows do; median = sorted(d)[n // 2] as in mark2r_score.py; straight-extension baseline; repeats), reading the
page key (data/mark2r/mark2r_key.json, local only: w00 position truth_t_um + straight extension ext_t_um per site) and
both raters' marks (data/mark2r/mark2r_<seb|chris>_ratings.json, local only). The "14 um affine residual" in the claim
is W00-NATIVE's transfer residual (see reproduce/w00native.py; not recomputed).
Usage: python reproduce/mark2r.py   (exit 0 only if every compared number matches)
"""
import json, math, sys
from pathlib import Path

D = Path(__file__).resolve().parent.parent / "data" / "mark2r"
ID_R, KEY_BAR, W00_BAR, REP_BAR, N_MIN = 75.0, 0.8, 0.85, 2 / 3, 15     # mark2r_score.py line 11-12 @ 60b819bd
RS = ("seb", "chris")

EXPECTED = {
    # item @60b819bd line 175 (Judge): "18/20 shared random sites within 75 um ... CI 0.683-0.988; median 14.4 um"
    "random_sites": 25, "hh": "18/20", "hh_ci95": "0.683-0.988", "hh_median_um": 14.4, "human_floor": "KEY OK",
    # item line 176: "w00 row 5 = MEASURED, not CONFIRMED (Sebastien 19/21, Chris 15/22)"
    "w00_seb": "19/21", "w00_chris": "15/22", "w00_row5": "MEASURED (per-rater rates printed)",
    # item line 154 / 165: straight-line baseline 23/25
    "straight_extension": "23/25",
    # item line 166 / 177: "Chris 0/2 within 75 um, diffs 137.8 um and 243.5 um" (outline: 138 / 244 um)
    "chris_repeats": "0/2", "chris_repeat_diffs_um": "138/244", "chris_repeats_unreliable": True,
    "flag_guide_line": True,                     # item line 177-178 ("consistent with following the guide line")
    # prereg L60-61: repeats "not assessable if < 2 pairs marked"; Sebastien marked 1 pair (printed line: reliability unmeasured)
    "seb_repeats_assessable": False,
    # prereg L64-65 centre bias (random + suspect first presentations, |t| <= 20 um, flag above 1/3); mark2r_summary.json centre_bias
    "centre_bias_seb": "5/30", "centre_bias_chris": "2/31", "centre_bias_flag_any": False,
    "summary_file_centre_bias_matches": True,    # cross-check vs the scorer's saved mark2r_summary.json
}
CENTRE_R, CENTRE_FLAG = 20.0, 1 / 3              # mark2r_score.py line 11 @ 60b819bd


def mark(R, pid):
    x = R["items"].get(pid)
    if not x or x.get("cant") or "t_um" not in x: return None
    return float(x["t_um"])


def cp(k, n, a=0.05):
    """exact Clopper-Pearson, by bisection (mark2r_score.py cp())."""
    def tail_ge(p): return sum(math.comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(k, n + 1))
    def tail_le(p): return sum(math.comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(0, k + 1))
    def bis(f, target, inc):
        lo, hi = 0.0, 1.0
        for _ in range(60):
            m = (lo + hi) / 2
            if (f(m) < target) == inc: lo = m
            else: hi = m
        return (lo + hi) / 2
    lo = 0.0 if k == 0 else bis(tail_ge, a / 2, True); hi = 1.0 if k == n else bis(tail_le, a / 2, False)
    return round(lo, 3), round(hi, 3)


def main():
    with open(D / "mark2r_key.json", encoding="utf-8") as fh: key = json.load(fh)
    RSd = {}
    for r in RS:
        with open(D / f"mark2r_{r}_ratings.json", encoding="utf-8") as fh: RSd[r] = json.load(fh)
    with open(D / "mark2r_summary.json", encoding="utf-8") as fh: summ = json.load(fh)
    S = key["sites"]; rnd = [s for s in S if s["stratum"] == "random"]
    # prereg L32-33: w00's position on the view line is t = -delta exactly (the site is a w00 point)
    assert all(abs(s["truth_t_um"] + s["delta_um"]) < 0.01 for s in rnd), "key: truth_t_um != -delta_um at a random site"
    m = {r: {s["id"]: mark(RSd[r], s["id"]) for s in S} for r in RS}
    hh = [round(abs(m["seb"][s["id"]] - m["chris"][s["id"]]), 1) for s in rnd if None not in (m["seb"][s["id"]], m["chris"][s["id"]])]
    k_hh = sum(d <= ID_R for d in hh); lo, hi = cp(k_hh, len(hh))
    w = {}
    for r in RS:
        dd = [round(abs(m[r][s["id"]] - s["truth_t_um"]), 1) for s in rnd if m[r][s["id"]] is not None]
        w[r] = (sum(d <= ID_R for d in dd), len(dd))
    ext = [s for s in rnd if s.get("ext_t_um") is not None]
    k_ext = sum(abs(s["ext_t_um"] - s["truth_t_um"]) <= ID_R for s in ext)
    orig = {s["pool_k"]: s["id"] for s in S if s["stratum"] in ("random", "suspect")}
    rep = {}
    for r in RS:
        both = [(m[r][orig[s["pool_k"]]], m[r][s["id"]]) for s in S if s["stratum"] == "repeat"]
        both = [(a, b) for a, b in both if a is not None and b is not None]
        rep[r] = (sum(abs(a - b) <= ID_R for a, b in both), len(both), [round(abs(a - b), 1) for a, b in both])
    cb = {}
    for r in RS:
        mm = [m[r][s["id"]] for s in S if s["stratum"] in ("random", "suspect") and m[r][s["id"]] is not None]
        cb[r] = (sum(abs(t) <= CENTRE_R for t in mm), len(mm))
    cb_flag = {r: cb[r][1] > 0 and cb[r][0] / cb[r][1] > CENTRE_FLAG for r in RS}
    summ_ok = all(summ["centre_bias"][r] == dict(marks=cb[r][1], within_20um_of_centre=cb[r][0], flag=cb_flag[r]) for r in RS)
    wmin = min(w[r][0] / w[r][1] for r in RS)
    v1 = "UNDECIDED" if len(hh) < N_MIN else ("KEY OK" if k_hh >= math.ceil(KEY_BAR * len(hh) - 1e-9) else "NOT A SINGLE-RATER KEY")
    v2 = "CONFIRMED" if all(w[r][0] / w[r][1] >= W00_BAR - 1e-9 for r in RS) else "MEASURED (per-rater rates printed)"
    got = {
        "random_sites": len(rnd), "hh": f"{k_hh}/{len(hh)}", "hh_ci95": f"{lo:.3f}-{hi:.3f}",
        "hh_median_um": sorted(hh)[len(hh) // 2], "human_floor": v1,
        "w00_seb": f"{w['seb'][0]}/{w['seb'][1]}", "w00_chris": f"{w['chris'][0]}/{w['chris'][1]}", "w00_row5": v2,
        "straight_extension": f"{k_ext}/{len(ext)}",
        "chris_repeats": f"{rep['chris'][0]}/{rep['chris'][1]}", "chris_repeat_diffs_um": "/".join(str(round(x)) for x in rep["chris"][2]),
        "chris_repeats_unreliable": rep["chris"][1] >= 2 and rep["chris"][0] / rep["chris"][1] < REP_BAR - 1e-9,
        "flag_guide_line": bool(ext) and k_ext / len(ext) >= wmin - 1e-9,
        "seb_repeats_assessable": rep["seb"][1] >= 2,
        "centre_bias_seb": f"{cb['seb'][0]}/{cb['seb'][1]}", "centre_bias_chris": f"{cb['chris'][0]}/{cb['chris'][1]}",
        "centre_bias_flag_any": any(cb_flag.values()), "summary_file_centre_bias_matches": summ_ok,
    }
    print(f"sites {len(S)} (random {len(rnd)}); Sebastien repeats {rep['seb'][0]}/{rep['seb'][1]} {rep['seb'][2]} (1 pair: "
          f"reliability unmeasured); Judge low-median of hh {sorted(hh)[(len(hh) - 1) // 2]:.1f} um")
    bad = 0
    for k, e in EXPECTED.items():
        g = got[k]; ok = (g == e) if isinstance(e, (str, bool)) else math.isclose(g, e, abs_tol=1e-9)
        bad += not ok; print(f"{'MATCH   ' if ok else 'MISMATCH'} {k}: got {g} expected {e}")
    print("MARK-2R:", "ALL MATCH" if not bad else f"{bad} MISMATCH")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
