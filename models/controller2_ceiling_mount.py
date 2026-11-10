"""Cabinet ceiling mount for the AC Infinity Controller 2 (AI-ATC), screwed.

One piece: a ceiling flange (Command strips) with an inverted-U front frame
hanging from its front edge. The controller's plate screws to the frame's
front face through its 4 holes; its body passes through the opening. The
frame is open at the bottom so it prints without bridging the 114 mm cutout,
and the body's rear ports stay fully accessible.

Print orientation: ceiling face down on the bed (smooth strip surface).
No supports.

Dimensions: refs/ac_infinity_controller2.md (manufacturer specs, not yet measured).

In-use frame (mm):
  X = width, centered; -X edge goes against the cabinet's left wall
  Y = up; y=0 is the bottom edge of the controller's front plate
  Z = depth, +Z back into the cabinet; z=0 is the frame's front face
layout="print" (default) rotates it ceiling-down for printing;
"assembled" leaves it in the in-use frame, with a phantom controller if show_unit=True.
"""
from build123d import Box, Compound, Cylinder, Plane, Polygon, Pos, Rot, extrude, mirror


def _box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _prism_yz(pts, x0, x1):
    """Extrude a (Y, Z) polygon along X from x0 to x1."""
    face = Plane.YZ.offset(x0) * Polygon(*pts, align=None)
    return extrude(face, amount=x1 - x0, dir=(1, 0, 0))


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
    frame_t: float = 4.0,       # front frame thickness = screw bite
    ceiling_gap: float = 0.5,   # plate top edge to ceiling
    flange_t: float = 3.0,
    flange_depth: float = 45.0, # room for 2 Command strips side by side
    gusset_t: float = 3.0,
    corner_brace: float = 2.0,  # 45 deg brace along the frame/flange inside corner
    layout: str = "print",      # "print" or "assembled"
    show_unit: bool = False,
):
    W = plate_w / 2
    yc = plate_h + ceiling_gap                      # ceiling plane
    cut_x = cut_w / 2
    cut_top = plate_h / 2 + cut_h / 2
    hy = [plate_h / 2 - hole_dy / 2, plate_h / 2 + hole_dy / 2]

    # Ceiling flange
    part = _box(-W, W, yc - flange_t, yc, 0, flange_depth)
    # Front frame: top rail + two legs (open bottom)
    part += _box(-W, W, cut_top, yc, 0, frame_t)
    leg = _box(cut_x, W, 0, yc, 0, frame_t)
    # Gusset at the outer edge (the left one sits flush on the cabinet wall)
    leg += _prism_yz([(0, frame_t), (yc, frame_t), (yc, flange_depth)], W - gusset_t, W)
    part += leg + mirror(leg, about=Plane.YZ)
    # Brace along the inside corner between frame and flange, over the body
    if corner_brace > 0:
        y0 = yc - flange_t
        part += _prism_yz([(y0, frame_t), (y0, frame_t + corner_brace),
                           (y0 - corner_brace, frame_t)], -cut_x, cut_x)

    # Screw pilots through the frame
    for sx in (-1, 1):
        for y in hy:
            part -= Pos(sx * hole_dx / 2, y, frame_t / 2) * Cylinder(pilot_d / 2, frame_t + 2)

    if layout == "assembled":
        if not show_unit:
            return part
        bx, by = body_w / 2, plate_h / 2
        unit = _box(-bx, bx, by - body_h / 2, by + body_h / 2, 0, body_d)
        unit += _box(-W, W, 0, plate_h, -2, 0)
        return Compound(children=[part, unit])

    return Pos(0, 0, yc) * (Rot(-90, 0, 0) * part)

