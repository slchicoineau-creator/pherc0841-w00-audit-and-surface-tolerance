"""Run every reproduce/<test>.py; exit 0 only if every quoted number matches its Judge verdict."""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
results = []
skipped = []
for script in sorted(HERE.glob("*.py")):
    if script.name == "run_all.py":
        continue
    if not (DATA / script.stem).is_dir():  # each test reads data/<test>/; a folder not in this copy is skipped
        skipped.append(script.stem)
        print(f"SKIPPED  {script.stem} (data/{script.stem}/ not in this copy)")
        continue
    r = subprocess.run([sys.executable, str(script)], capture_output=True, text=True, encoding="utf-8")
    results.append((script.stem, r.returncode))
    print(f"{'MATCH   ' if r.returncode == 0 else 'MISMATCH'} {script.stem}")
    if r.returncode != 0:
        print("   " + (r.stdout + r.stderr).strip().replace("\n", "\n   ")[-1500:])
bad = [n for n, c in results if c != 0]
print(f"\n{len(results) - len(bad)}/{len(results)} tests match" + (f", {len(skipped)} skipped (data not in this copy)" if skipped else ""))
sys.exit(1 if bad else 0)
