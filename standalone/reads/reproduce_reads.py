"""Reproduce the blind human-read verdicts: per-picture calls (human_data/reads) -> each pre-registered rule (read_rules.py) -> the
named verdict, plus the descriptive non-human numbers the write-up quotes (data/reads/*_numbers.json).

    python reads/reproduce_reads.py

Standard library only. When human_data/reads/<test>.json is missing, that test prints
`SKIPPED: human data not in this copy (<file>)`; the selftest and the data-only numbers still run.
`run()` returns {"ok": bool, "tests": {...}, "numbers": {...}} for a top-level reproduce script.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import read_rules as rules  # noqa: E402

REL = os.path.dirname(HERE)
HD = os.path.join(REL, "human_data", "reads")
DD = os.path.join(REL, "data", "reads")

TESTS = ("partsheet_tolerance", "human_vs_agent", "fullhop_w", "fullhop_s022814", "line_spacing", "depth_w", "depth_s022814",
         "spiral_field", "grown_field")

# the named verdict each Judge re-score obtained (the full oracle, with counts, is tests/test_reads.py)
EXPECTED_OUTCOME = {
    "partsheet_tolerance": "(ii):C70 + (ii):L70",
    "human_vs_agent": "HUMANS-NOISY",
    "fullhop_w": "FULL-HOP-FAILS",
    "fullhop_s022814": "FAILS-814",
    "line_spacing": "O2-READS",
    "depth_w": "WIDE-OUT",
    "depth_s022814": "CONFIRMED (WIDE-HOLDS, two raters)",
    "spiral_field": "SPIRAL-NO-ROWS (one rater: chris)",
    "grown_field": "GROWER-READS (two raters)",
}


def jload(*p):
    with open(os.path.join(*p), encoding="utf-8") as f:
        return json.load(f)


def human(test):
    p = os.path.join(HD, test + ".json")
    if not os.path.exists(p):
        return None, os.path.relpath(p, REL).replace(os.sep, "/")
    return jload(p), None


def calls_by_rater(h, page=None):
    out = {}
    for c in h["calls"]:
        if page is None or c["page"] == page:
            out.setdefault(c["rater"], {})[c["picture"]] = c["call"]
    return out


def facts(h):
    return {p["rater"]: p for p in h["pages"]}


def table(h, pictures=None):
    """per-picture call table: one line per picture, one column per rater (own pages shown per rater)."""
    raters = sorted({c["rater"] for c in h["calls"]})
    order, seen = [], set()
    for c in sorted(h["calls"], key=lambda c: (c["rater"] != raters[0], c["shown_position"])):
        if c["picture"] not in seen:
            seen.add(c["picture"]); order.append(c["picture"])
    cb = calls_by_rater(h)
    lines = ["    %-16s %s" % ("picture", "  ".join("%-10s" % r for r in raters))]
    for p in order:
        if pictures and p not in pictures:
            continue
        lines.append("    %-16s %s" % (p, "  ".join("%-10s" % (cb[r].get(p) or "-") for r in raters)))
    return "\n".join(lines)


def score(test):
    h, missing = human(test)
    if h is None:
        return dict(skipped=missing)
    jload(DD, test + "_design.json")   # the design must exist next to the human data
    cb = calls_by_rater(h)
    if test == "partsheet_tolerance":
        r = rules.partsheet_tolerance(cb, jload(DD, "agent_reads_partsheet_page.json")["pictures"])
    elif test == "human_vs_agent":
        f = facts(h)
        r = rules.human_vs_agent(cb, jload(DD, "agent_reads_partsheet_page.json")["pictures"],
                                 bool(f["chris"]["chris_rated_after_prereg_first_commit"]))
    elif test == "fullhop_w":
        r = rules.fullhop_w(cb, jload(DD, "fullhop_w_numbers.json"))
    elif test == "fullhop_s022814":
        r = rules.fullhop_s022814(cb, jload(DD, "fullhop_s022814_numbers.json"))
    elif test == "line_spacing":
        r = rules.line_spacing(cb)
    elif test == "depth_w":
        r = rules.depth_w(cb)
    elif test == "depth_s022814":
        r = rules.depth_s022814(cb)
    elif test == "spiral_field":
        r = rules.spiral_field(cb, facts(h))
    elif test == "grown_field":
        r = rules.grown_field(cb)
    else:
        raise KeyError(test)
    lv = h.get("judge", {}).get("loop_verdict_for_observed_outcome", {})
    r["loop_verdict"] = lv.get(r["outcome"], "n/a (the Judge's loop verdict is recorded only for the observed outcome)")
    r["judge"] = h.get("judge", {})
    r["_table"] = table(h)
    return r


def numbers():
    """Descriptive numbers from saved non-human outputs (no human data needed)."""
    out = {}
    fh = jload(DD, "fullhop_w_numbers.json")
    out["fullhop_w"] = {n: dict(hop_auc=fh["stage0b"][n]["auc_hop"], bar=fh["stage0b"][n]["bar_hop"],
                                margin=round(fh["stage0b"][n]["bar_hop"] - fh["stage0b"][n]["auc_hop"], 4),
                                blank=fh["stage0b"][n]["auc_blank_same_offset"], unmoved=fh["stage0b"][n]["auc_unmoved"],
                                unmoved_parent=fh["stage0b"][n]["auc_unmoved_rated_parent"],
                                moved_gt50_pixel_share=round(sum(b["frac_px"] for b in fh["stage0b"][n]["bands"].values()), 2),
                                offset_layers=fh["stage0b"][n]["picked_offset"]) for n in ("L70d", "C70d")}
    t8 = jload(DD, "fullhop_s022814_numbers.json")
    out["fullhop_s022814"] = dict(
        floor140=dict(hop_auc=t8["stage0b_f140"]["auc_hop"], bar=t8["stage0b_f140"]["bar_hop"], passed=t8["stage0b_f140"]["hop_ok"]),
        floor170=dict(hop_auc=t8["stage0b_f170"]["auc_hop"], blank=t8["stage0b_f170"]["auc_blank_same_px"], bar=t8["stage0b_f170"]["bar_hop"],
                      ctrl_same_px=t8["stage0b_f170"]["auc_ctrl_hop_px"], passed=t8["stage0b_f170"]["hop_ok"],
                      unmoved=t8["stage0b_f170"]["auc_unmoved"], unmoved_ctrl=t8["stage0b_f170"]["auc_unmoved_ctrl"]),
        moved_gt50_vertex_pct={n: round(100 * t8["surfaces"][n]["moved_gt50_vertex_frac"], 1) for n in ("L85_814", "L70_814", "L55_814")},
        median_move_um={n: t8["surfaces"][n]["moved_um_pct"]["p50"] for n in ("L85_814", "L70_814", "L55_814")},
        ctrl_map_auc=t8["stage0a_plumbing"]["auc_rev"])
    fw = jload(DD, "depth_s022814_numbers.json")
    out["depth_s022814"] = dict(r_vs_ctrl={k: fw["r_vs_ctrl_map"][k] for k in ("out24", "in24", "out48", "in48")},
                                label_auc={k: fw["label_auc_inked_order"][k] for k in ("out48", "out24", "ctrl", "in24", "in48")},
                                blank_auc=fw["label_auc_wrong_order_blanks"], astar_layers=fw["stage0"]["astar_layers"],
                                w10_ctrl_auc={k: v["ctrl_auc"] for k, v in fw["windows_10mm"].items()})
    gf = jload(DD, "grown_field_numbers.json")
    out["grown_field"] = dict(row_score_grown=round(gf["row_score"]["grown"]["RP"], 2), row_score_ctrl=round(gf["row_score"]["ctrl"]["RP"], 1),
                              row_score_grown_blank=gf["row_score"]["grown_blank"]["RP"], grown_over_ctrl=gf["grown_over_ctrl_RP"],
                              agents_rows_grown=f'{gf["agent_screen"]["grown"]["rows"]}/{gf["agent_screen"]["grown"]["valid"]}',
                              agents_rows_ctrl=f'{gf["agent_screen"]["ctrl"]["rows"]}/{gf["agent_screen"]["ctrl"]["valid"]}')
    return out


# oracle values of the descriptive numbers (copied from the saved outputs; checked with or without human data)
EXPECTED_NUMBERS = [
    ("fullhop_w L70d hop AUC / bar / margin / blank", lambda n: (n["fullhop_w"]["L70d"]["hop_auc"], n["fullhop_w"]["L70d"]["bar"],
                                                               n["fullhop_w"]["L70d"]["margin"], n["fullhop_w"]["L70d"]["blank"]), (0.5755, 0.5756, 0.0001, 0.5256)),
    ("fullhop_w C70d hop AUC / bar", lambda n: (round(n["fullhop_w"]["C70d"]["hop_auc"], 3), n["fullhop_w"]["C70d"]["bar"]), (0.611, 0.614)),
    ("fullhop_w moved > 50 um pixel share L70d / C70d", lambda n: (n["fullhop_w"]["L70d"]["moved_gt50_pixel_share"],
                                                                  n["fullhop_w"]["C70d"]["moved_gt50_pixel_share"]), (0.40, 0.39)),
    ("fullhop_s022814 floor 140 hop AUC / bar / passed", lambda n: tuple(n["fullhop_s022814"]["floor140"][k] for k in ("hop_auc", "bar", "passed")),
     (0.5765, 0.559, False)),
    ("fullhop_s022814 floor 170 hop AUC / blank / bar / passed", lambda n: tuple(n["fullhop_s022814"]["floor170"][k] for k in ("hop_auc", "blank", "bar", "passed")),
     (0.5033, 0.4945, 0.5445, True)),
    ("fullhop_s022814 moved > 50 um vertex %", lambda n: n["fullhop_s022814"]["moved_gt50_vertex_pct"], {"L85_814": 16.5, "L70_814": 32.2, "L55_814": 47.6}),
    ("depth_s022814 map r vs control", lambda n: n["depth_s022814"]["r_vs_ctrl"], {"out24": 0.868, "in24": 0.851, "out48": 0.689, "in48": 0.691}),
    ("depth_s022814 label AUC", lambda n: {k: round(v, 3) for k, v in n["depth_s022814"]["label_auc"].items()},
     {"out48": 0.776, "out24": 0.837, "ctrl": 0.868, "in24": 0.867, "in48": 0.821}),
    ("grown_field row score grown / ctrl / ratio", lambda n: (n["grown_field"]["row_score_grown"], n["grown_field"]["row_score_ctrl"],
                                                             n["grown_field"]["grown_over_ctrl"]), (0.40, 23.3, 0.017)),
    ("grown_field agent screen grown / ctrl", lambda n: (n["grown_field"]["agents_rows_grown"], n["grown_field"]["agents_rows_ctrl"]), ("0/5", "5/5")),
]


def check_numbers(nums):
    return [(name, got, want) for name, f, want in EXPECTED_NUMBERS for got in [f(nums)] if got != want]


def cross():
    """Cross-test descriptions quoted in the write-up (need human data)."""
    pt, m1 = human("partsheet_tolerance"); dw, m2 = human("depth_w")
    if pt is None or dw is None:
        return dict(skipped=m1 or m2)
    out = dict(surface_rows=rules.surface_rows_counts(calls_by_rater(pt), calls_by_rater(dw)))
    holes = {}
    for test, pic in (("partsheet_tolerance", "H50"), ("fullhop_w", "H50n"), ("fullhop_s022814", "H50_814")):
        h, _ = human(test)
        if h is not None:
            cb = calls_by_rater(h); holes[f"{test}:{pic}"] = sum(rules.is_rows(cb[r][pic]) for r in cb)
    out["holes50_rows_of_2"] = holes
    return out


def run(verbose=True):
    p = print if verbose else (lambda *a, **k: None)
    fails = rules.selftest()
    p("reads: rules selftest", "PASS" if not fails else f"FAIL {fails}")
    ok = not fails
    res = {}
    for t in TESTS:
        r = score(t); res[t] = r
        if "skipped" in r:
            p(f"\n[{t}] SKIPPED: human data not in this copy ({r['skipped']})"); continue
        p(f"\n[{t}]")
        p(r.pop("_table"))
        p(f"  verdict: {r['outcome']}   (loop verdict: {r['loop_verdict']})")
        if t == "partsheet_tolerance":
            p("  per level:", ", ".join(f"{k} {v}" for k, v in r["per_level"].items()))
        if t == "human_vs_agent" and "k" in r:
            p(f"  k {r['k']} of {r['n_discordant']}, m {r['m']} of {r['n_concordant']}; agree of 18 {r['agree_of_18']}; kappa {r['kappa']}")
        if t == "fullhop_s022814" and "descriptive_L85" in r:
            p("  descriptive:", r["descriptive_L85"])
        if t == "line_spacing":
            p("  O45:", r["secondary"])
        if t == "depth_w":
            p(f"  lines: outward >= {r['outward_line_um']} um, inward >= {r['inward_line_um']} um ({r['label']}); s214732 {r['s214732']}; "
              f"10 mm {r['unit10']}")
        if t == "depth_s022814":
            p(f"  1 cm2: {r['cm2']}; reader: {r['reader']}; edge +-48 um calls: {r['edge_calls']}")
        if t == "spiral_field":
            p(f"  classes {r['rater_class']}; arms called rows {r['arms_called_rows']}")
        ok &= r["outcome"] == EXPECTED_OUTCOME[t]
        if t == "line_spacing":
            ok &= r["secondary"] == "O45-FAILS (O45-SPLIT)"
    nums = numbers()
    bad = check_numbers(nums)
    ok &= not bad
    p("\n[descriptive numbers oracle]", "PASS (%d checks)" % len(EXPECTED_NUMBERS) if not bad else f"FAIL {bad}")
    p("\n[descriptive numbers, non-human]")
    for k, v in nums.items():
        p(f"  {k}: {json.dumps(v)}")
    cr = cross()
    p("\n[cross-test]", "SKIPPED: human data not in this copy (" + cr["skipped"] + ")" if "skipped" in cr else json.dumps(cr))
    p("\nreads:", "OK" if ok else "MISMATCH")
    return dict(ok=bool(ok), tests=res, numbers=nums, cross=cr)


if __name__ == "__main__":
    sys.exit(0 if run()["ok"] else 1)
