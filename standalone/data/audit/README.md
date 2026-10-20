# data/audit: mark-free geometry for the w00 audit

`guidefree_strips.json` holds the 25 strips of the guide-free audit: 16 in the primary pool
(10 fresh along strips, 7 bend / 3 flat, plus 6 cross strips at the development sites) and 9 in the
fresh cross replication pool. No human mark is in this folder.

## Coordinate frame and units

- Coordinates: x, y, z voxel indices (level 0) of the public PHerc0841 2.403 um volume 20260319124803-2.403um-0.2m-77keV-masked.zarr (s3://vesuvius-challenge-open-data/PHerc0841/volumes/). Strip coordinates: s (mm) along the strip axis t, n (mm) along the strip normal n, from the frame origin o; a point (s, n) is o + (s * t + n * n) * 1000 / 2.403 voxels.
- `frame.o_vx` is the strip frame origin (voxels); `t`, `n`, `w` are unit vectors (w = t x n). `L_mm` is the strip length.
- `station_s_mm[k]`: the 7 station positions along the strip (k = 0 is the shared w00 start; k = 1..6 are scored, 0.75-4.5 mm from it).
  Each station's search line is the line through `station_line_origin_vx[k]` along `n`.
- `w00_n_mm[k]`: where the organizers' w00 mesh crosses station k's search line (mm along n); `w00_point_vx[k]` is that point in voxels.
  `null` = no w00 trace there (2 stations, both at k = 6 and both without a mark, so no scored station lacks w00). `w00_gap_mm[k]`: distance to the nearest valid 0.02 mm trace bin (description).
- `seed_n_mm`: the w00 start at station 0 (equals `w00_n_mm[0]` within 1 um on every strip: the mark-free frame check).
- `kind`: bend / flat (fresh along strips), cross (cross strips at the development sites), fresh_cross (replication pool).
- Tolerance for agreement: 75 um along n.

## How w00's position at a station was computed

w00 densified x10 (bilinear), points within 1.2 voxels of the strip plane and |n| <= 3 mm, median n per 0.02 mm s-bin, linear interpolation between valid bins (`audit/score_surface.py` does the same for any tifxyz surface).
The w00 surface is public: `s3://vesuvius-challenge-open-data/PHerc0841/segments/20260220213127-w00/mesh/20260220213127-on-20260319124803-2.403um.tifxyz/`.
