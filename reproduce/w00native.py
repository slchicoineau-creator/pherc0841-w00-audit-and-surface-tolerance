"""W00-NATIVE re-score (outline row 5; prereg standalone/preregs/w00_native_scan.md @ 60b819bd).

Re-applies the frozen verdict rule ([private path], function verdict(), @ 60b819bd) to the saved
per-cross A25 values. A25 itself needs the CT volumes (CPU, S3 download), so this script starts from the saved per-cross
rows (data/w00native/w00native_rows.csv = w00native_rows.json, local only, losslessly converted to CSV to stay < 1 MB).
The 187 um grid is recomputed from the native mesh's meta.json. The 14 um affine residual needs both full meshes (TIFF,
> 1 MB) and is NOT reproduced here (quoted from the prereg).
Usage: python reproduce/w00native.py   (exit 0 only if every compared number matches)
"""
import csv, json, math, sys
from pathlib import Path
import numpy as np
from scipy.stats import binomtest, spearmanr

D = Path(__file__).resolve().parent.parent / "data" / "w00native"

EXPECTED = {
    # PROPOSAL_truth.md @60b819bd line 158 (table: 0.10 | 0.10); checks/truth-audit/w00native_result.json "median_A25"
    "median_A25_copy": 0.100,
    "median_A25_native": 0.101,
    # PROPOSAL_truth.md line 168 ("raises the median from 0.10 to only 0.11 / 0.13"); w00native_result.json copy arm
    "median_A25_copy_+75um": 0.113,
    "median_A25_copy_-75um": 0.133,
    "median_A25_native_+75um": 0.120,   # w00native_result.json
    "median_A25_native_-75um": 0.139,   # w00native_result.json
    "n_both": 6479,                     # w00native_result.json "n_both"
    "median_D": 0.0,                    # PROPOSAL_truth.md line 161 ("median 0.00 (2 760 vs 2 939)")
    "D_pos": 2760,
    "D_neg": 2939,
    "share_gt_0p3_copy": 0.170,         # PROPOSAL_truth.md line 159 (17.0 %)
    "share_gt_0p3_native": 0.169,       # PROPOSAL_truth.md line 159 (16.9 %)
    "spearman_native_A25_vs_bend": 0.327,  # PROPOSAL_truth.md line 162 ("Spearman 0.33"); w00native_result.json
    "verdict": "G: the mesh itself (its 187 um grid) is the main cause",  # PROPOSAL_truth.md line 163
    "grid_um_rounded": 187,             # PROPOSAL_truth.md line 151 / prereg line 14 ("187 um")
}
NOT_REPRODUCED = {
    "affine_residual_median_um": "13.9 (standalone/preregs/w00_native_scan.md line 15; outline rounds to 14). Needs both full "
                                 "tifxyz meshes (> 1 MB TIFFs); not recomputed here.",
}

C, N = "copy", "native"


def load_rows():
    rows = []
    with open(D / "w00native_rows.csv", newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            f = lambda s: None if s == "" else float(s)
            rows.append({C: [f(r["copy_0"]), f(r["copy_p75"]), f(r["copy_m75"])],
                         N: [f(r["native_0"]), f(r["native_p75"]), f(r["native_m75"])],
                         "bend_deg": float("nan") if r["bend_deg"] == "" else float(r["bend_deg"])})
    return rows


def verdict(rows):
    # same rule as w00native.py verdict() @ 60b819bd
    ok = [r for r in rows if None not in r[C] and None not in r[N]]
    a = lambda arm, s: np.array([r[arm][s] for r in ok])
    med = {arm: [float(np.median(a(arm, s))) for s in range(3)] for arm in (C, N)}
    sens = {arm: med[arm][1] > med[arm][0] and med[arm][2] > med[arm][0] for arm in (C, N)}
    Dd = a(C, 0) - a(N, 0); pos, neg = int((Dd > 0).sum()), int((Dd < 0).sum())
    p = binomtest(pos, pos + neg, 0.5).pvalue if pos + neg else 1.0
    sh_c, sh_n = float(np.mean(a(C, 0) > 0.3)), float(np.mean(a(N, 0) > 0.3))
    if not all(sens.values()): v = "INCONCLUSIVE"
    elif np.median(Dd) >= 0.05 and p < 0.001 and sh_n <= sh_c / 2: v = "T: the transfer is a major cause"
    elif abs(np.median(Dd)) < 0.03 and sh_n >= 0.75 * sh_c: v = "G: the mesh itself (its 187 um grid) is the main cause"
    else: v = "MIXED"
    b = np.array([r["bend_deg"] for r in ok]); kb = ~np.isnan(b)
    rho = float(spearmanr(a(N, 0)[kb], b[kb])[0])
    return dict(n_both=len(ok), med=med, sens=sens, median_D=round(float(np.median(Dd)), 3), D_pos=pos, D_neg=neg, sign_p=p,
                sh_c=sh_c, sh_n=sh_n, rho=rho, verdict=v)


def main():
    rows = load_rows(); r = verdict(rows)
    with open(D / "mesh_N94_meta.json", encoding="utf-8") as fh: meta = json.load(fh)
    vox_um = 9.366                       # native scan 20250821151531-9.366um (prereg line 7-8)
    grid_um = vox_um / meta["scale"][0]  # tifxyz scale 0.05 -> one vertex every 20 voxels
    got = {
        "median_A25_copy": round(r["med"][C][0], 3), "median_A25_native": round(r["med"][N][0], 3),
        "median_A25_copy_+75um": round(r["med"][C][1], 3), "median_A25_copy_-75um": round(r["med"][C][2], 3),
        "median_A25_native_+75um": round(r["med"][N][1], 3), "median_A25_native_-75um": round(r["med"][N][2], 3),
        "n_both": r["n_both"], "median_D": r["median_D"], "D_pos": r["D_pos"], "D_neg": r["D_neg"],
        "share_gt_0p3_copy": round(r["sh_c"], 3), "share_gt_0p3_native": round(r["sh_n"], 3),
        "spearman_native_A25_vs_bend": round(r["rho"], 3), "verdict": r["verdict"], "grid_um_rounded": round(grid_um),
    }
    print(f"rows {len(rows)}, sensitivity gate {r['sens']}, sign-test p {r['sign_p']:.4g}, grid {grid_um:.2f} um")
    bad = 0
    for k, e in EXPECTED.items():
        g = got[k]; m = (g == e) if isinstance(e, str) else math.isclose(g, e, abs_tol=1e-9)
        bad += not m; print(f"{'MATCH   ' if m else 'MISMATCH'} {k}: got {g} expected {e}")
    for k, v in NOT_REPRODUCED.items(): print(f"NOT REPRODUCED {k}: {v}")
    print("W00-NATIVE:", "ALL MATCH" if not bad else f"{bad} MISMATCH")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
