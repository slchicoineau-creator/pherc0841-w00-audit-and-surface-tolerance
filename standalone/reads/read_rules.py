"""Pre-registered decision rules of the blind human-read tests (standard library only).

Every rule below is the rule written in the test's pre-registration (and its amendments) BEFORE any rating existed, as the
independent Judge re-score applied it. Input format, for every test:

    calls  = {rater: {picture_label: "rows" | "strokes" | "nothing" | None}}
    design = the test's data/reads/<test>_design.json (mark-free), facts = per-rater page facts from human_data

"strokes" and "nothing" are both "not rows". Picture labels are the public labels in data/reads/<test>_design.json.
`selftest()` checks every rule on synthetic answers (no real data needed).
"""
from math import comb

ROWS = "rows"
ANSWERS = ("rows", "strokes", "nothing")


def is_rows(x):
    return x == ROWS


# ================================================================================================ partsheet_tolerance
PT_LEVELS = ("L100", "L85", "L70", "L55", "C85", "C70", "H70", "H50")


def pt_valid(c):
    """Valid rater: calibration = rows and at most 1 of the 9 blanks (8 level blanks + the calibration blank) = rows."""
    blanks = [c[f"{L}_blank"] for L in PT_LEVELS] + [c["calib_blank"]]
    return is_rows(c["calib"]) and sum(map(is_rows, blanks)) <= 1


def pt_level_calls(c):
    """Per level: 'rows' / 'not' / 'masked' (that level's own blank was called rows, so the call does not count)."""
    return {L: ("masked" if is_rows(c[f"{L}_blank"]) else ("rows" if is_rows(c[L]) else "not")) for L in PT_LEVELS}


def agents_read_levels(agent_pictures):
    """Agents' call per level (the screen's own rule): a level reads for agents if >= 2 of its valid readers said rows."""
    return {L: sum(map(is_rows, agent_pictures[L]["valid_reader_calls"])) >= 2 for L in PT_LEVELS}


def partsheet_tolerance(calls, agent_pictures):
    """Part-sheet tolerance, pre-registered 2026-10-02 (scoring fixed then; edge cases settled 2026-10-06 before scoring).

    Rule text: "Valid rater: calibration = 'rows' and at most 1 of the 9 blanks = 'rows'. A level's call counts only if that
    level's own blank is not 'rows' for that rater. Per level: 'reads for humans' if both valid raters say 'rows'; 'split' if one
    does; 'does not read' if neither. Decision: (i) H70 reads for humans -> holes at ~30 % are tolerable to human eyes;
    (ii) C70 or L70 reads for humans (and not for agents) -> the wrong-layer bar relaxes toward ~30 % for human reading;
    (iii) none of H70 / C70 / L70 reads -> the agents' bar stands for humans too: >= ~85 % on the right sheet."
    Edge cases: a masked call counts as not rows; 'split' fires neither (i) nor (ii) and counts as not reading for (iii);
    the agents' level call is ">= 2 of its valid readers said rows"; a level that reads for both humans and agents does not
    fire (ii) (literal reading) and is reported as a contradiction; (i) and (ii) can both fire. Stage 0 (d): both raters valid.
    """
    raters = sorted(calls)
    valid = {r: pt_valid(calls[r]) for r in raters}
    if len(raters) != 2 or not all(valid.values()):
        return dict(valid=valid, outcome="INCONCLUSIVE (Stage 0: a rater is invalid)", branches=[])
    lc = {r: pt_level_calls(calls[r]) for r in raters}
    per_level = {}
    for L in PT_LEVELS:
        k = sum(lc[r][L] == "rows" for r in raters)
        per_level[L] = {2: "reads for humans", 1: "split", 0: "does not read"}[k]
    agents = agents_read_levels(agent_pictures)
    reads = {L: per_level[L] == "reads for humans" for L in PT_LEVELS}
    branches, contra = [], []
    if reads["H70"]:
        branches.append("(i)")
    for L in ("C70", "L70"):
        if reads[L] and not agents[L]:
            branches.append("(ii):" + L)
        if reads[L] and agents[L]:
            contra.append(L)
    if not (reads["H70"] or reads["C70"] or reads["L70"]):
        branches.append("(iii)")
    return dict(valid=valid, masked={r: [L for L in PT_LEVELS if lc[r][L] == "masked"] for r in raters},
                per_level=per_level, agents_read=agents, branches=branches, contradiction_with_agent_record=contra,
                outcome=" + ".join(branches) if branches else "no branch fired (contradiction with the agent record)")


# ================================================================================================ human_vs_agent
def kappa(a, b):
    """Cohen's kappa for two binary call lists; None when the expected agreement is 1."""
    n = len(a); po = sum(x == y for x, y in zip(a, b)) / n
    pa, pb = sum(a) / n, sum(b) / n; pe = pa * pb + (1 - pa) * (1 - pb)
    return None if abs(1 - pe) < 1e-12 else round((po - pe) / (1 - pe), 3)


def sign_p(k, n):
    """Exact sign test, X ~ Bin(n, 1/2): one-sided P(X >= k) and two-sided."""
    if n == 0:
        return dict(one_sided=None, two_sided=None)
    up = sum(comb(n, i) for i in range(k, n + 1)) / 2 ** n
    lo = sum(comb(n, i) for i in range(0, k + 1)) / 2 ** n
    return dict(one_sided=round(up, 4), two_sided=round(min(1.0, 2 * min(up, lo)), 4))


def hva_verdict(k, m):
    """Gap-free table (bars written for 5 discordant / 13 concordant pictures)."""
    if k >= 4 and m <= 1:
        return "AGENTS-OFF"
    if k <= 1 and m <= 1:
        return "SEB-OFF"
    return "HUMANS-NOISY"


def human_vs_agent(calls, agent_pictures, chris_rated_after_prereg):
    """Human vs agent readers, pre-registered 2026-10-05 (before the second rater opened the page).

    Rule text: every call binary ("rows" vs not). Discordant set = the pictures where Sebastien and the agent majority differ.
    k = on the discordant pictures, how many times Chris sides with Sebastien; m = on the concordant pictures, how many times
    Chris differs from both. "Valid Chris first (the partsheet rule): calibration = rows and at most 1 of the 9 blanks = rows. If
    not valid -> UNDECIDED. AGENTS-OFF = k >= 4 of 5 and m <= 1 of 13. SEB-OFF = k <= 1 and m <= 1. HUMANS-NOISY = every other
    outcome." (prereg wording, with '=' for its colons) Agent majority = binary majority of the 3 valid agent readers of each exact tile. The partsheet blank mask is NOT
    applied. Stage 0 (e): 3 valid agent readers per picture, 0 ties, 5 disagreements with Sebastien, Sebastien valid, else
    INCONCLUSIVE. Stage 0 (g): Chris's file later than the prereg's first commit, else the numbers are descriptive only.
    Descriptive: exact sign test on k, Cohen's kappa per pair, agreement of 18, the same k / m on levels + calibration only.
    """
    ids = sorted(agent_pictures)
    S = {p: is_rows(calls["sebastien"][p]) for p in ids}
    Cc = {p: is_rows(calls["chris"][p]) for p in ids}
    nr = {p: sum(map(is_rows, agent_pictures[p]["valid_reader_calls"])) for p in ids}
    nv = {p: len(agent_pictures[p]["valid_reader_calls"]) for p in ids}
    A = {p: 2 * nr[p] > nv[p] for p in ids}
    kind = {p: ("calib" if p == "calib" else "calib_blank" if p == "calib_blank" else "blank" if p.endswith("_blank") else "level") for p in ids}

    def valid(X):
        cal = [X[p] for p in ids if kind[p] == "calib"]; bl = [X[p] for p in ids if kind[p] in ("blank", "calib_blank")]
        return len(cal) == 1 and len(bl) == 9 and cal[0] and sum(bl) <= 1

    disc = [p for p in ids if S[p] != A[p]]; conc = [p for p in ids if S[p] == A[p]]
    stage0 = (len(ids) == 18 and all(nv[p] == 3 for p in ids) and not any(2 * nr[p] == nv[p] for p in ids)
              and len(disc) == 5 and valid(S))
    out = dict(stage0_pass=stage0, n_pictures=len(ids), seb_valid=valid(S), chris_valid=valid(Cc),
               n_discordant=len(disc), n_concordant=len(conc))
    if not stage0:
        out["outcome"] = "INCONCLUSIVE (Stage 0)"; return out
    if not out["chris_valid"]:
        out["outcome"] = "UNDECIDED (Chris invalid by the partsheet rule; that is the finding)"; return out
    k = sum(Cc[p] == S[p] for p in disc); m = sum(Cc[p] != S[p] for p in conc)
    v = hva_verdict(k, m) if (len(disc), len(conc)) == (5, 13) else None
    out.update(k=k, m=m, verdict=v,
               outcome=v if chris_rated_after_prereg else f"DESCRIPTIVE ONLY (timing not shown to follow the prereg): would be {v}")
    out["sign_p"] = sign_p(k, len(disc))
    keep = [p for p in ids if kind[p] in ("level", "calib")]
    out["levels_only"] = dict(n_discordant=sum(S[p] != A[p] for p in keep), k=sum(Cc[p] == S[p] for p in keep if S[p] != A[p]),
                              n_concordant=sum(S[p] == A[p] for p in keep), m=sum(Cc[p] != S[p] for p in keep if S[p] == A[p]))
    L = lambda D: [D[p] for p in ids]
    out["kappa"] = dict(seb_chris=kappa(L(S), L(Cc)), seb_agents=kappa(L(S), L(A)), chris_agents=kappa(L(Cc), L(A)))
    out["agree_of_18"] = dict(seb_chris=sum(S[p] == Cc[p] for p in ids), seb_agents=sum(S[p] == A[p] for p in ids),
                              chris_agents=sum(Cc[p] == A[p] for p in ids))
    out["rows_calls_of_18"] = dict(seb=sum(S.values()), chris=sum(Cc.values()), agents=sum(A.values()))
    out["direction"] = dict(seb_rows_agents_not=sum(S[p] and not A[p] for p in ids), seb_not_agents_rows=sum(A[p] and not S[p] for p in ids),
                            chris_rows_agents_not=sum(Cc[p] and not A[p] for p in ids), chris_not_agents_rows=sum(A[p] and not Cc[p] for p in ids),
                            seb_rows_chris_not=sum(S[p] and not Cc[p] for p in ids), chris_rows_seb_not=sum(Cc[p] and not S[p] for p in ids))
    out["disagreements_by_kind"] = {nm: {kk: sum(1 for p in ids if f(p) and kind[p] == kk) for kk in ("level", "blank", "calib", "calib_blank")}
                                    for nm, f in (("seb_chris", lambda p: S[p] != Cc[p]), ("seb_agents", lambda p: S[p] != A[p]),
                                                  ("chris_agents", lambda p: Cc[p] != A[p]))}
    out["agent_majority"] = {p: A[p] for p in ids}
    return out


# ================================================================================================ fullhop_w
FH_PRIMARY = ("L70d", "C70d")
FH_GUARDS = ("L40d", "H50n")


def fh_valid(c):
    need = ("L70d", "C70d", "L40d", "H50n", "L100", "L70d_blank", "C70d_blank", "calib", "calib_blank")
    return (all(c.get(p) is not None for p in need) and is_rows(c["calib"]) and not is_rows(c["calib_blank"])
            and not is_rows(c["L70d_blank"]) and not is_rows(c["C70d_blank"]) and is_rows(c["L100"]))


def fullhop_w(calls, numbers=None):
    """Full-sheet hops on the known-text window, pre-registered 2026-10-08 (page amendment F2 before any page existed).

    Rule text: "Valid rater: every own picture answered; calib 'rows'; calibration blank, L70d blank and C70d blank each not
    'rows'; L100 'rows'. UNDECIDED if < 2 valid raters. FULL-HOP-FAILS: >= 1 valid rater calls L70d or C70d not 'rows'.
    FULL-HOP-HOLDS: both valid raters call 'rows' on both L70d and C70d, AND >= 1 valid rater calls L40d or H50n not 'rows'.
    UNDECIDED (lenient page): both say rows on both primaries and nobody calls a guard not rows. DARK-HOPS / INCONCLUSIVE
    'reader still reaches' / VOID: by Stage 0 (no page)." Pictures of the other test on a shared page never count (F2).
    """
    if numbers is not None:
        g = numbers["stage0_gates"]
        if not g["dark_hops"]["pass_"]:
            return dict(outcome="DARK-HOPS")
        if not g["stage0b_pass"]:
            return dict(outcome="INCONCLUSIVE (reader still reaches)")
        if not g["tiles_pass"]:
            return dict(outcome="VOID")
    valid = {r: fh_valid(c) for r, c in calls.items()}
    V = [r for r in calls if valid[r]]
    out = dict(valid=valid)
    if len(V) < 2:
        out["outcome"] = "UNDECIDED (fewer than 2 valid raters)"; return out
    fails_by = {r: [p for p in FH_PRIMARY if not is_rows(calls[r][p])] for r in V}
    out["fails_carried_by"] = fails_by
    if any(fails_by.values()):
        out["outcome"] = "FULL-HOP-FAILS"
    elif any(not is_rows(calls[r][g]) for r in V for g in FH_GUARDS):
        out["outcome"] = "FULL-HOP-HOLDS"
    else:
        out["outcome"] = "UNDECIDED (no guard picture called not rows: lenient page)"
    return out


# ================================================================================================ fullhop_s022814
T8_OWN = ("ctrl814", "L85_814", "L70_814", "L55_814", "H50_814", "ctrl814_blank", "L70_814_blank", "calib", "calib_blank")


def t8_valid(c):
    return (all(c.get(p) is not None for p in T8_OWN) and is_rows(c["calib"]) and not is_rows(c["calib_blank"])
            and not is_rows(c["ctrl814_blank"]) and not is_rows(c["L70_814_blank"]))


def fullhop_s022814(calls, numbers=None):
    """Full-sheet hops on the organizers' s022814 window, pre-registered 2026-10-08 (masked page bound 2026-10-11 before rating).

    Rule text: "Valid rater: every own picture of this test and the calibration pair answered; calib 'rows'; calibration blank, ctrl814 blank
    and L70_814 blank each not 'rows'. A valid rater who does not call ctrl814 'rows' is UNDECIDED for this window. UNDECIDED if
    < 2 valid raters. FAILS-814: >= 1 valid rater with ctrl814 'rows' calls L70_814 not 'rows'. HOLDS-814: both valid raters call
    ctrl814 and L70_814 'rows', AND >= 1 of them calls H50_814 or L55_814 not 'rows'. UNDECIDED: a rater's ctrl814 not rows (and no
    FAILS from the other); no 814 guard called not rows (lenient). L85_814 is descriptive: if FAILS-814 and both valid raters read
    L85_814 rows, write 'this window read with ~15 % deep hops, not ~30 %'." The line_spacing pictures (O2, O45) never count.
    Stage 0b: fails at floor 140 -> the pre-written 170 fallback once; fails again -> INCONCLUSIVE ('reader still reaches').
    """
    if numbers is not None:
        g = numbers["stage0_gates"]
        if not g["0b_f140"]["pass_"] and not g.get("0b_f170", {}).get("pass_", False):
            return dict(outcome="INCONCLUSIVE (reader still reaches)")
        floor = 140 if g["0b_f140"]["pass_"] else 170
        if not g[f"0d_f{floor}"]["pass_"]:
            return dict(outcome="DARK-HOPS")
    valid = {r: t8_valid(c) for r, c in calls.items()}
    V = [r for r in calls if valid[r]]
    W = [r for r in V if is_rows(calls[r]["ctrl814"])]
    out = dict(valid=valid, window_ok={r: r in W for r in calls})
    if len(V) < 2:
        out["outcome"] = "UNDECIDED (fewer than 2 valid raters)"; return out
    if any(not is_rows(calls[r]["L70_814"]) for r in W):
        out["outcome"] = "FAILS-814"
    elif len(W) < 2:
        out["outcome"] = "UNDECIDED (ctrl814 not rows for a rater: window too weak for him)"
    elif any(not is_rows(calls[r][g]) for r in W for g in ("H50_814", "L55_814")):
        out["outcome"] = "HOLDS-814"
    else:
        out["outcome"] = "UNDECIDED (no 814 guard called not rows: lenient on this window)"
    if out["outcome"] == "FAILS-814" and len(W) == 2 and all(is_rows(calls[r]["L85_814"]) for r in W):
        n55 = sum(is_rows(calls[r]["L55_814"]) for r in W)
        out["descriptive_L85"] = ("this window read with ~15 % deep hops, not ~30 %; the same raters read the heavier 45 % picture "
                                  f"rows for {n55} of 2")
    out["rows_count_of_2"] = {p: sum(is_rows(calls[r][p]) for r in calls) for p in ("ctrl814", "L85_814", "L70_814", "L55_814", "H50_814")}
    out["raters_rejecting_L70_but_reading_nested_L55"] = sum(not is_rows(calls[r]["L70_814"]) and is_rows(calls[r]["L55_814"]) for r in calls)
    return out


# ================================================================================================ line_spacing
def line_spacing(calls):
    """Line spacing with perfect lines, pre-registered 2026-10-11 (rules F3 / F4).

    Rule text: "F3, valid rater (= the s022814 hop test's rule): every fullhop_s022814, calibration and O picture answered; calib 'rows';
    the calibration blank, ctrl814 blank and L70_814 blank each not 'rows'. Let d = the valid raters who call ctrl814 'rows'.
    F4, per arm X in {O2 (primary), O45}: X-READS: both raters in d call X 'rows', AND at least one of them calls H50_814 or
    L55_814 not 'rows'. X-FAILS: at least one rater in d calls X not 'rows'. This decides whatever the guards say. Labels: X-NO if
    both, X-SPLIT if one of two, 'X-FAILS (one valid rater)' if d has one rater. X-LENIENT: both 'rows', but no 814 guard was
    called not rows -> undecided. X-VOID: d is empty. With one rater in d, that rater's 'rows' is a one-rater lead (undecided)."
    """
    valid = {r: (t8_valid(c) and c.get("O2") is not None and c.get("O45") is not None) for r, c in calls.items()}
    d = [r for r in calls if valid[r] and is_rows(calls[r]["ctrl814"])]
    arms = {}
    for x in ("O2", "O45"):
        nots = [r for r in d if not is_rows(calls[r][x])]
        if not d:
            v = f"{x}-VOID"
        elif nots:
            v = f"{x}-FAILS (one valid rater)" if len(d) == 1 else (f"{x}-FAILS ({x}-NO)" if len(nots) == 2 else f"{x}-FAILS ({x}-SPLIT)")
        elif len(d) == 1:
            v = f"{x}-UNDECIDED (one-rater lead: rows)"
        elif any(not is_rows(calls[r][g]) for r in d for g in ("H50_814", "L55_814")):
            v = f"{x}-READS"
        else:
            v = f"{x}-LENIENT (no 814 guard called not rows)"
        arms[x] = dict(verdict=v, n_d=len(d), rows=len(d) - len(nots),
                       guard_rejected_by=[r for r in d if any(not is_rows(calls[r][g]) for g in ("H50_814", "L55_814"))])
    return dict(valid=valid, d=d, arms=arms, outcome=arms["O2"]["verdict"], secondary=arms["O45"]["verdict"])


# ================================================================================================ depth_w
DW_OUT = ("out12", "out24")
DW_IN = ("in12", "in24")


def dw_rater(c, has10=True):
    """One rater of the depth_w page (20 mm block primary; s214732; 10 mm unit)."""
    surface_blanks = [p for p in c if p.endswith("_blank") and p != "calib_blank"]
    r = dict(missing=sorted(p for p, a in c.items() if a is None))
    r["blank_rows"] = sum(is_rows(c[p]) for p in surface_blanks); r["n_blanks"] = len(surface_blanks)
    r["valid"] = not r["missing"] and is_rows(c.get("calib")) and r["blank_rows"] <= 1
    cnt = lambda a: not is_rows(c.get(f"{a}_blank"))
    R = lambda a: cnt(a) and is_rows(c.get(a))
    U = lambda a: not cnt(a)
    if not r["valid"]:
        r["outcome20"] = "VOID (invalid rater)"; return r
    if U("ctrl") or not is_rows(c.get("ctrl")):
        r["outcome20"] = "VOID (control not read as rows)"; return r
    flags = []
    if R("out12") or R("out24"):
        out_line = 24 if R("out24") else 12
        if R("out24") and not R("out12"):
            flags.append("non-monotone outward (+24 rows, +12 not)")
        oc = "WIDE-OUT"
    elif U("out12") or U("out24"):
        out_line, oc = None, "INCOMPLETE"
    else:
        out_line, oc = 0, None
    if R("in24"):
        in_line = 24
        if not R("in12"):
            flags.append("non-monotone inward (-24 rows, -12 not)")
    elif U("in24"):
        in_line = None
    elif R("in12"):
        in_line = 12
    elif U("in12"):
        in_line = None
    else:
        in_line = 0
    if oc is None:
        oc = {24: "ASYMMETRIC", 12: "ASYMMETRIC-SHORT", 0: "NARROW", None: "INCOMPLETE"}[in_line]
    r.update(outcome20=oc, outward_line_um=out_line, inward_line_um=in_line, flags=flags)
    r["s214732"] = "UNCOUNTABLE" if U("s214732") else ("ROWS" if R("s214732") else "NOT ROWS")
    if has10:
        if is_rows(c.get("w10_P_blank")) or is_rows(c.get("w10_S_blank")):
            r["unit10"] = "UNCOUNTABLE"
        else:
            kP = sum(is_rows(c.get(f"w10_P_{p}")) for p in ("top", "mid", "bot"))
            kS = sum(is_rows(c.get(f"w10_S_{p}")) for p in ("top", "mid", "bot"))
            r["k10_P"], r["k10_S"] = kP, kS
            r["unit10"] = "1 cm2 USABLE" if kP >= 2 and kS == 0 else ("20 mm ONLY" if kP == 0 or kS >= kP else "DESCRIPTIVE")
    return r


def depth_w(calls):
    """Uniform depth shifts around w00 on the known-text window, pre-registered 2026-10-05 (+ amendment 1, same evening).

    Rule text: "Valid rater: all 22 answered; calibration = rows; at most 1 of the 8 surface blanks (6 at 20 mm, 2 at 10 mm) =
    rows. A level counts only if its own blank is not 'rows' (else uncountable). 20 mm block, per valid rater: VOID: ctrl not rows,
    or ctrl's blank rows, or invalid rater. Outward line = furthest + tile that reads rows (none / +12 / +24); inward line = furthest
    - tile that reads rows. A non-monotone pattern keeps the furthest tile and is flagged. WIDE-OUT: +12 or +24 reads rows; else
    INCOMPLETE if +12 or +24 is uncountable; else ASYMMETRIC: -24 rows; else ASYMMETRIC-SHORT: -12 rows, -24 not; else NARROW:
    +-12 both not rows (an uncountable inward tile needed for the call -> INCOMPLETE). Two valid raters: per side the stricter
    (narrower) line, both printed; the outcome name follows the combined lines; a rater whose call is INCOMPLETE is reported tile
    by tile and the combined call uses the other rater ('one rater'). s214732: rows / not rows per rater (uncountable if its blank
    reads rows); all countable valid raters not rows -> confirmed; all rows -> the agent-only line is removed; otherwise SPLIT.
    10 mm block: 1 cm2 USABLE if k_P >= 2 and k_S = 0; 20 mm ONLY if k_P = 0 or k_S >= k_P; otherwise DESCRIPTIVE; uncountable
    if either 10 mm blank reads rows; two raters: a named unit only if both agree."
    """
    rs = {r: dw_rater(c) for r, c in calls.items()}
    v = [x for x in rs.values() if not x["outcome20"].startswith("VOID")]
    full = [x for x in v if x["outcome20"] != "INCOMPLETE"]
    if not v:
        return dict(raters=rs, outcome="VOID (no valid rater)")
    if not full:
        return dict(raters=rs, outcome="INCOMPLETE (tile by tile, see raters)")
    o = min(x["outward_line_um"] for x in full)
    ins = [x["inward_line_um"] for x in full if x["inward_line_um"] is not None]   # a WIDE-OUT rater may have an uncountable inward tile
    i = min(ins) if ins else None
    if o > 0:
        oc = "WIDE-OUT"
    elif i is None:
        oc = "INCOMPLETE (inward tile uncountable)"
    else:
        oc = {24: "ASYMMETRIC", 12: "ASYMMETRIC-SHORT", 0: "NARROW"}[i]
    s = [x["s214732"] for x in v if x["s214732"] != "UNCOUNTABLE"]
    s214 = ("none countable" if not s else "NOT ROWS (confirmed: does not read)" if all(y == "NOT ROWS" for y in s)
            else "ROWS (the agent-only 'does not read' line is removed)" if all(y == "ROWS" for y in s) else "SPLIT")
    u = [x.get("unit10") for x in v if x.get("unit10") not in (None, "UNCOUNTABLE")]
    unit = "none countable" if not u else (u[0] if len(set(u)) == 1 and u[0] != "DESCRIPTIVE" else "DESCRIPTIVE / SPLIT")
    return dict(raters=rs, outcome=oc, outward_line_um=o, inward_line_um=i, label="one rater" if len(full) == 1 else "two raters",
                disagree=len({(x["outward_line_um"], x["inward_line_um"]) for x in full}) > 1, s214732=s214, unit10=unit)


# ================================================================================================ depth_s022814
def ds_rater(c):
    """One rater of the fresh-text depth page (own page; guards = that rater's own partsheet not-rows pictures)."""
    r = dict(missing=sorted(p for p, a in c.items() if a is None))
    blanks = [p for p in c if p.endswith("_blank") and p != "calib_blank"]
    r["blank_rows"] = sum(is_rows(c[p]) for p in blanks); r["n_blanks"] = len(blanks)
    g = [p for p in c if p.startswith("guard_")]
    r["guard_rows"] = sum(is_rows(c[p]) for p in g); r["n_guard"] = len(g)
    r["lenient"] = bool(g) and r["guard_rows"] * 2 > len(g)
    r["valid"] = not r["missing"] and is_rows(c.get("calib")) and r["blank_rows"] <= 1 and bool(g)
    cnt = lambda a: f"{a}_blank" not in c or not is_rows(c[f"{a}_blank"])
    if not r["valid"]:
        r["window"] = "VOID (invalid rater)"; return r
    if not cnt("ctrl"):
        r["window"] = "VOID (control blank read as rows)"; return r
    r["edge"] = {k: c[k] for k in ("in48", "out48") if k in c}
    if not is_rows(c["ctrl"]):
        r["window"] = "WINDOW-NO"; return r
    r["window"] = "WINDOW-YES"
    if not (cnt("in24") and cnt("out24")):
        r["depth"] = "INCOMPLETE"
    else:
        i, o = is_rows(c["in24"]), is_rows(c["out24"])
        r["depth"] = "WIDE-HOLDS" if i and o else "NARROW-OUT" if i else "NARROW-IN" if o else "NARROW-BOTH"
        if r["depth"] == "WIDE-HOLDS" and r["lenient"]:
            r["depth"] = "ALL-ROWS"
    r["reader"] = ("UNCOUNTABLE" if not cnt("H9") else ("H9-ROWS" if is_rows(c["H9"]) else "H9-NO-ROWS")) if "H9" in c else "H9 DROPPED"
    if "w10_top" in c:
        r["cm2"] = ("UNCOUNTABLE" if is_rows(c.get("w10_blank")) else
                    ("1CM-READS-PRIMED" if is_rows(c["w10_top"]) and is_rows(c["w10_bot"]) else "20MM-NEEDED"))
    else:
        r["cm2"] = "10 MM DROPPED"
    return r


def depth_s022814(calls):
    """Uniform depth shifts on fresh text (the organizers' s022814), pre-registered 2026-10-06.

    Rule text: "Valid rater: every picture answered, the calibration called rows, <= 1 of the surface blanks (ctrl, in24, out24,
    H9, 10 mm) called rows, and >= 1 guard on the page. Else VOID. A level counts only if its own blank is not rows. Window: ctrl
    blank rows -> VOID; WINDOW-YES = ctrl rows; WINDOW-NO = ctrl not rows. Depth (WINDOW-YES): an arm whose blank is rows is
    uncountable -> INCOMPLETE. Else WIDE-HOLDS = in24 and out24 rows; NARROW-OUT = in24 rows, out24 not; NARROW-IN = out24 rows,
    in24 not; NARROW-BOTH = neither. Guard: the rater is lenient if more than half of their guard pictures are called rows. A
    lenient rater's WIDE-HOLDS becomes ALL-ROWS. 1 cm2 (descriptive): 1CM-READS-PRIMED = both 10 mm windows rows; 20MM-NEEDED =
    fewer; UNCOUNTABLE if the 10 mm blank is rows. Edge +-48 um: descriptive calls only. Item verdict (two raters): CONFIRMED =
    WIDE-HOLDS from two valid raters (neither lenient); NARROWED: NARROW-X = the same NARROW label from two valid raters;
    WINDOW-NO = both valid raters WINDOW-NO; ONE RATER / SPLIT / ALL-ROWS / INCOMPLETE = reported per rater, no rewording;
    VOID = no valid rater." (The 9.6 um reader pair was dropped at Stage 0 by its alignment rule.)
    """
    rs = {r: ds_rater(c) for r, c in calls.items()}
    v = {k: x for k, x in rs.items() if not x["window"].startswith("VOID")}
    out = dict(raters=rs)
    if not v:
        out["outcome"] = "VOID (no valid rater)"; return out
    out.update(n_valid=len(v), label="two raters" if len(v) == 2 else "one rater")
    w = {x["window"] for x in v.values()}
    if w == {"WINDOW-NO"}:
        out["outcome"] = "WINDOW-NO" + ("" if len(v) == 2 else " (one rater)"); return out
    if w != {"WINDOW-YES"}:
        out["outcome"] = "SPLIT (window)"; return out
    d = {x["depth"] for x in v.values()}
    if len(v) == 2 and d == {"WIDE-HOLDS"}:
        out["outcome"] = "CONFIRMED (WIDE-HOLDS, two raters)"
    elif len(v) == 2 and len(d) == 1 and d <= {"NARROW-OUT", "NARROW-IN", "NARROW-BOTH"}:
        out["outcome"] = "NARROWED: " + next(iter(d)) + " (two raters, on a weaker surface)"
    elif len(v) == 1:
        out["outcome"] = "ONE RATER: " + next(iter(d)) + " (reported, no rewording)"
    else:
        out["outcome"] = "SPLIT / NOT DECIDED: " + " vs ".join(sorted(x["depth"] for x in v.values())) + " (reported, no rewording)"
    for k in ("reader", "cm2"):
        s = {x[k] for x in v.values()}
        out[k] = (next(iter(s)) if len(s) == 1 else "SPLIT") + " (" + out["label"] + ")"
    out["edge_calls"] = {r: x.get("edge", {}) for r, x in v.items()}
    return out


# ================================================================================================ spiral_field
def sp_rater_class(c, arms, noguard=False):
    rows = lambda p: is_rows(c.get(p))
    need = [x for a in arms for x in (a, f"{a}_blank")] + ["C", "C_blank", "calib", "calib_blank"] + ([] if noguard else ["guard"])
    if any(c.get(p) is None for p in need) or not rows("calib"):
        return "VOID"
    nb = sum(rows(b) for b in ["C_blank", "calib_blank"] + [f"{a}_blank" for a in arms])
    if nb > 1:
        return "INVALID"
    if not rows("C"):
        return "UNINFORMATIVE-C"
    if noguard:
        return "VALID-LENIENT" if nb == 1 else "VALID"
    return "VALID-LENIENT" if rows("guard") else "VALID"


def spiral_field(calls, facts, arms=("A1", "A2")):
    """One spiral-fit winding from one anchor point, pre-registered 2026-10-12 (+ amendment 3, 2026-10-13, before any rating).

    Rule text (per rater; strokes and nothing are both not rows): "VOID: a picture unanswered, calib not rows, or the answers'
    `when` earlier than the page build. INVALID: more than 1 of the blanks (C-blank, A1-blank, A2-blank, blank09) called rows.
    UNINFORMATIVE-C: C not rows. VALID, or VALID-LENIENT when the guard is called rows: a lenient rater's 'rows' calls do not count
    toward a READS outcome; his 'not rows' calls still count." Amendment 3 (Sebastien's page has no guard): "VALID only if he calls
    EVERY empty picture 'not rows'. Exactly one empty picture called rows = VALID-LENIENT; more than one = INVALID."
    "Outcome (first match wins): 1. SPIRAL-NO-ROWS: a valid (or valid-lenient) rater calls every shown arm not rows. One rater
    suffices; labelled '(one rater)' unless both. 2. SPIRAL-READS: both raters VALID (not lenient) and both call A1 rows.
    3. SPIRAL-READS-WITH-PICK: both VALID, A1 fails for at least one, both call A2 rows. 4. SPLIT: anything else with two valid
    raters. 5. INCONCLUSIVE: exactly one valid rater and no NO-ROWS. 6. UNINFORMATIVE: no valid rater."
    """
    cls = {}
    for r, c in calls.items():
        f = facts[r]
        k = sp_rater_class(c, arms, noguard=not f["has_guard"])
        if not f["rated_after_page_built"]:
            k = "VOID"
        cls[r] = k
    valid = [r for r in cls if cls[r] in ("VALID", "VALID-LENIENT")]
    strict = [r for r in valid if cls[r] == "VALID"]
    no = [r for r in valid if all(not is_rows(calls[r].get(a)) for a in arms)]
    if no:
        oc = "SPIRAL-NO-ROWS (" + ("both raters" if len(no) == 2 else "one rater: " + no[0]) + ")"
    elif len(strict) == 2 and all(is_rows(calls[r].get("A1")) for r in strict):
        oc = "SPIRAL-READS (raters know the field)"
    elif len(strict) == 2 and "A2" in arms and all(is_rows(calls[r].get("A2")) for r in strict):
        oc = "SPIRAL-READS-WITH-PICK (best of two; kept apart from the main claim)"
    elif len(valid) == 2:
        oc = "SPLIT (no claim)"
    elif len(valid) == 1:
        oc = "INCONCLUSIVE (one valid rater, rows on an arm: no claim)"
    else:
        oc = "UNINFORMATIVE (no valid rater)"
    return dict(rater_class=cls, arms_called_rows={r: sum(is_rows(calls[r].get(a)) for a in arms) for r in calls},
                empties_called_rows={r: sum(is_rows(calls[r].get(b)) for b in ["C_blank", "calib_blank"] + [f"{a}_blank" for a in arms]) for r in calls},
                outcome=oc)


# ================================================================================================ grown_field
GF_ROLES = ("grown", "grown_blank", "ctrl", "calib", "calib_blank", "guard")


def gf_class(c):
    if any(c.get(p) is None for p in GF_ROLES) or not is_rows(c["calib"]) or not is_rows(c["ctrl"]):
        return "VOID (a picture unanswered, or the calibration or the w00 control not called rows)"
    if is_rows(c["grown_blank"]) or is_rows(c["calib_blank"]):
        return "VOID (a wrong-order blank called rows)"
    if is_rows(c["guard"]):
        return "VOID (the not-rows guard called rows)"
    return "GROWER-READS" if is_rows(c["grown"]) else "GROWER-FAILS"


def grown_field(calls):
    """Uncorrected grown field on the regular 9.366 um scan, pre-registered 2026-10-07 (+ amendment 1 for Sebastien's read-2 guard).

    Rule text: "Per rater: VOID if a picture is unanswered, the calibration or the w00 control is not called rows, a wrong-order
    blank (grown_blank or blank09) is called rows, or the guard is called rows. Else GROWER-READS if the grown tile is called
    rows, GROWER-FAILS otherwise. The result's class is Chris's: Chris VOID -> VOID. Chris GROWER-READS + Sebastien GROWER-READS
    -> GROWER-READS (two raters). Chris GROWER-READS + Sebastien not rows -> GROWER-READS (one rater: Chris), reported as a split.
    Chris GROWER-FAILS + Sebastien rows -> stays GROWER-FAILS (one rater: Chris). Chris GROWER-FAILS + Sebastien not rows ->
    GROWER-FAILS (both raters). Sebastien VOID or not rated -> Chris's class, labelled 'one rater (Chris)'."
    """
    ch = gf_class(calls["chris"]) if "chris" in calls else "VOID (not rated)"
    se = gf_class(calls["sebastien"]) if "sebastien" in calls else None
    if ch.startswith("VOID"):
        oc = "VOID"
    elif se is None:
        oc = f"{ch} (one rater: Chris; Sebastien's read not made)"
    elif se.startswith("VOID"):
        oc = f"{ch} (one rater: Chris; Sebastien's read void)"
    elif ch == "GROWER-READS":
        oc = "GROWER-READS (two raters)" if se == "GROWER-READS" else "GROWER-READS (one rater: Chris); split"
    else:
        oc = "GROWER-FAILS (both raters)" if se == "GROWER-FAILS" else "GROWER-FAILS (one rater: Chris); Sebastien read rows"
    return dict(rater_class=dict(chris=ch, sebastien=se), outcome=oc)


# ================================================================================================ cross-test descriptions
def surface_rows_counts(pt_calls, dw_calls):
    """Rows calls on the surface (level) pictures of the partsheet (8) and depth_w (12: six 20 mm + six 10 mm) pages, per rater."""
    out = {}
    for r in pt_calls:
        n_pt = sum(is_rows(pt_calls[r][L]) for L in PT_LEVELS)
        lv = [p for p in dw_calls[r] if not p.endswith("_blank") and p not in ("calib", "calib_blank")]
        n_dw = sum(is_rows(dw_calls[r][p]) for p in lv)
        out[r] = dict(rows=n_pt + n_dw, of=len(PT_LEVELS) + len(lv), partsheet=n_pt, depth_w=n_dw, depth_w_10mm=sum(is_rows(dw_calls[r][p]) for p in lv if p.startswith("w10_")))
    return out


# ================================================================================================ self-test (synthetic only)
def selftest():
    fails = []

    def ok(cond, msg):
        if not cond:
            fails.append(msg)

    # ---- partsheet
    def pt_page(rows_levels, rows_blanks=(), calib="rows", cb="nothing"):
        c = {L: ("rows" if L in rows_levels else "strokes") for L in PT_LEVELS}
        c.update({f"{L}_blank": ("rows" if L in rows_blanks else "nothing") for L in PT_LEVELS})
        c.update(calib=calib, calib_blank=cb); return c
    ag = {L: dict(valid_reader_calls=(["rows"] * 3 if L == "L100" else ["strokes"] * 3)) for L in PT_LEVELS}
    ok(pt_valid(pt_page([])) and not pt_valid(pt_page([], calib="strokes")), "pt valid/calib")
    ok(pt_valid(pt_page([], ["L55"])) and not pt_valid(pt_page([], ["L55"], cb="rows")), "pt one blank ok, two not")
    r = partsheet_tolerance(dict(a=pt_page(["L100", "L85"]), b=pt_page(["L100"])), ag)
    ok(r["branches"] == ["(iii)"] and r["per_level"]["L85"] == "split", "pt (iii)")
    r = partsheet_tolerance(dict(a=pt_page(["H70", "C70", "L70"]), b=pt_page(["H70", "C70"])), ag)
    ok(r["branches"] == ["(i)", "(ii):C70"], f"pt (i)+(ii) {r['branches']}")
    r = partsheet_tolerance(dict(a=pt_page(["C70"]), b=pt_page(["C70"], ["C70"])), ag)
    ok(r["per_level"]["C70"] == "split" and r["branches"] == ["(iii)"], "pt masked -> split")
    ag2 = dict(ag); ag2["C70"] = dict(valid_reader_calls=["rows", "rows", "strokes"])
    r = partsheet_tolerance(dict(a=pt_page(["C70"]), b=pt_page(["C70"])), ag2)
    ok(r["branches"] == [] and r["contradiction_with_agent_record"] == ["C70"], "pt literal (ii) contradiction")
    ok(partsheet_tolerance(dict(a=pt_page([], calib="nothing"), b=pt_page([])), ag)["outcome"].startswith("INCONCLUSIVE"), "pt stage0")
    # ---- human_vs_agent
    for k in range(6):
        for m in range(14):
            exp = "AGENTS-OFF" if (k >= 4 and m <= 1) else "SEB-OFF" if (k <= 1 and m <= 1) else "HUMANS-NOISY"
            ok(hva_verdict(k, m) == exp, f"hva grid {k},{m}")
    ok(sign_p(5, 5) == dict(one_sided=0.0312, two_sided=0.0625) and sign_p(4, 5)["one_sided"] == 0.1875, "sign p")
    ok(kappa([True, False] * 9, [True, False] * 9) == 1.0 and kappa([True] * 18, [True] * 18) is None, "kappa")
    labels = list(PT_LEVELS) + [f"{L}_blank" for L in PT_LEVELS] + ["calib", "calib_blank"]
    agp = {p: dict(valid_reader_calls=["rows"] * 3 if p in ("calib", "L100") else ["strokes"] * 3) for p in labels}
    seb = {p: ("rows" if p in ("calib", "L100", "L85", "L70", "C85", "C70", "H70") else "nothing") for p in labels}
    chris_agentlike = {p: ("rows" if p in ("calib", "L100") else "nothing") for p in labels}
    r = human_vs_agent(dict(sebastien=seb, chris=chris_agentlike), agp, True)
    ok(r["outcome"] == "SEB-OFF" and (r["k"], r["m"]) == (0, 0), f"hva seb-off {r.get('outcome')}")
    r = human_vs_agent(dict(sebastien=seb, chris=dict(seb)), agp, True)
    ok(r["outcome"] == "AGENTS-OFF" and r["k"] == 5, "hva agents-off")
    r = human_vs_agent(dict(sebastien=seb, chris=dict(seb)), agp, False)
    ok(r["outcome"].startswith("DESCRIPTIVE ONLY"), "hva timing")
    r = human_vs_agent(dict(sebastien=seb, chris=dict(seb, calib="strokes")), agp, True)
    ok(r["outcome"].startswith("UNDECIDED"), "hva chris invalid")
    r = human_vs_agent(dict(sebastien=dict(seb, H50="rows"), chris=dict(seb)), agp, True)
    ok(r["outcome"].startswith("INCONCLUSIVE"), "hva stage0 (6 disagreements)")
    # ---- fullhop_w
    base = dict(L70d="rows", C70d="rows", L40d="strokes", H50n="rows", L100="rows", L70d_blank="nothing", C70d_blank="nothing",
                calib="rows", calib_blank="nothing")
    ok(fullhop_w(dict(a=base, b=base))["outcome"] == "FULL-HOP-HOLDS", "fh holds")
    ok(fullhop_w(dict(a=base, b=dict(base, C70d="strokes")))["outcome"] == "FULL-HOP-FAILS", "fh fails")
    ok(fullhop_w(dict(a=dict(base, L40d="rows"), b=dict(base, L40d="rows")))["outcome"].startswith("UNDECIDED (no guard"), "fh lenient")
    ok(fullhop_w(dict(a=base, b=dict(base, L100="strokes", C70d="strokes")))["outcome"].startswith("UNDECIDED (fewer"), "fh invalid")
    ok(fullhop_w(dict(a=base, b=dict(base, calib_blank="rows")))["outcome"].startswith("UNDECIDED (fewer"), "fh calib blank")
    gates = dict(stage0_gates=dict(dark_hops=dict(pass_=False), stage0b_pass=True, tiles_pass=True))
    ok(fullhop_w(dict(a=base, b=base), gates)["outcome"] == "DARK-HOPS", "fh dark hops")
    # ---- fullhop_s022814 + line_spacing
    t = dict(ctrl814="rows", L85_814="rows", L70_814="rows", L55_814="strokes", H50_814="rows", ctrl814_blank="nothing",
             L70_814_blank="nothing", calib="rows", calib_blank="nothing", O2="rows", O45="rows")
    ok(fullhop_s022814(dict(a=t, b=t))["outcome"] == "HOLDS-814", "t8 holds")
    ok(fullhop_s022814(dict(a=t, b=dict(t, L70_814="strokes")))["outcome"] == "FAILS-814", "t8 fails")
    ok(fullhop_s022814(dict(a=dict(t, L55_814="rows"), b=dict(t, L55_814="rows")))["outcome"].startswith("UNDECIDED (no 814 guard"), "t8 lenient")
    ok(fullhop_s022814(dict(a=t, b=dict(t, ctrl814="strokes")))["outcome"].startswith("UNDECIDED (ctrl814"), "t8 weak window")
    ok(fullhop_s022814(dict(a=dict(t, ctrl814="strokes", L70_814="strokes"), b=dict(t, L70_814="strokes")))["outcome"] == "FAILS-814",
       "t8 fails from the window-ok rater")
    ok(fullhop_s022814(dict(a=t, b=dict(t, ctrl814_blank="rows")))["outcome"].startswith("UNDECIDED (fewer"), "t8 invalid")
    ok(fullhop_s022814(dict(a=t, b=dict(t, O2=None)))["outcome"] == "HOLDS-814", "t8 ignores O pictures")
    r = fullhop_s022814(dict(a=dict(t, L70_814="strokes", L55_814="rows"), b=t))
    ok("descriptive_L85" in r and "1 of 2" in r["descriptive_L85"], "t8 L85 line")
    g8 = dict(stage0_gates={"0b_f140": dict(pass_=False), "0b_f170": dict(pass_=False)})
    ok(fullhop_s022814(dict(a=t, b=t), g8)["outcome"] == "INCONCLUSIVE (reader still reaches)", "t8 reader reaches")
    ok(line_spacing(dict(a=t, b=t))["arms"]["O2"]["verdict"] == "O2-READS", "lf reads")
    ok(line_spacing(dict(a=t, b=dict(t, O45="strokes")))["arms"]["O45"]["verdict"] == "O45-FAILS (O45-SPLIT)", "lf split")
    ok(line_spacing(dict(a=dict(t, O45="nothing"), b=dict(t, O45="strokes")))["arms"]["O45"]["verdict"] == "O45-FAILS (O45-NO)", "lf no")
    ok(line_spacing(dict(a=dict(t, L55_814="rows"), b=dict(t, L55_814="rows")))["arms"]["O2"]["verdict"].startswith("O2-LENIENT"), "lf lenient")
    ok(line_spacing(dict(a=t, b=dict(t, ctrl814="strokes")))["arms"]["O2"]["verdict"].startswith("O2-UNDECIDED"), "lf one-rater lead")
    ok(line_spacing(dict(a=t, b=dict(t, ctrl814="strokes", O2="strokes")))["arms"]["O2"]["verdict"] == "O2-UNDECIDED (one-rater lead: rows)",
       "lf a not-rows outside d does not count")
    ok(line_spacing(dict(a=t, b=dict(t, O45=None)))["valid"]["b"] is False, "lf F3 needs O answered")
    ok(line_spacing(dict(a=dict(t, ctrl814="nothing"), b=dict(t, ctrl814="nothing")))["arms"]["O2"]["verdict"] == "O2-VOID", "lf void")
    # ---- depth_w
    dw = {p: "strokes" for p in ("out12", "out24", "in12", "in24", "s214732", "w10_P_top", "w10_P_mid", "w10_P_bot", "w10_S_top",
                                 "w10_S_mid", "w10_S_bot")}
    dw.update({p + "_blank": "nothing" for p in ("ctrl", "out12", "out24", "in12", "in24", "s214732")})
    dw.update(ctrl="rows", calib="rows", calib_blank="nothing", w10_P_blank="nothing", w10_S_blank="nothing")
    ok(dw_rater(dw)["outcome20"] == "NARROW", "dw narrow")
    ok(dw_rater(dict(dw, in24="rows", in12="rows"))["outcome20"] == "ASYMMETRIC", "dw asym")
    ok(dw_rater(dict(dw, in12="rows"))["outcome20"] == "ASYMMETRIC-SHORT", "dw asym short")
    x = dw_rater(dict(dw, out24="rows")); ok(x["outcome20"] == "WIDE-OUT" and x["flags"], "dw wide-out non-monotone flag")
    ok(dw_rater(dict(dw, out12_blank="rows"))["outcome20"] == "INCOMPLETE", "dw incomplete (outward uncountable)")
    ok(dw_rater(dict(dw, in24_blank="rows"))["outcome20"] == "INCOMPLETE", "dw incomplete (inward uncountable)")
    ok(dw_rater(dict(dw, ctrl="strokes"))["outcome20"].startswith("VOID (control"), "dw void ctrl")
    ok(dw_rater(dict(dw, out12_blank="rows", in12_blank="rows"))["outcome20"].startswith("VOID (invalid"), "dw void 2 blanks")
    ok(dw_rater(dict(dw, w10_P_top="rows", w10_P_mid="rows"))["unit10"] == "1 cm2 USABLE", "dw unit usable")
    ok(dw_rater(dict(dw, w10_P_top="rows", w10_S_top="rows"))["unit10"] == "20 mm ONLY", "dw unit 20 only")
    ok(dw_rater(dict(dw, w10_P_top="rows"))["unit10"] == "DESCRIPTIVE", "dw unit descriptive")
    r = depth_w(dict(a=dict(dw, out24="rows", out12="rows", in24="rows", in12="rows"), b=dict(dw, out12="rows", in12="rows")))
    ok(r["outcome"] == "WIDE-OUT" and r["outward_line_um"] == 12 and r["inward_line_um"] == 12 and r["disagree"], "dw combine stricter")
    r = depth_w(dict(a=dict(dw, in24="rows", in12="rows"), b=dict(dw, out12_blank="rows")))
    ok(r["outcome"] == "ASYMMETRIC" and r["label"] == "one rater", "dw combine one rater")
    r = depth_w(dict(a=dict(dw, s214732="rows"), b=dict(dw, s214732="rows", w10_P_top="rows", w10_P_mid="rows")))
    ok(r["s214732"].startswith("ROWS") and r["unit10"] == "DESCRIPTIVE / SPLIT", "dw s214732 + unit split")
    r = depth_w(dict(a=dict(dw, out12="rows", in24_blank="rows"), b=dict(dw, out24="rows", out12="rows", in12="rows")))
    ok(r["outcome"] == "WIDE-OUT" and r["inward_line_um"] == 12, "dw WIDE-OUT rater with an uncountable inward tile")
    r = depth_w(dict(a=dict(dw, out12="rows", in24_blank="rows")))
    ok(r["outcome"] == "WIDE-OUT" and r["inward_line_um"] is None, "dw one WIDE-OUT rater, inward uncountable")
    # ---- depth_s022814
    ds = dict(ctrl="rows", ctrl_blank="nothing", in24="rows", in24_blank="nothing", out24="rows", out24_blank="nothing",
              in48="rows", out48="strokes", w10_top="strokes", w10_bot="rows", w10_blank="nothing", guard_1="strokes",
              calib="rows", calib_blank="nothing")
    ok(ds_rater(ds)["depth"] == "WIDE-HOLDS" and ds_rater(ds)["cm2"] == "20MM-NEEDED", "ds wide")
    ok(ds_rater(dict(ds, guard_1="rows"))["depth"] == "ALL-ROWS", "ds lenient")
    ok(ds_rater(dict(ds, out24="nothing"))["depth"] == "NARROW-OUT", "ds narrow out")
    ok(ds_rater(dict(ds, in24="nothing"))["depth"] == "NARROW-IN", "ds narrow in")
    ok(ds_rater(dict(ds, in24="nothing", out24="nothing"))["depth"] == "NARROW-BOTH", "ds narrow both")
    ok(ds_rater(dict(ds, in24_blank="rows"))["depth"] == "INCOMPLETE", "ds incomplete")
    ok(ds_rater(dict(ds, ctrl="strokes"))["window"] == "WINDOW-NO", "ds window no")
    ok(ds_rater(dict(ds, ctrl_blank="rows"))["window"].startswith("VOID"), "ds ctrl blank void")
    nog = {k: v for k, v in ds.items() if k != "guard_1"}
    ok(ds_rater(nog)["window"].startswith("VOID"), "ds no guard invalid")
    ok(ds_rater(dict(ds, w10_top="rows"))["cm2"] == "1CM-READS-PRIMED", "ds 1cm")
    ok(depth_s022814(dict(a=ds, b=ds))["outcome"] == "CONFIRMED (WIDE-HOLDS, two raters)", "ds confirmed")
    ok(depth_s022814(dict(a=ds, b=dict(ds, guard_1="rows")))["outcome"].startswith("SPLIT / NOT DECIDED"), "ds all-rows split")
    ok(depth_s022814(dict(a=dict(ds, out24="nothing"), b=dict(ds, out24="nothing")))["outcome"].startswith("NARROWED: NARROW-OUT"), "ds narrowed")
    ok(depth_s022814(dict(a=dict(ds, ctrl="nothing"), b=dict(ds, ctrl="nothing")))["outcome"] == "WINDOW-NO", "ds window-no")
    ok(depth_s022814(dict(a=ds, b=dict(ds, calib="strokes")))["outcome"].startswith("ONE RATER"), "ds one rater")
    # ---- spiral_field
    sp = dict(A1="rows", A1_blank="nothing", A2="rows", A2_blank="nothing", C="rows", C_blank="nothing", guard="strokes",
              calib="rows", calib_blank="nothing")
    F = dict(has_guard=True, rated_after_page_built=True); NG = dict(has_guard=False, rated_after_page_built=True)
    spn = {k: v for k, v in sp.items() if k != "guard"}
    ok(spiral_field(dict(c=sp, s=spn), dict(c=F, s=NG))["outcome"] == "SPIRAL-READS (raters know the field)", "sp reads")
    ok(spiral_field(dict(c=dict(sp, A1="strokes", A2="nothing"), s=spn), dict(c=F, s=NG))["outcome"] == "SPIRAL-NO-ROWS (one rater: c)", "sp no-rows one")
    ok(spiral_field(dict(c=dict(sp, A1="strokes"), s=dict(spn, A1="strokes")), dict(c=F, s=NG))["outcome"].startswith("SPIRAL-READS-WITH-PICK"), "sp pick")
    ok(spiral_field(dict(c=dict(sp, guard="rows"), s=spn), dict(c=F, s=NG))["outcome"] == "SPLIT (no claim)", "sp lenient -> split")
    ok(spiral_field(dict(c=dict(sp, A1="strokes", A2="strokes", guard="rows"), s=spn), dict(c=F, s=NG))["outcome"].startswith("SPIRAL-NO-ROWS"),
       "sp lenient not-rows still counts")
    ok(sp_rater_class(dict(spn, C_blank="rows"), ("A1", "A2"), noguard=True) == "VALID-LENIENT", "sp amend3 lenient")
    ok(sp_rater_class(dict(spn, C_blank="rows", A1_blank="rows"), ("A1", "A2"), noguard=True) == "INVALID", "sp invalid")
    ok(sp_rater_class(dict(sp, C="strokes"), ("A1", "A2")) == "UNINFORMATIVE-C", "sp uninformative")
    ok(spiral_field(dict(c=sp, s=spn), dict(c=dict(F, rated_after_page_built=False), s=NG))["outcome"].startswith("INCONCLUSIVE"), "sp order void")
    ok(spiral_field(dict(c=dict(sp, calib="strokes"), s=dict(spn, C="nothing")), dict(c=F, s=NG))["outcome"].startswith("UNINFORMATIVE"), "sp none valid")
    # ---- grown_field
    gf = dict(grown="rows", grown_blank="nothing", ctrl="rows", calib="rows", calib_blank="nothing", guard="strokes")
    ok(grown_field(dict(chris=gf, sebastien=gf))["outcome"] == "GROWER-READS (two raters)", "gf two")
    ok(grown_field(dict(chris=gf, sebastien=dict(gf, grown="strokes")))["outcome"].endswith("split"), "gf split")
    ok(grown_field(dict(chris=dict(gf, grown="nothing"), sebastien=gf))["outcome"].startswith("GROWER-FAILS (one rater"), "gf fails one")
    ok(grown_field(dict(chris=dict(gf, grown="nothing"), sebastien=dict(gf, grown="strokes")))["outcome"] == "GROWER-FAILS (both raters)", "gf fails both")
    ok(grown_field(dict(chris=dict(gf, guard="rows"), sebastien=gf))["outcome"] == "VOID", "gf chris void")
    ok(grown_field(dict(chris=gf, sebastien=dict(gf, ctrl="strokes")))["outcome"].endswith("read void)"), "gf seb void")
    ok(grown_field(dict(chris=gf))["outcome"].endswith("not made)"), "gf seb missing")
    return fails
