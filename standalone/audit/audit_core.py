"""Shared pieces of the w00 audit: file paths, the frozen agreement rule and its statistics, and the strip-plane trace of a
tifxyz surface. numpy + scipy only. Every path is relative to this file.

Coordinates: x, y, z voxel indices (level 0) of the public PHerc0841 2.403 um volume (20260319124803-2.403um-0.2m-77keV-masked.zarr).
Strip coordinates: s (mm) along the strip axis t, n (mm) along the strip normal n, from the frame origin o."""
import os, json
import numpy as np
from scipy.stats import binom, beta as betad

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data", "audit")
HUMAN = os.path.join(ROOT, "human_data", "audit")

UM_PER_VX = 2.403                       # level-0 voxel size of the 2.4 um volume
TOL_UM = 75.0                           # agreement tolerance along n
P_ON0 = 0.90                            # the "9 in 10" being tested
ALPHA = 0.05
BOOT, BOOT_SEED = 2000, 2026100901      # strip bootstrap (fixed seed: the printed upper bounds depend on it and on strip order)
KEYNOISE = (0.0, 0.065, 0.10)           # rater sheet-switch rates for the key-noise bracket
# trace rule (identical to the rule that produced data/audit/guidefree_strips.json)
BIN_MM, SLAB_VX, SEARCH_N_MM, UPSAMPLE = 0.02, 1.2, 3.0, 10


def load(path):
    with open(path, encoding="utf8") as fh:
        return json.load(fh)


def human_file(name):
    """path of a human-data file, or None when human_data/ has not been released."""
    p = os.path.join(HUMAN, name)
    return p if os.path.exists(p) else None


# ------------------------------------------------------------------ statistics
def cp(k, n, nd=4):
    """exact two-sided 95 % Clopper-Pearson interval of k / n."""
    if n == 0:
        return [None, None]
    lo = 0.0 if k == 0 else float(betad.ppf(0.025, k, n - k + 1))
    hi = 1.0 if k == n else float(betad.ppf(0.975, k + 1, n - k))
    return [round(lo, nd), round(hi, nd)]


def off_crit(n):
    """smallest OFF count with one-sided exact binomial p <= 0.05 against p_off = 0.10."""
    return next((x for x in range(n + 1) if binom.sf(x - 1, n, 1 - P_ON0) <= ALPHA), None)


def rule(per_strip, seed=BOOT_SEED):
    """per_strip: ordered {strip: (on, n)}; strips with n = 0 dropped. The frozen rule: AGREE-BELOW-9IN10 needs both
    (a) OFF >= the exact binomial critical count and (b) strip-bootstrap 95 % upper bound of the agreement rate < 0.90."""
    ps = {s: v for s, v in per_strip.items() if v[1] > 0}
    on = np.array([v[0] for v in ps.values()]); nn = np.array([v[1] for v in ps.values()])
    N, ON = int(nn.sum()), int(on.sum()); OFF = N - ON
    if N == 0:
        return dict(n=0, verdict="NO-DATA")
    crit = off_crit(N); p = float(binom.sf(OFF - 1, N, 1 - P_ON0)) if OFF > 0 else 1.0
    rng = np.random.default_rng(seed); idx = rng.integers(0, len(nn), size=(BOOT, len(nn)))
    rate = on[idx].sum(1) / nn[idx].sum(1); ub = float(np.quantile(rate, 0.95))
    legA = crit is not None and OFF >= crit; legB = ub < P_ON0
    return dict(n=N, on=ON, off=OFF, strips=len(nn), off_crit=crit, binom_p=p, leg_a=bool(legA), boot_ub95=round(ub, 4), leg_b=bool(legB),
                rate=round(ON / N, 4), cp95=cp(ON, N), verdict="AGREE-BELOW-9IN10" if (legA and legB) else "NOT-SHOWN-BELOW")


def score_rows(strips, marks, positions, tol_um=TOL_UM):
    """one row per scored station (k = 1..6 with a mark). positions[strip] = 7 surface n values (mm) or None.
    status: ON (|surface - mark| <= tol), OFF, or NO-SURFACE (no trace at that station)."""
    rows = []
    for s in strips:
        mk = marks[s["strip"]]; W = positions[s["strip"]]
        for k in range(1, 7):
            if mk[k] is None:
                continue
            r = dict(strip=s["strip"], set=s["set"], kind=s["kind"], k=k)
            if W[k] is None:
                r.update(status="NO-SURFACE")
            else:
                d = (W[k] - mk[k]) * 1000.0
                r.update(signed_um=d, abs_um=abs(d), status="ON" if abs(d) <= tol_um else "OFF")
            rows.append(r)
    return rows


def per_strip(rows, tol_um=TOL_UM):
    out = {}
    for r in rows:
        if r["status"] == "NO-SURFACE":
            continue
        a = out.setdefault(r["strip"], [0, 0]); a[0] += r["abs_um"] <= tol_um; a[1] += 1
    return {s: tuple(v) for s, v in out.items()}


def cant_tell(strips, marks):
    """stations 1..6 without a mark (can't tell, or a strip with no marking page)."""
    return sum(sum(1 for k in range(1, 7) if marks[s["strip"]][k] is None) for s in strips)


def keynoise(on, n):
    """agreement corrected for the rater's own sheet switches at rate e: min(1, rate / (1 - e))."""
    return {str(e): round(min(1.0, on / n / (1 - e)), 4) for e in KEYNOISE}


def summarize(strips, marks, positions, tol_um=TOL_UM):
    rows = score_rows(strips, marks, positions, tol_um); ps = per_strip(rows, tol_um); v = rule(ps)
    sc = [r for r in rows if r["status"] != "NO-SURFACE"]; off = [r for r in sc if r["abs_um"] > tol_um]
    ct = cant_tell(strips, marks)

    def sub(f):
        rr = [r for r in sc if f(r)]; k = sum(r["abs_um"] <= tol_um for r in rr); return (k, len(rr))
    out = dict(rule=v, rows=rows, no_surface=sum(r["status"] == "NO-SURFACE" for r in rows),
               by_kind={kd: sub(lambda r, kd=kd: r["kind"] == kd) for kd in sorted({r["kind"] for r in sc})},
               by_set={st: sub(lambda r, st=st: r["set"] == st) for st in sorted({r["set"] for r in sc})},
               off_75_150=sum(r["abs_um"] <= 150 for r in off), off_over150=sum(r["abs_um"] > 150 for r in off),
               on_at_150=sum(r["abs_um"] <= 150 for r in sc), cant_tell=ct,
               cant_as_off=rule({**ps, "_ct": (0, ct)}) if ct else None, cant_as_on=rule({**ps, "_ct": (ct, ct)}) if ct else None,
               keynoise=keynoise(v["on"], v["n"]) if v.get("n") else None)
    if v.get("verdict") == "AGREE-BELOW-9IN10":
        drops = {s: rule({t: x for t, x in ps.items() if t != s})["verdict"] for s in ps}
        out["loso_turned_off"] = sum(d != "AGREE-BELOW-9IN10" for d in drops.values())
    return out


# ------------------------------------------------------------------ tifxyz surfaces
def densify(X, Y, Z, V, up):
    """bilinear upsample of a vertex grid by `up`; returns points (H', W', 3) and validity (all 4 corners valid)."""
    H, W = X.shape
    r = np.arange(0, H - 1 + 1e-9, 1.0 / up); c = np.arange(0, W - 1 + 1e-9, 1.0 / up)
    R, C = np.meshgrid(r, c, indexing="ij")
    r0 = np.clip(np.floor(R).astype(int), 0, H - 2); c0 = np.clip(np.floor(C).astype(int), 0, W - 2)
    fr, fc = R - r0, C - c0
    ok = V[r0, c0] & V[r0 + 1, c0] & V[r0, c0 + 1] & V[r0 + 1, c0 + 1]
    bil = lambda G: G[r0, c0] * (1 - fr) * (1 - fc) + G[r0 + 1, c0] * fr * (1 - fc) + G[r0, c0 + 1] * (1 - fr) * fc + G[r0 + 1, c0 + 1] * fr * fc
    return np.stack([bil(X), bil(Y), bil(Z)], -1), ok


def frame_arrays(fr):
    return dict(o=np.array(fr["o_vx"], float), t=np.array(fr["t"], float), n=np.array(fr["n"], float), w=np.array(fr["w"], float), L=float(fr["L_mm"]))


def locate(S, V, f, grid_step_vx):
    """float grid position (row, col) where the line o + lambda * n crosses the surface, |lambda| <= 3.6 mm; if it crosses more than
    once, the crossing nearest to o along the line. Every valid bilinear cell with a corner within 2 grid steps of the line is solved
    exactly (Newton). S: (H, W, 3) vertices, V: validity. Returns None if the line does not cross the surface there."""
    lim = (SEARCH_N_MM + 0.6) * 1000 / UM_PER_VX
    d = S - f["o"]; lam = d @ f["n"]; perp = np.linalg.norm(d - lam[..., None] * f["n"], axis=-1)
    near = V & (np.abs(lam) <= lim + 2 * grid_step_vx) & (perp <= 2.0 * grid_step_vx)
    if not near.any():
        return None
    H, W = V.shape; cells = set()
    for i, j in zip(*np.nonzero(near)):
        for i0 in (i - 1, i):
            for j0 in (j - 1, j):
                if 0 <= i0 < H - 1 and 0 <= j0 < W - 1 and V[i0:i0 + 2, j0:j0 + 2].all():
                    cells.add((int(i0), int(j0)))
    best = None
    for i0, j0 in sorted(cells):
        a, b, c, e = S[i0, j0], S[i0 + 1, j0], S[i0, j0 + 1], S[i0 + 1, j0 + 1]
        x = np.array([0.5, 0.5, 0.0])                             # (fr, fc, lambda)
        for _ in range(50):
            fr_, fc_, lm = x
            P = a * (1 - fr_) * (1 - fc_) + b * fr_ * (1 - fc_) + c * (1 - fr_) * fc_ + e * fr_ * fc_
            F = P - (f["o"] + lm * f["n"])
            Jm = np.stack([(b - a) * (1 - fc_) + (e - c) * fc_, (c - a) * (1 - fr_) + (e - b) * fr_, -f["n"]], 1)
            try:
                dx = np.linalg.solve(Jm, -F)
            except np.linalg.LinAlgError:
                break
            x = x + dx
            if np.abs(dx).max() < 1e-13:
                break
        res = np.linalg.norm(a * (1 - x[0]) * (1 - x[1]) + b * x[0] * (1 - x[1]) + c * (1 - x[0]) * x[1] + e * x[0] * x[1] - (f["o"] + x[2] * f["n"]))
        if res < 1e-6 and abs(x[2]) <= lim and -1e-9 <= x[0] <= 1 + 1e-9 and -1e-9 <= x[1] <= 1 + 1e-9:
            cand = (abs(x[2]), i0 + x[0], j0 + x[1])
            if best is None or cand < best:
                best = cand
    return None if best is None else (best[1], best[2])


def strip_trace(S, V, f, grid_step_vx):
    """the surface's intersection with the strip plane: median n (mm) per 0.02 mm s-bin over [-L/2, L/2).
    Crop: a grid window around the located crossing (rows +-(3.6 mm), cols +-(L/2 + 0.6 mm) in grid steps), densified x10;
    points within 1.2 voxels of the plane and |n| <= 3 mm. Returns (bin centres, median n, spread) or None."""
    g = locate(S, V, f, grid_step_vx)
    if g is None:
        return None
    grid_mm = grid_step_vx * UM_PER_VX / 1000
    rr = int((SEARCH_N_MM + 0.6) / grid_mm) + 2; cc = int((f["L"] / 2 + 0.6) / grid_mm) + 2
    gr, gc = int(g[0]), int(g[1]); H, W = V.shape
    r0, r1 = max(gr - rr, 0), min(gr + rr + 2, H); c0, c1 = max(gc - cc, 0), min(gc + cc + 2, W)
    Q, ok = densify(S[r0:r1, c0:c1, 0], S[r0:r1, c0:c1, 1], S[r0:r1, c0:c1, 2], V[r0:r1, c0:c1], UPSAMPLE)
    d = Q[ok] - f["o"]
    k = np.abs(d @ f["w"]) <= SLAB_VX; s = d[k] @ f["t"] * UM_PER_VX / 1000; nn = d[k] @ f["n"] * UM_PER_VX / 1000
    k2 = np.abs(nn) <= SEARCH_N_MM; s, nn = s[k2], nn[k2]
    E = np.arange(-f["L"] / 2, f["L"] / 2 - 1e-9, BIN_MM); med = np.full(len(E), np.nan); spr = np.full(len(E), np.nan)
    b = np.floor((s - E[0]) / BIN_MM).astype(int); kk = (b >= 0) & (b < len(E))
    for i in np.unique(b[kk]):
        v = nn[kk][b[kk] == i]; med[i] = np.median(v); spr[i] = v.max() - v.min()
    return E + BIN_MM / 2, med, spr


def at_stations(trace, cols):
    """surface n at each station (np.interp across valid bins; None outside their range) and gap to the nearest valid bin."""
    if trace is None:
        return [None] * len(cols), [None] * len(cols)
    x, med, _ = trace; ok = ~np.isnan(med)
    if not ok.any():
        return [None] * len(cols), [None] * len(cols)
    xs, ms = x[ok], med[ok]
    val = [float(np.interp(c, xs, ms)) if xs.min() <= c <= xs.max() else None for c in cols]
    gap = [round(float(np.min(np.abs(xs - c))), 4) for c in cols]
    return val, gap


def read_tifxyz(d, affine=None):
    """organizers' tifxyz folder (x.tif, y.tif, z.tif, meta.json) -> S (H, W, 3) float64, V (valid = all three > 0), grid step (voxels).
    affine: optional 3x4 or 4x4 matrix mapping the surface's xyz into the 2.403 um volume's level-0 xyz."""
    import tifffile
    X, Y, Z = (tifffile.imread(os.path.join(d, a + ".tif")).astype(np.float64) for a in "xyz")
    V = (X > 0) & (Y > 0) & (Z > 0); S = np.stack([X, Y, Z], -1)
    if affine is not None:
        A = np.asarray(affine, float); S = np.where(V[..., None], S @ A[:3, :3].T + A[:3, 3], 0.0)
    step = None
    mp = os.path.join(d, "meta.json")
    if os.path.exists(mp):
        sc = load(mp).get("scale")
        if sc:
            step = round(1.0 / float(sc[0]), 4)
    if step is None:                                      # median spacing of valid neighbours along columns
        dv = np.linalg.norm(S[:, 1:] - S[:, :-1], axis=-1)[V[:, 1:] & V[:, :-1]]
        step = float(np.median(dv))
    if affine is not None:                                # grid step in target voxels
        dv = np.linalg.norm(S[:, 1:] - S[:, :-1], axis=-1)[V[:, 1:] & V[:, :-1]]
        step = float(np.median(dv))
    return S, V, step
