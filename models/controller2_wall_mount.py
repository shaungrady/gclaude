"""Cabinet wall mount for the AC Infinity Controller 2 (AI-ATC), screwed.

One piece: a wall plate (Command strips) on the cabinet's left wall, a front
frame the controller's plate screws to, and top/bottom shelves that brace the
frame back to the wall plate. The controller's body passes through the frame;
its rear ports stay open to the back.

Print orientation: wall plate face down on the bed (smooth strip surface).
No supports. The frame's right leg prints as a ~70 mm bridge between the two
shelves; it's hidden behind the controller's plate, and `right_relief` leaves
room for bridge sag.

Strip face: 45 x 79 mm, fits two Medium Command strips (16 x 70 mm) vertically.
Point the pull tabs down.

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
from build123d import Box, Compound, Cylinder, Plane, Polygon, Pos, Rot, extrude


def _box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _prism_xz(pts, y0, y1):
    """Extrude an (X, Z) polygon along Y from y0 to y1."""
    face = Plane.XZ.offset(-y0) * Polygon(*pts, align=None)
    return extrude(face, amount=y1 - y0, dir=(0, 1, 0))


def build(
    plate_w: float = 135.0,     # controller front plate
    plate_h: float = 79.0,
    body_w: float = 112.0,      # controller body behind the plate
    body_h: float = 68.0,
    body_d: float = 26.0,       # 28 overall minus ~2 mm plate (unverified)
    cut_w: float = 114.0,       # opening for the body (AC Infinity cut hole size)
    cut_h: float = 70.0,
    right_relief: float = 1.0,  # extra opening on the right for bridge sag
    hole_dx: float = 123.0,     # screw spacing (template + product photo)
    hole_dy: float = 67.0,
    pilot_d: float = 2.5,       # M3 / #4 thread-forming screws into PLA
    frame_t: float = 4.0,       # front frame thickness = screw bite
    wall_t: float = 3.0,        # wall plate thickness
    depth: float = 45.0,        # wall plate depth (front to back)
    shelf_t: float = 3.0,       # top/bottom brace shelves
    shelf_tip: float = 8.0,     # shelf depth behind the frame at the far (right) end
    layout: str = "print",      # "print" or "assembled"
    show_unit: bool = False,
):
    W = plate_w / 2
    H = plate_h
    cy = H / 2
    cut_l, cut_r = -cut_w / 2, cut_w / 2 + right_relief
    cut_b, cut_t = cy - cut_h / 2, cy + cut_h / 2
    body_b, body_t = cy - body_h / 2, cy + body_h / 2
    hx, hy = hole_dx / 2, hole_dy / 2

    # Guard against parameter combos that silently make bad geometry
    assert layout in ("print", "assembled"), f"unknown layout {layout!r}"
    assert body_w < cut_w and body_h < cut_h, "body must fit the opening"
    assert hx - pilot_d / 2 > cut_r + 1.0, "pilot holes break into the opening"
    assert hx + pilot_d / 2 < W - 1.0, "pilot holes break out of the frame edge"
    assert shelf_t < body_b and H - shelf_t > body_t, "shelves hit the body"
    assert 0 < cut_b and cut_t < H, "opening must leave top and bottom rails"

    # Wall plate
    part = _box(-W, -W + wall_t, 0, H, 0, depth)
    # Front frame with the body opening
    part += _box(-W, W, 0, H, 0, frame_t)
    part -= _box(cut_l, cut_r, cut_b, cut_t, -1, frame_t + 1)
    # Top and bottom shelves: full depth at the wall, tapering to shelf_tip
    shelf = [(-W, frame_t), (W, frame_t), (W, frame_t + shelf_tip), (-W, depth)]
    part += _prism_xz(shelf, 0, shelf_t)
    part += _prism_xz(shelf, H - shelf_t, H)

    # Screw pilots
    for sx in (-1, 1):
        for sy in (-1, 1):
            part -= Pos(sx * hx, cy + sy * hy, frame_t / 2) * Cylinder(pilot_d / 2, frame_t + 2)

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
