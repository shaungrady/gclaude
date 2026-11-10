#!/usr/bin/env python3
"""Render multi-part scenes (colored pieces, isometric views) into one PNG.

Use for assembled / exploded / per-piece views of multi-part designs. Parts are
build123d shapes in an in-use frame where +Y is up (as in models/*); they are
rotated so +Y points up in the image.

    from render_scene import render_scenes, ORANGE, BLUE, GRAY
    render_scenes({"Assembled": [(A, ORANGE), (B, BLUE)]}, "out/x/views.png", title="...")

Views default to front-left-above and back-right-above (front = -Z in use).
"""
from __future__ import annotations

import tempfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import trimesh
from build123d import Rot, export_stl

import render as R

ORANGE = np.array([0.95, 0.55, 0.15])
BLUE = np.array([0.3, 0.6, 0.95])
GRAY = np.array([0.65, 0.65, 0.65])
GREEN = np.array([0.35, 0.75, 0.4])

# Views are named from the viewer's position in the in-use frame of models/*:
# +Y up, -Z toward the viewer (front), and +X on the viewer's LEFT when facing
# the part from the front (right-handed: facing +Z with +Y up puts +X on the left).
def _view(left: bool, front: bool, above: bool):
    cam = (1 if left else -1, 0.8 if above else -0.6, -1 if front else 1)  # in-use x, y, z
    rx, ry, rz = cam[0], -cam[2], cam[1]          # same Rot(90, 0, 0) as the meshes
    return (-rx, -ry, -rz)                        # direction from camera toward the model


VIEWS = {
    f"from {fb} {lr}, {ud}": _view(lr == "left", fb == "front", ud == "above")
    for fb in ("front", "back") for lr in ("left", "right") for ud in ("above", "below")
}


def _mesh(shape, tmpdir, i):
    f = Path(tmpdir) / f"p{i}.stl"
    export_stl(Rot(90, 0, 0) * shape, str(f))
    return trimesh.load_mesh(f)


def _image(m, colors, view, center, half):
    fid, _, _ = R._rasterize(m, view, (0, 0, 1), center, half)
    v = np.asarray(view, float) / np.linalg.norm(view)
    light = -v + np.array([0.2, 0.3, 0.8])
    light /= np.linalg.norm(light)
    lum = np.clip(m.face_normals @ light, 0, 1) * 0.6 + 0.35
    img = np.ones((R.RES, R.RES, 3))
    hit = fid >= 0
    img[hit] = np.clip(colors[fid[hit]] * lum[fid[hit], None], 0, 1)
    n = np.zeros((R.RES, R.RES, 3))
    n[hit] = m.face_normals[fid[hit]]
    edge = np.zeros((R.RES, R.RES), bool)
    for dy, dx in ((0, 1), (1, 0)):
        h2 = np.roll(hit, (-dy, -dx), (0, 1))
        n2 = np.roll(n, (-dy, -dx), (0, 1))
        edge |= (hit != h2) | (hit & h2 & ((n * n2).sum(-1) < 0.94))
    img[edge] = (0.12, 0.12, 0.12)
    return img


def render_scenes(scenes: dict, out: str, title: str = "", views=None, zoom=None) -> Path:
    """scenes: {name: [(shape, rgb), ...]}; views: list of VIEWS keys.
    zoom: optional {name: (center_xyz_in_use, half_size_mm)} to frame a detail."""
    views = views or ["from front left, above", "from back right, above"]
    zoom = zoom or {}
    fig, axes = plt.subplots(len(scenes), len(views), figsize=(7 * len(views), 5.5 * len(scenes)),
                             dpi=100, squeeze=False)
    with tempfile.TemporaryDirectory() as tmp:
        for row, (name, parts) in enumerate(scenes.items()):
            meshes = [_mesh(s, tmp, f"{row}_{i}") for i, (s, _) in enumerate(parts)]
            colors = np.vstack([np.tile(c, (len(mm.faces), 1)) for mm, (_, c) in zip(meshes, parts)])
            m = trimesh.util.concatenate(meshes)
            if name in zoom:
                (cx, cy, cz), half = zoom[name]
                center, half = np.array([cx, -cz, cy]), half   # same rotation as the meshes
            else:
                lo, hi = m.bounds
                center, half = (lo + hi) / 2, np.linalg.norm(hi - lo) / 2 * 1.02
            for col, vname in enumerate(views):
                ax = axes[row, col]
                ax.imshow(_image(m, colors, VIEWS[vname], center, half))
                ax.axis("off")
                ax.set_title(f"{name}, {vname}", fontsize=12)
    if title:
        fig.suptitle(title, fontsize=13)
    fig.tight_layout(rect=(0, 0, 1, 0.97 if title else 1))
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out)
    plt.close(fig)
    return out
