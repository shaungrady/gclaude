"""Two-piece hook-over cleat mount for the AC Infinity Controller 2 (AI-ATC).

Concept
  A (wall piece): wall plate (hook-and-loop strips on the cabinet's left wall),
    ceiling flange (one strip on the ceiling), one cleat bar near the top of
    the plate, and a short tab below the plate with a latch recess.
  B (front piece): frame the controller screws to (all 4 screws), shelves, and a
    left web with a pocket that hooks down over the cleat bar. A latch finger
    hangs below B's bottom left corner and clicks into A's recess.

  The cleat bar runs front to back (along Z). Its top face carries the weight;
  its FRONT and BACK ends are 45-degree dovetails (the bar is wider at its top
  than at the plate). B's pocket wraps those ends, so pulling B's top away
  from the wall loads faces whose normals lie in the horizontal XZ plane: no
  component lifts B off the cleat. A horizontal French cleat can't do that
  here: with A printed wall face down, any A face that resists "away from the
  wall" has to be a <=45 degree overhang in X-Y, and that slope pushes B up and
  out (it holds only by friction).

Use
  0. Optional: print layout="fit_test" (B's flat frame) to check the screw
     spacing, and layout="fit_coupon" (bar/pocket pairs at fit 0.12, 0.16,
     0.20; 1, 2, 3 dimples) to pick the cleat fit.
  1. Screw the controller to B on the bench.
  2. Stick A to the cabinet wall and ceiling (strips on the wall face and on top
     of the ceiling flange).
  3. Hold B + controller about 8 mm higher than its final position, push it
     against A (the latch finger presses on A's tab and flexes away from the
     wall), then let it drop 8 mm. The bar slides into the pocket, B lands on
     the bar's top face and the finger clicks into the recess.
  Removal: lift the controller firmly (~15 to 23 N estimated, including its
  weight). The latch's 45-degree face pushes the finger out of the recess.
  Or pull the finger's tip (it sticks out below A) away from the wall and lift.
  Then move B up 8 mm and away from the wall. Leave ~40 mm cable slack.

Load path
  Weight: B's pocket top rests on the bar's top face (gravity seats B, so the
  vertical position is repeatable and the latch sits unloaded with a set gap).
  Twisting moment (controller hangs ~60 mm out from the wall): B's top is pulled
  away from the wall at the bar's dovetail ends; B's bottom pushes into A's
  plate. Front/back pushes: the bar ends (45-degree flanks) in Z.
  The latch only resists lifting B.

Print orientation
  A: wall face down on the smooth sheet (in-use +X up). Bar flanks and the
     ceiling brace are 45-degree overhangs; the latch recess is a pocket in the
     top face.
  B: front face (touches the controller plate) down (in-use +Z up). The latch
     finger stands on the bed and bends within the layers (on edge, best case in
     snap_fits.md section 2). The pocket's back flank and window ceiling are
     45-degree overhangs; its other faces are vertical walls or floors.

Key numbers (joinery docs: refs/joinery/*)
  Cleat flank clearance 0.12 mm normal to each flank (dovetail "locating" fit,
    0.1 to 0.2: interlocking_and_press_fits.md quick reference). The drop is only
    8 mm long so a snug fit is acceptable; tune with fit_coupon.
  X float of B at the cleat: web_gap + fit/sin(45) = 0.15 + 0.17 = 0.32 mm
    [derived, interlocking section 1 formula].
  Latch finger: 18 mm to the hook, 2.2 mm tapered to 1.1 mm, 10 mm wide, hook
    1.2 mm, 45-degree retention face (snap_fits.md: "45 for releasable").
    Strain at 1.2 mm deflection: 1.2 x 2.2 / (1.09 x 18^2) = 0.75% in-layer
    (limit 1.2% repeated PLA [derived table], so it's also fine across
    many cycles). The guard limits hook deflection to ~1.9 mm (1.2%).
    Hook engagement 1.2 mm with B's bottom against the plate (the hanging
    moment holds it there); 0.88 mm worst case with all X float the wrong way
    (snap_fits.md section 4: keep y minus play >= 0.5).
  Retention [derived, snap_fits.md formulas; E = 2.0 GPa, mu 0.3 to 0.5
    unverified]: P = b h^2 E eps / (6 L) = 6.7 N; release
    W = P (mu + tan45)/(1 - mu tan45) = 12 to 20 N, plus the ~3 N weight.

Dimensions: refs/ac_infinity_controller2.md (manufacturer specs, not yet measured).

In-use frame (mm), same as models/controller2_slide_mount.py:
  X = width, centered on the controller; x=-plate_w/2 is the cabinet wall
  Y = up; y=0 is the bottom edge of the controller's front plate
  Z = depth, +Z back into the cabinet; z=0 is B's front face (seated)
layout: "print", "assembled" (children [A, B] or [A, B, controller] with
show_unit=True), "fit_test" (B's flat frame) or "fit_coupon".
"""
import math

from build123d import Box, Compound, Cone, Cylinder, Plane, Polygon, Pos, Rot, extrude, loft


def _box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _zcyl(x, y, d, z0, z1):
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(d / 2, z1 - z0)


def _xy_prism(pts, z0, z1):
    return extrude(Plane.XY.offset(z0) * Polygon(*pts, align=None), amount=z1 - z0, dir=(0, 0, 1))


def _xz_face(pts, y):
    # Plane.XZ maps local (u, v) to global (X, Z); its normal is -Y.
    return Plane.XZ.offset(-y) * Polygon(*pts, align=None)


def _xz_prism(pts, y0, y1):
    return extrude(_xz_face(pts, y0), amount=y1 - y0, dir=(0, 1, 0))


def _lay_flat(shape, x_offset=0.0, y_offset=0.0):
    bb = shape.bounding_box()
    return Pos(-bb.min.X + x_offset, -bb.min.Y + y_offset, -bb.min.Z) * shape


def _beam_shape(s):
    """Deflection at fraction s of a tip-loaded cantilever, relative to the tip."""
    return s * s * (3 - s) / 2


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
    pilot_d: float = 2.6,       # M3 / #4 thread-forming; size to the real screws
    # B (front piece)
    frame_t: float = 4.0,
    boss_d: float = 7.0,
    boss_h: float = 4.0,        # screw bite = frame_t + boss_h
    shelf_t: float = 3.0,
    shelf_tip: float = 8.0,
    b_depth: float = 31.0,      # B's length front to back
    web_t: float = 2.0,         # B's left web below the cleat block
    back_wall: float = 1.7,     # behind the cleat pocket (4 perimeters)
    # Cleat (bar on A, pocket in B)
    cleat_h: float = 3.0,       # bar height out from the wall plate
    cleat_angle: float = 45.0,  # end flank undercut from the plate normal (A's print overhang)
    cleat_z0: float = 8.0,      # bar front end at the plate
    cleat_z1: float = 22.0,     # bar back end at the plate
    cleat_top: float = 67.0,    # bar top face = B's seat
    cleat_len: float = 5.0,     # bar height in Y
    fit: float = 0.12,          # clearance normal to each end flank; tune with fit_coupon
    web_gap: float = 0.15,      # B's web to A's plate, B centered on the bar
    floor_gap: float = 0.35,    # bar top to pocket floor with B pushed against the plate
    window_clear: float = 0.5,  # entry window around the bar head
    lead: float = 2.0,          # window-to-pocket transition (45-degree lead in Y-Z)
    below: float = 0.5,         # narrow pocket runs this far below the seated bar
    drop_margin: float = 0.5,
    # Latch finger (on B) and recess (on A)
    latch_len: float = 18.0,    # root (B's bottom) to the hook's retention face
    latch_t: float = 2.2,       # finger thickness at the root (X)
    latch_tip_t: float = 1.1,   # at the hook (taper to half: snap_fits.md)
    latch_w: float = 10.0,      # finger width (Z), standing on B's print bed
    hook: float = 1.2,          # undercut
    hook_land: float = 0.6,
    ret_angle: float = 45.0,    # retention face: 45 = releasable by lifting
    latch_gap: float = 0.3,     # hook to recess top in Y with B seated and against the plate
    recess_clear: float = 0.4,  # hook tip to recess floor
    root_r: float = 1.2,        # root fillet (0.55 h)
    tail: float = 4.0,          # finger tip below A's tab, for a fingernail
    guard_t: float = 3.0,       # over-travel stop beside the finger
    guard_len: float = 14.0,
    guard_stop: float = 1.9,    # hook deflection at which the finger meets the guard
    # A (wall piece)
    wall_t: float = 3.0,
    depth: float = 100.0,       # wall plate depth (strips are 92 long)
    ceiling_w: float = 25.0,    # ceiling flange width (strip is 19)
    ceiling_t: float = 3.0,
    ceiling_gap: float = 1.0,   # above B's top while B is lifted by the drop
    brace: float = 4.0,         # 45-degree brace under the ceiling flange
    brace_gap: float = 2.0,     # brace starts this far behind B
    a_relief: float = 0.5,      # A starts behind B's front face (controller plate overhangs B)
    tab_d: float = 18.0,        # latch tab front to back
    tab_below: float = 2.0,     # tab material below the recess
    lighten: bool = True,       # windows in the plate between the two wall strips
    lw_y: tuple = (25.0, 56.0),
    lw_rib: float = 6.0,
    coupon_fits: tuple = (0.12, 0.16, 0.20),
    layout: str = "print",
    show_unit: bool = False,
):
    W = plate_w / 2
    H = plate_h
    cy = H / 2
    xa = -W + wall_t                  # A plate inner face
    xb = xa + web_gap                 # B web wall face (B centered)
    x_fl = xb + cleat_h + floor_gap   # pocket floor
    xw = x_fl + back_wall             # B cleat block outer face
    xl = -cut_w / 2
    cut_b, cut_t = cy - cut_h / 2, cy + cut_h / 2
    body_b, body_t = cy - body_h / 2, cy + body_h / 2
    hx, hy = hole_dx / 2, hole_dy / 2
    tf = math.tan(math.radians(cleat_angle))
    cf = math.cos(math.radians(cleat_angle))
    u = cleat_h * tf                  # undercut of each bar end

    # Y layout of the cleat (B seated)
    y_b1, y_b0 = cleat_top, cleat_top - cleat_len
    y_n0 = y_b0 - below               # narrow pocket bottom
    y_w1 = y_n0 - lead                # window top
    drop = y_b1 - (y_w1 - drop_margin)
    y_w0 = y_w1 - cleat_len - 2 * drop_margin
    y_blk = y_w0 - 2.0                # cleat block bottom
    y_ceil0 = H + drop + ceiling_gap
    y_top = y_ceil0 + ceiling_t

    # Pocket and window profiles in X-Z (B frame)
    def narrow_pts(c, grow=0.0):
        fz = c / cf + grow            # grow: extra Z opening at each end (lead-in)
        x0, x1 = xb - 1, x_fl
        f = lambda x: cleat_z0 - (x - xa) * tf - fz
        b = lambda x: cleat_z1 + (x - xa) * tf + fz
        return [(x0, f(x0)), (x1, f(x1)), (x1, b(x1)), (x0, b(x0))]

    wz_f = cleat_z0 - u - window_clear                     # vertical (floor in B's print)
    wz_b = lambda x: cleat_z1 + u + window_clear + (x - xb)  # 45-degree ceiling in B's print

    def window_pts():
        x0, x1 = xb - 1, x_fl
        return [(x0, wz_f), (x1, wz_f), (x1, wz_b(x1)), (x0, wz_b(x0))]

    def bar_pts():
        return [(xa - 0.01, cleat_z0), (xa + cleat_h, cleat_z0 - u),
                (xa + cleat_h, cleat_z1 + u), (xa - 0.01, cleat_z1)]

    # Latch geometry (X-Y, B frame)
    tr = math.tan(math.radians(ret_angle))
    y_r = -latch_len                                # top of the retention face
    dr = hook / tr
    y_hb = y_r - dr - hook_land - hook              # hook bottom (45-degree lower face)
    gn = latch_gap + web_gap / tr                   # Y gap with B centered
    y_rb = y_hb - 0.6                               # recess bottom
    y_tab = y_rb - tab_below                        # A tab bottom
    y_tip = y_tab - tail
    xd = xa - hook - recess_clear                   # recess floor
    th = lambda y: latch_tip_t + (latch_t - latch_tip_t) * (1 + y / latch_len) if y > y_r else latch_tip_t
    # Strain, taper to half: y = 1.09 eps L^2 / h (snap_fits.md); constant: 0.67
    k = 1.09 if latch_tip_t <= 0.55 * latch_t else 0.67
    eps = hook * latch_t / (k * latch_len ** 2)
    eps_stop = eps * guard_stop / hook
    # Guard face: clears the root fillet at the top, stops the finger at guard_stop below
    s_g = guard_len / latch_len
    gi_top = xb + latch_t + root_r + 0.4
    gi_bot = xb + th(-guard_len) + guard_stop * _beam_shape(s_g)

    # ---------------- asserts ----------------
    assert layout in ("print", "assembled", "fit_test", "fit_coupon"), f"unknown layout {layout!r}"
    assert body_w < cut_w and body_h < cut_h, "body must fit the opening"
    assert xw <= xl, f"cleat block ({xw:.2f}) must sit on the frame's left leg ({xl:.2f})"
    assert xw + 1.0 <= -body_w / 2, "cleat block too close to the controller body"
    assert hx + boss_d / 2 <= W and hx - boss_d / 2 > body_w / 2, "right bosses must clear body and edge"
    assert shelf_t < body_b and H - shelf_t > body_t, "shelves hit the body"
    assert cleat_angle <= 45, "bar flanks would overhang more than 45 degrees in A's print"
    assert wz_f >= frame_t, "entry window cuts into the frame"
    # pocket must not reach the top-left boss unless it sits behind it
    assert y_b1 + 1.0 <= cy + hy - boss_d / 2 or wz_f >= frame_t + boss_h, "pocket hits the top-left boss"
    assert wz_b(x_fl) + 1.5 <= b_depth, "window breaks through B's back edge"
    assert narrow_pts(fit)[1][1] >= frame_t - 0.5, "narrow pocket digs too far into the frame"
    assert y_blk > shelf_t + 5, "cleat block runs into the bottom shelf"
    assert cleat_z0 - u >= a_relief + 2, "bar head too close to A's front edge"
    assert depth >= b_depth + brace_gap + 5, "wall plate too short for the ceiling brace"
    assert drop >= cleat_len + below + lead, "drop too short: bar would not leave the narrow pocket"
    # Gravity seating: the bar's top face must reach in front of the controller's CG (~z 9 to 13)
    assert cleat_z0 - u <= 8.0, "bar's bearing face starts behind the controller's center of mass"
    assert eps <= 0.012, f"latch strain {eps:.4f} over the repeated in-layer limit (PLA 1.2%)"
    assert eps_stop <= 0.02, f"latch strain at the guard {eps_stop:.4f} over the one-time limit (2%)"
    assert hook - (web_gap + fit / math.sin(math.radians(cleat_angle))) >= 0.5, "latch engagement < 0.5 after play"
    assert gi_bot - (xb + th(-guard_len)) >= hook * _beam_shape(s_g) + 0.3, "guard touches the finger in normal use"
    assert gi_bot - (xb + th(-guard_len)) >= 0.3 and gi_top - (xb + latch_t + root_r) >= 0.3, "guard slot < 0.3 mm"
    assert gi_top + guard_t <= xl, "guard must hang from the frame's left leg"
    assert latch_tip_t >= 0.9, "finger tip thinner than 2 perimeters"
    assert wall_t - (hook + recess_clear) >= 1.2, "recess leaves too thin a floor in A's tab"
    assert latch_w + 0.5 <= tab_d + a_relief, "tab narrower than the finger"
    assert ret_angle <= 90 and latch_gap > 0

    # ---------------- feature builders ----------------
    def bar(y0, y1):
        return _xz_prism(bar_pts(), y0, y1)

    def pocket(c, y_lo=None):
        """Window + 45-degree transition + narrow pocket, as one cutter."""
        y_lo = y_w0 if y_lo is None else y_lo
        cut = _xz_prism(window_pts(), y_lo, y_w1 + 0.01)
        # Transition: the narrow pocket opening up 45 degrees in Y-Z, clipped to the window.
        # Corresponding edges are parallel, so every face stays planar.
        flare = loft([_xz_face(narrow_pts(c, lead + 0.02), y_w1 - 0.02),
                      _xz_face(narrow_pts(c), y_n0 + 0.01)], ruled=True)
        cut += flare & _xz_prism(window_pts(), y_w1 - 0.01, y_n0 + 0.01)
        cut += _xz_prism(narrow_pts(c), y_n0 - 0.01, y_b1)
        return cut

    if layout == "fit_coupon":
        # Short A plate with the bar, and B blocks with the pocket at each fit
        # (k+1 dimples). Pick the snuggest that drops on freely, set `fit`.
        pieces = []
        z_lo, z_hi = wz_f - 2, wz_b(x_fl) + 2
        for k_, f in enumerate(coupon_fits):
            a = _box(xa - wall_t, xa, y_b0 - 4, y_b1 + 2, z_lo, z_hi) + bar(y_b0, y_b1)
            for i in range(k_ + 1):
                a -= Pos(xa, y_b1 + 1, z_lo + 2 + 2.5 * i) * (Rot(0, 90, 0) * Cylinder(0.6, 1.6))
            blk = _box(xb, xw, y_w0 - 1.5, y_b1 + 3, z_lo, z_hi) - pocket(f)
            for i in range(k_ + 1):
                blk -= _zcyl(xw - 0.9, y_w0 + 1 + 2.5 * i, 1.0, z_hi - 0.8, z_hi + 1)
            pieces.append(_lay_flat(Rot(0, -90, 0) * a, x_offset=0, y_offset=k_ * 32))
            pieces.append(_lay_flat(blk, x_offset=40, y_offset=k_ * 32))
        return Compound(children=pieces)

    # ---------------- B: front piece ----------------
    frame = _box(xb, W, 0, H, 0, frame_t)
    frame -= _box(xl, -xl, cut_b, cut_t, -1, frame_t + 1)
    for sx in (-1, 1):
        for sy in (-1, 1):
            frame -= _zcyl(sx * hx, cy + sy * hy, pilot_d, -1, frame_t + 1)
    if layout == "fit_test":
        return _lay_flat(frame)

    B = frame
    B += _box(xb, xb + web_t, 0, y_blk + 0.01, frame_t - 0.01, b_depth)       # lower web
    B += _box(xb, xw, y_blk, H, frame_t - 0.01, b_depth)                      # cleat block
    shelf = [(xb, frame_t), (W, frame_t), (W, frame_t + shelf_tip), (xw, b_depth), (xb, b_depth)]
    B += _xz_prism(shelf, 0, shelf_t)
    B += _xz_prism(shelf, H - shelf_t, H)
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * hx, cy + sy * hy
            boss = _zcyl(x, y, boss_d, frame_t - 0.01, frame_t + boss_h)
            B += boss & _box(xb, W, 0, H, 0, frame_t + boss_h + 1)
            zp = frame_t + boss_h + 1
            B -= _zcyl(x, y, pilot_d, -1, zp)
            # 90-degree drill point where the pilot ends blind in the web (no flat ceiling)
            B -= Pos(x, y, zp - 0.01 + 0.7) * Cone(pilot_d / 2, 0.15, 1.4)
    B -= pocket(fit)

    # Latch finger: profile in X-Y, standing on B's print bed (z = 0..latch_w)
    fx = xb
    finger = [(fx, 0.01), (fx, y_r), (fx - hook, y_r - dr), (fx - hook, y_r - dr - hook_land),
              (fx, y_hb), (fx, y_tip), (fx + latch_tip_t, y_tip), (fx + latch_tip_t, y_r),
              (fx + latch_t, 0.01)]
    B += _xy_prism(finger, 0, latch_w)
    fil = _box(fx + latch_t - 0.05, fx + latch_t + root_r, -root_r, 0.01, 0, latch_w)
    fil -= _zcyl(fx + latch_t + root_r, -root_r, 2 * root_r, -1, latch_w + 1)
    B += fil
    guard = [(gi_top, 0.01), (gi_top + guard_t, 0.01), (gi_bot + guard_t, -guard_len), (gi_bot, -guard_len)]
    B += _xy_prism(guard, 0, latch_w)

    # ---------------- A: wall piece ----------------
    A = _box(-W, xa, 0, y_top, a_relief, depth)
    A += _box(xa - 0.01, xa + ceiling_w, y_ceil0, y_top, a_relief, depth)
    A += _xy_prism([(xa - 0.01, y_ceil0 - brace), (xa - 0.01, y_ceil0), (xa + brace, y_ceil0)],
                   b_depth + brace_gap, depth)
    A += bar(y_b0, y_b1)
    # Latch tab and recess (recess open at the front; top face parallel to the hook's)
    A += _box(-W, xa, y_tab, 0.01, a_relief, a_relief + tab_d)
    ytop = lambda x: y_r + gn - (fx - x) / tr
    recess = [(xa + 0.01, ytop(xa + 0.01)), (xd, ytop(xd)), (xd, y_rb), (xa + 0.01, y_rb)]
    A -= _xy_prism(recess, -1, latch_w + 0.5)
    if lighten:
        # Three windows between the strip zones (strips at y ~0..20 and ~68..88)
        z0w, z1w = a_relief + 8, depth - 6
        n = 3
        wlen = (z1w - z0w - (n - 1) * lw_rib) / n
        for i in range(n):
            za = z0w + i * (wlen + lw_rib)
            A -= _box(-W - 1, xa + 1, lw_y[0], lw_y[1], za, za + wlen)
        assert lw_y[0] >= 22 and lw_y[1] <= y_b0 - 4, "windows overlap a strip zone or the bar"

    if layout == "assembled":
        parts = [A, B]
        if show_unit:
            unit = _box(-body_w / 2, body_w / 2, body_b, body_t, 0, body_d)
            unit += _box(-W, W, 0, H, -plate_t, 0)
            parts.append(unit)
        return Compound(children=parts)

    a = _lay_flat(Rot(0, -90, 0) * A)            # in-use +X becomes print +Z (wall face down)
    b = _lay_flat(B, x_offset=a.bounding_box().size.X + 8)   # front face down
    return Compound(children=[a, b])
