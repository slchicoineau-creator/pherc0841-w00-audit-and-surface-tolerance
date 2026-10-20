"""HUMAN-FLOOR re-score (outline row 8): is the agent reader or Sebastien the odd reader on the 18 HUMAN-TOL pictures?

Rule (standalone/preregs/human_vs_agent.md), as the loop Judge re-implemented it
([private path] @60b819bd):
  - binary call per picture: 'rows' vs anything else, for Sebastien (S), Chris (C) and the agent majority (A, >= 2 of 3);
  - agent calls: level/blank pictures from the tol20 / tol20b / tolholes agent results, the calibration pair from format20;
  - Chris valid = calibration rows and <= 1 of 9 blanks rows;
  - disc = pictures where S != A; k = # of disc where C sides with S; m = # of concordant pictures where C differs;
  - Chris not valid -> UNDECIDED (prereg L40-41, nothing else decided); else
    AGENTS-OFF if k >= 4 and m <= 1; SEB-OFF if k <= 1 and m <= 1; else HUMANS-NOISY (FAIL);
  - exact sign test on k of n = len(disc), one- and two-sided (prereg L45);
  - both ratings files pinned by sha256 (prefixes f81d3a3c / b647c0aa as in HUMAN-TOL V L266-267).
Counts only; never a per-picture call. Inputs: ../data/humanfloor/. Run: python reproduce/humanfloor.py
"""
import hashlib, json, sys
from math import comb
from pathlib import Path

D = Path(__file__).resolve().parent.parent / "data" / "humanfloor"
PINS = {"humantol_seb_ratings.json": "f81d3a3cbc05fde7ee448f872551587246383f90df9cfd422da299d9e4971ed9",
        "humantol_chris_ratings.json": "b647c0aa40c701f7d8313459b66fb2c7bff41f43a478c6a35a0f131f1ce1049e"}
V = "[private path] @60b819bd"

EXPECTED = {
    "chris_valid": True,                       # V L208-209 ("Chris valid, so not UNDECIDED")
    "n_disc_seb_vs_agents": 5,                 # V L218 (k = 3 of 5); outline row 8 "disagree on 5/18"
    "k": 3, "m": 0,                            # V L218: "k = 3 of 5, m = 0 of 13"
    "verdict": "HUMANS-NOISY",                 # V L208: FAIL = HUMANS-NOISY
    "sign_one_sided": 0.5,                     # V L218
    "sign_two_sided": 1.0,                     # prereg L45 names it; not quoted in V (computed: 2 x 0.5, capped at 1)
    "pins_ok": True,                           # both ratings files = the pinned sha256
    "kappa_seb_chris": 0.769,                  # V L218-219 (outline row 8 rounds to 0.77)
    "kappa_seb_chris_2dp": 0.77,               # outline row 8 "kappa 0.77"
    "kappa_seb_agents": 0.4, "kappa_chris_agents": 0.571,   # V L219
    "agree_seb_chris": 16, "agree_seb_agents": 13, "agree_chris_agents": 15,  # V L219; outline "16/18"
    # V L223-225: every disagreement with the agents is human 'rows' / agents not
    "seb_rows_agents_not": 5, "seb_not_agents_rows": 0,
    "chris_rows_agents_not": 3, "chris_not_agents_rows": 0,
    "rows_calls_seb": 8, "rows_calls_chris": 6, "rows_calls_agents": 3,       # V L223
}

J = lambda n: json.loads((D / n).read_text(encoding="utf-8"))
key = J("humantol_key.json")
seb = J("humantol_seb_ratings.json")["answers"]
chr_ = J("humantol_chris_ratings.json")["answers"]
per = {}
for d in ("tol20", "tol20b", "tolholes"):
    per.update(J(f"{d}_result.json")["per_level"])
f20 = J("format20_result.json")["answers"]


def agent(p):
    k = key[p]
    if k["kind"] in ("level", "blank"):
        c = [r["answers"][k["kind"]] for r in per[k["level"]]["readers"] if r["valid"]]
    elif k["kind"] == "calib":
        c = list(f20["calib/canon09_fwd/"].values())
    else:
        c = list(f20["blank09/canon09_rev/"].values())
    n = sum(x == "rows" for x in c)
    assert len(c) == 3 and 2 * n != len(c)
    return n >= 2


ids = sorted(key)
assert len(ids) == 18 and set(seb) == set(ids) == set(chr_)
S = {p: seb[p] == "rows" for p in ids}
C = {p: chr_[p] == "rows" for p in ids}
A = {p: agent(p) for p in ids}
kind = {p: key[p]["kind"] for p in ids}
cal = [C[p] for p in ids if kind[p] == "calib"]
bl = [C[p] for p in ids if kind[p] in ("blank", "blank09")]
valid = len(cal) == 1 and cal[0] and sum(bl) <= 1 and len(bl) == 9
disc = [p for p in ids if S[p] != A[p]]
conc = [p for p in ids if S[p] == A[p]]
k = sum(C[p] == S[p] for p in disc)
m = sum(C[p] != S[p] for p in conc)
v = "UNDECIDED" if not valid else "AGENTS-OFF" if k >= 4 and m <= 1 else "SEB-OFF" if k <= 1 and m <= 1 else "HUMANS-NOISY"


def kap(a, b):
    n = 18
    po = sum(a[p] == b[p] for p in ids) / n
    pa, pb = sum(a.values()) / n, sum(b.values()) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return (po - pe) / (1 - pe)


n = len(disc)
p_hi = sum(comb(n, i) for i in range(k, n + 1)) / 2 ** n          # P(K >= k), Chris sides with Seb by chance
p_lo = sum(comb(n, i) for i in range(0, k + 1)) / 2 ** n          # P(K <= k)
pins_bad = [f for f, h in PINS.items() if hashlib.sha256((D / f).read_bytes()).hexdigest() != h]
if pins_bad: print("sha256 pin mismatches:", pins_bad)
got = dict(chris_valid=valid, pins_ok=not pins_bad, sign_two_sided=min(1.0, 2 * min(p_hi, p_lo)), n_disc_seb_vs_agents=len(disc), k=k, m=m, verdict=v,
           sign_one_sided=p_hi,
           kappa_seb_chris=round(kap(S, C), 3), kappa_seb_chris_2dp=round(kap(S, C), 2),
           kappa_seb_agents=round(kap(S, A), 3), kappa_chris_agents=round(kap(C, A), 3),
           agree_seb_chris=sum(S[p] == C[p] for p in ids), agree_seb_agents=sum(S[p] == A[p] for p in ids),
           agree_chris_agents=sum(C[p] == A[p] for p in ids),
           seb_rows_agents_not=sum(S[p] and not A[p] for p in ids), seb_not_agents_rows=sum(A[p] and not S[p] for p in ids),
           chris_rows_agents_not=sum(C[p] and not A[p] for p in ids), chris_not_agents_rows=sum(A[p] and not C[p] for p in ids),
           rows_calls_seb=sum(S.values()), rows_calls_chris=sum(C.values()), rows_calls_agents=sum(A.values()))

bad = 0
print(f"HUMAN-FLOOR re-score (expected values from {V})")
for kk, e in EXPECTED.items():
    g = got.get(kk)
    ok = g == e
    bad += not ok
    print(f"  {'MATCH   ' if ok else 'MISMATCH'} {kk:24s} got={g!r} expected={e!r}")
print("RESULT:", "ALL MATCH" if not bad else f"{bad} MISMATCH(ES)")
sys.exit(1 if bad else 0)
