"""Recompute the numbers quoted for two computer-only results from their exported data.

reader_phase  (data/numbers/reader_phase.json)
    For one w00 surface patch of PHerc0841's known text, the 9.6 um reader's share of the 2.4 um reader's letter-shape
    signal: band-pass (difference-of-Gaussians) correlation with the organizers' 2.4 um ink prediction, window by window,
    median ratio r(9.6 um) / r(2.4 um) over good windows. The reference comes from the 2.4 um scan, so the measure favours
    the 2.4 um reader. Both readers' tile phases were moved (16 x 16 = 256 pairs per region). This script takes the 256
    stored ratios per region and applies the pre-registered class and outcome rules (preregs/reader_phase.md).

lasagna_fit   (data/numbers/lasagna_fit.json)
    One run of the organizers' shipped lasagna seed fit on PHerc0841 (9.366 um). This script re-derives the quoted numbers
    (distance from the seed in mm, windings inward, coverage share vs the 0.70 rule) from the exported measurements.

Run:  python numbers/reproduce_numbers.py      (exit 0 only if every number equals the Judge's re-score)
Needs numpy only. Paths are relative to this file.
"""
from decimal import Decimal, ROUND_HALF_UP
import json, re, sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data" / "numbers"

# Oracle: the Judge's independent re-score outputs (hard-coded; tests/test_numbers.py repeats them independently).
EXPECTED = {
    "reader_phase.R2.median": 0.426, "reader_phase.R2.min": 0.268, "reader_phase.R2.max": 0.625,
    "reader_phase.R2.n_le_0.60": 253, "reader_phase.R2.n_mixed": 3, "reader_phase.R2.n_surface": 0,
    "reader_phase.R2.T_phase_effect": 0.176, "reader_phase.R2.H9_phase_effect": 0.176,
    "reader_phase.R2.outcome": "PHASE-DEPENDENT", "reader_phase.R2.T_phase_class": "T-PHASE-MATERIAL",
    "reader_phase.R.median": 0.588, "reader_phase.R.min": 0.452, "reader_phase.R.max": 0.827,
    "reader_phase.R.n_le_0.60": 142, "reader_phase.R.n_mixed": 114, "reader_phase.R.n_surface": 0,
    "reader_phase.R.T_phase_effect": 0.149, "reader_phase.R.H9_phase_effect": 0.215,
    "reader_phase.R.outcome": "PHASE-DEPENDENT", "reader_phase.R.T_phase_class": "T-PHASE-MATERIAL",
    "reader_phase.headline": "R2: PHASE-DEPENDENT",
    "lasagna_fit.stage3_stop_step": 2459, "lasagna_fit.stage3_max_steps": 10000,
    "lasagna_fit.final_dist_vx": 369.3, "lasagna_fit.final_dist_mm": 3.46,
    "lasagna_fit.stage2_end_dist_vx": 28.1, "lasagna_fit.max_dist_through_stage2_vx": 34.7,
    "lasagna_fit.windings_inward_min": 11.5, "lasagna_fit.windings_inward_max": 12.7,
    "lasagna_fit.pitch_vx": 35.1, "lasagna_fit.coverage_share": 0.046,
    "lasagna_fit.self_snap_loss": (4.8e3, 486.5), "lasagna_fit.seed_anchor_loss": (7.1656, 0.0, 19.458),
    "lasagna_fit.coverage_rule": "KILL",
}


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def ratio_class(v):
    return "READER-LIMITED" if v <= 0.60 else ("SURFACE-CANDIDATE" if v >= 0.85 else "MIXED")


def phase_effects(pairs):
    """The Judge's definition: per-pair keys 'T<a>,<b>|H<c>,<d>'; ranges from the unrounded stored ratios."""
    p = {tuple(int(x) for x in re.findall(r"\d+", k)): float(v) for k, v in pairs.items()}
    tps = sorted({k[:2] for k in p}); hps = sorted({k[2:] for k in p})
    t_eff = float(np.median([np.ptp([p[t + h] for t in tps]) for h in hps]))
    h_eff = float(np.median([np.ptp([p[t + h] for h in hps]) for t in tps]))
    return round(t_eff, 3), round(h_eff, 3)


def reader_phase():
    d = load("reader_phase.json"); out = {}
    for reg in ("R2", "R"):
        r = d["regions"][reg]
        v = np.array(list(r["pairs"].values()), float)
        assert len(v) == 256, f"{reg}: expected 256 pairs, got {len(v)}"
        classes = {ratio_class(x) for x in v}
        n_void = len(r["void_T_phases"])
        if n_void > 4:
            outcome = "VOID"
        elif len(classes) == 1:
            outcome = "CLASS-STABLE " + classes.pop()
        else:
            outcome = "PHASE-DEPENDENT"
        t_eff, h_eff = phase_effects(r["pairs"])
        t_cls = "T-PHASE-MATERIAL" if t_eff > 0.10 else ("T-PHASE-MINOR" if t_eff <= 0.05 else f"T phase effect {t_eff}")
        k = f"reader_phase.{reg}."
        out.update({k + "median": round(float(np.median(v)), 3), k + "min": round(float(v.min()), 3),
                    k + "max": round(float(v.max()), 3), k + "n_le_0.60": int((v <= 0.60).sum()),
                    k + "n_mixed": int(((v > 0.60) & (v < 0.85)).sum()), k + "n_surface": int((v >= 0.85).sum()),
                    k + "T_phase_effect": t_eff, k + "H9_phase_effect": h_eff, k + "outcome": outcome,
                    k + "T_phase_class": t_cls})
    out["reader_phase.headline"] = "R2: " + out["reader_phase.R2.outcome"]
    return out


def lasagna_fit():
    d = load("lasagna_fit.json")["numbers"]; out = {}
    out["lasagna_fit.stage3_stop_step"] = d["stage3_stop_step"]["value"]
    out["lasagna_fit.stage3_max_steps"] = d["stage3_stop_step"]["of"]
    dist = d["final_nearest_vertex_to_seed_vx"]["value"]
    out["lasagna_fit.final_dist_vx"] = dist
    out["lasagna_fit.final_dist_mm"] = round(dist * 9.366 / 1000, 2)
    snaps = d["drift_per_snapshot"]["value"]
    st = [s for s in snaps if s["snapshot"].startswith(("model_stage0", "model_stage1", "model_stage2"))]
    out["lasagna_fit.stage2_end_dist_vx"] = [s for s in st if s["snapshot"].startswith("model_stage2")][-1]["nearest_vertex_to_seed_vx"]
    out["lasagna_fit.max_dist_through_stage2_vx"] = max(s["nearest_vertex_to_seed_vx"] for s in st)
    pitch = 329 / 9.366
    seed_r = d["seed_radius_vx"]["value"]
    wind = [round((seed_r - c) / pitch, 1) for c in d["seed_ray_crossings_radius_vx"]["value"]]
    out["lasagna_fit.windings_inward_min"] = min(wind); out["lasagna_fit.windings_inward_max"] = max(wind)
    out["lasagna_fit.pitch_vx"] = round(pitch, 1)
    cov = d["coverage_share_within_one_pitch"]["value"]
    out["lasagna_fit.coverage_share"] = round(cov, 3)
    out["lasagna_fit.self_snap_loss"] = (d["self_snap_loss"]["start"], d["self_snap_loss"]["end"])
    sa = d["seed_anchor_loss"]  # (end of stage 2, stage-3 start after the anchor term restarts, stage-3 stop)
    out["lasagna_fit.seed_anchor_loss"] = (sa["stage2_end"], sa["start"], sa["end"])
    out["lasagna_fit.coverage_rule"] = "KILL" if cov < load("lasagna_fit.json")["coverage_rule"]["threshold"] else "PASS"
    return out


def compute():
    out = reader_phase(); out.update(lasagna_fit()); return out


def main():
    got = compute(); bad = 0
    print(f"{'quantity':42s} {'reproduced':>22s} {'expected':>22s}  ok")
    for k, exp in EXPECTED.items():
        g = got[k]; ok = (g == exp) if not isinstance(exp, float) else abs(g - exp) < 1e-9
        bad += not ok
        print(f"{k:42s} {str(g):>22s} {str(exp):>22s}  {'OK' if ok else 'MISMATCH'}")
    def r2(x):  # half-up to 2 decimals, as the README rounds (0.625 -> 0.63; %.2f would print 0.62)
        return str(Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
    print("reader_phase: phase-dependent, R2 (fresh, headline) %s-%s (median %s); R (reported) %s-%s (median %s)" % tuple(
        r2(got[k]) for k in ("reader_phase.R2.min", "reader_phase.R2.max", "reader_phase.R2.median",
                             "reader_phase.R.min", "reader_phase.R.max", "reader_phase.R.median")))
    print("ALL OK" if not bad else f"{bad} MISMATCH(ES)")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
