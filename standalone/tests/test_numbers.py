"""Oracle tests for numbers/reproduce_numbers.py: every value is hard-coded from the Judge's independent re-score.

Run from the release root:  python -m pytest tests/test_numbers.py -q     or     python tests/test_numbers.py
"""
import importlib.util, json, re, sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
# numbers/ has no __init__.py on purpose (a package named "numbers" would shadow the standard library module)
_spec = importlib.util.spec_from_file_location("reproduce_numbers", ROOT / "numbers" / "reproduce_numbers.py")
rn = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(rn)
GOT = rn.compute()
RP = json.loads((ROOT / "data" / "numbers" / "reader_phase.json").read_text(encoding="utf-8"))
LF = json.loads((ROOT / "data" / "numbers" / "lasagna_fit.json").read_text(encoding="utf-8"))


def test_reader_phase_R2_headline():
    assert GOT["reader_phase.R2.median"] == 0.426
    assert (GOT["reader_phase.R2.min"], GOT["reader_phase.R2.max"]) == (0.268, 0.625)
    assert GOT["reader_phase.R2.n_le_0.60"] == 253 and GOT["reader_phase.R2.n_mixed"] == 3
    assert GOT["reader_phase.R2.n_surface"] == 0
    assert GOT["reader_phase.R2.outcome"] == "PHASE-DEPENDENT"
    assert GOT["reader_phase.headline"] == "R2: PHASE-DEPENDENT"


def test_reader_phase_R_reported():
    assert GOT["reader_phase.R.median"] == 0.588
    assert (GOT["reader_phase.R.min"], GOT["reader_phase.R.max"]) == (0.452, 0.827)
    assert (GOT["reader_phase.R.n_le_0.60"], GOT["reader_phase.R.n_mixed"], GOT["reader_phase.R.n_surface"]) == (142, 114, 0)
    assert GOT["reader_phase.R.outcome"] == "PHASE-DEPENDENT"


def test_reader_phase_effects_judge_definition():
    assert (GOT["reader_phase.R2.T_phase_effect"], GOT["reader_phase.R2.H9_phase_effect"]) == (0.176, 0.176)
    assert (GOT["reader_phase.R.T_phase_effect"], GOT["reader_phase.R.H9_phase_effect"]) == (0.149, 0.215)
    assert GOT["reader_phase.R2.T_phase_class"] == GOT["reader_phase.R.T_phase_class"] == "T-PHASE-MATERIAL"


def test_reader_phase_job_rounding_note():
    # the job's 0.175 for R2's H9 effect = median of ranges already rounded to 3 decimals (documented in the JSON)
    p = {tuple(int(x) for x in re.findall(r"\d+", k)): v for k, v in RP["regions"]["R2"]["pairs"].items()}
    tps = sorted({k[:2] for k in p}); hps = sorted({k[2:] for k in p})
    pre_rounded = [round(max(p[t + h] for h in hps) - min(p[t + h] for h in hps), 3) for t in tps]
    assert round(float(np.median(pre_rounded)), 3) == 0.175 == RP["regions"]["R2"]["job_reported"]["H9_phase_effect"]


def test_reader_phase_judge_pair_rescores_match_stored():
    # five pairs the Judge recomputed from the raw maps with an independent implementation
    expected = {"R2 T0,96|H40,40": 0.625, "R2 T32,64|H56,64": 0.268, "R2 T0,0|H40,40": 0.551,
                "R T0,0|H64,64": 0.646, "R T96,32|H48,56": 0.576}
    for key, val in expected.items():
        reg, pair = key.split(" ")
        assert RP["judge_independent_pair_rescores"][key]["median_ratio"] == val
        assert RP["regions"][reg]["pairs"][pair] == val


def test_reader_phase_controls():
    st = RP["stage0"]
    assert st["code_replay_earlier_single_phase"]["median_ratio"] == 0.508
    assert st["code_replay_earlier_single_phase"]["good_windows"] == 21
    assert st["reader_2um_repeatability"]["rerun2_vs_rerun1"]["identical"] is True
    assert st["crop_back_binding"]["T_96_32_vs_T_0_0"][:2] == [0, 0]
    assert st["crop_back_binding"]["H9_40_64_vs_H9_64_64"][:2] == [0, 0]
    for reg, (t, trev, h, hrev) in {"R2": (0.767, 0.202, 0.657, 0.046), "R": (0.832, 0.182, 0.78, -0.002)}.items():
        pl = RP["regions"][reg]["plumbing_registered_global_r"]
        assert (pl["T"], pl["T_rev"], pl["H9_registered"], pl["H9_rev_registered"]) == (t, trev, h, hrev)
        assert pl["pass"] is True
        assert RP["regions"][reg]["void_T_phases"] == []
    assert RP["regions"]["R2"]["ct_registration"]["shift_dy_dx"] == [-6, -9]
    assert RP["regions"]["R"]["ct_registration"]["shift_dy_dx"] == [-8, -8]


def test_lasagna_fit_numbers():
    assert (GOT["lasagna_fit.stage3_stop_step"], GOT["lasagna_fit.stage3_max_steps"]) == (2459, 10000)
    assert GOT["lasagna_fit.final_dist_vx"] == 369.3 and GOT["lasagna_fit.final_dist_mm"] == 3.46
    assert GOT["lasagna_fit.stage2_end_dist_vx"] == 28.1
    assert GOT["lasagna_fit.max_dist_through_stage2_vx"] == 34.7
    assert (GOT["lasagna_fit.windings_inward_min"], GOT["lasagna_fit.windings_inward_max"]) == (11.5, 12.7)
    assert GOT["lasagna_fit.pitch_vx"] == 35.1
    assert GOT["lasagna_fit.coverage_share"] == 0.046
    assert LF["numbers"]["coverage_share_within_one_pitch"]["value"] == 0.0456
    assert LF["numbers"]["coded_gate_share"]["value"] == 1.0
    assert GOT["lasagna_fit.self_snap_loss"] == (4.8e3, 486.5)
    # the anchor term restarts at stage 3: 7.17 at the end of stage 2, 0 at stage-3 start, 19.46 at the stop
    assert GOT["lasagna_fit.seed_anchor_loss"] == (7.1656, 0.0, 19.458)
    assert GOT["lasagna_fit.coverage_rule"] == "KILL"
    assert LF["coverage_rule"]["threshold"] == 0.70 and "< 0.70" in LF["coverage_rule"]["prereg_text"]


def test_lasagna_sources_labelled():
    n = LF["numbers"]
    assert n["stage3_stop_step"]["source"].startswith("judge verdict text")
    for k in ("self_snap_loss", "seed_anchor_loss"):
        assert n[k]["source"].startswith("fit log of the run")
    assert n["final_nearest_vertex_to_seed_mm"]["source"].startswith("derived")


def test_reproduce_numbers_main_exit_0():
    assert rn.main() == 0


if __name__ == "__main__":
    fails = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn(); print("PASS", name)
            except AssertionError as e:
                fails += 1; print("FAIL", name, e)
    sys.exit(1 if fails else 0)
