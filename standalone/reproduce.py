"""Recompute every number in the README from the files in this repo (CPU only, numpy + scipy, a few seconds).

    python reproduce.py

Parts:
  audit    the w00 audit against blind 2.4 um marks (guide-free and guided) and the timed hand fix
  reads    the blind human-read tests: per-picture calls -> each pre-registered rule -> named verdict
  numbers  the reader tile-phase sweep and the lasagna fit numbers (from saved, non-human outputs)

Parts that need the human marks or ratings print "SKIPPED: human data not in this copy (...)" when `human_data/` is absent.
Exit code 0 only if every check that ran matches its expected value.
"""
import importlib.util
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))


def load(name, rel):
    """Load a part's script by file path (the folder `numbers/` would shadow Python's own `numbers` module)."""
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, rel))
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, os.path.dirname(os.path.join(ROOT, rel)))
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.path.pop(0)
    return mod


def main():
    results = {}

    print("=" * 30, "audit", "=" * 30)
    audit = load("pkgb_reproduce_audit", os.path.join("audit", "reproduce_audit.py"))
    ok, rows, skipped = audit.run()
    results["audit"] = (ok, f"{sum(r[3] for r in rows)}/{len(rows)} checks pass" + (f", {len(skipped)} part(s) skipped" if skipped else ""))

    print("\n" + "=" * 30, "reads", "=" * 30)
    reads = load("pkgb_reproduce_reads", os.path.join("reads", "reproduce_reads.py"))
    r = reads.run()
    results["reads"] = (bool(r["ok"]), "OK" if r["ok"] else "MISMATCH")

    print("\n" + "=" * 30, "numbers", "=" * 30)
    numbers = load("pkgb_reproduce_numbers", os.path.join("numbers", "reproduce_numbers.py"))
    rc = numbers.main()
    results["numbers"] = (rc == 0, "ALL OK" if rc == 0 else "MISMATCH")

    print("\n" + "=" * 30, "summary", "=" * 30)
    for part, (ok, msg) in results.items():
        print(f"{part:8s} {'PASS' if ok else 'FAIL'}  {msg}")
    have_human = os.path.isdir(os.path.join(ROOT, "human_data"))
    if not have_human:
        print("note: human_data/ is absent, so the parts that need the marks or ratings were skipped.")
    all_ok = all(ok for ok, _ in results.values())
    print("ALL CHECKS PASS" if all_ok else "SOME CHECKS FAILED")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
