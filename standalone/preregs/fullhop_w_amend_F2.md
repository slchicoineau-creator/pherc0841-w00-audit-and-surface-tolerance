> **Scrubbed public copy** (public name `fullhop_w`). The original was first committed to the authors' private repository at `a10666ff0` (2026-10-11T17:24:38Z). Timing: Page amendment for the shared page; committed before the page build and before any rating (Judges' checks). Timestamps live in a private repository; ask the authors for a verification. Scrubbing removed mentions of non-public scrolls and local paths (paths into the authors' private repository read `[private path]` and do not resolve) and replaced internal item ids and test names with public slugs (unmapped internal ids read `[internal item]`); the scientific text is otherwise unchanged.

# fullhop_w: page amendment F2 (2026-10-11 ~12:40 CDT, Runner)

Written for line_spacing (`preregs/line_spacing.md`, "Amendments needed in the two damage tests"), after Sebastien's
A of 2026-10-11 12:01 and the main session's unpark at 12:21. Before any fullhop_w page, rating or picture view exists:
`fh_page_key.json`, `fullhop_rating.html` and every rating file are absent, and nobody has seen a fullhop_w tile. Public code only.
This changes only the PAGE step of `preregs/fullhop_w.md`; its arms, Stage 0, bars and outcome rules are unchanged.

What changed in `[private path]` (sha256 before a7708cf3..., after edbb1f6a49cf...):
1. `fh.py page <extra.json>`: an extra entry may carry its own `item` tag (before: `dict(item="fullhop_s022814", **meta)` raised on a meta
   with an `item` key). Default tag stays `fullhop_s022814`.
2. `fh.py rater` ignores `line_spacing` pictures (O2, O45) as well as `fullhop_s022814`'s: they never count in fullhop_w's validity,
   FAILS, HOLDS or lenient line.
3. Adjacency: after the frozen shuffle (`default_rng(20261008)`), if O2 and O45 are next to each other, O45 swaps with the picture
   after it (the one before it if last; if that is O2, the nearest slot that leaves them apart); the swap is written into that
   picture's entry in `fh_page_key.json` (`adjacency_swap`).
4. 1 MB: if the built page is over 1,000,000 bytes, `page` deletes the page and its key, prints `PAGE_OVER_1MB` and exits 4
   (before: the oversized file stayed behind). Fallback, as fullhop_s022814's prereg already says: the Runner builds fullhop_w's own page
   with no extras (`fh.py page`) and fullhop_s022814's `t8.py page` carries the 814 pictures plus O2 / O45 from the same extra file;
   both are rated in the one sitting. fullhop_w's own scoring does not change in either case.
5. `fh.py selftest` gains the O-picture cases (rater ignores O; adjacency in 5 positions incl. the ends; a good order untouched);
   it still passes (8 verdict cases + the new checks).

NOT changed here (other stations): fullhop_s022814's masked tiles and `t8.py page` (its station); the masked 814 pictures come from
`lf_page_extra_key.json`, written by line_spacing's job 2. fullhop_w's W pictures are another window and are not masked.
The code edit in `fh.py` is uncommitted: the Planner commits it with this note.
