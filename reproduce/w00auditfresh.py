"""W00-AUDIT-FRESH re-score (outline row 5; prereg standalone/preregs/audit_guidefree.md, item
[private path], Judge checks/20261009-01-*/judge_rescore.py, @ 60b819bd).

Pair audit: is w00's strip trace within 75 um of Chris's guide-free 2.4 um mark at each station k = 1..6?
w00's trace at each station needs the w00 mesh + CT frames, so this script starts from the saved per-station rows
(data/w00auditfresh/wa_result.json, local only; signed/abs distance per station). It
  1. recounts ON/OFF at 75 um from abs_um (as the Judge did) and re-applies the frozen rule of wa.py rule()
     (one-sided exact binomial vs p_on 0.90 + strip bootstrap, seed 2026100901, 2000 draws) and its descriptions
     (Clopper-Pearson CI, OFF distance bins, key-noise bracket K/N/(1-e), bend/flat split, strip counts);
  2. cross-checks the rows against Chris's mark files (of9/oc9/cf9_chris_key.json + page keys): every scored station is a
     station Chris marked (k 1..6, not can't-tell) and the can't-tell counts are 14 / 14;
  3. ties Chris's mark POSITIONS to the w00 geometry at station 0 (the shared ring): for every strip,
     (mark[0] - ring n) * 1000 from the mark files + the frames files (of9/oc9/cf9_frames.json, ring = f.seed[1]) must equal the
     Judge's station0_mark_minus_ring_um (judge_station0_result.json, local only) within 0.5 um, and w00's trace at station 0
     sits within 1 um of the ring on every strip (wa_stage0.json b_ring, Stage 0b). A shift of a whole mark file fails here;
  4. checks the sha256 pins that wa.py PINS (@ 60b819bd) holds for the of9/oc9 mark files, the 3 page keys and the 3 frames files.
LIMIT: w00's trace position at stations 1..6 is NOT in any saved file. wa.py computes it on the fly from the w00 mesh (line9.mesh,
mesh_P) and keeps only the distances in wa_result.json, so abs_um at k = 1..6 cannot be recomputed from the marks here;
a mark change confined to stations 1..6 that crosses no 75 um line is not caught. cf9_chris_key.json has no pin in wa.py
(it arrived after the prereg).
Usage: python reproduce/w00auditfresh.py   (exit 0 only if every compared number matches)
"""
import hashlib, json, math, sys
from pathlib import Path
import numpy as np
from scipy.stats import binom, beta as betad

D = Path(__file__).resolve().parent.parent / "data" / "w00auditfresh"
TOL_UM, P_ON0, ALPHA, BOOT, BSEED = 75.0, 0.90, 0.05, 2000, 2026100901   # wa.py line 37 @ 60b819bd
PINS = {   # wa.py PINS @ 60b819bd (source paths there: [private path],8-15,8-21}-.../(cache/))
    "of9_chris_key.json": "9b08a193585035fb57848e41fa5e09c0d4ccb922e1562a05b8805d0ab88f0a36",
    "of9_pages_key.json": "e01d70721fbd96582695b6b8f8a7b24f531b0cb34dd4a63bbdb0f5949ef2ede6",
    "oc9_chris_key.json": "e349095454e8852a43711e30bf31f13039ba942c1ab019abdf1b2b6128739f83",
    "oc9_pages_key.json": "c6e181288c5541c341cc18de8a1179fee315164e8d41805fad7a42062d526876",
    "cf9_pages_key.json": "cdd6cee20c69ea7b927488da00e29886dbd01483b001b29ce7a7f4026e3b419f",
    "of9_frames.json": "86c98a01507222c92a267b8c59fe5a8c27bbd66ad2cadbf23a1cf12cade2f2a7",
    "oc9_frames.json": "6e4b9f233439717626bd508ddda968de17dbfb67f214db2487bd98263289adff",
    "cf9_frames.json": "88635fd2fddf953686e594b263960745cfe1228326c1b7f87e329c007a1cc405",
}
ST0_TOL_UM, RING_UM = 0.5, 1.0   # Judge value is rounded to 0.1 um; wa.py RING_UM
I = "items/20261009-01-w00-audit-fresh-at-chris.md @60b819bd"

EXPECTED = {
    # item line 250-251 (Runner) and Judge line 293 ("42 ON / 40 OFF of 82, critical OFF 14 ... upper bound 0.637")
    "primary_on_n": "42/82", "primary_off_crit": 14, "primary_boot_ub95": 0.6374, "primary_verdict": "AGREE-BELOW-9IN10",
    "primary_rate": 0.51, "primary_cp95": "0.40-0.62",          # item line 251 (0.512, CI 0.399-0.624); outline "0.51, CI 0.40-0.62"
    "primary_off_75_150": 20, "primary_off_over150": 20,          # item line 256; outline "20 of the 40 misses are 75-150 um"
    "keynoise_e0.10": 0.57,                                       # item line 260-261 (0.569); Judge line 305 ("e = 0.10 -> 0.57")
    "fresh_along_on_n": "19/46",                                  # item line 254
    "fresh_bend_on_n": "5/28", "fresh_flat_on_n": "14/18",        # item line 255; Judge line 318; outline "bend 5/28 vs flat 14/18"
    "cross_on_n": "23/36",                                        # item line 254-255
    "fresh_along_strips": "10 (7 bend / 3 flat)", "cross_strips": 6,   # item line 79 / 270 / 330; outline "10 fresh along strips, 7 bend / 3 flat, + 6 cross strips"
    "primary_cant_tell": 14,                                      # item line 259
    "line2_on_n": "18/40", "line2_off_over150": "16/22",          # item line 263-264; Judge line 321
    "line2_boot_ub95": 0.6667,                                    # Judge line 294 ("Line 2: 18 / 40, upper bound 0.667")
    "line2_cant_tell": 14,                                        # wa_result.json line2.describe.cant_tell.n
    "rows_match_chris_marks": True,                               # provenance check (no saved number)
    "pins_ok": True,                                              # wa.py PINS for the 8 pinned inputs
    "station0_marks_match_judge": True,                           # mark positions vs ring geometry (step 3)
    "w00_on_ring_station0": True,                                 # wa_stage0.json b_ring, all 16 + 9 strips <= 1 um
}


def cp(k, n):
    lo = 0.0 if k == 0 else float(betad.ppf(0.025, k, n - k + 1)); hi = 1.0 if k == n else float(betad.ppf(0.975, k + 1, n - k))
    return lo, hi


def per_strip(rows):
    out = {}
    for r in rows:
        if r["status"] == "NO-W00": continue
        on = r["abs_um"] <= TOL_UM
        assert on == (r["status"] == "ON"), r          # Judge's recount check
        a = out.setdefault(r["strip"], [0, 0]); a[0] += on; a[1] += 1
    return out


def rule(ps):
    on = np.array([v[0] for v in ps.values()]); nn = np.array([v[1] for v in ps.values()])
    N, ON = int(nn.sum()), int(on.sum()); OFF = N - ON
    crit = next((x for x in range(N + 1) if binom.sf(x - 1, N, 1 - P_ON0) <= ALPHA), None)
    rng = np.random.default_rng(BSEED); idx = rng.integers(0, len(nn), size=(BOOT, len(nn)))
    ub = float(np.quantile(on[idx].sum(1) / nn[idx].sum(1), 0.95))
    v = "AGREE-BELOW-9IN10" if (crit is not None and OFF >= crit and ub < P_ON0) else "NOT-SHOWN-BELOW"
    return dict(n=N, on=ON, off=OFF, strips=len(nn), crit=crit, ub=round(ub, 4), verdict=v)


def marked(chris, pages, strips):
    """strip -> set of marked stations k in 1..6 (can't-tell = mark None, left out), from 'test' pages (wa.py marks())."""
    out = {}
    for p in pages:
        if p["tag"] != "test" or p["strip"] not in strips: continue
        out[p["strip"]] = {int(m[0]) for m in chris["items"].get(p["id"], {}).get("marks", []) if m[1] is not None and 1 <= int(m[0]) <= 6}
    return out


def station0(J):
    """(mark[0] - ring) um per strip from the mark files + frames vs the Judge's saved value; w00 on the ring at station 0."""
    js = J("judge_station0_result.json")["per_strip"]
    sets = [("of9_chris_key.json", J("of9_pages_key.json")["pages"], "of9_frames.json"),
            ("oc9_chris_key.json", J("oc9_pages_key.json")["pages"], "oc9_frames.json"),
            ("cf9_chris_key.json", J("cf9_pages_key.json")["chris"], "cf9_frames.json")]
    got, bad = {}, []
    for ck, pages, fr in sets:
        ch, F = J(ck), J(fr)
        for p in pages:
            if p["tag"] != "test" or p["strip"] not in js: continue
            m0 = {int(m[0]): m[1] for m in ch["items"].get(p["id"], {}).get("marks", []) if m[1] is not None}.get(0)
            got[p["strip"]] = None if m0 is None else (m0 - F[p["strip"]]["f"]["seed"][1]) * 1000
    for st, d in js.items():
        e, g = d["station0_mark_minus_ring_um"], got.get(st, "missing")
        if (e is None) != (g is None) or g == "missing" or (e is not None and abs(g - e) > ST0_TOL_UM): bad.append((st, e, g))
    b = J("wa_stage0.json")["b_ring"]; ring = {**b["primary_um"], **b["line2_um"]}
    on_ring = set(ring) == set(js) and all(v is not None and v <= RING_UM for v in ring.values())
    return not bad and len(got) == len(js), on_ring, bad


def main():
    with open(D / "wa_result.json", encoding="utf-8") as fh: R = json.load(fh)
    rows = R["rows"]
    prim = [r for r in rows if r["set"] in ("fresh_along", "design_cross")]; l2 = [r for r in rows if r["set"] == "fresh_cross"]
    P, L = rule(per_strip(prim)), rule(per_strip(l2))
    sc = [r for r in prim if r["status"] != "NO-W00"]; off = [r for r in sc if r["status"] == "OFF"]
    lo, hi = cp(P["on"], P["n"])
    sub = lambda f: f"{sum(r['status'] == 'ON' for r in sc if f(r))}/{sum(1 for r in sc if f(r))}"
    kind_of = {}
    for r in prim: kind_of[r["strip"]] = r["kind"]
    nb = sum(v == "bend" for v in kind_of.values()); nf = sum(v == "flat" for v in kind_of.values())
    l2off = [r for r in l2 if r["status"] == "OFF"]
    # cross-check against Chris's mark files
    def J(f):
        with open(D / f, encoding="utf-8") as fh: return json.load(fh)
    of_s = {r["strip"] for r in prim if r["set"] == "fresh_along"}; oc_s = {r["strip"] for r in prim if r["set"] == "design_cross"}
    cfp = J("cf9_pages_key.json"); cfc = J("cf9_chris_key.json"); assert cfc.get("build") == cfp["build"]
    cf_s = {p["strip"] for p in cfp["chris"] if p["tag"] == "test"}
    mk = {**marked(J("of9_chris_key.json"), J("of9_pages_key.json")["pages"], of_s),
          **marked(J("oc9_chris_key.json"), J("oc9_pages_key.json")["pages"], oc_s)}
    mk2 = marked(cfc, cfp["chris"], cf_s)
    rk = lambda rr: {s: {r["k"] for r in rr if r["strip"] == s} for s in {r["strip"] for r in rr}}
    same = rk(prim) == {s: v for s, v in mk.items() if v} and rk(l2) == {s: v for s, v in mk2.items() if v}
    pins_bad = [f for f, h in PINS.items() if hashlib.sha256((D / f).read_bytes()).hexdigest() != h]
    st0_ok, on_ring, st0_bad = station0(J)
    if st0_bad: print("station-0 mark vs ring mismatches (strip, judge um, recomputed um):", st0_bad[:5])
    if pins_bad: print("sha256 pin mismatches:", pins_bad)
    assert set(r["strip"] for r in rows) <= set(J("judge_station0_result.json")["per_strip"]), "scored strip without a station-0 check"
    cant_p = sum(6 - len(v) for v in mk.values()); cant_l = sum(6 - len(v) for v in mk2.values())
    got = {
        "primary_on_n": f"{P['on']}/{P['n']}", "primary_off_crit": P["crit"], "primary_boot_ub95": P["ub"], "primary_verdict": P["verdict"],
        "primary_rate": round(P["on"] / P["n"], 2), "primary_cp95": f"{lo:.2f}-{hi:.2f}",
        "primary_off_75_150": sum(r["abs_um"] <= 150 for r in off), "primary_off_over150": sum(r["abs_um"] > 150 for r in off),
        "keynoise_e0.10": round(min(1.0, P["on"] / P["n"] / (1 - 0.10)), 2),
        "fresh_along_on_n": sub(lambda r: r["set"] == "fresh_along"),
        "fresh_bend_on_n": sub(lambda r: r["kind"] == "bend"), "fresh_flat_on_n": sub(lambda r: r["kind"] == "flat"),
        "cross_on_n": sub(lambda r: r["set"] == "design_cross"),
        "fresh_along_strips": f"{nb + nf} ({nb} bend / {nf} flat)", "cross_strips": sum(v == "cross" for v in kind_of.values()),
        "primary_cant_tell": cant_p,
        "line2_on_n": f"{L['on']}/{L['n']}", "line2_off_over150": f"{sum(r['abs_um'] > 150 for r in l2off)}/{len(l2off)}",
        "line2_boot_ub95": L["ub"], "line2_cant_tell": cant_l, "rows_match_chris_marks": same,
        "pins_ok": not pins_bad, "station0_marks_match_judge": st0_ok, "w00_on_ring_station0": on_ring,
    }
    print(f"primary: n {P['n']}, strips {P['strips']}, binom p {binom.sf(P['off'] - 1, P['n'], 0.10):.3g}, CP {lo:.4f}-{hi:.4f}, "
          f"key-noise e=0.10 {P['on'] / P['n'] / 0.9:.4f}; line 2: {L['verdict']}, strips {L['strips']} scored of {len(cf_s)}")
    bad = 0
    for k, e in EXPECTED.items():
        g = got[k]; m = (g == e) if isinstance(e, (str, bool)) else math.isclose(g, e, abs_tol=1e-9)
        bad += not m; print(f"{'MATCH   ' if m else 'MISMATCH'} {k}: got {g} expected {e}")
    print("W00-AUDIT-FRESH:", "ALL MATCH" if not bad else f"{bad} MISMATCH")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
