"""TRUSTED-P re-score (outline row 5; prereg standalone/preregs/w00_trusted_crosses.md @ 60b819bd; results PROPOSAL_truth.md §6).

One rater (Sebastien) rated 48 blind 2.4 um crosses (+4 repeats): does w00 (P) stay on one papyrus sheet?
Re-applies trustedP.py fit() @ 60b819bd (same threshold grid, stricter-first tie-break, same gate) to the saved page key
(data/trustedp/trustedP_key.json, local only) and ratings (data/trustedp/trustedP_seb_ratings.json, local only), and
recounts the No share per audit-suspicion third (can't-tells excluded from the denominator, as the outline prints it).
The "fresh h0/h2 crosses 20/29" in the outline is the w00 arm of the row-6 tests (REFINE-24/MIDLINE 11/14 on h0,
SHEETLINE 9/15 on h2; PROPOSAL_truth.md lines 186 and 214); it is NOT recomputed here (other tests' rating files).
Usage: python reproduce/trustedp.py   (exit 0 only if every compared number matches)
"""
import json, math, sys
from pathlib import Path
import numpy as np

D = Path(__file__).resolve().parent.parent / "data" / "trustedp"
TH_A = (0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.50); TH_B = (15, 20, 25, 30, 40, np.inf)   # trustedP.py line 35 (amendment 1)
THIRDS = {0: "clean", 1: "middle", 2: "suspect"}

EXPECTED = {
    # PROPOSAL_truth.md @60b819bd line 126: "13 Yes, 33 No, 2 Can't tell. The repeats agreed 3/4."
    "n_yes": 13, "n_no": 33, "n_cant": 2, "repeats_agree": "3/4",
    # outline row 5 "33 of 46"; PROPOSAL_truth.md line 127: "clean 7/15, middle 12/16, suspect 14/15"
    "no_of_decided": "33/46", "clean": "7/15", "middle": "12/16", "suspect": "14/15",
    # PROPOSAL_truth.md line 129 ("0.70 balanced accuracy, under the 0.80 gate"); checks/truth-audit/trustedP_fit.json
    "balanced_accuracy": 0.696, "tpr": 0.545, "tnr": 0.846, "thetaA": 0.1, "thetaB": 15, "gate": "FAIL",
}
NOT_REPRODUCED = {
    "fresh_h0_h2_w00_stayed": "20/29 = 11/14 (h0, PROPOSAL_truth.md line 186) + 9/15 (h2, line 214); row-6 tests "
                              "(REFINE-24/MIDLINE/SHEETLINE), re-scored by their own script, not here.",
}


def main():
    with open(D / "trustedP_key.json", encoding="utf-8") as fh: key = json.load(fh)
    with open(D / "trustedP_seb_ratings.json", encoding="utf-8") as fh: RF = json.load(fh)
    R = RF["items"]
    first = [s for s in key["sites"] if not s["repeat"]]; reps = [s for s in key["sites"] if s["repeat"]]
    ch = lambda s: R.get(s["id"], {}).get("choice")
    # fit() as in trustedP.py
    lab = [(s["A"], s["B"], ch(s)) for s in first if ch(s) in ("Yes", "No")]
    A = np.array([a for a, _, _ in lab]); B = np.array([b for _, b, _ in lab]); bad = np.array([c == "No" for _, _, c in lab])
    best = None
    for ta in TH_A:
        for tb in TH_B:
            pred = (A > ta) | (B > tb)
            tpr = float(np.mean(pred[bad])); tnr = float(np.mean(~pred[~bad])); ba = (tpr + tnr) / 2
            if best is None or ba > best[0] + 1e-12: best = (ba, ta, tb, tpr, tnr)
    agree = nrep = 0
    for s in reps:
        f = [x for x in first if x["k"] == s["k"]][0]; a1, a2 = ch(f), ch(s)
        if a1 and a2: nrep += 1; agree += int(a1 == a2)
    gate = best[0] >= 0.80 and int(bad.sum()) >= 8 and int((~bad).sum()) >= 8 and agree >= 3
    got = dict(n_yes=int((~bad).sum()), n_no=int(bad.sum()), n_cant=sum(1 for s in first if ch(s) == "Cant"),
               repeats_agree=f"{agree}/{nrep}", balanced_accuracy=round(best[0], 3), tpr=round(best[3], 3), tnr=round(best[4], 3),
               thetaA=best[1], thetaB=None if np.isinf(best[2]) else best[2], gate="PASS" if gate else "FAIL")
    got["no_of_decided"] = f"{got['n_no']}/{got['n_no'] + got['n_yes']}"
    for t, name in THIRDS.items():
        cs = [ch(s) for s in first if s["third"] == t]
        got[name] = f"{cs.count('No')}/{cs.count('No') + cs.count('Yes')}"
    print(f"sites {len(key['sites'])} (first {len(first)}, repeats {len(reps)}); rater {RF.get('rater')}")
    bad_n = 0
    for k, e in EXPECTED.items():
        g = got[k]; m = (g == e) if isinstance(e, str) else math.isclose(g, e, abs_tol=1e-9)
        bad_n += not m; print(f"{'MATCH   ' if m else 'MISMATCH'} {k}: got {g} expected {e}")
    for k, v in NOT_REPRODUCED.items(): print(f"NOT REPRODUCED {k}: {v}")
    print("TRUSTED-P:", "ALL MATCH" if not bad_n else f"{bad_n} MISMATCH")
    return 0 if not bad_n else 1


if __name__ == "__main__":
    sys.exit(main())
