"""Screwless two-piece cabinet ceiling mount for the AC Infinity Controller 2 (AI-ATC).

The controller's front plate bears on the sleeve's front face; a back lip frame
behind the body stops it sliding forward and leaves the rear ports open.

  TOP piece:    ceiling flange (Command strips go here) + side walls + back lip
                (top and sides). Prints ceiling face down, so the strip surface
                is the smooth bed side. No overhangs.
  BOTTOM piece: floor + back lip (bottom) + two cantilever snap arms that hook
                into pockets on the outside of the side walls. Prints floor down.

Assembly: push the controller up into the top piece from below, then snap the
bottom piece on. Release by spreading both arms outward.

Dimensions: refs/ac_infinity_controller2.md. Body/plate sizes are from the
manufacturer and not yet measured on a real unit; adjust `clearance` and the
body_* params after a test fit.

In-use frame (mm), used for all geometry below:
  X = width (centered; -X side goes against the cabinet's left wall)
  Y = up; y=0 is the floor the controller body rests on
  Z = depth, +Z back into the cabinet; z=0 is where the front plate's back face sits

layout="print" lays both pieces out for printing; "assembled" shows them in use,
with a phantom controller if show_unit=True.
"""
from build123d import Axis, Box, Compound, Plane, Polygon, Pos, Rot, extrude, mirror


def _box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def build(
    body_w: float = 112.0,      # controller body behind the plate
    body_h: float = 68.0,
    body_d: float = 26.0,       # 28 overall minus ~2 mm plate (unverified)
    plate_w: float = 135.0,
    plate_h: float = 79.0,
    clearance: float = 0.5,     # per side, around the body
    wall: float = 3.0,          # side walls and floor
    flange_t: float = 3.0,      # ceiling flange thickness
    flange_depth: float = 45.0, # room for 2 Command strips side by side
    ceiling_gap: float = 0.5,   # plate top edge to ceiling
    lip_t: float = 3.0,         # back lip thickness
    lip_w: float = 4.0,         # how far the back lip covers the body's back edge
    arm_t: float = 2.2,         # snap arm thickness (flex direction)
    arm_w: float = 14.0,        # snap arm width (along Z)
    arm_h: float = 25.0,        # snap arm length above the floor
    hook: float = 1.0,          # hook engagement depth
    snap_gap: float = 0.2,      # arm to side wall
    layout: str = "print",      # "print" or "assembled"
    show_unit: bool = False,
):
    c = clearance
    xi = body_w / 2 + c                     # cavity half width
    xo = xi + wall                          # side wall outer face
    yt = body_h + 2 * c                     # cavity top
    zb = body_d + c                         # cavity back = back lip front face
    zl = zb + lip_t                         # back of sleeve
    plate_over = (plate_h - body_h) / 2     # plate overhang above/below the body
    y_ceiling = body_h + plate_over + ceiling_gap
    xa0, xa1 = xo + snap_gap, xo + snap_gap + arm_t   # arm inner/outer faces
    za0, za1 = zb / 2 - arm_w / 2, zb / 2 + arm_w / 2  # arm Z span (centered on body)
    hook_y = arm_h - 3.0                    # hook retention face height

    # ---------------- TOP piece ----------------
    top = _box(-plate_w / 2, plate_w / 2, y_ceiling - flange_t, y_ceiling, 0, flange_depth)
    top += _box(-xo, xo, yt, y_ceiling - flange_t, 0, zl)            # spacer over the body
    top += _box(-xi, xi, yt - lip_w, yt, zb, zl)                     # back lip, top band
    side = _box(xi, xo, 0, yt, 0, zl)                                # right side wall
    side += _box(xi - lip_w, xi, 0, yt, zb, zl)                      # back lip, right band
    # pocket for the snap hook on the wall's outer face
    side -= _box(xo - hook - 0.2, xo + 0.01, hook_y - 0.15, hook_y + 2.5, za0 - 0.3, za1 + 0.3)
    top += side + mirror(side, about=Plane.YZ)

    # ---------------- BOTTOM piece ----------------
    bottom = _box(-xa1, xa1, -wall, 0, 0, zl)                        # floor
    bottom += _box(-(xi - lip_w - 0.3), xi - lip_w - 0.3, 0, lip_w, zb, zl)  # back lip, bottom band
    arm = _box(xa0, xa1, -wall, arm_h, za0, za1)
    # hook: flat retention face at hook_y, 45 deg lead-in ramp above it
    hook_profile = Polygon((xa0, hook_y), (xa0 - hook, hook_y), (xa0 - hook, hook_y + 0.6),
                           (xa0, hook_y + 0.6 + hook), align=None)
    arm += extrude(Plane.XY.offset(za0) * hook_profile, amount=arm_w, dir=(0, 0, 1))
    bottom += arm + mirror(arm, about=Plane.YZ)

    if layout == "assembled":
        parts = [top, bottom]
        if show_unit:
            unit = _box(-body_w / 2, body_w / 2, 0, body_h, 0, body_d)
            unit += _box(-plate_w / 2, plate_w / 2, -plate_over, body_h + plate_over, -2, 0)
            parts.append(unit)
        return Compound(children=parts)

    # Print layout: top piece ceiling-down, bottom piece floor-down, side by side.
    top_p = Pos(0, 0, y_ceiling) * (Rot(-90, 0, 0) * top)
    bot_p = Pos(0, -10, wall) * (Rot(90, 0, 0) * bottom)
    return Compound(children=[top_p, bot_p])
