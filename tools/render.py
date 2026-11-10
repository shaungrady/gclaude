#!/usr/bin/env python3
"""Render an STL from several angles into one PNG (headless, no GPU).

Uses a small numpy z-buffer rasterizer with orthographic projection, flat
shading, and outlines at silhouettes and sharp edges, so occlusion is correct.
Axes are in mm so dimensions can be read off the image.

Usage: python tools/render.py out/part/part.stl [outdir]
Writes <stem>_views.png (2x3 grid: iso, iso back, front, right, top, bottom).
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import trimesh

RES = 700  # pixels per view side

# (title, view direction = from camera toward model, up vector)
VIEWS = [
    ("iso (from -X -Y +Z)", (1, 1, -1), (0, 0, 1)),
    ("iso back (from +X +Y +Z)", (-1, -1, -1), (0, 0, 1)),
    ("front (from -Y)", (0, 1, 0), (0, 0, 1)),
    ("right (from +X)", (-1, 0, 0), (0, 0, 1)),
    ("top (from +Z)", (0, 0, -1), (0, 1, 0)),
    ("bottom (from -Z)", (0, 0, 1), (0, 1, 0)),
]
BASE = np.array([0.95, 0.55, 0.15])  # Prusa orange


def _basis(view, up):
    d = np.asarray(view, float); d /= np.linalg.norm(d)
    u = np.asarray(up, float)
    right = np.cross(d, u); right /= np.linalg.norm(right)
    true_up = np.cross(right, d)
    return right, true_up, d


def _rasterize(mesh: trimesh.Trimesh, view, up, center, half):
    right, upv, d = _basis(view, up)
    v = mesh.vertices - center
    px = (v @ right / half * 0.5 + 0.5) * (RES - 1)
    py = (0.5 - v @ upv / half * 0.5) * (RES - 1)
    pz = v @ d  # larger = farther
    zbuf = np.full((RES, RES), np.inf)
    fid = np.full((RES, RES), -1, dtype=np.int64)

    faces = mesh.faces
    X, Y, Z = px[faces], py[faces], pz[faces]
    for i in range(len(faces)):
        x, y, z = X[i], Y[i], Z[i]
        x0, x1 = max(int(np.floor(x.min())), 0), min(int(np.ceil(x.max())), RES - 1)
        y0, y1 = max(int(np.floor(y.min())), 0), min(int(np.ceil(y.max())), RES - 1)
        if x1 < x0 or y1 < y0:
            continue
        den = (y[1] - y[2]) * (x[0] - x[2]) + (x[2] - x[1]) * (y[0] - y[2])
        if abs(den) < 1e-12:
            continue
        gx, gy = np.meshgrid(np.arange(x0, x1 + 1), np.arange(y0, y1 + 1))
        a = ((y[1] - y[2]) * (gx - x[2]) + (x[2] - x[1]) * (gy - y[2])) / den
        b = ((y[2] - y[0]) * (gx - x[2]) + (x[0] - x[2]) * (gy - y[2])) / den
        c = 1 - a - b
        inside = (a >= -1e-6) & (b >= -1e-6) & (c >= -1e-6)
        if not inside.any():
            continue
        depth = a * z[0] + b * z[1] + c * z[2]
        sub_z = zbuf[y0:y1 + 1, x0:x1 + 1]
        closer = inside & (depth < sub_z)
        sub_z[closer] = depth[closer]
        fid[y0:y1 + 1, x0:x1 + 1][closer] = i
    return fid, zbuf, d


def _shade(mesh, fid, d):
    light = -d + np.array([0.3, 0.2, 0.6])
    light /= np.linalg.norm(light)
    lum = np.clip(mesh.face_normals @ light, 0, 1) * 0.6 + 0.35
    img = np.ones((RES, RES, 3))
    hit = fid >= 0
    img[hit] = np.clip(np.outer(lum[fid[hit]], BASE), 0, 1)

    # Outlines: silhouette plus boundaries between faces with different normals.
    n = np.zeros((RES, RES, 3))
    n[hit] = mesh.face_normals[fid[hit]]
    edge = np.zeros((RES, RES), bool)
    for dy, dx in ((0, 1), (1, 0)):
        h2 = np.roll(hit, (-dy, -dx), (0, 1))
        n2 = np.roll(n, (-dy, -dx), (0, 1))
        sharp = (hit != h2) | (hit & h2 & ((n * n2).sum(-1) < 0.94))
        edge |= sharp
    img[edge] = (0.12, 0.12, 0.12)
    return img


def render(stl: Path, outdir: Path | None = None) -> list[Path]:
    stl = Path(stl)
    outdir = Path(outdir or stl.parent)
    mesh = trimesh.load_mesh(stl)
    lo, hi = mesh.bounds
    center = (lo + hi) / 2
    half = np.linalg.norm(hi - lo) / 2 * 1.08  # fits any view direction

    fig, axes = plt.subplots(2, 3, figsize=(15, 10.5), dpi=100)
    for ax, (title, view, up) in zip(axes.flat, VIEWS):
        fid, _, d = _rasterize(mesh, view, up, center, half)
        img = _shade(mesh, fid, d)
        right, upv, _ = _basis(view, up)
        cr, cu = center @ right, center @ upv
        ax.imshow(img, extent=(cr - half, cr + half, cu - half, cu + half))
        ax.set_title(title, fontsize=10)
        ax.tick_params(labelsize=7)
        ax.grid(alpha=0.25)
        axis_name = lambda vec: next((("+" if c > 0 else "-") + "XYZ"[k]
                                      for k, c in enumerate(vec) if abs(c) > 0.99), "")
        ax.set_xlabel(f"mm {axis_name(right)}", fontsize=8)
        ax.set_ylabel(f"mm {axis_name(upv)}", fontsize=8)
    size = hi - lo
    fig.suptitle(f"{stl.stem}   bbox {size[0]:.1f} × {size[1]:.1f} × {size[2]:.1f} mm   "
                 f"(z=0 is the print bed)", fontsize=12)
    fig.tight_layout()
    out = outdir / f"{stl.stem}_views.png"
    fig.savefig(out)
    plt.close(fig)
    return [out]


if __name__ == "__main__":
    for p in render(Path(sys.argv[1]), Path(sys.argv[2]) if len(sys.argv) > 2 else None):
        print(p)
