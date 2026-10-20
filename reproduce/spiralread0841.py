"""SPIRAL-READ-0841 re-score (outline: "Failures and limits", SPIRAL-READ-0841 bullet).

Ports the rater-class + outcome part and the order check of the Judge's independent re-score
([private path] at private commit `60b819bd`), written from
standalone/preregs/spiral_field.md + standalone/preregs/spiral_field_amend3.md (no guard on
Sebastien's page; VALID only if he calls every empty picture not rows).
NOT ported: the Judge's pixel key-check (decodes each page JPEG and matches it to the tile PNGs); it needs the pictures,
which this package does not carry. Its saved result (9/9 and 8/8 slots match) is in data/spiralread0841/judge_rescore_out.json.
Control exposure counts are RE-READ (not recounted) from the saved planner_exposure_out.json (committed) and stage0.json.
Both rating files are pinned to the sha prefixes the Runner recorded when it scored (ITEM L288).

Stdlib only. Paths are relative to this file. Exit 0 only if every number matches EXPECTED.
"""
import datetime
import hashlib
import json
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "spiralread0841"
ITEM = "[private path] @60b819bd"

EXPECTED = {
    # ITEM L296: "SPIRAL-NO-ROWS (one rater: Chris)"; checks/20261012-07-*/judge_rescore_out.json "outcome"
    "outcome": "SPIRAL-NO-ROWS (one rater: chris)",
    # ITEM L313-L314: Chris VALID; Sebastien VALID under amendment 3
    "rater_class": {"chris": "VALID", "seb": "VALID"},
    # ITEM L316: "Chris: strokes on A1 and A2; Sebastien: rows on A1 and A2"
    "arm_calls": {"chris": ("strokes", "strokes"), "seb": ("rows", "rows")},
    "arms_called_rows": {"chris": 0, "seb": 2},
    # ITEM L313-L314: control rows for both; 0 of 4 empty pictures rows for both; Chris's guard not rows
    "control_rows": {"chris": True, "seb": True},
    "empties_called_rows_of_4": {"chris": 0, "seb": 0},
    "chris_guard_not_rows": True,
    # amendment 3 / ITEM L302: no guard on Sebastien's page
    "seb_page_has_guard": False,
    # judge_rescore_out.json key_check n_pictures; order_check
    "n_pictures": {"chris": 9, "seb": 8},
    "rated_after_build": {"chris": True, "seb": True},
    # ITEM L288 (Runner, scored): "Chris's file ... byte-identical (sha 35d6ce58); Sebastien's is sha 9085638c"; ITEM L424
    "seb_sha8": "9085638c",
    "chris_sha8": "35d6ce58",
    # judge_rescore_out.json key_check: every saved all_match flag True (pixel key-check itself NOT reproduced here)
    "saved_key_check_all_match": {"chris": True, "seb": True},
    # planner_exposure_out.json totals (@60b819bd); ITEM L325 "6 earlier byte-identical showings";
    # outline "Chris had seen W's control 6 times and Sebastien once (+2 re-framed each)"
    "C_byte_identical_before": {"chris": 6, "seb": 1},
    "C_other_frame_before": {"chris": 2, "seb": 2},
}

fails = []


def check(name, got, exp):
    ok = got == exp
    print(f"{'OK      ' if ok else 'MISMATCH'} {name}: got {got!r}  expected {exp!r}")
    if not ok:
        fails.append(name)


key = json.loads((DATA / "spiralread_key.json").read_text(encoding="utf-8"))
iso = lambda s: datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))
EMPTIES = ["C_blank", "A1_blank", "A2_blank", "blank09"]
cls, calls, after, shas = {}, {}, {}, {}
for r in ("chris", "seb"):
    raw = (DATA / f"spiralread_{r}_ratings.json").read_bytes()
    shas[r] = hashlib.sha256(raw).hexdigest()
    rat = json.loads(raw)
    after[r] = iso(rat["when"]) > iso(key[r]["built"])
    c = {v["role"]: rat["answers"].get(sid) for sid, v in key[r]["images"].items()}
    calls[r] = c
    rows = lambda x: c.get(x) == "rows"
    nb = sum(rows(e) for e in EMPTIES)
    if any(v is None for v in c.values()) or not rows("calib") or not after[r]:
        k = "VOID"
    elif nb > 1:
        k = "INVALID"
    elif not rows("C_level"):
        k = "UNINFORMATIVE-C"
    elif r == "seb":      # amendment 3: no guard; exactly one empty called rows = lenient
        k = "VALID-LENIENT" if nb == 1 else "VALID"
    else:
        k = "VALID-LENIENT" if rows("guard") else "VALID"
    cls[r] = k

valid = [r for r, k in cls.items() if k.startswith("VALID")]
strict = [r for r in valid if cls[r] == "VALID"]
no = [r for r in valid if sum(calls[r].get(a) == "rows" for a in ("A1", "A2")) == 0]
if no:
    oc = "SPIRAL-NO-ROWS (" + ("both raters" if len(no) == 2 else "one rater: " + no[0]) + ")"
elif len(strict) == 2 and all(calls[r]["A1"] == "rows" for r in strict):
    oc = "SPIRAL-READS"
elif len(strict) == 2 and all(calls[r]["A2"] == "rows" for r in strict):
    oc = "SPIRAL-READS-WITH-PICK"
elif len(valid) == 2:
    oc = "SPLIT"
elif len(valid) == 1:
    oc = "INCONCLUSIVE"
else:
    oc = "UNINFORMATIVE"

check("outcome", oc, EXPECTED["outcome"])
check("rater_class", cls, EXPECTED["rater_class"])
check("arm_calls", {r: (calls[r]["A1"], calls[r]["A2"]) for r in calls}, EXPECTED["arm_calls"])
check("arms_called_rows", {r: sum(calls[r][a] == "rows" for a in ("A1", "A2")) for r in calls},
      EXPECTED["arms_called_rows"])
check("control_rows", {r: calls[r]["C_level"] == "rows" for r in calls}, EXPECTED["control_rows"])
check("empties_called_rows_of_4", {r: sum(calls[r][e] == "rows" for e in EMPTIES) for r in calls},
      EXPECTED["empties_called_rows_of_4"])
check("chris_guard_not_rows", calls["chris"]["guard"] != "rows", EXPECTED["chris_guard_not_rows"])
check("seb_page_has_guard", "guard" in calls["seb"], EXPECTED["seb_page_has_guard"])
check("n_pictures", {r: len(key[r]["images"]) for r in key}, EXPECTED["n_pictures"])
check("rated_after_build", after, EXPECTED["rated_after_build"])
check("seb_sha8", shas["seb"][:8], EXPECTED["seb_sha8"])
check("chris_sha8", shas["chris"][:8], EXPECTED["chris_sha8"])

exp = json.loads((DATA / "planner_exposure_out.json").read_text(encoding="utf-8"))["totals"]
check("C_byte_identical_before", {"chris": exp["chris"]["C_byte_identical"], "seb": exp["sebastien"]["C_byte_identical"]},
      EXPECTED["C_byte_identical_before"])
check("C_other_frame_before", {"chris": exp["chris"]["W_control_other_frame"],
                               "seb": exp["sebastien"]["W_control_other_frame"]}, EXPECTED["C_other_frame_before"])
st = json.loads((DATA / "stage0.json").read_text(encoding="utf-8"))
check("stage0 guard_counts chris C_byte_identical_showings", st["guard_counts"]["chris"]["C_byte_identical_showings"],
      EXPECTED["C_byte_identical_before"]["chris"])

jo = json.loads((DATA / "judge_rescore_out.json").read_text(encoding="utf-8"))
print("NOT REPRODUCED here: pixel key-check (needs the tiles); the Judge's saved all_match flags are RE-READ and asserted:")
check("saved_key_check_all_match", {r: jo["key_check"][r]["all_match"] for r in jo["key_check"]},
      EXPECTED["saved_key_check_all_match"])

print(f"\nSPIRAL-READ-0841: {'MATCH' if not fails else 'MISMATCH ' + ', '.join(fails)}  (source: {ITEM})")
sys.exit(1 if fails else 0)
