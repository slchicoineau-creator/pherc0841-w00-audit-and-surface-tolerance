"""Oracle tests for reads/: every verdict and count below is hard-coded from the independent Judge re-score of each test.

    python -m unittest tests/test_reads.py      (or: python -m pytest tests/test_reads.py)

Tests that need human_data/reads skip cleanly when it is not in this copy; the selftest and the data-only numbers always run.
"""
import json, os, sys, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "reads"))
import read_rules as rules  # noqa: E402
import reproduce_reads as rr  # noqa: E402

HD = os.path.join(ROOT, "human_data", "reads")
DD = os.path.join(ROOT, "data", "reads")


def has(*tests):
    return all(os.path.exists(os.path.join(HD, t + ".json")) for t in tests)


def need(*tests):
    return unittest.skipUnless(has(*tests), "human data not in this copy (human_data/reads/%s.json)" % "/".join(tests))


def calls(test):
    return rr.calls_by_rater(rr.jload(HD, test + ".json"))


class TestSelftest(unittest.TestCase):
    def test_rules_selftest(self):
        self.assertEqual(rules.selftest(), [])


class TestNumbers(unittest.TestCase):
    """Descriptive numbers from saved non-human outputs (always run)."""

    @classmethod
    def setUpClass(cls):
        cls.n = rr.numbers()

    def test_fullhop_w_dose(self):
        L, C = self.n["fullhop_w"]["L70d"], self.n["fullhop_w"]["C70d"]
        self.assertEqual((L["hop_auc"], L["bar"], L["margin"], L["blank"]), (0.5755, 0.5756, 0.0001, 0.5256))
        self.assertEqual((round(C["hop_auc"], 3), C["bar"], C["blank"]), (0.611, 0.614, 0.564))
        self.assertEqual((round(L["unmoved"], 3), round(L["unmoved_parent"], 3)), (0.955, 0.959))
        self.assertEqual((round(C["unmoved"], 3), round(C["unmoved_parent"], 3)), (0.860, 0.861))
        self.assertEqual((L["moved_gt50_pixel_share"], C["moved_gt50_pixel_share"]), (0.40, 0.39))
        self.assertEqual((L["offset_layers"], C["offset_layers"]), (0, -22))
        d = rr.jload(DD, "fullhop_w_numbers.json")
        self.assertTrue(d["stage0_gates"]["dark_hops"]["pass_"] and d["stage0_gates"]["stage0b_pass"])
        self.assertEqual(d["stage0b_floor_um"], 140)

    def test_fullhop_s022814_dose(self):
        t = self.n["fullhop_s022814"]
        self.assertEqual((t["floor140"]["hop_auc"], t["floor140"]["bar"], t["floor140"]["passed"]), (0.5765, 0.559, False))
        f = t["floor170"]
        self.assertEqual((f["hop_auc"], f["blank"], f["bar"], f["passed"]), (0.5033, 0.4945, 0.5445, True))
        self.assertEqual((round(f["ctrl_same_px"], 3), round(f["unmoved"], 3), round(f["unmoved_ctrl"], 3)), (0.840, 0.861, 0.876))
        self.assertEqual(t["moved_gt50_vertex_pct"], {"L85_814": 16.5, "L70_814": 32.2, "L55_814": 47.6})
        self.assertTrue(all(195 <= v <= 205 for v in t["median_move_um"].values()))
        self.assertEqual(round(t["ctrl_map_auc"], 3), 0.867)

    def test_depth_s022814_maps(self):
        d = self.n["depth_s022814"]
        self.assertEqual(d["r_vs_ctrl"], {"out24": 0.868, "in24": 0.851, "out48": 0.689, "in48": 0.691})
        self.assertEqual({k: round(v, 3) for k, v in d["label_auc"].items()},
                         {"out48": 0.776, "out24": 0.837, "ctrl": 0.868, "in24": 0.867, "in48": 0.821})
        self.assertEqual(d["astar_layers"], 0)
        self.assertEqual({k: round(v, 3) for k, v in d["w10_ctrl_auc"].items()}, {"top": 0.714, "bot": 0.913})

    def test_grown_field_row_score_and_agents(self):
        g = self.n["grown_field"]
        self.assertEqual((g["row_score_grown"], g["row_score_ctrl"], g["grown_over_ctrl"]), (0.40, 23.3, 0.017))
        self.assertEqual(g["row_score_grown_blank"], 1.27)
        self.assertEqual((g["agents_rows_grown"], g["agents_rows_ctrl"]), ("0/5", "5/5"))

    def test_numbers_oracle_in_run(self):
        self.assertEqual(rr.check_numbers(self.n), [])

    def test_designs_carry_no_observed_outcome(self):
        for t in rr.TESTS:
            d = rr.jload(DD, t + "_design.json")
            for k in ("loop_verdict_for_observed_outcome", "claim_wording", "judge_notes", "calls"):
                self.assertNotIn(k, d, f"{t}: {k} belongs in human_data")

    def test_agent_screen_partsheet(self):
        ag = rr.jload(DD, "agent_reads_partsheet_page.json")["pictures"]
        self.assertEqual(len(ag), 18)
        self.assertTrue(all(len(v["valid_reader_calls"]) == 3 for v in ag.values()))
        reads = rules.agents_read_levels(ag)
        self.assertEqual(sorted(L for L, v in reads.items() if v), ["C85", "L100"])


class TestShared(unittest.TestCase):
    @need("fullhop_s022814", "line_spacing")
    def test_shared_s022814_page_identical(self):
        self.assertEqual(rr.jload(HD, "fullhop_s022814.json")["calls"], rr.jload(HD, "line_spacing.json")["calls"])

    @need("partsheet_tolerance", "human_vs_agent")
    def test_shared_partsheet_page_identical(self):
        self.assertEqual(calls("partsheet_tolerance"), calls("human_vs_agent"))


class TestVerdicts(unittest.TestCase):
    @need("partsheet_tolerance")
    def test_partsheet_tolerance(self):
        r = rr.score("partsheet_tolerance")
        self.assertEqual(r["valid"], {"chris": True, "sebastien": True})
        self.assertEqual(r["masked"], {"chris": [], "sebastien": []})
        self.assertEqual(r["per_level"], {"L100": "reads for humans", "L85": "reads for humans", "L70": "reads for humans",
                                          "L55": "split", "C85": "reads for humans", "C70": "reads for humans", "H70": "split",
                                          "H50": "does not read"})
        self.assertEqual(r["branches"], ["(ii):C70", "(ii):L70"])
        self.assertEqual(r["contradiction_with_agent_record"], [])
        self.assertTrue(r["loop_verdict"].startswith("PASS"))
        for who in ("chris", "sebastien"):
            c = calls("partsheet_tolerance")[who]
            self.assertEqual(sum(rules.is_rows(c[f"{L}_blank"]) for L in rules.PT_LEVELS) + rules.is_rows(c["calib_blank"]), 0)

    @need("human_vs_agent")
    def test_human_vs_agent(self):
        r = rr.score("human_vs_agent")
        self.assertTrue(r["stage0_pass"] and r["chris_valid"])
        self.assertEqual((r["n_discordant"], r["k"], r["n_concordant"], r["m"]), (5, 3, 13, 0))
        self.assertEqual(r["outcome"], "HUMANS-NOISY")
        self.assertEqual(r["sign_p"]["one_sided"], 0.5)
        self.assertEqual(r["kappa"], {"seb_chris": 0.769, "seb_agents": 0.4, "chris_agents": 0.571})
        self.assertEqual(r["agree_of_18"], {"seb_chris": 16, "seb_agents": 13, "chris_agents": 15})
        self.assertEqual(r["rows_calls_of_18"], {"seb": 8, "chris": 6, "agents": 3})
        self.assertEqual(r["direction"], dict(seb_rows_agents_not=5, seb_not_agents_rows=0, chris_rows_agents_not=3,
                                              chris_not_agents_rows=0, seb_rows_chris_not=2, chris_rows_seb_not=0))
        for nm in ("seb_chris", "seb_agents", "chris_agents"):
            d = r["disagreements_by_kind"][nm]
            self.assertEqual(d["blank"] + d["calib"] + d["calib_blank"], 0)
        self.assertTrue(r["loop_verdict"].startswith("FAIL"))

    @need("fullhop_w")
    def test_fullhop_w(self):
        r = rr.score("fullhop_w")
        self.assertEqual(r["outcome"], "FULL-HOP-FAILS")
        self.assertEqual(r["valid"], {"chris": True, "sebastien": True})
        self.assertEqual(r["fails_carried_by"], {"chris": ["L70d", "C70d"], "sebastien": ["C70d"]})
        c = calls("fullhop_w")
        for who in c:   # outline: L40d (60 % full hops) not rows for both; H50n (50 % holes) rows for both; L100 rows for both
            self.assertFalse(rules.is_rows(c[who]["L40d"])); self.assertTrue(rules.is_rows(c[who]["H50n"]))
            self.assertTrue(rules.is_rows(c[who]["L100"]))
            self.assertEqual(sum(rules.is_rows(c[who][b]) for b in ("L70d_blank", "C70d_blank", "calib_blank")), 0)

    @need("fullhop_s022814")
    def test_fullhop_s022814(self):
        r = rr.score("fullhop_s022814")
        self.assertEqual(r["outcome"], "FAILS-814")
        self.assertEqual(r["valid"], {"chris": True, "sebastien": True})
        self.assertEqual(r["window_ok"], {"chris": True, "sebastien": True})
        self.assertEqual(r["rows_count_of_2"], {"ctrl814": 2, "L85_814": 2, "L70_814": 1, "L55_814": 1, "H50_814": 2})
        self.assertEqual(r["raters_rejecting_L70_but_reading_nested_L55"], 1)
        c = calls("fullhop_s022814")   # outline: crossed calls, Chris 30 % strokes and 45 % rows, Sebastien the reverse
        self.assertEqual((c["chris"]["L70_814"], c["chris"]["L55_814"]), ("strokes", "rows"))
        self.assertEqual((c["sebastien"]["L70_814"], c["sebastien"]["L55_814"]), ("rows", "strokes"))
        self.assertIn("1 of 2", r["descriptive_L85"])

    @need("line_spacing")
    def test_line_spacing(self):
        r = rr.score("line_spacing")
        self.assertEqual(r["outcome"], "O2-READS")
        self.assertEqual(r["secondary"], "O45-FAILS (O45-SPLIT)")
        self.assertEqual(sorted(r["d"]), ["chris", "sebastien"])
        self.assertEqual((r["arms"]["O2"]["rows"], r["arms"]["O45"]["rows"]), (2, 1))
        self.assertEqual(r["arms"]["O2"]["guard_rejected_by"], ["sebastien"])

    @need("depth_w")
    def test_depth_w(self):
        r = rr.score("depth_w")
        self.assertEqual(r["outcome"], "WIDE-OUT")
        self.assertEqual((r["outward_line_um"], r["inward_line_um"], r["label"], r["disagree"]), (24, 24, "two raters", False))
        self.assertTrue(r["s214732"].startswith("ROWS"))
        self.assertEqual(r["unit10"], "DESCRIPTIVE / SPLIT")
        s, c = r["raters"]["sebastien"], r["raters"]["chris"]
        self.assertEqual((s["valid"], s["blank_rows"], s["outcome20"], s["k10_P"], s["k10_S"], s["unit10"]),
                         (True, 0, "WIDE-OUT", 3, 3, "20 mm ONLY"))
        self.assertEqual((c["valid"], c["blank_rows"], c["outcome20"], c["k10_P"], c["k10_S"], c["unit10"]),
                         (True, 0, "WIDE-OUT", 2, 0, "1 cm2 USABLE"))
        h = rr.jload(HD, "depth_w.json"); cb = calls("depth_w")
        size = {x["picture"]: x["size"] for x in h["calls"]}
        agree = lambda sz: sum(cb["sebastien"][p] == cb["chris"][p] for p in size if size[p] == sz)
        self.assertEqual((agree("20mm"), agree("10mm")), (14, 4))

    @need("depth_s022814")
    def test_depth_s022814(self):
        r = rr.score("depth_s022814")
        self.assertEqual(r["outcome"], "CONFIRMED (WIDE-HOLDS, two raters)")
        self.assertTrue(r["loop_verdict"].startswith("PASS"))
        for who, gr in (("sebastien", (0, 1)), ("chris", (1, 3))):
            x = r["raters"][who]
            self.assertEqual((x["valid"], x["lenient"], x["window"], x["depth"], x["cm2"]),
                             (True, False, "WINDOW-YES", "WIDE-HOLDS", "20MM-NEEDED"))
            self.assertEqual(((x["guard_rows"], x["n_guard"]), (x["blank_rows"], x["n_blanks"])), (gr, (0, 4)))
        self.assertEqual(r["reader"], "H9 DROPPED (two raters)")
        # outline: Chris called +48 um outward strokes (the only fresh depth picture either rater called not rows), -48 um rows;
        # Sebastien called both rows
        self.assertEqual(r["edge_calls"], {"chris": {"in48": "rows", "out48": "strokes"}, "sebastien": {"in48": "rows", "out48": "rows"}})
        cb = calls("depth_s022814")
        surf = ("ctrl", "in24", "out24", "in48", "out48", "w10_top", "w10_bot")
        self.assertEqual({w: sum(rules.is_rows(cb[w][p]) for p in surf) for w in cb}, {"sebastien": 6, "chris": 5})

    @need("spiral_field")
    def test_spiral_field(self):
        r = rr.score("spiral_field")
        self.assertEqual(r["outcome"], "SPIRAL-NO-ROWS (one rater: chris)")
        self.assertEqual(r["rater_class"], {"chris": "VALID", "sebastien": "VALID"})
        self.assertEqual(r["arms_called_rows"], {"chris": 0, "sebastien": 2})
        self.assertEqual(r["empties_called_rows"], {"chris": 0, "sebastien": 0})
        f = rr.facts(rr.jload(HD, "spiral_field.json"))
        self.assertEqual((f["chris"]["has_guard"], f["sebastien"]["has_guard"]), (True, False))
        self.assertTrue(all(v["rated_after_page_built"] and v["page_pictures_match_key"] for v in f.values()))
        self.assertEqual((f["chris"]["n_pictures"], f["sebastien"]["n_pictures"]), (9, 8))
        self.assertFalse(rules.is_rows(calls("spiral_field")["chris"]["guard"]))

    @need("grown_field")
    def test_grown_field(self):
        r = rr.score("grown_field")
        self.assertEqual(r["outcome"], "GROWER-READS (two raters)")
        self.assertEqual(r["rater_class"], {"chris": "GROWER-READS", "sebastien": "GROWER-READS"})
        self.assertTrue(r["loop_verdict"].startswith("PASS"))

    @need("partsheet_tolerance", "depth_w", "fullhop_w", "fullhop_s022814")
    def test_cross_test_lines(self):
        cr = rr.cross()
        # Sebastien called rows on 19 of 20 surface-picture showings on the partsheet and depth_w pages (20 showings of 19
        # unique pictures: the depth_w control is the same picture as the partsheet L100); Chris 13 of 20 (2/6 at 10 mm)
        self.assertEqual((cr["surface_rows"]["sebastien"]["rows"], cr["surface_rows"]["sebastien"]["of"]), (19, 20))
        self.assertEqual((cr["surface_rows"]["chris"]["rows"], cr["surface_rows"]["chris"]["depth_w_10mm"]), (13, 2))
        # 50 % holes: not rows for both on partsheet; rows for both on fullhop_w's H50n and fullhop_s022814's H50_814
        self.assertEqual(cr["holes50_rows_of_2"], {"partsheet_tolerance:H50": 0, "fullhop_w:H50n": 2, "fullhop_s022814:H50_814": 2})


class TestRun(unittest.TestCase):
    def test_run_ok(self):
        res = rr.run(verbose=False)
        self.assertTrue(res["ok"])


if __name__ == "__main__":
    unittest.main()
