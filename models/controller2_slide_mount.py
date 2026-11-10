"""Two-piece slide-and-snap cabinet wall mount for the AC Infinity Controller 2 (AI-ATC).

  A (wall piece): wall plate (hook-and-loop strips on the cabinet's left wall),
    ceiling flange (one strip on the cabinet ceiling), and two dovetail rails
    running front to back. The bottom rail has a snap notch. Prints wall face down.
  B (front piece): frame the controller screws to (all 4 screws), shelves for
    bracing, and a left side with two dovetail grooves. A spring tongue over
    the bottom groove carries the snap hook. Prints front face down.

Use:
  1. Screw the controller to B on the bench (all 4 screws reachable).
  2. Stick A to the cabinet wall and ceiling.
  3. Slide B + controller straight back onto A's rails until it clicks.
  To remove: pull the controller straight forward firmly (~6 to 8 N estimated); the hook's
  45-degree face lifts the tongue out of the notch.

Loads: the dovetails carry the weight and the twisting from it (B can't pull
away from the wall). Pushing back on the controller seats B against the rail
ends. Only forward pulls load the snap.

Snap tongue: a cantilever cut from B's side web, flexing away from the wall.
B prints with the tongue vertical, so it bends across layers; deflection is
at most 1.2 mm over ~29 mm (~0.5% strain, worst case with B pushed against
the wall), and the slots end in round stop holes. The hook's retention face is 45
degrees so it prints without support (it faces down in B's print).

Screws: 4 controller screws (M3 / #4 thread-forming, 8 to 12 mm) into B's
bosses. No other fasteners.

Printing: A on the smooth PEI sheet. PETG for B if the cabinet runs warm
(above ~40 C) or for a longer-lived snap.

Dimensions: refs/ac_infinity_controller2.md (manufacturer specs, not yet measured).

In-use frame (mm):
  X = width, centered on the controller; x=-plate_w/2 is the cabinet wall
  Y = up; y=0 is the bottom edge of the controller's front plate
  Z = depth, +Z back into the cabinet; z=0 is B's front face (seated)
layout: "print", "assembled" (with a phantom controller if show_unit=True),
or "fit_test" (B's 4 mm frame only, to check the screw spacing on the real unit).
"""
import math

from build123d import Box, Compound, Cylinder, Plane, Polygon, Pos, Rot, extrude, loft


def _box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _zcyl(x, y, d, z0, z1):
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(d / 2, z1 - z0)


def _xy_prism(pts, z0, z1):
    return extrude(Plane.XY.offset(z0) * Polygon(*pts, align=None), amount=z1 - z0, dir=(0, 0, 1))


def _xz_prism(pts, y0, y1):
    # Plane.XZ maps local (u, v) to global (X, Z); its normal is -Y.
    return extrude(Plane.XZ.offset(-y0) * Polygon(*pts, align=None), amount=y1 - y0, dir=(0, 1, 0))


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
    fit: float = 0.12,          # dovetail clearance normal to each face; tune with a test coupon
    min_wall: float = 1.2,
    # B (front piece)
    frame_t: float = 4.0,
    boss_d: float = 7.0,
    boss_h: float = 4.0,        # screw bite = frame_t + boss_h
    shelf_t: float = 3.0,
    shelf_tip: float = 8.0,
    b_depth: float = 40.0,      # B's length front to back (= rail length)
    web_t: float = 2.4,         # B's side web; also the snap tongue thickness
    groove_wall: float = 2.5,   # material beside each dovetail groove
    # Dovetail rails (on A)
    rail_h: float = 4.0,        # out from the wall plate
    rail_base: float = 6.0,     # width at the wall plate
    rail_angle: float = 20.0,   # flank angle; also A's print overhang angle
    rail_y: float = 22.0,       # rail centers from top/bottom edges
    # Snap
    tongue_len: float = 33.0,
    hook: float = 1.2,          # hook height above the groove floor
    hook_flat: float = 1.0,
    ret_angle: float = 45.0,    # retention face; <= 45 prints without support
    ramp_angle: float = 30.0,   # lead-in face
    slot_w: float = 0.6,
    slot_relief_d: float = 1.6, # round stop hole at each slot end (eases the tongue root)
    notch_play: float = 0.25,   # hook to notch front wall when seated
    lead: float = 1.5,          # 45-degree lead-in on rail fronts and groove mouths
    # A (wall piece)
    wall_t: float = 3.0,
    depth: float = 100.0,       # wall plate depth
    ceiling_w: float = 25.0,    # ceiling flange width (strip is 19)
    ceiling_t: float = 3.0,
    ceiling_gap: float = 0.5,
    brace: float = 4.0,         # 45-degree brace under the ceiling flange
    a_relief: float = 0.5,      # A starts this far behind B's front face, so the controller
                                # plate (which overhangs B on the wall side) can't touch A
    layout: str = "print",
    show_unit: bool = False,
):
    W = plate_w / 2
    H = plate_h
    cy = H / 2
    t = math.tan(math.radians(rail_angle))
    xa = -W + wall_t                 # A wall plate inner face
    xb = xa + fit                    # B's left face
    xt = xa + rail_h                 # rail top
    xg = xt + fit                    # groove floor = web inner face
    xw = xg + web_t                  # web outer face
    xl = -cut_w / 2
    cut_b, cut_t = cy - cut_h / 2, cy + cut_h / 2
    body_b, body_t = cy - body_h / 2, cy + body_h / 2
    hx, hy = hole_dx / 2, hole_dy / 2
    rys = [rail_y, H - rail_y]
    y_ceil0 = H + ceiling_gap
    y_top = y_ceil0 + ceiling_t

    def rail_half(x):                # rail half width at x
        return rail_base / 2 + (x - xa) * t

    def groove_half(x):              # groove half width, fit measured normal to the flank
        return rail_half(x) + fit / math.cos(math.radians(rail_angle))

    gh = groove_half(xg)             # groove half width at its floor
    tr, tm = math.tan(math.radians(ret_angle)), math.tan(math.radians(ramp_angle))
    z_hook_end = b_depth - 0.5
    zh = z_hook_end - hook / tm - hook_flat          # hook tip front edge
    z_root = b_depth - tongue_len
    lever = zh - z_root                               # tongue root to hook
    # Worst case: the ramp pushes B against the wall plate, so the tongue bends the full hook height
    strain = 1.5 * web_t * hook / lever ** 2

    assert layout in ("print", "assembled", "fit_test"), f"unknown layout {layout!r}"
    assert body_w < cut_w and body_h < cut_h, "body must fit the opening"
    assert xw <= xl, "B's side web must sit on the frame's left leg"
    assert xw + hook + 0.5 <= -body_w / 2, "flexed tongue hits the controller body"
    assert hx + boss_d / 2 <= W and hx - boss_d / 2 > body_w / 2, "right bosses must clear body and edge"
    assert shelf_t < body_b and H - shelf_t > body_t, "shelves hit the body"
    for yr in rys:
        g0, g1 = yr - gh - groove_wall, yr + gh + groove_wall
        for sy in (-1, 1):
            by = cy + sy * hy
            assert by + boss_d / 2 < g0 or by - boss_d / 2 > g1, "left boss overlaps a groove block"
    assert rail_y - gh - groove_wall > shelf_t, "groove block runs into the shelf"
    assert z_root > frame_t + 2, "tongue too long for B"
    assert strain < 0.006, f"tongue strain {strain:.4f} too high for across-layer bending"
    hook_half = groove_half(xg - hook) - 0.25         # hook half width: clears the flanks at its tip
    assert hook_half >= 2.0, "hook too narrow"
    assert groove_wall - 0.3 >= min_wall, "tongue slots leave too thin a groove wall"
    assert depth >= b_depth + 2 + 5, "wall plate too short for the ceiling brace"
    assert a_relief > 0, "controller plate would touch A's front edge"
    assert hook - fit >= 0.8, "too little hook engagement"
    assert ret_angle <= 45, "retention face would overhang in B's print"

    # ---------------- B: front piece ----------------
    frame = _box(xb, W, 0, H, 0, frame_t)
    frame -= _box(xl, -xl, cut_b, cut_t, -1, frame_t + 1)
    for sx in (-1, 1):
        for sy in (-1, 1):
            frame -= _zcyl(sx * hx, cy + sy * hy, pilot_d, -1, frame_t + 1)
    if layout == "fit_test":
        return _lay_flat(frame)

    B = frame
    # Side web and groove blocks
    B += _box(xg, xw, shelf_t - 0.01, H - shelf_t + 0.01, frame_t - 0.01, b_depth)
    for yr in rys:
        B += _box(xb, xg + 0.01, yr - gh - groove_wall, yr + gh + groove_wall, frame_t - 0.01, b_depth)
        x0 = xb - 1
        B -= _xy_prism([(x0, yr - groove_half(x0)), (xg, yr - gh), (xg, yr + gh), (x0, yr + groove_half(x0))],
                       frame_t, b_depth + 1)
        # Flared groove mouth (wider in Y by `lead`, same depth in X) to guide B onto the rails
        sec = lambda z, e: Plane.XY.offset(z) * Polygon(
            (x0, yr - groove_half(x0) - e), (xg, yr - gh - e), (xg, yr + gh + e), (x0, yr + groove_half(x0) + e),
            align=None)
        B -= loft([sec(b_depth - lead, 0), sec(b_depth + 0.01, lead)])
    # Shelves: full depth at the side web, tapering to the right
    shelf = [(xb, frame_t), (W, frame_t), (W, frame_t + shelf_tip), (xw, b_depth), (xb, b_depth)]
    B += _xz_prism(shelf, 0, shelf_t)
    B += _xz_prism(shelf, H - shelf_t, H)
    # Bosses and pilots for all 4 controller screws
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * hx, cy + sy * hy
            boss = _zcyl(x, y, boss_d, frame_t - 0.01, frame_t + boss_h)
            B += boss & _box(xb, W, 0, H, 0, frame_t + boss_h + 1)
            B -= _zcyl(x, y, pilot_d, -1, frame_t + boss_h + 1)
    # Snap tongue over the bottom groove: two slots free a strip of the web
    yr = rys[0]
    for y0 in (yr + gh - 0.3, yr - gh - slot_w + 0.3):
        B -= _box(xg - 0.3, xw + 0.1, y0, y0 + slot_w, z_root, b_depth + 1)
        # Stop hole: rounds the slot end so the tongue root has no sharp notch
        B -= Pos((xg - 0.3 + xw + 0.1) / 2, y0 + slot_w / 2, z_root) * (
            Rot(0, 90, 0) * Cylinder(slot_relief_d / 2, xw - xg + 0.4))
    hook_pts = [(xg + 0.01, zh - (hook + 0.01) / tr), (xg - hook, zh), (xg - hook, zh + hook_flat),
                (xg + 0.01, zh + hook_flat + (hook + 0.01) / tm)]
    B += _xz_prism(hook_pts, yr - hook_half, yr + hook_half)

    # ---------------- A: wall piece ----------------
    A = _box(-W, xa, 0, y_top, a_relief, depth)
    A += _box(xa - 0.01, xa + ceiling_w, y_ceil0, y_top, a_relief, depth)
    A += _xy_prism([(xa - 0.01, y_ceil0 - brace), (xa - 0.01, y_ceil0), (xa + brace, y_ceil0)],
                   b_depth + 2, depth)
    for yr in rys:
        A += _xy_prism([(xa - 0.01, yr - rail_half(xa)), (xt, yr - rail_half(xt)),
                        (xt, yr + rail_half(xt)), (xa - 0.01, yr + rail_half(xa))],
                       frame_t + fit, b_depth)
        # 45-degree lead-in on the rail's front top edge
        rz0 = frame_t + fit
        A -= _xz_prism([(xt - lead, rz0 - 0.01), (xt + 0.01, rz0 - 0.01), (xt + 0.01, rz0 + lead)],
                       yr - rail_half(xt) - 1, yr + rail_half(xt) + 1)
    # Snap notch in the bottom rail's top, matching the seated hook
    n = hook - fit + 0.2
    front = lambda x: zh - notch_play - (x - (xg - hook)) / tr  # notch front wall, parallel to the hook face
    z_back = zh + hook_flat + 0.4
    notch = [(xt + 0.5, front(xt + 0.5)), (xt - n, front(xt - n)),
             (xt - n, z_back), (xt + 0.5, z_back + (n + 0.5) / tm)]
    A -= _xz_prism(notch, rys[0] - rail_half(xt) - 1, rys[0] + rail_half(xt) + 1)

    if layout == "assembled":
        parts = [A, B]
        if show_unit:
            unit = _box(-body_w / 2, body_w / 2, body_b, body_t, 0, body_d)
            unit += _box(-W, W, 0, H, -plate_t, 0)
            parts.append(unit)
        return Compound(children=parts)

    a = _lay_flat(Rot(0, -90, 0) * A)    # in-use +X becomes print +Z (wall face down)
    b = _lay_flat(B, y_offset=y_top + 10)
    return Compound(children=[a, b])
