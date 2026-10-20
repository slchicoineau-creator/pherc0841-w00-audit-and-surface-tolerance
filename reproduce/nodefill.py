"""NODE-FILL-READ + NODE-FILL-REREAD re-score (outline row 2 holes sentences; row 8 'a 50 % holes picture ... is not a
usable guard'). Both tests are VOID; only their validity checks are reproduced here.

Rules ([private path] and [private path], outcome rule), as the loop Judges
re-implemented them (checks/20261008-18-node-fill-read-with-the/judge_rescore.py and
checks/20261010-04-node-fill-reread-with-th/judge_rescore.py @60b819bd):
  a rater is valid if all 6 scored pictures are answered, the L100 control is 'rows', the 50 % holes guard is NOT 'rows'
  and both wrong-order blanks (NF30, NF45) are not 'rows'; fewer than 2 valid raters -> VOID.
  NODE-FILL-READ's guard = a fresh 50 % holes layout (H50f); NODE-FILL-REREAD's guard = HUMAN-TOL's H50 picture itself.
Prints validity counts and guard counts only: NO arm call (NF30, NF45, BL45) is printed (both page keys are unreleased).
Inputs: ../data/nodefill/. Run: python reproduce/nodefill.py
"""
import hashlib, json, sys
from pathlib import Path

D = Path(__file__).resolve().parent.parent / "data" / "nodefill"
V1 = "[private path] @60b819bd"
V2 = "[private path] @60b819bd"

EXPECTED = {
    # NODE-FILL-READ: V1 L293 VOID (1 of 2 valid); V1 L298-300 one rater fails exactly the holes guard; sha prefixes
    "nf1_sha8_seb": "d42c180f", "nf1_sha8_chris": "1ea995fd",
    "nf1_valid_raters": "1/2", "nf1_guard_H50f_rows": "1/2", "nf1_L100_rows": "2/2",
    "nf1_verdict": "VOID",
    # NODE-FILL-REREAD: V2 L286 VOID (0 of 2 valid); V2 L291-293 each fails exactly the guard (H50 'rows'); L100 2/2;
    # blanks not rows 4/4; sha prefixes 3d76bcb8 / 01ce291f
    "nf2_sha8_seb": "3d76bcb8", "nf2_sha8_chris": "01ce291f",
    "nf2_valid_raters": "0/2", "nf2_guard_H50_rows": "2/2", "nf2_L100_rows": "2/2", "nf2_blanks_not_rows": "4/4",
    "nf2_validity_failures_per_rater": [1, 1],
    "nf2_verdict": "VOID",
    # V2 L296-298: the guard is HUMAN-TOL's H50 file (md5 49968cf2...), called not rows by both on HUMAN-TOL
    "nf2_guard_md5_8": "49968cf2",
    # [private path] pins the guard's full md5; both tile_hashes.json entries must equal it.
    # (tile_hashes.json was computed 2026-10-18 from the local PNGs, which are not shipped: a hash RE-READ, not recomputed.)
    "nf2_guard_md5_pin_prereg_L14": True,
    "nf2_guard_is_humantol_H50": True,
    "humantol_H50_not_rows": "2/2",
    # V2 L305-307: stability (same call on the first page's 6 scored pictures, BL45 excluded): Seb 6/6, Chris 4/6
    "stability_seb": "6/6", "stability_chris": "4/6",
    # outline row 2: "NODE-FILL-READ's (1 of 2, VOID)" fresh 50 % holes picture called rows by >= 1 rater
    "nf1_fresh_holes_rows_by_at_least_one": True,
    # outline row 2 "both raters called it rows on 10-10": 'when' stamps in US Central (UTC-5); V2 L318 Chris 01:47Z (= 10-10 CDT)
    "nf2_rated_seb_CDT": "2026-10-10", "nf2_rated_chris_CDT": "2026-10-10",
}

J = lambda n: json.loads((D / n).read_text(encoding="utf-8"))
sha8 = lambda n: hashlib.sha256((D / n).read_bytes()).hexdigest()[:8]
got = {}


def calls(ans, key):
    return {f"{m['surface']}_{m['kind']}": ans.get(t) for t, m in key.items()}


def validity(c, guard):
    fails = [p for p in ("NF30_level", "NF45_level", "L100_level", guard, "NF30_blank", "NF45_blank") if c.get(p) is None]
    fails += [] if c.get("L100_level") == "rows" else ["L100"]
    fails += [p for p in (guard, "NF30_blank", "NF45_blank") if c.get(p) == "rows"]
    return fails


# --- NODE-FILL-READ (first sitting)
k1 = J("nf_page_key.json")
c1, v1 = {}, 0
for w, f in (("seb", "nodefill_seb_ratings.json"), ("chris", "nodefill_chris_ratings.json")):
    got[f"nf1_sha8_{w}"] = sha8(f)
    c1[w] = calls(J(f)["answers"], k1)
    v1 += not validity(c1[w], "H50f_level")
got["nf1_valid_raters"] = f"{v1}/2"
got["nf1_guard_H50f_rows"] = f"{sum(c1[w]['H50f_level'] == 'rows' for w in c1)}/2"
got["nf1_L100_rows"] = f"{sum(c1[w]['L100_level'] == 'rows' for w in c1)}/2"
got["nf1_verdict"] = "VOID" if v1 < 2 else "not VOID"
got["nf1_fresh_holes_rows_by_at_least_one"] = any(c1[w]["H50f_level"] == "rows" for w in c1)

# --- NODE-FILL-REREAD (second sitting)
k2 = J("nodefill2_page_key.json")
c2, v2, nfail = {}, 0, []
for w, f in (("seb", "nodefill2_seb_ratings.json"), ("chris", "nodefill2_chris_ratings.json")):
    got[f"nf2_sha8_{w}"] = sha8(f)
    c2[w] = calls(J(f)["answers"], k2)
    fl = validity(c2[w], "H50_level")
    nfail.append(len(fl))
    v2 += not fl
got["nf2_valid_raters"] = f"{v2}/2"
got["nf2_guard_H50_rows"] = f"{sum(c2[w]['H50_level'] == 'rows' for w in c2)}/2"
got["nf2_L100_rows"] = f"{sum(c2[w]['L100_level'] == 'rows' for w in c2)}/2"
got["nf2_blanks_not_rows"] = f"{sum(c2[w][b] != 'rows' for w in c2 for b in ('NF30_blank', 'NF45_blank'))}/4"
got["nf2_validity_failures_per_rater"] = nfail
from datetime import datetime, timedelta
for w, f in (("seb", "nodefill2_seb_ratings.json"), ("chris", "nodefill2_chris_ratings.json")):
    got[f"nf2_rated_{w}_CDT"] = (datetime.fromisoformat(J(f)["when"].replace("Z", "+00:00")) - timedelta(hours=5)).date().isoformat()
got["nf2_verdict"] = "VOID" if v2 < 2 else "not VOID"

# the guard file = HUMAN-TOL's H50 (source path in the page key + hashes of the PNGs, images not copied)
g = [m for m in k2.values() if m["surface"] == "H50"][0]
th = J("tile_hashes.json")["tiles"]
got["nf2_guard_md5_8"] = th[g["file"]]["md5"][:8]
got["nf2_guard_is_humantol_H50"] = g["source"].endswith("tolholes/tiles/level_H50.png") and \
    th[g["file"]]["sha256"] == th[next(k for k in th if k.endswith("tolholes/tiles/level_H50.png"))]["sha256"]
PIN_MD5 = "49968cf29b3d540f27ff9babf6556223"     # [private path]
got["nf2_guard_md5_pin_prereg_L14"] = th[g["file"]]["md5"] == PIN_MD5 == th[next(k for k in th if k.endswith("tolholes/tiles/level_H50.png"))]["md5"]
hk = J("humantol_key.json")
h50 = [t for t, m in hk.items() if m.get("level") == "H50" and m["kind"] == "level"]
assert len(h50) == 1 and hk[h50[0]]["file"] == "tolholes/tiles/level_H50.png"
got["humantol_H50_not_rows"] = f"{sum(J(f)['answers'][h50[0]] != 'rows' for f in ('humantol_seb_ratings.json', 'humantol_chris_ratings.json'))}/2"

# stability across sittings (Judge-only descriptive line)
for w in ("seb", "chris"):
    first6 = [p for p in sorted(set(c1[w]) & set(c2[w])) if p != "BL45_level"]
    assert len(first6) == 6
    got[f"stability_{w}"] = f"{sum(c1[w][p] == c2[w][p] for p in first6)}/6"

# cross-check vs the Judges' saved count files
j1 = J("nf_judge_rescore_out_60b819bd.json")
assert j1["verdict"].startswith(got["nf1_verdict"]) and j1["seb"]["sha256_prefix"] == got["nf1_sha8_seb"]
j2 = J("nf2_judge_counts_60b819bd.json")
assert j2["verdict"] == got["nf2_verdict"] and j2["valid_raters"] == v2
assert j2["stability_same_call_of_6"] == {"seb": int(got["stability_seb"][0]), "partner": int(got["stability_chris"][0])}

bad = 0
print(f"NODE-FILL-READ / NODE-FILL-REREAD re-score (expected values from {V1} and {V2})")
for kk, e in EXPECTED.items():
    gg = got.get(kk)
    ok = gg == e
    bad += not ok
    print(f"  {'MATCH   ' if ok else 'MISMATCH'} {kk:38s} got={gg!r} expected={e!r}")
print("RESULT:", "ALL MATCH" if not bad else f"{bad} MISMATCH(ES)")
sys.exit(1 if bad else 0)
