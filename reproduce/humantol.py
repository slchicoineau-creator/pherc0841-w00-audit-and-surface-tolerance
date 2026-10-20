"""HUMAN-TOL + HUMAN-TOL-SCORE re-score (outline row 2).

Scoring rule: standalone/preregs/partsheet_tolerance.md '## Scoring' + standalone/preregs/partsheet_tolerance_score.md, exactly as the
loop Judge re-implemented it ([private path] @60b819bd):
  - a rater is valid if the calibration picture is 'rows' and at most 1 of the 9 blanks is 'rows';
  - a level counts for a rater if he is valid, its level picture is 'rows' and its own wrong-order blank is not 'rows';
  - per level: 2 raters -> "reads for humans", 1 -> "split", 0 -> "does not read";
  - agents read a level if >= 2 of its 3 valid agent readers said 'rows' (tol20 / tol20b / tolholes result files);
  - branches: (i) H70 reads for humans; (ii:X) X in C70/L70 reads for humans and not for agents; (iii) none of H70/C70/L70 reads.
Prints per-level calls only (released 2026-10-07); never a per-rater call.
Inputs: ../data/humantol/ (local-only keys/ratings; see docs/manifest_A1.json). Run: python reproduce/humantol.py
"""
import hashlib, json, sys
from pathlib import Path

D = Path(__file__).resolve().parent.parent / "data" / "humantol"
V = "[private path] @60b819bd"

EXPECTED = {
    # V L266-267: "both sha prefixes match the prereg (f81d3a3c..., b647c0aa...)"; judge_rescore_out.txt L1-2 (12 hex)
    "sha12_seb": "f81d3a3cbc05",
    "sha12_chris": "b647c0aa40c7",
    # V L266-267: "both raters valid with 0 of 9 blanks rows"
    "valid_seb": True, "valid_chris": True, "blank_rows_seb": 0, "blank_rows_chris": 0,
    # V L313-316 (proposed BRIEF line) + judge_rescore_out.txt L5-12; outline row 2
    "call_L100": "reads for humans", "call_L85": "reads for humans", "call_L70": "reads for humans",
    "call_L55": "split", "call_C85": "reads for humans", "call_C70": "reads for humans",
    "call_H70": "split", "call_H50": "does not read",
    # V L268-269: agent rule -> "rows only on L100 and C85"
    "agents_read": ["C85", "L100"],
    # V L257 + L267: branches ['ii:C70', 'ii:L70'] -> PASS
    "branches": ["ii:C70", "ii:L70"],
    # The Judge's PASS label (V L257) is "pre-registered verdict obtained"; the preregs define no PASS/FAIL rule of their
    # own, so no verdict is computed here: the label is quoted, the branches above are what is reproduced.
    # tracked [private path] @60b819bd (written when Sebastien rated) = sha256 of his file
    "seb_sha_matches_tracked_file": True,
    # outline row 2 "(Sebastien 10-03, Chris 10-06)": 'when' stamps, US Central (UTC-5 in October);
    # tracked sha file says 'rated 2026-10-03T14:00Z'; HUMAN-FLOOR V L212: Chris's file when 2026-10-06T16:29:40Z
    "rated_seb_CDT": "2026-10-03", "rated_chris_CDT": "2026-10-06",
    # outline row 2: C70 "read at a -22-layer render offset, about -53 um" (tol20b/tiles.json C70.level.offset;
    # layer pitch ~2.40 um (48.1 um / 20 layers) from standalone/preregs/depth_s022814.md: 10 layers = 24.0 um, 20 = 48.1 um)
    "C70_offset_layers": -22,
    "C70_offset_um_rounded": -53,
    # every picture on the page answered, nothing else in the file, only the three page answers used (Judge audit)
    "answer_ids_equal_key_ids": {"seb": True, "chris": True},
    "answers_in_vocabulary": {"seb": True, "chris": True},
}

J = lambda n: json.loads((D / n).read_text(encoding="utf-8"))
key = J("humantol_key.json")
files = {"seb": "humantol_seb_ratings.json", "chris": "humantol_chris_ratings.json"}
R = {w: J(f)["answers"] for w, f in files.items()}
got = {}
VOCAB = {"rows", "strokes", "nothing"}
got["answer_ids_equal_key_ids"] = {w: set(a) == set(key) for w, a in R.items()}
got["answers_in_vocabulary"] = {w: all(v in VOCAB for v in a.values()) for w, a in R.items()}
for w, f in files.items():
    got[f"sha12_{w}"] = hashlib.sha256((D / f).read_bytes()).hexdigest()[:12]
# the tracked sha file written at Sebastien's rating time ([private path] @60b819bd)
seb_sha_full = (D / "seb_ratings_sha256.txt").read_text(encoding="utf-8").split()[0]
got["seb_sha_matches_tracked_file"] = hashlib.sha256((D / files["seb"]).read_bytes()).hexdigest() == seb_sha_full
from datetime import datetime, timedelta
cdt = lambda w: (datetime.fromisoformat(w.replace("Z", "+00:00")) - timedelta(hours=5)).date().isoformat()
for w, f in files.items():
    got[f"rated_{w}_CDT"] = cdt(J(f)["when"])

levels = sorted({k["level"] for k in key.values() if k["kind"] == "level"})
ids = lambda kind, L=None: [p for p, k in key.items() if k["kind"] == kind and (L is None or k["level"] == L)]
counts = {L: 0 for L in levels}
for w, a in R.items():
    cal = a[ids("calib")[0]]
    nb = sum(a[p] == "rows" for p in ids("blank") + ids("blank09"))
    valid = cal == "rows" and nb <= 1
    got[f"valid_{w}"], got[f"blank_rows_{w}"] = valid, nb
    for L in levels:
        counts[L] += int(valid and a[ids("blank", L)[0]] != "rows" and a[ids("level", L)[0]] == "rows")
call = {L: {2: "reads for humans", 1: "split", 0: "does not read"}[counts[L]] for L in levels}
for L in levels:
    got[f"call_{L}"] = call[L]

agent = {}
for d in ("tol20", "tol20b", "tolholes"):
    for L, v in J(f"{d}_result.json")["per_level"].items():
        agent[L] = sum(r["valid"] and r["answers"]["level"] == "rows" for r in v["readers"]) >= 2   # 2+ of 3 agents
got["agents_read"] = sorted(L for L in agent if agent[L])
rd = lambda L: call[L] == "reads for humans"
br = (["i"] if rd("H70") else []) + [f"ii:{L}" for L in ("C70", "L70") if rd(L) and not agent[L]]
if not any(rd(L) for L in ("H70", "C70", "L70")):
    br.append("iii")
got["branches"] = br

t = J("tol20b_tiles.json")
off = int(t["C70"]["level"]["offset"])
got["C70_offset_layers"] = off
got["C70_offset_um_rounded"] = round(off * 48.1 / 20)

bad = 0
print(f"HUMAN-TOL-SCORE re-score (expected values from {V})")
for k, e in EXPECTED.items():
    g = got.get(k)
    ok = g == e
    bad += not ok
    print(f"  {'MATCH   ' if ok else 'MISMATCH'} {k:30s} got={g!r} expected={e!r}")
print("RESULT:", "ALL MATCH" if not bad else f"{bad} MISMATCH(ES)")
sys.exit(1 if bad else 0)
