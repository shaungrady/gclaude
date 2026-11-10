#!/usr/bin/env python3
"""Printability checks for an STL on a Prusa MK3S+.

Usage: python tools/check.py part.stl [--overhang 45]

Checks:
  - watertight / manifold mesh
  - fits the MK3S+ build volume (250 x 210 x 210 mm)
  - sits on the bed (min Z == 0) and has a usable first-layer contact area
  - overhang area steeper than the threshold (would need supports)
  - per body: inverted normals, floating above the bed, bodies overlapping each other
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

    # Per-body checks: an STL may hold several parts laid out for printing.
    shells = mesh.split(only_watertight=False)
    z0 = mesh.bounds[0][2]

    def _pts(m, n=20000):
        v = m.vertices
        return v if len(v) <= n else v[np.random.default_rng(0).choice(len(v), n, replace=False)]

    # A negative-volume shell fully enclosed by another body is a sealed cavity
    # (e.g. an embedded magnet pocket), not an inside-out part.
    pos = [sh for sh in shells if not (sh.is_watertight and sh.volume <= 0)]
    bodies, cavities = [], 0
    for sh in shells:
        neg = sh.is_watertight and sh.volume <= 0
        if neg and any(o.is_watertight and o.contains(_pts(sh)).all() for o in pos):
            cavities += 1
        else:
            bodies.append(sh)
    if cavities:
        warnings.append(f"{cavities} sealed internal cavit{'y' if cavities == 1 else 'ies'} "
                        f"(intended? needs a print pause to embed anything)")

    gap_min = 0.3   # closer than ~one extrusion width prints fused
    for i, b in enumerate(bodies):
        if b.is_watertight and b.volume <= 0:
            errors.append(f"body {i}: inverted normals (negative volume)")
        if b.bounds[0][2] - z0 > 1e-3:
            errors.append(f"body {i}: floats {b.bounds[0][2] - z0:.2f} mm above the bed")
            continue
        down = (b.face_normals[:, 2] < -0.999) & (b.triangles_center[:, 2] - z0 < 1e-3)
        contact = float(b.area_faces[down].sum())
        if contact < 1:
            errors.append(f"body {i}: no flat face on the bed (tilted or point contact)")
        elif contact < 25:
            warnings.append(f"body {i}: small bed contact area ({contact:.1f} mm^2); adhesion risk")
    for i in range(len(bodies)):
        for j in range(i + 1, len(bodies)):
            a_, c_ = bodies[i], bodies[j]
            lo_ = np.maximum(a_.bounds[0], c_.bounds[0]) - gap_min
            hi_ = np.minimum(a_.bounds[1], c_.bounds[1]) + gap_min
            if not np.all(hi_ > lo_):
                continue            # bounding boxes are farther apart than gap_min
            # Real geometry check: interpenetration, then surface-to-surface gap.
            if (c_.is_watertight and c_.contains(_pts(a_)).any()) or \
               (a_.is_watertight and a_.contains(_pts(c_)).any()):
                errors.append(f"bodies {i} and {j} intersect; they would print fused")
                continue
            d = min(trimesh.proximity.closest_point(c_, _pts(a_))[1].min(),
                    trimesh.proximity.closest_point(a_, _pts(c_))[1].min())
            if d < gap_min:
                errors.append(f"bodies {i} and {j} are {d:.2f} mm apart; they would print fused")

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
    bed_contact = float(areas[on_bed].sum())   # total; per-body thresholds are checked above

    # Slope measured from horizontal, same convention as PrusaSlicer's
    # support threshold: a downward face whose slope is below the threshold overhangs.
    cos_t = math.cos(math.radians(overhang_deg))
    overhang = (normals[:, 2] < -cos_t - 1e-3) & ~on_bed  # tolerance: exactly 45 deg is fine
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
        "bodies": len(bodies),
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
