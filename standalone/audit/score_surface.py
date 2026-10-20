"""Score any tifxyz surface of the PHerc0841 audit window against the guide-free 2.4 um marks (tier 2).

  python audit/score_surface.py selftest
      planted synthetic traces (flat and tilted sheets) are returned within 1 um; ON/OFF at 75 um; NO-SURFACE past the
      strip end; the frozen rule's verdict logic. Needs no human data and no download.
  python audit/score_surface.py score SURFACE_DIR [--affine A.json] [--pool primary|replication|all] [--json OUT.json] [--expect-w00]
      SURFACE_DIR is an organizers'-format tifxyz folder (x.tif, y.tif, z.tif, optional meta.json with "scale").

What `score` does, per strip of data/audit/guidefree_strips.json:
  1. finds where the surface crosses the strip frame's normal line through o (nearest crossing to o) and takes a grid window around
     it (rows +-3.6 mm, cols +-(L/2 + 0.6) mm in grid steps), densified x10;
  2. keeps points within 1.2 voxels of the strip plane and |n| <= 3 mm, and takes the median n per 0.02 mm s-bin;
  3. reads the surface's n at each station (k = 0..6) by linear interpolation between valid bins (none outside them).
  Then, mark-free: distance to w00's position at each station. With human_data/audit/guidefree_marks_chris.json present:
  per-station distance to the rater's mark, agreement at 75 and 150 um, exact Clopper-Pearson 95 % intervals, the exact binomial
  test against 9 in 10, the strip bootstrap (2000 resamples of strips, fixed seed), the key-noise bracket and can't-tell bounds.
  --expect-w00 asserts that the surface reproduces data/audit's w00 positions (|diff| <= 1e-9 mm at every station): run it on the
  organizers' w00 tifxyz to check this code; the guide-free numbers (42/82, 18/40) then follow.

Inputs it needs:
  - the surface in x, y, z voxel coordinates (level 0) of the public PHerc0841 2.403 um volume
    (20260319124803-2.403um-0.2m-77keV-masked.zarr); a surface in another frame needs --affine (3x4 or 4x4 JSON matrix, key
    "matrix" or a bare list) that maps its xyz into that frame. Vertices with any coordinate <= 0 are invalid (tifxyz convention).
  - no CT volume: scoring is geometry only.
  - for the w00 self-check: download the organizers' w00 mesh on the 2.403 um volume (x.tif, y.tif, z.tif, meta.json, ~9 MB) from
    s3://vesuvius-challenge-open-data/PHerc0841/segments/20260220213127-w00/mesh/20260220213127-on-20260319124803-2.403um.tifxyz/
  - tifffile (pip install tifffile) to read the .tif grids.

What it cannot do:
  - it takes one median n per 0.02 mm bin, so a surface that crosses a strip plane more than once within +-3 mm of the frame
    (several windings of a spiral fit, a fold, a large multi-winding auto-grown surface) is not scored faithfully: the median
    mixes the crossings. Each strip reports `multi_bins`, the share of its valid bins whose points spread over > 0.1 mm; a large
    share means "do not trust this strip's number". Crop such a surface to the one winding near the window first.
  - it scores agreement with ONE rater's marks (the pair), not which of the two is on the true sheet.
  - the window is fixed: 25 strips of PHerc0841 near the w00 known-text region; nothing outside it is scored."""
import os, sys, json, argparse
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import audit_core as C  # noqa: E402

MULTI_MM = 0.1


# ------------------------------------------------------------------ selftest (no human data, no download)
def synth_mesh(h_vx, slope, R=300, Cn=300):
    """flat (slope 0) or tilted sheet Z = 1000 + h + slope * (X - Xc) on a 20-voxel grid; frame at the centre, n = +z."""
    rr, cc = np.mgrid[0:R, 0:Cn].astype(float); X, Y = cc * 20.0, rr * 20.0; Xc = (Cn // 2) * 20.0
    Z = 1000.0 + h_vx + slope * (X - Xc); V = np.ones((R, Cn), bool)
    S = np.stack([X, Y, Z], -1)
    t = np.array([1.0, 0, 0]); n = np.array([0, 0, 1.0])
    f = dict(o=np.array([Xc, (R // 2) * 20.0, 1000.0]), t=t, n=n, w=np.cross(t, n), L=4.8)
    return S, V, f


def selftest():
    res = dict(traces=[])
    for h_um, slope in ((123.0, 0.0), (-40.0, 0.0), (60.0, 0.05), (0.0, -0.08)):
        S, V, f = synth_mesh(h_um / C.UM_PER_VX, slope)
        cols = [-2.0, -0.5, 0.0, 0.75, 1.9, 0.0, 0.0]
        W, _ = C.at_stations(C.strip_trace(S, V, f, 20.0), cols)
        truth = [h_um / 1000 + slope * c for c in cols]                        # in mm: n = h + slope * s
        err = max(abs(a - b) * 1000 for a, b in zip(W, truth))
        mk = [None, truth[1] + 0.070, truth[2] - 0.080, truth[3], truth[4] + 0.074, None, None]
        rows = C.score_rows([dict(strip="S", set="s", kind="s")], {"S": mk}, {"S": W})
        st = [r["status"] for r in rows]
        res["traces"].append(dict(h_um=h_um, slope=slope, max_err_um=round(err, 3), status=st, ok=bool(err <= 1.0 and st == ["ON", "OFF", "ON", "ON"])))
    S, V, f = synth_mesh(0.0, 0.0); W, _ = C.at_stations(C.strip_trace(S, V, f, 20.0), [3.5]); res["no_surface_ok"] = W[0] is None
    S, V, f = synth_mesh(0.0, 0.0); f["o"] = f["o"] + np.array([0, 0, 5000.0]); res["far_surface_none"] = C.strip_trace(S, V, f, 20.0) is None
    sizes = [6, 4, 4, 1, 2, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6]

    def mk(offs): return {f"s{i}": (s - o, s) for i, (s, o) in enumerate(zip(sizes, offs))}
    spread = mk([1, 1, 1, 0, 1, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 1])                 # 20 OFF spread out
    few = mk([0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0])                    # 5 OFF
    lumped = mk([0, 0, 0, 0, 0, 0, 6, 6, 2, 0, 0, 0, 0, 0, 0, 0])                 # 14 OFF in 3 strips
    a, b, c = C.rule(spread), C.rule(few), C.rule(lumped)
    res["verdict_cases"] = dict(spread=[a["off"], a["verdict"]], few=[b["off"], b["verdict"]], lumped=[c["off"], c["verdict"], c["leg_a"], c["leg_b"]])
    res["crit_82"] = C.off_crit(82); res["crit_80"] = C.off_crit(80)
    res["ok"] = bool(all(t["ok"] for t in res["traces"]) and res["no_surface_ok"] and res["far_surface_none"]
                     and a["verdict"] == "AGREE-BELOW-9IN10" and b["verdict"] == "NOT-SHOWN-BELOW"
                     and c["leg_a"] and c["verdict"] == "NOT-SHOWN-BELOW" and res["crit_82"] == 14)
    return res


# ------------------------------------------------------------------ score
def trace_surface(S, V, step, strips):
    pos, info = {}, {}
    for s in strips:
        f = C.frame_arrays(s["frame"]); tr = C.strip_trace(S, V, f, step)
        W, G = C.at_stations(tr, s["station_s_mm"]); pos[s["strip"]] = W
        if tr is None:
            info[s["strip"]] = dict(found=False, multi_bins=None)
        else:
            ok = ~np.isnan(tr[1]); info[s["strip"]] = dict(found=True, valid_bins=int(ok.sum()),
                                                            multi_bins=round(float(np.mean(tr[2][ok] > MULTI_MM)), 4) if ok.any() else None, gap_mm=G)
    return pos, info


def pool_summary(strips, marks, pos):
    out = {}
    for tol in (75.0, 150.0):
        a = C.summarize(strips, marks, pos, tol); v = a["rule"]
        d = dict(n=v.get("n"), on=v.get("on"), rate=v.get("rate"), cp95=v.get("cp95"), off_crit_vs_9in10=v.get("off_crit"),
                 binom_p=v.get("binom_p"), strip_bootstrap_ub95=v.get("boot_ub95"), verdict=v.get("verdict"),
                 no_surface=a["no_surface"], cant_tell=a["cant_tell"], by_kind={k: f"{x[0]}/{x[1]}" for k, x in a["by_kind"].items()})
        if tol == 75.0:
            d.update(misses_75_150=a["off_75_150"], misses_over150=a["off_over150"], keynoise_bracket=a["keynoise"],
                     cant_tell_as_miss=None if not a["cant_as_off"] else f"{a['cant_as_off']['on']}/{a['cant_as_off']['n']}",
                     cant_tell_as_agree=None if not a["cant_as_on"] else f"{a['cant_as_on']['on']}/{a['cant_as_on']['n']}",
                     rows=[{k: (round(x, 2) if isinstance(x, float) else x) for k, x in r.items()} for r in a["rows"]])
        out[f"tol_{int(tol)}um"] = d
    return out


def load_affine(p):
    m = C.load(p); m = m.get("matrix", m) if isinstance(m, dict) else m
    m = np.asarray(m, float); assert m.shape in ((3, 4), (4, 4)), "affine must be 3x4 or 4x4"
    return m


def cmd_score(a):
    D = C.load(os.path.join(C.DATA, "guidefree_strips.json"))["strips"]
    if a.pool != "all":
        D = [s for s in D if s["pool"] == a.pool]
    S, V, step = C.read_tifxyz(a.surface, load_affine(a.affine) if a.affine else None)
    pos, info = trace_surface(S, V, step, D)
    out = dict(surface=os.path.basename(os.path.normpath(a.surface)), grid_step_vx=step, strips={})
    dmax = 0.0
    for s in D:
        W = pos[s["strip"]]; dw = [None if (x is None or y is None) else round((x - y) * 1000, 3) for x, y in zip(W, s["w00_n_mm"])]
        out["strips"][s["strip"]] = dict(pool=s["pool"], kind=s["kind"], surface_n_mm=W, minus_w00_um=dw, **info[s["strip"]])
        for x, y in zip(W, s["w00_n_mm"]):
            if (x is None) != (y is None):
                dmax = float("inf")
            elif x is not None:
                dmax = max(dmax, abs(x - y))
    for pool in sorted({s["pool"] for s in D}):
        ss = [s for s in D if s["pool"] == pool]
        k = [(s["strip"], j) for s in ss for j in range(1, 7)]
        dd = [out["strips"][st]["minus_w00_um"][j] for st, j in k]
        out[f"{pool}_vs_w00_markfree"] = dict(stations=len(dd), within_75um=sum(1 for x in dd if x is not None and abs(x) <= 75),
                                              no_surface=sum(x is None for x in dd), note="agreement with w00 (not with a person): description only")
    print(f"surface {out['surface']}: grid step {step} vx; strips found {sum(i['found'] for i in info.values())}/{len(D)}; "
          f"max |surface - w00| at stations {dmax * 1000:.6f} um")
    if a.expect_w00:
        assert dmax <= 1e-9, f"surface does not reproduce w00's station positions (max diff {dmax} mm)"
        print("expect-w00: OK (every station equals data/audit's w00 position within 1e-9 mm)")
    mf = C.human_file("guidefree_marks_chris.json")
    if mf is None:
        print("SKIPPED: human data not in this copy (human_data/audit/guidefree_marks_chris.json): mark-free comparison only")
    else:
        MK = C.load(mf)["pools"]
        for pool in sorted({s["pool"] for s in D}):
            ss = [s for s in D if s["pool"] == pool]; r = pool_summary(ss, MK[pool], pos); out[f"{pool}_vs_marks"] = r
            t, u = r["tol_75um"], r["tol_150um"]
            print(f"{pool}: within 75 um {t['on']}/{t['n']} ({t['rate']}, CP {t['cp95']}, strip-bootstrap ub {t['strip_bootstrap_ub95']}, "
                  f"{t['verdict']}); within 150 um {u['on']}/{u['n']} (CP {u['cp95']}); key-noise {t['keynoise_bracket']}; "
                  f"can't tell {t['cant_tell']}; no surface {t['no_surface']}")
    for st, i in out["strips"].items():
        if i["multi_bins"] is not None and i["multi_bins"] > 0.05:
            print(f"warning: strip {st}: {i['multi_bins']:.0%} of bins spread > {MULTI_MM} mm (several crossings?): its number is not faithful")
    if a.json:
        with open(a.json, "w", encoding="utf8") as fh:
            json.dump(out, fh, indent=1)
        print("wrote", a.json)
    return out


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0]); sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("selftest")
    q = sub.add_parser("score"); q.add_argument("surface"); q.add_argument("--affine"); q.add_argument("--json")
    q.add_argument("--pool", default="all", choices=["primary", "replication", "all"]); q.add_argument("--expect-w00", action="store_true")
    a = p.parse_args(argv)
    if a.cmd == "selftest":
        r = selftest(); print("SELFTEST", "OK" if r["ok"] else "FAIL", json.dumps(r)); return 0 if r["ok"] else 1
    cmd_score(a); return 0


if __name__ == "__main__":
    sys.exit(main())
