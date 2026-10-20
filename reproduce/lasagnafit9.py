"""Failures: LASAGNA-FIT-9 (standalone/preregs/lasagna_fit.md), the organizers' lasagna self-map seed fit, one run.

Re-derives from saved files (no GPU, no torch):
  - the stop step and rule, and the stage-3 loss terms, from the fit's own log (fit.log). The log's progress tables are
    fixed-width and right-aligned; on each stage's step-0 row the it/s field is blank, so values are assigned to columns by
    their end position under the header (a plain whitespace split shifts that row one column left);
  - the final surface's distance to its own seed anchor and its winding offset along the seed's ray, re-implementing the
    Judge's check ([private path] at 60b819bd) on the
    exported winding_0000 grid (x/y/z converted once from the .tif files to winding_0000_xyz.json) and the clicked axis
    (umbilicus.json); seed (3696, 4054, 14558) from fit.log / the prereg;
  - the seed patch's share within one winding pitch (< 0.70 -> KILL): this is the Judge's reading of the prereg's step-7
    "leaves the patch" clause (verdict finding 2), not a number the prereg wrote down; the prereg's literal coverage metric
    is the coded gate (1.0), printed beside it;
  - nearest-vertex-to-seed per snapshot through stage 2 needs the torch model snapshots: RE-READ from
    runner_job2_drift.json (derived), not recomputed.
docs/WORDING_FLAGS.md flags 1 and 4 (accepted by Chris 2026-10-20, outline cf541ce98) corrected two README values the
saved files contradicted: the stage-3 anchor start is 0.0000 after the stage-3 re-set (7.17 at the end of stage 2), not
0.0009 (a column shift), and the surface stayed within ~35 voxels of the seed through stage 2 (first snapshots 34.7 vx),
not 28. The measured values are asserted under measured_* keys.

Run: python reproduce/lasagnafit9.py   (numpy)
"""
import json, re, sys
from pathlib import Path
import numpy as np

DATA = Path(__file__).resolve().parent.parent / "data" / "lasagnafit9"
VOX_UM = 9.366
SEED = np.array([3696, 4054, 14558.0])

IT = "[private path]"   # at 60b819bd, Verdict section
EXPECTED = {
    "stage3_stop_step": 2459,                 # IT finding 4 "Stage 3 stopped itself at 2459/10000 steps"; outline
    "stage3_max_steps": 10000,
    "stop_rule": "rel_improvement_100 < 1e-4",  # IT finding 4; outline "rel_improvement_100 < 1e-4"
    "nearest_vertex_to_seed_vx": 369.3,       # IT finding 1 "369.3 vx (3.46 mm)"
    "nearest_vertex_to_seed_mm": 3.46,        # IT finding 1; outline "ended 3.46 mm from the point it was told to hold"
    "windings_inward_min": 11.5,              # IT finding 1 "11.5-12.7 windings inward" (outline: "roughly 11-13",
    "windings_inward_max": 12.7,              #   the Judge's own instruction for outside wording, same finding)
    "seed_patch_share_within_1_pitch": 0.046,  # IT finding 1 "only 0.046 of its vertices"
    "coded_gate_coverage": 1.0,               # IT finding 1 "The coded gate said 1.0"; outline "our coded check ... said covered"
    "verdict_by_judge_reading_of_step7": "KILL",   # IT "Verdict by the pre-written rule: KILL"; share < 0.70 = Judge's reading (finding 2)
    "nearest_vx_end_of_stage2": 28.1,         # IT finding 4 "within 28 vx of the seed through the end of stage 2" (derived)
    "self_snap_stage3_start": 4.8e3,          # IT finding 4 "self-snap loss fell 4.8e3 -> 4.9e2"; outline
    "self_snap_stage3_end": 4.9e2,
    "anchor_station_t_stage3_start": 0.0,     # outline (flag 1) "0.0000 after the stage-3 re-set -> 19.5"; IT's 0.0009 = next column
    "anchor_station_t_stage3_end": 19.5,
    # README (flag 4) "the surface stayed within ~35 voxels of the seed through stage 2"
    "max_vx_thru_stage2_within_35": True,
    # MEASURED (asserted): max nearest-vertex distance over the stage 0-2 snapshots (runner_job2_drift.json, derived)
    "measured_max_vx_thru_stage2": 34.7,
    # MEASURED (asserted): fit.log station_t at the last stage-2 row (7.1656); stage 3 re-sets the anchor (WORDING_FLAGS flag 1)
    "measured_station_t_end_stage2": 7.17,
}
TOL = {"nearest_vertex_to_seed_vx": 0.05, "nearest_vertex_to_seed_mm": 0.005, "windings_inward_min": 0.05,
       "windings_inward_max": 0.05, "seed_patch_share_within_1_pitch": 0.0005, "coded_gate_coverage": 1e-9,
       "nearest_vx_end_of_stage2": 0.05, "self_snap_stage3_start": 0.05e3, "self_snap_stage3_end": 0.05e2,
       "anchor_station_t_stage3_start": 0.00005, "anchor_station_t_stage3_end": 0.05,
       "measured_max_vx_thru_stage2": 0.05, "measured_station_t_end_stage2": 0.005}


def parse_tables(lines):
    """Rows of the optimizer progress tables -> list of dicts {stage, step, col: value}, columns placed by end position."""
    rows, hdr = [], None
    for ln in lines:
        if re.match(r"^\s+step\s+loss\s", ln):
            hdr = [(m.group(0), m.end()) for m in re.finditer(r"\S+", ln)]
            continue
        m = re.match(r"^\s*stage(\d+)\s+(\d+)/\S+", ln)
        if hdr is None or not m:
            continue
        toks = [(t.group(0), t.end()) for t in re.finditer(r"\S+", ln)][2:]   # skip 'stageN' and 'k/total'
        cols = hdr[1:]   # skip the 'step' header (stage step)
        rec = {"stage": int(m.group(1)), "step": int(m.group(2))}
        for tok, end in toks:
            name = min(cols, key=lambda c: abs(c[1] - end))[0]
            if name in rec:   # duplicate header names (two 'step' columns): keep the one nearest by position
                name = name + "#2"
            rec[name] = float(tok)
        rows.append(rec)
    return rows


def main():
    got = {}
    log = (DATA / "fit.log").read_text(encoding="utf-8").splitlines()
    stop = [l for l in log if "auto steps stopped at" in l][0]
    m = re.search(r"stopped at (\d+)/(\d+) (rel_improvement_100)=(\S+) < (\S+)", stop)
    got["stage3_stop_step"], got["stage3_max_steps"] = int(m.group(1)), int(m.group(2))
    got["stop_rule"] = f"{m.group(3)} < {float(m.group(5)):.0e}".replace("e-04", "e-4")
    print("log:", stop.strip())

    rows = parse_tables(log)
    s3 = [r for r in rows if r["stage"] == 3]
    first, last = s3[0], s3[-1]
    s2end = [r for r in rows if r["stage"] == 2][-1]
    got["self_snap_stage3_start"], got["self_snap_stage3_end"] = first["smap"], last["smap"]
    got["anchor_station_t_stage3_start"], got["anchor_station_t_stage3_end"] = first["station_t"], last["station_t"]
    naive = log[[i for i, l in enumerate(log) if re.match(r"^\s*stage3 0/", l)][0]].split()
    print(f"stage3 step {first['step']}: station_t {first['station_t']} (column-aligned); a whitespace split of that row "
          f"would put {naive[7]} under station_t, which is really the next column ('step' term = {first.get('step#2')})")
    row1 = log[[i for i, l in enumerate(log) if re.match(r"^\s*stage3 1/", l)][0]].split()   # it/s filled in on this row
    print(f"parser-independent check: plain split of the 'stage3 1/' row (it/s present) gives station_t {row1[7]}, "
          f"next column {row1[8]}; aligned parse of row 0 gives station_t {first['station_t']} -> "
          f"{'agree' if float(row1[7]) == first['station_t'] else 'DISAGREE'}")
    print(f"stage3 step {last['step']}: station_t {last['station_t']}, smap {last['smap']}; "
          f"stage2 end (step {s2end['step']}): station_t {s2end['station_t']}, smap {s2end['smap']}")
    st = [l.strip() for l in log if l.startswith("[station] initial")]
    print("anchor-to-seed distance at each stage start (log):", [re.search(r"seed_dist=(\S+)", l).group(1) for l in st])

    # --- surface vs its own seed (judge_patch_check.py re-implemented) ---
    with open(DATA / "winding_0000_xyz.json", encoding="utf-8") as fh:
        g = json.load(fh)
    X, Y, Z = (np.array(g[a], dtype=np.float32).astype(float) for a in "xyz")
    with open(DATA / "umbilicus.json", encoding="utf-8") as fh:
        cp = json.load(fh)["control_points"]
    z = np.array([c["z"] for c in cp], float); o = np.argsort(z); z = z[o]
    ax = np.array([c["x"] for c in cp], float)[o]; ay = np.array([c["y"] for c in cp], float)[o]
    V = (X >= 0) & np.isfinite(X) & np.isfinite(Y) & np.isfinite(Z)
    sx, sy = np.interp(SEED[2], z, ax), np.interp(SEED[2], z, ay)
    seed_r = float(np.hypot(SEED[0] - sx, SEED[1] - sy)); seed_th = float(np.arctan2(SEED[1] - sy, SEED[0] - sx))
    D = np.where(V, np.sqrt((X - SEED[0]) ** 2 + (Y - SEED[1]) ** 2 + (Z - SEED[2]) ** 2), np.inf)
    i, j = np.unravel_index(np.argmin(D), D.shape)
    qx = np.interp(Z, z, ax); qy = np.interp(Z, z, ay); r = np.hypot(X - qx, Y - qy); th = np.arctan2(Y - qy, X - qx)
    cross = []
    for a in range(V.shape[0]):
        if not V[a].any() or abs(np.nanmedian(np.where(V[a], Z[a], np.nan)) - SEED[2]) > 100:
            continue
        t = np.where(V[a], th[a], np.nan); dt = np.angle(np.exp(1j * (t - seed_th)))
        for b in range(V.shape[1] - 1):
            if V[a, b] and V[a, b + 1] and np.sign(dt[b]) != np.sign(dt[b + 1]) and abs(dt[b] - dt[b + 1]) < 1.0:
                f = dt[b] / (dt[b] - dt[b + 1]); cross.append(r[a, b] + f * (r[a, b + 1] - r[a, b]))
    pitch = 329 / VOX_UM
    wind = sorted(round((seed_r - c) / pitch, 1) for c in cross)
    got["nearest_vertex_to_seed_vx"] = round(float(D[i, j]), 1)
    got["nearest_vertex_to_seed_mm"] = round(float(D[i, j]) * VOX_UM / 1000, 2)
    got["windings_inward_min"], got["windings_inward_max"] = wind[0], wind[-1]
    print(f"seed radius {seed_r:.1f} vx; seed-ray crossings {sorted(round(float(c), 1) for c in cross)} vx; pitch {pitch:.1f} vx")

    W_Z = (13498, 15593); HALF_W_VX = 5.85e3 / VOX_UM
    e = np.sqrt(np.diff(X, axis=1) ** 2 + np.diff(Y, axis=1) ** 2 + np.diff(Z, axis=1) ** 2)[V[:, 1:] & V[:, :-1]]
    hc = int(np.ceil(HALF_W_VX / float(np.median(e))))
    zr = np.nanmedian(np.where(V, Z, np.nan), axis=1); rows_ = (zr >= W_Z[0]) & (zr <= W_Z[1])
    cols = np.abs(np.arange(V.shape[1]) - j) <= hc
    P = np.zeros_like(V); P[np.ix_(rows_, cols)] = True; P &= V
    share = float((np.abs(r[P] - seed_r) <= pitch).mean())
    got["seed_patch_share_within_1_pitch"] = round(share, 4)
    got["coded_gate_coverage"] = round(float(V[np.ix_(rows_, cols)].mean()), 4)
    got["verdict_by_judge_reading_of_step7"] = "KILL" if share < 0.70 else "coverage passes"
    print(f"seed patch: Judge's reading of step 7 (verdict finding 2): share within one pitch {share:.4f} (< 0.70 -> KILL); "
          f"prereg's literal coverage metric (the coded gate): {got['coded_gate_coverage']}")

    with open(DATA / "runner_job2_drift.json", encoding="utf-8") as fh:
        drift = json.load(fh)
    s2 = [d for d in drift if d["tag"].startswith("model_stage2_")]
    got["nearest_vx_end_of_stage2"] = s2[-1]["nearest_vertex_to_seed_vx"]
    thru2 = [d["nearest_vertex_to_seed_vx"] for d in drift if re.match(r"model_stage[0-2]_", d["tag"])]
    print(f"nearest vertex to seed per snapshot through stage 2 (derived, torch snapshots): {thru2} -> max {max(thru2)}")
    got["measured_max_vx_thru_stage2"] = max(thru2)
    got["max_vx_thru_stage2_within_35"] = max(thru2) <= 35.5      # "within ~35 voxels" (34.7 counts)
    got["measured_station_t_end_stage2"] = round(s2end["station_t"], 2)
    print("  note: from the model_stage1_000200 snapshot on it is 27.8, 27.8, 28.1 vx; the first three snapshots read"
          " 34.7 / 33.9 / 33.9 vx (snapshot tags count optimizer stages 0-3).")
    print(f"export (derived) {drift[-1]['nearest_vertex_to_seed_vx']} vx vs recomputed {got['nearest_vertex_to_seed_vx']} vx")

    ok = True
    for k, v in EXPECTED.items():
        gv = got[k]
        mt = abs(gv - v) <= TOL[k] if k in TOL else gv == v
        ok &= mt
        print(f"{'MATCH   ' if mt else 'MISMATCH'} {k}: got {gv} expected {v}")
    print("ALL MATCH" if ok else "SOME MISMATCH")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
