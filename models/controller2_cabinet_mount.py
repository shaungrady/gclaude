"""Cabinet ceiling mount for the AC Infinity Controller 2 (AI-ATC).

A front panel holds the controller (screwed through its 4 plate holes, body
through the cutout). A top flange runs back from the panel's top edge and sticks
to the cabinet ceiling with two Command strips. Side gussets stiffen the corner;
the left one sits flush against the cabinet's left wall. Back and bottom stay
open for the rear power/sensor/fan cables.

Dimensions: refs/ac_infinity_controller2.md.

Print orientation: front face down on the bed. No supports.

Model frame (mm), in use:
  X = width (x=0 is the left wall side)
  Y = height, +Y up; y = panel_h + flange_t is the ceiling contact face
  Z = depth, +Z goes back into the cabinet; z=0 is the front face
"""
from build123d import (
    Align, Box, BuildPart, BuildSketch, Hole, Locations, Mode, Plane, Polygon,
    Pos, chamfer, extrude,
)


def build(
    plate_w: float = 135.0,     # controller front plate
    plate_h: float = 79.0,
    cut_w: float = 114.0,       # AC Infinity's recommended cut hole
    cut_h: float = 70.0,
    hole_dx: float = 123.0,     # screw hole spacing (template + photo)
    hole_dy: float = 67.0,
    pilot_d: float = 2.5,       # pilot for M3 / #4 thread-forming screws in PLA
    margin: float = 3.0,        # panel border around the controller plate
    panel_t: float = 5.0,       # gives screws ~5 mm of bite
    flange_depth: float = 50.0, # how far the ceiling flange runs back
    flange_t: float = 4.0,
    gusset_t: float = 4.0,
    front_chamfer: float = 0.6, # hides elephant foot on the visible front edges
):
    W = plate_w + 2 * margin
    H = plate_h + 2 * margin
    D = flange_depth
    cx, cy = W / 2, H / 2

    with BuildPart() as bp:
        # Front panel
        Box(W, H, panel_t, align=(Align.MIN, Align.MIN, Align.MIN))
        # Ceiling flange, above the panel's top edge, flush with the front face
        with Locations(Pos(0, H, 0)):
            Box(W, flange_t, D, align=(Align.MIN, Align.MIN, Align.MIN))
        # Side gussets: right triangles in YZ, legs along the panel and the flange
        tri = [(0, 0), (H + flange_t, 0), (H + flange_t, D)]  # (Y, Z) on Plane.YZ
        for x0 in (0, W - gusset_t):
            with BuildSketch(Plane.YZ.offset(x0)):
                Polygon(*tri, align=None)
            extrude(amount=gusset_t)

        # Controller body cutout
        with Locations(Pos(cx, cy, 0)):
            Box(cut_w, cut_h, panel_t * 3, mode=Mode.SUBTRACT)

        # Screw pilots, drilled from the front face
        front = Plane.XY.offset(panel_t)
        with Locations(*[front * Pos(cx + sx * hole_dx / 2, cy + sy * hole_dy / 2)
                         for sx in (-1, 1) for sy in (-1, 1)]):
            Hole(radius=pilot_d / 2, depth=panel_t)

        if front_chamfer > 0:
            def on_outline(e):
                c = e.center()
                return (abs(c.Z) < 1e-6 and
                        (min(abs(c.X), abs(c.X - W)) < 1e-6
                         or min(abs(c.Y), abs(c.Y - H - flange_t)) < 1e-6))
            chamfer([e for e in bp.edges() if on_outline(e)], length=front_chamfer)

    return bp.part
