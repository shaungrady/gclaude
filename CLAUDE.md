# gclaude: functional parts for a Prusa MK3S+

Pipeline: build123d script → STEP/STL/3MF → render + printability check → PrusaSlicer CLI → G-code.

## Setup

```bash
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
```

PrusaSlicer must be on PATH (`prusa-slicer`) or set `PRUSA_SLICER=/path/to/PrusaSlicer`.

## Workflow when asked to model a part

1. Clarify what's ambiguous and matters for fit: mating dimensions, screw sizes, load direction, clearances. Don't ask about things with sane defaults.
2. Write `models/<name>.py` exposing `build(**params)` with every dimension as a keyword parameter (mm). Put a docstring stating the print orientation and model frame.
3. Model in print orientation: the face that goes on the bed at z=0, part in +Z.
4. Run `python tools/build.py models/<name>.py`. Read the JSON, then **look at** `out/<name>/<name>_views.png` with the Read tool. Fix anything that looks wrong before going further; don't trust code alone.
5. Resolve check errors. Treat overhang warnings seriously: reorient, add 45° chamfers instead of flat ceilings, or teardrop horizontal holes before accepting supports.
6. Slice: `python tools/slice.py out/<name>/<name>.3mf` (add `--3mf` for a project file the user can open in PrusaSlicer). Report time, filament, and anything surprising.
7. Iterate with `--set key=value` on build.py for parameter tweaks instead of editing defaults.
   Values are Python literals (`1.5`, `(1, 2)`, `None`); `true`/`false` work too; anything else is a
   string. `--set` needs a `build()` function. For multi-part designs, check fit and install paths in
   an `assembled` layout with build123d booleans, and render with `tools/render_scene.py`.

Notes:
- slice.py `--set` takes PrusaSlicer config-file keys (`support_material=1`, `fill_density=25%`).
- The PrusaSlicer CLI re-arranges objects on the bed, so a model's print layout only matters when the
  3MF is opened in the GUI. check.py still flags bodies that overlap or float in the layout.

## Slicing defaults for functional parts

The bundled profiles are Prusa's stock presets (2 perimeters, 15% infill), tuned for looks.
For load-bearing parts pass `--set perimeters=4 --set fill_density=40%` (or more) to slice.py; perimeters add more strength than infill.
Profiles: `mk3s_pla_0.15mm.ini` (detail), `mk3s_pla_0.20mm.ini` (default), `mk3s_pla_0.30mm.ini` (draft).
Regenerate or add filaments with `tools/flatten_profile.py` against `/usr/share/PrusaSlicer/profiles/PrusaResearch.ini`.
The MK3S+ takes plain `.gcode` (not binary `.bgcode`).

## Design rules for FDM on a 0.4 mm nozzle

- Walls: multiples of the 0.45 mm extrusion width; ≥1.2 mm, ≥2 mm for anything load bearing.
- Clearance for parts that must fit together: 0.2 mm per side for sliding fit, 0.1 mm for snug. Holes print undersized; add ~0.2 mm to diameter for screw clearance.
- Overhangs ≤45° without supports; bridges ≤~10 mm are fine.
- Horizontal holes: teardrop or flat-top them if > ~8 mm diameter.
- Strength: layer lines are the weak axis. Orient so loads run along layers, not across them.
- Fillet or chamfer inside corners under load. Chamfer the bottom edge ~0.4 mm to hide elephant foot on mating faces.
- Heat-set inserts (M3): hole 4.0–4.2 mm, depth insert length + 1 mm. Nut traps: M3 hex 5.5 mm flats + 0.3 mm.
- MK3S+ build volume: 250 × 210 × 210 mm.

## Joinery reference

Before designing any joint between parts (screws, inserts, snaps, dovetails, pins, press fits, glue, splits, adhesive mounting), read `refs/joinery/README.md` and the relevant doc(s) there. Prefer their numbers over the short rules above, and mind the [derived]/[unverified] tags.

## Layout

- `models/`: part scripts (source of truth; commit these)
- `tools/build.py`: export + render + check
- `tools/render.py`: 6-view PNG of an STL
- `tools/render_scene.py`: colored multi-part scenes (exploded/assembled), named views, zoomed close-ups
- `tools/check.py`: watertight, build-volume fit, bed contact, overhangs; per body: inverted, floating, overlapping
- `tools/slice.py`: PrusaSlicer CLI wrapper, parses estimates from G-code
- `tools/flatten_profile.py`: resolve vendor preset inheritance into a single CLI `.ini`
- `profiles/`: flattened PrusaSlicer `.ini` configs
- `refs/`: reference data (controller dimensions, joinery library in `refs/joinery/`)
- `out/`: generated, gitignored
