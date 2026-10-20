"""RAW-READ-9H re-score (outline "Known-window ceiling" section; row 2's "Chris rejected the same H50 again on 10-08").

Rule (standalone/preregs/grown_field.md 'Outcome' + amendment 1), as the loop Judge re-implemented it
([private path] @60b819bd, cls() and combine()):
  - per rater: VOID if any answer is missing, or calibration / control not 'rows', or the grown tile's blank, the 0009B
    blank or the rater's guard is 'rows'; else GROWER-READS if the grown tile is 'rows', else GROWER-FAILS;
  - combine: Chris first (prereg order), then Sebastien.
Not portable (needs the page HTML + PNG tiles): the Judge's check that every page picture re-encodes to the page bytes;
the frozen row score RP (needs the tiles + rs20.py). RP values are RE-READ from the Judge's saved output (kind
'derived'), NOT recomputed; only their ratio is formed here.
Agent screen counts are recounted from the per-reader rows ('readers') of the screen's saved result r9_screen_result.json.
Rating order (prereg L72-73): Chris's 'when' must be later than his COPY-FIX-9 read page (copyfix_read_chris_ratings.json)
and his INSET-NEG page (stamp from the INSET-NEG Judge's saved output, insetneg_judge_rescore_out_60b819bd.txt).
Counts and labels only; never a guard identity. Inputs: ../data/rawread9h/. Run: python reproduce/rawread9h.py
"""
import json, re, sys
from datetime import datetime, timedelta
from pathlib import Path

D = Path(__file__).resolve().parent.parent / "data" / "rawread9h"
V = "[private path] @60b819bd"
ROLES = ("grown", "grown_blank", "ctrl", "calib", "blank09", "guard")

EXPECTED = {
    "cls_chris": "GROWER-READS", "cls_seb": "GROWER-READS",          # V L430
    "outcome": "GROWER-READS (two raters)",                          # V L415; outline ceiling section
    "matches_runner_outcome": True,                                  # V L430-431
    "agents_rows_grown": "0/5", "agents_rows_ctrl": "5/5",           # V L446; outline "agents rows 0 of 5 (control 5 of 5)"
    # RE-READ (derived; judge_rp_out.json @60b819bd), not recomputed: needs the tiles
    "RP_grown": 0.399, "RP_ctrl": 23.338,                            # V L443-444 (0.40 vs 23.3), judge_rp_out.json
    "RP_ratio": 0.017,                                               # V L444; outline "0.017 of the control's"
    # outline row 2: "Chris rejected the same H50 again on 10-08 (his RAW-READ-9H guard)": Chris's guard sha = HUMAN-TOL
    # tolholes/tiles/level_H50.png (V L417 "Chris's guard (H50)"), and his guard call was not 'rows' (his class is not VOID)
    "chris_guard_is_humantol_H50": True,
    "chris_guard_not_rows": True,
    "chris_rated": "2026-10-08",                                     # judge_rescore_out.json chris.when (CDT date)
    "chris_rated_after_copyfix_read_and_insetneg": True,             # prereg L72-73
}

J = lambda n: json.loads((D / n).read_text(encoding="utf-8"))


def cls(c):
    if any(c.get(r) not in ("rows", "strokes", "nothing") for r in ROLES):
        return "VOID"
    if c["calib"] != "rows" or c["ctrl"] != "rows" or c["grown_blank"] == "rows" or c["blank09"] == "rows" or c["guard"] == "rows":
        return "VOID"
    return "GROWER-READS" if c["grown"] == "rows" else "GROWER-FAILS"


def combine(ch, se):
    if ch == "VOID":
        return "VOID"
    if se in (None, "VOID"):
        return ch + " (one rater: Chris)"
    if ch == "GROWER-READS":
        return "GROWER-READS (two raters)" if se == "GROWER-READS" else "GROWER-READS (one rater: Chris); split"
    return "GROWER-FAILS (both raters)" if se == "GROWER-FAILS" else "GROWER-FAILS (one rater: Chris); Sebastien rows"


key = J("rawread9h_key.json")
got = {}
calls = {}
for who in ("chris", "seb"):
    rat = J(f"rawread9h_{who}_ratings.json")
    a = rat["answers"]
    c = {v["role"]: str(a.get(tid, "")).strip().lower() or None for tid, v in key[who]["images"].items()}
    assert sorted(c) == sorted(ROLES)
    calls[who] = c
    got[f"cls_{who}"] = cls(c)
    if who == "chris":
        chris_when = datetime.fromisoformat(rat["when"].replace("Z", "+00:00"))
        got["chris_rated"] = (chris_when - timedelta(hours=5)).date().isoformat()   # CDT (UTC-5), as humantol/nodefill
got["outcome"] = combine(got["cls_chris"], got["cls_seb"])
got["matches_runner_outcome"] = J("rawread9h_result.json")["outcome"].startswith(got["outcome"].split(";")[0])

scr = J("r9_screen_result.json")
for tag, part in (("grown", "raw"), ("ctrl", "ctrl")):
    rd = scr[part]["readers"]
    nv = sum(bool(r["valid"]) for r in rd)
    nr = sum(bool(r["valid"]) and r["level"] == "rows" for r in rd)
    got[f"agents_rows_{tag}"] = f"{nr}/{nv}"
    assert (nr, nv) == (scr[part]["rows"], scr[part]["valid"]), (part, nr, nv)   # recount == the screen's own totals

# rating order (prereg L72-73)
iso = lambda t: datetime.fromisoformat(t.replace("Z", "+00:00"))
cf_when = iso(J("copyfix_read_chris_ratings.json")["when"])
txt = (D / "insetneg_judge_rescore_out_60b819bd.txt").read_text(encoding="utf-8")
m = re.search(r"copyfix read when: (\S+) \| insetneg when: (\S+)", txt)
assert iso(m.group(1)) == cf_when, "INSET-NEG Judge's copyfix stamp differs from the copyfix ratings file"
got["chris_rated_after_copyfix_read_and_insetneg"] = chris_when > cf_when and chris_when > iso(m.group(2))

rp = J("judge_rp_out_60b819bd.json")
got["RP_grown"], got["RP_ctrl"] = rp["raw_level"]["RP"], rp["ctrl_level"]["RP"]
got["RP_ratio"] = round(got["RP_grown"] / got["RP_ctrl"], 3)   # ratio of two re-read numbers (not an independent check)

th = J("tile_hashes.json")["tiles"]
h50 = th[next(k for k in th if k.endswith("tolholes/tiles/level_H50.png"))]["sha256"]
chris_guard_sha = [v["sha"] for v in key["chris"]["images"].values() if v["role"] == "guard"][0]
got["chris_guard_is_humantol_H50"] = chris_guard_sha == h50
got["chris_guard_not_rows"] = calls["chris"]["guard"] != "rows"

bad = 0
print(f"RAW-READ-9H re-score (expected values from {V}); RP RE-READ from the Judge's saved output (not recomputed)")
for kk, e in EXPECTED.items():
    g = got.get(kk)
    ok = g == e
    bad += not ok
    print(f"  {'MATCH   ' if ok else 'MISMATCH'} {kk:28s} got={g!r} expected={e!r}")
print("RESULT:", "ALL MATCH" if not bad else f"{bad} MISMATCH(ES)")
sys.exit(1 if bad else 0)
