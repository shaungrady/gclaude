"""L-shaped wall shelf bracket with a gusset and countersunk screw holes.

Printed lying on its side (the L profile on the bed) so layer lines run
along the arms, which is the strong orientation for a bracket.

Model frame: the corner is at the origin. The wall touches the x=0 face, the
shelf board touches the y=0 face, and the gusset fills the inside corner.
Countersinks face the inside so screws go through the arms into wall and board.
"""
from build123d import (
    Axis, BuildPart, BuildSketch, CounterSinkHole, Locations, Plane, Polygon,
    Pos, extrude, fillet,
)


def build(
    wall_arm: float = 60.0,     # vertical arm length (mm)
    shelf_arm: float = 50.0,    # horizontal arm length (mm)
    width: float = 20.0,        # bracket width = print height (mm)
    thickness: float = 5.0,     # arm thickness (mm)
    gusset: float = 25.0,       # gusset leg length (mm), 0 to disable
    screw_d: float = 4.0,       # screw shank clearance (mm)
    head_d: float = 8.0,        # countersink diameter (mm)
    edge_fillet: float = 1.0,
):
    t = thickness
    # L profile in XY: wall arm along +Y at x in [0, t], shelf arm along +X at y in [0, t]
    pts = [(0, 0), (shelf_arm, 0), (shelf_arm, t), (t + gusset, t),
           (t, t + gusset), (t, wall_arm), (0, wall_arm)]
    if gusset <= 0:
        pts = [(0, 0), (shelf_arm, 0), (shelf_arm, t), (t, t), (t, wall_arm), (0, wall_arm)]

    with BuildPart() as bp:
        with BuildSketch(Plane.XY):
            Polygon(*pts, align=None)
        extrude(amount=width)
        fillet(bp.edges().filter_by(Axis.Z), radius=edge_fillet)

        # Screw holes through the wall arm (along X, countersunk from the +X face)
        hole_y = [t + gusset + (wall_arm - t - gusset) / 2] if gusset > 0 else [wall_arm * 0.6]
        wall_face = Plane.YZ.offset(t)
        with Locations(*[wall_face * Pos(y, width / 2) for y in hole_y]):
            CounterSinkHole(radius=screw_d / 2, counter_sink_radius=head_d / 2, depth=t)
        # Screw hole through the shelf arm (along Y, from the +Y face)
        with Locations(Plane((shelf_arm - (shelf_arm - t - gusset) / 2, t, width / 2),
                             z_dir=(0, 1, 0), x_dir=(1, 0, 0))):
            CounterSinkHole(radius=screw_d / 2, counter_sink_radius=head_d / 2, depth=t)
    return bp.part
