"""Two-piece cabinet wall mount for the AC Infinity Controller 2 (AI-ATC).

  A (wall piece): wall plate (hook-and-loop strips on the cabinet's left wall),
    a ceiling flange (one strip on the cabinet ceiling), and a front and rear
    flange standing off the wall plate. Prints wall face down.
  B (front piece): full frame the controller's plate screws to, with top/bottom
    shelves for bracing and two rear tie blocks. Prints front face down (smooth
    face against the controller's plate; the body opening is just a hole in a
    flat plate, so nothing bridges).

Joints (in-use, controller facing you):
  - Left controller screws pass through B's left leg (clearance) and thread into
    A's front flange: controller + B + A clamped together at the front.
  - Two rear tie screws go from behind through A's rear flange (clearance) into
    B's tie blocks, 40 mm behind the front.
  Pushing on the controller's face presses B into A's front flange and B's
  shelves into A's wall plate. Pulling it forward (e.g. unplugging cables at the
  back) puts the left and rear tie screws in tension. Expected use is light:
  the controller mostly hangs, and the owner braces its right edge while
  pressing buttons.

Strips (hook-and-loop, e.g. Command picture-hanging strips, Large = 19 x 92 mm):
  - Wall face: 100 x 82.5 mm; two strips front to back along top and bottom edges.
  - Ceiling face: 25 x 100 mm; one strip front to back. This face prints as a
    vertical wall (fine layer lines); only the wall face is bed-smooth.

Screws (6 total, M3 / #4 thread-forming):
  - Right controller pair: into B's bosses, 8 mm bite.
  - Left controller pair: through the plate (plate_t), B (4 mm) and A's flange
    (6 mm). Length 12 to 21 mm; longer runs into B's tie blocks.
  - Rear tie pair: from behind through A's rear flange; 10 to 16 mm long. A's
    wall plate runs past the screw heads 3.75 mm from their axis, so use a
    driver with a shaft of at least 60 mm (not a stubby or bit holder).
  The controller's box includes 4 mounting screws; buy 2 more for the rear tie.

Assembly: tie B to A with the rear screws, push the controller's body through
B, drive the 4 controller screws, then stick A up. The left screws are 6 mm
from the wall, so this is bench assembly.

Printing: A on the smooth PEI sheet (textured hurts strip adhesion). PLA is
fine at room temperature; use PETG if the cabinet runs above ~40 C (PLA creeps
under screw preload when warm).

Before the full print: layout="fit_test" prints only B's 4 mm frame with the
screw holes. Hold it against the real controller to confirm the 123 mm hole
spacing (the website says 120; refs/ac_infinity_controller2.md).

Dimensions: refs/ac_infinity_controller2.md (manufacturer specs, not yet measured).

In-use frame (mm):
  X = width, centered on the controller; x=-plate_w/2 is the cabinet wall
  Y = up; y=0 is the bottom edge of the controller's front plate
  Z = depth, +Z back into the cabinet; z=0 is B's front face
layout: "print" (both pieces on the bed), "assembled" (in use, with a phantom
controller if show_unit=True), or "fit_test" (B's frame only).
"""
from build123d import Box, Compound, Cylinder, Plane, Polygon, Pos, Rot, extrude


def _box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _zcyl(x, y, d, z0, z1):
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(d / 2, z1 - z0)


def _lay_flat(shape, y_offset=0.0):
    bb = shape.bounding_box()
    return Pos(-bb.min.X, -bb.min.Y + y_offset, -bb.min.Z) * shape


def build(
    plate_w: float = 135.0,     # controller front plate
    plate_h: float = 79.0,
    plate_t: float = 2.0,       # controller plate thickness (unverified)
    body_w: float = 112.0,      # controller body behind the plate
    body_h: float = 68.0,
    body_d: float = 26.0,       # 28 overall minus plate_t (unverified)
    cut_w: float = 114.0,       # opening for the body (AC Infinity cut hole size)
    cut_h: float = 70.0,
    hole_dx: float = 123.0,     # controller screw spacing (template + product photo)
    hole_dy: float = 67.0,
    pilot_d: float = 2.5,       # M3 / #4 thread-forming
    clear_d: float = 3.2,       # screw clearance (close fit)
    fit: float = 0.2,           # gap between A and B wherever they slide past each other
    step_gap: float = 0.4,      # extra gap under B's 45-degree notch step (allows droop)
    min_wall: float = 1.2,
    # B (front piece)
    frame_t: float = 4.0,
    boss_d: float = 7.0,        # right screw bosses
    boss_h: float = 4.0,        # extra bite behind the frame
    shelf_t: float = 3.0,
    shelf_tip: float = 8.0,     # shelf depth behind the frame at the far (right) end
    tie_z0: float = 18.0,       # tie block 45-degree start
    tie_z1: float = 40.0,       # tie block top = A's rear flange front face
    tie_y: float = 8.0,         # rear tie screw height from top/bottom edge
    tie_bite: float = 14.0,     # rear tie pilot depth (screws 10 to 16 mm)
    # A (wall piece)
    wall_t: float = 3.0,
    depth: float = 100.0,       # wall plate depth
    front_flange_t: float = 6.0,  # left screw bite
    rear_flange_t: float = 4.0,
    ceiling_w: float = 25.0,    # ceiling flange width out from the wall (strip is 19)
    ceiling_t: float = 3.0,
    ceiling_gap: float = 0.5,   # controller plate top to ceiling flange underside
    layout: str = "print",      # "print", "assembled" or "fit_test"
    show_unit: bool = False,
):
    W = plate_w / 2
    H = plate_h
    cy = H / 2
    xa = -W + wall_t                     # A's wall plate inner face
    xl = -cut_w / 2                      # opening left edge = A flange inner edge
    xb = xa + fit                        # B's left edge, just off A's wall plate
    xs = xl + fit                        # B's shelf face beside A's front flange
    cut_b, cut_t = cy - cut_h / 2, cy + cut_h / 2
    body_b, body_t = cy - body_h / 2, cy + body_h / 2
    hx, hy = hole_dx / 2, hole_dy / 2
    ff_back = frame_t + front_flange_t   # back face of A's front flange
    nz = ff_back + step_gap              # B's shelf notch height
    step_top = nz + (xs - xb)            # top of B's 45-degree notch step at the wall
    rf0 = tie_z1 + fit                   # A's rear flange front face
    rf1 = rf0 + rear_flange_t
    tie_x = (xa + xl) / 2
    tie_ys = [tie_y, H - tie_y]
    y_ceil0 = H + ceiling_gap            # ceiling flange underside
    y_top = y_ceil0 + ceiling_t          # ceiling contact face
    rise = tie_z1 - tie_z0
    pilot_bot = tie_z1 - tie_bite

    assert layout in ("print", "assembled", "fit_test"), f"unknown layout {layout!r}"
    assert body_w < cut_w and body_h < cut_h, "body must fit the opening"
    assert -hx - clear_d / 2 - xb >= min_wall - 1e-9 and xl - (-hx + clear_d / 2) >= min_wall - 1e-9, \
        "left clearance holes leave too thin a wall in B's leg"
    assert hx + boss_d / 2 <= W and hx - boss_d / 2 > body_w / 2, "right bosses must clear body and edge"
    assert shelf_t < body_b and H - shelf_t > body_t, "shelves hit the body"
    assert step_top < tie_z0, "B's notch step runs into the tie blocks"
    assert pilot_bot > tie_z0, "rear tie pilot deeper than the tie block"
    # Pilot must stay inside the 45-degree block at its deepest (narrowest) point
    assert tie_y + pilot_d / 2 + min_wall <= shelf_t + (pilot_bot - tie_z0), \
        "rear tie pilot breaks out of the tie block's 45-degree face"
    assert tie_x - pilot_d / 2 - xb >= min_wall and xl - (tie_x + pilot_d / 2) >= min_wall, \
        "rear tie pilot too close to the tie block's sides"
    assert depth >= rf1, "wall plate must reach behind the rear flange"
    assert ceiling_w >= 21, "ceiling flange must fit a 19 mm strip"

    # ---------------- B: front piece ----------------
    frame = _box(xb, W, 0, H, 0, frame_t)
    frame -= _box(xl, -xl, cut_b, cut_t, -1, frame_t + 1)
    for sy in (-1, 1):
        frame -= _zcyl(hx, cy + sy * hy, pilot_d, -1, frame_t + 1)
        frame -= _zcyl(-hx, cy + sy * hy, clear_d, -1, frame_t + 1)
    if layout == "fit_test":
        return _lay_flat(frame)

    B = frame
    # Shelves (X, Z profile): notched around A's front flange with a 45-degree
    # step, reaching tie_z1 across the tie blocks, tapering to the right.
    shelf = [(xs, frame_t), (W, frame_t), (W, frame_t + shelf_tip),
             (xs, tie_z1), (xb, tie_z1), (xb, step_top), (xs, nz)]
    for y0 in (0, H - shelf_t):
        B += extrude(Plane.XZ.offset(-y0) * Polygon(*shelf, align=None), amount=shelf_t, dir=(0, 1, 0))
    # Rear tie blocks: grow at 45 deg from each shelf so they print without support
    for tri in ([(shelf_t, tie_z0), (shelf_t, tie_z1), (shelf_t + rise, tie_z1)],
                [(H - shelf_t, tie_z0), (H - shelf_t - rise, tie_z1), (H - shelf_t, tie_z1)]):
        B += extrude(Plane.YZ.offset(xb) * Polygon(*tri, align=None), amount=xs - xb, dir=(1, 0, 0))
    # Right screw bosses
    for sy in (-1, 1):
        B += _zcyl(hx, cy + sy * hy, boss_d, frame_t - 0.01, frame_t + boss_h)
        B -= _zcyl(hx, cy + sy * hy, pilot_d, frame_t - 1, frame_t + boss_h + 1)
    for ty in tie_ys:
        B -= _zcyl(tie_x, ty, pilot_d, pilot_bot, tie_z1 + 1)

    # ---------------- A: wall piece ----------------
    A = _box(-W, xa, 0, y_top, 0, depth)                                   # wall plate
    A += _box(xa - 0.01, xa + ceiling_w, y_ceil0, y_top, 0, depth)         # ceiling flange
    # 45-degree brace under the ceiling flange, behind everything of B's
    brace = 4.0
    A += extrude(Plane.XY.offset(rf1) * Polygon((xa - 0.01, y_ceil0 - brace), (xa - 0.01, y_ceil0),
                                                (xa + brace, y_ceil0), align=None),
                 amount=depth - rf1, dir=(0, 0, 1))
    A += _box(xa - 0.01, xl, 0, H, frame_t, ff_back)                       # front flange
    A += _box(xa - 0.01, xl, 0, H, rf0, rf1)                               # rear flange
    for sy in (-1, 1):
        A -= _zcyl(-hx, cy + sy * hy, pilot_d, frame_t - 1, ff_back + 1)
    for ty in tie_ys:
        A -= _zcyl(tie_x, ty, clear_d, rf0 - 1, rf1 + 1)

    if layout == "assembled":
        parts = [A, B]
        if show_unit:
            unit = _box(-body_w / 2, body_w / 2, body_b, body_t, 0, body_d)
            unit += _box(-W, W, 0, H, -plate_t, 0)
            parts.append(unit)
        return Compound(children=parts)

    # Print layout: A wall face down, B front face down, side by side.
    a = _lay_flat(Rot(0, -90, 0) * A)    # in-use +X becomes print +Z
    b = _lay_flat(B, y_offset=y_top + 10)
    return Compound(children=[a, b])
