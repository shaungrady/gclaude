#!/usr/bin/env python3
"""Slice a 3MF/STL with the PrusaSlicer CLI using profiles in profiles/.

Usage:
  python tools/slice.py out/part/part.3mf [--profile profiles/mk3s_pla_0.20mm.ini]
                        [--set key=value ...] [--3mf]

--set passes PrusaSlicer config overrides, e.g. --set fill_density=40% --set perimeters=4
--3mf also writes a project 3MF with the config embedded, to open in PrusaSlicer.
Prints JSON with output paths and estimates parsed from the G-code.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PROFILE = ROOT / "profiles" / "mk3s_pla_0.20mm.ini"


def find_slicer() -> str:
    for name in (os.environ.get("PRUSA_SLICER"), "prusa-slicer", "PrusaSlicer",
                 "/Applications/PrusaSlicer.app/Contents/MacOS/PrusaSlicer"):
        if name and (shutil.which(name) or Path(name).exists()):
            return shutil.which(name) or name
    sys.exit("PrusaSlicer not found; set PRUSA_SLICER to its executable")


def estimates(gcode: Path) -> dict:
    keys = {
        "estimated printing time (normal mode)": "time",
        "filament used [mm]": "filament_mm",
        "filament used [g]": "filament_g",
        "total filament used [g]": "filament_g",
        "filament_type": "filament_type",
        "layer_height": "layer_height",
        "fill_density": "fill_density",
        "perimeters": "perimeters",
        "support_material": "supports",
    }
    found = {}
    with open(gcode, errors="replace") as f:
        for line in f:
            m = re.match(r";\s*([^=]+?)\s*=\s*(.+)", line)
            if m and m.group(1) in keys:
                found[keys[m.group(1)]] = m.group(2).strip()
    return found


def slice_model(model: Path, profile: Path = DEFAULT_PROFILE, overrides=(), project=False) -> dict:
    slicer = find_slicer()
    out_gcode = model.with_suffix(".gcode")
    base = [slicer, "--load", str(profile)]
    for o in overrides:
        k, _, v = o.partition("=")
        base += [f"--{k.replace('_', '-')}", v]
    cmd = base + ["--export-gcode", "--output", str(out_gcode), str(model)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    result = {"cmd": cmd, "returncode": r.returncode}
    if r.returncode != 0 or not out_gcode.exists():
        result["error"] = (r.stderr or r.stdout)[-3000:]
        return result
    result["gcode"] = str(out_gcode)
    result["estimates"] = estimates(out_gcode)
    if project:
        out_3mf = model.with_name(model.stem + "_project.3mf")
        subprocess.run(base + ["--export-3mf", "--output", str(out_3mf), str(model)],
                       capture_output=True, text=True)
        result["project_3mf"] = str(out_3mf)
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("model", type=Path)
    ap.add_argument("--profile", type=Path, default=DEFAULT_PROFILE)
    ap.add_argument("--set", action="append", default=[], metavar="KEY=VALUE")
    ap.add_argument("--3mf", dest="project", action="store_true")
    a = ap.parse_args()
    res = slice_model(a.model, a.profile, a.set, a.project)
    print(json.dumps(res, indent=2))
    sys.exit(0 if "gcode" in res else 1)
