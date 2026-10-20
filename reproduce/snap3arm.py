"""Row 6: REFINE-24 / MIDLINE / SHEETLINE vs w00, 3-arm blind rating by one rater (Sebastien).

Re-scores the two blind pages (h0: w00 | REFINE-24 | MIDLINE; h2: w00 | REFINE-24 | SHEETLINE) from the saved key and
ratings with the rule of standalone/preregs/snapping_midline.md ("paired Yes per cross, with exact McNemar tests";
"Can't tell" pairs left out), the same rule reused by standalone/preregs/snapping_sheetline.md.
Ported from [private path] score() (lines 234-247 at 60b819bd): first showings only, keyed by
(cross k, arm); repeats are checked against the first showing. Exact McNemar = two-sided binomial test on the
discordant pairs (scipy.stats.binomtest there; math.comb here, identical for p = 0.5).

Run: python reproduce/snap3arm.py   (stdlib only)
"""
import json, math, sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "snap3arm"

# Expected numbers (source: [private path] at 60b819bd, §8, and the saved result JSONs
# [private path] / midline3arm_result_h2_sheet.json)
EXPECTED = {
    "h0_crosses": 14,                    # PROPOSAL_truth.md:182 "14 fresh h0 crosses x 3 arms"
    "h0_w00_yes": 11,                    # PROPOSAL_truth.md:186 "w00 copy | 11 / 14"
    "h0_refine_yes": 9,                  # PROPOSAL_truth.md:187 "REFINE-24 | 9 / 14"
    "h0_midline_yes": 8,                 # PROPOSAL_truth.md:188 "MIDLINE | 8 / 14"
    "h0_midline_vs_w00_p": 0.25,         # PROPOSAL_truth.md:190 "worse on 3 crosses (McNemar p 0.25)"
    "h0_midline_vs_w00_discordant": (0, 3),
    "h0_refine_vs_w00_p": 0.5,           # PROPOSAL_truth.md:190 "REFINE-24 was worse on 2 (p 0.5)"
    "h0_refine_vs_w00_discordant": (0, 2),
    "h0_repeats_agree": "4/4",           # PROPOSAL_truth.md:182 "His repeats agreed 4/4"
    "h2_crosses": 15,                    # PROPOSAL_truth.md:209 "15 fresh h2 crosses"
    "h2_w00_yes": 9,                     # PROPOSAL_truth.md:214 "w00 | 9 / 15"
    "h2_refine_yes": 6,                  # PROPOSAL_truth.md:215 "REFINE-24 | 6 / 15"
    "h2_sheetline_yes": 6,               # PROPOSAL_truth.md:216 "SHEETLINE | 6 / 15"
    "h2_sheetline_vs_w00_p": 0.375,      # PROPOSAL_truth.md:218 "better at 1 cross, worse at 4 (p 0.375)"
    "h2_sheetline_vs_w00_discordant": (1, 4),
    "h2_refine_vs_w00_p": 0.375,         # midline3arm_result_h2_sheet.json refine_vs_w00 p 0.375 (not in §8 text)
    "h2_refine_vs_w00_discordant": (1, 4),
    "h2_repeats_agree": "4/4",           # PROPOSAL_truth.md:209-210 "repeats agreed 4/4"
    "w00_yes_both_crops": "20/29",       # outline row 5 "w00 stayed on the sheet at 20/29 (row 6)" = 11/14 + 9/15
    "any_arm_better": False,             # outline row 6 "not significant"; better = p < 0.05 and more Yes
}
# Outline row 6 quotes "McNemar p 0.25-0.5": the range over the four comparisons with w00 above (0.25, 0.5, 0.375, 0.375).
EXPECTED["mcnemar_p_range_vs_w00"] = "0.25-0.5"


def mcnemar_exact(b, c):
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    return min(1.0, 2.0 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)


def score(key_file, ratings_file, arm):
    with open(DATA / key_file, encoding="utf-8") as fh: key = json.load(fh)
    with open(DATA / ratings_file, encoding="utf-8") as fh: R = json.load(fh)["items"]
    first = [s for s in key["sites"] if not s["repeat"]]
    ans = {(s["k"], s["arm"]): R.get(s["id"], {}).get("choice") for s in first}
    ks = sorted({s["k"] for s in first})
    yes = {a: [ans.get((k, a)) == "Yes" for k in ks if ans.get((k, a)) in ("Yes", "No")] for a in ("w00", "refine", arm)}

    def mcn(a, b):
        pr = [(ans.get((k, a)), ans.get((k, b))) for k in ks
              if ans.get((k, a)) in ("Yes", "No") and ans.get((k, b)) in ("Yes", "No")]
        ab = sum(1 for x, y in pr if x == "Yes" and y == "No")
        ba = sum(1 for x, y in pr if x == "No" and y == "Yes")
        p = mcnemar_exact(ab, ba)
        return dict(pairs=len(pr), a_yes_b_no=ab, a_no_b_yes=ba, p=round(p, 4), a_better=bool(p < 0.05 and ab > ba))

    rep = [s for s in key["sites"] if s["repeat"]]
    agree = sum(1 for s in rep if R.get(s["id"], {}).get("choice")
                and R.get(s["id"], {}).get("choice") == ans.get((s["k"], s["arm"])))
    return dict(crosses=len(ks), yes={a: sum(v) for a, v in yes.items()}, n={a: len(v) for a, v in yes.items()},
                arm_vs_w00=mcn(arm, "w00"), refine_vs_w00=mcn("refine", "w00"), arm_vs_refine=mcn(arm, "refine"),
                repeats_agree=f"{agree}/{len(rep)}")


def main():
    h0 = score("h0_key.json", "h0_seb_ratings.json", "midline")
    h2 = score("h2_key.json", "h2_seb_ratings.json", "sheetline")
    got = {
        "h0_crosses": h0["crosses"], "h0_w00_yes": h0["yes"]["w00"], "h0_refine_yes": h0["yes"]["refine"],
        "h0_midline_yes": h0["yes"]["midline"],
        "h0_midline_vs_w00_p": h0["arm_vs_w00"]["p"],
        "h0_midline_vs_w00_discordant": (h0["arm_vs_w00"]["a_yes_b_no"], h0["arm_vs_w00"]["a_no_b_yes"]),
        "h0_refine_vs_w00_p": h0["refine_vs_w00"]["p"],
        "h0_refine_vs_w00_discordant": (h0["refine_vs_w00"]["a_yes_b_no"], h0["refine_vs_w00"]["a_no_b_yes"]),
        "h0_repeats_agree": h0["repeats_agree"],
        "h2_crosses": h2["crosses"], "h2_w00_yes": h2["yes"]["w00"], "h2_refine_yes": h2["yes"]["refine"],
        "h2_sheetline_yes": h2["yes"]["sheetline"],
        "h2_sheetline_vs_w00_p": h2["arm_vs_w00"]["p"],
        "h2_sheetline_vs_w00_discordant": (h2["arm_vs_w00"]["a_yes_b_no"], h2["arm_vs_w00"]["a_no_b_yes"]),
        "h2_refine_vs_w00_p": h2["refine_vs_w00"]["p"],
        "h2_refine_vs_w00_discordant": (h2["refine_vs_w00"]["a_yes_b_no"], h2["refine_vs_w00"]["a_no_b_yes"]),
        "h2_repeats_agree": h2["repeats_agree"],
        "w00_yes_both_crops": f"{h0['yes']['w00'] + h2['yes']['w00']}/{h0['n']['w00'] + h2['n']['w00']}",
        "any_arm_better": any(d[c]["a_better"] for d in (h0, h2) for c in ("arm_vs_w00", "refine_vs_w00", "arm_vs_refine")),
    }
    print("h0 (w00 | REFINE-24 | MIDLINE):", json.dumps(h0))
    print("h2 (w00 | REFINE-24 | SHEETLINE):", json.dumps(h2))
    ps = [got[k] for k in ("h0_midline_vs_w00_p", "h0_refine_vs_w00_p", "h2_sheetline_vs_w00_p", "h2_refine_vs_w00_p")]
    got["mcnemar_p_range_vs_w00"] = f"{min(ps):g}-{max(ps):g}"
    ok = True
    for k, v in EXPECTED.items():
        g = got[k]
        m = (abs(g - v) < 1e-9) if isinstance(v, float) else (g == v)
        ok &= m
        print(f"{'MATCH   ' if m else 'MISMATCH'} {k}: got {g} expected {v}")
    print("ALL MATCH" if ok else "SOME MISMATCH")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
