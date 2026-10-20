"""Row 7: PHASE-SYM-ROW7 (standalone/preregs/reader_phase.md), reader-ratio phase dependence. Numbers only, no rater.

What this script can and cannot re-derive (CPU, no GPU, small files only):
  - CAN: the class rule and every summary number of the verdict from the saved 16 x 16 tile-phase pair table
    (psym_result.json "pairs": median r_H9 / r_T over the good windows, one value per (T phase, H9 phase) pair, 3 decimals),
    using the Judge's own re-derivation (checks/20261009-06-phase-sym-row7-from-lane/judge_rescore.py, lines 37-55 at
    60b819bd): class per pair (READER-LIMITED <= 0.60, MIXED in between, SURFACE-CANDIDATE >= 0.85), PHASE-DEPENDENT if any
    pair's class differs; T-phase effect = median over H9 phases of the range (ptp) over the 16 T phases, and vice versa.
  - CANNOT: the per-pair ratios themselves (they need the 2.4 um / 9.6 um ink PNG maps and team_ink.tif, images not shipped
    here). The Judge's independent window-level re-score of 5 pairs (judge_rescore.json, derived from the PNG maps) is
    asserted: for each pair, Judge value == job value == the value in the shipped pair table.
  - The earlier 0.508 (sorstrip_stage0a.json, SOR-STRIP Stage 0a) is SAVED-NOT-REPRODUCED: PHASE-SYM's own Stage 0b found
    the current venv gives 0.524 for it (item:196, item:223). EXPECTED keeps 0.508 because the README quotes it; the
    script only checks that the saved file says 0.508 (WORDING_FLAGS flag 6).

Run: python reproduce/phasesym.py   (stdlib only)
"""
import json, re, statistics, sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "phasesym"
TOL = 0.0015   # the verdict quotes 3-decimal values; the outline rounds them to 2 decimals (see notes below)

# Expected (item [private path] at 60b819bd)
EXPECTED = {
    "R2_n_pairs": 256,              # item:204 / judge_rescore.json R2_class_count n 256 ("16 x 16 tile phases")
    "R2_median": 0.426,             # item:204 "Median ratio 0.426" (outline: median 0.43)
    "R2_min": 0.268,                # item:204 "range 0.268-0.625" (outline: 0.27)
    "R2_max": 0.625,                # item:204 (outline: 0.62)
    "R2_outcome": "PHASE-DEPENDENT",  # item:204 "Primary (R2): PHASE-DEPENDENT"; item:213 Judge "PASS = PHASE-DEPENDENT"
    "R2_reader_limited_pairs": 253,  # item:211 Judge "253 of 256"
    "R2_T_phase_effect": 0.176,     # item:204 "T-PHASE-MATERIAL ... 0.176" (outline: 0.18)
    "R2_H9_phase_effect": 0.175,    # item:204 "the H9 phase effect is 0.175" (outline: 0.18)
    "R_n_pairs": 256,
    "R_median": 0.588,              # item:205 "Median 0.588, range 0.452-0.827" (outline: median 0.59)
    "R_min": 0.452,                 # item:205 (outline: 0.45)
    "R_max": 0.827,                 # item:205 (outline: 0.83)
    "R_outcome": "PHASE-DEPENDENT",  # item:205
    "R_T_phase_effect": 0.149,      # item:205 "T-PHASE-MATERIAL 0.149" (outline: 0.15)
    "R_H9_phase_effect": 0.215,     # item:205 "H9 phase effect 0.215" (outline: 0.22)
    "earlier_0508": 0.508,          # SAVED-NOT-REPRODUCED: re-read from sorstrip_stage0a.json; current venv gives 0.524 (item:196)
    # prereg L65-66 sub-answer: T-PHASE-MATERIAL if T effect > 0.10, T-PHASE-MINOR if <= 0.05 (item:204-205)
    "R2_T_label": "T-PHASE-MATERIAL", "R_T_label": "T-PHASE-MATERIAL",
    # prereg L60: VOID if > 4 of 16 T phases VOID; none were (psym_result.json void_T_phases)
    "R2_void_T_phases": 0, "R_void_T_phases": 0,
    # Judge's window-level re-score of 5 pairs: judge == job == shipped table, all 5
    "judge_5pairs_agree": 5,
}
BAR_LO, BAR_HI = 0.60, 0.85     # item:60 "READER-LIMITED <= 0.60, SURFACE-CANDIDATE >= 0.85, MIXED in between"


def cls(v):
    return "READER-LIMITED" if v <= BAR_LO else ("SURFACE-CANDIDATE" if v >= BAR_HI else "MIXED")


def ptp(xs):
    return max(xs) - min(xs)


def region(res, reg):
    pairs = res[reg]["pairs"]
    p = {tuple(map(int, re.findall(r"\d+", k))): v for k, v in pairs.items()}
    vals = list(pairs.values())
    classes = sorted({cls(v) for v in vals})
    tps = sorted({k[:2] for k in p}); hps = sorted({k[2:] for k in p})
    t_eff = statistics.median([ptp([p[t + h] for t in tps]) for h in hps])
    h_eff = statistics.median([ptp([p[t + h] for h in hps]) for t in tps])
    return {
        f"{reg}_n_pairs": len(vals), f"{reg}_median": statistics.median(vals), f"{reg}_min": min(vals), f"{reg}_max": max(vals),
        f"{reg}_outcome": "PHASE-DEPENDENT" if len(classes) > 1 else f"CLASS-STABLE ({classes[0]})",
        f"{reg}_reader_limited_pairs": sum(cls(v) == "READER-LIMITED" for v in vals),
        f"{reg}_T_phase_effect": t_eff, f"{reg}_H9_phase_effect": h_eff, f"{reg}_classes": classes,
        f"{reg}_n_T_phases": len(tps), f"{reg}_n_H9_phases": len(hps),
        f"{reg}_T_label": "T-PHASE-MATERIAL" if t_eff > 0.10 else ("T-PHASE-MINOR" if t_eff <= 0.05 else "reported"),
        f"{reg}_void_T_phases": len(res[reg]["void_T_phases"]),
    }


def main():
    with open(DATA / "psym_result.json", encoding="utf-8") as fh:
        res = json.load(fh)
    got = {}
    for reg in ("R2", "R"):
        got.update(region(res, reg))
    with open(DATA / "sorstrip_stage0a.json", encoding="utf-8") as fh:
        got["earlier_0508"] = json.load(fh)["primary"]["median_ratio"]
    for k in sorted(got):
        print(f"{k}: {got[k]}")
    print("NOTE: 0.508 is SAVED-NOT-REPRODUCED; the current venv re-run gives 0.524 (20 good windows vs 21; item:196, item:223).")
    with open(DATA / "judge_rescore.json", encoding="utf-8") as fh:
        jr = json.load(fh)
    print("Judge window-level re-score of 5 pairs (derived, needs the PNG maps):")
    agree = 0
    for k, v in jr.items():
        if isinstance(v, dict) and "median_ratio" in v:
            reg, pair = k.split(" ", 1)
            table = res[reg]["pairs"][pair]
            same = v["median_ratio"] == v["job"] == table
            agree += same
            print(f"  {k}: judge {v['median_ratio']} vs job {v['job']} vs table {table} {'same' if same else 'DIFFERENT'}")
    got["judge_5pairs_agree"] = agree
    from decimal import Decimal, ROUND_HALF_UP
    r2 = lambda x: str(Decimal(str(round(x, 3))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
    print(f"2-decimal wording (half-up from the 3-decimal values): R2 {r2(got['R2_min'])}-{r2(got['R2_max'])} "
          f"(median {r2(got['R2_median'])}); R {r2(got['R_min'])}-{r2(got['R_max'])} (median {r2(got['R_median'])}); "
          f"own phase 2.4 um {r2(EXPECTED['R2_T_phase_effect'])} / {r2(EXPECTED['R_T_phase_effect'])} vs 9.6 um "
          f"{r2(EXPECTED['R2_H9_phase_effect'])} / {r2(EXPECTED['R_H9_phase_effect'])} (R2 / R)")
    print("  note: the outline (and the job's own row7_wording) writes R2's max 0.625 as 0.62 but R's H9 effect 0.215 as 0.22;"
          " half-up gives 0.63 / 0.22. Cosmetic only.")
    ok = True
    for k, v in EXPECTED.items():
        g = got[k]
        if isinstance(v, float):
            m = abs(g - v) <= TOL
            note = "" if abs(g - v) < 1e-9 else f" (diff {g - v:+.4f}, rounding of the 3-decimal pair table)"
        else:
            m, note = g == v, ""
        ok &= m
        print(f"{'MATCH   ' if m else 'MISMATCH'} {k}: got {g if not isinstance(g, float) else round(g, 4)} expected {v}{note}")
    print("ALL MATCH" if ok else "SOME MISMATCH")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
