#!/usr/bin/env python3
"""Printability checks for an STL on a Prusa MK3S+.

Usage: python tools/check.py part.stl [--overhang 45]

Checks:
  - watertight / manifold mesh
  - fits the MK3S+ build volume (250 x 210 x 210 mm)
  - sits on the bed (min Z == 0) and has a usable first-layer contact area
  - overhang area steeper than the threshold (would need supports)
Prints JSON. Exit code 1 on hard failures.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
import trimesh

BED = (250.0, 210.0, 210.0)  # MK3S+ printable volume, mm


def check(stl: Path, overhang_deg: float = 45.0) -> dict:
    mesh = trimesh.load_mesh(stl)
    lo, hi = mesh.bounds
    size = hi - lo
    errors, warnings = [], []

    if not mesh.is_watertight:
        errors.append("mesh is not watertight")
    if not mesh.is_winding_consistent:
        errors.append("inconsistent face winding")

    fits = all(s <= b for s, b in zip(size, BED))
    fits_rotated = size[0] <= BED[1] and size[1] <= BED[0] and size[2] <= BED[2]
    if not fits:
        if fits_rotated:
            warnings.append("fits only if rotated 90 deg about Z")
        else:
            errors.append(f"exceeds MK3S+ build volume {BED}")

    if abs(lo[2]) > 1e-3:
        warnings.append(f"min Z is {lo[2]:.3f}, not 0 (slicer will drop it to the bed)")

    normals, areas = mesh.face_normals, mesh.area_faces
    z_face = mesh.triangles_center[:, 2]
    on_bed = (normals[:, 2] < -0.999) & (z_face - lo[2] < 1e-3)
    bed_contact = float(areas[on_bed].sum())
    if bed_contact < 25:
        warnings.append(f"small bed contact area ({bed_contact:.1f} mm^2); adhesion risk")

    # Slope measured from horizontal, same convention as PrusaSlicer's
    # support threshold: a downward face whose slope is below the threshold overhangs.
    cos_t = math.cos(math.radians(overhang_deg))
    overhang = (normals[:, 2] < -cos_t) & ~on_bed
    overhang_area = float(areas[overhang].sum())
    if overhang_area > 1.0:
        zs = z_face[overhang]
        warnings.append(
            f"{overhang_area:.1f} mm^2 overhang steeper than {overhang_deg} deg "
            f"(z {zs.min():.1f} to {zs.max():.1f}); supports, bridging, or reorient"
        )

    return {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "bbox_mm": [round(float(s), 3) for s in size],
        "volume_cm3": round(float(mesh.volume) / 1000, 3) if mesh.is_watertight else None,
        "bed_contact_mm2": round(bed_contact, 1),
        "overhang_mm2": round(overhang_area, 1),
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("stl", type=Path)
    ap.add_argument("--overhang", type=float, default=45.0)
    a = ap.parse_args()
    r = check(a.stl, a.overhang)
    print(json.dumps(r, indent=2))
    sys.exit(0 if r["ok"] else 1)
