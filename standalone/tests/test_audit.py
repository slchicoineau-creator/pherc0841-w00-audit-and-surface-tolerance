"""Oracle tests for audit/ (w00 audit: guide-free, guided, hand fix). Expected values are hard-coded from the judged re-scores.
Human-data tests skip cleanly when human_data/audit/ is absent; the selftest and the mark-free checks always run.

  python -m unittest tests.test_audit -v                       (from the repository root)
  W00_TIFXYZ=<folder with w00's x/y/z.tif + meta.json> python -m unittest tests.test_audit -v
      also scores the organizers' w00 surface itself through score_surface.py and checks it gives 42/82 and 18/40."""
import os, sys, tempfile, unittest, argparse
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "audit"))
import audit_core as C            # noqa: E402
import reproduce_audit as RA      # noqa: E402
import score_surface as SS        # noqa: E402

try:
    import tifffile               # noqa: F401
    HAVE_TIF = True
except ImportError:
    HAVE_TIF = False


def need(*names):
    miss = [n for n in names if C.human_file(n) is None]
    return unittest.skipIf(bool(miss), f"human data not in this copy ({', '.join(miss)})")


class TestMarkFree(unittest.TestCase):
    def test_selftest(self):
        r = SS.selftest()
        self.assertTrue(r["ok"], r)
        self.assertEqual(r["crit_82"], 14)
        self.assertEqual(r["verdict_cases"]["spread"], [20, "AGREE-BELOW-9IN10"])

    def test_data(self):
        got, D = RA.part_data()
        self.assertEqual(got["data: strips (primary / replication)"], "16 / 9")
        self.assertTrue(got["data: w00 at station 0 == shared start, max |diff| <= 1 um"])
        self.assertTrue(all(len(s["station_s_mm"]) == 7 and len(s["w00_n_mm"]) == 7 for s in D))
        self.assertEqual([(s["strip"], k) for s in D for k, x in enumerate(s["w00_n_mm"]) if x is None], [("F+10-20", 6), ("F+15+15", 6)])

    def test_clopper_pearson(self):
        self.assertEqual(C.cp(42, 82), [0.3992, 0.6242])
        self.assertEqual(C.cp(18, 20, 3), [0.683, 0.988])
        self.assertEqual(C.cp(20, 25, 3), [0.593, 0.932])
        self.assertEqual(C.off_crit(40), 8)

    @unittest.skipUnless(HAVE_TIF, "tifffile not installed")
    def test_tifxyz_roundtrip(self):
        S, V, f = SS.synth_mesh(60.0 / C.UM_PER_VX, 0.05)
        with tempfile.TemporaryDirectory() as d:
            for i, a in enumerate("xyz"):
                tifffile.imwrite(os.path.join(d, a + ".tif"), S[..., i].astype(np.float32))
            with open(os.path.join(d, "meta.json"), "w") as fh:
                fh.write('{"format": "tifxyz", "scale": [0.05, 0.05]}')
            S2, V2, step = C.read_tifxyz(d)
        self.assertEqual(step, 20.0)
        W, _ = C.at_stations(C.strip_trace(S2, V2, f, step), [-1.0, 0.0, 1.0])
        for c, w in zip([-1.0, 0.0, 1.0], W):
            self.assertLess(abs(w - (0.06 + 0.05 * c)) * 1000, 1.0)


class TestGuideFree(unittest.TestCase):
    @need("guidefree_marks_chris.json")
    def test_primary(self):
        _, D = RA.part_data(); g, _ = RA.part_guidefree(D)
        self.assertEqual(g["guidefree primary: on / n"], "42/82")
        self.assertEqual(g["guidefree primary: rate"], 0.5122)
        self.assertEqual(g["guidefree primary: Clopper-Pearson 95 %"], [0.3992, 0.6242])
        self.assertEqual(g["guidefree primary: OFF critical count (p_on 0.90, one-sided 0.05)"], 14)
        self.assertEqual(g["guidefree primary: strip-bootstrap 95 % upper bound"], 0.6374)
        self.assertEqual(g["guidefree primary: frozen verdict"], "AGREE-BELOW-9IN10")
        self.assertEqual(g["guidefree primary: misses 75-150 um / > 150 um"], "20 / 20")
        self.assertEqual(g["guidefree primary: can't-tell stations"], 14)
        self.assertEqual(g["guidefree primary: can't-tells as misses / as agreements"], "42/96 / 56/96")
        self.assertEqual(g["guidefree primary: key-noise bracket e = 0 / 0.065 / 0.10"], [0.5122, 0.5478, 0.5691])
        self.assertEqual(g["guidefree primary: leave-one-strip-out drops that change the verdict"], 0)
        self.assertEqual(g["guidefree primary (post hoc): fresh along bend / flat"], "5/28 / 14/18")
        self.assertEqual(g["guidefree primary: fresh along / cross at dev sites"], "19/46 / 23/36")

    @need("guidefree_marks_chris.json")
    def test_replication(self):
        _, D = RA.part_data(); g, _ = RA.part_guidefree(D)
        self.assertEqual(g["guidefree replication: on / n (strips)"], "18/40 (8)")
        self.assertEqual(g["guidefree replication: Clopper-Pearson 95 %"], [0.2926, 0.6151])
        self.assertEqual(g["guidefree replication: OFF critical count"], 8)
        self.assertEqual(g["guidefree replication: strip-bootstrap 95 % upper bound"], 0.6667)
        self.assertEqual(g["guidefree replication: misses 75-150 um / > 150 um"], "6 / 16")
        self.assertEqual(g["guidefree replication: can't-tell stations"], 14)
        self.assertEqual(g["guidefree replication: key-noise bracket e = 0 / 0.065 / 0.10"], [0.45, 0.4813, 0.5])

    @need("guidefree_marks_chris.json")
    @unittest.skipUnless(HAVE_TIF and os.environ.get("W00_TIFXYZ"), "set W00_TIFXYZ to the downloaded w00 2.403 um tifxyz folder")
    def test_w00_surface_reproduces_42_of_82(self):
        out = SS.cmd_score(argparse.Namespace(surface=os.environ["W00_TIFXYZ"], affine=None, json=None, pool="all", expect_w00=True))
        p, r = out["primary_vs_marks"]["tol_75um"], out["replication_vs_marks"]["tol_75um"]
        self.assertEqual((p["on"], p["n"], p["cp95"], p["strip_bootstrap_ub95"]), (42, 82, [0.3992, 0.6242], 0.6374))
        self.assertEqual((r["on"], r["n"], r["cp95"], r["strip_bootstrap_ub95"]), (18, 40, [0.2926, 0.6151], 0.6667))


class TestGuided(unittest.TestCase):
    @need("guided_sites.json", "guided_marks.json")
    def test_guided(self):
        g, _ = RA.part_guided()
        self.assertEqual(g["guided random: human-human within 75 um / shared"], "18/20")
        self.assertEqual(g["guided random: human-human median (um)"], 14.4)
        self.assertEqual(g["guided random: human-human Clopper-Pearson 95 %"], [0.683, 0.988])
        self.assertEqual(g["guided random: w00 vs Sebastien / vs Chris"], "19/21 / 15/22")
        self.assertEqual(g["guided random: w00 vs Sebastien CI / vs Chris CI"], [[0.696, 0.988], [0.451, 0.861]])
        self.assertEqual(g["guided random: can't tell Sebastien / Chris"], "4 / 3")
        self.assertEqual(g["guided random: straight extension of the guide within 75 um of w00"], "23/25")
        self.assertEqual(g["guided random: marks within 75 um of the straight extension Sebastien / Chris"], "18/21 / 13/22")
        self.assertEqual(g["guided random: sites where both raters agree and both are > 75 um off the extension"], 2)
        self.assertEqual(g["guided random: centre-click baseline"], "15/25")
        self.assertEqual(g["guided repeats: Chris pairs within 75 um (diffs um)"], "0/2 (137.8, 243.5)")
        self.assertEqual(g["guided repeats: Sebastien pairs marked (diffs um)"], "1 (2.4): unmeasured")
        self.assertEqual(g["guided suspect: human-human / w00 vs Sebastien / w00 vs Chris"], "9/9 / 6/9 / 6/9")
        self.assertEqual(g["guided: verdict (human floor; w00 row; flags)"],
                         "KEY OK; MEASURED; chris repeats unreliable + consistent with following the guide line")


class TestHandFix(unittest.TestCase):
    @need("handfix_sites.json", "handfix_marks_chris.json")
    def test_handfix(self):
        g, _ = RA.part_handfix()
        self.assertEqual(g["handfix session 1: hand-fixed / control / start / copy (on of valid)"], "17 / 23 / 16 / 14 of 24")
        self.assertEqual(g["handfix session 1: class (KILL <= control - 5; MIDDLE from control - 4)"], "KILL-marks (KILL line 18, MIDDLE at 19)")
        self.assertEqual(g["handfix session 1: hand-fixed on at 50 / 75 / 100 um (control)"], "13 / 17 / 20 (20 / 23 / 24)")
        self.assertEqual(g["handfix session 1: start -> hand-fixed sites gained / lost"], "4 / 3")
        self.assertEqual(g["handfix session 1: marks within 75 um of the straight guide"], "22/24")
        self.assertEqual(g["handfix session 2: hand-fixed / control / copy (on of valid)"], "16 / 19 / 14 of 23")
        self.assertEqual(g["handfix session 2: class (KILL line, PASS needs)"], "MIDDLE (14, 18)")
        self.assertEqual(g["handfix: 23 sites valid in both sessions, session 1 hand-fixed / control"], "17 / 22 (KILL-marks)")
        self.assertEqual(g["handfix: hand-fixed on/off same in both sessions"], "16/23")

    def test_mark_class(self):
        self.assertEqual(RA.mark_class(24, 23, 18), "KILL-marks")
        self.assertEqual(RA.mark_class(24, 23, 19), "MIDDLE")
        self.assertEqual(RA.mark_class(24, 23, 21), "PASS-marks")
        self.assertEqual(RA.mark_class(17, 15, 15), "TOO FEW")


class TestReproduce(unittest.TestCase):
    def test_all_checks_pass(self):
        ok, rows, skipped = RA.run(verbose=False)
        self.assertTrue(ok, [r for r in rows if not r[3]])
        self.assertGreaterEqual(len(rows), 2)


if __name__ == "__main__":
    unittest.main()
