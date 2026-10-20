# Public inputs (only needed for the GPU / tifxyz parts)

The data-free parts of this repository (the `numbers/` checks, the tests and the pre-registrations) need nothing from below.
Rebuilding pictures, reader maps or audit geometry from scratch needs the organizers' public PHerc0841 data. Everything listed
here is on the organizers' open-data hosting (Vesuvius Challenge open data, licence CC BY-NC 4.0, no login). Each key is
given in its S3 form; the same key works over HTTPS at
`https://vesuvius-challenge-open-data.s3.us-east-1.amazonaws.com/<key>`.

Base: `s3://vesuvius-challenge-open-data/`

| input | key (relative to the base) |
|---|---|
| PHerc0841 2.4 µm volume (2.403 µm, 77 keV) | `PHerc0841/volumes/20260319124803-2.403um-0.2m-77keV-masked.zarr` |
| PHerc0841 9.366 µm volume (113 keV) | `PHerc0841/volumes/20250821151531-9.366um-1.2m-113keV-masked.zarr` |
| w00 surface on the 9.366 µm scan (tifxyz) | `PHerc0841/segments/20260220213127-w00/mesh/20260220213127-on-20250821151531-9.366um.tifxyz/` |
| w00 surface on the 2.4 µm scan (tifxyz) | `PHerc0841/segments/20260220213127-w00/mesh/20260220213127-on-20260319124803-2.403um.tifxyz/` |
| w00 surface volumes | `PHerc0841/segments/20260220213127-w00/surface-volumes/` |
| organizers' 2.4 µm ink prediction on w00 (the reference map of `numbers/reader_phase`) | `PHerc0841/segments/20260220213127-w00/ink-detection/PHerc0841-20260220213127-2.403um-0.22m-77keV-volume-20260319124803-20260417190342-new_canon_autoresearch_recipe-tile256-stride128.tif` |
| s022814 surface on the 9.366 µm scan (tifxyz) | `PHerc0841/segments/20260221022814-auto_grown_20260220174252405/mesh/20260221022814-on-20250821151531-9.366um.tifxyz/` |
| s022814 surface on the 2.4 µm scan (tifxyz) | `PHerc0841/segments/20260221022814-auto_grown_20260220174252405/mesh/20260221022814-on-20260319124803-2.403um.tifxyz/` |
| s022814 surface volumes | `PHerc0841/segments/20260221022814-auto_grown_20260220174252405/surface-volumes/2.403um-0.22m-77keV-volume-20260319124803.zarr/` and `.../surface-volumes/9.366um-1.2m-113keV-volume-20250821151531.zarr/` |
| s022814 ink labels (2.4 µm; `inklabels.zarr`, `supervision.zarr`, `validation.zarr`) | `PHerc0841/segments/20260221022814-auto_grown_20260220174252405/ink-labels/2.403um-volume-20260319124803/20260918/` |
| organizers' 2.4 µm ink prediction on s022814 | `PHerc0841/segments/20260221022814-auto_grown_20260220174252405/ink-detection/PHerc0841-20260221022814-2.403um-0.22m-77keV-volume-20260319124803-20260417190342-new_canon_autoresearch_recipe-tile256-stride128.tif` |
| s214732 surface on the 9.366 µm scan (tifxyz) | `PHerc0841/segments/20260220214732-auto_grown_20260220144552896/mesh/20260220214732-on-20250821151531-9.366um.tifxyz/` |
| s214732 surface volumes | `PHerc0841/segments/20260220214732-auto_grown_20260220144552896/surface-volumes/2.403um-0.22m-77keV-volume-20260319124803.zarr/` and `.../surface-volumes/9.366um-1.2m-113keV-volume-20250821151531.zarr/` |
| organizers' 2.4 µm ink prediction on s214732 | `PHerc0841/segments/20260220214732-auto_grown_20260220144552896/ink-detection/PHerc0841-20260220214732-2.403um-0.22m-77keV-volume-20260319124803-20260417190342-new_canon_autoresearch_recipe-tile256-stride128.tif` |
| public m7 surface predictions (optional; used to build the hop doses) | `PHerc0841/representations/predictions/surfaces/20250821151531-surface-20260413222639-surface-m7-L0-th0.2.zarr` (9.366 µm) and `PHerc0841/representations/predictions/surfaces/20260319124803-surface-20260413222639-surface-m7-L2-th0.2.zarr` (2.4 µm) |

Example (one file over HTTPS):

```
curl -o w00_ink_2um.tif "https://vesuvius-challenge-open-data.s3.us-east-1.amazonaws.com/PHerc0841/segments/20260220213127-w00/ink-detection/PHerc0841-20260220213127-2.403um-0.22m-77keV-volume-20260319124803-20260417190342-new_canon_autoresearch_recipe-tile256-stride128.tif"
```

**For `audit/score_surface.py`, use the w00 copy on the 2.403 µm volume** (about 9 MB; the scorer works in that volume's
voxel coordinates):

```
aws s3 sync --no-sign-request "s3://vesuvius-challenge-open-data/PHerc0841/segments/20260220213127-w00/mesh/20260220213127-on-20260319124803-2.403um.tifxyz/" w00_2um.tifxyz/
python audit/score_surface.py score w00_2um.tifxyz --expect-w00
```

The organizers' original w00 on the 9.366 µm scan (not for `score_surface.py` unless you pass a 9.366 → 2.403 µm `--affine`):

```
aws s3 sync --no-sign-request "s3://vesuvius-challenge-open-data/PHerc0841/segments/20260220213127-w00/mesh/20260220213127-on-20250821151531-9.366um.tifxyz/" w00_9um.tifxyz/
```

Not listed here: the two ink readers' checkpoints (Hecate 2.4 and Hecate 9.6) and the lasagna / VC3D tools; get them from the
organizers' own pages and repositories (villa). The volumes are very large; download only the crops you need.
