# standalone/: a second, independent re-check of the numbers in the main README

`../reproduce/` re-scores the original saved keys, ratings and marks. This folder is a separate, smaller re-implementation
that reads only small exported files:
- `data/`: mark-free geometry, page designs and saved reader/fit numbers;
- `human_data/`: marks and per-picture calls, released with both authors' OK, file by file.

It recomputes the numbers from those files with its own code. Two independent codings that agree are a stronger check than one.

```
python reproduce.py                    # exit 0 only if every check that ran matches
python -m pytest tests -q
python audit/score_surface.py selftest
python audit/score_surface.py score <path/to/surface.tifxyz>
```

Python 3.11 or newer (`requirements.txt`). CPU only, a few seconds. Without `human_data/`, the parts that need it print
`SKIPPED: human data not in this copy (...)`, and the rest still runs.

## What is here

| Path | What |
|---|---|
| `reproduce.py` | runs the three parts below and prints one summary |
| `audit/` | the w00 audit against blind 2.4 µm marks (guide-free and guided) and the hand-fix marks |
| `audit/score_surface.py` | scores ANY tifxyz surface of the known-text window against the 25 audit strips (per-station distance, agreement at 75 and 150 µm, Clopper-Pearson CI, strip bootstrap, key-noise bracket) |
| `reads/` | the blind-read tests: per-picture calls → each pre-registered rule (`read_rules.py`) → named verdict |
| `numbers/` | the reader tile-phase sweep and the lasagna fit numbers (from saved, non-human outputs) |
| `tests/` | the same checks as unit tests, with hard-coded expected values |
| `preregs/` | scrubbed copies of the pre-registrations behind the results, with commit times (`PREREG_INDEX.md`); release needs both authors' OK |
| `scripts/download_public_inputs.md` | where the public inputs live (e.g. w00's tifxyz for `score_surface.py`) |

**Limits of `score_surface.py`:**
- It cannot faithfully score a surface that crosses a strip plane more than once within ±3 mm. It warns when that happens.
- It says nothing about which of the surface and the rater is on the true sheet.
- Scoring the organizers' w00 through it gives exactly 42/82 and 18/40.
