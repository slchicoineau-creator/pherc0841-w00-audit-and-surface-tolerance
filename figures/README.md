# Figures

Pre-rendered by the authors from the blind rating pages, which are not in this repo; the calls printed on each picture are checked against the README by that build.
In figures 1 and 2, each tile is the JPEG exactly as embedded in the blind rating page, so the orientation is the one the raters saw. The picture
name comes from the released page key; the two calls ("rows", "strokes" or "nothing") are each rater's recorded answer on that
page. Blanks, calibration pictures and other fillers from the same pages are not shown. The script stops if any call
differs from the README's wording. The 5 mm bar under each tile of figures 1 and 2 is drawn outside the picture: every tile
is an ink map on the render grid of 2.403 µm pixels (meshes at 20 voxels per vertex), cropped to 8320 × 4877 pixels
(19.99 × 11.72 mm) and resized to 800 × 469, so 1 page pixel = 25.0 µm (nominal grid spacing, not a measured length).

Rules for every figure here: a scale bar and the scan/licence line on the image; "one picture per level" or "not a rate"
on every human-call or picked figure; pair wording on any README row 5 figure; each figure was cleared for release.
All three: Chris checked the captions, and both authors OK'd releasing the page keys and calls they show.

## Figure 1: `fig1_humantol_fullhop.png`

Ink maps (white = predicted ink) of the PHerc0841 known-text window W (about 20 × 12 mm), built on the w00 surface. Top row:
the HUMAN-TOL page (Sebastien 10-03, Chris 10-06): undamaged control (L100), ~30 % dispersed (L70) and clustered (C70)
displacement of less than one sheet, 30 % holes (H70) and 50 % holes (H50). Bottom row: the FULL-HOP-W page (one sitting; Chris 10-11 23:02 UTC,
Sebastien 10-12 01:08 UTC): its control, L70 and C70 rebuilt with every damaged patch moved a full sheet (L70d, C70d), and its two guards
(60 % full hops, L40d; 50 % holes, H50n). Calls are as recorded on these pages only; later re-ratings of the same H50 are in
README row 2. One picture per level, two raters: a description, not a threshold.
Sources: `[private path]` + `humantol_key.json`;
`[private path]` + `fh_page_key.json`; ratings in
`ratings/seb/` and `ratings/partner/` (`humantol_ratings.json`, `fullhop_ratings.json`).
Scan: PHerc0841, Vesuvius Challenge open data, CC BY-NC 4.0.

## Figure 2: `fig2_tol814_linefield.png`

Ink maps of the organizers' labelled surface s022814, all from one 11-picture page rated in one sitting (Chris 10-11 23:03 UTC,
Sebastien 10-12 01:10 UTC). TOL-814: undamaged control (ctrl814), ~15 %, ~30 % and ~45 % of the field moved a full sheet
(L85_814, L70_814, L55_814; the 45 % picture holds every 30 % hop plus 15 % more) and the 50 % holes guard (H50_814).
LINE-FIELD-READ: 10 constant-height lines cut from s022814 itself, ~2 mm apart by design (1.80 mm measured, O2), and 5 lines ~4.5 mm apart by design (4.05 mm measured, O45),
joined by the sheet-direction fill; an oracle check of line spacing, not a traced route. The 30 % and 45 % calls are
crossed between the raters. One picture per level: a description, not a threshold.
Sources: `[private path]` + `t8_page_key.json`; ratings in
`ratings/seb/tol814_ratings.json` and `ratings/partner/tol814_ratings.json`.
Scan: PHerc0841 (s022814 is the organizers' surface on it), Vesuvius Challenge open data, CC BY-NC 4.0.

## Figure 3: `fig3_w00native.png`

W00-NATIVE (a computer measure; not the guide-free w00 audit W00-AUDIT-FRESH of README row 5): the organizers' w00 surface
(green line) in cross-section at 12 crosses on PHerc0841. Left: the 2.4 µm scan, read at 9.6 µm (band level 2), with the
copy of w00 moved there by one affine transform. Right: w00's own 9.366 µm scan with the original mesh. Both panels are
~9.5 µm pictures; the 2.4 µm detail is not shown. Each cross is 1.5 mm along w00 by 0.6 mm across the sheets; each panel
has its own 0.5 mm bar. A25 = share of the trace with no papyrus within 25 µm. The 12 crosses are 4 picked at random
(seeded) from each third of the copy's A25, so the sheet is not a rate; over all 6 479 crosses, 17.0 % (copy) and 16.9 %
(own scan) have A25 > 0.3 (W00-NATIVE result in the authors' private notes; the README does not quote these two numbers). Pre-loop test, no loop Judge verdict; Chris's caption check is its only review.
The tiles are cut whole from the 2026-10-05 picture sheet (no re-render, no resampling; the build stops if its sha256
b925ce0a… or its gap pixels change); the small yellow text in each tile is that sheet's own label.
Sources: `[private path]` (made by `[private path]
pictures`, `standalone/preregs/w00_native_scan.md`); result in `[private path]`.
No marks, keys or ratings are used. A planned panel b (one 2.4 µm bend strip) is not included: no mark-free 2.4 µm picture
of it with the w00 trace exists, and making one would be a new render.
Scan: PHerc0841, Vesuvius Challenge open data, CC BY-NC 4.0.
