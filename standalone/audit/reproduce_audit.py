"""Reproduce every number of the w00 audit from data/audit/ and human_data/audit/ (numpy + scipy only).

  python audit/reproduce_audit.py          prints one table (expected vs got); exit 0 only if every check passes

Three parts:
  audit_guidefree  w00 vs one rater's guide-free 2.4 um marks at stations 0.75-4.5 mm from a shared w00 start
                   (primary pool: 10 fresh along strips + 6 cross strips; replication pool: 9 fresh cross strips)
  audit_guided     two raters marking blind where the followed sheet crosses a short view line, with w00's line shown up
                   to 0.3 mm before the spot, at 25 random + 10 suspect w00 sites (+ 3 repeats)
  handfix          a 1 cm2 hand-fixed square vs the control (w00) at 24 sites, under two marking sessions of the same rater
The mark-free checks run without human data. Each part that needs human data prints
`SKIPPED: human data not in this copy (<file>)` when that file is missing, and does not fail."""
import os, sys, math
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import audit_core as C  # noqa: E402

# ---------------------------------------------------------------- expected values (copied from the judged re-score outputs)
EXPECTED = {
    # mark-free
    "data: strips (primary / replication)": "16 / 9",
    "data: w00 at station 0 == shared start, max |diff| <= 1 um": True,
    # guide-free audit (one rater, guide-free marks)
    "guidefree primary: on / n": "42/82",
    "guidefree primary: rate": 0.5122,
    "guidefree primary: Clopper-Pearson 95 %": [0.3992, 0.6242],
    "guidefree primary: OFF critical count (p_on 0.90, one-sided 0.05)": 14,
    "guidefree primary: strip-bootstrap 95 % upper bound": 0.6374,
    "guidefree primary: frozen verdict": "AGREE-BELOW-9IN10",
    "guidefree primary: misses 75-150 um / > 150 um": "20 / 20",
    "guidefree primary: can't-tell stations": 14,
    "guidefree primary: can't-tells as misses / as agreements": "42/96 / 56/96",
    "guidefree primary: key-noise bracket e = 0 / 0.065 / 0.10": [0.5122, 0.5478, 0.5691],
    "guidefree primary: leave-one-strip-out drops that change the verdict": 0,
    "guidefree primary (post hoc): fresh along bend / flat": "5/28 / 14/18",
    "guidefree primary: fresh along / cross at dev sites": "19/46 / 23/36",
    "guidefree replication: on / n (strips)": "18/40 (8)",
    "guidefree replication: Clopper-Pearson 95 %": [0.2926, 0.6151],
    "guidefree replication: OFF critical count": 8,
    "guidefree replication: strip-bootstrap 95 % upper bound": 0.6667,
    "guidefree replication: misses 75-150 um / > 150 um": "6 / 16",
    "guidefree replication: can't-tell stations": 14,
    "guidefree replication: key-noise bracket e = 0 / 0.065 / 0.10": [0.45, 0.4813, 0.5],
    # guided audit (two raters, guide shown)
    "guided random: human-human within 75 um / shared": "18/20",
    "guided random: human-human median (um)": 14.4,
    "guided random: human-human Clopper-Pearson 95 %": [0.683, 0.988],
    "guided random: w00 vs Sebastien / vs Chris": "19/21 / 15/22",
    "guided random: w00 vs Sebastien CI / vs Chris CI": [[0.696, 0.988], [0.451, 0.861]],
    "guided random: w00 median distance Sebastien / Chris (um)": [25.3, 53.0],
    "guided random: can't tell Sebastien / Chris": "4 / 3",
    "guided random: straight extension of the guide within 75 um of w00": "23/25",
    "guided random: marks within 75 um of the straight extension Sebastien / Chris": "18/21 / 13/22",
    "guided random: sites where both raters agree and both are > 75 um off the extension": 2,
    "guided random: centre-click baseline": "15/25",
    "guided repeats: Chris pairs within 75 um (diffs um)": "0/2 (137.8, 243.5)",
    "guided repeats: Sebastien pairs marked (diffs um)": "1 (2.4): unmeasured",
    "guided suspect: human-human / w00 vs Sebastien / w00 vs Chris": "9/9 / 6/9 / 6/9",
    "guided: verdict (human floor; w00 row; flags)": "KEY OK; MEASURED; chris repeats unreliable + consistent with following the guide line",
    # hand fix
    "handfix session 1: hand-fixed / control / start / copy (on of valid)": "17 / 23 / 16 / 14 of 24",
    "handfix session 1: class (KILL <= control - 5; MIDDLE from control - 4)": "KILL-marks (KILL line 18, MIDDLE at 19)",
    "handfix session 1: hand-fixed on at 50 / 75 / 100 um (control)": "13 / 17 / 20 (20 / 23 / 24)",
    "handfix session 1: start -> hand-fixed sites gained / lost": "4 / 3",
    "handfix session 1: marks within 75 um of the straight guide": "22/24",
    "handfix session 2: hand-fixed / control / copy (on of valid)": "16 / 19 / 14 of 23",
    "handfix session 2: class (KILL line, PASS needs)": "MIDDLE (14, 18)",
    "handfix: 23 sites valid in both sessions, session 1 hand-fixed / control": "17 / 22 (KILL-marks)",
    "handfix: hand-fixed on/off same in both sessions": "16/23",
    "handfix: label": "KEY-LIMITED (classes differ between the two sessions of one rater)",
}


def _fmt(v):
    return v if isinstance(v, str) else repr(v)


# ---------------------------------------------------------------- mark-free
def part_data():
    D = C.load(os.path.join(C.DATA, "guidefree_strips.json"))["strips"]
    npri = sum(s["pool"] == "primary" for s in D); nrep = sum(s["pool"] == "replication" for s in D)
    ring = max(abs(s["w00_n_mm"][0] - s["seed_n_mm"]) * 1000 for s in D)
    return {"data: strips (primary / replication)": f"{npri} / {nrep}",
            "data: w00 at station 0 == shared start, max |diff| <= 1 um": bool(ring <= 1.0)}, D


# ---------------------------------------------------------------- guide-free
def guidefree_pool(strips, marks):
    pos = {s["strip"]: s["w00_n_mm"] for s in strips}
    return C.summarize(strips, marks, pos)


def part_guidefree(D):
    f = C.human_file("guidefree_marks_chris.json")
    if f is None:
        return None, "guidefree_marks_chris.json"
    MK = C.load(f)["pools"]; out = {}
    P = [s for s in D if s["pool"] == "primary"]; Rp = [s for s in D if s["pool"] == "replication"]
    a = guidefree_pool(P, MK["primary"]); v = a["rule"]
    out["guidefree primary: on / n"] = f"{v['on']}/{v['n']}"
    out["guidefree primary: rate"] = v["rate"]
    out["guidefree primary: Clopper-Pearson 95 %"] = v["cp95"]
    out["guidefree primary: OFF critical count (p_on 0.90, one-sided 0.05)"] = v["off_crit"]
    out["guidefree primary: strip-bootstrap 95 % upper bound"] = v["boot_ub95"]
    out["guidefree primary: frozen verdict"] = v["verdict"]
    out["guidefree primary: misses 75-150 um / > 150 um"] = f"{a['off_75_150']} / {a['off_over150']}"
    out["guidefree primary: can't-tell stations"] = a["cant_tell"]
    out["guidefree primary: can't-tells as misses / as agreements"] = (f"{a['cant_as_off']['on']}/{a['cant_as_off']['n']} / "
                                                                       f"{a['cant_as_on']['on']}/{a['cant_as_on']['n']}")
    out["guidefree primary: key-noise bracket e = 0 / 0.065 / 0.10"] = list(a["keynoise"].values())
    out["guidefree primary: leave-one-strip-out drops that change the verdict"] = a.get("loso_turned_off")
    bk = a["by_kind"]; bs = a["by_set"]
    out["guidefree primary (post hoc): fresh along bend / flat"] = f"{bk['bend'][0]}/{bk['bend'][1]} / {bk['flat'][0]}/{bk['flat'][1]}"
    out["guidefree primary: fresh along / cross at dev sites"] = (f"{bs['fresh_along'][0]}/{bs['fresh_along'][1]} / "
                                                                  f"{bs['design_cross'][0]}/{bs['design_cross'][1]}")
    b = guidefree_pool(Rp, MK["replication"]); w = b["rule"]
    out["guidefree replication: on / n (strips)"] = f"{w['on']}/{w['n']} ({w['strips']})"
    out["guidefree replication: Clopper-Pearson 95 %"] = w["cp95"]
    out["guidefree replication: OFF critical count"] = w["off_crit"]
    out["guidefree replication: strip-bootstrap 95 % upper bound"] = w["boot_ub95"]
    out["guidefree replication: misses 75-150 um / > 150 um"] = f"{b['off_75_150']} / {b['off_over150']}"
    out["guidefree replication: can't-tell stations"] = b["cant_tell"]
    out["guidefree replication: key-noise bracket e = 0 / 0.065 / 0.10"] = list(b["keynoise"].values())
    return out, None


# ---------------------------------------------------------------- guided (two raters, guide shown)
def part_guided():
    fs, fm = C.human_file("guided_sites.json"), C.human_file("guided_marks.json")
    if fs is None or fm is None:
        return None, "guided_sites.json" if fs is None else "guided_marks.json"
    S = C.load(fs)["sites"]; MK = C.load(fm)["raters"]; seb, chr_ = MK["sebastien"], MK["chris"]; out = {}
    rand = [s for s in S if s["stratum"] == "random"]; susp = [s for s in S if s["stratum"] == "suspect"]

    def hh(ss):
        return [abs(seb[s["id"]] - chr_[s["id"]]) for s in ss if seb[s["id"]] is not None and chr_[s["id"]] is not None]

    def w00(ss, M):
        return [abs(M[s["id"]] - s["w00_t_um"]) for s in ss if M[s["id"]] is not None]

    def k(d): return sum(x <= C.TOL_UM for x in d)
    def med(d): return round(sorted(d)[len(d) // 2], 1)            # upper median, as the pre-registered scorer
    h = hh(rand); ws, wc = w00(rand, seb), w00(rand, chr_)
    out["guided random: human-human within 75 um / shared"] = f"{k(h)}/{len(h)}"
    out["guided random: human-human median (um)"] = med(h)
    out["guided random: human-human Clopper-Pearson 95 %"] = C.cp(k(h), len(h), 3)
    out["guided random: w00 vs Sebastien / vs Chris"] = f"{k(ws)}/{len(ws)} / {k(wc)}/{len(wc)}"
    out["guided random: w00 vs Sebastien CI / vs Chris CI"] = [C.cp(k(ws), len(ws), 3), C.cp(k(wc), len(wc), 3)]
    out["guided random: w00 median distance Sebastien / Chris (um)"] = [med(ws), med(wc)]
    out["guided random: can't tell Sebastien / Chris"] = f"{sum(seb[s['id']] is None for s in rand)} / {sum(chr_[s['id']] is None for s in rand)}"
    xr = [s for s in rand if s["straight_extension_t_um"] is not None]; ext = lambda s: s["straight_extension_t_um"]
    out["guided random: straight extension of the guide within 75 um of w00"] = f"{sum(abs(ext(s) - s['w00_t_um']) <= C.TOL_UM for s in xr)}/{len(xr)}"
    pr = []
    for M in (seb, chr_):
        mm = [s for s in xr if M[s["id"]] is not None]; pr.append(f"{sum(abs(M[s['id']] - ext(s)) <= C.TOL_UM for s in mm)}/{len(mm)}")
    out["guided random: marks within 75 um of the straight extension Sebastien / Chris"] = " / ".join(pr)
    both_off = sum(1 for s in xr if seb[s["id"]] is not None and chr_[s["id"]] is not None and abs(seb[s["id"]] - chr_[s["id"]]) <= C.TOL_UM
                   and abs(seb[s["id"]] - ext(s)) > C.TOL_UM and abs(chr_[s["id"]] - ext(s)) > C.TOL_UM)
    out["guided random: sites where both raters agree and both are > 75 um off the extension"] = both_off
    out["guided random: centre-click baseline"] = f"{sum(abs(s['w00_t_um']) <= C.TOL_UM for s in rand)}/{len(rand)}"
    reps = {}
    for name, M in (("sebastien", seb), ("chris", chr_)):
        d = [round(abs(M[s["original_id"]] - M[s["id"]]), 1) for s in S if s["stratum"] == "repeat"
             and M[s["original_id"]] is not None and M[s["id"]] is not None]
        reps[name] = d
    dc = reps["chris"]; ds = reps["sebastien"]
    out["guided repeats: Chris pairs within 75 um (diffs um)"] = f"{sum(x <= C.TOL_UM for x in dc)}/{len(dc)} ({', '.join(str(x) for x in dc)})"
    out["guided repeats: Sebastien pairs marked (diffs um)"] = f"{len(ds)} ({', '.join(str(x) for x in ds)}): " + ("unmeasured" if len(ds) < 2 else "measured")
    hs, wss, wcs = hh(susp), w00(susp, seb), w00(susp, chr_)
    out["guided suspect: human-human / w00 vs Sebastien / w00 vs Chris"] = f"{k(hs)}/{len(hs)} / {k(wss)}/{len(wss)} / {k(wcs)}/{len(wcs)}"
    # verdict by the pre-registered rules (random stratum)
    floor = "UNDECIDED" if len(h) < 15 else ("KEY OK" if k(h) >= math.ceil(0.8 * len(h) - 1e-9) else "NOT A SINGLE-RATER KEY")
    row = "CONFIRMED" if min(k(ws) / len(ws), k(wc) / len(wc)) >= 0.85 - 1e-9 else "MEASURED"
    flags = [f"{n} repeats unreliable" for n, d in reps.items() if len(d) >= 2 and sum(x <= C.TOL_UM for x in d) / len(d) < 2 / 3 - 1e-9]
    ext_rate = sum(abs(ext(s) - s["w00_t_um"]) <= C.TOL_UM for s in xr) / len(xr)
    if ext_rate >= min(k(ws) / len(ws), k(wc) / len(wc)) - 1e-9:
        flags.append("consistent with following the guide line")
    out["guided: verdict (human floor; w00 row; flags)"] = f"{floor}; {row}; " + " + ".join(flags)
    return out, None


# ---------------------------------------------------------------- hand fix
def mark_class(valid, on_c, on_x):
    if valid < 18:
        return "TOO FEW"
    if on_x <= on_c - 5:
        return "KILL-marks"
    if on_x >= on_c - 2 and on_x >= 0.75 * valid:
        return "PASS-marks"
    return "MIDDLE"


def part_handfix():
    fs, fm = C.human_file("handfix_sites.json"), C.human_file("handfix_marks_chris.json")
    if fs is None or fm is None:
        return None, "handfix_sites.json" if fs is None else "handfix_marks_chris.json"
    H = C.load(fs); MK = C.load(fm)["marks"]; S = H["sites"]; out = {}
    k1 = MK["session1"]
    k2 = {m["site_id"]: (None if MK["session2"][m["session2_id"]] is None else MK["session2"][m["session2_id"]] + m["delta_um"] - m["delta_old_um"])
          for m in H["session2_map"]}

    def on(c, t, r=C.TOL_UM): return len(c) == 1 and abs(c[0] - t) <= r

    def count(key, arm, only=None, r=C.TOL_UM):
        v = c = x = 0
        for s in S:
            t = key.get(s["id"])
            if t is None or (only is not None and s["id"] not in only):
                continue
            v += 1; c += on(s["crossings_um"]["control"], t, r); x += on(s["crossings_um"][arm], t, r)
        return v, c, x

    v, cC, fF = count(k1, "handfix"); _, _, st = count(k1, "start"); _, _, cp_ = count(k1, "copy")
    out["handfix session 1: hand-fixed / control / start / copy (on of valid)"] = f"{fF} / {cC} / {st} / {cp_} of {v}"
    c1 = mark_class(v, cC, fF)
    out["handfix session 1: class (KILL <= control - 5; MIDDLE from control - 4)"] = f"{c1} (KILL line {cC - 5}, MIDDLE at {cC - 4})"
    rad = [count(k1, "handfix", r=r) for r in (50.0, 75.0, 100.0)]
    out["handfix session 1: hand-fixed on at 50 / 75 / 100 um (control)"] = (" / ".join(str(x[2]) for x in rad) + " (" + " / ".join(str(x[1]) for x in rad) + ")")
    gain = sum(1 for s in S if k1[s["id"]] is not None and on(s["crossings_um"]["handfix"], k1[s["id"]]) and not on(s["crossings_um"]["start"], k1[s["id"]]))
    lost = sum(1 for s in S if k1[s["id"]] is not None and on(s["crossings_um"]["start"], k1[s["id"]]) and not on(s["crossings_um"]["handfix"], k1[s["id"]]))
    out["handfix session 1: start -> hand-fixed sites gained / lost"] = f"{gain} / {lost}"
    ex = [s for s in S if k1[s["id"]] is not None and s["straight_extension_t_um"] is not None]
    out["handfix session 1: marks within 75 um of the straight guide"] = f"{sum(abs(s['straight_extension_t_um'] - k1[s['id']]) <= C.TOL_UM for s in ex)}/{len(ex)}"
    v2, cC2, fF2 = count(k2, "handfix"); _, _, cp2 = count(k2, "copy")
    out["handfix session 2: hand-fixed / control / copy (on of valid)"] = f"{fF2} / {cC2} / {cp2} of {v2}"
    c2 = mark_class(v2, cC2, fF2)
    out["handfix session 2: class (KILL line, PASS needs)"] = f"{c2} ({cC2 - 5}, {max(cC2 - 2, math.ceil(0.75 * v2))})"
    both = {i for i in k1 if k1[i] is not None and k2.get(i) is not None}
    vb, cb, fb = count(k1, "handfix", only=both)
    out["handfix: 23 sites valid in both sessions, session 1 hand-fixed / control"] = f"{fb} / {cb} ({mark_class(vb, cb, fb)})"
    same = sum(on(s["crossings_um"]["handfix"], k1[s["id"]]) == on(s["crossings_um"]["handfix"], k2[s["id"]]) for s in S if s["id"] in both)
    out["handfix: hand-fixed on/off same in both sessions"] = f"{same}/{len(both)}"
    out["handfix: label"] = ("KEY-LIMITED (classes differ between the two sessions of one rater)" if c1 != c2 else "SAME CLASS at both sessions")
    return out, None


# ---------------------------------------------------------------- table
def run(verbose=True):
    got, D = part_data(); skipped = []; skipped_parts = set()
    for part, fn in (("guidefree", lambda: part_guidefree(D)), ("guided", part_guided), ("handfix", part_handfix)):
        r, miss = fn()
        if r is None:
            skipped.append(miss); skipped_parts.add(part)
        else:
            got.update(r)
    rows = []
    for name, exp in EXPECTED.items():
        part = name.split(":")[0].split()[0]
        if part in skipped_parts:
            continue
        if name not in got:
            rows.append((name, exp, "<not computed>", False)); continue
        g = got[name]; ok = (g == exp) if not isinstance(exp, float) else abs(g - exp) < 1e-12
        rows.append((name, exp, g, ok))
    if verbose:
        w = max(len(r[0]) for r in rows)
        print(f"{'check'.ljust(w)} | {'expected':<40} | {'got':<40} | ok")
        for name, exp, g, ok in rows:
            print(f"{name.ljust(w)} | {_fmt(exp):<40} | {_fmt(g):<40} | {'PASS' if ok else 'FAIL'}")
        for m in skipped:
            print(f"SKIPPED: human data not in this copy ({os.path.join('human_data', 'audit', m)})")
    return all(r[3] for r in rows), rows, skipped


if __name__ == "__main__":
    ok, rows, skipped = run()
    print(f"audit: {sum(r[3] for r in rows)}/{len(rows)} checks pass" + (f", {len(skipped)} part(s) skipped" if skipped else ""))
    sys.exit(0 if ok else 1)
