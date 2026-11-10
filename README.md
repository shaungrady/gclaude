# gclaude

Agentic toolkit for Claude to design functional parts and slice them for a Prusa MK3S+.

```
models/<part>.py  ──build.py──▶  STEP / STL / 3MF  ──▶  6-view render + printability check
                                        │
                                        └──slice.py (PrusaSlicer CLI)──▶  .gcode
```

- **CAD:** [build123d](https://github.com/gumyr/build123d) (OpenCascade B-rep). Parametric, real fillets/chamfers, exports STEP so you can keep editing in other CAD tools.
- **Feedback loop:** `render.py` produces a 6-view image with mm axes that Claude reads to catch geometry mistakes. `check.py` flags non-manifold meshes, build-volume overflow, poor bed contact, and overhangs.
- **Slicing:** PrusaSlicer CLI with profiles in `profiles/`. The 3MF also opens directly in PrusaSlicer if you'd rather slice by hand.

## Quick start

```bash
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
```

```bash
python tools/build.py models/wall_bracket.py --set width=25 --set thickness=6
```

```bash
python tools/slice.py out/wall_bracket/wall_bracket.3mf --3mf
```

## Profiles

`profiles/mk3s_pla_{0.15,0.20,0.30}mm.ini` are flattened from PrusaSlicer's bundled
"0.15mm QUALITY", "0.20mm QUALITY" and "0.30mm DRAFT" @MK3 print presets with "Prusament PLA" on
"Original Prusa i3 MK3S & MK3S+" (`tools/flatten_profile.py`; 0.20 mm is the default).
To use your own tuned settings instead: in PrusaSlicer select your presets, then
**File → Export → Export Config** and save into `profiles/`.

See `CLAUDE.md` for the workflow and FDM design rules Claude follows.
