"""Cabinet wall mount for the AC Infinity Controller 2 (AI-ATC), screwed.

One piece: a wall plate (Command strips) on the cabinet's left wall, a C-shaped
front frame the controller's plate screws to, and top/bottom shelves that brace
the frame back to the wall plate. The controller's body passes through the
frame; its rear ports stay open to the back.

The frame is open on the right (no right leg). Once screwed on, the controller's
own metal plate ties the top and bottom rails together. The two right screws go
into 45-degree corner ears on the rail ends.

Print orientation: wall plate face down on the bed (smooth strip surface).
In that orientation the right side of the frame is at the top of the print. A
right leg there would be a 70 mm unsupported bridge over the body opening; the
ears instead grow outward at 45 degrees from the rails. No supports, no bridges.

Strip face: 100 x 79 mm. Two Large Command strips (19 x 92 mm) run front to
back, one along the top edge and one along the bottom, which puts them as far
apart as possible against both twisting loads: button presses (resisted over the
plate's depth) and the controller's weight (resisted over its height).
Point the pull tabs toward the back.

Dimensions: refs/ac_infinity_controller2.md (manufacturer specs, not yet measured).
Screw the controller on before sticking the mount up: the wall-side screws are
6 mm from the wall.

In-use frame (mm):
  X = width, centered on the controller; x=-plate_w/2 is the cabinet wall
  Y = up; y=0 is the bottom edge of the controller's front plate
  Z = depth, +Z back into the cabinet; z=0 is the frame's front face
layout="print" (default) lays it wall-face down; "assembled" leaves it in the
in-use frame, with a phantom controller if show_unit=True.
"""
import math

from build123d import Box, Compound, Cylinder, Plane, Polygon, Pos, Rot, extrude


def _box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _prism_xz(pts, y0, y1):
    """Extrude an (X, Z) polygon along Y from y0 to y1."""
    face = Plane.XZ.offset(-y0) * Polygon(*pts, align=None)
    return extrude(face, amount=y1 - y0, dir=(0, 1, 0))


def _prism_xy(pts, z0, z1):
    """Extrude an (X, Y) polygon along Z from z0 to z1."""
    face = Plane.XY.offset(z0) * Polygon(*pts, align=None)
    return extrude(face, amount=z1 - z0, dir=(0, 0, 1))


def build(
    plate_w: float = 135.0,     # controller front plate
    plate_h: float = 79.0,
    body_w: float = 112.0,      # controller body behind the plate
    body_h: float = 68.0,
    body_d: float = 26.0,       # 28 overall minus ~2 mm plate (unverified)
    cut_w: float = 114.0,       # opening for the body (AC Infinity cut hole size)
    cut_h: float = 70.0,
    hole_dx: float = 123.0,     # screw spacing (template + product photo)
    hole_dy: float = 67.0,
    pilot_d: float = 2.5,       # M3 / #4 thread-forming screws into PLA
    frame_t: float = 4.0,       # front frame thickness
    ear_d: float = 8.0,         # right corner ear depth = right screw bite
    ear_clear: float = 0.5,     # ear start, past the body's side
    wall_t: float = 3.0,        # wall plate thickness
    depth: float = 100.0,       # wall plate depth; deeper = less strip peel from button presses
    shelf_t: float = 3.0,       # top/bottom brace shelves
    shelf_root: float = 45.0,   # shelf depth at the wall plate (front face to back edge)
    shelf_tip: float = 8.0,     # shelf depth behind the frame at the far (right) end
    layout: str = "print",      # "print" or "assembled"
    show_unit: bool = False,
):
    W = plate_w / 2
    H = plate_h
    cy = H / 2
    cut_l = -cut_w / 2
    cut_b, cut_t = cy - cut_h / 2, cy + cut_h / 2
    body_b, body_t = cy - body_h / 2, cy + body_h / 2
    hx, hy = hole_dx / 2, hole_dy / 2
    ex = body_w / 2 + ear_clear          # x where the 45-degree ear edge starts

    # Material between each right pilot and the ear's 45-degree edge.
    # Edge line (bottom ear): y = cut_b + (x - ex); distance from the hole center.
    ear_wall = abs((cy - hy) - cut_b - (hx - ex)) / math.sqrt(2) - pilot_d / 2

    # Guard against parameter combos that silently make bad geometry
    assert layout in ("print", "assembled"), f"unknown layout {layout!r}"
    assert body_w < cut_w and body_h < cut_h, "body must fit the opening"
    assert -hx + pilot_d / 2 < cut_l - 1.0, "left pilots break into the opening"
    assert hx + pilot_d / 2 < W - 1.0, "pilot holes break out of the frame edge"
    assert ear_wall >= 1.0, f"only {ear_wall:.2f} mm of ear around the right pilots"
    assert shelf_t < body_b and H - shelf_t > body_t, "shelves hit the body"
    assert 0 < cut_b and cut_t < H, "opening must leave top and bottom rails"

    # Wall plate
    part = _box(-W, -W + wall_t, 0, H, 0, depth)
    # C-shaped front frame: left leg + top and bottom rails, open on the right
    part += _box(-W, W, 0, H, 0, frame_t)
    part -= _box(cut_l, W + 1, cut_b, cut_t, -1, frame_t + 1)
    # Right corner ears: triangles growing at 45 deg from the rails
    rise = W - ex
    part += _prism_xy([(ex, cut_b), (W, cut_b), (W, cut_b + rise)], 0, ear_d)
    part += _prism_xy([(ex, cut_t), (W, cut_t - rise), (W, cut_t)], 0, ear_d)
    part += _box(ex, W, 0, cut_b, 0, ear_d)          # rail behind the bottom ear
    part += _box(ex, W, cut_t, H, 0, ear_d)          # rail behind the top ear
    # Top and bottom shelves: shelf_root deep at the wall, tapering to shelf_tip
    shelf = [(-W, frame_t), (W, frame_t), (W, frame_t + shelf_tip), (-W, min(shelf_root, depth))]
    part += _prism_xz(shelf, 0, shelf_t)
    part += _prism_xz(shelf, H - shelf_t, H)

    # Screw pilots (left ones go through the 4 mm leg; right ones are 8 mm deep in the ears)
    for sx in (-1, 1):
        for sy in (-1, 1):
            part -= Pos(sx * hx, cy + sy * hy, ear_d / 2) * Cylinder(pilot_d / 2, ear_d + 2)

    if layout == "assembled":
        if not show_unit:
            return part
        unit = _box(-body_w / 2, body_w / 2, body_b, body_t, 0, body_d)
        unit += _box(-W, W, 0, H, -2, 0)
        return Compound(children=[part, unit])

    # Wall face (x = -W) down on the bed
    p = Rot(0, -90, 0) * part   # in-use +X becomes print +Z
    bb = p.bounding_box()
    return Pos(-bb.min.X, -bb.min.Y, -bb.min.Z) * p
