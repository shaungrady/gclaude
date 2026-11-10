"""Two-piece cabinet wall mount for the AC Infinity Controller 2 (AI-ATC).

  A (wall piece): wall plate for the Command strips, plus a front and a rear
    flange standing off it. Prints wall face down (smooth strip face).
  B (front piece): full frame the controller's plate screws to, with top/bottom
    shelves for bracing and two rear tie blocks. Prints front face down (smooth
    face against the controller's plate, and the body opening is just a hole in
    a flat plate, so nothing bridges).

Joints (in-use, controller facing you):
  - Left controller screws pass through B's left leg (clearance) and thread into
    A's front flange: controller + B + A clamped together at the front.
  - Two rear tie screws go from behind through A's rear flange (clearance) into
    B's tie blocks, 40 mm behind the front.
  Button presses push B's shelves into A's wall plate; plugging cables into the
  back pushes B into both flanges. Either way the screws work in shear over a
  ~40 mm lever, not in tension over the ~4 mm a front-only joint would have.

Screws: 4 for the controller (right pair into B's bosses, 8 mm bite; left pair
through B into A's flange, needs >= ~12 mm length: 2 mm plate + 4 mm B + 6 mm A),
plus 2 rear tie screws (~10 mm). All M3 / #4 thread-forming.

Assembly: tie B to A with the rear screws, push the controller's body through
B, drive the 4 controller screws, then stick A to the wall. The left screws
are 6 mm from the wall, so this is bench assembly.

Strip face (A): 100 x 79 mm, two Large Command strips (19 x 92 mm) front to
back along the top and bottom edges; pull tabs toward the back.

Dimensions: refs/ac_infinity_controller2.md (manufacturer specs, not yet measured).

In-use frame (mm):
  X = width, centered on the controller; x=-plate_w/2 is the cabinet wall
  Y = up; y=0 is the bottom edge of the controller's front plate
  Z = depth, +Z back into the cabinet; z=0 is B's front face
layout="print" lays out both pieces for printing; "assembled" shows them in use,
with a phantom controller if show_unit=True.
"""
from build123d import Box, Compound, Cylinder, Plane, Polygon, Pos, Rot, extrude


def _box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _zcyl(x, y, d, z0, z1):
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(d / 2, z1 - z0)


def build(
    plate_w: float = 135.0,     # controller front plate
    plate_h: float = 79.0,
    body_w: float = 112.0,      # controller body behind the plate
    body_h: float = 68.0,
    body_d: float = 26.0,       # 28 overall minus ~2 mm plate (unverified)
    cut_w: float = 114.0,       # opening for the body (AC Infinity cut hole size)
    cut_h: float = 70.0,
    hole_dx: float = 123.0,     # controller screw spacing (template + product photo)
    hole_dy: float = 67.0,
    pilot_d: float = 2.5,       # M3 / #4 thread-forming
    clear_d: float = 3.3,       # screw clearance
    fit: float = 0.2,           # gap between A and B where they don't clamp
    # B (front piece)
    frame_t: float = 4.0,
    boss_d: float = 7.0,        # right screw bosses
    boss_h: float = 4.0,        # extra bite behind the frame
    shelf_t: float = 3.0,
    shelf_tip: float = 8.0,     # shelf depth behind the frame at the far (right) end
    tie_z0: float = 22.0,       # tie block 45-degree start
    tie_z1: float = 40.0,       # tie block top = A's rear flange front face
    tie_y: float = 8.0,         # rear tie screw height from top/bottom edge
    tie_bite: float = 8.0,
    # A (wall piece)
    wall_t: float = 3.0,
    depth: float = 100.0,       # wall plate depth; deeper = less strip peel from button presses
    front_flange_t: float = 6.0,  # left screw bite
    rear_flange_t: float = 4.0,
    layout: str = "print",      # "print" or "assembled"
    show_unit: bool = False,
):
    W = plate_w / 2
    H = plate_h
    cy = H / 2
    xa = -W + wall_t                     # A's wall plate inner face
    xl = -cut_w / 2                      # opening left edge = flange inner edge
    cut_b, cut_t = cy - cut_h / 2, cy + cut_h / 2
    body_b, body_t = cy - body_h / 2, cy + body_h / 2
    hx, hy = hole_dx / 2, hole_dy / 2
    ff_back = frame_t + front_flange_t   # back face of A's front flange
    tie_x = (xa + xl) / 2
    tie_ys = [tie_y, H - tie_y]

    assert layout in ("print", "assembled"), f"unknown layout {layout!r}"
    assert body_w < cut_w and body_h < cut_h, "body must fit the opening"
    assert xa + clear_d / 2 + 1 < -hx < xl - clear_d / 2 - 1, "left screws must land in the leg/flange"
    assert hx + boss_d / 2 <= W and hx - boss_d / 2 > body_w / 2, "right bosses must clear body and edge"
    assert shelf_t < body_b and H - shelf_t > body_t, "shelves hit the body"
    assert tie_z0 > ff_back + (xl - xa) + 2, "tie blocks overlap the front flange region"
    assert tie_z1 - tie_bite > tie_z0 and tie_y + pilot_d / 2 + 1 < shelf_t + (tie_z1 - tie_bite - tie_z0), \
        "rear tie pilot breaks out of the tie block"

    # ---------------- B: front piece ----------------
    xb = xa + fit                        # B's left edge, just off A's wall plate
    B = _box(xb, W, 0, H, 0, frame_t)
    B -= _box(xl, -xl, cut_b, cut_t, -1, frame_t + 1)
    # Shelves (X, Z profile): notched on the left around A's front flange with a
    # 45-degree step, full height to tie_z1 at the wall, tapering to the right.
    nz = ff_back + fit
    shelf = [(xl, frame_t), (W, frame_t), (W, frame_t + shelf_tip),
             (xb, tie_z1), (xb, nz + (xl - xb)), (xl, nz)]
    for y0 in (0, H - shelf_t):
        B += extrude(Plane.XZ.offset(-y0) * Polygon(*shelf, align=None), amount=shelf_t, dir=(0, 1, 0))
    # Rear tie blocks: grow at 45 deg from each shelf so they print without support
    rise = tie_z1 - tie_z0
    for tri in ([(shelf_t, tie_z0), (shelf_t, tie_z1), (shelf_t + rise, tie_z1)],
                [(H - shelf_t, tie_z0), (H - shelf_t - rise, tie_z1), (H - shelf_t, tie_z1)]):
        B += extrude(Plane.YZ.offset(xb) * Polygon(*tri, align=None), amount=xl - xb, dir=(1, 0, 0))
    # Right screw bosses
    for sy in (-1, 1):
        B += _zcyl(hx, cy + sy * hy, boss_d, frame_t - 0.01, frame_t + boss_h)
    # Holes: right pilots through frame + boss, left clearance through the leg
    for sy in (-1, 1):
        B -= _zcyl(hx, cy + sy * hy, pilot_d, -1, frame_t + boss_h + 1)
        B -= _zcyl(-hx, cy + sy * hy, clear_d, -1, frame_t + 1)
    for ty in tie_ys:
        B -= _zcyl(tie_x, ty, pilot_d, tie_z1 - tie_bite, tie_z1 + 1)

    # ---------------- A: wall piece ----------------
    A = _box(-W, xa, 0, H, 0, depth)
    A += _box(xa - 0.01, xl, 0, H, frame_t, ff_back)                            # front flange
    rf0 = tie_z1 + fit
    A += _box(xa - 0.01, xl, 0, H, rf0, rf0 + rear_flange_t)                    # rear flange
    for sy in (-1, 1):
        A -= _zcyl(-hx, cy + sy * hy, pilot_d, frame_t - 1, ff_back + 1)
    for ty in tie_ys:
        A -= _zcyl(tie_x, ty, clear_d, rf0 - 1, rf0 + rear_flange_t + 1)

    if layout == "assembled":
        parts = [A, B]
        if show_unit:
            unit = _box(-body_w / 2, body_w / 2, body_b, body_t, 0, body_d)
            unit += _box(-W, W, 0, H, -2, 0)
            parts.append(unit)
        return Compound(children=parts)

    # Print layout: A wall face down, B front face down, side by side.
    a = Rot(0, -90, 0) * A               # in-use +X becomes print +Z
    ab = a.bounding_box()
    a = Pos(-ab.min.X, -ab.min.Y, -ab.min.Z) * a
    bb = B.bounding_box()
    b = Pos(-bb.min.X, -bb.min.Y + H + 10, -bb.min.Z) * B
    return Compound(children=[a, b])
